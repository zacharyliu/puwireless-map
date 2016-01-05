import csv
import requests
from bs4 import BeautifulSoup

r = requests.get("https://mrtg.net.princeton.edu/cgi-bin/mrtg.active/core-87.switch.bps?interval=86400")
soup = BeautifulSoup(r.content, "html.parser")
raw_data = [[x.get_text() for x in row] for row in soup.find("table").find_all("tr")[1::]]
data = [{"in": row[4], "out": row[5], "interface": row[6]} for row in raw_data]

with open("bandwidth.csv", "wb") as csvfile:
  writer = csv.DictWriter(csvfile, fieldnames=["interface", "in", "out"])

  writer.writeheader()
  for row in data:
    writer.writerow(row)
