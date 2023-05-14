from typing import Optional, Tuple

import rich_click as click

from hledger_args.output_result import output_report

from .batch_args import BatchArgs
from .inter_args import InteractiveArgs

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

click.rich_click.USE_MARKDOWN = True
click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.GROUP_ARGUMENTS_OPTIONS = True
click.rich_click.MAX_WIDTH = 80
click.rich_click.SHOW_METAVARS_COLUMN = False
click.rich_click.APPEND_METAVARS_HELP = True
click.rich_click.STYLE_ERRORS_SUGGESTION = "magenta italic"
click.rich_click.ERRORS_SUGGESTION = (
    "Try running the '--help' flag for more information."
)
click.rich_click.ERRORS_EPILOGUE = "To find out more, visit [link=https://github.com/edkedk99/hledger-args]https://github.com/edkedk99/hledger-args[/link]"
click.rich_click.STYLE_OPTIONS_TABLE_LEADING = 1
click.rich_click.STYLE_OPTIONS_TABLE_BOX = "SIMPLE"
click.rich_click.STYLE_OPTIONS_PANEL_BORDER = "dim"  # Possibly conceal


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-f",
    "--file",
    type=click.STRING,
    required=True,
    help="Inform the journal file path",
)
@click.option(
    "-i",
    "--interactive",
    is_flag=True,
    required=False,
    help="Run in interactive mode by answering the prompts. [NAME] and [EXTRA_HLEDGER_OPTIONS] are not used in this mode.",
)
@click.option(
    "-d",
    "--pdf-dir",
    type=click.Path(
        file_okay=False,
        dir_okay=True,
    ),
    required=False,
    help="Save the report to a folder named according to the current date under the specified directory",
)
@click.option(
    "-o",
    "--pdf-file",
    type=click.Path(file_okay=True, dir_okay=False),
    required=False,
    help="output the report to the specified file in pdf",
)
@click.argument("name", type=click.STRING, required=False)
@click.argument("extra_hledger_options", nargs=-1)
def cli(
    file: str,
    interactive: bool,
    name: str,
    extra_hledger_options: Tuple[str, ...],
    pdf_dir: Optional[str],
    pdf_file: Optional[str],
):
    """
     ---

     **NAME**: Command name to run saved in the journal sub directives. Not available in Interactive mode

    **EXTRA_HLEDGER_OPTIONS**: Extra options to send to hledger command. Not available in Interactive mode. The name **"all"** is special and output all the *no interactive* commands.

     ---

     In basic usage, this package is a replacement for [hledger argument file](https://hledger.org/1.29/hledger.html#command-arguments) using custom directives inside the journal file, instead of referencing to an argument file

     **Interactive Mode**: Instead of giving the desired command thru a command-line argument, choose it by selecting from a menu using the flag *--interactive*

     **Placeholder Command Substitution**: In Interactive Mode, a command can use placeholders by putting them between *curly braces* and additional prompts wil ask for the value and do the proper substitution

     **Special Placeholders**: *{account}, {payee}, {tag}, {tag_name}, {months}, {type}, {cur}* are special placeholders that offers autocomplete with fuzzy search using data from the journal. See the [README](https://github.com/edkedk99/hledger-args) for explanation on each of them

     **Sub directive format**:

     ```text
     #+args [command name]:[hledger options]
     #+args [other command_name]:[other hledger options]
     ```

     **Example**:

     ```text
     #+args buy_aapl:bal desc:\"Buy AAPL\"
     #+args aapl_cur:bal desc:\"Buy AAPL\" cur:{commodity}
    ```
    """

    if interactive:
        args = InteractiveArgs((file,))
    else:
        args = BatchArgs((file,), name, extra_hledger_options)

    output_report(args, pdf_dir, pdf_file)
