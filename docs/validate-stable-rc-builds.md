# Stable rc review validation process
Following steps to be performed when a stable rc review pushed on stable mailing
list

## Wait for stable rc review email
Greg KH pushes on to stable rc trees then sends out email on stable ML
with the list of patches included in that branch.

stable-rc tree link:

*https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable-rc.git*

stable-rc review email example link,

*https://lore.kernel.org/stable/20190808190453.582417307@linuxfoundation.org/T/#mda3573d436265842df547701dc61f9e236627d6c*

Longterm release kernels details

|Version|Maintainer|Released|Projected EOL|
|-------|:---------|:-------|:-----------:|
|4.19|Greg Kroah-Hartman|2018-10-22|Dec, 2020|
|4.14|Greg Kroah-Hartman|2017-11-12|Jan, 2024|
|4.9|Greg Kroah-Hartman|2016-12-11|Jan, 2023|
|4.4|Greg Kroah-Hartman|2016-01-10|Feb, 2022|

one must have to subscribe to the stable mailing list.
You may check your inbox with given filters to identify the stable rc review
for a given branch.

## Build Test
### Check for build is PASS
open lkft.linaro.org website and check the build status
From *https://lkft.linaro.org* you will re-directed to each branch builds for
each device. If you see build status is in progress wait for the
build to finish or if there are builds queued.

*https://qa-reports.linaro.org/lkft/*

### Report build failure
If build FAIL report the build failure along with build error log on
respective email thread. build error should be in plain text and include
branch, head commit id and architecture device.

Example:
If you notice build failure for stable-rc-4.9 branch arm architecture that shows
as "MACHINE=am57xx-evm" for "beagleboard x15" and click on it

*https://ci.linaro.org/job/openembedded-lkft-linux-stable-rc-4.9/*

You could open the link like this,

*https://ci.linaro.org/job/openembedded-lkft-linux-stable-rc-4.9/DISTRO=lkft,MACHINE=am57xx-evm,label=docker-lkft/*

click on build number for view build error on plan text mode
### Bisecting bad commit
git bisect is helpful for finding the bad commit
If you could track down and find bad commit causing build failure then
report the detailed email on stable rc ML and include patch author and
Sub-system maintainers.

### Cancel multiple pushes
If you see multiple git pushes in short period of time on a given branch.
Cancel the old build jobs
There are two ways to cancel
#### Abort build job
Abort build jobs on ci.linaro.org for a given BRANCH and build number

Example:

When there are multiple git pushes on 4.9 BRANCH this page gets updated with build numbers. one build would be in progress and other one would be waiting for the first build to finish. In this case we can abort lower number build by clicking on abort status button. you have to login first.

*https://ci.linaro.org/job/openembedded-lkft-linux-stable-rc-4.9/*

#### Cancel LAVA testjobs
If you notice multiple git pushes on a given BRANCH and by the time you notice the builds are completed and running test jobs on LAVA. Instead of waiting for the old commit around ~170 jobs to finish per build we can cancel those lava test jobs by using cancel_squad_testjobs.py script.
the respective build details page is been created under qa-reports.linaro.org
browse to that page and cancel the lava jobs associated with that build number.

Please refer this document for more details for setup and cancel steps,

*https://github.com/Linaro/lkft-tools/blob/master/docs/cancel_squad_testjobs.md*

## LAB ready
Check all devices status on lkft.linaro.org instance,
make sure you have good number of devices are online to finish the testing
in time. If devices are offline check with LAB team and know the reason for
offline or maintenance mode

Ping LAB team on IRC and report device related problem.
sendout email to LAB team
Create a critical Ticket if needed.

### Sanity test
For each branch build testing the sanity test will be done and these
sanity jobs have high priority and runs LTP ltp-quickhit-tests jobs on
4 architecture's devices arm64, arm, x86_64 and i386.


*https://qa-reports.linaro.org/lkft/linux-stable-rc-4.9-oe-sanity*

Check boot log and ensure no kernel panic, BUG, warning in boot log and test log. If you find Kernel panic or warnings please report on stable ML
If you find boot failure with or without kernel crash log please report on
stable ML.


### Validate each branch test results
The 4.9 branch have high priority so check 4.9 branch jobs are getting
finished first and look for the test finished and check any new failures
and followed by other LTS {4.4, 4.9, 4.14, 4.19 and 5.x} branches.

stable-rc-4.4: *https://qa-reports.linaro.org/lkft/linux-stable-rc-4.4-oe/*

