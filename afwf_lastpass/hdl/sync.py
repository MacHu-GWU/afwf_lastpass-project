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
    def lower_level_api(self, query: str = None) -> afwf.ScriptFilter:
        """
        """
        sf = afwf.ScriptFilter()
        cmd = f"{lasspass_cli} export --sync=now --fields=name > {path_alfred_workflow_name_txt.abspath} && {python_interpreter} {path_user_workflow_main_py} 'build_index_action noquery'"
        item = afwf.Item(
            title="Sync lastpass data, hit 'enter' to run",
            arg=cmd,
            icon=afwf.Icon.from_image_file(images.sync)
        )
        item.variables["terminal_command"] = afwf.VarValueEnum.y.value
        item.variables["terminal_command_arg"] = cmd
        sf.items.append(item)
        return sf

    def handler(self, query: str = None) -> afwf.ScriptFilter:
        return self.lower_level_api(query=query)


handler = Handler(id="sync")
