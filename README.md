# Web Security Lab

Laboratório de segurança web desenvolvido em Flask para estudo pratico de autenticação, gerenciamento de sessões, controle de acesso e APIs REST 

## Índice

- [Objetivo](#Objetivo)
- [Conceitos estudados](#Conceitos-estudados)
- [Vulnerabilidades reproduzidas](#Vulnerabilidades-reproduzidas)
  - [IDOR / BOLA](#IDOR-/-BOLA)
  - [RBAC e escalada vertical](#RBAC-e-escalada-vertical)
- [Testes automatizados](#Testes-automatizados)
- [Estrutura](#Estrutura)
- [Execução](#Execucao)
- [Testes](#Testes)
- [Aviso](#Aviso)
- [Tecnologias](#Tecnologias)
- [Resultados](#Resultados)
- [Arquitetura](#Arquitetura)

## Objetivo

O projeto foi desenvolvido para estudar, reproduzir, analisar e corrigir vulnerabilidades relacionadas a autenticação e autorização em aplicações web.

## Conceitos estudados

- HTTP e analise de requisições
- Burp Suite
- Autenticação
- Cookies e sessões
- Password hashing
- IDOR 
- BOLA
- APIs REST
- RBAC
- Escalada de privilégios horizontal
- Escalada de privilégios vertical
- Validação de dados controlados pelo cliente
- Testes automatizados com pytest

## Vulnerabilidades reproduzidas

### IDOR / BOLA

Foi criada uma versão vulnerável em que um usuário autenticado conseguia acessar objetos pertencentes a outro usuário através de alteração do identificador do recurso.

A aplicação foi posteriormente corrigida com uma verificação de autorização baseada no usuário autenticado

### RBAC e escalada vertical

Foi implementado controle de acesso baseado em funções, sendo elas "user" e "admin". Usuários comum são impedidos de acessar endpoints administrativos

Também foi criada uma versão deliberadamente vulnerável que confia em uma função (role) fornecida pelo cliente, permitindo demostrar uma falha de escalada de privilégios.

## Testes automatizados

O projeto possui testes automatizados com pytest para verificar:

- Login valido
- Credenciais invalidas
- Acesso sem autenticação
- Acesso ao próprio perfil
- Tentativa de acesso ao perfil de outro usuário
- Acesso ao próprio pedido
- Tentativa de acesso ao pedido de outro usuário
- Restrições de acesso administrativo
- acesso administrativo autorizado
- Tratamento de recursos inexistentes

## Estrutura

```text
ciber-lab/
├── labs/
├── src/
├── tests/
├── docs/
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Execução

Clone o projeto e crie um ambiente virtual:

```bash
python3 -m venv venv 
source venv/bin/activate
```

Instale as dependências do projeto

```bash
pip install -r requirements.txt
```

Configure a chave da aplicação 

```bash
export SECRET_KEY="sua-chave-de-desenvolvimento"
```

Execute:

```bash
python src/app.py
```

A aplicação ficara disponível localmente em:

http://127.0.0.1:14464

## Testes

Execute:

```bash
pytest -v
```

## Aviso

Este projeto contem implementações deliberadamente vulneráveis para fins educacionais.

O laboratório deve ser executado somente em ambiente controlado e não deve ser exposto a internet ou utilizado em sistemas de terceiros.

## Tecnologias

- Python
- Flask
- Werkzeug
- pytest
- Burp Suite

## Resultados 

O laboratório foi utilizado para reproduzir e corrigir diferentes cenários de controle de acesso.

| Cenário | Antes | Depois |
|---------|-------|--------|
| Joao -> perfil de Maria | 200 OK | 403 Forbidden | 
| Joao -> pedido de Maria | 200 OK | 403 Forbidden |
| Usuario -> endpoint administrativo | 200 OK / vulneravel | 403 Forbidden |
| Administrador -> endpoint administrativo | 200 OK | 200 OK |
| 'role=user' -> 'role=admin' em implementação vulnerável | 403 Forbidden | 200 OK |

## Arquitetura 

```text
              +------------------+
              |      Cliente     |
              +--------+---------+
                       |
              +--------+---------+
              |                  |
            curl             Navegador
              |                  |
              +--------+---------+
                       |
                  Burp Suite
                       |
                       v
             Flask 127.0.0.1:14464
                       |
               +-------+-------+
               |               |
               v               v
            Sessão       Autorização
               |               |
               +-------+-------+
                       |
                       v
                 Dados locais
 ```
