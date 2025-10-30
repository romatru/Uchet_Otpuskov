import sqlite3

def insert(path="vacations.db"):
    conn = sqlite3.connect(path)
    c = conn.cursor()

    # departments
    departments = [("Бухгалтерия",), ("ИТ-отдел",), ("Отдел кадров",)]
    c.executemany("INSERT INTO Department (name) VALUES (?)", departments)

    # employees
    employees = [
        ("Иванов И.И.", 1, "Бухгалтер", 28, 5),
        ("Петров П.П.", 2, "Программист", 28, 10),
        ("Сидоров Г.В.", 3, "HR", 28, 7),
        ("Трушков Р.Е.", 2, "Программист", 28, 0)
    ]
    c.executemany("INSERT INTO Employee (name, department, position, total_days, used_days) VALUES (?, ?, ?, ?, ?)", employees)

    # requests
    requests = [
        (1, "2025-06-01", "2025-06-14", 14, "APPROVED"),
        (2, "2025-07-10", "2025-07-20", 10, "PENDING"),
        (3, "2025-08-01", "2025-08-15", 14, "APPROVED"),
        (4, "2025-10-01", "2025-10-15", 14, "APPROVED")
    ]
    c.executemany("INSERT INTO VacationRequest (emp_id, start_date, end_date, days, status) VALUES (?, ?, ?, ?, ?)", requests)

    conn.commit()
    conn.close()
    print("Тестовые данные добавлены.")

if __name__ == "__main__":
    insert()
