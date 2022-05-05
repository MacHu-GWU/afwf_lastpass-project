# -*- coding: utf-8 -*-

"""
detect current runtime.
"""

import os


class Runtime:
    local = "local"
    alfred = "alfred"
    ci = "ci"


IS_LOCAL = False
IS_ALFRED = False
IS_CI = False

if "CI" in os.environ:
    CURRENT_RUNTIME = Runtime.ci
    IS_CI = True
elif "Alfred.alfredpreferences/workflows/user.workflow." in os.path.abspath(__file__):
    CURRENT_RUNTIME = Runtime.alfred
    IS_ALFRED = True
else:
    CURRENT_RUNTIME = Runtime.local
    IS_LOCAL = True
