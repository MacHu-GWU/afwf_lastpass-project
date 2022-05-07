# -*- coding: utf-8 -*-

import pytest
from afwf_lastpass.hdl.password import handler

class TestHandler:
    def test(self):
        sf = handler.handler(query="aws/aws-data-lab-sanhe/sanhe")
        sf = handler.handler(query="aws/aws-data-lab-sanhe/sanhe@@")


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
