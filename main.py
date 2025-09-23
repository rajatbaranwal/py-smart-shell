"""
Main CLI for Python Terminal Project with Natural Language Processing.
Handles user input, runs commands, and prints results.
"""

import os
import sys
import time
import readline
import glob
from datetime import datetime
import psutil
from colorama import init, Fore, Style

from commands import pwd, ls, cd, mkdir, rm, cat, echo
from monitor import cpu_usage, memory_usage, processes

# Import NLP parser
try:
    from nlp_parser import NLPCommandParser
    NLP_AVAILABLE = True
except ImportError:
    print("Warning: NLP parser not available. Using command-only mode.")
    NLP_AVAILABLE = False

init(autoreset=True)

def completer(text, state):
    options = glob.glob(text + '*')
    if state < len(options):
        return options[state]
    return None

readline.parse_and_bind("tab: complete")
readline.set_completer(completer)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_prompt():
    return f"{Fore.CYAN}{os.getcwd()} > {Style.RESET_ALL}"

def is_traditional_command(user_input: str) -> bool:
    first_word = user_input.split()[0] if user_input.split() else ""
    traditional_commands = {
        'pwd', 'ls', 'cd', 'mkdir', 'rm', 'cat', 'echo',
        'cpu', 'mem', 'ps', 'whoami', 'date', 'uptime',
        'clear', 'history', 'help', 'exit', 'quit'
    }
    return first_word.lower() in traditional_commands

def process_command(cmd: str, args: list):
    if cmd in ("exit", "quit"):
        print(Fore.GREEN + "Goodbye!")
        return "exit"

    elif cmd == "help":
        print(Fore.YELLOW + """Available commands:
    pwd, ls, cd, mkdir, rm, cat, echo
    cpu, mem, ps
    whoami, date, uptime
    clear, history, help, exit

You can also use natural language:
    "create a folder called test and open it"
    "show me the files"
    "where am i"
    "delete myproject"
    "what's the cpu usage"
""")

    elif cmd == "pwd":
        print(Fore.GREEN + pwd())
    elif cmd == "ls":
        print(ls(args[0]) if args else ls())
    elif cmd == "cd":
        print(cd(args[0]) if args else Fore.RED + "cd: path required")
    elif cmd == "mkdir":
        print(mkdir(args[0]) if args else Fore.RED + "mkdir: path required")
    elif cmd == "rm":
        if args and args[0] == "-r" and len(args) > 1:
            confirm = input(Fore.YELLOW + f"Delete '{args[1]}'? (y/n): ").lower()
            if confirm == "y":
                print(rm(args[1], recursive=True))
        elif args:
            print(rm(args[0]))
        else:
            print(Fore.RED + "rm: path required")
    elif cmd == "cat":
        print(cat(args[0]) if args else Fore.RED + "cat: file required")
    elif cmd == "echo":
        print(Fore.GREEN + echo(*args))
    elif cmd == "cpu":
        print(cpu_usage())
    elif cmd == "mem":
        print(memory_usage())
    elif cmd == "ps":
        print(processes())
    elif cmd == "whoami":
        try:
            print(Fore.GREEN + os.getlogin())
        except OSError:
            print(Fore.GREEN + os.environ.get("USER", "unknown"))
    elif cmd == "date":
        print(Fore.GREEN + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    elif cmd == "uptime":
        boot_time = psutil.boot_time()
        uptime_seconds = int(time.time() - boot_time)
        h, rem = divmod(uptime_seconds, 3600)
        m, s = divmod(rem, 60)
        print(Fore.GREEN + f"System Uptime: {h}h {m}m {s}s")
    elif cmd == "clear":
        clear_screen()
    elif cmd == "history":
        for i in range(1, readline.get_current_history_length() + 1):
            print(f"{i}: {readline.get_history_item(i)}")
    else:
        print(Fore.RED + f"{cmd}: command not found.")

def run_terminal():
    print(Fore.GREEN + "=== Python Terminal with NLP ===")
    if NLP_AVAILABLE:
        print("You can type commands OR natural language.")
    print("Type 'help' to see available commands. Type 'exit' to quit.\n")

    nlp_parser = NLPCommandParser() if NLP_AVAILABLE else None

    while True:
        try:
            user_input = input(get_prompt()).strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting terminal.")
            break

        if not user_input:
            continue

        if is_traditional_command(user_input):
            parts = user_input.split()
            cmd, args = parts[0], parts[1:]
            result = process_command(cmd, args)
            if result == "exit":
                break
        elif NLP_AVAILABLE:
            cmd, args = nlp_parser.parse(user_input)
            if cmd is None:
                suggestions = nlp_parser.get_suggestions(user_input)
                print(Fore.YELLOW + f"Sorry, I didn't understand '{user_input}'.")
                if suggestions:
                    print(Fore.CYAN + f"Try: {', '.join(suggestions[:3])}")
                continue
            if cmd == "multi":
                for (c, a) in args:
                    print(Fore.MAGENTA + f"→ Executing: {c} {' '.join(a)}")
                    process_command(c, a)
            else:
                print(Fore.MAGENTA + f"→ Executing: {cmd} {' '.join(args)}")
                process_command(cmd, args)
        else:
            print(Fore.RED + "Command not found.")

if __name__ == "__main__":
    run_terminal()
