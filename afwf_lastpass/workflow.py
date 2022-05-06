# -*- coding: utf-8 -*-

"""
workflow handler register.
"""

import afwf
from .hdl import (
    password,
    rebuild_index,
    rebuild_index_action,
)

wf = afwf.Workflow()
wf.register(password.handler)
wf.register(rebuild_index.handler)
wf.register(rebuild_index_action.handler)

