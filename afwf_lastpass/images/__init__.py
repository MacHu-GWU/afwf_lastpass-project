# -*- coding: utf-8 -*-

from pathlib_mate import Path

_dir_here = Path.dir_here(__file__)

lastpass = Path(_dir_here, "lastpass.png").abspath
plus = Path(_dir_here, "plus.png").abspath
refresh = Path(_dir_here, "refresh.png").abspath
signin = Path(_dir_here, "signin.png").abspath
sync = Path(_dir_here, "sync.png").abspath
