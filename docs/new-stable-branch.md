# Steps to perform when a new Linux branch is released

This enumerates all actions needed in order to fully enable 5.1.

## When 5.1-rc6 is released...

### QA Reports
- Create project linux-stable-rc-5.1-oe
- Create project linux-stable-rc-5.1-oe-sanity
- Create project linux-stable-rc-5.1-oe in staging
- Create project linux-stable-rc-5.1-oe-sanity in staging
- Can do: Dan Rue, Milosz Wasilewski, or Antonio Terceiro

References:
- https://qa-reports.linaro.org/lkft/linux-stable-rc-5.0-oe/
- https://qa-reports.linaro.org/lkft/linux-stable-rc-5.0-oe-sanity/
- https://staging-qa-reports.linaro.org/lkft/linux-stable-rc-5.0-oe/
- https://staging-qa-reports.linaro.org/lkft/linux-stable-rc-5.0-oe-sanity/

### Bugzilla
- Request Bugzilla branch
- Can do: Anyone on the team

Reference: https://projects.linaro.org/browse/LSS-389

### Jenkins
- Create 5.1-rc trigger and build (*do not merge*)
  - Set job priorities according to [LAVA Job Priorities](lava-job-priority.md)
- Can do: Anyone on the team

Reference: https://review.linaro.org/c/ci/job/configs/+/30341

## When 5.1 is released...

### meta-lkft
- Add kernel for 5.1 and 5.1 RC
- Update PV and SRCREV in Linux mainline and next
- Update PV in kselftests-next
- Can do: Anyone on the team
- Can merge: Daniel Díaz, Dan Rue

Reference: https://github.com/Linaro/meta-lkft/pull/18

- Upgrade kselftests-mainline (*do not merge*)
- Can do: Anyone on the team
- Can merge: Daniel Díaz, Dan Rue
Reference: https://github.com/Linaro/meta-lkft/pull/21

### qa-reports-known-issues
- Add new project to kselftests, libhugetlbfs, and LTP lists

References:
- https://github.com/Linaro/qa-reports-known-issues/pull/40

### Jenkins
- Merge 5.1-rc trigger and build
- Can merge: Anyone on the team
- Note: Only after all other changes have been merged

### lkft.linaro.org
- Add branch to [lkft-website](https://github.com/Linaro/lkft-website)
- Can do: Anyone on the team
- Can merge: Daniel Díaz, Dan Rue, or Rafael Tinoco

Reference: https://github.com/Linaro/lkft-website/pull/124

### lkft-tools
- Add branch to lkft-tools lib/squad_client.py
- Can do: Anyone on the team
- Can merge: Daniel Díaz, Dan Rue, or Rafael Tinoco

Reference: https://github.com/Linaro/lkft-tools/commit/f8842ee6a584b615789a51a4b46254140504ade7

## Soon after...

### meta-lkft
- Validate and merge kselftests-mainline 5.1
- Can merge: Daniel Díaz
