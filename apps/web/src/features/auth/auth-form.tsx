"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState, type FormEvent } from "react";
import { useAuth } from "@/features/auth/auth-context";

type AuthFormProps = {
  mode: "login" | "signup";
};

const authErrorMessages: Record<string, string> = {
  "auth/email-already-in-use": "Este e-mail já possui uma conta.",
  "auth/invalid-credential": "E-mail ou senha incorretos.",
  "auth/invalid-email": "Informe um e-mail válido.",
  "auth/weak-password": "Use uma senha mais forte, com pelo menos 6 caracteres.",
  "auth/network-request-failed": "Falha de conexão. Verifique sua internet e tente novamente."
};

function getErrorMessage(error: unknown) {
  if (error instanceof Error && "code" in error) {
    const code = String(error.code);
    return authErrorMessages[code] ?? "Não foi possível concluir. Tente novamente.";
  }
  return error instanceof Error
    ? error.message
    : "Não foi possível concluir. Tente novamente.";
}

export function AuthForm({ mode }: AuthFormProps) {
  const router = useRouter();
  const { signIn, signUp, configurationError } = useAuth();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const isSignup = mode === "signup";

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setSubmitting(true);

    try {
      if (isSignup) {
        await signUp(name.trim(), email.trim(), password);
      } else {
        await signIn(email.trim(), password);
      }
      router.replace("/");
    } catch (caughtError) {
      setError(getErrorMessage(caughtError));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="grid min-h-screen bg-[#f5f4ed] lg:grid-cols-[1.05fr_0.95fr]">
      <section className="relative hidden overflow-hidden bg-[#17483f] px-12 py-10 text-white lg:flex lg:flex-col lg:justify-between xl:px-20">
        <Link href="/" className="w-fit text-xl font-bold tracking-wide">
          Hub Brasil
        </Link>
        <div className="relative z-10 max-w-xl pb-16">
          <p className="mb-5 text-sm font-semibold uppercase text-[#f2bd62]">
            Informação pública, clara e independente
          </p>
          <h1 className="font-serif text-5xl leading-tight xl:text-6xl">
            O Brasil acontece. O povo precisa entender.
          </h1>
          <p className="mt-6 max-w-lg text-lg leading-8 text-white/75">
            Entre para acompanhar informações que ajudam a entender o país e o
            que muda no seu cotidiano.
          </p>
        </div>
        <p className="text-sm text-white/60">Informação para todos.</p>
        <div aria-hidden="true" className="absolute -right-28 top-1/4 h-96 w-96 rounded-full border border-white/10" />
        <div aria-hidden="true" className="absolute -right-4 top-[38%] h-64 w-64 rounded-full border border-[#f2bd62]/30" />
      </section>

      <section className="flex min-h-screen flex-col px-6 py-8 sm:px-12 lg:px-16 xl:px-24">
        <Link href="/" className="w-fit text-lg font-bold text-[#17483f] lg:hidden">
          Hub Brasil
        </Link>
        <div className="m-auto w-full max-w-md py-12">
          <p className="text-sm font-semibold uppercase text-[#b07724]">
            Sua conta Hub Brasil
          </p>
          <h2 className="mt-3 font-serif text-4xl text-[#182723]">
            {isSignup ? "Crie sua conta" : "Que bom ter você de volta"}
          </h2>
          <p className="mt-3 leading-7 text-[#596762]">
            {isSignup
              ? "Acompanhe informações e personalize sua experiência."
              : "Entre para acessar sua conta e suas preferências."}
          </p>

          <form onSubmit={handleSubmit} className="mt-9 space-y-5">
            {isSignup && (
              <label className="block text-sm font-semibold text-[#253832]">
                Nome
                <input
                  autoComplete="name"
                  className="mt-2 block w-full rounded border border-[#cbd3cc] bg-white px-4 py-3 font-normal outline-none transition focus:border-[#17483f] focus:ring-2 focus:ring-[#17483f]/15"
                  onChange={(event) => setName(event.target.value)}
                  required
                  value={name}
                />
              </label>
            )}
            <label className="block text-sm font-semibold text-[#253832]">
              E-mail
              <input
                autoComplete="email"
                className="mt-2 block w-full rounded border border-[#cbd3cc] bg-white px-4 py-3 font-normal outline-none transition focus:border-[#17483f] focus:ring-2 focus:ring-[#17483f]/15"
                onChange={(event) => setEmail(event.target.value)}
                required
                type="email"
                value={email}
              />
            </label>
            <label className="block text-sm font-semibold text-[#253832]">
              Senha
              <input
                autoComplete={isSignup ? "new-password" : "current-password"}
                className="mt-2 block w-full rounded border border-[#cbd3cc] bg-white px-4 py-3 font-normal outline-none transition focus:border-[#17483f] focus:ring-2 focus:ring-[#17483f]/15"
                minLength={6}
                onChange={(event) => setPassword(event.target.value)}
                required
                type="password"
                value={password}
              />
            </label>

            {(error || configurationError) && (
              <p role="alert" className="rounded border border-[#d99b88] bg-[#fff3ef] px-4 py-3 text-sm text-[#8e3828]">
                {error ?? configurationError}
              </p>
            )}

            <button
              className="w-full rounded bg-[#17483f] px-5 py-3.5 font-semibold text-white transition hover:bg-[#103a32] disabled:cursor-not-allowed disabled:opacity-60"
              disabled={submitting || Boolean(configurationError)}
              type="submit"
            >
              {submitting
                ? "Aguarde..."
                : isSignup
                  ? "Criar conta"
                  : "Entrar"}
            </button>
          </form>

          <p className="mt-7 text-center text-sm text-[#596762]">
            {isSignup ? "Já tem uma conta?" : "Ainda não tem uma conta?"}{" "}
            <Link
              className="font-semibold text-[#17483f] underline decoration-[#b07724] underline-offset-4"
              href={isSignup ? "/login" : "/cadastro"}
            >
              {isSignup ? "Entrar" : "Cadastre-se"}
            </Link>
          </p>
          <Link href="/" className="mt-8 block text-center text-sm text-[#596762] hover:text-[#17483f]">
            Voltar para a página inicial
          </Link>
        </div>
      </section>
    </main>
  );
}