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


## Options

```shell
                                                                               
╭─ Options ────────────────────────────────────────────────────────────────────╮
│                                                                              │
│  *   --file          -f   Pass the journal file path. Can be multiple files  │
│                           (TEXT)                                             │
│                           [required]                                         │
│                                                                              │
│      --interactive   -i   Run in interactive mode by answering prompts.      │
│                           [NAME] is not used in this mode.                   │
│                                                                              │
│      --pdf-file      -o   output the report to the specified file in pdf     │
│                           (FILE)                                             │
│                                                                              │
│      NAME                 (TEXT)                                             │
│                                                                              │
│      --help          -h   Show this message and exit.                        │
│                                                                              │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## Installation

### Dependencies

- python 3.8
- hledger

### Installation command

`pip install --upgrade hledger-args`
