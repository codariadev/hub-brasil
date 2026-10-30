import type { Category } from "@/types/category";

export function CategoryList({
  categories,
  error,
}: {
  categories: Category[] | null;
  error: boolean;
}) {
  if (error || categories === null) {
    return (
      <p role="status" className="text-sm text-[#596762]">
        Não foi possível carregar as categorias. Confira se a API está em execução.
      </p>
    );
  }

  return (
    <div className="mt-8 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
      {categories.map((category) => (
        <article
          key={category.id}
          className="border border-[#d7ddd8] bg-[#fbfbf8] p-6 transition hover:border-[#17483f]"
        >
          <h3 className="text-lg font-bold text-[#182723]">{category.name}</h3>
          <p className="mt-3 text-sm leading-relaxed text-[#596762]">
            {category.description}
          </p>
        </article>
      ))}
    </div>
  );
}