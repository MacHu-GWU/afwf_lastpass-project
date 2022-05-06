# -*- coding: utf-8 -*-

from typing import List, Dict, Iterable

import attr
import afwf

from ..fts import search_name
from ..lpass import password_name_to_items
from ..fuzzy_filter import FuzzyObjectSearch


@attr.define
class Handler(afwf.Handler):
    def lower_level_api(self, query: str) -> afwf.ScriptFilter:
        """

        :param kwargs:
        :return:
        """
        sf = afwf.ScriptFilter()
        query = query.strip()
        if not query:
            sf.items.append(afwf.Item(
                title="Type to search lastpass ...",
            ))
            return sf

        if "@@" in query:
            password_name, field = query.split("@@", 1)
            field = field.strip()
            if field:
                item_list = password_name_to_items(password_name)
                fzy = FuzzyObjectSearch(
                    keys=[item.variables["field"] for item in item_list],
                    mapper={item.variables["field"]: item for item in item_list},
                )
                for item in fzy.match(field, limit=20):
                    sf.items.append(item)
            else:
                item_list = password_name_to_items(password_name)
                for item in item_list:
                    sf.items.append(item)

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
                        autocomplete=name + "@@",
                        arg=name,
                    )
                    sf.items.append(item)
        return sf

    def handler(self, query: str) -> afwf.ScriptFilter:
        return self.lower_level_api(query=query)


handler = Handler(id="password")
