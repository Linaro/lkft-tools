#!/bin/env python3

import requests
import sys

def usage():
    print("{} [4.4|4.9|4.14|4.16]".format(sys.argv[0]))
    sys.exit(1)

if len(sys.argv) < 2:
    usage()
branch = sys.argv[1]
if branch not in ['4.4', '4.9', '4.14', '4.16']:
    usage()

branches = {
    '4.4': [
        'https://qa-reports.linaro.org/api/projects/40/',
        'https://qa-reports.linaro.org/api/projects/34/',
    ],
    '4.9': ['https://qa-reports.linaro.org/api/projects/23/'],
    '4.14': ['https://qa-reports.linaro.org/api/projects/58/'],
    '4.16': ['https://qa-reports.linaro.org/api/projects/101/'],

}

report = ""
no_regressions = True
for i, url in enumerate(branches[branch]):
    r = requests.get(url+'builds')
    result = r.json()['results'][0]

    # Check status, make sure it is finished
    r = requests.get(result['status'])
    status = r.json()
    assert status['finished'], "ERROR: Build {} not yet Finished".format(url)

    r = requests.get(result['url']+'email?template=9')
    text = r.text
    if "Regressions" in text:
        no_regressions = False

    if len(branches[branch]) > 1 and i != len(branches[branch])-1:
        # Remove the last 3 line (sig) if there are more reports
        # coming
        text = '\n'.join(text.split('\n')[:-3])
    report += text

if no_regressions:
    report = (
"""Results from Linaro’s test farm.
No regressions on arm64, arm and x86_64.

""" + report)
else:
    report = (
"""Results from Linaro’s test farm.
Regressions detected.

""" + report)

print(report)

