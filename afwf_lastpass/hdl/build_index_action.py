# -*- coding: utf-8 -*-

import attr
import afwf

from ..fts import rebuild_name_index
from ..lpass import parse_name_txt


@attr.define
class Handler(afwf.Handler):
    def handler(self, query: str = None) -> afwf.ScriptFilter:
        rebuild_name_index(name_list=parse_name_txt())
        return afwf.ScriptFilter()


handler = Handler(id="build_index_action")
