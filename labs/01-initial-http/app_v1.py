from flask import Flask

app = Flask(__name__)

@app.route("/")
def inicio():
	return """
	<h1>Laboratorio de Pentest</h1>
	<p>Aplicacao web local.</p>

	<a href="/perfil/1001">Perfil Joao</a><br>
	<a href="/perfil/1002">Perfil Maria</a>
	"""

@app.route("/perfil/<int:id>")
def perfil(id):
	usuarios = {
		1001: "Joao",
		1002: "Maria"
	}

	if id not in usuarios:
		return "Usuario nao encontrado", 404

	return f"<h1>Perfil</h1><p>Usuario: {usuarios[id]}</p>"

if __name__ == "__main__":
	app.run(host="127.0.0.1", port=80000)
