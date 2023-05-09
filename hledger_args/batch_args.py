from typing import Optional, Tuple

from .base_args import BaseArgs


class BatchArgs(BaseArgs):
    def __init__(self, files: Tuple[str, ...]) -> None:
        super().__init__(files)

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

    def run_batch(self, name: Optional[str], hledger_options: Tuple[str, str]):
        if not name:
            print(self.available_txt)
            return
        elif name not in self.names:
            raise KeyError(f"{name} not found.\n\n{self.available_txt}")
        elif name in self.has_ask:
            raise KeyError(f"{name} is interactive only.\n\n{self.available_txt}")
        else:
            options = self.args[name]
            self.run_args(options, hledger_options)
