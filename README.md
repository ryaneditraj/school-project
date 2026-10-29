# KADAL KANAKKU – Fish Catch, Auction & Sea-Safety Manager
CBSE Class XII Computer Science (083) Project 2026-27 – Ryan, XII A

## Files
- `kadal_kanakku.py` – main Python program (menu driven)
- `schema.sql` – creates database `kadal_kanakku`, 5 tables and sample data
- `outputs/` – real outputs captured while testing
- `Project_Report_Kadal_Kanakku.docx / .pdf` – project report
- `Viva_QA_Kadal_Kanakku.md` – viva questions and answers

## How to run on your PC (Windows)
1. Install **Python 3** from python.org (tick "Add Python to PATH").
2. Install **MySQL Community Server 8.x** (MySQL Installer from dev.mysql.com).
   During setup, set a root password and remember it.
3. Open Command Prompt and run:
   `pip install mysql-connector-python`
4. Load the database (one time only). Open "MySQL 8.0 Command Line Client", type your password, then:
   `SOURCE C:/path/to/cs_project/schema.sql;`
   (use forward slashes in the path). Running it again RESETS all data to the sample data.
5. Open `kadal_kanakku.py` in IDLE and change the line
   `PASSWORD = "root"` to your own MySQL root password.
6. Run it (F5 in IDLE, or `python kadal_kanakku.py`).

## Troubleshooting
- "Access denied" → wrong PASSWORD in the program.
- "Unknown database 'kadal_kanakku'" → step 4 not done.
- "Can't connect to MySQL server" → MySQL service not running (Services → MySQL80 → Start).
- "No module named mysql" → step 3 not done (try `py -m pip install mysql-connector-python`).
- The CSV export (Reports → 6) creates `species_report.csv` in the folder you run from; open it in Excel.
