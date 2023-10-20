import sys
from glob import glob
from io import TextIOWrapper
from typing import Dict, List, Tuple

from yaml import dump

NAMESPACE_START = "#+"


def get_vars(f: TextIOWrapper, namespace: str):
    start = NAMESPACE_START + namespace
    start_pos = len(start)

    args_list = [
        row[start_pos:].split(":", 1)
        for row in f
        if row.startswith(start) and ":" in row[start_pos:]
    ]

    args_dicts = {arg[0].strip(): arg[1].strip() for arg in args_list}
    return args_dicts


def get_included(f: TextIOWrapper):
    included_lines = [row.split(" ", 1)[1] for row in f if row.startswith("include ")]
    included_files = [
        file
        for line in included_lines
        for included_list in glob(line, recursive=True)
        for file in included_list
    ]
    return included_files


def get_namespace_vars(files: Tuple[str, ...], namespace: str):
    result: Dict[str, str] = {}
    for file in files:
        with open(file, "r") as f:
            args = get_vars(f, namespace)
            result = {**result, **args}

    return result


def get_namespaces(files: Tuple[str, ...]):
    result: List = []
    for file in files:
        with open(file, "r") as f:
            for row in f:
                pass


if __name__ == "__main__":
    file_name = sys.argv[1]
    namespace = sys.argv[2]

    namespace = get_namespace_vars((file_name,), namespace)
    print(dump(namespace))
