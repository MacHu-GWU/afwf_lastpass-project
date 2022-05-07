# -*- coding: utf-8 -*-

import pytest
import json
from rich import print as jprint
from afwf_lastpass import lpass
from afwf_lastpass.paths import path_name_txt_for_test

sample_password_data = {
    "id": "123456789",
    "name": "Alice Gmail",
    "fullname": "Folder/Alice Gmail",
    "username": "alice@gmail.com",
    "password": "1a2b3c",
    "last_modified_gmt": "",
    "last_touch": "",
    "group": "Email",
    "url": "https://accounts.google.com/servicelogin",
    "note": "this is Alice's gmail",
}


def test_parse_lpass_show_output_json():
    output = json.dumps([sample_password_data, ])
    data = lpass.parse_lpass_show_output_json(output=output)
    assert data == {
        "id": "123456789",
        "name": "Alice Gmail",
        "fullname": "Folder/Alice Gmail",
        "username": "alice@gmail.com",
        "password": "1a2b3c",
        "last_modified_gmt": "",
        "last_touch": "",
        "group": "Email",
        "url": "https://accounts.google.com/servicelogin",
        "note": "this is Alice's gmail",
    }


def test_parse_name_txt():
    l = lpass.parse_name_txt(path_name_txt_for_test)
    l.sort()
    assert l == [
        "alice gmail",
        "bob outlook email",
        "cathy yahoo email",
    ]


def test_password_to_item():
    items = lpass.password_data_to_items(sample_password_data)
    assert items[0].variables["field"] == "name"


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
