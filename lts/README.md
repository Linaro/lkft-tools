# LKFT LTS Tools

This directory contains tools related to testing LTS branches.

## generate_lts_report.py usage

generate_lts_report.py by default takes a branch as an argument (i.e. 4.4, 4.9,
4.14, etc), and provides a report suitable for use on the stable mailing list.

The following options are supported:

- --unfinished. This is useful for when results should be sent out, even though
  the build has not yet been marked 'finished' in qa-reports.

- --force-good. This can be used to mark a report as 'no regressions', even if
  regressions were found. Note that it only modifies the header - regressions
  inside the report will still be shown.

- --baseline. By default the previous build in a branch will be used as a
  baseline, but often it is handy to be able to specify an alternative
  baseline. The format is a build id, which can be found by navigating to a
  project's api page and finding the appropriate build id. For example,
  https://qa-reports.linaro.org/api/projects ->
  https://qa-reports.linaro.org/api/projects/23/ ->
  https://qa-reports.linaro.org/api/projects/23/builds/.

- --build. By default the latest build is reported on. --build takes a build
  id, and reports on it instead.

Tip: If you use vim for email, these results can be inlined using e.g. ":read !generate_lts_report.py 4.17".

### Example

```sh
# Typical usage
$ generate_lts_report.py 4.17
ERROR: Build 8756(v4.17.14-102-g8164cbf5064a) not yet Finished. Pass --unfinished to force a report.

# Force results, even though the tests have not completed
drue@xps:~$ generate_lts_report.py 4.17 --unfinished
Results from Linaro’s test farm.
No regressions on arm64, arm and x86_64.
...

# Specify an alternative baseline
$:~$ generate_lts_report.py 4.17 --unfinished --baseline 8631
...
No regressions (compared to build v4.17.14)
...

# Specify a different build and a different baseline
$ generate_lts_report.py 4.17 --baseline 8631 --unfinished --build 8750
Results from Linaro’s test farm.
No regressions on arm64, arm and x86_64.

Summary
------------------------------------------------------------------------

kernel: 4.17.15-rc2
git repo: https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable-rc.git
git branch: linux-4.17.y
git commit: 2293fe70092e6b788833a9d7e12327b8bc66fa07
git describe: v4.17.14-101-g2293fe70092e
Test details: https://qa-reports.linaro.org/lkft/linux-stable-rc-4.17-oe/build/v4.17.14-101-g2293fe70092e


No regressions (compared to build v4.17.14)
```
