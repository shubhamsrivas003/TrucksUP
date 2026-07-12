# parser.py
"""
Core log parsing module.
Handles reading and converting log lines into structured objects.
"""

# Import dataclass decorator to create simple data containers
from dataclasses import dataclass

# Define valid log levels recognized by the system
# Any level not in this set will be treated as unknown
VALID_LEVELS = {'INFO', 'DEBUG', 'WARNING', 'ERROR', 'CRITICAL'}


@dataclass
class LogEntry:
    """
    Represents a single parsed log entry.
    
    Attributes:
        date: Date portion extracted from log line
        time: Time portion extracted from log line
        level: Log level (INFO, ERROR, WARNING, etc.)
        message: The actual log message content
    """
    date: str      # Date portion from log line
    time: str      # Time portion from log line
    level: str     # Log level (INFO, ERROR, etc.)
    message: str   # The actual log message


def parse_line(line: str) -> LogEntry:
    """
    Convert a single log line into a LogEntry object.
    
    Args:
        line: A single line from the log file
              Expected format: DATE TIME LEVEL message...
        
    Returns:
        LogEntry object with parsed components
    """
    # Remove leading/trailing whitespace from the line
    stripped_line = line.strip()
    
    # Split the line by spaces into individual components
    # First 3 parts are: date, time, level
    # Everything after becomes the message
    parts = stripped_line.split(' ')
    
    # Extract each component from the split result
    date = parts[0]    # First element is the date
    time = parts[1]    # Second element is the time
    level = parts[2]   # Third element is the log level
    
    # Join all remaining parts back into a single message string
    # This handles messages that may contain spaces
    message_parts = parts[3:]
    message = ' '.join(message_parts)
    
    # Normalize the log level to uppercase for consistency
    # This ensures 'info' and 'INFO' are treated the same
    normalized_level = level.upper()
    
    # Create and return the LogEntry instance
    return LogEntry(
        date=date,
        time=time,
        level=normalized_level,
        message=message
    )


def load_entries(log_content: str) -> list[LogEntry]:
    """
    Parse entire log content into a list of LogEntry objects.
    
    Args:
        log_content: Raw log data as a string containing multiple lines
        
    Returns:
        List of LogEntry objects, one for each valid log line
    """
    # Split the content into individual lines
    all_lines = log_content.splitlines()
    
    # Filter out empty lines and lines with only whitespace
    # Then parse each remaining line into a LogEntry
    parsed_entries = []
    
    for line in all_lines:
        # Check if line has content
        if line.strip():
            # Parse the line and add to our list
            entry = parse_line(line)
            parsed_entries.append(entry)
    
    return parsed_entries