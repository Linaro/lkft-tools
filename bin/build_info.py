#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import ast
import os
import sys

import requests

sys.path.append(os.path.join(sys.path[0], "../", "lib"))
import lkft_squad_client  # noqa: E402


def print_build_info(url, build):
    print("URL: %s" % url)
    print("ID: %s" % build["id"])
    print("Version: %s" % build["version"])
    print("Project URL: %s" % build["project"])
    print("Date: %s" % build["created_at"])
    print("Finished: %s" % build["finished"])


def print_build_info_row(build):
    finished = "Finished"
    if not build["finished"]:
        finished = "Running"

    print(
        "%6d %-40s %-8s %s"
        % (build["id"], build["version"], finished, build["created_at"])
    )


def get_testjob_status(testjob):
    status = "unknown"
    submitted = testjob["submitted"]
    fetched = testjob["fetched"]
    if "job_status" in testjob:
        if testjob["job_status"] == "Complete":
            status = "complete"
        elif testjob["job_status"] == "Incomplete":
            status = "incomplete"
        elif testjob["job_status"] == "Canceled":
            status = "canceled"
    if not submitted:
        status = "unsubmitted"
    if not fetched:
        status = "unfetched"
    return status


def format_test_job(testjob):
    status = get_testjob_status(testjob)

    completed = False
    if "completed" in testjob:
        completed = True

    return status, completed


def get_testjob_lavajob_id(testjob):
    split_lavajob_id = testjob["external_url"].split("/")
    lavajob_id = split_lavajob_id[-1]
    return lavajob_id


def save_testjob_log(testjob):
    lavajob_id = get_testjob_lavajob_id(testjob)
    name = testjob["name"]
    url = testjob["testrun"]

    filename = lavajob_id + "-" + name + ".log"
    handle = open(filename, "w")
    response = requests.get(url + "log_file/")
    if response.status_code == 200:
        handle.write(response.text)
    handle.close()


def get_failure_reason(testjob):
    failure = testjob["failure"]
    failure_dict = ast.literal_eval(failure)
    if "error_msg" in failure_dict:
        reason = failure_dict["error_msg"]
    else:
        reason = "<Unknown>"
    # Just first line
    reason = reason.split("\n", 1)[0]
    return reason


def print_test_jobs(build):
    testruns = {}
    testruns["complete"] = []
    testruns["incomplete"] = []
    testruns["canceled"] = []
    testruns["unfetched"] = []
    testruns["unsubmitted"] = []
    testruns["unknown"] = []
    base_url = build["testjobs"]
    try:
        # testruns_info = lkft_squad_client.get_objects(base_url, params)[0]
        testruns_list = lkft_squad_client.get_objects(base_url)
    except Exception:
        exit("Error: not found at {}".format(base_url))

    # Get list of testruns for that group/project

    for testrun in testruns_list:
        status = get_testjob_status(testrun)
        testruns[status].append(testrun)

    print("#" * len(testruns["complete"]), end="")
    print("X" * len(testruns["incomplete"]), end="")
    print("c" * len(testruns["canceled"]), end="")
    print("-" * len(testruns["unfetched"]), end="")
    print("." * len(testruns["unsubmitted"]), end="")
    print("?" * len(testruns["unknown"]), end="")
    print("")
    print(
        "Total:       %8d"
        % (
            len(testruns["complete"])
            + len(testruns["incomplete"])
            + len(testruns["canceled"])
            + len(testruns["unfetched"])
            + len(testruns["unsubmitted"])
            + len(testruns["unknown"])
        )
    )
    print("Complete:    %8d" % len(testruns["complete"]))
    print("Incomplete:  %8d" % len(testruns["incomplete"]))
    print("Canceled:    %8d" % len(testruns["canceled"]))
    print("Unfetched:   %8d" % len(testruns["unfetched"]))
    print("Unsubmitted: %8d" % len(testruns["unsubmitted"]))
    print("Unknown:     %8d" % len(testruns["unknown"]))
    # for category in ["complete", "incomplete", "unfetched", "unsubmitted"]:
    #     for testrun in testruns[category]:
    #         print("{}".format(testrun), end="")

    print()

    if args.save_logs:
        for testjob in testruns["incomplete"]:
            logfile = save_testjob_log(testjob)

    if args.incomplete:
        for testjob in testruns["incomplete"]:
            reason = get_failure_reason(testjob)
            print(
                "%d,%s,%s,%s"
                % (
                    int(get_testjob_lavajob_id(testjob)),
                    testjob["environment"],
                    testjob["name"],
                    reason,
                )
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("build_url", help="URL of the build")
    parser.add_argument(
        "--incomplete",
        "-i",
        action="store_true",
        help="List incomplete jobs and their failure when --printing-jobs",
    )
    parser.add_argument(
        "--max-builds",
        "-m",
        default=10,
        type=int,
        help="Number of recent builds to look for information",
    )
    parser.add_argument(
        "--print-jobs",
        "-p",
        action="store_true",
        help="Print a representation of the test jobs",
    )
    parser.add_argument(
        "--save-logs",
        "-s",
        action="store_true",
        help="Save logs of incomplete jobs",
    )
    args = parser.parse_args()

    try:
        (
            url,
            group,
            project,
            build_version,
        ) = lkft_squad_client.get_squad_params_from_build_url(args.build_url)
    except Exception:
        sys.exit("Error parsing url: {}".format(args.build_url))

    # Determine group ID
    base_url = lkft_squad_client.urljoiner(url, "api/groups/")
    params = {"slug": group}
    try:
        group_object = lkft_squad_client.get_objects(base_url, params)[0]
    except Exception:
        exit("Error: group {} not found at {}".format(project, base_url))
    group_id = group_object["id"]

    # Get builds URL for the given group/project
    base_url = lkft_squad_client.urljoiner(url, "api/projects/")
    params = {"slug": project, "group": group_id}
    try:
        project_info = lkft_squad_client.get_objects(base_url, params)[0]
    except Exception:
        exit("Error: project {} not found at {}".format(project, base_url))

    # Get list of builds for that group/project
    build_list = lkft_squad_client.get_objects(
        project_info["url"] + "builds/",
        parameters={"version": build_version},
        limit=args.max_builds,
    )

    main_build = None
    for build in build_list:
        if build["version"] == build_version:
            main_build = build

    if main_build:
        print_build_info(args.build_url, main_build)
        print("")

    print("Other builds from the same project:")
    for build in build_list:
        print_build_info_row(build)

    if args.print_jobs:
        print_test_jobs(main_build)
