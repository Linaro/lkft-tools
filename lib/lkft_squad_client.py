# -*- coding: utf-8 -*-

import re
import requests


def get_projects_by_branch():
    return {
        "4.4": "https://qa-reports.linaro.org/api/projects/40/",
        "4.4-hikey": "https://qa-reports.linaro.org/api/projects/34/",
        "4.9": "https://qa-reports.linaro.org/api/projects/23/",
        "4.13": "https://qa-reports.linaro.org/api/projects/57/",
        "4.14": "https://qa-reports.linaro.org/api/projects/58/",
        "4.15": "https://qa-reports.linaro.org/api/projects/93/",
        "4.16": "https://qa-reports.linaro.org/api/projects/101/",
        "4.17": "https://qa-reports.linaro.org/api/projects/118/",
        "4.18": "https://qa-reports.linaro.org/api/projects/133/",
        "4.19": "https://qa-reports.linaro.org/api/projects/135/",
        "4.20": "https://qa-reports.linaro.org/api/projects/141/",
        "5.0": "https://qa-reports.linaro.org/api/projects/159/",
        "5.1": "https://qa-reports.linaro.org/api/projects/167/",
        "5.2": "https://qa-reports.linaro.org/api/projects/183/",
        "5.3": "https://qa-reports.linaro.org/api/projects/204/",
        "5.4": "https://qa-reports.linaro.org/api/projects/232/",
        "5.5": "https://qa-reports.linaro.org/api/projects/263/",
        "5.6": "https://qa-reports.linaro.org/api/projects/284/",
        "5.7": "https://qa-reports.linaro.org/api/projects/310/",
        "5.8": "https://qa-reports.linaro.org/api/projects/347/",
        "5.9": "https://qa-reports.linaro.org/api/projects/497/",
        "5.10": "https://qa-reports.linaro.org/api/projects/597/",
        "5.11": "https://qa-reports.linaro.org/api/projects/651/",
        "5.12": "https://qa-reports.linaro.org/api/projects/758/",
        "5.13": "https://qa-reports.linaro.org/api/projects/833/",
        "5.14": "https://qa-reports.linaro.org/api/projects/961/",
        "5.15": "https://qa-reports.linaro.org/api/projects/1022/",
        "5.16": "https://qa-reports.linaro.org/api/projects/1107/",
        "5.17": "https://qa-reports.linaro.org/api/projects/1154/",
        "5.18": "https://qa-reports.linaro.org/api/projects/1198/",
        "5.19": "https://qa-reports.linaro.org/api/projects/1259/",
        "6.0": "https://qa-reports.linaro.org/api/projects/1419/",
        "6.1": "https://qa-reports.linaro.org/api/projects/1597/",
        "6.2": "https://qa-reports.linaro.org/api/projects/1697/",
        "6.3": "https://qa-reports.linaro.org/api/projects/1764/",
        "6.4": "https://qa-reports.linaro.org/api/projects/1796/",
        # Refer to mainline by its version number
        # This is necessary so that lkft_notify_developer can determine
        # which branch to use
        "6.5": "https://qa-reports.linaro.org/api/projects/22/",
        "next": "https://qa-reports.linaro.org/api/projects/6/",
    }


def get_domain_from_url(url):
    """
    Given a fully qualified http or https url, return the
    domain name.
    IN:
        https://qa-reports.linaro.org/lkft/linux-stable-rc-4.9-oe/
        https://qa-reports.linaro.org
        http://qa-reports.linaro.org
    OUT:
        qa-reports.linaro.org
    """
    return re.match(r"https?://([^/$]*)", url).groups()[0]


def get_squad_params_from_build_url(url):
    """
    Given a url to a build, return a tuple consisting of
    (squad-url, group-slug, project-slug, build-version)

    For example:
    IN:
        https://qa-reports.linaro.org/lkft/linux-stable-rc-4.9-oe/build/v4.9.162-94-g0384d1b03fc9/
    OUT:
        ('https://qa-reports.linaro.org',
         'lkft',
         'linux-stable-rc-4.9-oe',
         'v4.9.162-94-g0384d1b03fc9'
        )
    IN:
        https://qa-reports.linaro.org/lkft/linux-stable-rc-4.9-oe/
    OUT:
        ('https://qa-reports.linaro.org',
         'lkft',
         'linux-stable-rc-4.9-oe',
         None
        )
    """
    # first
    try:
        rematch = re.match(
            r"(https?://[^/$]*)/([^/]*)/([^/]*)/build/([^/]*)", url
        ).groups()
    except:
        # second
        try:
            rematch = re.match(r"(https?://[^/$]*)/([^/]*)/([^/]*)", url).groups() + (
                None,
            )
        except:
            pass

    return rematch


def urljoiner(*args):
    """
    Joins given arguments into an url. Trailing but not leading slashes are
    stripped for each argument.
    """
    return "/".join(map(lambda x: str(x).rstrip("/"), args))


def get_objects(endpoint_url, parameters={}, limit=None):
    """
    gets list of objects from endpoint_url
    optional parameters allow for filtering
    expect_count
    """
    if limit:
        parameters["limit"] = limit
    obj_r = requests.get(endpoint_url, parameters)
    if obj_r.status_code == 200:
        objs = obj_r.json()
        if "count" in objs.keys():
            if limit == 1 and objs["count"] == 1:
                return objs["results"][0]
            else:
                ret_obj = []
                while True:
                    for obj in objs["results"]:
                        ret_obj.append(obj)
                    if objs["next"] is None or len(ret_obj) == limit:
                        break
                    else:
                        obj_r = requests.get(objs["next"])
                        if obj_r.status_code == 200:
                            objs = obj_r.json()
                return ret_obj
        else:
            return objs


class Builds(object):
    def __init__(self, builds_url):
        self.builds_url = builds_url

    def __iter__(self):
        obj_r = requests.get(self.builds_url)
        obj_r.raise_for_status()
        objs = obj_r.json()
        while True:
            for obj in objs["results"]:
                yield obj
            if objs["next"] is None:
                break
            else:
                obj_r = requests.get(objs["next"])
                obj_r.raise_for_status()
                objs = obj_r.json()


class Build(object):
    def __init__(self, build_url):
        self.build = get_objects(build_url)
        self.build_metadata = get_objects(self.build["metadata"])
