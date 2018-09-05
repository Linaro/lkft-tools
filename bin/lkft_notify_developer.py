#!/usr/bin/env python3

import argparse
import os
import re
import requests
import sys
from pprint import pprint

sys.path.append(os.path.join(sys.path[0],'../','lib'))
import squad_client

from urllib.parse import urljoin

def get_branch_from_make_kernelversion(make_kernelversion):
    """
        IN: "4.4.118"
        OUT: "4.4"
        IN: "4.9.118-rc1"
        OUT: "4.9"
    """
    pattern = re.compile(r'^(\d+\.\d+).*$')
    match = pattern.match(make_kernelversion)
    return match.group(1)

def get_most_recent_release(builds_url):
    """
        Given a list of builds that is sorted with the newest first,
        return the most recent finished build.
    """

    first_build = None
    for build in squad_client.Builds(builds_url):
        if not first_build:
            first_build = build
        if build['finished']:
            return build

    # If none found, return first build
    return first_build

def get_build_report(build_url):
    build = squad_client.Build(build_url)
    baseline_branch = get_branch_from_make_kernelversion(
            build.build_metadata['make_kernelversion'])

    # Get baseline
    baseline_project_url = squad_client.get_projects_by_branch()[baseline_branch]
    baseline_builds_url = urljoin(baseline_project_url, "builds")
    baseline_build = get_most_recent_release(baseline_builds_url)

    template_url = urljoin(build_url, 'email')
    parameters = {
        'baseline': baseline_build['id'],
        'template': '9',
        }
    result = requests.get(template_url, parameters)

    return result.text

if __name__ == "__main__":

    # Given a build, generate an email notification using a production baseline.
    #build_url = "https://qa-reports.linaro.org/api/builds/9143/"
    #build_url = "https://qa-reports.linaro.org/api/builds/9141/"

    parser = argparse.ArgumentParser()
    parser.add_argument("build_url", help="API URL to developer build")
    args = parser.parse_args()
    print(get_build_report(args.build_url))
