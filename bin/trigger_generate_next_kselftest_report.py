#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import sys
import yaml

sys.path.append(os.path.join(sys.path[0], "../", "lib"))
import lkft_squad_client  # noqa: E402

BUILDS_URL = "https://qa-reports.linaro.org/api/projects/6/builds/"
STATE_FILE = "/var/tmp/trigger_generate_next_kselftest_report.notified"

# Disregard builds older than MAX_AGE_DAYS
MAX_AGE_DAYS = 2


def get_notified_builds(state_file):
    """Return a list of build ids that have already been notified"""

    if not os.path.isfile(state_file):
        with open(state_file, "w") as f:
            yaml.dump([], f)

    with open(state_file, "r") as f:
        return yaml.load(f)


def set_build_notified(state_file, build_id):
    notified = get_notified_builds(state_file)
    notified.append(build_id)
    with open(state_file, "w") as f:
        yaml.dump(notified, f)


if __name__ == "__main__":

    notified_builds = get_notified_builds(STATE_FILE)

    developer_builds_url = BUILDS_URL
    builds = lkft_squad_client.Builds(developer_builds_url)
    for build in builds:
        if build["id"] in notified_builds:
            # Skip builds that have already been notified
            print("Build {}:{} already notified".format(build["id"], build["version"]))
            continue
        if not build["finished"]:
            # Skip incomplete builds
            print("Build {}:{} not yet finished".format(build["id"], build["version"]))
            continue
        if datetime.datetime.utcnow() - datetime.timedelta(
            days=MAX_AGE_DAYS
        ) > datetime.datetime.strptime(build["datetime"], "%Y-%m-%dT%H:%M:%S.%fZ"):
            # Stop once builds are older than MAX_AGE_DAYS
            # This avoids spamming old builds if state file gets removed
            # It also stops looking for additional builds, saving API requests
            print(
                "Build {}:{} older than {} days; stopping".format(
                    build["id"], build["version"], MAX_AGE_DAYS
                )
            )
            break

        # Notify
        print("Notifying {}".format(build["id"]))
        with open("{}.build_notify_parameters".format(build["id"]), "w") as f:
            f.write("BUILD_ID={}".format(build["id"]))

        # Record notification in state file
        set_build_notified(STATE_FILE, build["id"])
