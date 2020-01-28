# Steps to perform when a new Linux branch is released

This enumerates all actions needed in order to fully enable 5.6.

## When 5.6-rc6 is released around 2020-03-21...

### QA Reports
- Create project linux-stable-rc-5.6-oe
- Create project linux-stable-rc-5.6-oe-sanity
- Create project linux-stable-rc-5.6-oe (staging-lkft)
- Create project linux-stable-rc-5.6-oe in staging-qa-reports
- Create project linux-stable-rc-5.6-oe-sanity in staging-qa-reports
- Can do: Dan Rue, Milosz Wasilewski, or Antonio Terceiro

References:
- https://qa-reports.linaro.org/lkft/linux-stable-rc-5.5-oe/
- https://qa-reports.linaro.org/lkft/linux-stable-rc-5.5-oe-sanity/
- https://staging-qa-reports.linaro.org/lkft/linux-stable-rc-5.5-oe/
- https://staging-qa-reports.linaro.org/lkft/linux-stable-rc-5.5-oe-sanity/

### Bugzilla
- Request Bugzilla branch
- Can do: Anyone on the team

Reference: https://projects.linaro.org/browse/LSS-1166

### Jenkins
- Create 5.6-rc trigger and build (*do not merge*)
  - Set job priorities according to [LAVA Job Priorities](lava-job-priority.md)
- Can do: Anyone on the team

Reference: https://review.linaro.org/c/ci/job/configs/+/34039

## When 5.6 is released...

### meta-lkft
- Add kernel for 5.6 RC
- Update PV and SRCREV in Linux mainline and next
- Update PV in kselftests-next
- Can do: Anyone on the team
- Can merge: Daniel Díaz, Dan Rue

Reference: https://github.com/Linaro/meta-lkft/pull/67

- Upgrade kselftests-mainline (*do not merge*)
- Can do: Anyone on the team
- Can merge: Daniel Díaz, Dan Rue

Reference: https://github.com/Linaro/meta-lkft/pull/68

### qa-reports-known-issues
- Add new project to kselftests, libhugetlbfs, and LTP lists

References:
- https://github.com/Linaro/qa-reports-known-issues/pull/96

### Jenkins
- Merge 5.6-rc trigger and build
- Can merge: Anyone on the team
- Note: Only after all other changes have been merged

### Gitlab
- Add 5.6-rc to kernel-trigger
- Can merge: Anyone on the team

Reference: https://gitlab.com/Linaro/lkft/kernel-trigger/-/merge_requests/11

### lkft.linaro.org
- Add branch to [lkft-website](https://github.com/Linaro/lkft-website)
- Can do: Anyone on the team
- Can merge: Daniel Díaz or Dan Rue

Reference: https://github.com/Linaro/lkft-website/pull/224

### lkft-tools
- Add branch to lkft-tools lib/squad_client.py
- Can do: Anyone on the team
- Can merge: Daniel Díaz or Dan Rue

Reference: https://github.com/Linaro/lkft-tools/pull/38

## Soon after...

### meta-lkft
- Validate and merge kselftests-mainline 5.6
- Can merge: Daniel Díaz
