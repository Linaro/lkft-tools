#!/usr/bin/env python3

import argparse
import os
import sys

sys.path.append(os.path.join(sys.path[0], "../", "lib"))
import squad_client  # noqa: E402


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("build_url", help="URL of the build")
    parser.add_argument(
        "--max-builds",
        "-m",
        default=10,
        type=int,
        help="Number of recent builds to look for information",
    )
    args = parser.parse_args()

    try:
        (
            url,
            group,
            project,
            build_version,
        ) = squad_client.get_squad_params_from_build_url(args.build_url)
    except:
        sys.exit("Error parsing url: {}".format(args.build_url))

    # Determine group ID
    base_url = squad_client.urljoiner(url, "api/groups/")
    params = {"slug": group}
    try:
        group_object = squad_client.get_objects(base_url, params)[0]
    except:
        exit("Error: group {} not found at {}".format(project, base_url))
    group_id = group_object["id"]

    # Get builds URL for the given group/project
    base_url = squad_client.urljoiner(url, "api/projects/")
    params = {"slug": project, "group": group_id}
    try:
        project_info = squad_client.get_objects(base_url, params)[0]
    except:
        exit("Error: project {} not found at {}".format(project, base_url))

    # Get list of builds for that group/project
    build_list = squad_client.get_objects(
        project_info["builds"],
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
