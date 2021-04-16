# Steps to perform when a new Linux branch is released

This enumerates all actions needed in order to fully enable 5.12.

## When Linux 5.12 is released around 2021-04-18...

### Bugzilla
- Request Bugzilla branch
- Can do: Anyone on the team

Reference: https://projects.linaro.org/browse/LSS-1957

### meta-lkft
- Add kernel for 5.12 RC
- Update PV and SRCREV in Linux mainline and next
- Update PV in kselftests-next
- Can do: Anyone on the team
- Can merge: Daniel Díaz, anyone on the team

Reference: https://github.com/Linaro/meta-lkft/pull/136

- Upgrade kselftests-mainline (*do not merge*)
- Can do: Anyone on the team
- Can merge: Daniel Díaz, anyone on the team

Reference: https://github.com/Linaro/meta-lkft/pull/129

### qa-reports-known-issues
- Add new project to kselftests, libhugetlbfs, and LTP lists

References:
- https://github.com/Linaro/qa-reports-known-issues/pull/139

### Gitlab
- Add 5.12-rc to `common/gen-variables` branch priority
  - Set job priorities according to [LAVA Job Priorities](lava-job-priority.md)
- Can do: Anyone on the team

Reference: https://gitlab.com/Linaro/lkft/pipelines/common/-/merge_requests/50

### lkft-tools
- Add branch to lkft-tools lib/squad_client.py
- Can do: Anyone on the team
- Can merge: Anyone on the team

Reference: https://github.com/Linaro/lkft-tools/pull/56

### Jenkins
- Create 5.12-rc trigger and build
  - Set job priorities according to [LAVA Job Priorities](lava-job-priority.md)
- Can do: Anyone on the team

Note: Only merge when kernel and PV has been upgraded in meta-lkft.

Reference: https://review.linaro.org/c/ci/job/configs/+/37876

### lkft.linaro.org
- Add branch to [lkft-website](https://github.com/Linaro/lkft-website)
- Can do: Anyone on the team
- Can merge: Anyone on the team

Note: Only merge when Jenkins job and Gitlab CI pipeline have run

Reference: https://github.com/Linaro/lkft-website/pull/292

## Soon after...

### meta-lkft
- Validate and merge kselftests-mainline 5.12
- Can merge: Daniel Díaz
