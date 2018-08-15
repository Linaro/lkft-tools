# cancel_squad_testjobs.py

This script can be used to cancel lava jobs that have not yet run, based on a
given qa-reports build.

## Example Usage

Create a ~/.netrc, mode 600, with contents similar to the following. Note that password should not be your user password, but instead an API key available from the qa-reports or lava UI, accordingly.
```
machine qa-reports.linaro.org
        login dan.rue@linaro.org
        password XXX

machine lkft.validation.linaro.org
        login dan.rue
        password XXX
```

Then, provide the required arguments. For example:
```
cancel_squad_testjobs.py --project-slug linux-stable-rc-4.4-oe --squad-url https://qa-reports.linaro.org --build-version v4.4.147-46-g41fa2bf55dc9
```

