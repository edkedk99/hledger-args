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
        namespace_args = HledgerVars(files, self.NAMESPACE).vars

        self.args = {
            key: value.replace("[file]", self.files[0])
            for key, value in namespace_args.items()
        }
        self.names = list(self.args.keys())
        self.has_ask = {
            name for name, var in self.args.items() if re.search(r"\{(.*?)\}", var)
        }
        self.no_ask = set(self.names).difference(self.has_ask)

        self.files_comm = get_files_comm(files)

    def run_args(self, options: str, extra: Optional[Tuple[str, ...]] = None):
        options_list = shlex.split(options)
        if extra:
            options_list = [*options_list, *extra]

        base_comm = ["hledger", *self.files_comm, *options_list]
        base_comm_str = shlex.join(base_comm)

        proc = subprocess.run(base_comm, capture_output=True)
        if proc.returncode == 0:
            report = proc.stdout.decode("utf8")
            print(f"stderr: {base_comm_str}\n", file=sys.stderr)
            return report
        else:
            err = proc.stderr.decode("utf8")
            raise ValueError(f"\n\ncommand: {base_comm_str}\n\n{err}")

    def run_shell(self, options: str, extra: Optional[Tuple[str, ...]] = None):
        options_list = shlex.split(options)
        if extra:
            options_list = [*options_list, *extra]

        base_comm_str = shlex.join(options_list)
        print(f"stderr: {base_comm_str}\n", file=sys.stderr)

        subprocess.run(options_list, capture_output=False, input=None)
