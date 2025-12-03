import sqlite3

conn = sqlite3.connect("students.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    grade TEXT,
    email TEXT UNIQUE
);
""")
print("Hello")
conn.commit()
conn.close()

print("Database created successfully!")
