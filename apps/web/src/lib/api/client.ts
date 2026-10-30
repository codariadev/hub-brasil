import { getFirebaseAuth } from "@/lib/firebase/client";

const apiBaseUrl = process.env.NEXT_PUBLIC_API_URL;

export async function apiFetch(
	path: string,
	init: RequestInit = {}
): Promise<Response> {
	if (!apiBaseUrl) {
		throw new Error("Configure a variável NEXT_PUBLIC_API_URL.");
	}

	const user = getFirebaseAuth().currentUser;
	if (!user) {
		throw new Error("Entre na sua conta para continuar.");
	}

	const headers = new Headers(init.headers);
	headers.set("Authorization", `Bearer ${await user.getIdToken()}`);

	return fetch(new URL(path, apiBaseUrl), {
		...init,
		headers
	});
}
