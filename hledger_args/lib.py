import os
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

from fpdf import FPDF


def get_default_file():
    ledger_file = os.getenv("LEDGER_FILE")
    if ledger_file:
        return (ledger_file,)

    default_path = Path.home() / ".hledger.journal"
    if default_path.exists():
        return (str(default_path),)


def create_pdf(text: str, output_path: str):
    pdf = FPDF()
    pdf.add_page(orientation="L")
    pdf.set_font("Courier", "", 12)

    pdf.multi_cell(0, None, "Report", ln=True)
    lines = text.split("\n")

    for line in lines:
        if pdf.get_y() > pdf.h - 20:
            pdf.add_page()
        if line == "":
            pdf.cell(0, 6, ln=True)
        else:
            pdf.cell(0, None, line, ln=True)

    pdf.output(output_path)


def is_batch(var: str):
    test_batch = re.search(r"\{(.*?)\}", var)
    if test_batch is None:
        return False
    else:
        return True


def title(txt: str):
    txt_len = len(txt)
    under = "-" * txt_len
    result = f"{txt}\n{under}"
    return result


def list_commands(args: Dict[str, str]):
    batch_args = [name for name, var in args.items() if not is_batch(var)]
    inter_args = [name for name, var in args.items() if is_batch(var)]

    batch_str = "\n".join(batch_args)
    inter_str = "\n".join(inter_args)

    output = f"""
{title('Interactive Commands')}
{inter_str}

{title('Batch Commands')}
{batch_str}
"""

    return output


def get_files_comm(file_path: Tuple[str, ...]) -> List[str]:
    files = []
    for file in file_path:
        files = [*files, "-f", file]
    return files


def run_args(files: Tuple[str, ...], options: str):
    files_comm = get_files_comm(files)
    options_list = shlex.split(options)
    base_comm = ["hledger", *files_comm, *options_list]
    base_comm_str = shlex.join(base_comm)

    proc = subprocess.run(base_comm, capture_output=True)
    if proc.returncode == 0:
        report = proc.stdout.decode("utf8")
        print(f"stderr: {base_comm_str}\n", file=sys.stderr)
        return report
    else:
        err = proc.stderr.decode("utf8")
        print(f"\n\ncommand: {base_comm_str}\n\n{err}")
        sys.exit()


def run_shell(options: str, first_file: str):
    options_replaced = options.replace("[file]", first_file)
    options_list = shlex.split(options_replaced)
    print(f"stderr: {options}\n", file=sys.stderr)

    subprocess.run(options_list, capture_output=False, input=None)
