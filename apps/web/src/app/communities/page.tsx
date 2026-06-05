"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

export default function CommunitiesPage() {
  const [communities, setCommunities] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/communities")
      .then((r) => r.json())
      .then((data) => {
        setCommunities(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const languageMap: Record<string, string> = {
    cre: "Cree",
    iku: "Inuktitut",
    oji: "Ojibwe",
    mri: "Māori",
    haw: "Hawaiian",
    eng: "English",
  };

  const policyColors: Record<string, { bg: string; color: string }> = {
    restricted: { bg: "rgba(204,68,68,0.1)", color: "var(--color-danger)" },
    "community-review": { bg: "rgba(212,168,83,0.1)", color: "var(--color-accent)" },
    open: { bg: "rgba(51,170,51,0.1)", color: "var(--color-success)" },
  };

  return (
    <main
      style={{
        maxWidth: 640,
        margin: "0 auto",
        padding: "1.5rem",
        display: "flex",
        flexDirection: "column",
        gap: "1.5rem",
      }}
    >
      <header>
        <h1 style={{ fontSize: "1.5rem", fontWeight: 600, margin: 0 }}>Communities</h1>
        <p style={{ color: "var(--color-text-muted)", fontSize: "0.875rem", marginTop: "0.25rem" }}>
          Indigenous and endangered-language communities preserving their heritage
        </p>
      </header>

      {loading && (
        <p style={{ textAlign: "center", color: "var(--color-text-muted)" }}>Loading communities...</p>
      )}

      <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
        {communities.map((c) => {
          const policy = policyColors[c.data_policy] || policyColors.open;
          return (
            <Link
              key={c.id}
              href={`/community/${c.slug}`}
              style={{
                display: "block",
                background: "var(--color-surface)",
                borderRadius: "var(--radius-lg)",
                padding: "1.25rem",
                border: "1px solid var(--color-border)",
                textDecoration: "none",
                color: "inherit",
                transition: "border-color 0.15s ease, transform 0.15s ease",
              }}
              onMouseEnter={(e) => {
                (e.currentTarget as HTMLElement).style.borderColor = "var(--color-accent)";
                (e.currentTarget as HTMLElement).style.transform = "translateY(-2px)";
              }}
              onMouseLeave={(e) => {
                (e.currentTarget as HTMLElement).style.borderColor = "var(--color-border)";
                (e.currentTarget as HTMLElement).style.transform = "translateY(0)";
              }}
            >
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "flex-start",
                  marginBottom: "0.5rem",
                }}
              >
                <h3 style={{ fontSize: "1.1rem", fontWeight: 600, margin: 0 }}>{c.name}</h3>
                <span
                  style={{
                    fontSize: "0.65rem",
                    padding: "0.2rem 0.5rem",
                    borderRadius: 999,
                    background: policy.bg,
                    color: policy.color,
                    fontWeight: 600,
                    textTransform: "uppercase",
                    letterSpacing: "0.05em",
                    flexShrink: 0,
                  }}
                >
                  {c.data_policy}
                </span>
              </div>
              <p style={{ color: "var(--color-text-muted)", fontSize: "0.8rem", margin: "0 0 0.5rem" }}>
                {c.languages?.map((l: string) => languageMap[l] || l).join(" · ")}
              </p>
              <div style={{ fontSize: "0.75rem", color: "var(--color-text-dim)" }}>
                → View recordings
              </div>
            </Link>
          );
        })}
      </div>
    </main>
  );
}
