#!/usr/bin/env python3

import argparse
import os
import re
import requests
import sys
import time
from urllib.parse import urljoin

sys.path.append(os.path.join(sys.path[0], "../", "lib"))
import squad_client  # noqa: E402


def extract_version_info(version):
    """
        IN: version="v4.18.4-23-gc456dc1ec5f9"
        OUT: (4, 18, 4, 23, gc456dc1ec5f9)

        IN: version="v4.18.4"
        OUT: (4, 18, 4, None, None)
    """
    pattern = re.compile(r"v(\d+)\.(\d+)\.(\d+)-?(\d+)?-?(\w+)?")
    match = pattern.match(version)
    return (
        match.group(1),
        match.group(2),
        match.group(3),
        match.group(4),
        match.group(5),
    )


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
    (
        current_major,
        current_minor,
        current_patch,
        current_patch_count,
        current_sha,
    ) = extract_version_info(build_result["version"])

    # Current version is a release tag if current_patch is None
    current_is_release = current_patch_count is None

    # Find the previous release, or, where patch number decriments in the event
    # there was not a tagged release.
    for build in squad_client.Builds(builds_url):
        (
            build_major,
            build_minor,
            build_patch,
            build_patch_count,
            build_sha,
        ) = extract_version_info(build["version"])
        if build_patch_count is None:
            # Release version is found
            return build["id"]
        elif current_is_release and int(build_patch) == int(current_patch) - 2:
            return build["id"]
        elif (not current_is_release) and int(build_patch) == int(current_patch) - 1:
            return build["id"]

    sys.exit("Baseline not found")


def get_build_report(
    project_url,
    unfinished=False,
    baseline=None,
    build_id=None,
    force_report=False,
    timeout=120,
):
    """ Given a project URL, return a test report """

    report = ""

    builds_url = urljoin(project_url, "builds")
    build_result = None
    for build in squad_client.Builds(builds_url):
        if not build_id:
            build_result = build
            break

        if int(build["id"]) == int(build_id):
            build_result = build
            break
    else:
        sys.exit("Build {} not found".format(build_id))

    r = requests.get(build_result["status"])
    r.raise_for_status()
    status = r.json()
    if not (status.get("finished", None) or unfinished):
        sys.exit(
            "ERROR: Build {}({}) not yet Finished. Pass --unfinished to force a report.".format(
                build_result["id"], build_result["version"]
            )
        )

    template_url = build_result["url"] + "report?template=9"
    if force_report:
        # Don't return cached report - force the generation of a new one
        template_url = template_url + "&force=1"
    if baseline:
        template_url = template_url + "&baseline={}".format(baseline)
    else:
        try:
            baseline = detect_baseline(build_result, builds_url)
            template_url = template_url + "&baseline={}".format(baseline)
        except AttributeError:
            # hikey doesn't work with detect_baseline; the regex match
            # will fail
            pass

    r = requests.get(template_url)
    r.raise_for_status()
    callback_url = r.json()["url"]
    report = ""
    for i in range(1, timeout):
        r = requests.get(callback_url)
        r.raise_for_status()
        if r.json()["status_code"] is None:
            time.sleep(1)
            continue
        if r.json()["status_code"] != 200:
            sys.exit("ERROR generating report: {}".format(r.json()["error_message"]))
        report = r.json()["output_text"]
        break
    else:
        sys.exit("ERROR: Waiting timeout exceeded, try again later.")

    return report


if __name__ == "__main__":
    # List of possible branches.
    # To add a branch, navigate in browser to
    # https://qa-reports.linaro.org/api/projects/.
    projects = squad_client.get_projects_by_branch()
    available_branches = projects.keys()
    # 4.4-hikey is automatically included when 4.4 is used. Remove it
    # for purposes of usage.
    branch_help = (
        "[" + "|".join([x for x in available_branches if x != "4.4-hikey"]) + "]"
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("branch", help=branch_help)
    parser.add_argument(
        "--force-good", help="Force report of 'no regressions'", action="store_true"
    )
    parser.add_argument(
        "--unfinished", help="Report even if build is unfinished'", action="store_true"
    )
    parser.add_argument("--baseline", help="Use build ID as baseline")
    parser.add_argument("--build", help="Use build ID instead of latest")
    parser.add_argument(
        "--force-report",
        action="store_true",
        default=False,
        help="Force a report regeneration from qa-reports",
    )
    args = parser.parse_args()

    force_good = args.force_good
    unfinished = args.unfinished
    baseline = args.baseline
    build_id = args.build
    branch = args.branch
    force_report = args.force_report
    if branch not in available_branches:
        sys.exit("Invalid branch specified")

    report = ""
    report = get_build_report(
        projects[branch],
        unfinished=unfinished,
        baseline=baseline,
        build_id=build_id,
        force_report=force_report,
    )

    if branch == "4.4":

        # In the case of 4.4, also get 4.4-hikey

        # Remove the last 3 line (sig) if there are more reports
        # coming
        report = "\n".join(report.split("\n")[:-3]) + "\n"

        report += get_build_report(
            projects["4.4-hikey"],
            unfinished=unfinished,
            baseline=baseline,
            build_id=build_id,
            force_report=force_report,
        )

    if "Regressions" not in report or force_good:
        report = (
            """Results from Linaro’s test farm.
No regressions on arm64, arm, x86_64, and i386.

"""
            + report
        )
    else:
        report = (
            """Results from Linaro’s test farm.
Regressions detected.

"""
            + report
        )

    print(report)
