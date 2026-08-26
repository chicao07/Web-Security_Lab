# Web Security Lab

Laboratorio de segurança web desenvolvido em Flask para estudo pratico de autenticacao, gerenciamento de sessoes, controle de acesso e APIs REST 

## Indice

- [Objetivo](#Objetivo)
- [Conceitos estudados](#Conceitos-estudados)

## Objetivo

O projeto foi desenvolvido para estudar, reproduzir, analisar e corrigir vulnerabilidades relacionadas a autenticacao e autorizacao em aplicacoes web.

## Conceitos estudados

- HTTP e analise de requisicoes
- Burp Suite
- Autenticacao
- Cookies e sessoes
- Password hashing
- IDOR 
- BOLA
- APIs REST
- RBAC
- Escalada de privilegios horizontal
- Escalada de privilegios vertical
- Validacao de dados controlados pelo cliente
- Testes automatizados com pytest

## Vulnerabilidades reproduzidas

### IDOR / BOLA

Foi criada uma versao vulneravel em que um usuario autenticado conseguia acessar objetos pertencentes a outro usuario atraves de alteracao do identificador do recurso.

A aplicacao foi posteriormente corrigida com uma verificacao de autorizacao baseada no usuario autenticado

### RBAC e escalada vertical

Foi implementado controle de acesso baseado em funcoes, sendo elas "user" e "admin". Usuarios comum sao impedidos de acessar endpoints administrativos

Tambem foi criada uma versao deliberadamente vulneravel que confia em uma funcao (role) fornecida pelo cliente, permitindo demostrar uma falha de escalada de privilegios.

## Testes automatizados

O projeto possui testes automatizados com pytest para verificar:

- Login valido
- Credenciais invalidas
- Acesso sem autenticacao
- Acesso ao proprio perfil
- Tentativa de acesso ao perfil de outro usuario
- Acesso ao proprio pedido
- Tentativa de acesso ao pedido de outro usuario
- Restricoes de acesso administrativo
- acesso administrativo autorizado
- Tratamento de recursos inexistentes

## Estrutura

ciber-lab/
|
|-- labs/
|
|-- src/
|
|-- tests/
|
|-- docs/
|
|-- .env.example
|
|-- .gitignore
|
|-- pyproject.toml
|
|-- requirements.txt
|
|__ README.md

## Execucao

Clone o projeto e crie um ambiente virtual:

```bash
python3 -m venv venv 
source venv/bin/activate
```

Instale as dependencias do projeto

```bash
pip install -r requirements.txt
```

Configure a chave da aplicacao 

```bash
export SECRET_KEY="sua-chave-de-desenvolvimento"
```

Execute:

```bash
python src/app.py
```

A aplicacao ficara disponivel localmente em:

http://127.0.0.1:14464

## Testes

Execute:

```bash
pytest -v
```

## Aviso

Este projeto contem implementacoes deliberadamente vulneraveis para fins educacionais.

O laboratorio deve ser executado somente em ambiente controlado e nao deve ser exposto a internet ou utilizado em sistemas de terceiros.

## Tecnologias

- Python
- Flask
- Werkzeug
- pytest
- Burp Suite

## Resultados 

O laboratorio foi utilizado para reproduzir e corrigir diferentes cenarios de controle de acesso.

| Cenario | Antes | Depois |
|---------|-------|--------|
| Joao -> perfil de Maria | 200 OK | 403 Forbidden | 
| Joao -> pedido de Maria | 200 OK | 403 Forbidden |
| Usuario -> endpoint administrativo | 200 OK / vulneravel | 403 Forbidden |
| Administrador -> endpoint administrativo | 200 OK | 200 OK |
| 'role=user' -> 'role=admin' em implementacao vulneravel | 403 Forbidden | 200 OK |

## Arquitetura 

Client / curl / navegador
          |
      Burp Suite
          |
 Flask 127.0.0.1:14464
          |
  +-------+-------+
  |               |
Sessao       Autorizacao
  |               |
  +-------+-------+
          |
     Dados locais
 
