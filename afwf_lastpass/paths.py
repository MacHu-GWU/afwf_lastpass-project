# -*- coding: utf-8 -*-

import sys
from pathlib_mate import Path
from .runtime import IS_LOCAL, IS_ALFRED

dir_home = Path.home()

dir_alfred_workflow = Path(dir_home, ".alfred-afwf_lastpass")
dir_alfred_workflow_cache = Path(dir_alfred_workflow, ".cache")
dir_alfred_workflow_name_index = Path(dir_alfred_workflow, "name_index")
path_alfred_workflow_name_index_write_lock = Path(dir_alfred_workflow_name_index, "MAIN_WRITELOCK")
path_alfred_workflow_name_txt = Path(dir_alfred_workflow, "name.txt")
path_alfred_workflow_lastpass_cli_txt = Path(dir_alfred_workflow, "lastpass_cli.txt")
path_alfred_workflow_log_txt = Path(dir_alfred_workflow, "log.txt")

dir_lpass = Path(dir_home, ".lpass")
path_lpass_username = Path(dir_home, ".lpass", "username")

dir_here = Path.dir_here(__file__)
dir_project_root = dir_here.parent
dir_tests = Path(dir_project_root, "tests")
dir_tests_cache = Path(dir_project_root, "tests", ".cache")
dir_tests_name_index = Path(dir_project_root, "tests", "name_index")
path_tests_name_txt = Path(dir_project_root, "tests", "name.txt")
path_tests_lastpass_cli_txt = Path(dir_project_root, "tests", "name.txt")

dir_alfred_workflow.mkdir_if_not_exists()
dir_lpass.mkdir_if_not_exists()


def find_lastpass_cli() -> str:
    """
    Find the full path of the lastpass cli.

    See also: https://github.com/lastpass/lastpass-cli
    """
    lpass_locations = [
        "/usr/bin/lpass",
        "/usr/local/bin/lpass",
        "/opt/local/bin/lpass",
        "/opt/homebrew/bin/lpass",
    ]
    for p in lpass_locations:
        if Path(p).exists():
            path_alfred_workflow_lastpass_cli_txt.write_text(p)
            return p
    raise FileNotFoundError


python_interpreter = sys.executable
if path_alfred_workflow_lastpass_cli_txt.exists():
    lasspass_cli: str = path_alfred_workflow_lastpass_cli_txt.read_text().strip()
else:
    lasspass_cli: str = find_lastpass_cli()
    path_alfred_workflow_lastpass_cli_txt.write_text(lasspass_cli)

if IS_LOCAL:
    dir_user_workflow = "/tmp/not-user-workflow"
elif IS_ALFRED:
    dir_user_workflow = dir_here.parent.parent
else:
    raise NotImplementedError

path_user_workflow_main_py = Path(dir_user_workflow, "main.py")
