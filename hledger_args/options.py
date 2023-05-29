from typing import Dict, Optional, Tuple


class HledgerVars:
    NAMESPACE_START = "#+"

    def __init__(self, files: Tuple[str, ...], namespace: str):
        self.files = files
        self.namespace = namespace
        self.vars = self.get_namespace_vars()

    def get_row_comm(self, row: str, namespace: str) -> Optional[Tuple[str, str]]:
        start = self.NAMESPACE_START + namespace
        if not row.startswith(start):
            return

        var_list = row[len(start) :].strip().split(":", 1)
        if len(var_list) == 2:
            return tuple(var_list)

    def get_file_vars(self, file: str, namespace: str):
        with open(file, "r") as f:
            args = [self.get_row_comm(row, namespace) for row in f]
            valid_args = [arg for arg in args if arg]
            args_dict = {name: command for name, command in valid_args}
            return args_dict

    def get_namespace_vars(self):
        result: Dict[str, str] = {}
        for file in self.files:
            file_vars = self.get_file_vars(file, self.namespace)
            if file_vars:
                result = {**result, **file_vars}

        return result
