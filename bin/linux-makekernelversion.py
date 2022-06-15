#!/usr/bin/env python

import fileinput

def get_git_tag(text):
    for line in text:
        if line.startswith("VERSION"):
            version = line.split("=")[1].strip()
        if line.startswith("PATCHLEVEL"):
            patchlevel = line.split("=")[1].strip()
        if line.startswith("SUBLEVEL"):
            sublevel = line.split("=")[1].strip()
        if line.startswith("EXTRAVERSION"):
            extraversion = line.split("=")[1].strip()
    return "v{}.{}.{}{}".format(version, patchlevel, sublevel, extraversion)

makekernelversion = get_git_tag(fileinput.input())
print(makekernelversion)
