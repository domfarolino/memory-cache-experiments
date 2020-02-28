import sys
import csv

url_buckets = {} # Map {url: {kLoad: N, kUse: N, kReload: N, kRevalidate: N 

def IsHistogramEvent(event):
  base = "RevalidationPolicy.AsyncScript."
  return (event == base + "kUse") or (event == base + "kLoad") or (event == base + "kReload") or (event == base + "kRevalidate")

def PossiblyTruncateUrl(url):
  return url[:50] + (url[50:] and '...')

def InitializeMap():
  return {"RevalidationPolicy.AsyncScript.kUse": 0, "RevalidationPolicy.AsyncScript.kLoad": 0, "RevalidationPolicy.AsyncScript.kReload": 0, "RevalidationPolicy.AsyncScript.kRevalidate": 0, "LOAD": 0, "DESTROY": 0}

file_name = sys.argv[1]
with open(file_name) as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  line_count = 0
  for row in csv_reader:
    event = row[0]
    if IsHistogramEvent(event):
      url = row[1]

      if url not in url_buckets:
        url_buckets[url] = InitializeMap()

      url_buckets[url][event] += 1

    line_count += 1

  url_buckets = {k: v for k, v in sorted(url_buckets.items(), key=lambda item: sum(item[1].values()), reverse=True)}
  print("URL,kUse,kLoad,kReload,kRevalidate")
  for item in url_buckets.items():
    print(PossiblyTruncateUrl(item[0]),
          item[1]["RevalidationPolicy.AsyncScript.kUse"],
          item[1]["RevalidationPolicy.AsyncScript.kLoad"],
          item[1]["RevalidationPolicy.AsyncScript.kReload"],
          item[1]["RevalidationPolicy.AsyncScript.kRevalidate"], sep=",")
