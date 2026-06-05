"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";

export default function LandingPage() {
  const [scrollY, setScrollY] = useState(0);
  const heroRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const onScroll = () => setScrollY(window.scrollY);
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <div style={{ background: "var(--color-bg)", color: "var(--color-text)" }}>
      {/* Hero */}
      <section
        ref={heroRef}
        style={{
          minHeight: "100dvh",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          textAlign: "center",
          padding: "2rem",
          position: "relative",
          overflow: "hidden",
        }}
      >
        {/* Animated gradient background */}
        <div
          style={{
            position: "absolute",
            inset: 0,
            background: `radial-gradient(ellipse at 50% ${30 + scrollY * 0.02}%, rgba(212,168,83,0.06) 0%, transparent 60%)`,
            pointerEvents: "none",
          }}
        />

        <div style={{ position: "relative", zIndex: 1, maxWidth: 720 }}>
          <div
            style={{
              display: "inline-block",
              padding: "0.35rem 1rem",
              borderRadius: 999,
              border: "1px solid var(--color-border)",
              fontSize: "0.75rem",
              fontWeight: 500,
              color: "var(--color-accent)",
              marginBottom: "1.5rem",
              letterSpacing: "0.05em",
              textTransform: "uppercase",
            }}
          >
            🎙️ Open Source · AGPL-3.0 · Built in 2026
          </div>

          <h1
            style={{
              fontSize: "clamp(2.8rem, 7vw, 4.5rem)",
              fontWeight: 700,
              lineHeight: 1.05,
              marginBottom: "1.25rem",
              letterSpacing: "-0.02em",
            }}
          >
            FirstVoice
          </h1>

          <p
            style={{
              fontSize: "clamp(1.1rem, 2.5vw, 1.35rem)",
              color: "var(--color-text-muted)",
              lineHeight: 1.6,
              marginBottom: "2rem",
            }}
          >
            Community-Controlled Digital Heritage. AI speech technology, Web3
            provenance, and sacred governance — returning data sovereignty to
            Indigenous communities.
          </p>

          <div
            style={{
              display: "flex",
              gap: "1rem",
              flexWrap: "wrap",
              justifyContent: "center",
            }}
          >
            <Link
              href="https://github.com/ctmakc/firstvoice"
              target="_blank"
              rel="noopener"
              className="btn btn-primary"
              style={{
                padding: "0.875rem 1.75rem",
                borderRadius: "var(--radius)",
                background: "var(--color-accent)",
                color: "#0a0a0a",
                fontWeight: 600,
                fontSize: "0.95rem",
                display: "inline-flex",
                alignItems: "center",
                gap: "0.5rem",
              }}
            >
              ⭐ View on GitHub
            </Link>
            <Link
              href="/"
              style={{
                padding: "0.875rem 1.75rem",
                borderRadius: "var(--radius)",
                background: "var(--color-surface-raised)",
                color: "var(--color-text)",
                border: "1px solid var(--color-border)",
                fontWeight: 600,
                fontSize: "0.95rem",
                display: "inline-flex",
                alignItems: "center",
                gap: "0.5rem",
              }}
            >
              🚀 Try the Demo
            </Link>
          </div>
        </div>
      </section>

      {/* Stats */}
      <section style={{ padding: "5rem 1.5rem", borderTop: "1px solid var(--color-border)" }}>
        <div
          style={{
            maxWidth: 900,
            margin: "0 auto",
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
            gap: "2rem",
            textAlign: "center",
          }}
        >
          <StatCard value="40%" label="of ~7,000 languages critically endangered" />
          <StatCard value="1" label="language dies every 2 weeks" />
          <StatCard value="0" label="existing platforms enforce OCAP by design" />
        </div>
      </section>

      {/* Features */}
      <section
        style={{
          padding: "5rem 1.5rem",
          background: "var(--color-surface)",
          borderTop: "1px solid var(--color-border)",
        }}
      >
        <div style={{ maxWidth: 1000, margin: "0 auto" }}>
          <h2
            style={{
              fontSize: "clamp(1.5rem, 3vw, 2rem)",
              fontWeight: 700,
              textAlign: "center",
              marginBottom: "0.75rem",
            }}
          >
            The Solution
          </h2>
          <p
            style={{
              textAlign: "center",
              color: "var(--color-text-muted)",
              maxWidth: 560,
              margin: "0 auto 3rem",
              fontSize: "1.05rem",
              lineHeight: 1.6,
            }}
          >
            Three pillars that make FirstVoice unlike any other preservation platform.
          </p>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
              gap: "1.5rem",
            }}
          >
            <FeatureCard
              icon="🗣️"
              title="AI Speech Technology"
              description="Fine-tuned Whisper ASR for low-resource languages. Gemini-powered translation to English and French. Coqui TTS voice cloning so the language can 'speak' again."
            />
            <FeatureCard
              icon="⛓️"
              title="Web3 Provenance"
              description="Soulbound NFTs on Polygon prove origin without speculation. Tamper-proof, censorship-resistant, community-owned attribution. No crypto hype — just immutable proof."
            />
            <FeatureCard
              icon="🔒"
              title="Sacred Governance"
              description="OCAP-by-design: communities decide what is public, what is sacred, who accesses it. Technical enforcement — not just policy documents. AI training gated per-item."
            />
          </div>
        </div>
      </section>

      {/* Tech Stack */}
      <section style={{ padding: "5rem 1.5rem", borderTop: "1px solid var(--color-border)" }}>
        <div style={{ maxWidth: 800, margin: "0 auto", textAlign: "center" }}>
          <h2
            style={{
              fontSize: "clamp(1.5rem, 3vw, 2rem)",
              fontWeight: 700,
              marginBottom: "0.75rem",
            }}
          >
            Technology Stack
          </h2>
          <p
            style={{
              color: "var(--color-text-muted)",
              maxWidth: 500,
              margin: "0 auto 2.5rem",
              fontSize: "1.05rem",
            }}
          >
            Built for production, designed for community ownership.
          </p>

          <div
            style={{
              display: "flex",
              flexWrap: "wrap",
              gap: "0.75rem",
              justifyContent: "center",
            }}
          >
            {[
              "Next.js 16",
              "FastAPI",
              "PostgreSQL + PostGIS",
              "faster-whisper",
              "Gemini AI",
              "Coqui TTS",
              "Solidity + Hardhat",
              "Polygon",
              "MinIO",
              "Docker",
              "Redis",
              "Celery",
            ].map((tag) => (
              <span
                key={tag}
                style={{
                  background: "var(--color-surface-raised)",
                  border: "1px solid var(--color-border)",
                  padding: "0.4rem 0.9rem",
                  borderRadius: 6,
                  fontSize: "0.85rem",
                  fontFamily: "'SF Mono', Monaco, monospace",
                  color: "var(--color-text-muted)",
                }}
              >
                {tag}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* Grants */}
      <section
        style={{
          padding: "5rem 1.5rem",
          background: "var(--color-surface)",
          borderTop: "1px solid var(--color-border)",
        }}
      >
        <div style={{ maxWidth: 1000, margin: "0 auto" }}>
          <h2
            style={{
              fontSize: "clamp(1.5rem, 3vw, 2rem)",
              fontWeight: 700,
              textAlign: "center",
              marginBottom: "0.75rem",
            }}
          >
            Grant Fit
          </h2>
          <p
            style={{
              textAlign: "center",
              color: "var(--color-text-muted)",
              maxWidth: 560,
              margin: "0 auto 2.5rem",
              fontSize: "1.05rem",
            }}
          >
            Aligned with major Indigenous language, AI-for-good, and decentralized tech funding programs.
          </p>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
              gap: "1rem",
            }}
          >
            <GrantCard
              amount="$150K – $400K"
              name="SSHRC (Canada)"
              fit="Indigenous research + digital humanities"
            />
            <GrantCard
              amount="$100K – $500K"
              name="Canadian Heritage ILP"
              fit="Language revitalization technology"
            />
            <GrantCard
              amount="NZ$50K – $300K"
              name="Te Taura Whiri (NZ)"
              fit="Māori digital tools"
            />
            <GrantCard
              amount="$5K – $50K"
              name="Filecoin Dev Grants"
              fit="Decentralized storage layer"
            />
            <GrantCard
              amount="$10K – $100K"
              name="Gitcoin Grants"
              fit="Open-source public good"
            />
            <GrantCard
              amount="$10K – $100K"
              name="Protocol Labs"
              fit="Decentralized knowledge"
            />
          </div>
        </div>
      </section>

      {/* CTA */}
      <section
        style={{
          padding: "5rem 1.5rem",
          textAlign: "center",
          borderTop: "1px solid var(--color-border)",
        }}
      >
        <div style={{ maxWidth: 560, margin: "0 auto" }}>
          <h2
            style={{
              fontSize: "clamp(1.5rem, 3vw, 2rem)",
              fontWeight: 700,
              marginBottom: "1rem",
            }}
          >
            Join Us
          </h2>
          <p
            style={{
              color: "var(--color-text-muted)",
              fontSize: "1.05rem",
              lineHeight: 1.6,
              marginBottom: "2rem",
            }}
          >
            We are actively seeking Indigenous advisors, computational linguists,
            and grant partners.
          </p>
          <div
            style={{
              display: "flex",
              gap: "1rem",
              justifyContent: "center",
              flexWrap: "wrap",
            }}
          >
            <Link
              href="https://github.com/ctmakc/firstvoice"
              target="_blank"
              rel="noopener"
              style={{
                padding: "0.875rem 1.75rem",
                borderRadius: "var(--radius)",
                background: "var(--color-accent)",
                color: "#0a0a0a",
                fontWeight: 600,
                fontSize: "0.95rem",
              }}
            >
              ⭐ Star on GitHub
            </Link>
            <a
              href="mailto:hello@firstvoice.dev"
              style={{
                padding: "0.875rem 1.75rem",
                borderRadius: "var(--radius)",
                background: "var(--color-surface-raised)",
                color: "var(--color-text)",
                border: "1px solid var(--color-border)",
                fontWeight: 600,
                fontSize: "0.95rem",
              }}
            >
              📧 Contact for Partnerships
            </a>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer
        style={{
          padding: "2.5rem 1.5rem",
          textAlign: "center",
          color: "var(--color-text-dim)",
          fontSize: "0.8rem",
          borderTop: "1px solid var(--color-border)",
        }}
      >
        <p>
          Built with respect for the voices that came before us. · AGPL-3.0 ·{" "}
          <a href="https://github.com/ctmakc/firstvoice" style={{ color: "var(--color-text-dim)" }}>
            GitHub
          </a>
        </p>
        <p style={{ marginTop: "0.5rem" }}>
          Team: Maksym Stepanenko (Technologist) · Indigenous advisors (recruiting)
        </p>
      </footer>
    </div>
  );
}

