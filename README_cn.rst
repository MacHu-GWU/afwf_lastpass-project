LastPass Alfred Workflow 文档
==============================================================================


简介
------------------------------------------------------------------------------
能找到这里来的肯定是 `Lastpass <https://www.lastpass.com/>`_ 和 `Alfred Workflow <https://www.alfredapp.com/workflows/>`_ 的用户. 都是喜欢 Lastpass 方便的密码管理功能, 以及浏览器网站登录或是手机 App 自动填写密码功能的用户. 而在电脑上搜索 Lastpass 还是要经过: 1. 打开浏览器插件或是桌面版 App -> 2. 点击搜索框 -> 3. 搜索并打开 -> 4. 复制粘贴 等几步. Alfred Workflow 作为 Mac 系统效率大杀器, 用命令行的方式搜索 Lastpass 中的信息并使用明显效率更高. 可惜开源社区里的 `Lastpass Search <https://www.packal.org/workflow/lastpass-search>`_ 项目的作者能力有限, 无论是搜索准确度还是功能都比较粗糙. 所以我决定自己用 Python 写一个功能更强, 代码质量更高, 扩展能力更强的 Workflow. 叫做 ``afwf_lastpass``.


工作原理
------------------------------------------------------------------------------
Lastpass 官方有一个 `命令行工具 <https://github.com/lastpass/lastpass-cli>`_. 功能主要是能安全的登录 (不要重新自己发明加密工具!), 并对 Lastpass 中的 Item 进行基于完全匹配 (不支持容错) 的查询. 给定一个 name, 返回这个 password 下的 url, username, password, note 等信息.

而 ``afwf_lastpass`` 则是基于 lastpass-cli, 先把所有的 name 用 ``lpass export --fields=name`` 命令缓存到本地, 然后用 Python 中的 Full text search 大杀器 `whoosh <https://github.com/mchaput/whoosh>`_ (是一个无服务器, 纯本地文件, 高性能的 Elasticsearch) 对其进行全文索引. 一旦索引构建成功, 在 Alfred 的搜索框中输入字符就可以对 item 进行搜索, 并且显示每个 password item 的 key, value 详细信息. 我们可以定义一些快捷键操作比如: Enter, Ctrl + C, Cmd + Enter, Alt + Enter, Shift + Enter 等操作对应不同的效果.


如何使用
------------------------------------------------------------------------------
**安装**

1. 首先你要安装 `lastpass-cli <https://github.com/lastpass/lastpass-cli>`_, 建议使用 homebrew 安装:

.. code-block:: bash

    # 用 homebrew 安装 lastpass cli
    brew update
    brew install lastpass-cli

2. 然后你要登录你的 Lastpass, **这步非常重要, 在每个新电脑上这个事情只需要做一次就可以永久生效**:

.. code-block:: bash

    # 登录
    lpass login ${your_lastpass_username_should_be_your_email}

    # 将加密后的数据 sync 到本地
    lpass sync

3. 然后安装 ``afwf_lastpass``, 到 `release <https://github.com/MacHu-GWU/afwf_lastpass-project/releases>`_ 下载最新的安装包 (请注意区分 Intel 和 M1 芯片的 Mac), 双击安装即可.

4. 这个 Workflow 是基于 Python3 的, 如果你用的是比较旧的 Mac 系统, 可能没有 ``/usr/bin/python3`` 那么你需要自行用 homebrew 安装 python3, 然后再 workflow 里的 script filter 中将 script 改成 ``/path/to/your/python3``

5. 在 Alfred 中用 ``lp-sync-name`` keyword 获取最新的 item name 列表. 如果你对 lastpass 中的密码进行了改动, 你又想获得最新的数据, 那么你就需要用这个命令更新数据.

6. 在 Alfred 中用 ``lp-build-index`` keyword 重新构建索引.

7. 现在你可以在 Alfred 中用 ``pw ${query}`` 对密码进行搜索了.

**进阶使用**

我们假设你有一个 ``alice@gmail.com`` 的 gmail 邮箱, 你给这个 password 取名为 ``Alice Gmail``.

1. 那么你可以在 Alfred 中输入: ``pw ali`` 或者 ``pw gma ali``, 甚至连续的任意匹配字符都行 ``pw mail``, 你都会在下拉菜单中看到结果.
2. 选中结果按 ``Tab`` auto complete, 你就能看到这个 password 的详细信息, 包括 name, folder, username, password, url, note. 默认 name 会在第一个.
3. 默认是你按回车则会在光标所在的地方, 比如密码输入框处输入密码. 按 Cmd + Enter 则是拷贝密码, 按 Alt + Enter 则是打开 Url.
