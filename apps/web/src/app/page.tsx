import Link from "next/link";
import { AccountNav } from "@/features/auth/account-nav";
import { ArticleList } from "@/features/articles/article-list";
import { CategoryList } from "@/features/home/category-list";
import { fetchPublicApi } from "@/lib/api/public";
import type { Article } from "@/types/article";
import type { Category } from "@/types/category";

async function loadContent<T>(path: string): Promise<T | null> {
  try {
    return await fetchPublicApi<T>(path);
  } catch {
    return null;
  }
}

export default async function HomePage() {
  const [articles, categories] = await Promise.all([
    loadContent<Article[]>("articles"),
    loadContent<Category[]>("categories"),
  ]);

  return (
    <main className="min-h-screen">
      <header className="border-b border-[var(--border)] bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <Link href="/" className="text-2xl font-bold text-[var(--primary)]">
            Hub Brasil
          </Link>

          <nav className="hidden gap-6 text-sm font-medium md:flex">
            <Link href="#brasil">Brasil</Link>
            <Link href="#categorias">Categorias</Link>
            <Link href="#orientacao">Orientação</Link>
          </nav>

          <AccountNav />
        </div>
      </header>

      <section className="bg-[#17483f] px-6 py-20 text-white">
        <div className="mx-auto max-w-7xl">
          <p className="mb-4 text-sm font-semibold uppercase tracking-widest text-amber-300">
            Informação pública em linguagem acessível
          </p>

          <h1 className="max-w-3xl text-4xl font-bold leading-tight md:text-6xl">
            O Brasil acontece. O povo precisa entender.
          </h1>

          <p className="mt-6 max-w-2xl text-lg leading-relaxed text-slate-200">
            Entenda o que está acontecendo no país, o que muda na sua vida
            e onde encontrar informações oficiais para agir.
          </p>

          <Link
            href="#brasil"
            className="mt-8 inline-block rounded-lg bg-amber-400 px-6 py-3 font-semibold !text-slate-950"
          >
            Explorar informações
          </Link>
        </div>
      </section>

      <section id="brasil" className="mx-auto max-w-7xl px-6 py-16">
        <div className="mb-8">
          <p className="text-sm font-semibold uppercase tracking-wider text-[var(--secondary)]">
            Informação para todos
          </p>
          <h2 className="mt-2 text-3xl font-bold">O que importa no Brasil</h2>
          <p className="mt-3 max-w-2xl text-[var(--muted)]">
            Acompanhe informações nacionais e entenda seus possíveis impactos.
          </p>
        </div>

        <ArticleList articles={articles} error={articles === null} />
      </section>

      <section id="categorias" className="bg-white px-6 py-16">
        <div className="mx-auto max-w-7xl">
          <h2 className="text-3xl font-bold">Entenda por assunto</h2>

          <CategoryList categories={categories} error={categories === null} />
        </div>
      </section>

      <section id="orientacao" className="mx-auto max-w-7xl px-6 py-16">
        <div className="rounded-2xl bg-slate-100 p-8 md:p-12">
          <h2 className="text-3xl font-bold">Informação que ajuda a agir</h2>
          <p className="mt-4 max-w-2xl leading-relaxed text-[var(--muted)]">
            Além de explicar acontecimentos, o Hub Brasil vai reunir
            orientações práticas, prazos, direitos e links para canais oficiais.
          </p>
        </div>
      </section>

      <footer className="border-t border-[var(--border)] bg-white px-6 py-8">
        <div className="mx-auto flex max-w-7xl flex-col justify-between gap-3 text-sm text-[var(--muted)] md:flex-row">
          <p>© {new Date().getFullYear()} Hub Brasil</p>
          <p>Informação pública, clara e independente.</p>
        </div>
      </footer>
    </main>
  );
}
