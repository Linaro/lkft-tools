# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.join(sys.path[0], "../", "bin"))
import lkft_notify_developer


def test_get_branch_from_make_kernelversion():
    result = lkft_notify_developer.get_branch_from_make_kernelversion("4.4.138")
    assert result == "4.4"

    result = lkft_notify_developer.get_branch_from_make_kernelversion("4.14.138")
    assert result == "4.14"

    result = lkft_notify_developer.get_branch_from_make_kernelversion("3.18")
    assert result == "3.18"

    result = lkft_notify_developer.get_branch_from_make_kernelversion("4.14.138-rc1")
    assert result == "4.14"
