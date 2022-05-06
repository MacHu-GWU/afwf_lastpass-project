# -*- coding: utf-8 -*-

import pytest
from afwf_lastpass import lpass
from afwf_lastpass.paths import path_name_txt_for_test


def test_parse_output():
    output = """
    Google/Email/Alice gmail 
    Username: alice@gmail.com
    Password: 1a2b3c
    URL: https://mail.google.com/
    Notes: This is Alice's gmail
    
    It's my favorite email
    """.strip()
    data = lpass.parse_output(name="alice gmail", output=output)
    note = data.pop("Notes")
    assert data == {
        'name': 'alice gmail',
        'folder': 'Google/Email/Alice gmail',
        'fullname': 'Google/Email/Alice gmail',
        'Username': 'alice@gmail.com',
        'Password': '1a2b3c',
        'URL': 'https://mail.google.com/',
    }
    # print(note)


# def test_parse_name_txt():
#     l = lpass.parse_name_txt(path_name_txt_for_test)
#     l.sort()
#     assert l == [
#         "alice gmail",
#         "bob outlook email",
#         "cathy yahoo email",
#     ]


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
