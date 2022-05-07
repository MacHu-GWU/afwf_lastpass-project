# -*- coding: utf-8 -*-

import attr
import afwf

from ..paths import lasspass_cli
from .. import images

@attr.define
class Handler(afwf.Handler):
    def lower_level_api(self, query: str = None) -> afwf.ScriptFilter:
        """
        """
        sf = afwf.ScriptFilter()
        cmd = f"{lasspass_cli} login"
        item = afwf.Item(
            title="Re-Login lastpass",
            subtitle="Hit enter to re-login lastpass",
            arg=cmd,
            icon=afwf.Icon.from_image_file(images.signin)
        )
        item.variables["terminal_command"] = afwf.VarValueEnum.y.value
        item.variables["terminal_command_arg"] = cmd
        sf.items.append(item)
        return sf

    def handler(self, query: str = None) -> afwf.ScriptFilter:
        return self.lower_level_api(query=query)


handler = Handler(id="login")
