"use client";

import { useState } from "react";

export default function LoginPage() {
  const [elderKey, setElderKey] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const res = await fetch("/api/auth/me", {
        headers: { "X-Elder-Key": elderKey },
        credentials: "include",
      });
      if (!res.ok) throw new Error("Invalid Elder Key");
      const user = await res.json();
      localStorage.setItem("demo_user", JSON.stringify(user));
      localStorage.setItem("elder_key", elderKey);
      window.location.href = "/";
    } catch (err: any) {
      setError(err.message || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        minHeight: "100dvh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "2rem",
        gap: "1.5rem",
      }}
    >
      <h1 style={{ fontSize: "1.5rem", fontWeight: 600 }}>Sign In</h1>

      <form
        onSubmit={handleSubmit}
        style={{
          background: "var(--color-surface)",
          borderRadius: "var(--radius)",
          padding: "1.5rem",
          width: "100%",
          maxWidth: 400,
          border: "1px solid var(--color-border)",
          display: "flex",
          flexDirection: "column",
          gap: "1rem",
        }}
      >
        <p style={{ fontSize: "0.875rem", color: "var(--color-text-muted)", margin: 0 }}>
          OAuth coming soon. For demo access, use an Elder Key.
        </p>

        <input
          type="password"
          value={elderKey}
          onChange={(e) => setElderKey(e.target.value)}
          placeholder="Enter Elder Key"
          required
          style={{
            padding: "0.6rem 0.75rem",
            borderRadius: "var(--radius)",
            border: "1px solid var(--color-border)",
            background: "var(--color-surface-raised)",
            color: "inherit",
            fontSize: "1rem",
          }}
        />

        {error && (
          <p style={{ color: "var(--color-danger)", fontSize: "0.875rem", margin: 0 }}>{error}</p>
        )}

        <button
          type="submit"
          disabled={loading}
          style={{
            padding: "0.75rem",
            borderRadius: "var(--radius)",
            border: "none",
            background: "var(--color-accent)",
            color: "#0a0a0a",
            fontWeight: 600,
            cursor: loading ? "not-allowed" : "pointer",
            opacity: loading ? 0.7 : 1,
            fontSize: "1rem",
          }}
        >
          {loading ? "Signing in..." : "Continue"}
        </button>
      </form>
    </div>
  );
}
