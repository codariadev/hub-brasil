"use client";

import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode
} from "react";
import {
  createUserWithEmailAndPassword,
  onAuthStateChanged,
  signInWithEmailAndPassword,
  signOut,
  updateProfile,
  type User
} from "firebase/auth";
import {
  getFirebaseAuth,
  getFirebaseConfigurationError
} from "@/lib/firebase/client";

type AuthContextValue = {
  user: User | null;
  loading: boolean;
  configurationError: string | null;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (name: string, email: string, password: string) => Promise<void>;
  signOutUser: () => Promise<void>;
};

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [configurationError] = useState(getFirebaseConfigurationError);
  const [loading, setLoading] = useState(!configurationError);

  useEffect(() => {
    if (configurationError) return;
    return onAuthStateChanged(getFirebaseAuth(), (nextUser) => {
      setUser(nextUser);
      setLoading(false);
    });
  }, [configurationError]);

  async function signIn(email: string, password: string) {
    await signInWithEmailAndPassword(getFirebaseAuth(), email, password);
  }

  async function signUp(name: string, email: string, password: string) {
    const credential = await createUserWithEmailAndPassword(
      getFirebaseAuth(),
      email,
      password
    );
    await updateProfile(credential.user, { displayName: name });
  }

  async function signOutUser() {
    await signOut(getFirebaseAuth());
  }

  return (
    <AuthContext.Provider
      value={{ user, loading, configurationError, signIn, signUp, signOutUser }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth deve ser usado dentro de AuthProvider.");
  }
  return context;
}