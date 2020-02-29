import sys
import csv

fcp = []
lcp = []

file_name = sys.argv[1]
with open(file_name) as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  line_count = 0
  for row in csv_reader:
    event = row[0]
    value = int(row[1])
    if event == "FCP":
      fcp.append(value)
    elif event == "LCP":
      lcp.append(value)

  fcp_average = sum(fcp) / len(fcp)
  lcp_average = sum(lcp) / len(lcp)
  print("FCP (avg):", fcp_average)
  print("LCP (avg):", lcp_average)
