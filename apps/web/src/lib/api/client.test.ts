import { afterEach, describe, expect, it, vi } from "vitest";

const { getFirebaseAuthMock, getIdToken } = vi.hoisted(() => ({
  getIdToken: vi.fn().mockResolvedValue("firebase-test-token"),
  getFirebaseAuthMock: vi.fn(() => ({
    currentUser: { getIdToken }
  }))
}));

vi.mock("@/lib/firebase/client", () => ({
  getFirebaseAuth: getFirebaseAuthMock
}));

describe("apiFetch", () => {
  afterEach(() => {
    vi.unstubAllEnvs();
    vi.unstubAllGlobals();
    vi.resetModules();
    getIdToken.mockClear();
    getFirebaseAuthMock.mockReset();
    getFirebaseAuthMock.mockImplementation(() => ({
      currentUser: { getIdToken }
    }));
  });

  it("sends the Firebase ID Token as a Bearer token", async () => {
    vi.stubEnv("NEXT_PUBLIC_API_URL", "http://localhost:8000");
    const fetchMock = vi.fn().mockResolvedValue(new Response(null, { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);

    const { apiFetch } = await import("@/lib/api/client");
    await apiFetch("/api/v1/users/me");

    expect(fetchMock).toHaveBeenCalledOnce();
    expect(String(fetchMock.mock.calls[0][0])).toBe(
      "http://localhost:8000/api/v1/users/me"
    );
    expect(fetchMock.mock.calls[0][1].headers.get("Authorization")).toBe(
      "Bearer firebase-test-token"
    );
  });

  it("rejects requests when there is no authenticated user", async () => {
    vi.stubEnv("NEXT_PUBLIC_API_URL", "http://localhost:8000");
    getFirebaseAuthMock.mockReturnValueOnce({ currentUser: null } as never);
    const { apiFetch } = await import("@/lib/api/client");

    await expect(apiFetch("/api/v1/users/me")).rejects.toThrow(
      "Entre na sua conta para continuar."
    );
  });
});