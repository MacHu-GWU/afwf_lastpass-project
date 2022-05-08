# -*- coding: utf-8 -*-

import subprocess
import attr
import afwf

from ..fts import search_name
from ..lpass import (
    parse_lpass_show_output_json,
    password_data_to_items,
)
from ..fuzzy_filter import FuzzyObjectSearch
from ..logger import logger
from ..paths import (
    path_lpass_username, lasspass_cli,
    path_alfred_workflow_name_index_write_lock,
    path_alfred_workflow_name_txt,
    python_interpreter,
    path_user_workflow_main_py,
)
from .. import images


@attr.define
class Handler(afwf.Handler):
    def login_lastpass_cli(self, query: str) -> afwf.ScriptFilter:
        sf = afwf.ScriptFilter()
        if len(query):
            item = afwf.Item(
                title=f"Enter username = '{query}' to login",
                subtitle="Lastpass username not found!",
                icon=afwf.Icon.from_image_file(images.signin),
            )
            cmd = f"{lasspass_cli} login \"{query}\""
            item.variables["terminal_command"] = afwf.VarValueEnum.y.value
            item.variables["terminal_command_arg"] = cmd
        else:
            item = afwf.Item(
                title=f"Enter username to login",
                subtitle="Lastpass username not found!",
                icon=afwf.Icon.from_image_file(images.signin),
            )
        sf.items.append(item)
        return sf

    def create_index(self) -> afwf.ScriptFilter:
        sf = afwf.ScriptFilter()
        cmd = f"{lasspass_cli} export --sync=now --fields=name > {path_alfred_workflow_name_txt.abspath} && {python_interpreter} {path_user_workflow_main_py} 'build_index_action noquery'"
        item = afwf.Item(
            title="Search index not found, hit 'enter' to create it",
            arg=cmd,
            icon=afwf.Icon.from_image_file(images.plus)
        )
        item.variables["terminal_command"] = afwf.VarValueEnum.y.value
        item.variables["terminal_command_arg"] = cmd
        sf.items.append(item)
        return sf

    def search_password_item(self, query: str) -> afwf.ScriptFilter:
        sf = afwf.ScriptFilter()
        if len(query) == 0:
            sf.items.append(afwf.Item(
                title="Type to search lastpass ...",
                icon=afwf.Icon.from_image_file(images.lastpass),
            ))
        else:
            doc_list = search_name(q=query)
            if len(doc_list) == 0:
                sf.items.append(afwf.Item(
                    title="No result found!",
                    icon=afwf.Icon.from_image_file(afwf.Icons.error)
                ))
            else:
                for doc in doc_list:
                    name = doc["name"]
                    item = afwf.Item(
                        title=name,
                        subtitle=name,
                        autocomplete=name + "@@",
                        arg=name,
                        icon=afwf.Icon.from_image_file(images.lastpass),
                    )
                    sf.items.append(item)
        return sf

    def search_password_item_field(self, query: str) -> afwf.ScriptFilter:
        sf = afwf.ScriptFilter()
        password_name, field = query.split("@@", 1)
        field = field.strip()
        output = subprocess.check_output([
            lasspass_cli, "show", password_name, "--json",
        ]).decode("utf-8")

        # re-login
        if "Perhaps you need to login with" in output:
            cmd = f"{lasspass_cli} export --sync=now --fields=name > {path_alfred_workflow_name_txt.abspath} && {python_interpreter} {path_user_workflow_main_py} 'build_index_action noquery'"
            item = afwf.Item(
                title="Login expired, hit 'enter' to re-login lastpass",
                arg=cmd,
                icon=afwf.Icon.from_image_file(images.signin)
            )
            item.variables["terminal_command"] = afwf.VarValueEnum.y.value
            item.variables["terminal_command_arg"] = cmd
        # pull password item details
        else:
            data = parse_lpass_show_output_json(output)
            item_list = password_data_to_items(data)
            if field:  # sort by fuzzy search
                fzy = FuzzyObjectSearch(
                    keys=[item.variables["field"] for item in item_list],
                    mapper={item.variables["field"]: item for item in item_list},
                )
                for item in fzy.match(field, limit=20):
                    sf.items.append(item)
            else:  # sort by default order
                for item in item_list:
                    sf.items.append(item)
        return sf

    def lower_level_api(self, query: str) -> afwf.ScriptFilter:
        """
        """
        logger.info(f"received query: {query!r}")
        if not path_lpass_username.exists():
            return self.login_lastpass_cli(query)

        if not path_alfred_workflow_name_index_write_lock.exists():
            return self.create_index()

        query = query.strip()
        if "@@" not in query:
            return self.search_password_item(query)
        else:
            return self.search_password_item_field(query)

    def handler(self, query: str) -> afwf.ScriptFilter:
        return self.lower_level_api(query=query)


handler = Handler(id="password")
