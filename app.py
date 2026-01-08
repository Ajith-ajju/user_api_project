from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "users.json"

def read_users():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        return json.load(file)

def write_users(users):
    with open(DATA_FILE, "w") as file:
        json.dump(users, file, indent=4)

@app.route("/users", methods=["GET"])
def get_users():
    users = read_users()
    return jsonify(users)

@app.route("/users", methods=["POST"])
def add_user():
    users = read_users()
    new_user = request.json
    users.append(new_user)
    write_users(users)
    return jsonify({"message": "User added successfully"}), 201

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    users = read_users()
    if user_id < len(users):
        return jsonify(users[user_id])
    return jsonify({"error": "User not found"}), 404

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    users = read_users()
    if user_id < len(users):
        users.pop(user_id)
        write_users(users)
        return jsonify({"message": "User deleted"})
    return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
