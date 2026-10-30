"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { useAuth } from "@/features/auth/auth-context";

const firebaseAuthErrorMessages: Record<string, string> = {
  "auth/operation-not-allowed": "Habilite o provedor de e-mail/senha no Firebase Authentication.",
  "auth/invalid-id-token": "A sessão expirou. Saia da conta e entre novamente.",
  "auth/user-token-expired": "A sessão expirou. Saia da conta e entre novamente.",
  "auth/too-many-requests": "Muitas tentativas. Aguarde antes de solicitar outro e-mail.",
  "auth/email-already-verified": "Este e-mail já está verificado. Atualize o estado da conta.",
  "auth/network-request-failed": "Falha de conexão com o Firebase. Tente novamente."
};

function getFirebaseAuthErrorMessage(error: unknown): string {
  const code =
    error instanceof Error && "code" in error ? String(error.code) : null;
  if (code && firebaseAuthErrorMessages[code]) {
    return firebaseAuthErrorMessages[code];
  }
  return code
    ? `Falha do Firebase (${code}).`
    : "Não foi possível concluir a operação com o Firebase.";
}

export function AccountNav() {
  const router = useRouter();
  const { user, loading, sendVerificationEmail, refreshUser, signOutUser } = useAuth();
  const [error, setError] = useState<string | null>(null);
  const [tokenMessage, setTokenMessage] = useState<string | null>(null);

  const isEditorialAccount =
    process.env.NODE_ENV === "development" &&
    user?.email?.trim().toLowerCase() === "alves2.eduardo@gmail.com";
  const canCopyApiToken = isEditorialAccount && user?.emailVerified === true;

  async function handleSignOut() {
    setError(null);
    try {
      await signOutUser();
      router.refresh();
    } catch {
      setError("Não foi possível sair agora.");
    }
  }

  async function handleCopyApiToken() {
    if (!user || !canCopyApiToken) return;

    setTokenMessage(null);
    try {
      const token = await user.getIdToken(true);
      await navigator.clipboard.writeText(token);
      setTokenMessage("ID Token copiado. Trate-o como uma credencial temporária.");
    } catch {
      setTokenMessage("Não foi possível copiar o ID Token.");
    }
  }

  async function handleSendVerification() {
    setTokenMessage(null);
    try {
      await sendVerificationEmail();
      setTokenMessage("E-mail de verificação enviado.");
    } catch (caughtError) {
      setTokenMessage(getFirebaseAuthErrorMessage(caughtError));
    }
  }

  async function handleRefreshVerification() {
    setTokenMessage(null);
    try {
      const emailVerified = await refreshUser();
      setTokenMessage(
        emailVerified
          ? "E-mail verificado. O botão Token API está disponível."
          : "E-mail ainda não confirmado. Confira sua caixa de entrada."
      );
    } catch (caughtError) {
      setTokenMessage(getFirebaseAuthErrorMessage(caughtError));
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
      {isEditorialAccount && !user.emailVerified && (
        <>
          <button
            className="rounded border border-[#b07724] px-3 py-2 text-sm font-semibold text-[#714b10] transition hover:bg-[#fff0c9]"
            onClick={handleSendVerification}
            type="button"
          >
            Verificar e-mail
          </button>
          <button
            className="rounded border border-[#b07724] px-3 py-2 text-sm font-semibold text-[#714b10] transition hover:bg-[#fff0c9]"
            onClick={handleRefreshVerification}
            type="button"
          >
            Já confirmei
          </button>
        </>
      )}
      {canCopyApiToken && (
        <button
          className="rounded border border-[#b07724] px-3 py-2 text-sm font-semibold text-[#714b10] transition hover:bg-[#fff0c9]"
          onClick={handleCopyApiToken}
          title="Copiar token de desenvolvimento para testar a API"
          type="button"
        >
          Token API
        </button>
      )}
      <button
        className="rounded border border-[#17483f] px-4 py-2 text-sm font-semibold text-[#17483f] transition hover:bg-[#17483f] hover:text-white"
        onClick={handleSignOut}
        type="button"
      >
        Sair
      </button>
      {tokenMessage && (
        <span
          aria-live="polite"
          className="max-w-48 text-xs text-[#8e3828]"
          role="status"
        >
          {tokenMessage}
        </span>
      )}
      {error && <span role="alert" className="sr-only">{error}</span>}
    </div>
  );
}