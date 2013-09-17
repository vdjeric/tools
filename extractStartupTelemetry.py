#!/bin/env python
import os
import sys
import json
import stat

if len(sys.argv) != 2:
  print "Usage: extractStartupTelemetry.py <Telemetry pings directory> > outFile.csv"
  sys.exit(2)

# Read all Telemetry payload files in directory
telemetryPings = []
for filename in os.listdir(sys.argv[1]):
  path = sys.argv[1] + os.sep + filename
  mtime = os.stat(path)[stat.ST_MTIME]
  file = open(path, "r")
  rawData = file.read()
  data = json.loads(rawData)
  telemetryPings.append((mtime, data["payload"]["simpleMeasurements"]))

# Present the data chronologically
sortedPings = sorted(telemetryPings)

milestones = ["start", "main", "startupCrashDetectionBegin",
              "AMI_startup_begin", "AMI_startup_end", "createTopLevelWindow",
              "firstPaint", "sessionRestoreInitialized",
              "delayedStartupFinished", "sessionRestored", "firstLoadURI"]

print ",".join(milestones)

for (mtime, ping) in sortedPings:
  row = ""
  for mstone in milestones:
    if mstone not in ping:
      row += "-1,"
      continue
    row += str(ping[mstone]) + ","
  print row

