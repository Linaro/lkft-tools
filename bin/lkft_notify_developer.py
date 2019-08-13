#!/usr/bin/env python3

import argparse
import os
import re
import requests
import sys

sys.path.append(os.path.join(sys.path[0], "../", "lib"))
import squad_client  # noqa: E402


def get_branch_from_make_kernelversion(make_kernelversion):
    """
        IN: "4.4.118"
        OUT: "4.4"
        IN: "4.9.118-rc1"
        OUT: "4.9"
    """
    pattern = re.compile(r"^(\d+\.\d+).*$")
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
        if build["finished"]:
            return build

    # If none found, return first build
    return first_build


def get_build_report(build_url):
    build = squad_client.Build(build_url)
    baseline_branch = get_branch_from_make_kernelversion(
        build.build_metadata["make_kernelversion"]
    )

    # Get baseline
    baseline_project_url = squad_client.get_projects_by_branch()[baseline_branch]
    baseline_builds_url = baseline_project_url + "builds"
    baseline_build = get_most_recent_release(baseline_builds_url)

    template_url = build_url + "email"
    parameters = {"baseline": baseline_build["id"], "template": "9"}
    result = requests.get(template_url, parameters)

    email = build.build_metadata.get("email-notification", "")

    if "No regressions" in result.text:
        subject = "{}: no regressions found".format(build.build["version"])
    else:
        subject = "{}: regressions detected".format(build.build["version"])

    return (email, subject, result.text)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("build_url", help="API URL to developer build")
    args = parser.parse_args()

    (email_destination, email_subject, email_body) = get_build_report(args.build_url)

    with open("email.to", "w") as f:
        f.write(email_destination)
    with open("email.subject", "w") as f:
        f.write(email_subject)
    with open("email.body", "w") as f:
        f.write(email_body)

    print("TO: {}".format(email_destination))
    print("SUBJECT: {}".format(email_subject))
    print("\n{}\n".format(email_body))
