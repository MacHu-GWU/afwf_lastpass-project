# -*- coding: utf-8 -*-

from diskcache import Cache
from .paths import dir_alfred_workflow_cache

cache = Cache(dir_alfred_workflow_cache.abspath)
DEFAULT_EXPIRE = 30 * 24 * 3600
