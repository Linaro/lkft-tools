#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import os
import subprocess
import sys

sys.path.append(os.path.join(sys.path[0], "../", "lib"))
import lkft_squad_client  # noqa: E402


def cancel_lava_jobs(
    url,
    project,
    build_version,
    environment="All",
    identity=None,
    dryrun=False,
    group="lkft",
):
    """
        Requires lavacli. If using a non-default lava identity, specify the identity
        string in 'identity'. The dryrun option, when True, will print the command
        to be executed but will not run it.

        If 'environment' is set, only jobs in the given environment will be
        cancelled.

        Given something like the following:
            url="https://qa-reports.linaro.org"
            project="linux-stable-rc-4.9-oe"
            build="v4.9.162-94-g0384d1b03fc9"

        Discover and cancel all lava jobs that are still running.

        Note this doesn't handle duplicate project names well..
    """

    base_url = lkft_squad_client.urljoiner(url, "api/groups/")

    params = {"slug": group}
    try:
        group_object = lkft_squad_client.get_objects(base_url, params)[0]
    except Exception:
        exit("Error: group {} not found at {}".format(project, base_url))

    group_id = group_object["id"]

    base_url = lkft_squad_client.urljoiner(url, "api/projects/")

    params = {"slug": project, "group": group_id}
    try:
        project = lkft_squad_client.get_objects(base_url, params)[0]
    except Exception:
        exit("Error: project {} not found at {}".format(project, base_url))
    build_list = lkft_squad_client.get_objects(
        project["builds"], {"version": build_version}
    )
    identity_argument = ""
    if identity:
        identity_argument = "-i {}".format(identity)
    for build in build_list:
        if build["version"] != build_version:
            # double check. but also, version filter is broken presently
            continue

        testjobs = lkft_squad_client.get_objects(build["testjobs"])
        for testjob in testjobs:
            if environment != "All":
                if testjob["environment"] != environment:
                    continue
            if (
                testjob["job_status"] != "Submitted"
                and testjob["job_status"] is not None
            ):
                print(
                    "Skipping: %s; status: %s"
                    % (testjob["job_id"], testjob["job_status"])
                )
                continue

            # backend 2 is lkft.validation.linaro.org, our home
            if testjob["backend"] != "https://qa-reports.linaro.org/api/backends/2/":
                print("Skipping: %s. Remote LAVA server." % testjob["job_id"])
                continue

            print("Canceling: %s" % (testjob["job_id"]))

            cmd = "lavacli {} jobs cancel {}".format(
                identity_argument, testjob["job_id"]
            )
            print(cmd)
            if not dryrun:
                subprocess.check_call(cmd, shell=True)


if __name__ == "__main__":

    example_url = "https://qa-reports.linaro.org/lkft/linux-stable-rc-4.9-oe/build/v4.9.162-94-g0384d1b03fc9/"
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Cancel LAVA jobs from a specific SQUAD build.",
        epilog=f"""
Example usage:
    cancel_squad_testjobs.py "{example_url}"
""",
    )
    parser.add_argument(
        "--identity", "-i", dest="identity", default=None, help="lavacli identity"
    )
    parser.add_argument(
        "--dry-run",
        "-n",
        dest="dryrun",
        action="store_true",
        help="Show what jobs would be cancelled",
    )
    parser.add_argument("build_url", help="URL of the build")
    parser.add_argument(
        "--environment_name",
        help="Only cancel jobs with the given environment (board) name. e.g. 'hi6220-hikey'",
        default="All",
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

    cancel_lava_jobs(
        url,
        project,
        build_version,
        identity=args.identity,
        dryrun=args.dryrun,
        group=group,
        environment=args.environment_name,
    )
