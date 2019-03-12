import os
import sys

sys.path.append(os.path.join(sys.path[0], "../", "lib"))
import squad_client


def test_get_domain_from_url_1():
    domain = squad_client.get_domain_from_url(
        "https://qa-reports.linaro.org/lkft/linux-stable-rc-4.9-oe/"
    )
    assert domain == "qa-reports.linaro.org"


def test_get_domain_from_url_2():
    domain = squad_client.get_domain_from_url("https://qa-reports.linaro.org")
    assert domain == "qa-reports.linaro.org"


def test_get_domain_from_url_3():
    domain = squad_client.get_domain_from_url(
        "http://qa-reports.linaro.org/lkft/linux-stable-rc-4.9-oe/"
    )
    assert domain == "qa-reports.linaro.org"


def test_get_domain_from_url_4():
    domain = squad_client.get_domain_from_url("http://qa-reports.linaro.org/")
    assert domain == "qa-reports.linaro.org"


def test_get_squad_params_from_build_url_1():
    url = "https://qa-reports.linaro.org/lkft/linux-stable-rc-4.9-oe/build/v4.9.162-94-g0384d1b03fc9/"
    assert squad_client.get_squad_params_from_build_url(url) == (
        "https://qa-reports.linaro.org",
        "lkft",
        "linux-stable-rc-4.9-oe",
        "v4.9.162-94-g0384d1b03fc9",
    )


def test_get_squad_params_from_build_url_2():
    url = "https://qa-reports.linaro.org/lkft/linux-stable-rc-4.9-oe/build/v4.9.162-94-g0384d1b03fc9/#!?details=6233"
    assert squad_client.get_squad_params_from_build_url(url) == (
        "https://qa-reports.linaro.org",
        "lkft",
        "linux-stable-rc-4.9-oe",
        "v4.9.162-94-g0384d1b03fc9",
    )
