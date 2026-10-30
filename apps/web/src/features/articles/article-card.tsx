import type { Article } from "@/types/article";

export function ArticleCard({ article }: { article: Article }) {
	return (
		<article className="flex h-full flex-col border-t-2 border-[#b07724] bg-white p-6 shadow-sm">
			<div className="flex items-center justify-between gap-3">
				<p className="text-xs font-semibold uppercase text-[#596762]">
					{article.category_name}
				</p>
				{article.is_example && (
					<span className="shrink-0 rounded-sm bg-[#fff0c9] px-2 py-1 text-[11px] font-bold uppercase text-[#714b10]">
						Exemplo
					</span>
				)}
			</div>
			<h3 className="mt-4 text-xl font-bold leading-snug text-[#182723]">
				{article.title}
			</h3>
			<p className="mt-3 text-sm leading-6 text-[#596762]">{article.summary}</p>
		</article>
	);
}
