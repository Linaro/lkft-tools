#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Generate a report for the purposes of jipdate status (for JIRA).

    Example usage:
        $ generate_lkft_tested_report.py 2019-1-1
        Ran 1171533 tests on 67 kernel versions on branch stable v4.4.y on OE since 2019-01-01.
        Ran 176266 tests on 60 kernel versions on branch linaro-hikey-stable v4.4.y on OE since 2019-01-01.
        Ran 1675279 tests on 77 kernel versions on branch stable v4.9.y on OE since 2019-01-01.
        Ran 1629238 tests on 73 kernel versions on branch stable v.4.14.y on OE since 2019-01-01.
        Ran 0 tests on 0 kernel versions on branch stable v4.17.y on OE since 2019-01-01.
        Ran 0 tests on 0 kernel versions on branch stable v4.18.y on OE since 2019-01-01.
        Ran 1561418 tests on 76 kernel versions on branch stable v4.19.y on OE since 2019-01-01.
        Ran 1099805 tests on 55 kernel versions on branch stable v4.20.y on OE since 2019-01-01.
        Ran 633531 tests on 29 kernel versions on branch stable v5.0.y on OE since 2019-01-01.
        Ran 5262469 tests on 250 kernel versions on branch mainline on OE since 2019-01-01.
        Ran 1182150 tests on 69 kernel versions on branch next on OE since 2019-01-01.
        Ran 14391689 total tests on 756 kernel versions in 96841 LAVA jobs since 2019-01-01.

"""

import argparse
import datetime
import os
import sys
from urllib.parse import urljoin

sys.path.append(os.path.join(sys.path[0], "../", "lib"))
import lkft_squad_client  # noqa: E402


def get_test_count(builds):
    test_count = 0
    test_run_count = 0
    for build in builds:
        status = lkft_squad_client.get_objects(build["status"], limit=1)
        test_run_count += status.get("test_runs_total", 0)
        test_count += (
            status["tests_pass"] + status["tests_fail"] + status["tests_xfail"]
        )
    return {"test_count": test_count, "test_run_count": test_run_count}


def get_project_name(project_url):
    """ Given a squad project url, return the project name """
    return lkft_squad_client.get_objects(project_url, limit=1)["name"]


def valid_date_type(arg_date_str):
    """custom argparse *date* type for user dates values given from the command line"""
    try:
        return datetime.datetime.strptime(arg_date_str, "%Y-%m-%d")
    except Exception:
        print(
            "Given Date ({0}) not valid! Expected format, YYYY-MM-DD!".format(
                arg_date_str
            )
        )
        sys.exit(1)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Generate report of branches tested recently"
    )
    parser.add_argument(
        dest="date",
        type=valid_date_type,
        help='Report on builds that occured since date given (inclusive) "YYYY-MM-DD"',
    )
    args = parser.parse_args()
    date = args.date

    branches = lkft_squad_client.get_projects_by_branch()

    test_count_total = 0
    test_run_total = 0
    build_count_total = 0
    for branch, branch_url in branches.items():
        builds_url = urljoin(branch_url, "builds")
        builds_to_report = []
        for build in lkft_squad_client.Builds(builds_url):
            if date > datetime.datetime.strptime(
                build["datetime"], "%Y-%m-%dT%H:%M:%S.%fZ"
            ):
                break
            builds_to_report.append(build)
        test_counts = get_test_count(builds_to_report)
        test_count_total += test_counts["test_count"]
        test_run_total += test_counts["test_run_count"]
        build_count_total += len(builds_to_report)
        print(
            "Ran {} tests on {} kernel versions on branch {} since {}.".format(
                test_counts["test_count"],
                len(builds_to_report),
                get_project_name(branch_url),
                date.strftime("%Y-%m-%d"),
            )
        )

    print(
        "Ran {} total tests on {} kernel versions in {} LAVA jobs since {}.".format(
            test_count_total,
            build_count_total,
            test_run_total,
            date.strftime("%Y-%m-%d"),
        )
    )
