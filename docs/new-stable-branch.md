# Steps to perform when a new Linux branch is released

This enumerates all actions needed in order to fully enable 5.8.

## When Linux 5.8 is released around 2020-08-02...

### QA Reports
- Create project lkft/linux-stable-rc-5.8-oe
- Create project lkft/linux-stable-rc-5.8-oe-sanity
- Create project lkft/linux-stable-rc-5.8-oe in *staging-qa-reports*
- Create project lkft/linux-stable-rc-5.8-oe-sanity in *staging-qa-reports*
- Can do: Dan Rue, Milosz Wasilewski, or Antonio Terceiro

References:
- https://qa-reports.linaro.org/lkft/linux-stable-rc-5.7-oe/
- https://qa-reports.linaro.org/lkft/linux-stable-rc-5.7-oe-sanity/
- https://staging-qa-reports.linaro.org/lkft/linux-stable-rc-5.7-oe/
- https://staging-qa-reports.linaro.org/lkft/linux-stable-rc-5.7-oe-sanity/


- Create project staging-lkft/linux-stable-rc-5.8-oe
- Can do: Daniel Díaz, Dan Rue, Milosz Wasilewski, or Antonio Terceiro

Reference: https://qa-reports.linaro.org/staging-lkft/linux-stable-rc-5.7-oe/

### Bugzilla
- Request Bugzilla branch
- Can do: Anyone on the team

Reference: https://projects.linaro.org/browse/LSS-1387

### meta-lkft
- Add kernel for 5.8 RC
- Update PV and SRCREV in Linux mainline and next
- Update PV in kselftests-next
- Can do: Anyone on the team
- Can merge: Daniel Díaz, Dan Rue

Reference: https://github.com/Linaro/meta-lkft/pull/84

- Upgrade kselftests-mainline (*do not merge*)
- Can do: Anyone on the team
- Can merge: Daniel Díaz, Dan Rue

Reference: https://github.com/Linaro/meta-lkft/pull/86

### qa-reports-known-issues
- Add new project to kselftests, libhugetlbfs, and LTP lists

References:
- https://github.com/Linaro/qa-reports-known-issues/pull/109

### Gitlab
- Add 5.8-rc to kernel-trigger
- Can merge: Anyone on the team

Reference: https://gitlab.com/Linaro/lkft/kernel-trigger/-/merge_requests/20

- Add 5.8-rc to ci-scripts/gen-variables' MIGRATED array and priority
  - Set job priorities according to [LAVA Job Priorities](lava-job-priority.md)
- Can do: Anyone on the team

Reference: https://gitlab.com/Linaro/lkft/ci-scripts/-/merge_requests/98

### lkft-tools
- Add branch to lkft-tools lib/squad_client.py
- Can do: Anyone on the team
- Can merge: Daniel Díaz or Dan Rue

Reference: https://github.com/Linaro/lkft-tools/pull/46

### Jenkins
- Create 5.8-rc trigger and build
  - Set job priorities according to [LAVA Job Priorities](lava-job-priority.md)
- Can do: Anyone on the team

Note: Only merge when kernel and PV has been upgraded in meta-lkft.

Reference: https://review.linaro.org/c/ci/job/configs/+/35469

### lkft.linaro.org
- Add branch to [lkft-website](https://github.com/Linaro/lkft-website)
- Can do: Anyone on the team
- Can merge: Daniel Díaz or Dan Rue

Note: Only merge when Jenkins job and Gitlab CI pipeline have run

Reference: https://github.com/Linaro/lkft-website/pull/245

## Soon after...

### meta-lkft
- Validate and merge kselftests-mainline 5.8
- Can merge: Daniel Díaz
