# API de conteúdo público

Prefixo: `/api/v1`. As rotas abaixo são públicas e não exigem Firebase ID Token.

## `GET /categories`

Retorna as seis categorias editoriais do produto.

```json
[
	{
		"id": "economia",
		"name": "Bolso e economia",
		"description": "Mudanças em preços, impostos, emprego e renda."
	}
]
```

## `GET /articles`

Retorna apenas artigos com `status=published` do Firestore. Em desenvolvimento,
se não houver artigos publicados, retorna registros demonstrativos com
`is_example: true`; eles não descrevem notícias reais.

```json
[
	{
		"id": "exemplo-canais-oficiais",
		"title": "Exemplo: como confirmar informações em canais oficiais",
		"summary": "Conteúdo demonstrativo; não descreve uma notícia real.",
		"category_id": "direitos-cotidiano",
		"category_name": "Direitos e cotidiano",
		"scope": "national",
		"published_at": null,
		"is_example": true
	}
]
```

## Rotas editoriais protegidas

As rotas editoriais exigem `Authorization: Bearer <Firebase ID Token>`. O token
é verificado pelo Firebase Admin SDK, incluindo revogação. Somente a conta
`alves2.eduardo@gmail.com` com e-mail verificado é autorizada nesta etapa.

### `GET /editorial/source-items`

Lista até 50 itens com `status=pending_review`. Retorna `401` sem token válido e
`403` para qualquer outra conta.

### `POST /editorial/source-items/{item_id}/publish`

Publica uma versão editorial revisada do item. A categoria precisa existir na
taxonomia do Hub Brasil, e o item precisa estar pendente e não ser demonstrativo.
A operação grava o artigo em `articles`, atualiza o item de origem e cria um
registro em `audit_logs` na mesma transação.

```json
{
	"title": "Título revisado pela editoria",
	"summary": "Resumo original escrito para o Hub Brasil, com contexto claro.",
	"content": "Texto editorial revisado, com fatos, contexto e orientação ao cidadão.",
	"category_id": "saude"
}
```

O e-mail do autor é obtido exclusivamente do token verificado; campos enviados
pelo cliente não podem substituir a identidade autenticada. Respostas: `201`
publicado, `401` token ausente/inválido, `403` conta não autorizada, `404` item
inexistente, `409` item já revisado/publicado e `422` dados/categoria inválidos.
