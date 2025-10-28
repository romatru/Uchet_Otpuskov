import sqlite3
from datetime import date

class DAL:
    def __init__(self, db_path="vacations.db"):
        self.db_path = db_path

    def _conn(self):
        return sqlite3.connect(self.db_path)

    # Department
    def add_department(self, name):
        conn = self._conn()
        c = conn.cursor()
        c.execute("INSERT INTO Department (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()

    def list_departments(self):
        conn = self._conn()
        c = conn.cursor()
        c.execute("SELECT id, name FROM Department")
        rows = c.fetchall()
        conn.close()
        return rows

    # Employee CRUD
    def add_employee(self, name, department=None, position="", total_days=28):
        conn = self._conn()
        c = conn.cursor()
        c.execute("INSERT INTO Employee (name, department, position, total_days) VALUES (?, ?, ?, ?)",
                  (name, department, position, total_days))
        conn.commit()
        emp_id = c.lastrowid
        conn.close()
        return emp_id

    def get_employee(self, emp_id):
        conn = self._conn()
        c = conn.cursor()
        c.execute("SELECT id, name, department, position, total_days, used_days FROM Employee WHERE id=?", (emp_id,))
        row = c.fetchone()
        conn.close()
        return row

    def update_employee_used_days(self, emp_id, add_days):
        conn = self._conn()
        c = conn.cursor()
        c.execute("UPDATE Employee SET used_days = used_days + ? WHERE id=?", (add_days, emp_id))
        conn.commit()
        conn.close()

    def list_employees(self):
        conn = self._conn()
        c = conn.cursor()
        c.execute("SELECT id, name, department, position, total_days, used_days FROM Employee")
        rows = c.fetchall()
        conn.close()
        return rows

    # VacationRequest CRUD
    def create_request(self, emp_id, start_date, end_date, days):
        conn = self._conn()
        c = conn.cursor()
        c.execute("INSERT INTO VacationRequest (emp_id, start_date, end_date, days) VALUES (?, ?, ?, ?)",
                  (emp_id, start_date, end_date, days))
        conn.commit()
        req_id = c.lastrowid
        conn.close()
        return req_id

    def get_request(self, req_id):
        conn = self._conn()
        c = conn.cursor()
        c.execute("SELECT id, emp_id, start_date, end_date, days, status FROM VacationRequest WHERE id=?", (req_id,))
        row = c.fetchone()
        conn.close()
        return row

    def list_requests(self, status=None):
        conn = self._conn()
        c = conn.cursor()
        if status:
            c.execute("SELECT id, emp_id, start_date, end_date, days, status FROM VacationRequest WHERE status=?", (status,))
        else:
            c.execute("SELECT id, emp_id, start_date, end_date, days, status FROM VacationRequest")
        rows = c.fetchall()
        conn.close()
        return rows

    def approve_request(self, req_id):
        conn = self._conn()
        c = conn.cursor()
        c.execute("SELECT emp_id, days, status FROM VacationRequest WHERE id=?", (req_id,))
        r = c.fetchone()
        if not r:
            conn.close()
            raise ValueError("Request not found")
        emp_id, days, status = r
        if status != "PENDING":
            conn.close()
            raise ValueError("Request already processed")
        c.execute("UPDATE VacationRequest SET status='APPROVED' WHERE id=?", (req_id,))
        c.execute("UPDATE Employee SET used_days = used_days + ? WHERE id=?", (days, emp_id))
        conn.commit()
        conn.close()

    def decline_request(self, req_id):
        conn = self._conn()
        c = conn.cursor()
        c.execute("UPDATE VacationRequest SET status='DECLINED' WHERE id=?", (req_id,))
        conn.commit()
        conn.close()

    def get_requests_by_employee(self, emp_id):
        conn = self._conn()
        c = conn.cursor()
        c.execute("SELECT id, start_date, end_date, days, status FROM VacationRequest WHERE emp_id=?", (emp_id,))
        rows = c.fetchall()
        conn.close()
        return rows

    # HRReport
    def generate_hr_report(self):
        conn = self._conn()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM Employee")
        total_employees = c.fetchone()[0]
        c.execute("SELECT SUM(used_days) FROM Employee")
        total_days_used = c.fetchone()[0] or 0
        report_date = date.today().isoformat()
        c.execute("INSERT INTO HRReport (report_date, total_employees, total_days_used) VALUES (?, ?, ?)",
                  (report_date, total_employees, total_days_used))
        conn.commit()
        conn.close()
        return {"report_date": report_date, "total_employees": total_employees, "total_days_used": total_days_used}

    def list_hr_reports(self):
        conn = self._conn()
        c = conn.cursor()
        c.execute("SELECT id, report_date, total_employees, total_days_used FROM HRReport ORDER BY id DESC")
        rows = c.fetchall()
        conn.close()
        return rows
