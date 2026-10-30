"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { useAuth } from "@/features/auth/auth-context";

export function AccountNav() {
  const router = useRouter();
  const { user, loading, signOutUser } = useAuth();
  const [error, setError] = useState<string | null>(null);

  async function handleSignOut() {
    setError(null);
    try {
      await signOutUser();
      router.refresh();
    } catch {
      setError("Não foi possível sair agora.");
    }
  }

  if (loading) {
    return <span aria-label="Carregando conta" className="h-10 w-24 animate-pulse rounded bg-[#e7e9e2]" />;
  }

  if (!user) {
    return (
      <Link
        href="/login"
        className="rounded bg-[#17483f] px-4 py-2.5 text-sm font-semibold !text-white transition hover:bg-[#103a32]"
      >
        Entrar
      </Link>
    );
  }

  return (
    <div className="flex items-center gap-3">
      <span className="hidden max-w-36 truncate text-sm font-medium sm:block">
        {user.displayName || user.email}
      </span>
      <button
        className="rounded border border-[#17483f] px-4 py-2 text-sm font-semibold text-[#17483f] transition hover:bg-[#17483f] hover:text-white"
        onClick={handleSignOut}
        type="button"
      >
        Sair
      </button>
      {error && <span role="alert" className="sr-only">{error}</span>}
    </div>
  );
}