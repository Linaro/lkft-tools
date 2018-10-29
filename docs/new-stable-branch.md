# Steps to perform when a new linux branch is released

For example, for creating 4.18-rc:

## Create Jenkins jobs
- Create 4.18-rc trigger and build
- Anyone on the team may do this
- May be merged by Dan Rue or Daniel Díaz
- ref: https://review.linaro.org/25779

## Add kernel branch to meta-96boards
- add kernel for 4.18 and 4.18 RC
- May be merged by Daniel Díaz or Anders Roxell
- ref: https://github.com/96boards/meta-96boards/pull/248

## Update PV and SRCREV in meta-96boards and meta-rpb
```
meta-96boards/ (72f8425e6763fe40f2175a888b020541787e474e)
 recipes-kernel/linux/linux-generic-mainline_git.bb
 recipes-kernel/linux/linux-generic-next_git.bb
meta-rpb/
 recipes-overlayed/kselftests/kselftests-next_git.bb
 recipes-overlayed/kselftests/kselftests-next_4.17.bb
```

## Update skiplists
- Add new branch to kselftest and ltp skiplists in test-definitions
- ref: https://review.linaro.org/#/c/ci/job/configs/+/25779/

## Add new branch to qa-reports
- Create linux-stable-rc-4.18-oe and linux-stable-rc-4.18-oe-sanity in
  qa-reports
- Dan Rue, Milosz Wasilewski, or Antonio Tercerio can do this
- *risk* - only one member of the KV team has privilege to do this.

## Add branch to lkft.linaro.org
- Add branch to [lkft-website](https://github.com/Linaro/lkft-website)
- Daniel, Dan, or Rafael can merge this
- ref: https://github.com/Linaro/lkft-website/pull/66
