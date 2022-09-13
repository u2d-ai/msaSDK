# -*- coding: utf-8 -*-
import os
from typing import Dict, List

import aiofiles
from aiofiles import os as asyncos


async def all_dirs_with_subdirs(path, subdirs) -> List:
    # make sure no relative paths are returned, can be omitted
    path: str = os.path.abspath(path)

    result: List = []
    for root, dirs, files in os.walk(path):
        if all(subdir in dirs for subdir in subdirs):
            result.append(root)
            result.extend([subdir for subdir in dirs])
    return result


async def get_directory_listing(path) -> Dict:
    output: Dict = {"text": path, "type": "directory", "children": await all_dirs_with_subdirs(path, ('collector', 'uploads'))}
    return output


async def save_content_to_file(file_name: str, content: str) -> None:
    async with aiofiles.open(file_name, "w") as file:
        await file.write(content)


async def save_binary_to_file(file_name: str, content: bytes) -> None:
    async with aiofiles.open(file_name, "wb") as file:
        await file.write(content)


async def load_content_from_file(file_name: str) -> str:
    async with aiofiles.open(file_name, "r") as file:
        return await file.read()
