# -*- coding: utf-8 -*-

from typing import List
import enum
import json
import subprocess

import afwf
from pathlib_mate import Path

from .paths import (
    lasspass_cli,
    path_name_txt,
)
from . import images


class PasswordForm(enum.Enum):
    id = "id"
    name = "name"
    fullname = "fullname"
    username = "username"
    password = "password"
    last_modified_gmt = "last_modified_gmt"
    last_touch = "last_touch"
    group = "folder"
    url = "url"
    note = "note"


no_show_fields = [
    PasswordForm.id.value,
    PasswordForm.fullname.value,
    PasswordForm.last_modified_gmt.value,
    PasswordForm.last_touch.value,
]

sensitive_fields = [
    PasswordForm.password.value,
    PasswordForm.note.value,
]


def parse_lpass_show_output_json(output: str) -> dict:
    """
    ``lpass show "${name}"`` command returns this, we want to parse the text
    output into machine readable format::

        [
            {
                "id": "123456789",
                "name": "Alice Gmail",
                "fullname": "Folder/Alice Gmail",
                "username": "alice@gmail.com",
                "password": "1a2b3c",
                "last_modified_gmt": "",
                "last_touch": "",
                "group": "Email",
                "url": "https://accounts.google.com/servicelogin",
                "note": "this is Alice's gmail"
            }
        ]
    """
    dct = json.loads(output)[0]
    return dct


def show(name: str) -> dict:
    output = subprocess.check_output([
        lasspass_cli, "show", name, "--json",
    ]).decode("utf-8")
    return parse_lpass_show_output_json(output)


def parse_name_txt(path: Path = path_name_txt) -> List[str]:
    """
    ``name.txt`` is a cache file locate at ``~/.alfred-afwf_lastpass/name.txt``.
    It stores the list of all lastpass item name for full text search.

    This function can parse the file and returns the name list.
    """
    return list(set([
        line.strip()
        for line in path.read_text().strip().split("\n")
        if line.strip()
    ]))


def password_data_to_items(data: dict) -> List[afwf.Item]:
    name = data[PasswordForm.name.value]
    items = list()
    for k, v in data.items():
        if k in no_show_fields:
            continue

        if k in sensitive_fields:
            title = f"{k} = ***"
        else:
            title = f"{k} = {v}"

        item = afwf.Item(
            title=title,
            subtitle="",
            autocomplete=f"{name}@@{k}",
            arg=v,
            icon=afwf.Icon.from_image_file(images.lastpass),
            variables={"field": k},
        )

        # special features for the 'name' fields, should be always on top
        if k == PasswordForm.name.value:
            # Cmd + L to preview large text
            # ref: https://www.alfredapp.com/help/features/large-type/
            item.text = afwf.Text(
                largetype="\n".join([
                    f"{k} = {v}"
                    for k, v in data.items()
                ])
            )

            # hit 'enter' to ENTER the secret
            secret_value = data.get(PasswordForm.password.value, f"Password Not Found in {name!r}")
            item.subtitle = "hit 'enter' to ENTER the secret"
            item.variables["run_apple_script"] = afwf.VarValueEnum.y.value
            item.variables["run_apple_script_arg"] = secret_value

            # hit 'CMD + enter' to COPY the secret
            item.add_modifier(
                mod=afwf.ModEnum.cmd.value,
                subtitle="hit 'CMD + enter' to COPY the secret",
                arg=secret_value,
            )

            # hit 'Alt + enter' to OPEN the url
            if data.get(PasswordForm.url.value, ""):
                item.add_modifier(
                    mod=afwf.ModEnum.alt.value,
                    subtitle="hit 'Alt + enter' to OPEN the url",
                    arg=data[PasswordForm.url.value],
                )

        # special features for the 'url' fields
        # hit 'enter' to OPEN the url
        if k == PasswordForm.url.value:
            item.variables["open_url"] = afwf.VarValueEnum.y.value
            item.variables["open_url_arg"] = v

        items.append(item)

    return items


def password_name_to_items(name: str):
    data = show(name)
    return password_data_to_items(data)
