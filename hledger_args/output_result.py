from datetime import datetime
from pathlib import Path
from typing import Optional, Union

from fpdf import FPDF

from .batch_args import BatchArgs
from .inter_args import InteractiveArgs


def create_pdf(header: str, text: str, output_path: Path):
    pdf = FPDF()
    pdf.add_page(orientation="L")
    pdf.set_font("Courier", "", 12)

    pdf.multi_cell(0, None, header, ln=True)
    lines = text.split("\n")

    for line in lines:
        if pdf.get_y() > pdf.h - 20:
            pdf.add_page()
        pdf.cell(0, None, line, ln=True)

    pdf.output(str(output_path))


def output_report(
    args: Union[BatchArgs, InteractiveArgs],
    pdf_dir: Optional[str],
    pdf_file: Optional[str],
):
    if pdf_file:
        file_dest = Path(pdf_file)
    elif pdf_dir:
        today = datetime.today().strftime("%Y%m%d")
        file_dir = Path(pdf_dir).joinpath(today)
        file_dir.mkdir(parents=True, exist_ok=True)
        name = args.name or "empty"
        file_dest = file_dir.joinpath(f"{name}.pdf")
    else:
        print(args.report or "")
        return

    header = f"""Report: {args.name}
_________________

"""

    if args.report:
        create_pdf(header, args.report, file_dest)
