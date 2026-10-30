import os

from app.schemas.article import Article
from app.schemas.category import Category

CATEGORIES = [
    Category(
        id="economia",
        name="Bolso e economia",
        description="Mudanças em preços, impostos, emprego e renda.",
    ),
    Category(
        id="saude",
        name="Saúde",
        description="Decisões, campanhas, serviços e orientações.",
    ),
    Category(
        id="educacao",
        name="Educação",
        description="Informações sobre escolas, universidades e oportunidades.",
    ),
    Category(
        id="direitos-cotidiano",
        name="Direitos e cotidiano",
        description="Direitos e caminhos para acessar serviços públicos.",
    ),
    Category(
        id="governo-decisoes",
        name="Governo e decisões",
        description="Decisões públicas e seus efeitos para a população.",
    ),
    Category(
        id="seguranca-meio-ambiente",
        name="Segurança e meio ambiente",
        description="Alertas, políticas e acontecimentos relevantes.",
    ),
]

EXAMPLE_ARTICLES = [
    Article(
        id="exemplo-canais-oficiais",
        title="Exemplo: como confirmar informações em canais oficiais",
        summary=(
            "Conteúdo demonstrativo para testar a apresentação de uma publicação. "
            "Não descreve uma notícia ou acontecimento real."
        ),
        category_id="direitos-cotidiano",
        category_name="Direitos e cotidiano",
        scope="national",
        is_example=True,
    ),
    Article(
        id="exemplo-orientacao-de-saude",
        title="Exemplo: onde buscar orientações de saúde pública",
        summary=(
            "Conteúdo demonstrativo para testar cartões e categorias na página inicial. "
            "Consulte os canais oficiais para informações vigentes."
        ),
        category_id="saude",
        category_name="Saúde",
        scope="national",
        is_example=True,
    ),
]


def list_categories() -> list[Category]:
    return CATEGORIES


def list_articles() -> list[Article]:
    if os.getenv("APP_ENV", "").lower() == "development":
        return EXAMPLE_ARTICLES
    return []