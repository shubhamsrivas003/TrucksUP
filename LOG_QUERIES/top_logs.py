# top_logs.py
# Identifies the top 3 most frequently occurring error messages

from parser import load_entries
from collections import Counter


def top_errors(log_content: str) -> dict:
    """
    Find the 3 most common error messages.
    Returns dict with rank (1-3) as key and message/count as value.
    """
    entries = load_entries(log_content)
    
    # Extract only ERROR level messages
    error_messages = [e.message for e in entries if e.level == 'ERROR']
    
    # Count frequency of each unique error message
    top3 = Counter(error_messages).most_common(3)

    # Build result dictionary
    top_error_log = {}
    for rank, (msg, count) in enumerate(top3, 1):
        top_error_log[rank] = {"message": msg, "count": count}

    return top_error_log