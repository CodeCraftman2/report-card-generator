from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Student Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    course = db.Column(db.String(100), nullable=False)

# Create Database Tables
with app.app_context():
    db.create_all()

# Create (POST)
@app.route("/students", methods=["POST"])
def add_student():
    data = request.json
    new_student = Student(name=data["name"], age=data["age"], course=data["course"])
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"message": "Student added!", "id": new_student.id})

# Read (GET)
@app.route("/students", methods=["GET"])
def get_students():
    students = Student.query.all()
    return jsonify([{"id": s.id, "name": s.name, "age": s.age, "course": s.course} for s in students])

# Update (PUT)
@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"message": "Student not found"}), 404

    data = request.json
    student.name = data["name"]
    student.age = data["age"]
    student.course = data["course"]
    db.session.commit()
    return jsonify({"message": "Student updated!"})

# Delete (DELETE)
@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"message": "Student not found"}), 404

    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted!"})

if __name__ == "__main__":
    app.run(debug=True)
