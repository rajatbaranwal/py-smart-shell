# commands.py
"""
Basic filesystem command implementations for the Python terminal project.
Each function returns a string message to be printed by the CLI frontend.
"""

import os
import shutil
from typing import Optional

def pwd() -> str:
    """Return current working directory."""
    try:
        return os.getcwd()
    except Exception as e:
        return f"Error getting current directory: {e}"

def ls(path: Optional[str] = ".") -> str:
    """List contents of directory. Default is current directory."""
    try:
        items = os.listdir(path)
        if not items:
            return "(empty)"
        # Mark directories with a trailing slash for readability
        formatted = []
        for name in sorted(items):
            full = os.path.join(path, name)
            if os.path.isdir(full):
                formatted.append(f"{name}/")
            else:
                formatted.append(name)
        return "\n".join(formatted)
    except FileNotFoundError:
        return f"ls: cannot access '{path}': No such file or directory"
    except NotADirectoryError:
        return f"ls: cannot access '{path}': Not a directory"
    except PermissionError:
        return f"ls: permission denied: '{path}'"
    except Exception as e:
        return f"ls: error: {e}"

def cd(path: str) -> str:
    """Change current working directory."""
    if not path:
        return "cd: path required"
    try:
        os.chdir(path)
        return f"Changed directory to {os.getcwd()}"
    except FileNotFoundError:
        return f"cd: no such file or directory: {path}"
    except NotADirectoryError:
        return f"cd: not a directory: {path}"
    except PermissionError:
        return f"cd: permission denied: {path}"
    except Exception as e:
        return f"cd: error: {e}"

def mkdir(path: str) -> str:
    """Create a directory. If intermediate dirs needed, create them."""
    if not path:
        return "mkdir: directory name required"
    try:
        # Use exist_ok=False so we can return an informative message if already exists
        os.makedirs(path, exist_ok=False)
        return f"Directory '{path}' created."
    except FileExistsError:
        return f"mkdir: cannot create directory '{path}': File exists"
    except PermissionError:
        return f"mkdir: permission denied: {path}"
    except Exception as e:
        return f"mkdir: error: {e}"

def rm(path: str, recursive: bool = False) -> str:
    """
    Remove file or directory.
    - If path is a file -> remove file.
    - If path is a directory:
        - if recursive True -> remove directory tree.
        - else -> return an error message.
    """
    if not path:
        return "rm: path required"
    try:
        if os.path.isfile(path) or os.path.islink(path):
            os.remove(path)
            return f"Removed file '{path}'"
        elif os.path.isdir(path):
            if recursive:
                shutil.rmtree(path)
                return f"Removed directory '{path}' (recursive)"
            else:
                return f"rm: '{path}' is a directory (use recursive=True to remove directories)"
        else:
            return f"rm: cannot remove '{path}': No such file or directory"
    except FileNotFoundError:
        return f"rm: cannot remove '{path}': No such file or directory"
    except PermissionError:
        return f"rm: permission denied: {path}"
    except Exception as e:
        return f"rm: error: {e}"

def cat(path: str) -> str:
    """Return file contents (small files only)."""
    if not path:
        return "cat: path required"
    try:
        if not os.path.exists(path):
            return f"cat: {path}: No such file or directory"
        if os.path.isdir(path):
            return f"cat: {path}: Is a directory"
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except PermissionError:
        return f"cat: permission denied: {path}"
    except Exception as e:
        return f"cat: error: {e}"

def echo(*args: str) -> str:
    """Echo arguments back as a string (like shell echo)."""
    return " ".join(args)
