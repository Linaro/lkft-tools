#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys
from urllib.parse import urljoin

sys.path.append(os.path.join(sys.path[0], "../", "lib"))
import lkft_squad_client  # noqa: E402


class TestStripWriter(object):
    BlOCK_SIZE = 50
    width_jobs = 40
    testruns = {}

    def __init__(self):
        self.testruns["complete"] = []
        self.testruns["incomplete"] = []
        self.testruns["canceled"] = []
        self.testruns["unfetched"] = []
        self.testruns["unsubmitted"] = []
        self.testruns["unknown"] = []
        self.block_x = 0
        self.block_y = 0
        self.num_jobs = 0

    def analyze(self, testruns_list):
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
            elif not fetched:
                status = "unfetched"
            return status

        for testrun in testruns_list:
            status = get_testjob_status(testrun)
            self.testruns[status].append(testrun)

        self.num_jobs = (
            len(self.testruns["complete"])
            + len(self.testruns["incomplete"])
            + len(self.testruns["canceled"])
            + len(self.testruns["unfetched"])
            + len(self.testruns["unsubmitted"])
            + len(self.testruns["unknown"])
        )

    def write_header(self):
        header = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   id="svg8"
   version="1.1"
   viewBox="0 0 {width_px} {height_px}"
   width="{width_px}"
   height="{height_px}">
  <metadata
     id="metadata5">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title></dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>
"""
        return header.format(
            width_px=self.BlOCK_SIZE * self.width_jobs,
            height_px=self.BlOCK_SIZE * int(1 + (self.num_jobs / self.width_jobs)),
        )

    def write_tail(self):
        return "</svg>"

    def add_block(self, status, testrun):
        block = """  <rect
     x="{x_px}"
     y="{y_px}"
     height="{blocksize}"
     width="{blocksize}"
     id="{test_id}"
     style="opacity:1;vector-effect:none;fill:#{color};fill-opacity:1;stroke:#000000;stroke-width:1.0000;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1" />
"""
        block_color = "b07000"
        if status == "complete":
            block_color = "00b020"
        elif status == "incomplete":
            block_color = "b00010"
        elif status == "canceled":
            block_color = "202020"
        elif status == "unfetched":
            block_color = "b0b0b0"
        elif status == "unsubmitted":
            block_color = "ffffff"
        elif status == "unknown":
            block_color = "ffff20"

        return block.format(
            x_px=self.block_x * self.BlOCK_SIZE,
            y_px=self.block_y * self.BlOCK_SIZE,
            blocksize=self.BlOCK_SIZE,
            test_id=testrun["id"],
            color=block_color,
        )

    def write_to_file(self, filename):
        if not filename:
            filename = "output.svg"
        fh = open(filename, "w")
        fh.write(self.write_header())
        for status in [
            "complete",
            "incomplete",
            "canceled",
            "unfetched",
            "unsubmitted",
            "unknown",
        ]:
            for testrun in self.testruns[status]:
                fh.write(self.add_block(status, testrun))
                self.block_x += 1
                if self.block_x == self.width_jobs:
                    self.block_x = 0
                    self.block_y += 1

        fh.write(self.write_tail())
        fh.close()

    def print_build_info(self):
        print("URL: %s" % build["url"])
        print("ID: %s" % build["id"])
        print("Version: %s" % build["version"])
        print("Project URL: %s" % build["project"])
        print("Date: %s" % build["created_at"])
        print("Finished: %s" % build["finished"])

    def print_line_summary(self):
        print("#" * len(self.testruns["complete"]), end="")
        print("X" * len(self.testruns["incomplete"]), end="")
        print("c" * len(self.testruns["canceled"]), end="")
        print("-" * len(self.testruns["unfetched"]), end="")
        print("." * len(self.testruns["unsubmitted"]), end="")
        print("?" * len(self.testruns["unknown"]), end="")
        print("")

    def print_progress_summary(self):
        print("Total:       %8d" % self.num_jobs)
        print("Complete:    %8d" % len(self.testruns["complete"]))
        print("Incomplete:  %8d" % len(self.testruns["incomplete"]))
        print("Canceled:    %8d" % len(self.testruns["canceled"]))
        print("Unfetched:   %8d" % len(self.testruns["unfetched"]))
        print("Unsubmitted: %8d" % len(self.testruns["unsubmitted"]))
        print("Unknown:     %8d" % len(self.testruns["unknown"]))
        progress = 0
        if self.num_jobs > 0:
            progress = (
                100
                * (
                    self.num_jobs
                    - len(self.testruns["unfetched"])
                    - len(self.testruns["unsubmitted"])
                )
                / self.num_jobs
            )
        print("Progress:      %3.02f%%" % progress)


def write_test_jobs(build, filename="strip.svg"):
    base_url = build["testjobs"]
    try:
        # testruns_info = lkft_squad_client.get_objects(base_url, params)[0]
        testruns_list = lkft_squad_client.get_objects(base_url)
    except Exception:
        exit("Error: not found at {}".format(base_url))

    test_strip = TestStripWriter()
    test_strip.analyze(testruns_list)
    # test_strip.print_build_info()
    # test_strip.print_line_summary()
    test_strip.write_to_file(filename)
    test_strip.print_progress_summary()


if __name__ == "__main__":
    # List of possible branches.
    # To add a branch, navigate in browser to
    # https://qa-reports.linaro.org/api/projects/.
    projects = lkft_squad_client.get_projects_by_branch()
    available_branches = projects.keys()
    branch_help = "[" + "|".join(available_branches) + "]"

    parser = argparse.ArgumentParser()
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--branch", "-b", help=branch_help)
    g.add_argument("--build", help="URL of the build")
    parser.add_argument(
        "--output", "-o", help="File name for the SVG test strip to write"
    )
    args = parser.parse_args()

    selected_build = None

    if args.branch:
        if args.branch not in available_branches:
            sys.exit("Invalid branch specified")

        # Get latest build available for given LKFT branch
        builds_url = urljoin(projects[args.branch], "builds")
        all_builds = lkft_squad_client.Builds(builds_url)
        for build in all_builds:
            selected_build = build
            break
        if all_builds is None:
            sys.exit("No builds")
    elif args.build:
        try:
            (
                url,
                group,
                project,
                build_version,
            ) = lkft_squad_client.get_squad_params_from_build_url(args.build)
        except Exception:
            sys.exit("Error parsing url: {}".format(args.build))

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
            project_info["builds"], parameters={"version": build_version}, limit=50
        )

        main_build = None
        for build in build_list:
            if build["version"] == build_version:
                selected_build = build

    write_test_jobs(selected_build, args.output)
