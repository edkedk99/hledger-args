import re
import subprocess
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

import questionary
from prompt_toolkit.shortcuts import CompleteStyle

from .lib import get_files_comm, run_args, run_shell
from .options import get_namespace_vars


def val_date(date: str):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return "Invalid date format"


def val_existing(choices: List[str], value: str):
    if value in choices:
        return True
    else:
        return "Only existing values are accepted"


def custom_autocomplete(name: str, choices: List[str]):
    question = questionary.autocomplete(
        f"{name} (TAB to autocomplete)",
        choices=choices,
        validate=lambda value: val_existing(choices, value),
        ignore_case=True,
        match_middle=True,
        style=questionary.Style([("answer", "fg:#f71b07")]),
        complete_style=CompleteStyle.MULTI_COLUMN,
    )
    return question


def get_hledger_lines(files_comm: List[str], cmds: List[str]):
    base_comm = ["hledger", *files_comm, *cmds]
    proc = subprocess.run(base_comm, capture_output=True, check=True)
    report = proc.stdout.decode("utf8")
    report_list = [line for line in report.split("\n") if line != ""]
    return report_list


def ask_placeholder(files_comm: List[str], placeholder: str) -> str:
    if placeholder == "account":
        choices = get_hledger_lines(files_comm, ["accounts"])
        answer = custom_autocomplete(placeholder, choices).ask()
    elif placeholder == "tag":
        tags = get_hledger_lines(files_comm, ["tags"])
        tag = custom_autocomplete(placeholder, choices=tags).ask()

        tag_values = get_hledger_lines(files_comm, ["tags", tag, "--values"])
        value = custom_autocomplete(f"Value for tag {tag}", choices=tag_values).ask()
        answer = f'"tag:{tag}={value}"'
    elif placeholder.startswith("tag_"):
        tag_name = placeholder.split("_", 1)[1]
        tag_values = get_hledger_lines(files_comm, ["tags", tag_name, "--values"])
        value = custom_autocomplete(
            f"Value for tag {tag_name}", choices=tag_values
        ).ask()
        answer = f'"tag:{tag_name}={value}"'
    elif placeholder == "months":
        initial: str = questionary.text(
            "Initial", instruction="YYYY-MM-DD", validate=val_date
        ).ask()
        final = questionary.text(
            "Final (inclusive)", instruction="YYYY-MM-DD", validate=val_date
        ).ask()
        next_final_date = datetime.strptime(final, "%Y-%m-%d") + timedelta(days=1)
        next_final = next_final_date.strftime("%Y-%m-%d")
        answer = f"--begin {initial} --end {next_final}"
    elif placeholder == "payee":
        choices = get_hledger_lines(files_comm, ["payees"])
        payee = custom_autocomplete(placeholder, choices).ask()
        answer = f'"payee:{payee}"'
    elif placeholder == "cur":
        choices = get_hledger_lines(files_comm, ["commodities"])
        commodity = custom_autocomplete(placeholder, choices).ask()
        answer = f'"cur:{commodity}"'
    elif placeholder == "type":
        types = dict(
            Asset="A",
            Liability="L",
            Equity="E",
            Revenue="R",
            Expense="X",
            Cash="C",
            Conversion="V",
        )
        choices = list(types.keys())
        _type = questionary.select("Account Type", choices=choices).ask()
        type_code = types[_type]
        answer = f'"type:{type_code}"'
    else:
        answer = questionary.text(placeholder).ask()

    return answer


def substitute(files_comm: List[str], match: re.Match):
    placeholder: Optional[str] = match.group(1)
    if placeholder:
        question_desc = placeholder.replace("{", "").replace("}", "")
        answer = ask_placeholder(files_comm, question_desc)
        return answer
    else:
        return ""


def replace_options(files_comm: List[str], options: str):
    result = re.sub(r"\{(.*?)\}", lambda match: substitute(files_comm, match), options)
    return result


def menu(names: List[str]):
    name: str = questionary.select(
        "Choose report",
        choices=names,
        use_shortcuts=True,
        use_indicator=False,
        show_selected=False,
    ).ask()
    return name


def get_inter_report(files: Tuple[str, ...]):
    args = get_namespace_vars(files, "args")
    names = list(args.keys())
    name = menu(names)

    options_str = args[name]
    files_comm = get_files_comm(files)
    replaced = replace_options(files_comm, options_str)

    if name.startswith("shell_"):
        return run_shell(replaced, files[0])
    else:
        return run_args(files, replaced)
