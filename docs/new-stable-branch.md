# Steps to perform when a new Linux branch is released

This enumerates all actions needed in order to fully enable 4.19.

## When 4.19-rc6 is released...

### QA Reports
- Create project linux-stable-rc-4.19-oe
- Create project linux-stable-rc-4.19-oe-sanity
- Create project linux-stable-rc-4.19-oe in staging
- Can do: Dan Rue, Milosz Wasilewski, or Antonio Tercerio

References:
- https://qa-reports.linaro.org/lkft/linux-stable-rc-4.19-oe/
- https://qa-reports.linaro.org/lkft/linux-stable-rc-4.19-oe-sanity/

### Bugzilla
- Request Bugzilla branch
- Can do: Anyone on the team

Reference: https://projects.linaro.org/browse/LSS-206

### Jenkins
- Create 4.19-rc trigger and build (*do not merge*)
- Can do: Anyone on the team

Reference: https://review.linaro.org/#/c/ci/job/configs/+/28832

## When 4.19 is released...

### meta-96boards
- Add kernel for 4.19 and 4.19 RC
- Update PV and SRCREV in Linux mainline and next
- Can do: Anyone on the team
- Can merge: Daniel Díaz

Reference: https://github.com/96boards/meta-96boards/pull/278

### meta-rpb
- Update PV and SRCREV in kselftests next
- Upgrade kselftests stable (*do not merge*)

References:
- https://github.com/96boards/meta-rpb/pull/195
- https://github.com/96boards/meta-rpb/pull/196

### test-definitions
- Update skiplists
- Add new branch to kselftest and LTP skiplists

References:
- https://review.linaro.org/#/c/qa/test-definitions/+/28865/
- https://review.linaro.org/#/c/qa/test-definitions/+/28866/

### Jenkins
- Merge 4.19-rc trigger and build
- Can merge: Anyone on the team
- Note: Only after all other changes have been merged

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

### meta-rpb
- Validate and merge kselftests stable
- Can merge: Daniel Díaz
