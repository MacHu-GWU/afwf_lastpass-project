# -*- coding: utf-8 -*-

import attr
import afwf

from ..paths import (
    lasspass_cli, path_alfred_workflow_name_txt,
    python_interpreter, path_user_workflow_main_py,
)
from .. import images


@attr.define
class Handler(afwf.Handler):
    def lower_level_api(self, query: str) -> afwf.ScriptFilter:
        """
        """
        sf = afwf.ScriptFilter()
        if len(query):
            item = afwf.Item(
                title=f"Enter username = '{query}' to login",
                icon=afwf.Icon.from_image_file(images.signin),
            )
            cmd = f"{lasspass_cli} login \"{query}\""
            item.variables["terminal_command"] = afwf.VarValueEnum.y.value
            item.variables["terminal_command_arg"] = cmd
        else:
            item = afwf.Item(
                title=f"Enter username to login",
                icon=afwf.Icon.from_image_file(images.signin),
            )
        sf.items.append(item)
        return sf

    def handler(self, query: str = None) -> afwf.ScriptFilter:
        return self.lower_level_api(query=query)


handler = Handler(id="login")
