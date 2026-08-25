from flask import Flask, request, session, jsonify

app = Flask(__name__)

app.secret_key = "chave-do-laboratorio"

usuarios = {
	"joao": {
		"senha": "1234",
		"id": 1001
	},
	"maria": {
		"senha": "5678",
		"id": 1002
	}
}

@app.route("/")
def inicio():
	return """
	<h1>Laboratorio de Pentest</h1>

	<a href="/login">Login</a><br>
	<a href="/perfil/1001">Perfil Joao</a><br>
	<a href="/perfil/1002">Perfil Maria</a>
	"""

@app.route("/login", methods=["GET", "POST"])
def login():

	if request.method == "GET":
		return """
		<h1>Login</h1>

		<form method="POST" action="/login">
			<label>Usuario:</label>
			<input type="text" name="username">

			<br><br>

			<label>Senha:</label>
			<input type="password" name="password">

			<br><br>

			<button type="submit">Entrar</button>
		</form>
		"""

	username = request.form.get("username")
	password = request.form.get("password")

	if username not in usuarios:
		return "Usuario ou senha invalidos", 401

	if usuarios[username]["senha"] != password:
		return "Usuario ou senha invalidos", 401

		
	session["usuario"] = username
	return f"Login realizado com sucesso! Usuario: {username}"

@app.route("/perfil/<int:id>")
def perfil(id):

	usuario_atual = session.get("usuario")

	if usuario_atual is None:
		return "Voce precisa estar logado", 401

	for username, dados in usuarios.items():

		if dados["id"] == id:

			if username != usuario_atual:
				return "Acesso negado", 403
		
			return f"""
			<h1>Perfil</h1>
			<p>Usuario: {username}</p>
			<p>ID: {id}</p>
			"""

	return "Usuario nao encontrado", 404

@app.route("/api/users/<int:id>")
def api_user(id):

	usuario_atual = session.get("usuario")

	if usuario_atual is None:
		return jsonify({
			"erro": "Autenticacao necessaria"
		}), 401

	for username, dados in usuarios.items():

		if dados["id"] == id:

			if username != usuario_atual:
				return jsonify({
					"erro": "Acesso negado"
				}), 403
		
			return jsonify({
				"id": id,
				"usuario": username
			})

	return jsonify({
		"erro": "Usuario nao encontrado"
	}), 404

pedidos = {
	501: {
		"id": 501,
		"cliente": "joao",
		"produto": "notebook"
	},

	502: {
		"id": 502,
		"cliente": "maria",
		"produto": "celular"
	}
}

@app.route("/api/orders/<int:id>")
def api_order(id):

	usuario_atual = session.get("usuario")

	if usuario_atual is None:
		return jsonify({
			"erro": "Autenticacao necessaria"
		}), 401

	if id not in pedidos:
		return jsonify({
			"erro": "Pedido nao encontrado"
		}), 404

	pedido = pedidos[id]

	if pedido["cliente"] != usuario_atual:
		return jsonify({
			"erro": "Acesso negado"
		}), 403

	return jsonify(pedidos[id])

if __name__ == "__main__":
	app.run(host="127.0.0.1", port=14464)
