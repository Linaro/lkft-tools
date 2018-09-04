#!/usr/bin/env python3

import argparse
import os
import re
import requests
import sys

sys.path.append(os.path.join(sys.path[0],'../','lib'))
import squad_client

def extract_version_info(version):
    """
        IN: version="v4.18.4-23-gc456dc1ec5f9"
        OUT: (4, 18, 4, 23, gc456dc1ec5f9)

        IN: version="v4.18.4"
        OUT: (4, 18, 4, None, None)
    """
    pattern = re.compile(r'v(\d+)\.(\d+)\.(\d+)-?(\d+)?-?(\w+)?')
    match = pattern.match(version)
    return(match.group(1), match.group(2), match.group(3),
           match.group(4), match.group(5))

def detect_baseline(build_result, builds_url):
    """
        Given a build and a build url, find the baseline

        The baseline is found by looking at the 'version' field in
        build_result, and looking through previous builds such that:

        Given the following list of versions:
            v4.18.5
            v4.18.4-23-gc456dc1ec5f9
            v4.18.4-13-g2a9a12ddb3b0
            v4.18.4-7-ga00ca2e5e60b
            v4.18.3-36-g28b2837b7236
            v4.18.3-36-g1b2dc862d5f3
            v4.18.3

        The following IN -> OUT should be returned:
            v4.18.5 -> v4.18.3-36-g28b2837b7236
            v4.18.4-23-gc456dc1ec5f9 -> v4.18.3-36-g28b2837b7236
            v4.18.3-36-g28b2837b7236 -> v4.18.3

    """
    (current_major, current_minor, current_patch, current_patch_count, current_sha) = extract_version_info(build_result['version'])

    # Current version is a release tag if current_patch is None
    current_is_release = current_patch_count is None

    # Find the previous release, or, where patch number decriments in the event
    # there was not a tagged release.
    r = requests.get(builds_url)
    for build in r.json()['results'][1:]:
        (build_major, build_minor, build_patch, build_patch_count, build_sha) = extract_version_info(build['version'])
        if build_patch_count is None:
            # Release version is found
            return build['id']
        elif current_is_release and int(build_patch) == int(current_patch)-2:
            return build['id']
        elif (not current_is_release) and int(build_patch) == int(current_patch)-1:
            return build['id']

    sys.exit("Baseline not found")


if __name__ == "__main__":
    # List of possible branches.
    # To add a branch, navigate in browser to
    # https://qa-reports.linaro.org/api/projects/.
    branches = squad_client.get_branches()
    branch_help = '['+'|'.join(branches.keys())+']'

    parser = argparse.ArgumentParser()
    parser.add_argument("branch", help=branch_help)
    parser.add_argument("--force-good",
        help="Force report of 'no regressions'",
        action="store_true")
    parser.add_argument("--unfinished",
        help="Report even if build is unfinished'",
        action="store_true")
    parser.add_argument("--baseline",
        help="Use build ID as baseline")
    parser.add_argument("--build",
        help="Use build ID instead of latest")
    args = parser.parse_args()

    force_good = args.force_good
    unfinished = args.unfinished
    baseline = args.baseline
    build = args.build
    branch = args.branch
    if branch not in branches:
        sys.exit("Invalid branch specified")

    report = ""
    no_regressions = True
    for i, url in enumerate(branches[branch]):

        builds_url = url+'builds'
        r = requests.get(builds_url)
        if build:
            for build_result in r.json()['results']:
                if int(build_result['id']) == int(build):
                    break
            else:
                sys.exit("Build {} not found".format(build))
        else:
            build_result = r.json()['results'][0]

        # Check status, make sure it is finished
        r = requests.get(build_result['status'])
        status = r.json()
        if not (status['finished'] or unfinished):
            sys.exit( "ERROR: Build {}({}) not yet Finished. Pass --unfinished to force a report.".format(build_result['id'], build_result['version']))

        template_url = build_result['url']+'email?template=9'
        if baseline:
            template_url = template_url+"&baseline={}".format(baseline)
        else:
            try:
                baseline = detect_baseline(build_result, builds_url)
                template_url = template_url+"&baseline={}".format(baseline)
            except AttributeError:
                # hikey doesn't work with detect_baseline; the regex match
                # will fail
                pass

        r = requests.get(template_url)
        text = r.text
        if "Regressions" in text:
            no_regressions = False

        if len(branches[branch]) > 1 and i != len(branches[branch])-1:
            # Remove the last 3 line (sig) if there are more reports
            # coming
            text = '\n'.join(text.split('\n')[:-3]) + "\n"
        report += text

    if no_regressions or force_good:
        report = (
"""Results from Linaro’s test farm.
No regressions on arm64, arm, x86_64, and i386.

""" + report)
    else:
        report = (
"""Results from Linaro’s test farm.
Regressions detected.

""" + report)

    print(report)

