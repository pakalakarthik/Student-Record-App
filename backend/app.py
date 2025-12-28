from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS
import time
import sqlite3
# Create the Flask application object. __name__ tells Flask where to look
# for templates and static files; it's the module name of the current file.
app = Flask(__name__)
CORS(app)


# Helper to open a database connection. We keep this in one function so
# all endpoints open the DB consistently and we can change settings here.
def get_db_connection():
    # Open (or create) the SQLite database file named students.db
    conn = sqlite3.connect("students.db", timeout=10, check_same_thread=False)
    # Enable WAL mode so concurrent reads/writes work better
    conn.execute("PRAGMA journal_mode=WAL;")
    # Make fetched rows behave like dictionaries (access by column name)
    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA synchronous=NORMAL;")
    # Return the connection object to the caller
    return conn


# Route for the root path. Visiting http://127.0.0.1:5000/ will call this.
@app.route("/")
def home():
    # Return a simple text response confirming the API is running
    return "Student API is running!"


# -------- READ All Students --------
# Handle GET requests to /students and return all student records
@app.route("/students", methods=["GET"])
def get_students():
    # Open DB connection using helper
    conn = get_db_connection()
    # Create a cursor to execute SQL queries
    cur = conn.cursor()
    # Run SQL to select all rows from the students table
    cur.execute("SELECT * FROM students")
    # Fetch all rows returned by the query
    rows = cur.fetchall()
    # Close the connection promptly to free the DB for other operations
    conn.close()
    # Debug print (not required) — removed or kept for learning purposes
    print("students fetched")

    # Convert each sqlite Row into a plain dict so it can be JSON-encoded
    students = [dict(row) for row in rows]
    # Return the list of students as JSON response
    return jsonify(students)


# -------- CREATE Student --------
# Handle POST requests to /students to insert a new student record
@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()
    name = data["name"]
    age = data["age"]
    grade = data["grade"]
    email = data["email"]

    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO students (name, age, grade, email) VALUES (?, ?, ?, ?)",
            (name, age, grade, email)
        )
        conn.commit()
        new_id = cur.lastrowid
        return jsonify({"message": "Student added", "id": new_id})
    finally:
        conn.close()



# -------- UPDATE Student --------
# Handle PUT requests to /students/<id> to update an existing student
@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):
    data = request.get_json()

    conn = get_db_connection()
    try:
        conn.execute("""
            UPDATE students
            SET name = ?, age = ?, grade = ?, email = ?
            WHERE id = ?
        """, (data["name"], data["age"], data["grade"], data["email"], id))
        conn.commit()
        return jsonify({"message": "Student updated"})
    finally:
        conn.close()



# -------- DELETE Student --------
# Handle DELETE requests to /students/<id> to remove a student record


@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    conn = get_db_connection()
    try:
        for attempt in range(5):
            try:
                conn.execute("DELETE FROM students WHERE id = ?", (id,))
                conn.commit()
                return jsonify({"message": "Student deleted"})
            except sqlite3.OperationalError as e:
                if "locked" in str(e).lower() and attempt < 4:
                    time.sleep(0.2)  # wait and retry
                else:
                    raise
    finally:
        conn.close()



# When this file is run directly, start Flask's development server
if __name__ == "__main__":
    # debug=True enables auto-reload and a helpful debugger on errors
    #app.run(debug=True)
      import os
      port = int(os.environ.get("PORT", 5000))
      app.run(host="0.0.0.0", port=port, debug=False)

