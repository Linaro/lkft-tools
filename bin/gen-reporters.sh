#!/bin/bash

export GIT_DIR=/data/linux/.git
export ORIGIN=linux-stable-rc

ROOT_DIR="$(dirname "$(readlink -e $0)")"

if [ $# -lt 1 ]; then
  echo "Need branch as an argument. E.g.:"
  echo "  $0 5.4"
  exit 1
fi

if ! command -v squad-report > /dev/null; then
  echo "squad-report is required. Please install with:"
  echo "  pip3 install squad-report"
  exit 1
fi

BRANCH="$1"

git_commit="$(git rev-parse "${ORIGIN}/linux-${BRANCH}.y")"
git_shortsha="${git_commit:0:11}"
git_describe="$(git describe --always --abbrev=12 ${ORIGIN}/linux-${BRANCH}.y)"
git_makekernelversion="$(git show ${ORIGIN}/linux-${BRANCH}.y:Makefile | ${ROOT_DIR}/linux-makekernelversion.py)"

curr_majmin="$(echo "${git_describe}" | cut -d- -f1)"
rc_majminy="$(echo "${git_makekernelversion}" | cut -d- -f1)"
rc_majmin="$(echo ${rc_majminy} | cut -d. -f1-2)"
rc_y="$(echo ${rc_majminy} | cut -d. -f3)"
prev_y="$((rc_y - 1))"
prev_majminy="${rc_majmin}.${prev_y}"

cat << EOF
#!/bin/sh

[ ! -f squad-report-config.yml ] && wget -O squad-report-config.yml https://gitlab.com/Linaro/lkft/pipelines/lkft-common/-/raw/master/squad-report-config.yml
[ ! -d squad-report ] && git clone https://gitlab.com/Linaro/lkft/reports/squad-report.git

export BASELINE="${prev_majminy}"
export BUILD="${git_describe}"

squad-report \\
  --url=https://qa-reports.linaro.org \\
  --group=lkft \\
  --config squad-report-config.yml \\
  --config-report-type=build \\
  --unfinished \\
  --project="linux-stable-rc-linux-${BRANCH}.y-sanity" \\
  --base-build \${BASELINE} \\
  --build \${BUILD}

mv -v build.txt "report-${git_makekernelversion}-sanity.txt"

./squad-report/scripts/squad-find-regressions \\
  --group=lkft \\
  --project="linux-stable-rc-linux-${BRANCH}.y-sanity" \\
  --build \${BUILD} \\
  > "regressions-${git_makekernelversion}-sanity.txt"

squad-report \\
  --url=https://qa-reports.linaro.org \\
  --group=lkft \\
  --config squad-report-config.yml \\
  --config-report-type=report \\
  --unfinished \\
  --project="linux-stable-rc-linux-${BRANCH}.y" \\
  --base-build \${BASELINE} \\
  --build \${BUILD}

mv -v report.txt "report-${git_makekernelversion}.txt"

./squad-report/scripts/squad-find-regressions \\
  --group=lkft \\
  --project="linux-stable-rc-linux-${BRANCH}.y" \\
  --build \${BUILD} \\
  > "regressions-${git_makekernelversion}.txt"
EOF
