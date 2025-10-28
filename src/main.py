import sqlite3

conn = sqlite3.connect("vacations.db")
c = conn.cursor()

query = '''
SELECT e.name, d.name, v.start_date, v.end_date, v.status
FROM Employee e
JOIN Department d ON e.department = d.id
JOIN VacationRequest v ON e.id = v.emp_id
ORDER BY e.name
'''
for row in c.execute(query):
    print(row)

conn.close()
