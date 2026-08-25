from flask import Flask, request, session

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

		
	session["Usuario"] = username
	return f"Login realizado com sucesso! Usuario: {username}"

@app.route("/perfil/<int:id>")
def perfil(id):

	for username, dados in usuarios.items():

		if dados["id"] == id:
			return f"""
			<h1>Perfil</h1>
			<p>Usuario: {username}</p>
			<p>ID: {id}</p>
			"""

	return "Usuario nao encontrado", 404
	

if __name__ == "__main__":
	app.run(host="127.0.0.1", port=14464)
