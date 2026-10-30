const apiBaseUrl =
  process.env.API_URL ??
  process.env.NEXT_PUBLIC_API_URL ??
  "http://127.0.0.1:8000";

export async function fetchPublicApi<T>(path: string): Promise<T> {
  const response = await fetch(new URL(`/api/v1/${path}`, apiBaseUrl), {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(`A API respondeu com status ${response.status}.`);
  }

  return response.json() as Promise<T>;
}