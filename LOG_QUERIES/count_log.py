# count_log.py
# Counts total number of log entries in the log content

from parser import load_entries


def count_logs(log_content: str):
    """Return total count of all log entries."""
    entries = load_entries(log_content)
    total = len(entries)
    return total