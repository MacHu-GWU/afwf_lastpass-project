# -*- coding: utf-8 -*-

import pytest
from afwf_lastpass.hdl.login import handler


def test_handler():
    handler.handler()



if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