function StatCard({ value, label }: { value: string; label: string }) {
  return (
    <div
      style={{
        padding: "2rem 1.5rem",
        borderRadius: "var(--radius-lg)",
        border: "1px solid var(--color-border)",
        background: "var(--color-bg)",
      }}
    >
      <div
        style={{
          fontSize: "2.5rem",
          fontWeight: 700,
          color: "var(--color-accent)",
          lineHeight: 1,
          marginBottom: "0.75rem",
        }}
      >
        {value}
      </div>
      <div style={{ color: "var(--color-text-muted)", fontSize: "0.875rem", lineHeight: 1.5 }}>{label}</div>
    </div>
  );
}

function FeatureCard({
  icon,
  title,
  description,
}: {
  icon: string;
  title: string;
  description: string;
}) {
  return (
    <div
      style={{
        padding: "2rem",
        borderRadius: "var(--radius-lg)",
        border: "1px solid var(--color-border)",
        background: "var(--color-bg)",
        transition: "border-color var(--transition-fast), transform var(--transition-fast)",
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.borderColor = "var(--color-accent)";
        e.currentTarget.style.transform = "translateY(-2px)";
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.borderColor = "var(--color-border)";
        e.currentTarget.style.transform = "translateY(0)";
      }}
    >
      <div style={{ fontSize: "2rem", marginBottom: "1rem" }}>{icon}</div>
      <h3 style={{ fontSize: "1.15rem", fontWeight: 600, marginBottom: "0.5rem" }}>{title}</h3>
      <p style={{ color: "var(--color-text-muted)", fontSize: "0.9rem", lineHeight: 1.6 }}>{description}</p>
    </div>
  );
}

function GrantCard({
  amount,
  name,
  fit,
}: {
  amount: string;
  name: string;
  fit: string;
}) {
  return (
    <div
      style={{
        padding: "1.5rem",
        borderRadius: "var(--radius-lg)",
        border: "1px solid var(--color-border)",
        background: "var(--color-bg)",
      }}
    >
      <div style={{ color: "var(--color-accent)", fontWeight: 600, fontSize: "0.9rem" }}>{amount}</div>
      <div style={{ fontWeight: 600, margin: "0.35rem 0", fontSize: "1rem" }}>{name}</div>
      <div style={{ color: "var(--color-text-muted)", fontSize: "0.8rem" }}>{fit}</div>
    </div>
  );
}
