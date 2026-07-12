# no_return_loads.py
# Identifies trucks that completed a delivery but couldn't find a return load

from parser import load_entries


def no_return_loads(log_content: str) -> dict:
    """
    Find warnings about trucks with no return load available.
    Returns count, truck IDs, and affected routes.
    """
    entries = load_entries(log_content)
    
    # Filter WARNING level entries containing 'no return load found'
    cases = [
        e for e in entries 
        if e.level == 'WARNING' and 'no return load found' in e.message.lower()
    ]

    # Extract truck IDs from messages
    # Format: "...truckId=ABC ..."
    truck_ids = [e.message.split('truckId=')[1].split(' ')[0] for e in cases]
    
    # Extract route information
    # Format: "...on route XYZ..."
    routes = [e.message.split('on route ')[1] for e in cases]

    return {
        "total": len(cases),
        "truck_ids": truck_ids,
        "routes": routes
    }