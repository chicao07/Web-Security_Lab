# Importando nossa aplicacao
from app import app

# Criando o teste de login bem sucedido
def test_login_sucesso():
	# Definindo nossa aplicacao em modo de teste
	app.config["TESTING"] = True

	# Criando nossa resposta com base nos dados certos do cliente, adquiridos com o metodo post
	with app.test_client() as client:
		response = client.post(
			"/login",
			data={
				"username": "joao",
				"password": "1234"
			}
		)

	# Compara se o codigo do status da resposta e igual a 200
	assert response.status_code == 200

# Criando teste de login com a senha errada
def test_login_senha_incorreta():
	# Definindo nossa aplicacao em modo de teste
	app.config["TESTING"] = True

	# Criando nossa resposta com base nos dados com a senha errada do usuario, adquiridos com o metodo post
	with app.test_client() as client:
		response = client.post(
			"/login",
			data={
				"username": "joao",
				"password": "senha_errada"
			}
		)

	# Compara de o codigo de status da resposta e igual a 401
	assert response.status_code == 401

# Criando o teste usuario tenta acessar um perfil que nao e dele 
def test_joao_nao_acessa_perfil_maria():
	# Definindo nossa aplicacao em modo de teste
	app.config["TESTING"] = True

	# Criando um login correto do usuario, usando o metodo post
	with app.test_client() as client:

		login = client.post(
			"/login",
			data={
				"username": "joao",
				"password": "1234"
			}
		)

		# Verificando se o codigo de status do login e igual a 200
		assert login.status_code == 200

		# Defindo nossa resposta com a saida do cliente acessando um perfil que nao e dele
		response = client.get("/perfil/1002")

	# Verifica se o codigo de status da resposta e igual a 403
	assert response.status_code == 403

# Criando o teste "Usuario acessa seu perfil"
def test_joao_acessa_proprio_perfil():
	# Definindo a nossa aplicacao em modo de teste
	app.config["TESTING"] = True

	# Criando login com base nos dados corretos do usuario, adquiridos com o metodo post
	with app.test_client() as client:

		login = client.post(
			"/login",
			data={
				"username": "joao",
				"password": "1234"
			}
		)

		# Verifica se o codigo de status do login e igual a 200
		assert login.status_code == 200

		# Define nossa resposta com a saida de "Cliente tenta acessar seu proprio perfil" 
		response = client.get("perfil/1001")

	# Verifica se o codigo de status da resposta e igual a 200
	assert response.status_code == 200

# Criando o teste "Usuario acessa seu proprio pedido"
def test_joao_acessa_proprio_pedido():
	# Definindo a nossa aplicacao com o modo de teste
	app.config["TESTING"] = True

	# Criando login com base nos dados corretos do usuario, adquiridos com o metodo post
	with app.test_client() as client:

		login = client.post(
			"/login",
			data={
				"username": "joao",
				"password": "1234"
			}
		)

		# Verificando se o codigo de status do login e igual a 200
		assert login.status_code == 200

		# Definindo nossa resposta com a saida de "Cliente tenta acessar um pedido que e seu"
		response = client.get("/api/orders/501")

	# Verifica se o codigo de status da resposta e igual a 200
	assert response.status_code == 200

	# Define a variavel dados com o get_json, que retorna um arquivo.json com os pedidos
	dados = response.get_json()

	# Verifica se o id do pedido e o nome do cliente sao iguais a 501 e "joao"
	assert dados["id"] == 501
	assert dados["cliente"] == "joao"

# Criando o teste "Usuario nao acessa pedido de outros usuarios"
def test_joao_nao_acessa_pedido_maria():
	# Definindo nossa aplicacao com modo de teste
	app.config["TESTING"] = True

	# Criando login com base nos dados corretos do usuario, adquiridos com o metodo post
	with app.test_client() as client:

		login = client.post(
			"/login",
			data={
				"username": "joao",
				"password": "1234"
			}
		)

		# Verifica se o codigo de status do login e igual a 200
		assert login.status_code == 200

		# Definindo nossa resposta com a saida de "Cliente tenta acessar pedido que nao e seu"
		response = client.get("/api/orders/502")

	# Verifica se o codigo de status da resposta e igual a 403 
	assert response.status_code == 403

	# Definindo a variavel dados com o get_json, que retorna um arquivo json
	dados = response.get_json()

	# Verifica se a mensagem de erro no arquivo json da variavel dados e igual a "Acesso negado"
	assert dados["erro"] == "Acesso negado"

# Criando o teste de "usuario nao acessa funcao admin"
def test_usuario_nao_acessa_admin():
	# Definindo nossa aplicacao em modo de teste
	app.config["TESTING"] = True

	# Criando login com base nos dados corretos do usuario, adquiridos com o metodo post
	with app.test_client() as client:

		login = client.post(
			"/login",
			data={
				"username": "joao",
				"password": "1234"
			}
		)

		# Verificando se o codigo de status do login e igual a 200
		assert login.status_code == 200

		# Definindo nossa resposta com a saida de "cliente com role user, tenta acessar funcao de admin" 
		response = client.get("/api/admin/users")

	# Verifica se o codigo de status da resposta e igual a 403
	assert response.status_code == 403

# Criando o teste do "admin acessando a funcao admin"
def test_admin_acessa_admin():
	# Definido nossa aplicacao em modo de teste
	app.config["TESTING"] = True

	# Criando login baseado nos dados corretos do usuario, adquiridos com o metodo post
	with app.test_client() as client:

		login = client.post(
			"/login",
			data={
				"username": "admin",
				"password": "admin123"
			}
		)

		# Verifica se o codigo de status do login e igual a 200
		assert login.status_code == 200

		# Define nossa resposta com a saida de "cliente com role admin tentando acessar uma funcao de admin" 
		response = client.get("/api/admin/users")

	# Verifica se o codigo de status da resposta e igual a 200
	assert response.status_code == 200

	# Define dados com a saida de get_json, que retornara todos os usuario
	dados = response.get_json()

	# Verifica se o tamanho da variavel dados e igual a tres
	assert len(dados) == 3

# Criando o teste "acessar perfil sem estar logado"
def test_acesso_perfil_sem_login():
	# Define nossa aplicacao em modo de teste
	app.config["TESTING"] = True

	# Define nossa resposta com a saida de "cliente tenta acessar perfil sem estar logado"
	with app.test_client() as client:
		response = client.get("/perfil/1001")

	# Verifica se o codigo de status da resposta e igual a 401
	assert response.status_code == 401

# Criando o teste de "usuario inexistente"
def test_usuario_inexistente():
	# Definindo nossa aplicacao em modo de teste
	app.config["TESTING"] = True

	# Criando um login com base nos dados corretos do usuario, adquiridos com o metodo post
	with app.test_client() as client:
		login = client.post(
		
			"/login",
			data={
				"username": "joao",
				"password": "1234"
			}
		)

		# Verifica se o codigo de status de login e igual a 200
		assert login.status_code == 200

		# Define nossa resposta com a saida do "cliente acessando um perfil que nao existe"
		response = client.get("/perfil/9998")

	# Verifica se o codigo de status da resposta e igual a 404 
	assert response.status_code == 404
