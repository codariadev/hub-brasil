import { ArticleCard } from "@/features/articles/article-card";
import type { Article } from "@/types/article";

export function ArticleList({
	articles,
	error,
}: {
	articles: Article[] | null;
	error: boolean;
}) {
	if (error || articles === null) {
		return (
			<p role="status" className="border border-[#d7ddd8] bg-white p-6 text-sm text-[#596762]">
				Não foi possível carregar as publicações. Confira se a API está em execução.
			</p>
		);
	}

	if (articles.length === 0) {
		return (
			<p className="border border-dashed border-[#cbd3cc] bg-white p-6 text-sm text-[#596762]">
				Nenhuma publicação disponível no momento.
			</p>
		);
	}

	return (
		<div className="grid gap-5 md:grid-cols-2">
			{articles.map((article) => (
				<ArticleCard key={article.id} article={article} />
			))}
		</div>
	);
}
