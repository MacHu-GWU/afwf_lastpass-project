# -*- coding: utf-8 -*-

"""
Full text search helpers.
"""

import shutil
from typing import List

from pathlib_mate import Path
from diskcache import Cache
from whoosh.index import open_dir, create_in, exists_in, FileIndex
from whoosh.fields import SchemaClass, TEXT, NGRAM, STORED
from whoosh.qparser import MultifieldParser

from .paths import dir_name_index
from .cache import cache


def get_index(
    path: Path,
    schema: SchemaClass,
    reset=True,
) -> FileIndex:
    if reset:
        try:
            shutil.rmtree(path.abspath)
        except:
            pass
    path.mkdir_if_not_exists()
    if exists_in(path.abspath):
        return open_dir(path.abspath)
    else:
        return create_in(dirname=path.abspath, schema=schema)


class PasswordNameSchema(SchemaClass):
    name = STORED()
    name_text = TEXT(stored=False)
    name_ngram = NGRAM(minsize=2, maxsize=10)


password_name_schema = PasswordNameSchema()


def rebuild_name_index(
    dir_index: Path = dir_name_index,
    name_list: List[str] = None,
):
    """
    Read data from cache, insert into whoosh index.
    """
    if name_list is None:
        return

    dir_name_index.remove_if_exists()
    index = get_index(dir_index, password_name_schema, reset=True)
    with index.writer(limitmb=128) as writer:
        for name in name_list:
            writer.add_document(
                name=name,
                name_text=name,
                name_ngram=name,
            )


def search_name(
    q: str,
    dir_index: Path = dir_name_index,
) -> List[dict]:
    index = get_index(dir_index, password_name_schema, reset=False)
    docs = list()
    with index.searcher() as sr:
        query = MultifieldParser(
            ["name_text", "name_ngram"],
            schema=password_name_schema,
        ).parse(q)
        results = sr.search(query, limit=20)
        for hit in results:
            doc = hit.fields()
            docs.append(doc)
    return docs
