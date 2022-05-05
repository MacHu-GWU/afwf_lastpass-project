# -*- coding: utf-8 -*-

from pathlib_mate import Path

dir_home = Path.home()

dir_alfred_workflow = Path(dir_home, ".alfred-afwf_lastpass")
dir_cache = Path(dir_alfred_workflow, ".cache")
dir_name_index = Path(dir_alfred_workflow, "name_index")
path_python_interpreter = Path(dir_alfred_workflow, "python_interpreter")

dir_here = Path.dir_here(__file__)
dir_project_root = dir_here.parent
dir_cache_for_test = Path(dir_project_root, "tests", ".cache")
dir_name_index_for_test = Path(dir_project_root, "tests", "name_index")
path_name_json_for_test = Path(dir_here, "tests", "repos.json")

dir_alfred_workflow.mkdir_if_not_exists()
