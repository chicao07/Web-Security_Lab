# Metodologia de Testes

## Objetivo

A metodologia utilizada no laboratorio busca reproduzir vulnerabilidades de forma controlada, identificar a causa da falha, implementar uma correcao e validar novamente o comportamento.

## Processo

O processo adotado foi:

```text
Reconhecimento
      |
Entendimento da aplicacao
      |
  Baseline
      |
Manipulacao controlada
      |
Analise da resposta
      |
Identificacao da falha
      |
   Correcao
      |
   Reteste
```

## Baseline

Antes de testar uma regra de seguranca, foi estabelecido um comportamento esperado.

Exemplo:

```text
Joao -> /perfil/1001 -> 200 OK
```

Esse comportamento foi utilizado como referencia para os testes seguintes.

## Manipulacao controlada

As requisicoes foram modificadas alterando-se uma variavel por vez, como:

- Identificador de objeto
- Usuario
- Senha
- Role
- Endpoint

## Analise

Foram analisados: 

- Metodo HTTP
- Endpoint
- Headers
- Cookies
- Corpo da requisicao
- Status HTTP
- Corpo da resposta
- Comportamento do servidor

## Exploracao controlada

As vulnerabilidades foram reproduzidas exclusivamente dentro da aplicacao desenvolvida para o laboratorio.

## Correcao

Apos a identificacao da falha, a logica de autorizacao foi alterada no lado do servidor

## Reteste

Apos a correcao, os mesmos cenarios foram executados novamente para verificar se o comportamento vulneravel havia sido removido

## Automacao

As principais regras de seguranca tambem foram convertidas em testes automatizados utilizando o pytest.

Isso permite detectar regressoes futuras no controle de acesso.
