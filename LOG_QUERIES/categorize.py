# categorize.py
# Groups log issues into categories based on keywords and log levels

from parser import load_entries


# Define categories and their matching rules
# Each category has a lambda that returns True if entry matches
CATEGORIES = {
    "Booking Issues": lambda e: e.level in ('ERROR', 'WARNING') and any(
        kw in e.message.lower() for kw in ['booking failed', 'driver unavailable', 'payment gateway']
    ),
    "Pricing Issues": lambda e: e.level in ('ERROR', 'WARNING') and 'pricing service' in e.message.lower(),
    "Supply-Demand Issues": lambda e: e.level in ('ERROR', 'WARNING') and any(
        kw in e.message.lower() for kw in ['high demand', 'no return load found']
    ),
}


def categorize_issues(log_content: str) -> dict:
    """
    Categorize all error/warning entries by matching against category rules.
    Returns dict with category name as key and {total, messages} as value.
    """
    entries = load_entries(log_content)
    
    # Initialize empty list for each category
    result = {category: [] for category in CATEGORIES}

    # Check each entry against all category rules
    for entry in entries:
        for category, matcher in CATEGORIES.items():
            if matcher(entry):
                result[category].append(entry.message)

    # Convert lists to summary format
    return {
        category: {"total": len(msgs), "messages": msgs}
        for category, msgs in result.items()
    }