## Ingestão de fontes

O sincronizador importa metadados de fontes oficiais para a coleção Firestore
`source_items`, sempre com `status=pending_review`. A importação não cria artigos
públicos e não aprova nem publica conteúdo.

São armazenados o título, resumo curto fornecido no feed, URL, fonte, data de
publicação, categorias e escopo regional. O corpo integral da matéria, imagens,
áudio e anexos não são copiados. A matéria original deve ser aberta e avaliada
por uma pessoa editora, que registra a fonte e redige conteúdo próprio antes da
publicação.

Categorias importadas são sugestões, não classificações editoriais finais. O
feed da Defesa Civil também contém monitoramentos e notícias; seus itens não são
marcados automaticamente como alertas. A classificação e a urgência precisam
ser confirmadas por uma pessoa revisora.

O catálogo inicial usa feeds oficiais confirmados do IBGE, Ministério da Saúde,
Notícias SC, Defesa Civil de SC, Alesc, ANS, IBAMA e Presidência da República.
As fontes marcadas como indisponíveis ou não confirmadas não são consultadas.
Novas fontes exigem confirmação do endpoint, frequência, acesso automatizado e
condições de reutilização antes de entrar no catálogo.

Links de itens importados só são aceitos quando usam o domínio oficial
configurado para a fonte. A coleta tem limite de tamanho e timeout, e IDs
determinísticos impedem importações duplicadas. Uma sincronização com falha em
uma fonte continua nas demais.

## Execução local

Instale as dependências em `apps/api` com `pip install -r requirements.txt`.
Configure Application Default Credentials do Firebase Admin fora do repositório
ou defina `GOOGLE_APPLICATION_CREDENTIALS` para um arquivo de credenciais local
protegido. Execute manualmente:

```bash
cd apps/api
python -m scripts.sync_sources
```

Uma fonte específica pode ser sincronizada com `--source`, por exemplo
`python -m scripts.sync_sources --source defesa-civil-sc`. A automação periódica
e a tela editorial de revisão ficam para etapas posteriores.
