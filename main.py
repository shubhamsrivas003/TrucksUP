# main.py
"""
Main entry point for log analysis application.
Coordinates all log analysis modules and returns combined results.
"""

# Import individual analysis functions from LOG_QUERIES package
# Each module handles a specific type of log analysis
from LOG_QUERIES.count_log import count_logs
from LOG_QUERIES.count_log_by_level import count_by_level
from LOG_QUERIES.top_logs import top_errors
from LOG_QUERIES.booking_failures import booking_failures
from LOG_QUERIES.no_return_loads import no_return_loads
from LOG_QUERIES.categorize import categorize_issues


def run_analysis(log_content: str) -> dict:
    """
    Run all analysis functions on the log content.
    
    Args:
        log_content: Raw log data as a string
        
    Returns:
        Dictionary containing all analysis results
    """
    # Execute each analysis module and collect results
    # Each function processes the log content differently
    
    # Count total number of log entries in the content
    total_entries = count_logs(log_content)
    
    # Group and count logs by their severity level (INFO, ERROR, WARNING, etc.)
    logs_by_level = count_by_level(log_content)
    
    # Find the top 3 most frequently occurring error messages
    top_error_messages = top_errors(log_content)
    
    # Identify all booking orders that failed
    failed_bookings = booking_failures(log_content)
    
    # Find trucks that arrived at destination but left without return load
    trucks_without_return = no_return_loads(log_content)
    
    # Categorize all issues into meaningful groups
    issue_categories = categorize_issues(log_content)
    
    # Combine all results into a single dictionary
    return {
        "total_entries": total_entries,
        "by_level": logs_by_level,
        "top_errors": top_error_messages,
        "booking_failures": failed_bookings,
        "no_return_loads": trucks_without_return,
        "categories": issue_categories,
    }

