#!/usr/bin/env python3

"""
    Generate a report for the purposes of jipdate status (for JIRA).

    Example usage:
        drue@xps:~/src/lkft-tools/bin$ ./generate_lkft_tested_report.py 7
        Ran 55358 tests on 3 builds on branch stable v4.4.y on OE in the last 7 days.
        Ran 11272 tests on 4 builds on branch linaro-hikey-stable v4.4.y on OE in the last 7 days.
        Ran 140220 tests on 6 builds on branch stable v4.9.y on OE in the last 7 days.
        Ran 137020 tests on 6 builds on branch stable v.4.14.y on OE in the last 7 days.
        Ran 113883 tests on 6 builds on branch stable v4.19.y on OE in the last 7 days.
        Ran 94965 tests on 6 builds on branch stable v4.20.y on OE in the last 7 days.
        Ran 96258 tests on 5 builds on branch stable v5.0.y on OE in the last 7 days.
        Ran 373652 tests on 22 builds on branch mainline on OE in the last 7 days.
        Ran 0 tests on 0 builds on branch next on OE in the last 7 days.

"""

import argparse
import datetime
import os
import sys

sys.path.append(os.path.join(sys.path[0], "../", "lib"))
import squad_client

from urllib.parse import urljoin


def get_test_count(days, builds):
    test_count = 0
    for build in builds:
        status = squad_client.get_objects(build["status"], expect_one=True)
        test_count += (
            status["tests_pass"] + status["tests_fail"] + status["tests_xfail"]
        )
    return test_count


def get_project_name(project_url):
    """ Given a squad project url, return the project name """
    return squad_client.get_objects(project_url, expect_one=True)["name"]


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Generate report of branches tested recently"
    )
    parser.add_argument(
        "days", help="Report on builds that occured in the last number of days"
    )
    args = parser.parse_args()
    days = args.days

    branches = squad_client.get_projects_by_branch()

    test_count_total = 0
    build_count_total = 0
    for branch, branch_url in branches.items():
        builds_url = urljoin(branch_url, "builds")
        builds_to_report = []
        for build in squad_client.Builds(builds_url):
            if datetime.datetime.utcnow() - datetime.timedelta(
                days=int(days)
            ) > datetime.datetime.strptime(build["datetime"], "%Y-%m-%dT%H:%M:%S.%fZ"):
                break
            builds_to_report.append(build)
        test_count = get_test_count(days, builds_to_report)
        test_count_total += test_count
        build_count_total += len(builds_to_report)
        print(
            "Ran {} tests on {} builds on branch {} in the last {} days.".format(
                test_count, len(builds_to_report), get_project_name(branch_url), days
            )
        )

    print(
        "Ran {} total tests on {} builds in the last {} days.".format(
            test_count_total, build_count_total, days
        )
    )
