# -*- coding: utf-8 -*-

import sys
from loguru import logger
from .paths import path_log_txt

logger.remove()
logger.add(sys.stderr)
logger.add(path_log_txt.abspath, rotation="10 MB", retention="30 days")
