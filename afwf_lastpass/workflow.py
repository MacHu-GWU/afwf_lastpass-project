# -*- coding: utf-8 -*-

"""
workflow handler register.
"""

import afwf
from .hdl import (
    password,
    login,
    build_index,
    build_index_action,
)

wf = afwf.Workflow()
wf.register(password.handler)
wf.register(login.handler)
wf.register(build_index.handler)
wf.register(build_index_action.handler)

