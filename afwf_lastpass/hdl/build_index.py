# -*- coding: utf-8 -*-

import sys
import attr
import afwf

from .. import images
from ..paths import path_name_txt, lasspass_cli


@attr.define
class Handler(afwf.Handler):
    def lower_level_api(self, query: str = None) -> afwf.ScriptFilter:
        """
        """
        sf = afwf.ScriptFilter()
        if path_name_txt.exists():
            cmd = f"{sys.executable} main.py 'build_index_action no_query'"
            item = afwf.Item(
                title="Re-build Index for Lastpass Alfred Workflow",
                subtitle="Hit enter to rebuild, it may takes 3 ~ 10 seconds",
                arg=cmd,
                icon=afwf.Icon.from_image_file(images.refresh)
            )
            item.variables["run_bash_script"] = afwf.VarValueEnum.y.value
            item.variables["run_bash_script_arg"] = cmd
            sf.items.append(item)
        else:
            cmd = f"{lasspass_cli} export --sync=now --fields=name > {path_name_txt.abspath}"
            item = afwf.Item(
                title="name.txt file not found!",
                subtitle="Hit enter to create name.txt",
                arg=cmd,
                icon=afwf.Icon.from_image_file(images.plus)
            )
            item.variables["terminal_command"] = afwf.VarValueEnum.y.value
            item.variables["terminal_command_arg"] = cmd
            sf.items.append(item)
        return sf

    def handler(self, query: str = None) -> afwf.ScriptFilter:
        return self.lower_level_api(query=query)


handler = Handler(id="build_index")
