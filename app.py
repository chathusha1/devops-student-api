from flask import Flask, request, jsonify
from database import get_db_connection

app = Flask(__name__)

@app.route('/students', methods=['GET'])
def get_students():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return jsonify(students)

@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor()
    query = "INSERT INTO students (name, age, course) VALUES (%s, %s, %s)"
    values = (data['name'], data['age'], data['course'])
    
    cursor.execute(query, values)
    conn.commit()
    
    cursor.close()
    conn.close()
    return jsonify({"message": "Student added successfully!"}), 201

# PATCH - Student කෙනෙක්ගේ විස්තර වෙනස් කරන්න
@app.route('/students/<int:id>', methods=['PATCH'])
def update_student(id):
    data = request.get_json()
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor()
    query = "UPDATE students SET name = %s, age = %s, course = %s WHERE id = %s"
    values = (data['name'], data['age'], data['course'], id)
    
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"message": f"Student {id} updated successfully!"}), 200

# DELETE - Student කෙනෙක්ව අයින් කරන්න
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor()
    query = "DELETE FROM students WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"message": f"Student {id} deleted successfully!"}), 200
if __name__ == '__main__':
    app.run(debug=True, port=5000)