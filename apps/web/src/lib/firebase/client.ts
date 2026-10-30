import { getApp, getApps, initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
	apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
	authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
	projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
	appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID
};

export function getFirebaseConfigurationError() {
	const missingConfig = Object.entries(firebaseConfig)
		.filter(([, value]) => !value)
		.map(([key]) => key);

	if (missingConfig.length > 0) {
		return `Configure as variáveis públicas do Firebase: ${missingConfig.join(", ")}.`;
	}
	return null;
}

export function getFirebaseAuth() {
	const configurationError = getFirebaseConfigurationError();
	if (configurationError) {
		throw new Error(configurationError);
	}

	const app = getApps().length > 0 ? getApp() : initializeApp(firebaseConfig);
	return getAuth(app);
}
