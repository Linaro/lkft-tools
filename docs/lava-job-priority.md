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
- 79: [Developer builder](developer-builder.md) jobs
- 78: stable branches which are not LTS (e.g. 5.x)
- 77: stable branches which are not LTS (e.g. 5.x)
- 76: stable-rc 5.10
- 75: stable-rc 5.4
- 74: stable-rc-4.19
- 73: stable-rc-4.14
- 72: stable-rc-4.9
- 71: stable-rc-4.4
- 60: higher priority AOSP jobs
- 50: AOSP jobs
- 40: lower priority AOSP jobs
- 30: linux-next sanity jobs
- 26: linux-next regular jobs
- 25:
  - linux-mainline regular jobs
  - lkft-staging jobs

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

These priorities are generally set in the [configs
repo](https://git.linaro.org/ci/job/configs.git/tree/). The easiest way to
audit and observe them is with the following command (output abridged):

```sh
drue@xps:~/src/configs$ grep -A1 PRIORITY *lkft*
...
openembedded-lkft-linux-stable-rc-4.4.yaml:            name: LAVA_JOB_PRIORITY
openembedded-lkft-linux-stable-rc-4.4.yaml-            default: '71'
--
openembedded-lkft-linux-stable-rc-4.4.yaml:            name: SANITY_LAVA_JOB_PRIORITY
openembedded-lkft-linux-stable-rc-4.4.yaml-            default: '80'
--
openembedded-lkft-linux-stable-rc-4.9.yaml:            name: LAVA_JOB_PRIORITY
openembedded-lkft-linux-stable-rc-4.9.yaml-            default: '72'
--
openembedded-lkft-linux-stable-rc-4.9.yaml:            name: SANITY_LAVA_JOB_PRIORITY
openembedded-lkft-linux-stable-rc-4.9.yaml-            default: '80'
--
openembedded-lkft-linux-stable-rc-4.14.yaml:            name: LAVA_JOB_PRIORITY
openembedded-lkft-linux-stable-rc-4.14.yaml-            default: '73'
--
openembedded-lkft-linux-stable-rc-4.14.yaml:            name: SANITY_LAVA_JOB_PRIORITY
openembedded-lkft-linux-stable-rc-4.14.yaml-            default: '80'
...
openembedded-lkft-linux-stable-rc-4.19.yaml:            name: LAVA_JOB_PRIORITY
openembedded-lkft-linux-stable-rc-4.19.yaml-            default: '74'
--
openembedded-lkft-linux-stable-rc-4.19.yaml:            name: SANITY_LAVA_JOB_PRIORITY
openembedded-lkft-linux-stable-rc-4.19.yaml-            default: '80'
--
openembedded-lkft-linux-stable-rc-5.4.yaml:            name: LAVA_JOB_PRIORITY
openembedded-lkft-linux-stable-rc-5.4.yaml-            default: '75'
--
openembedded-lkft-linux-stable-rc-5.4.yaml:            name: SANITY_LAVA_JOB_PRIORITY
openembedded-lkft-linux-stable-rc-5.4.yaml-            default: '80'
--
openembedded-lkft-linux-stable-rc-5.7.yaml:            name: LAVA_JOB_PRIORITY
openembedded-lkft-linux-stable-rc-5.7.yaml-            default: '78'
--
openembedded-lkft-linux-stable-rc-5.7.yaml:            name: SANITY_LAVA_JOB_PRIORITY
openembedded-lkft-linux-stable-rc-5.7.yaml-            default: '80'
--
lkft-member-build.yaml:            name: TEST_LAVA_JOB_PRIORITY
lkft-member-build.yaml-            default: 60
```
