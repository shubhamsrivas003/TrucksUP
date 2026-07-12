# 🚚 TrucksUp Log Analyzer
## Requirements

- **Python 3.10+** 
- **No external libraries**

## 🚀 Quick Start

**Run with the default log file** (looks for `trucksup.log`):
```bash
python app.py
```

**Want to analyze a different log file?** 
```bash
python app.py path/to/your/logfile.log
```

## 📋 Log File Format

The tool expects logs in the following format:

```
YYYY-MM-DD HH:MM:SS LEVEL Message with key=value pairs
```

**Example entries:**
```
2026-04-10 08:00:01 INFO  OrderId=ORD101 successfully assigned to driverId=DR201 on route Delhi-Mumbai
2026-04-10 08:01:15 ERROR Booking failed for orderId=ORD102 due to driver unavailable
2026-04-10 08:02:20 ERROR Pricing service timeout for route Delhi-Mumbai
2026-04-10 08:03:10 WARNING High demand detected for route Bangalore-Hyderabad
2026-04-10 08:05:30 WARNING No return load found for truckId=TR301 on route Mumbai-Delhi
```

**Supported log levels:** `INFO`, `DEBUG`, `WARNING`, `ERROR`, `CRITICAL`

---

## Output

Running `app.py` prints a full report to the console:

```
==================================================
  TOTAL LOG ENTRIES
==================================================
  Total : 100

==================================================
  LOG COUNT BY LEVEL
==================================================
  ERROR     : 45
  WARNING   : 27
  INFO      : 28
  DEBUG     : 0
  CRITICAL  : 0

==================================================
  TOP 3 ERROR MESSAGES
==================================================
  #1 [25x] Booking failed for orderId=<ID> due to driver unavailable
  #2 [10x] Pricing service timeout for route Delhi-Mumbai
  #3 [4x]  Booking failed for orderId=<ID> due to payment gateway failure

==================================================
  BOOKING FAILURES
==================================================
  Total Failures  : 29
  Affected Orders : ORD102, ORD103, ORD105 ...

==================================================
  EMPTY RUNS — NO RETURN LOAD
==================================================
  Total Cases     : 17
  Affected Trucks : TR301, TR302, TR303 ...
  Routes          : Mumbai-Delhi, Hyderabad-Chennai ...

==================================================
  ISSUES BY CATEGORY
==================================================

  [Booking Issues]        →  29 issues
  [Pricing Issues]        →  10 issues
  [Supply-Demand Issues]  →  17 issues

==================================================
  ANALYSIS COMPLETE
==================================================
```

---

## Approach & Logic

### 1. Parsing (`parser.py`)
Each log line is split on the first 3 spaces using `split(' ', 3)` which gives exactly:
`[date, time, level, message]` — no regex needed since the format is guaranteed.
These are stored as `LogEntry` dataclass instances for clean, typed access.

### 2. Analysis Modules
Each file is responsible for exactly one task and accepts `log_content: str` as input:

| File | Logic |
|------|-------|
| `count_log.py` | Counts all parsed `LogEntry` objects |
| `count_log_by_level.py` | Groups entries by `entry.level` |
| `top_logs.py` | Uses `collections.Counter` on `entry.message` for ERROR entries |
| `booking_failures.py` | Filters ERRORs with booking keywords, extracts `orderId=` values |
| `no_return_loads.py` | Filters WARNINGs with `no return load found`, extracts `truckId=` and route |
| `categorize.py` | Maps each entry to a category using keyword matching on `entry.message` |

### 3. Orchestration (`main.py`)
Calls all 6 analysis functions and returns a single structured `dict`.

### 4. Entry Point (`app.py`)
Reads the log file (from CLI arg or default), calls `run_analysis()`, and prints a formatted report.

---

## Assumptions

- Log format is strictly `YYYY-MM-DD HH:MM:SS LEVEL message` — no multi-line logs
- `orderId=`, `truckId=`, `driverId=` values are single words (no spaces)
- Route names follow the pattern `on route <City1>-<City2>`
- Booking failures are identified by keywords: `driver unavailable`, `payment gateway`
- Supply-Demand issues include both `high demand` and `no return load found` signals
- The log file is UTF-8 encoded plain text
