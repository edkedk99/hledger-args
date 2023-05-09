import re
import shlex
import subprocess
import sys
from typing import List, Optional, Tuple

from .options import HledgerVars


def get_files_comm(file_path: Tuple[str, ...]) -> List[str]:
    files = []
    for file in file_path:
        files = [*files, "-f", file]
    return files


class BaseArgs:
    NAMESPACE = "args"

    def __init__(self, files: Tuple[str, ...]) -> None:
        self.files = files

        vars = HledgerVars(files)
        self.args = vars.get_namespace_vars(self.NAMESPACE)
        self.names = set(list(self.args.keys()))
        self.has_ask = {
            name for name, var in self.args.items() if re.search(r"\{(.*?)\}", var)
        }
        self.no_ask = self.names.difference(self.has_ask)

        self.files_comm = get_files_comm(files)

    def run_args(self, options: str, extra: Optional[Tuple[str, ...]] = None):
        options_list = shlex.split(options)
        if extra:
            options_list = [*options_list, *extra]

        base_comm = ["hledger", *self.files_comm, *options_list]
        proc = subprocess.run(base_comm, capture_output=True, check=True)
        report = proc.stdout.decode("utf8")

        base_comm_str = shlex.join(base_comm)
        print(f"stderr: {base_comm_str}\n", file=sys.stderr)
        print(report)
