# Importando blibliotecas
import os
from flask import Flask, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

# Definindo o nome da API
app = Flask(__name__)

# Definido nossa chave secreta baseada na variavel secreta do sistema operacional
app.secret_key = os.environ.get("SECRET_KEY")

# Criando um dicionario onde armazenara os dados dos usuarios
usuarios = {
	"joao": {
		"senha": generate_password_hash("1234"),
		"id": 1001,
		"role": "user"
	},
	"maria": {
		"senha": generate_password_hash("5678"),
		"id": 1002,
		"role": "user"
	},
	"admin": {
		"senha": generate_password_hash("admin123"),
		"id": 9999,
		"role": "admin"
	}
}

# Criando nossa funcao inicio
@app.route("/")
def inicio():
	return """
	<h1>Laboratorio de Pentest</h1>

	<a href="/login">Login</a><br>
	<a href="/perfil/1001">Perfil Joao</a><br>
	<a href="/perfil/1002">Perfil Maria</a>
	"""

# Criando a funcao de login
@app.route("/login", methods=["GET", "POST"])
def login():

	# Se o metodo resultando for GET, pega o nome de usuario e senha do usuario
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

	# Definindo as variaveis de nome e senha, de acordo com o input do usuario
	username = request.form.get("username")
	password = request.form.get("password")

	# Se nome nao estiver dentro de usuarios, retorne erro
	if username not in usuarios:
		return "Usuario ou senha invalidos", 401

	# Se o hash da senha digitada pelo usuario for diferente do hash da senha correta, retorne erro
	if not check_password_hash(usuarios[username]["senha"], password):
		return "Usuario ou senha invalidos", 401

	# Define e guarda em sessao, o nome de usuario e seu role
	session["usuario"] = username
	session["role"] = usuarios[username]["role"]

	# Exibe mensagem de sucesso terminando o login do usuario
	return f"Login realizado com sucesso! Usuario: {username}"

# Criando a funcao de id
@app.route("/perfil/<int:id>")
def perfil(id):

	# Define a variavel de usuario atual com o usuario de sessao
	usuario_atual = session.get("usuario")

	# Verifica se o usuario esta logado 
	if usuario_atual is None:
		return "Voce precisa estar logado", 401

	# Itera os atributos de usuario
	for username, dados in usuarios.items():

		# Se o id digitado pelo usuario, diferente do id do seu perfil, entao retorna erro
		if dados["id"] == id:

			# Verifica se o usuario logado, e o mesmo do perfil que esta tentando acessar, se nao retorna erro
			if username != usuario_atual:
				return "Acesso negado", 403

			# Se tudo ocorrer bem, o perfil
			return f"""
			<h1>Perfil</h1>
			<p>Usuario: {username}</p>
			<p>ID: {id}</p>
			"""

	# Caso nao ache o usuario atual no dicionario, retorna erro
	return "Usuario nao encontrado", 404

# Definindo a funcao de id usuario, usando API
@app.route("/api/users/<int:id>")
def api_user(id):

	# Define usuario atual igual a usuario de sessao
	usuario_atual = session.get("usuario")

	# Verifica se usuario esta logado
	if usuario_atual is None:
		return jsonify({
			"erro": "Autenticacao necessaria"
		}), 401

	# Itera os atributos do dicionario do usuario
	for username, dados in usuarios.items():

		# Verifica se o id solicitado e o mesmo do usuario atual
		if dados["id"] == id:

			# Verifica se o nome do usuario pertencente aquele perfil e igual ao do usuario atual
			if username != usuario_atual:
				return jsonify({
					"erro": "Acesso negado"
				}), 403

			# Se tudo ocorrer bem, retorna o id e nome do usuario desejado
			return jsonify({
				"id": id,
				"usuario": username
			})

	# Se nao encontrar os dados no dicionario, retorna erro
	return jsonify({
		"erro": "Usuario nao encontrado"
	}), 404

# Criando um dicinario de pedidos, com id, nome do cliente e nome do produto
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

# Criando a funcao de pedido, usando API
@app.route("/api/orders/<int:id>")
def api_order(id):

	# Definindo o usuario atual como o usuario de sessao
	usuario_atual = session.get("usuario")

	# Verifica se o usuario esta logado
	if usuario_atual is None:
		return jsonify({
			"erro": "Autenticacao necessaria"
		}), 401

	# Verifica se o id do produto existe
	if id not in pedidos:
		return jsonify({
			"erro": "Pedido nao encontrado"
		}), 404

	# Define a variavel pedido com o pedido desejado pelo usuario
	pedido = pedidos[id]

	# Verifica se o nome do cliente do pedido desejado, e igual ao do usuario atual
	if pedido["cliente"] != usuario_atual:
		return jsonify({
			"erro": "Acesso negado"
		}), 403

	# Se tudo ocorrer bem retorna o pedido com o id desejado
	return jsonify(pedidos[id])

# Criando a funcao de adm usando API
@app.route("/api/admin/users")
def admin_users():

	# Define o usuario atual como o usuario de sessao
	usuario_atual = session.get("usuario")

	# Verifica se o usuario esta logado
	if usuario_atual is None:
		return jsonify({
			"erro": "Autenticacao necessaria"
		}), 401

	# Define a role atual como a role de sessao
	role_atual = session.get("role")

	# Verifica se o role atual e igual a admin
	if role_atual != "admin":
		return jsonify({
			"erro": "permissao insuficiente"
		}), 403

	# Criando uma lista	
	resultado = []

	# Itera todos os atributos do dicionario de usuario, e os adiciona na lista resultado 
	for username, dados in usuarios.items():
		resultado.append({
			"id": dados["id"],
			"usuario": username,
			"role": dados["role"]
		})

	# Se tudo ocorrer bem, retorna a lista com todos os usuarios
	return jsonify(resultado)

# Iniciando a aplicacao flask e defindo a porta 14464
if __name__ == "__main__":
	app.run(host="127.0.0.1", port=14464)
