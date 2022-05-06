# -*- coding: utf-8 -*-

import pytest
from afwf_lastpass import lpass
from afwf_lastpass.paths import path_name_txt_for_test

output = """
Google/Email/Alice gmail
Username: alice@gmail.com
Password: 1a2b3c
URL: https://mail.google.com/
Notes: This is Alice's gmail

My Comment: It's my favorite email

    1. a
    2. b
    3. c
""".strip()


def test_parse_output():
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
    assert "My Comment: It's my favorite email"
    assert "    1. a" in note


def test_parse_name_txt():
    l = lpass.parse_name_txt(path_name_txt_for_test)
    l.sort()
    assert l == [
        "alice gmail",
        "bob outlook email",
        "cathy yahoo email",
    ]


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
