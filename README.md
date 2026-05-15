# Placement Management

A simple placement management application. This repository contains a Python-based app (`app.py`), database schema (`schema.sql`), and supporting files.

## Prerequisites

- Python 3.8+ installed
- (Optional) virtual environment tool: `venv` or `virtualenv`
- MySQL server installed (for recommended setup)

## Setup

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Database (MySQL) — using your own username/password

This project can use MySQL. It's best practice to keep DB credentials outside source files and use environment variables. Create a MySQL database, a dedicated user, and grant privileges. Replace `your_root_password`, `placement_db`, `pm_user`, and `pm_password` with your own values.

Create the database and user (run in a shell where `mysql` client is available):

```bash
mysql -u root -p -e "CREATE DATABASE placement_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
mysql -u root -p -e "CREATE USER 'pm_user'@'localhost' IDENTIFIED BY 'pm_password';"
mysql -u root -p -e "GRANT ALL PRIVILEGES ON placement_db.* TO 'pm_user'@'localhost'; FLUSH PRIVILEGES;"
```

Apply the schema using the new user:

```bash
mysql -u pm_user -p placement_db < schema.sql
```

4. Configure credentials via environment variables

Create a `.env` file (do not commit it) or export environment variables. Use your own DB username and password.

Example environment variables (also provided in `.env.example`):

```
DB_HOST=localhost
DB_PORT=3306
DB_NAME=placement_db
DB_USER=pm_user
DB_PASSWORD=pm_password
```

If the application reads env vars differently, adapt these names accordingly. Never commit real passwords to the repository.

5. Run the application:

```powershell
# In PowerShell
python app.py
```

## Files

- `app.py`: Main application entrypoint.
- `schema.sql`: Database schema.
- `requirements.txt`: Python dependencies.
- `LICENSE`: Project license.
- `.env.example`: Example environment variables (no secrets).

## Security note

- Use strong passwords and limit user privileges to only what the app needs.
- For production, consider using a secrets manager or platform-provided environment variables instead of a plain `.env` file.

## License

See the `LICENSE` file for license details.
