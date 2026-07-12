# app.py
# Main entry point for log analysis application
# Takes a log file as input and displays formatted analysis results

import sys
from main import run_analysis


def print_section(title: str):
    """Print a formatted section header with title."""
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)


def print_results(result: dict):
    """
    Display analysis results in a readable format.
    Each section shows different insights from the log data.
    """

    # ── 1. Total Count ──────────────────────────────
    print_section("TOTAL LOG ENTRIES")
    total = result['total_entries']
    print(f"  Total : {total}")

    # ── 2. Count by Level ───────────────────────────
    print_section("LOG COUNT BY LEVEL")
    # Show count of each log level (ERROR, WARNING, INFO, etc.)
    for level, count in result['by_level'].items():
        print(f"  {level:<10}: {count}")

    # ── 3. Top 3 Errors ─────────────────────────────
    print_section("TOP 3 ERROR MESSAGES")
    # Display the most frequent error messages
    for rank, data in result['top_errors'].items():
        print(f"  #{rank} [{data['count']}x] {data['message']}")

    # ── 4. Booking Failures ─────────────────────────
    print_section("BOOKING FAILURES")
    bf = result['booking_failures']
    print(f"  Total Failures  : {bf['total']}")
    print(f"  Affected Orders : {', '.join(bf['order_ids'])}")

    # ── 5. Empty Runs ───────────────────────────────
    print_section("EMPTY RUNS — NO RETURN LOAD")
    nr = result['no_return_loads']
    print(f"  Total Cases     : {nr['total']}")
    print(f"  Affected Trucks : {', '.join(nr['truck_ids'])}")
    print(f"  Routes          : {', '.join(nr['routes'])}")

    # ── 6. Categories ───────────────────────────────
    print_section("ISSUES BY CATEGORY")
    # Group issues by category type
    for category, data in result['categories'].items():
        print(f"\n  [{category}]  →  {data['total']} issues")
        for msg in data['messages']:
            print(f"    • {msg}")

    # End marker
    print("\n" + "=" * 50)
    print("  ANALYSIS COMPLETE")
    print("=" * 50)


if __name__ == "__main__":
    # Get log file from command line argument, default to trucksup.log
    log_file = sys.argv[1] if len(sys.argv) > 1 else "trucksup.log"

    try:
        # Read the entire log file into memory
        with open(log_file, "r") as f:
            content = f.read()
        print(f"  Using log file: {log_file}")
    except FileNotFoundError:
        # Handle case when log file doesn't exist
        print(f"  ERROR: File '{log_file}' not found.")
        sys.exit(1)

    # Run analysis and display results
    result = run_analysis(content)
    print_results(result)