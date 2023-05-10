import re
import subprocess
from typing import List, Optional, Tuple
from datetime import datetime, timedelta
import questionary
from prompt_toolkit.shortcuts import CompleteStyle

from .base_args import BaseArgs


def custom_autocomplete(name: str, choices: List[str]):
    question = questionary.autocomplete(
        f"{name} (TAB to autocomplete)",
        choices=choices,
        ignore_case=True,
        match_middle=True,
        style=questionary.Style([("answer", "fg:#f71b07")]),
        complete_style=CompleteStyle.MULTI_COLUMN,
    )
    return question


def val_date(date: str):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return "Invalid date format"


class InteractiveArgs(BaseArgs):
    def __init__(self, files: Tuple[str, ...]) -> None:
        super().__init__(files)

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
            answer = f"\"tag:{tag}={value}\""
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
            answer = f"\"payee:{payee}\""
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
        name = questionary.select(
            "Choose report",
            choices=list(self.names),
            use_shortcuts=True,
            use_indicator=False,
            show_selected=False,
        ).ask()

        options_str = self.args[name]
        replaced = self.replace_options(options_str)
        self.run_args(replaced)
