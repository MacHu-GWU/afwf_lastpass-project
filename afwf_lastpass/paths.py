# -*- coding: utf-8 -*-

from pathlib_mate import Path

dir_home = Path.home()

dir_alfred_workflow = Path(dir_home, ".alfred-afwf_lastpass")
dir_cache = Path(dir_alfred_workflow, ".cache")
dir_name_index = Path(dir_alfred_workflow, "name_index")
path_name_txt = Path(dir_alfred_workflow, "name.txt")
path_lastpass_cli = Path(dir_alfred_workflow, "lastpass_cli")
path_log_txt = Path(dir_alfred_workflow, "log.txt")

dir_here = Path.dir_here(__file__)
dir_project_root = dir_here.parent
dir_cache_for_test = Path(dir_project_root, "tests", ".cache")
dir_name_index_for_test = Path(dir_project_root, "tests", "name_index")
path_name_txt_for_test = Path(dir_project_root, "tests", "name.txt")

dir_alfred_workflow.mkdir_if_not_exists()


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
            path_lastpass_cli.write_text(p)
            return p
    raise FileNotFoundError


if path_lastpass_cli.exists():
    lasspass_cli: str = path_lastpass_cli.read_text().strip()
else:
    lasspass_cli: str = find_lastpass_cli()
    path_lastpass_cli.write_text(lasspass_cli)
