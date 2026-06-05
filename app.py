from flask import Flask, jsonify, request
from database import get_db_connection, init_db

app = Flask(__name__)


@app.route("/students", methods=["GET"])
def get_students():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows])


@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
        (data["name"], data["age"], data["course"])
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Student added"}), 201


@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):
    data = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE id = ?", (id,))
    student = cursor.fetchone()

    if not student:
        return jsonify({"error": "Not found"}), 404

    cursor.execute("""
        UPDATE students
        SET name = ?, age = ?, course = ?
        WHERE id = ?
    """, (data["name"], data["age"], data["course"], id))

    conn.commit()
    conn.close()

    return jsonify({"message": "Updated"})


@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Deleted"})


if __name__ == "__main__":
    init_db()
    app.run(debug=True)