# -*- coding: utf-8 -*-

import pytest
from afwf_lastpass import lpass


def test_parse_output():
    output = """
    Google/Email/Alice gmail 
    Username: alice@gmail.com
    Password: 1a2b3c
    URL: https://mail.google.com/
    Notes: This is Alice's gmail 
    """.strip()
    data = lpass.parse(name="alice gmail", output=output)
    assert data == {
        'name': 'alice gmail',
        'folder': 'Google/Email/Alice gmail',
        'fullname': 'Google/Email/Alice gmail',
        'Username': 'alice@gmail.com',
        'Password': '1a2b3c',
        'URL': 'https://mail.google.com/',
        'Notes': "This is Alice's gmail",
    }


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
