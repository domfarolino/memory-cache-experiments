import matplotlib.pyplot as plt
import numpy as np
import sys
import csv

###########################################

# [HISTOGRAM]: Data for HISTOGRAM event.
async_script_histogram_data = {"kLoad": 0, "kUse": 0, "kReload": 0, "kRevalidate": 0}

def PlotRevalidationPolicyHistogramData():
  x_name = async_script_histogram_data.keys()
  y = async_script_histogram_data.values()
  x = np.arange(len(x_name))
  plt.bar(x, y)
  plt.xticks(x, x_name)

  plt.suptitle('RevalidationPolicy.Async Histogram', fontsize=18)
  plt.xlabel('RevalidationPolicy', fontsize=16)
  plt.ylabel('Occurrences', fontsize=16)
  plt.show()
  print(async_script_histogram_data)

###########################################

# [LOAD]: Data for LOAD event.

# A map of all {async_script: request_count}.
async_script_request_map = {}

def PopulateAsyncScriptRequestMap(row):
  is_async_script = (row[1] == "Script" and row[3] == "1")
  if not is_async_script:
    return

  # This row represents an async script.
  url = row[2]
  if url not in async_script_request_map:
    async_script_request_map[url] = 1
  else:
    async_script_request_map[url] += 1

def PlotAsyncScriptRequestCountHistogram():
  # First turn |async_script_request_map| into a map of {request_count: num_urls}.
  request_count_map = {}
  for val in async_script_request_map.values():
    if val not in request_count_map:
      request_count_map[val] = 1
    else:
      request_count_map[val] += 1

  x_name = request_count_map.keys()
  y = request_count_map.values()
  x = np.arange(len(x_name))
  plt.bar(x, y)
  plt.xticks(x, x_name)

  plt.suptitle('Async Script Request Count', fontsize=18)
  plt.xlabel('Request count', fontsize=16)
  plt.ylabel('Number of scripts', fontsize=16)
  plt.show()

  print(request_count_map)

###########################################

# [DESTROY]: Data for DESTROY event.
async_script_destroy_map = {}

def PopulateAsyncScriptDestroyMap(row):
  is_async_script = (row[1] == "Script" and row[3] == "1")
  if not is_async_script:
    return

  # This row represents an async script.
  url = row[2]
  if url not in async_script_destroy_map:
    async_script_destroy_map[url] = 1
  else:
    async_script_destroy_map[url] += 1

def PlotAsyncScriptDestroyCountHistogram():
  # First turn |async_script_request_map| into a map of {request_count: num_urls}.
  destroy_occurrence_map = {}
  for val in async_script_destroy_map.values():
    if val not in destroy_occurrence_map:
      destroy_occurrence_map[val] = 1
    else:
      destroy_occurrence_map[val] += 1

  x_name = destroy_occurrence_map.keys()
  y = destroy_occurrence_map.values()
  x = np.arange(len(x_name))
  plt.bar(x, y)
  plt.xticks(x, x_name)

  plt.suptitle('Async Script Destroy Count', fontsize=18)
  plt.xlabel('Destroy count', fontsize=16)
  plt.ylabel('Number of scripts', fontsize=16)
  plt.show()

  print(destroy_occurrence_map)

###########################################

# [LOAD/FCP]: Data for requests types loaded before FCP.

is_loading_pre_fcp = True
pre_fcp_request_types = [] # [Script, Font, Manifest, etc].

def RecordPreFCPRequestType(request_type):
  if is_loading_pre_fcp == False:
    return

  # This LOAD event happened after the last LCP and before the next FCP.
  # This is because LCP is recorded when you navigate away from the previous
  # page.

  # TODO(domfarolino): Distinguish between Script and AsyncScript.
  pre_fcp_request_types.append(request_type)

def PlotPreFCPRequestTypeHistogram():
  request_occurrence_map = {} # {RequestType: occurrence}.
  for request_type in pre_fcp_request_types:
    if request_type not in request_occurrence_map:
      request_occurrence_map[request_type] = 1
    else:
      request_occurrence_map[request_type] += 1

  x_name = request_occurrence_map.keys()
  y = request_occurrence_map.values()
  x = np.arange(len(x_name))
  plt.bar(x, y)
  plt.xticks(x, x_name)

  plt.suptitle('Pre-FCP RequestType Load Histogram', fontsize=18)
  plt.xlabel('RequestType', fontsize=16)
  plt.ylabel('Load Count (before FCP)', fontsize=16)
  plt.show()

  print(request_occurrence_map)

###########################################

# [FCP/LCP]: Data for FCP & LCP events.

fcp_times = []
lcp_times = []

def PrintFCPLCP():
  print "FCP:"
  print "  50%:", np.percentile(fcp_times, 50)
  print "  75%:", np.percentile(fcp_times, 75)
  print "LCP:"
  print "  50%:", np.percentile(lcp_times, 50)
  print "  75%:", np.percentile(lcp_times, 75)

###########################################

def PossiblyTruncateUrl(url):
  return url[:50] + (url[50:] and '...')

file_name = sys.argv[1]
with open(file_name) as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  for row in csv_reader:
    # Find what event we're currently reading.
    event = row[0]

    if event == "HISTOGRAM":
      hist_name = row[1] # Throw this away for now, since there is only one histogram.
      revalidation_policy = row[2]
      async_script_histogram_data[revalidation_policy] += 1
    elif event == "LOAD":
      # First populate some |async_script_request_map| if necessary.
      PopulateAsyncScriptRequestMap(row)
      resource_type = row[1]
      RecordPreFCPRequestType(resource_type)
    elif event == "DESTROY":
      PopulateAsyncScriptDestroyMap(row)
    elif event == "FCP":
      is_loading_pre_fcp = False
      fcp_time = float(row[1])
      fcp_times.append(fcp_time)
    elif event == "LCP":
      is_loading_pre_fcp = True
      lcp_time = float(row[1])
      lcp_times.append(lcp_time)

  PlotRevalidationPolicyHistogramData()
  PlotAsyncScriptRequestCountHistogram()
  PlotAsyncScriptDestroyCountHistogram()
  PlotPreFCPRequestTypeHistogram()
  PrintFCPLCP()
