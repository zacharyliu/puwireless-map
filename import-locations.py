import csv
import requests
import re
from bs4 import BeautifulSoup

regex = re.compile(r"<h4>([^<]*?)<")

with open("core-87.csv") as infile, open("core-87-locations.csv", "wb") as outfile:
  reader = csv.reader(infile)
  writer = csv.DictWriter(outfile, fieldnames=["interface", "name", "lat", "lon"])

  writer.writeheader()

  for row in reader:
    interface = row[0]
    row = {"interface": interface}
    print "Interface: " + interface

    # Run only on Holder Hall (for testing)
    # if interface != "core-87-4-19":
    #   continue

    url = "https://mrtg.net.princeton.edu/fcgi/mrtg-rrd/" + interface + ".html"
    r = requests.get(url)
    search = regex.search(r.text)

    if search is not None:
      name = search.group(1)
      row["name"] = name
      print name

      print "Name: " + name
      payload = {"q": name, "v": "2", "provider": "esri", "group": "princeton", "projection": "900913"}
      r = requests.get("http://m.princeton.edu/rest/map/search", params=payload)
      results = r.json()["response"]["results"]

      print "Results: " + str(len(results))
      if len(results) > 0:
        row["lat"] = sum([x["attribs"]["lat"] for x in results]) / float(len(results))
        row["lon"] = sum([x["attribs"]["lon"] for x in results]) / float(len(results))
    
    writer.writerow(row)
