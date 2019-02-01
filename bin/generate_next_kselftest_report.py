#!/usr/bin/env python3

import argparse
import os
import requests
import sys
import time

sys.path.append(os.path.join(sys.path[0], "../", "lib"))
import squad_client

project_url = "https://qa-reports.linaro.org/api/projects/6/" # linux-next-oe
template_id = "12" # kselftest-specific template

def get_build_report(
    project_url, unfinished=False, build_id=None, force_report=False, timeout=120
):
    """ Given a project URL, return a test report """

    report = ""

    builds_url = project_url+"builds"
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

    template_url = build_result["url"] + "report?template={}".format(template_id)
    if force_report:
        # Don't return cached report - force the generation of a new one
        template_url = template_url + "&force=1"

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
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--unfinished", help="Report even if build is unfinished'", action="store_true"
    )
    parser.add_argument("--build", help="Use build ID instead of latest")
    parser.add_argument(
        "--force-report",
        action="store_true",
        default=False,
        help="Force a report regeneration from qa-reports",
    )
    args = parser.parse_args()

    unfinished = args.unfinished
    build_id = args.build
    force_report = args.force_report

    report = ""
    report = get_build_report(
        project_url,
        unfinished=unfinished,
        build_id=build_id,
        force_report=force_report,
    )

    print(report)
