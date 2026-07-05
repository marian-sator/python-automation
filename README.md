# Python Automation Scripts
**Author:** Marian Sator

A collection of Python automation scripts developed as part of my transition into Enterprise IT.

## About
These scripts were written after one week of learning Python, transferring 14 years of software development experience from Lua into Python syntax.

## Scripts

### get_purchase_summary.py
Filters and ranks customers by purchase amount from transaction data.

### password_generator.py
Generates secure passwords with customizable character sets, length, and complexity rules.

### api_monitor.py
Monitors URL availability and response times. Runs continuously and alerts on failures.

### data_processor.py
Processes large transaction datasets (100,000+ entries) with performance tracking.

Key features:
- Duplicate detection using dictionary lookup O(1) instead of iteration O(n²)
- Single-pass processing - filters and aggregates in one loop
- Optional sorting for flexibility
- Built-in performance measurement in milliseconds

### csv_processor.py
Validates and processes CSV data with comprehensive error reporting and performance tracking.

Key features:
- Input validation and normalization (strip, lowercase)
- Duplicate detection using dictionary lookup O(1)
- Multi-rule validation - email format, age restriction, required fields
- Built-in performance measurement in milliseconds

### midea_portasplit_tracker.py
Monitors three Austrian retailers (BAUHAUS, MediaMarkt, OBI) for availability of the Midea PortaSplit air conditioning unit and sends a Discord notification the moment it becomes purchasable.

Key features:
- Headless browser automation with Selenium to handle JavaScript-rendered content
- Retailer-specific parsing strategies: dataLayer extraction (BAUHAUS), unicode-escaped hydration JSON (MediaMarkt), and ld+json structured data (OBI)
- Continuous polling at a configurable interval
- Discord webhook notification on availability

### exchange-rate-tracker/
Tracks the EUR/USD exchange rate daily via the Frankfurter API and stores historical data in a local SQLite database.

- `run.py` – Fetches the current rate once per day during a configured hour and stores it in the database
- `analyzer.py` – Queries the database and outputs lowest, highest and average exchange rates with timestamps

Key features:
- SQLite database integration for persistent storage
- Time-based execution control
- REST API integration with error handling and response validation
- Separation of data collection and analysis into independent scripts

## Skills demonstrated
- REST API integration
- SQLite database integration
- Data processing and filtering
- Error handling
- Performance-oriented thinking
- Data validation and cleaning
- CSV processing
