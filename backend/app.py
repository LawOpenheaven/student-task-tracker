print("app.py is running")
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config import Config
from models import db
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from flask_cors import CORS
from models import Task

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)

@app.route("/")
def home():
    return jsonify({"message": "Student Task Tracker API running"})
#new
@app.route("/register", methods=["OPTIONS"])
def register_options():
    return jsonify({}), 200


@app.route("/register", methods=["POST", "OPTIONS"])
def register():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    hashed_password = generate_password_hash(password)

    new_user = User(
        email=email,
        password_hash=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user.id))

    return jsonify({"access_token": access_token}), 200

@app.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    return jsonify({"message": f"Hello user {user_id}, you are authenticated!"})


from datetime import datetime

# Create a task
@app.route("/tasks", methods=["POST"])
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    data = request.get_json()

    title = data.get("title")
    description = data.get("description")
    due_date = data.get("due_date")

    if not title or not due_date:
        return jsonify({"error": "Title and due_date are required"}), 400

    task = Task(
        title=title,
        description=description,
        due_date=datetime.strptime(due_date, "%Y-%m-%d").date(),
        user_id=user_id
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({"message": "Task created successfully"}), 201

# Get all tasks 
@app.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()

    tasks = Task.query.filter_by(user_id=user_id).all()

    result = []
    for task in tasks:
        result.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "due_date": task.due_date.isoformat(),
            "completed": task.completed
        })

    return jsonify(result), 200


# update task
@app.route("/tasks/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if not task:
        return jsonify({"error": "Task not found"}), 404

    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.completed = data.get("completed", task.completed)

    db.session.commit()

    return jsonify({"message": "Task updated successfully"}), 200

# Delete Task
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()

    task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted successfully"}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)