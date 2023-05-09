# hledger-args

## Description

In basic usage, this package is a replacement for [hledger command file](https://hledger.org/1.29/hledger.html#command-arguments) using custom directives inside the journal file, instead of referencing to a command args file.

In interactive mode, the user can create menus using placeholders. Each placeholders will become a prompt and be replaced by the value entered. So the user will be able to create a multi prompt report composed by fixed options already defined and leave some to the user each time this package is executed.

### Interactive Mode

Instead of giving the the desired command thru a command-line argument, choose it by selecting from a menu using the flag *--interactive*

### Special placeholders

*{account}* and *{tag}* are reserved placeholders that offers autocomplete with fuzzy search using data from the journal

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

If not running on *interactive mode*, arguments after 

```bash
Usage: hledger-args [OPTIONS] [NAME] [EXTRA_HLEDGER_OPTIONS]...                

NAME: Command name to run saved in the journal sub directives. Not available   
in Interactive mode                                                            
                                                                                
EXTRA_HLEDGER_OPTIONS: Extra options to send to hledger command. Not available 
in Interactive mode.     
                                                                             
 *   --file                  -f   Inform the journal file path               
                                  (TEXT)                                     ```
                                  [required]                                 
                                                                             
     --interactive           -i   Run in interactive mode by answering the   
                                  prompts. [NAME] and                        
                                  [EXTRA_HLEDGER_OPTIONS] are not used in    
                                  this mode.                                 
                                                                             
     NAME                         (TEXT)                                     
                                                                             
     EXTRA_HLEDGER_OPTIONS        (TEXT)                                     
                                                                             
     --help                  -h   Show this message and exit.                
                                                                             
```																			 
