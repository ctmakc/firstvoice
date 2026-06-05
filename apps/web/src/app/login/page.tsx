"use client";

import { useState } from "react";

export default function LoginPage() {
  const [elderKey, setElderKey] = useState("");

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

      <div
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
          style={{
            padding: "0.6rem 0.75rem",
            borderRadius: "var(--radius)",
            border: "1px solid var(--color-border)",
            background: "var(--color-surface-raised)",
            color: "inherit",
            fontSize: "1rem",
          }}
        />

        <button
          style={{
            padding: "0.75rem",
            borderRadius: "var(--radius)",
            border: "none",
            background: "var(--color-accent)",
            color: "#0a0a0a",
            fontWeight: 600,
            cursor: "pointer",
            fontSize: "1rem",
          }}
        >
          Continue
        </button>
      </div>
    </div>
  );
}
