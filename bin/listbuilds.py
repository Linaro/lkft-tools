#!/usr/bin/env python3

from squad_client.core.models import Squad, Project
from squad_client.core.api import SquadApi
import reportconfig
import os
import sys

token = os.getenv("QA_REPORTS_TOKEN")
if token:
    SquadApi.configure(url="https://qa-reports.linaro.org", token=token)
else:
    SquadApi.configure(url="https://qa-reports.linaro.org")

# arg = "EAP-android12-5.4-lts"
arg = "4.19"
# arg = "android13-5.10"
# arg = "EAP-android12-5.10-lts"
if len(sys.argv) > 1:
    arg = sys.argv[1]

print(f"Kernel branch: {arg}")

rawkernels = reportconfig.get_all_report_kernels()
projectids = reportconfig.get_all_report_projects()

squad_projects = []
if arg in rawkernels:
    projects = rawkernels[arg]
    for project in projects:
        if project in projectids:
            squad_project = project
            if "slug" in projectids[project]:
                squad_project = projectids[project]["slug"]
            elif "project_id" in projectids[project]:
                squad_project = projectids[project]["project_id"]
            squad_projects.append(squad_project)

print(squad_projects)

android_lkft_group = Squad().group("android-lkft")
android_build = {}
for project in squad_projects:
    if isinstance(project, int):
        this_project = android_lkft_group.projects(count=1, id=project)[project]
    else:
        this_project = android_lkft_group.project(project)

    builds = this_project.builds(
        count=10, fields="id,version,finished,datetime", ordering="-datetime"
    ).values()

    # builds = this_project.builds(
    #     count=10, fields="id,version,finished,datetime", ordering="datetime"
    # ).values()

    print(f"{this_project.name}:")
    for build in sorted(builds, key=lambda x: x.datetime):
        if not build.version in android_build:
            android_build[build.version] = build.finished
        if not build.finished:
            android_build[build.version] = build.finished
        print(f"{build.id} {build.version} Finished({build.finished}) {build.datetime}")

print("Summary across projects:")
for build_version in android_build:
    print("%s %s" % (build_version, android_build[build_version]))
