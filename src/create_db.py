import sqlite3

def create_db(path="vacations.db"):
    conn = sqlite3.connect(path)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS Department (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS Employee (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    department INTEGER,
                    position TEXT,
                    total_days INTEGER DEFAULT 28,
                    used_days INTEGER DEFAULT 0,
                    FOREIGN KEY(department) REFERENCES Department(id)
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS VacationRequest (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    emp_id INTEGER,
                    start_date TEXT,
                    end_date TEXT,
                    days INTEGER,
                    status TEXT DEFAULT "PENDING",
                    FOREIGN KEY(emp_id) REFERENCES Employee(id)
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS HRReport (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    report_date TEXT,
                    total_employees INTEGER,
                    total_days_used INTEGER
                )''')

    c.execute("CREATE INDEX IF NOT EXISTS idx_emp_department ON Employee(department)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_vr_emp ON VacationRequest(emp_id)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_vr_status ON VacationRequest(status)")

    conn.commit()
    conn.close()
    print("База данных создана:", path)

if __name__ == "__main__":
    create_db()
