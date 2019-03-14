# Steps to perform when a new Linux branch is released

This enumerates all actions needed in order to fully enable 5.0.

## When 5.0-rc6 is released...

### QA Reports
- Create project linux-stable-rc-5.0-oe
- Create project linux-stable-rc-5.0-oe-sanity
- Create project linux-stable-rc-5.0-oe in staging
- Can do: Dan Rue, Milosz Wasilewski, or Antonio Tercerio

References:
- https://qa-reports.linaro.org/lkft/linux-stable-rc-4.20-oe/
- https://qa-reports.linaro.org/lkft/linux-stable-rc-4.20-oe-sanity/

### Bugzilla
- Request Bugzilla branch
- Can do: Anyone on the team

Reference: https://projects.linaro.org/browse/LSS-206

### Jenkins
- Create 5.0-rc trigger and build (*do not merge*)
- Can do: Anyone on the team

Reference: https://review.linaro.org/#/c/ci/job/configs/+/28832

## When 5.0 is released...

### meta-lkft
- Add kernel for 5.0 and 5.0 RC
- Update PV and SRCREV in Linux mainline and next
- Update PV in kselftests-next
- Can do: Anyone on the team
- Can merge: Daniel Díaz, Dan Rue

Reference: https://github.com/Linaro/meta-lkft/pull/1

- Upgrade kselftests-mainline (*do not merge*)
- Can do: Anyone on the team
- Can merge: Daniel Díaz, Dan Rue
Reference: https://github.com/Linaro/meta-lkft/pull/2

### test-definitions
- Update skiplists
- Add new branch to kselftest and LTP skiplists

References:
- https://review.linaro.org/#/c/qa/test-definitions/+/28865/
- https://review.linaro.org/#/c/qa/test-definitions/+/28866/

### Jenkins
- Merge 5.0-rc trigger and build
- Can merge: Anyone on the team
- Note: Only after all other changes have been merged
- Note: Never change sanity job priority
- Note: For test jobs set the priority as one less than existing priority list

### lkft.linaro.org
- Add branch to [lkft-website](https://github.com/Linaro/lkft-website)
- Can do: Anyone on the team
- Can merge: Daniel Díaz, Dan Rue, or Rafael Tinoco

Reference: https://github.com/Linaro/lkft-website/pull/88

### lkft-tools
- Add branch to lkft-tools lib/squad_client.py
- Can do: Anyone on the team
- Can merge: Daniel Díaz, Dan Rue, or Rafael Tinoco

Reference: https://github.com/Linaro/lkft-tools/commit/a60b68f41fe13224c1710a79e861c910de028a56

## Soon after...

### meta-lkft
- Validate and merge kselftests-mainline 5.0
- Can merge: Daniel Díaz

### LAVA job priority
Stable branch names and LAVA job priorities defined as below
 - stable-rc-4.4 - 78
 - stable-rc-4.9 - 77
 - stable-rc-4.14 - 76
 - stable-rc-4.19 - 75
 - stable-rc-4.20 - 74
 - stable-rc-5.0  - 73
