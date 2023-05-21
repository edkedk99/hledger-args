import re
import subprocess
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

import questionary
from prompt_toolkit.shortcuts import CompleteStyle

from .base_args import BaseArgs


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


class InteractiveArgs(BaseArgs):
    def __init__(self, files: Tuple[str, ...]) -> None:
        super().__init__(files)
        self.name = self.menu()
        self.report = self.get_report()

    def ask_placeholder(self, placeholder: str) -> str:
        if placeholder == "account":
            choices = self.get_hledger_lines(["accounts"])
            answer = custom_autocomplete(placeholder, choices).ask()
        elif placeholder == "tag":
            tags = self.get_hledger_lines(["tags"])
            tag = custom_autocomplete(placeholder, choices=tags).ask()

            tag_values = self.get_hledger_lines(["tags", tag, "--values"])
            value = custom_autocomplete(
                f"Value for tag {tag}", choices=tag_values
            ).ask()
            answer = f'"tag:{tag}={value}"'
        elif placeholder.startswith("tag_"):
            tag_name = placeholder.split("_", 1)[1]
            tag_values = self.get_hledger_lines(["tags", tag_name, "--values"])
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
            choices = self.get_hledger_lines(["payees"])
            payee = custom_autocomplete(placeholder, choices).ask()
            answer = f'"payee:{payee}"'
        elif placeholder == "cur":
            choices = self.get_hledger_lines(["commodities"])
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

    def substitute(self, match: re.Match):
        placeholder: Optional[str] = match.group(1)
        if placeholder:
            question_desc = placeholder.replace("{", "").replace("}", "")
            answer = self.ask_placeholder(question_desc)
            return answer
        else:
            return ""

    def replace_options(self, options: str):
        result = re.sub(r"\{(.*?)\}", self.substitute, options)
        return result

    def get_hledger_lines(self, cmds: List[str]):
        base_comm = ["hledger", *self.files_comm, *cmds]
        proc = subprocess.run(base_comm, capture_output=True, check=True)
        report = proc.stdout.decode("utf8")
        report_list = [line for line in report.split("\n") if line != ""]
        return report_list

    def menu(self):
        name: str = questionary.select(
            "Choose report",
            choices=list(self.names),
            use_shortcuts=True,
            use_indicator=False,
            show_selected=False,
        ).ask()
        return name

    def get_report(self):
        options_str = self.args[self.name]
        replaced = self.replace_options(options_str)

        if self.name.startswith("shell_"):
            return self.run_shell(replaced)
        else:
            return self.run_args(replaced)
