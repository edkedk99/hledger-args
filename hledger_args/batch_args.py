import sys
from typing import Dict, Tuple

from .lib import is_batch, list_commands, run_args, run_shell, title
from .options import get_namespace_vars


def check_name(args: Dict[str, str], name: str):
    batch_args = [name for name, var in args.items() if not is_batch(var)]
    inter_args = [name for name, var in args.items() if is_batch(var)]

    if name in batch_args:
        return

    commands = list_commands(args) + "\n\n"

    if name in inter_args:
        print(commands + f"Command {name} is interactive")
        sys.exit()

    if name not in args.keys():
        print(commands + f"Unknown command {name}")
        sys.exit()


def get_batch_report(files: Tuple[str, ...], name: str, args: Dict[str, str]):
    check_name(args, name)
    options = args[name]
    if name.startswith("shell"):
        run_shell(options, files[0])
        return f"Shell Command: {name}\n"
    else:
        result = title(name) + "\n\n"
        result += run_args(files, options) + "\n"
        return result


def get_batch_reports(files: Tuple[str, ...], names: Tuple[str, ...]):
    args = get_namespace_vars(files, "args")

    if len(names) == 0:
        commands = list_commands(args)
        print(f"{commands}\n\nMissing name")
        sys.exit()

    for name in names:
        check_name(args, name)

    reports = [get_batch_report(files, name, args) for name in names]
    reports_str = "\n".join(reports)
    return reports_str
