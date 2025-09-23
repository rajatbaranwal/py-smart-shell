# nlp_parser.py
"""
NLP Parser for Natural Language Commands in Python Terminal.
Maps human-friendly text into CLI commands and arguments.
"""

import os

class NLPCommandParser:
    def __init__(self):
        # Synonym mapping for commands
        self.command_map = {
            "pwd": ["where am i", "show current directory", "current path"],
            "ls": ["list files", "show files", "what's here", "list directory", "list contents"],
            "cd": ["go to", "navigate to", "open folder", "enter directory", "change folder"],
            "mkdir": ["create folder", "make folder", "create directory", "make directory"],
            "rm": ["delete", "remove", "erase", "trash"],
            "cat": ["show file", "read file", "view file"],
            "echo": ["say", "print", "write text"],
            "cpu": ["show cpu usage", "cpu usage", "processor usage"],
            "mem": ["show memory usage", "memory usage", "ram usage"],
            "ps": ["show processes", "list processes", "running processes", "tasks"],
            "whoami": ["who am i", "current user", "show user"],
            "date": ["show date", "what's the time", "time now"],
            "clear": ["clear screen", "reset screen"],
            "help": ["help", "show help", "what can you do"],
            "exit": ["exit", "quit", "close terminal"]
        }

    def parse(self, user_input: str):
        text = user_input.lower().strip()

        # 1. Handle multi-step commands: create + cd
        if "create" in text and "and open" in text:
            # Example: "create a folder called test and open it"
            folder_name = self._extract_name(text)
            if folder_name:
                return "MULTI", [("mkdir", folder_name), ("cd", folder_name)]

        # 2. Match against known commands
        for cmd, phrases in self.command_map.items():
            for phrase in phrases:
                if phrase in text:
                    # Special cases: create, delete, etc.
                    if cmd == "mkdir":
                        folder_name = self._extract_name(text)
                        if folder_name:
                            return cmd, [folder_name]
                        return None, []
                    elif cmd == "cd":
                        folder_name = self._extract_name(text)
                        if folder_name:
                            return cmd, [folder_name]
                        return None, []
                    elif cmd == "rm":
                        target_name = self._extract_name(text)
                        if target_name:
                            # Auto-detect if it's a folder and use recursive
                            if os.path.isdir(target_name):
                                return cmd, ["-r", target_name]
                            return cmd, [target_name]
                        return None, []
                    elif cmd == "cat":
                        file_name = self._extract_name(text)
                        if file_name:
                            return cmd, [file_name]
                        return None, []
                    else:
                        return cmd, []

        # 3. If no match found, try to detect "create/remove folder XYZ" manually
        if text.startswith("create"):
            folder_name = self._extract_name(text)
            if folder_name:
                return "mkdir", [folder_name]

        if text.startswith("remove") or text.startswith("delete"):
            folder_name = self._extract_name(text)
            if folder_name:
                if os.path.isdir(folder_name):
                    return "rm", ["-r", folder_name]
                return "rm", [folder_name]

        return None, []

    def get_suggestions(self, user_input: str):
        """Return a list of closest matching command suggestions."""
        matches = []
        for cmd, phrases in self.command_map.items():
            for phrase in phrases:
                if any(word in phrase for word in user_input.split()):
                    matches.append(cmd)
        return list(set(matches))  # unique suggestions

    def _extract_name(self, text):
        """Extract a file/folder name after 'called', 'named', or last word."""
        keywords = ["called", "named", "folder", "directory", "file"]
        parts = text.split()
        for i, word in enumerate(parts):
            if word in keywords and i + 1 < len(parts):
                return parts[i + 1]
        # fallback: last word
        return parts[-1] if len(parts) > 1 else None
