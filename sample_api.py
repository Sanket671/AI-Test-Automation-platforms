from __future__ import annotations

from flask import Flask, jsonify, request

app = Flask(__name__)
USERS = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/users")
def list_users():
    return jsonify(USERS)


@app.get("/users/<int:user_id>")
def get_user(user_id: int):
    for user in USERS:
        if user["id"] == user_id:
            return jsonify(user)
    return jsonify({"error": "user not found"}), 404


@app.post("/users")
def create_user():
    body = request.get_json(silent=True) or {}
    name = body.get("name")
    if not name:
        return jsonify({"error": "name is required"}), 400
    user = {"id": len(USERS) + 1, "name": name}
    USERS.append(user)
    return jsonify(user), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
