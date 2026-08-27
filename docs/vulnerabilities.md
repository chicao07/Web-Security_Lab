# Vulnerabilidades e Controle de Segurança

## Índice

- [1. IDOR / BOLA](#1-IDOR-/-BOLA)
  - [1.1 Descrição](#11-Descricao)
  - [1.2 Cenário vulnerável](#12-Cenario-vulneravel)
  - [1.3 Causa](#13-Causa)
  - [1.4 Impacto](#14-Impacto)
  - [1.5 Correção](#15-Correcao)
- [2. BOLA em API](#2-BOLA-em-API)
  - [2.1 Descrição](#21-Descricao)
  - [2.2 Cenário vulnerável](#22-Cenario-vulneravel)
  - [2.3 Causa](#23-Causa)
  - [2.4 Correção](#24-Correcao)
- [3. RBAC](#3-RBAC)
  - [3.1 Descrição](#31-Descricao)
  - [3.2 Regra](#32-Regra)
  - [3.3 Resultado esperado](#33-Resultado-esperado)
  - [3.4 Correção](#34-Correcao)
- [4. Escalada vertical de privilégios](#4-Escalada-vertical-de-privilégios)
  - [4.1 Descrição](#41-Descricao)
  - [4.2 Cenário](#42-Cenário)
- [5. Autorização baseada em dado controlado pelo cliente](#5-Autorização-baseada-em-dado-controlado-pelo-cliente)
  - [5.1 Descrição](#51-Descricao)
  - [5.2 Cenário](#52-Cenário)
  - [5.3 Causa](#53-Causa)
  - [5.4 Cenário](#54-Correção-conceitual)
 
    
## 1. IDOR / BOLA

### 1.1 Descrição

Foi criada uma rota de perfil na qual o identificador do recurso era fornecido pelo cliente.

### 1.2 Cenário vulnerável

Um usuário autenticado como Joao conseguiu solicitar: 

```http
GET /perfil/1002
```

e recebeu o perfil pertencente a Maria.

### 1.3 Causa

A implementação inicial verificava apenas se o identificador existia e não validava a relação entre o usuário autenticado e o objeto solicitado. 

### 1.4 Impacto

Um usuário autenticado poderia acessar objetos pertencentes a outros usuários.

### 1.5 Correção

A aplicação passou a obter o usuário autenticado através da sessão e comparar sua identidade com o proprietário do recurso.

Resultado esperado após a correção:

```text
Joao -> próprio perfil -> 200 OK
Joao -> perfil de Maria -> 403 Forbidden
```

## 2. BOLA em API

### 2.1 Descrição 

O mesmo conceito de controle de acesso foi reproduzido em uma API REST

### 2.2 Cenário vulnerável

Foi utilizado o endpoint:

```http
GET /api/orders/<id>
```

A implementação vulnerável retornava o objeto apenas verificando sua existência.

### 2.3 Causa

A API não verificava se o pedido solicitado pertencia ao usuário autenticado.

### 2.4 Correção

A implementação corrigida compara o usuário armazenado na sessão com o campo cliente do pedido.

## 3. RBAC

### 3.1 Descrição

Foi implementado controle de acesso baseado em funções

As funções utilizadas no laboratório são:

```text
user
admin
```

### 3.2 Regra

Usuários comuns não podem acessar: 

```http
GET /api/admin/users
```

Enquanto administradores podem.

### 3.3 Resultado esperado

```text
Não autenticado -> 401
user            -> 403
admin           -> 200
```

## 4. Escalada vertical de privilégios 

### 4.1 Descrição

Foi criado um cenário para testar se um usuário de baixo privilegio consegue acessar funcionalidades administrativas

### 4.2 Cenário

```text
Joao (user)
    |
/api/admin/users
```

O comportamento seguro e:

```text
403 Forbidden
```

Enquanto: 

```text
Admin
   |
/api/admin/users
   |
200 OK
```

## 5. Autorização baseada em dado controlado pelo cliente

### 5.1 Descrição 

Foi criada uma implementação deliberadamente vulnerável que utiliza o valor de role recebido através de um cookie para tomar decisões de autorização.

### 5.2 Cenário

```text
role=user
    |
   403
```

Após a alteração do valor controlado pelo cliente:

```text
role=admin
    |
   200
```

### 5.3 Causa

A aplicação confiava diretamente em um valor fornecido pelo cliente para determinar privilégios

### 5.4 Correção conceitual

A autorização deve ser baseada em uma identidade e privilégios determinados ou validados pelo servidor, e não simplesmente em uma declaração enviada pelo cliente.
