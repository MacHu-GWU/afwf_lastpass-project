.. image:: https://readthedocs.org/projects/afwf_lastpass/badge/?version=latest
    :target: https://afwf_lastpass.readthedocs.io/index.html
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/afwf_lastpass-project/workflows/CI/badge.svg
    :target: https://github.com/MacHu-GWU/afwf_lastpass-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/afwf_lastpass-project/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/afwf_lastpass-project

.. image:: https://img.shields.io/pypi/v/afwf_lastpass.svg
    :target: https://pypi.python.org/pypi/afwf_lastpass

.. image:: https://img.shields.io/pypi/l/afwf_lastpass.svg
    :target: https://pypi.python.org/pypi/afwf_lastpass

.. image:: https://img.shields.io/pypi/pyversions/afwf_lastpass.svg
    :target: https://pypi.python.org/pypi/afwf_lastpass

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/afwf_lastpass-project

------


.. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://afwf_lastpass.readthedocs.io/index.html

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://afwf_lastpass.readthedocs.io/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Source_Code-blue.svg
    :target: https://afwf_lastpass.readthedocs.io/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/afwf_lastpass-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/afwf_lastpass-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/afwf_lastpass-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/afwf_lastpass#files


Welcome to ``afwf_lastpass`` Documentation
==============================================================================
Documentation for ``afwf_lastpass``. See README_cn.rst for better doc


How it Work
------------------------------------------------------------------------------
`lastpass has a CLI interface <https://github.com/lastpass/lastpass-cli>`_ allow you to securely login, and retrieve lastpass data.


How to Use
------------------------------------------------------------------------------
- All lastpass item including "Password with URL", "Secure Note", "Driver's License" are just a Form having a field called ``name``
- First, you **SEARCH** the lastpass item based on ``name``, it support full text search, ngram search
- Second, once you locate an item, then you can do **ACTION** like, enter the password, copy the value of the form, open URL in browser.

How to SEARCH::

1. call out Alfred input box, and enter the keyword ``pw``, then enter ``pw {query}`` to search
2. select the desired item using mouse or ``up``, ``down``, then hit 'Tab' to lock this item. Once you lock the item, then you can take action.

How to do ACTION::

1. by default, the ``name`` field is always on top.
2. Hit 'Enter': type the secret at current focus cursor. The secret is different based on
3. Hit 'CMD + Enter': copy the secret to clipboard
4. Hit 'Alt (Option) + Enter': open the URL in browser (if available)
5. type more to select different field
6. if you are on field other than ``name``, you can hit 'Ctrl + C' to copy the value to clipboard.
