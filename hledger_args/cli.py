from typing import Optional, Tuple

import rich_click as click

from .batch_args import get_batch_reports
from .inter_args import get_inter_report
from .lib import create_pdf, get_default_file

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
    default=lambda: get_default_file,
    multiple=True,
    help="Pass the journal file path. Can be multiple files",
)
@click.option(
    "-i",
    "--interactive",
    is_flag=True,
    required=False,
    help="Run in interactive mode by answering prompts. [NAME] is not used in this mode.",
)
@click.option(
    "-o",
    "--pdf-file",
    type=click.Path(file_okay=True, dir_okay=False),
    required=False,
    help="output the report to the specified file in pdf",
)
@click.argument("name", type=click.STRING, required=False, nargs=-1)
def cli(
    file: Tuple[str, ...],
    interactive: bool,
    name: Tuple[str, str],
    pdf_file: Optional[str],
):
    """
    # hledger-args

    This package is a replacement for [hledger command file](https://hledger.org/1.29/hledger.html#command-arguments) with additional features.

    ## Basic Usage

    - Save commands directly in the journal file using the custom directive format below.
    - List available commands with *--file* option without additional name argument
    - Pass multiple command names to output the reports
    - Use option *--pdf-file* to save the reports as pdf

    ## Interactive Mode

    Select the report from a menu using the flag *--interactive*.

    Using *placeholders* as below, the user can create a report asking multiple additional information on runtime that read the journal files to provide fuzzy search autocompletion, validation and other conveniences.

    ### Placeholder Command Substitution

     In *Interactive Mode* only, a command can use placeholders by putting them between *curly braces* and additional prompts wil ask for the value and do the proper substitution.

    For example, *{example_placeholder}* will ask for this value and substitute where it is located in the command saved in the journal file.

    Some placehoder's name offers additional features

    #### Special Placeholders

    - **{account}** : Fuzzy search existing accounts
    - **{payee}**   : Fuzzy search existing payees
    - **{cur}**     : Fuzzy search existing commodities
    - **{tag}**     : Fuzzy search existing tags and values
    - **{tag_name}**: Search tag name after "_" and fuzzy search existing values for this tag
    - **{months}**  : Prompt initial and end dates both inclusive. **Diferent from default hledger**
    - **{type}**    : Select between accounts type

     ## Shell Commands

    Commands name using *{shell_name}* doesn't run hledger by default. It can accept any shell command and receive aditional data from TUI programs with dialog, menus, etc.

    > Placeholder **[file]** subtitute for the path of the first file informed with *--file* option.

    > Can not save to pdf file. Only output to stdout.

     ## Sub directive format

     ```text
     #+args [command name]:[hledger options]
     #+args [other command_name]:[other hledger options]
     ```

     **Example**:

     ```text
     #+args buy_aapl:bal desc:\"Buy AAPL\"
     #+args aapl_cur:bal desc:\"Buy AAPL\" cur:{commodity}
    ```

     ---

     **[NAME]**: Command names to run saved in the journal sub directives. Not available in Interactive mode

     ---

    """

    if interactive:
        output = get_inter_report(file)
    else:
        output = get_batch_reports(file, name)

    if pdf_file:
        create_pdf(output or "", pdf_file)
        print(f"Report saved on {pdf_file}")
    else:
        click.echo(output)
