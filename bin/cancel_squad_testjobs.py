#!/usr/bin/env python3
import argparse
import json
import os
import sys

sys.path.append(os.path.join(sys.path[0],'../','lib'))
from netrcauth import Auth
from proxy import LAVA
from squad_client import get_objects
from pprint import pprint


def main():

    parser = argparse.ArgumentParser(description='Cancel LAVA jobs')
    parser.add_argument('--project-slug',
        dest='project_slug',
        required=True,
        help='slug of the project which test jobs will be canceled')
    parser.add_argument('--squad-url',
        dest='squad_url',
        required=True,
        help='URL of SQUAD instance in form https://example.com')
    parser.add_argument('--build-version',
        dest='build_version',
        required=True,
        help='Version of the build from which testjobs will be canceled')

    args = parser.parse_args()
    params={"slug": args.project_slug}
    base_url = args.squad_url + "/api/projects/"

    project = get_objects(base_url, True, params)
    build_list = get_objects(project['builds'], {'version': args.build_version})
    for build in build_list:
        if build['version'] != args.build_version:
            # double check. but also, version filter is broken presently
            continue

        testjobs = get_objects(build['testjobs'])
        for testjob in testjobs:
            if testjob['job_status'] != 'Submitted':
                print("Skipping: %s; status: %s" % (testjob['job_id'], testjob['job_status']))
                continue
            backend = get_objects(testjob['backend'])
            print("Canceling: %s/scheduler/job/%s" % (backend['url'].replace("/RPC2/",""), testjob['job_id']))
            a = Auth(backend['url'])
            l = LAVA(backend['url'], a.username, a.token)
            c_results = l.proxy.scheduler.cancel_job(testjob['job_id'])
            pprint (c_results)

if __name__ == "__main__":
    main()
