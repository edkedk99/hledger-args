from typing import Optional, Tuple

from .base_args import BaseArgs


class BatchArgs(BaseArgs):
    def __init__(
        self,
        files: Tuple[str, ...],
        name: Optional[str],
        hledger_options: Tuple[str, str],
    ) -> None:
        super().__init__(files)
        self.name = name
        self.hledger_options = hledger_options
        self.report = self.run_batch()

    @property
    def available_txt(self):
        text = "Available args\n\n"

        text += "No interactive allowed args (Report)\n"
        text += "----------------------------\n"
        no_ask_str = "\n".join(self.no_ask)
        text += no_ask_str + "\n\n"

        if len(self.has_ask) > 0:
            text += "Interactive-only args (Report)\n"
            text += "------------------------------\n"
            has_ask_str = "\n".join(self.has_ask)
            text += has_ask_str + "\n\n"
        return text

    def run_one_for_all(self, name: str, hledger_options: Tuple[str, ...]):
        report = self.run_args(name, hledger_options)
        result = f"""================================

Report: {name}

{report}

"""
        return result

    def run_all(self):
        reports = [
            self.run_one_for_all(self.args[name], self.hledger_options)
            for name in self.no_ask
        ]
        reports_txt = "\n".join(reports) + "================================"
        return reports_txt

    def run_batch(self):
        if not self.name:
            return f"Missing command\n\n{self.available_txt}"
        elif self.name == "all":
            return self.run_all()
        elif self.name not in self.names:
            raise KeyError(f"{self.name} not found.\n\n{self.available_txt}")
        elif self.name in self.has_ask:
            raise KeyError(f"{self.name} is interactive only.\n\n{self.available_txt}")
        else:
            options = self.args[self.name]
            if self.name.startswith("shell_"):
                return self.run_shell(options, self.hledger_options)
            else:
                return self.run_args(options, self.hledger_options)
