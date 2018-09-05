#!/usr/bin/env python3

import os
import requests
import sys
import yaml

sys.path.append(os.path.join(sys.path[0],'../','lib'))
import squad_client

import lkft_notify_developer

BUILDS_URL = "https://qa-reports.linaro.org/api/projects/131/builds/"
STATE_FILE = "/var/tmp/trigger_lkft_notify_developer.notified"

def get_notified_builds(state_file):
    """ Return a list of build ids that have already been notified """

    if not os.path.isfile(state_file):
        with open(state_file, 'w') as f:
            yaml.dump([], f)

    with open(state_file, 'r') as f:
        return yaml.load(f)

def set_build_notified(state_file, build_id):
    notified = get_notified_builds(state_file)
    notified.append(build_id)
    with open(state_file, 'w') as f:
        yaml.dump(notified, f)

if __name__ == "__main__":

    notified_builds = get_notified_builds(STATE_FILE)

    developer_builds_url = BUILDS_URL
    builds = squad_client.Builds(developer_builds_url)
    for build in builds:
        if build['id'] in notified_builds:
            # Skip builds that have already been notified
            continue
        if not build['finished']:
            # Skip incomplete builds
            continue

        # Notify
        print("Notifying {}".format(build['id']))
        report = lkft_notify_developer.get_build_report(build['url'])
        print(report)
        set_build_notified(STATE_FILE, build['id'])


