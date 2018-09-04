import requests

def get_objects(endpoint_url, expect_one=False, parameters={}):
    """
    gets list of objects from endpoint_url
    optional parameters allow for filtering
    expect_count
    """
    obj_r = requests.get(endpoint_url, parameters)
    if obj_r.status_code == 200:
        objs = obj_r.json()
        if 'count' in objs.keys():
            if expect_one and objs['count'] == 1:
                return objs['results'][0]
            else:
                ret_obj = []
                while True:
                    for obj in objs['results']:
                        ret_obj.append(obj)
                    if objs['next'] is None:
                        break
                    else:
                        obj_r = requests.get(objs['next'])
                        if obj_r.status_code == 200:
                            objs = obj_r.json()
                return ret_obj
        else:
            return objs

