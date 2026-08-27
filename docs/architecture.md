# Arquitetura do Laboratorio

## Índice

- [Visao geral](#Visao-geral)
- [Componentes](#Componentes)
  - [Aplicacao Flask](#Aplicacao-Flask)
  - [Cliente HTTP](#Cliente-HTTP)
  - [Burp Suite](#Burp-Suite)
  - [Testes automatizados](#Testes-automatizados)
- [Fluxo de comunicacao](#Fluxo-de-comunicacao)
- [Controle de sessao](#Controle-de-sessao)
- [Controle de acesso](#Controle-de-acesso)
- [Ambiente](#Ambiente)
 
## Visao geral

O Web Security Lab e uma aplicacao web local desenvolvida em Flask para estudo pratico de autenticacao, sessoes, controle de acesso, APIs REST e vulnerabilidades relacionadas a autorizacao.

## Componentes

### Aplicacao Flask

A aplicacao principal esta localizada em 'src/app.py' e e executada localmente na porta '14464'.

### Cliente HTTP

Durante os exercicios, foram utilizados 'curl' e navegador para gerar requisicoes HTTP

### Burp Suite

O Burp Suite atua como proxy entre o cliente e a aplicacao, permitindo interceptar, visualizar e repetir requisicoes HTTP.

### Testes automatizados

Os testes estao em 'tests/tests_app.py' e utilizam 'pytest' e o cliente de testes do Flask.

## Fluxo de comunicacao

```text
Cliente
   |
   | HTTP Request
   |
Burp Suite
   |
   | HTTP Request
   |
 Flask
   |
   +--> Autenticacao
   |
   +--> Sessao
   |
   +--> Autorizacao
   |
   +--> APIs REST
   |
   |
HTTP Response
   |
   |
Burp / Cliente
```

## Controle de sessao

Apos a autenticacao, a aplicacao utiliza a sessao do Flask para identificar o usuario autenticado entre diferentes requisicoes.

A sessao e associada a um cookie enviado pelo cliente nas requisicoes subsequentes.

## Controle de acesso

A aplicacao utiliza diferentes mecanismos de autorizacao:

- Controle horizontal sobre objetos pertencentes a diferentes usuarios.
- RBAC para diferenciar usuarios comuns e administradores.
- Verificacao de autorizacao no lado do servidor.

## Ambiente

A aplicacao foi desenvolvida e testada em ambiente virtual Python dentro de uma maquina virtual dedicada ao laboratorio

O servico Flask utiliza:

```text
127.0.0.1:14464
```

O Burp Suite utiliza o proxy local configurado para interceptacao das requisicoes. 
