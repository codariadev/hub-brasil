# Autorização editorial

As rotas `/api/v1/editorial/*` exigem Firebase ID Token no cabeçalho Bearer. O
backend verifica assinatura, validade e revogação com Firebase Admin SDK e exige
`email_verified=true`.

Na primeira etapa, a allowlist contém somente `alves2.eduardo@gmail.com`, conforme
solicitado. O e-mail nunca é aceito do corpo da requisição. Esta allowlist é uma
medida temporária de bootstrap; a evolução prevista é atribuir papel editorial
por custom claims definidos exclusivamente pelo backend.

A publicação é transacional: somente itens `pending_review` e não demonstrativos
podem gerar artigo. A mesma transação atualiza o item de origem e grava uma ação
em `audit_logs`, com ator e data. O Admin SDK ignora Firestore Security Rules;
por isso, as credenciais do serviço devem ter IAM mínimo e permanecer apenas no
backend.
