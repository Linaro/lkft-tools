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
- 78: stable-rc-4.4
- 77: stable-rc-4.9
- 76: stable-rc-4.14
- 75: stable-rc-4.19
- 74: reserved for 2019 lts kernel (perhaps 5.3?)
- 73: reserved for 2020 lts kernel (perhaps 5.8?)
- 72/71: stable branches which are not lts (e.g. 4.20, 5.0)
- 50: aosp jobs
- 30: linux-next sanity jobs
- 25:
  - linux-next regular jobs
  - linux-mainline regular jobs
  - lkft-staging jobs

## Design

A few notes on how the above priorities are decided.

- stable-rc results have strict requirements on turnaround time, and are
  therefore prioritbbbized above mainline and next.
- aosp jobs take a lot of wall time, and are prioritized between stable and
  next/mainline.
- -sanity jobs are used for rapid turnaround, and should have the highest
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
openembedded-lkft-linux-stable-rc-4.20.yaml:            name: LAVA_JOB_PRIORITY
openembedded-lkft-linux-stable-rc-4.20.yaml-            default: '72'
--
openembedded-lkft-linux-stable-rc-4.20.yaml:            name: SANITY_LAVA_JOB_PRIORITY
openembedded-lkft-linux-stable-rc-4.20.yaml-            default: '80'
--
openembedded-lkft-linux-stable-rc-4.4.yaml:            name: LAVA_JOB_PRIORITY
openembedded-lkft-linux-stable-rc-4.4.yaml-            default: '78'
--
openembedded-lkft-linux-stable-rc-4.4.yaml:            name: SANITY_LAVA_JOB_PRIORITY
openembedded-lkft-linux-stable-rc-4.4.yaml-            default: '80'
--
openembedded-lkft-linux-stable-rc-4.9.yaml:            name: LAVA_JOB_PRIORITY
openembedded-lkft-linux-stable-rc-4.9.yaml-            default: '77'
--
openembedded-lkft-linux-stable-rc-4.9.yaml:            name: SANITY_LAVA_JOB_PRIORITY
openembedded-lkft-linux-stable-rc-4.9.yaml-            default: '80'
--
openembedded-lkft-linux-stable-rc-5.0.yaml:            name: LAVA_JOB_PRIORITY
openembedded-lkft-linux-stable-rc-5.0.yaml-            default: '71'
--
openembedded-lkft-linux-stable-rc-5.0.yaml:            name: SANITY_LAVA_JOB_PRIORITY
openembedded-lkft-linux-stable-rc-5.0.yaml-            default: '80'
```
