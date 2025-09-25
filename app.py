# app.py
from flask import Flask, render_template, request, jsonify
import os
import subprocess
from commands import pwd, ls, cd, mkdir, rm, cat, echo
from monitor import cpu_usage, memory_usage, processes
import getpass
import socket

# Import NLP Parser
from nlp_parser import NLPCommandParser

app = Flask(__name__)

# Initialize NLP parser
nlp_parser = NLPCommandParser()

def generate_prompt():
    """Generate a realistic shell-like prompt."""
    user = getpass.getuser()
    hostname = socket.gethostname().split(".")[0]
    cwd = os.getcwd()
    return f"{user}@{hostname}:{cwd}$"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run():
    data = request.get_json()
    command = data.get("command", "").strip()

    # Special case: clear command
    if command == "clear":
        return jsonify({"output": "__CLEAR__", "prompt": generate_prompt()})

    # Known traditional commands
    traditional_commands = [
        "pwd", "ls", "cd", "mkdir", "rm", "cat", "echo",
        "cpu", "mem", "ps", "exit", "quit"
    ]

    # Default command + args
    c, args = None, []

    # Split by semicolon (basic chaining support)
    commands = [cmd.strip() for cmd in command.split(";") if cmd.strip()]
    outputs = []

    for cmd in commands:
        parts = cmd.split()
        if not parts:
            continue

        c = parts[0]
        args = parts[1:]

        # If not a known command, try NLP
        if c not in traditional_commands:
            parsed_cmd, parsed_args = nlp_parser.parse(cmd)
            if parsed_cmd:
                c = parsed_cmd
                args = parsed_args
            else:
                outputs.append(f"{cmd}: command not found")
                continue

        # --- Command Handling ---
        if c == "pwd":
            outputs.append(pwd())
        elif c == "ls":
            outputs.append(ls(args[0]) if args else ls())
        elif c == "cd":
            outputs.append(cd(args[0]) if args else "cd: path required")
        elif c == "mkdir":
            outputs.append(mkdir(args[0]) if args else "mkdir: path required")
        elif c == "rm":
            if args and args[0] == "-r" and len(args) > 1:
                outputs.append(rm(args[1], recursive=True))
            elif args:
                outputs.append(rm(args[0]))
            else:
                outputs.append("rm: path required")
        elif c == "cat":
            outputs.append(cat(args[0]) if args else "cat: file required")
        elif c == "echo":
            outputs.append(echo(*args))
        elif c == "cpu":
            outputs.append(cpu_usage())
        elif c == "mem":
            outputs.append(memory_usage())
        elif c == "ps":
            outputs.append(processes())
        elif c in ("exit", "quit"):
            outputs.append("Goodbye!")
        else:
            outputs.append(f"{c}: command not found")

    return jsonify({"output": "\n".join(outputs), "prompt": generate_prompt()})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # Render gives PORT env var
    app.run(host="0.0.0.0", port=port, debug=False)
