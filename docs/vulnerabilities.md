# Vulnerabilidades e Controle de Seguranca

## 1. IDOR / BOLA

### Descricao

Foi criada uma rota de perfil na qual o identificador do recurso era fornecido pelo cliente.

### Cenario vulneravel

Um usuario autenticado como Joao conseguiu solicitar: 

```http
GET /perfil/1002
```

e recebeu o perfil pertencente a Maria.

### Causa

A implementacao inicial verificava apenas se o identificador existia e nao validava a relacao entre o usuario autenticado e o objeto solicitado. 

### Impacto

Um usuario autenticado poderia acessar objetos pertencentes a outros usuarios.

### Correcao

A aplicacao passou a obter o usuario autenticado atraves da sessao e comparar sua identidade com o proprietario do recurso.

Resultado esperado apos a correcao:

```text
Joao -> proprio perfil -> 200 OK
Joao -> perfil de Maria -> 403 Forbidden
```

## 2. BOLA em API

### Descricao 

O mesmo conceito de controle de acesso foi reproduzido em uma API REST

### Cenario vulneravel

Foi utilizado o endpoint:

```http
GET /api/orders/<id>
```

A implementacao vulneravel retornava o objeto apenas verificando sua existencia.

### Causa

A API nao verificava se o pedido solicitado pertencia ao usuario autenticado.

### Correcao

A implementacao corrigida compara o usuario armazenado na sessao com o campo cliente do pedido.

## 3. RBAC

### Descricao

Foi implementado controle de acesso baseado em funcoes

As funcoes utilizadas no laboratorio sao:

```text
user
admin
```

### Regra

Usuarios comuns nao podem acessar: 

```http
GET /api/admin/users
```

Enquanto administradores podem.

### Resultado esperado

```text
Nao autenticado -> 401
user            -> 403
admin           -> 200
```

## 4. Escalada vertical de privilegios 

### Descricao

Foi criado um cenario para testar se um usuario de baixo privilegio consegue acessar funcionalidades administrativas

### Cenario

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

## 5. Autorizacao baseada em dado controlado pelo cliente

### Descricao 

Foi criada uma implementacao deliberadamente vulneravel que utiliza o valor de role recebido atraves de um cookie para tomar decisoes de autorizacao.

### Cenario

```text
role=user
    |
   403
```

Apos a alteracao do valor controlado pelo cliente:

```text
role=admin
    |
   200
```

### Causa

A aplicacao confiava diretamente em um valor fornecido pelo cliente para determinar privilegios

### Correcao conceitual

A autorizacao deve ser baseada em uma identidade e privilegios determinados ou validados pelo servidor, e nao simplesmente em uma declaracao enviada pelo cliente.
