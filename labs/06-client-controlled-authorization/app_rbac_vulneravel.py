from flask import Flask, request, jsonify

app = Flask(__name__)

app.route("/login")
def login():
	return "Use /api/admin/users com um cookie role=user ou role=admin"

@app.route("/api/admin/users")
def admin_users():

	role  = request.cookies.get("role")

	if role != "admin":
		return jsonify({
			"erro": "Permissao insuficiente"
		}), 403

	return jsonify([
		{
			"id": 1001,
			"usuario": "joao",
			"role": "user"
		},
		
		{
			"id": 1002,
			"usuario": "maria",
			"role": "user"
		},

		{
			"id": 9999,
			"usuario": "admin",
			"role": "admin"
		}
	])

if __name__ == "__main__":
	app.run(host="127.0.0.1", port=15555)
