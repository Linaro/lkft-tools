# Local jenkins development

Developing jenkins jobs against ci.linaro.org can be difficult to do in
production. The following instructions may be used to reproduce ci.linaro.org
locally (in part):

## Start Jenkins at http://localhost:8080

```sh
# Make jenkins directory. This will get mounted into /var/jenkins in the
# jenkins container
sudo mkdir /srv/jenkins
chown $USER:$USER /srv/jenkins
alias docker-jenkins="docker run --rm --privileged --name jenkins --volume /srv/jenkins:/var/jenkins_home:rw --publish 0.0.0.0:2222:2222 --publish 0.0.0.0:2233:2233 --publish 0.0.0.0:50000:50000 --publish 0.0.0.0:8080:8080 linaro/ci-x86_64-jenkins-master-debian:lts"
docker-jenkins
# The first time this runs, it will print an administrative token to stdout,
# and also write it into /srv/jenkins. This is used to log into jenkins for
# the first time. Once in, create a local user account for yourself. This
# example uses user named "bill", password "clinton".
```

## Set up Jenkins Job Builder

```sh
pip3 install --user jenkins-job-builder
```

Set up your config file like so:
```sh
cat ~/.config/jenkins_jobs/jenkins_jobs.ini
[job_builder]
ignore_cache=True
keep_descriptions=False
include_path=.:scripts:~/git/
recursive=False
exclude=.*:manual:./development
allow_duplicates=False

[jenkins]
user=bill
password=clinton
url=http://localhost:8080/
query_plugins_info=False
```

## Send jobs to local jenkins using jenkins-jobs

Finally, given a jenkins jobs file such as exist in
https://git.linaro.org/ci/job/configs.git/:

```sh
jenkins-jobs update trigger-lkft-notify-developer.yaml
```

The job should show up at http://localhost:8080.
