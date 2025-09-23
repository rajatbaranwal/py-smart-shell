# monitor.py
"""
System monitoring utilities for the Python terminal project.
Provides functions to get CPU usage, memory usage, and running processes.
"""

import psutil

def cpu_usage() -> str:
    """Return current CPU usage as percentage."""
    try:
        return f"CPU Usage: {psutil.cpu_percent(interval=0.5)}%"
    except Exception as e:
        return f"cpu: error: {e}"

def memory_usage() -> str:
    """Return memory usage summary."""
    try:
        mem = psutil.virtual_memory()
        used_mb = mem.used // (1024 ** 2)
        total_mb = mem.total // (1024 ** 2)
        return f"Memory Usage: {mem.percent}% ({used_mb} MB / {total_mb} MB)"
    except Exception as e:
        return f"mem: error: {e}"

def processes(limit: int = 10) -> str:
    """
    List top running processes (up to `limit`).
    Shows PID, name, and CPU usage.
    """
    try:
        proc_list = []
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            proc_list.append(p.info)
        # Sort by CPU usage descending
        proc_list.sort(key=lambda x: x['cpu_percent'], reverse=True)
        top = proc_list[:limit]
        lines = [f"{p['pid']:>5}  {p['cpu_percent']:>5}%  {p['name']}" for p in top]
        return "PID    CPU%  NAME\n" + "\n".join(lines)
    except Exception as e:
        return f"ps: error: {e}"