stable-rc-4.4-linaro-hikey: *https://qa-reports.linaro.org/lkft/linaro-hikey-stable-rc-4.4-oe/*

stable-rc-4.9: *https://qa-reports.linaro.org/lkft/linux-stable-rc-4.9-oe/*

stable-rc-4.14: *https://qa-reports.linaro.org/lkft/linux-stable-rc-4.14-oe/*

stable-rc-4.19: *https://qa-reports.linaro.org/lkft/linux-stable-rc-4.19-oe/*

stable-rc-5.2: *https://qa-reports.linaro.org/lkft/linux-stable-rc-5.2-oe/*

Check each test results and ensure no failures.
If you find any test failure, try to reproduce the test failure with possible
minimal steps and report failure on stable ML include respective mailing lists
and maintainers of that sub system and commit author for example LTP / kselfest / netdev / bpf mailing lists

Example:
Regression reported on mailing list
Re: [PATCH 4.19 000/105] 4.19.45-stable review
*https://lore.kernel.org/lkml/20190520222342.wtsjx227c6qbkuua@xps.therub.org*

details of steps to reproduce the regression
*https://lore.kernel.org/lkml/CA+G9fYunxonkqmkhz+zmZYuMTfyRMVBxn6PkTFfjd8tTT+bzHQ@mail.gmail.com*

The each device submits 16 common jobs and few special test suites

#### Number of tests
16 tests * 10 devices= 160 + 4 open posix  + 2 kvm unit test  + 2  ssuite  + 2 kselftests-vsyscalls = 170 Total jobs on each build ( other than 4.4)

### List of devices
- db410c
- Hikey
- i386
- Juno
- qemu_arm
- qemu_arm64
- qemu_i386
- qemu_x86_64
- x15
- x86_64

### List of tests
* build
* kselftest
* libgpiod
* libhugetlbfs
* ltp-cap_bounds-tests
* ltp-commands-tests
* ltp-containers-tests
* ltp-cpuhotplug-tests
* ltp-cve-tests
* ltp-dio-tests
* ltp-fcntl-locktests-tests
* ltp-filecaps-tests
* ltp-fs-tests
* ltp-fs_bind-tests
* ltp-fs_perms_simple-tests
* ltp-fsx-tests
* ltp-hugetlb-tests
* ltp-io-tests
* ltp-ipc-tests
* ltp-math-tests
* ltp-mm-tests
* ltp-nptl-tests
* ltp-pty-tests
* ltp-sched-tests
* ltp-securebits-tests
* ltp-syscalls-tests
* ltp-timers-tests
* network-basic-tests
* perf
* spectre-meltdown-checker-test
* v4l2-compliance
* kvm-unit-tests
* ltp-open-posix-tests


And Generates around 24,000 Test results

### Summary e-mail reports
Use lkft-tools to fetch results from each branch at a time

#### fetch results for BRANCH
 - git clone *https://github.com/Linaro/lkft-tools*
 - cd lkft-tools/bin
 - python3 generate_lts_report.py {{BRANCH}}
   - {{BRANCH}} == {{ 4.4, 4,9, 4.14, 4.19, 5.x }}

Please refer generate lts report document,

*https://github.com/Linaro/lkft-tools/blob/master/docs/generate_lts_report.md*

##### Checklist example
- Generate LTS reports for 4.9 branch and save it in 4.9.results.file
- python3 generate_lts_report.py 4.9 > 4.9.results.file
- You will get to see results summary and test count.
- List of regression test cases and device name
- List of fixed test cases and device name
- Check for false positives
- Check for intermittent failures
- You might notice few tests failures as regressions
- You might notice few tests fixes
- Double check is it an intermittent issues

If it is an intermittent issue the test are expected report as regressions or fix

Please add these intermittent issues and known to fail test cases on
qa-reports-known-issues.git
*https://github.com/Linaro/qa-reports-known-issues*

#### Send out report
open Greg stable rc review e-mail and reply all for a given branch
Remove the list of patch commit headers and file details
Copy and paste results summary generated by lkft-tools generate_lts_report.py

Ex:
- Reply all to stable-rc 4.9 e-mail
- python3 generate_lts_report.py 4.9 > 4.9.results.file
- open and review 4.9.results.file
- do the required changes as described above
- copy and paste results summary on stable-rc 4.9 e-mail thread after trimming e-mail body and send out.

Refer this link for example email report on mailing list,

*https://www.spinics.net/lists/stable/msg320466.html*
