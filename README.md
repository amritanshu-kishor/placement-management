# Placement Management

A simple placement management application. This repository contains a Python-based app (`app.py`), database schema (`schema.sql`), and supporting files.

## Prerequisites

- Python 3.8+ installed
- (Optional) virtual environment tool: `venv` or `virtualenv`

## Setup

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Initialize the database using `schema.sql` (adjust for your DB engine):

```powershell
# Example for SQLite (create a DB file and apply schema)
# sqlite3 placement.db < schema.sql
```

4. Run the application:

```powershell
python app.py
```

## Files

- `app.py`: Main application entrypoint.
- `schema.sql`: Database schema.
- `requirements.txt`: Python dependencies.
- `LICENSE`: Project license.

## License

See the `LICENSE` file for license details.
