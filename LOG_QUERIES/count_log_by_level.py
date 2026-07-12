# count_log_by_level.py
# Groups and counts log entries by their log level (ERROR, WARNING, INFO, etc.)

from parser import load_entries


def count_by_level(log_content: str) -> dict:
    """
    Count entries for each log level.
    Returns dict with level name as key and count as value.
    """
    entries = load_entries(log_content)
    result = {}
    
    # Define order for display
    for level in ['ERROR', 'WARNING', 'INFO', 'DEBUG', 'CRITICAL']:
        result[level] = sum(1 for e in entries if e.level == level)
    
    return result