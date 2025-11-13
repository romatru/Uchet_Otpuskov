import os
import csv
import json
import yaml
import sqlite3
import xml.etree.ElementTree as ET
from xml.dom import minidom

DB_PATH = "vacations.db"
OUT_DIR = "out"

os.makedirs(OUT_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("""
    SELECT 
        e.id,
        e.name,
        e.position,
        e.total_days,
        e.used_days,
        d.name AS department
    FROM Employee e
    LEFT JOIN Department d ON e.department = d.id
""")
rows = [dict(row) for row in cursor.fetchall()]
conn.close()

# JSON
with open(f"{OUT_DIR}/data.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=4)

# CSV
with open(f"{OUT_DIR}/data.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

# XML
root = ET.Element("employees")
for r in rows:
    emp = ET.SubElement(root, "employee")
    for k, v in r.items():
        child = ET.SubElement(emp, k)
        child.text = str(v)
xml_str = ET.tostring(root, encoding="utf-8")
parsed_xml = minidom.parseString(xml_str)
pretty_xml = parsed_xml.toprettyxml(indent="  ", encoding="utf-8")
with open(f"{OUT_DIR}/data.xml", "wb") as f:
    f.write(pretty_xml)

# YAML
with open(f"{OUT_DIR}/data.yaml", "w", encoding="utf-8") as f:
    yaml.dump(rows, f, allow_unicode=True, sort_keys=False)

print("Экспорт завершён.")