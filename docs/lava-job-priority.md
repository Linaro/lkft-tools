# LAVA Job Priorities for the LKFT Lab

This page documents how LAVA priorities are managed in the LKFT lab at
[lkft.validation.linaro.org](https://lkft.validation.linaro.org/).

Historically, LAVA only allowed "High", "Medium", and "Low" priorities. As of
LAVA 2018.10, LAVA supports priority levels 0-100, where "High" is 100, "Low"
is 0, and "Medium" is 50.

The LKFT lab has many competing jobs with varying degrees of timeliness
requirements, and it fully takes advantage of having 101 priorities available.

## Priorities

- 100: Reserved for limited quantities of jobs submitted by humans
  interactively. Useful for interactive debugging, where human time is spent
  waiting.
- 80:
  - stable-rc sanity jobs (all branches)
  - mainline sanity jobs
  - next sanity jobs
- 77: stable branches which are not LTS (e.g. 6.9)
- 76: stable-rc 6.6
- 75: stable-rc 6.1
- 74: stable-rc 5.15
- 73: stable-rc 5.10
- 72: stable-rc 5.4
- 71: stable-rc-4.19
- 60: higher priority AOSP jobs
- 50: AOSP jobs
- 45: stable-rt and rt-devel jobs
- 40: lower priority AOSP jobs
- 27: linux-next regular jobs
- 27: linux-mainline regular jobs

## Design

A few notes on how the above priorities are decided.

- stable-rc results have strict requirements on turnaround time, and are
  therefore prioritized above mainline and next.
- There are the cases that some AOSP jobs need to be run first to have
  test results in time than the other normal jobs, but still not affect
  other non-AOSP jobs.
- AOSP jobs take a lot of wall time, and are prioritized between stable and
  next/mainline.
- Sanity jobs are used for rapid turnaround, and should have the highest
  automated priority.
- stable-rc job priorities are staggered, so that we can have complete test
  results for some branches earlier, rather than waiting for all branches.


## Implementation

These priorities are generally set in the [common
repo](https://gitlab.com/Linaro/lkft/pipelines/common.git) or [lkft-common
repo](https://gitlab.com/Linaro/lkft/pipelines/lkft-common.git) in the files in
the gitlab-ci/ directory. The easiest way to audit and observe them is with the
following command (output abridged):

```sh
drue@xps:~/src/pipelines/lkft-common$ git grep "^lava-job-priority" tuxconfig/*plan.yml
tuxconfig/linux-4.19.y-plan.yml:lava-job-priority: &lava-job-priority 71
tuxconfig/linux-4.19.y-plan.yml:lava-job-priority-sanity: &lava-job-priority-sanity 80
tuxconfig/linux-5.10.y-plan.yml:lava-job-priority: &lava-job-priority 73
tuxconfig/linux-5.10.y-plan.yml:lava-job-priority-sanity: &lava-job-priority-sanity 80
tuxconfig/linux-5.15.y-plan.yml:lava-job-priority: &lava-job-priority 74
tuxconfig/linux-5.15.y-plan.yml:lava-job-priority-sanity: &lava-job-priority-sanity 80
tuxconfig/linux-5.4.y-plan.yml:lava-job-priority: &lava-job-priority 72
tuxconfig/linux-5.4.y-plan.yml:lava-job-priority-sanity: &lava-job-priority-sanity 80
tuxconfig/linux-6.1.y-plan.yml:lava-job-priority: &lava-job-priority 75
tuxconfig/linux-6.1.y-plan.yml:lava-job-priority-sanity: &lava-job-priority-sanity 80
tuxconfig/linux-6.6.y-plan.yml:lava-job-priority: &lava-job-priority 76
tuxconfig/linux-6.6.y-plan.yml:lava-job-priority-sanity: &lava-job-priority-sanity 80
tuxconfig/linux-6.9.y-plan.yml:lava-job-priority: &lava-job-priority 77
tuxconfig/linux-6.9.y-plan.yml:lava-job-priority-sanity: &lava-job-priority-sanity 80
tuxconfig/linux-tools-plan.yml:lava-job-priority: &lava-job-priority 77
tuxconfig/linux-tools-plan.yml:lava-job-priority-sanity: &lava-job-priority-sanity 80
tuxconfig/master-plan.yml:lava-job-priority: &lava-job-priority 27
tuxconfig/master-plan.yml:lava-job-priority-sanity: &lava-job-priority-sanity 80
```
