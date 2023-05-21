# hledger-args

## Description

In basic usage, this package is a replacement for [hledger command file](https://hledger.org/1.29/hledger.html#command-arguments) using custom directives inside the journal file, instead of referencing to a command args file.

In interactive mode, the user can create menus using placeholders. Each placeholders will become a prompt and be replaced by the value entered. So the user will be able to create a multi prompt report composed by fixed options already defined and leave some to the user each time this package is executed.

### Interactive Mode

Instead of giving the the desired command thru a command-line argument, choose it by selecting from a menu using the flag *--interactive*

### Special placeholders

| Placeholders | Description                                                                    |
|--------------|--------------------------------------------------------------------------------|
| {account}    | fuzzy search existing accounts                                                 |
| {payee}      | fuzzy search existing payee                                                    |
| {tag}        | fuzzy search existing tags and values                                          |
| {tag_name}   | search tag name after "_" and fuzzy search existing values for this tag        |
| {months}     | prompt initial and end dates both inclusive. **Diferent from default hledger** |
| {type}       | select between accounts type                                                   |
| {cur}        | fuzzy search existing commodities                                              |

### Non hledger commands

It is possible to run other commands beside the default *hledger*. For that, name the arg as /shell_name/ and /hledger-args/ will execute it according to the conditions:

- It can accept inputs from the terminal stdin.
- The string /[file]/ will be replaces by the name of the "--file" option.
- It will not be saved in PDF report

It is useful if you want to add a command that doesn't use hledger but needs the file name being used.

### PDF output.

There are two ways to output the reports to pdf:

- Option **--pdf-file**: Save the report to the specified file.
- Option **--pdf-dir**: Save the report to a directory named after the current date under the specified directory. Creates it if doesn't exist. Should be used to keep a history of generated reports.


## Installation

### Dependencies

- python 3.8
- hledger

### Installation command

`pip install --upgrade hledger-args`

## Sub directive

Add lines according to the format below:

```text
     #+args [command name]:[hledger options]
     #+args [other command_name]:[other hledger options]
```

### Examples/Data

```text
     #+args buy_aapl:bal desc:\"Buy AAPL\"
     #+args aapl_cur:bal desc:\"Buy AAPL\" cur:{commodity}
```

## Usage

After adding the commands using sub directives, run `hledger-args -f [journal file]`. Without any option or argument, it output the existing ones divided between *interactive* and *non interactive*. Those with *placeholders* can only be on interactive-mode, so an error if be raised without the *--interactive* flag.

If not running on *interactive mode*, arguments after [NAME] are passed to hledger. If the name is **all**, output all *no interactive* reports

```bash
python -m hledger_args -h
                                                                                
 Usage: python -m hledger_args [OPTIONS] [NAME] [EXTRA_HLEDGER_OPTIONS]...      
                                                                                
 ────────────────────────────────────────────────────────────────────────────── 
 NAME: Command name to run saved in the journal sub directives. Not available   
 in Interactive mode                                                            
                                                                                
 EXTRA_HLEDGER_OPTIONS: Extra options to send to hledger command. Not available 
 in Interactive mode. The name "all" is special and output all the no           
 interactive commands.                                                          
                                                                                
 ────────────────────────────────────────────────────────────────────────────── 
 In basic usage, this package is a replacement for hledger argument file using  
 custom directives inside the journal file, instead of referencing to an        
 argument file                                                                  
                                                                                
 Interactive Mode: Instead of giving the desired command thru a command-line    
 argument, choose it by selecting from a menu using the flag --interactive      
                                                                                
 Placeholder Command Substitution: In Interactive Mode, a command can use       
 placeholders by putting them between curly braces and additional prompts wil   
 ask for the value and do the proper substitution                               
                                                                                
 Special Placeholders: {account}, {payee}, {tag}, {tag_name}, {months}, {type}, 
 {cur} are special placeholders that offers autocomplete with fuzzy search      
 using data from the journal. See the README for explanation on each of them    
                                                                                
 Sub directive format:                                                          
                                                                                
                                                                                
  #+args [command name]:[hledger options]                                       
  #+args [other command_name]:[other hledger options]                           
                                                                                
                                                                                
 Example:                                                                       
                                                                                
                                                                                
  #+args buy_aapl:bal desc:"Buy AAPL"                                           
  #+args aapl_cur:bal desc:"Buy AAPL" cur:{commodity}                           
                                                                                
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│                                                                              │
│  *   --file                  -f   Inform the journal file path               │
│                                   (TEXT)                                     │
│                                   [required]                                 │
│                                                                              │
│      --interactive           -i   Run in interactive mode by answering the   │
│                                   prompts. [NAME] and                        │
│                                   [EXTRA_HLEDGER_OPTIONS] are not used in    │
│                                   this mode.                                 │
│                                                                              │
│      --pdf-dir               -d   Save the report to a folder named          │
│                                   according to the current date under the    │
│                                   specified directory                        │
│                                   (DIRECTORY)                                │
│                                                                              │
│      --pdf-file              -o   output the report to the specified file    │
│                                   in pdf                                     │
│                                   (FILE)                                     │
│                                                                              │
│      NAME                         (TEXT)                                     │
│                                                                              │
│      EXTRA_HLEDGER_OPTIONS        (TEXT)                                     │
│                                                                              │
│      --help                  -h   Show this message and exit.                │
│                                                                              │
╰──────────────────────────────────────────────────────────────────────────────╯

```																			 
