# cancel_squad_testjobs.py

This script can be used to cancel lava jobs that have not yet run, based on a
given qa-reports build.

## Example Usage

Set up [lavacli](https://pypi.org/project/lavacli/). Configuration instructions can be found [here](https://git.lavasoftware.org/lava/lavacli/blob/master/doc/configuration.rst).

Then, run cancel_squad_testjobs.py with a given url to a build. Use -i to pass
a lavacli identity, if necessary.

```
drue@xps:~/src/lkft-tools$ cancel_squad_testjobs.py 'https://qa-reports.linaro.org/lkft/linux-stable-rc-4.14-oe/build/v4.14.105-132-g4dc8caa88c8b/'
Skipping: 636948; status: Complete
Skipping: 636947; status: Complete
Skipping: 636946; status: Complete
Skipping: 636945; status: Complete
Skipping: 636944; status: Complete
Skipping: 636943; status: Complete
Skipping: 636942; status: Complete
Skipping: 636941; status: Complete
Skipping: 636940; status: Complete
Skipping: 636939; status: Complete
Skipping: 636938; status: Complete
Skipping: 636937; status: Complete
Skipping: 636936; status: Complete
Skipping: 636935; status: Complete
Skipping: 636931; status: Complete
Skipping: 636930; status: Complete
Skipping: 636929; status: Complete
Skipping: 636928; status: Complete
Skipping: 636927; status: Complete
Skipping: 636926; status: Complete
Skipping: 636925; status: Complete
Skipping: 636924; status: Complete
Skipping: 636923; status: Complete
Skipping: 636922; status: Complete
Skipping: 636921; status: Complete
Skipping: 636920; status: Complete
Skipping: 636919; status: Complete
Skipping: 636918; status: Canceled
Canceling: 636917
lavacli  jobs cancel 636917
Skipping: 636916; status: Complete
...
```

