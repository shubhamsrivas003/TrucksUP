# booking_failures.py
# Identifies booking-related failures from error logs

from parser import load_entries


def booking_failures(log_content: str) -> dict:
    """
    Find all booking failure errors.
    Looks for keywords: 'driver unavailable', 'payment gateway'
    Returns total count and list of affected order IDs.
    """
    entries = load_entries(log_content)
    
    # Filter entries that are errors related to booking failures
    failures = [
        e for e in entries
        if e.level == 'ERROR' and any(
            kw in e.message.lower() for kw in ['driver unavailable', 'payment gateway']
        )
    ]

    # Extract order IDs from error messages
    # Format expected: "...orderId=XYZ ..."
    order_ids = list(dict.fromkeys(
        e.message.split('orderId=')[1].split(' ')[0] for e in failures
    ))

    return {
        "total": len(failures),
        "order_ids": order_ids
    }