import re
import requests


def get_projects_by_branch():
    return {
        "4.4": "https://qa-reports.linaro.org/api/projects/40/",
        "4.4-hikey": "https://qa-reports.linaro.org/api/projects/34/",
        "4.9": "https://qa-reports.linaro.org/api/projects/23/",
        "4.14": "https://qa-reports.linaro.org/api/projects/58/",
        "4.18": "https://qa-reports.linaro.org/api/projects/133/",
        "4.19": "https://qa-reports.linaro.org/api/projects/135/",
        "4.20": "https://qa-reports.linaro.org/api/projects/141/",
        # Refer to mainline by its version number
        # This is necessary so that lkft_notify_developer can determine
        # which branch to use
        "5.0": "https://qa-reports.linaro.org/api/projects/22/",
    }


def get_objects(endpoint_url, expect_one=False, parameters={}):
    """
    gets list of objects from endpoint_url
    optional parameters allow for filtering
    expect_count
    """
    obj_r = requests.get(endpoint_url, parameters)
    if obj_r.status_code == 200:
        objs = obj_r.json()
        if "count" in objs.keys():
            if expect_one and objs["count"] == 1:
                return objs["results"][0]
            else:
                ret_obj = []
                while True:
                    for obj in objs["results"]:
                        ret_obj.append(obj)
                    if objs["next"] is None:
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
