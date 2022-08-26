import os
from typing import Dict, List


def all_dirs_with_subdirs(path, subdirs) -> List:
    # make sure no relative paths are returned, can be omitted
    path: str = os.path.abspath(path)

    result: List = []
    for root, dirs, files in os.walk(path):
        if all(subdir in dirs for subdir in subdirs):
            result.append(root)
            for subdir in dirs:
                result.append(subdir)
    return result


def get_directory_listing(path) -> Dict:
    output: Dict = {"text": path, "type": "directory", "children": all_dirs_with_subdirs(path, ('collector', 'uploads'))}
    return output
