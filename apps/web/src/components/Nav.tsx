"use client";

import { usePathname } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/hooks/useAuth";

const links = [
  { href: "/", label: "Feed", icon: "🏠" },
  { href: "/record", label: "Record", icon: "🎙️" },
  { href: "/admin", label: "Admin", icon: "⚙️" },
];

export default function Nav() {
  const path = usePathname();
  const { user, logout } = useAuth();

  return (
    <nav
      style={{
        position: "fixed",
        bottom: 0,
        left: 0,
        right: 0,
        display: "flex",
        justifyContent: "space-around",
        alignItems: "center",
        padding: "0.75rem 0",
        background: "var(--color-surface)",
        borderTop: "1px solid var(--color-border)",
        zIndex: 100,
      }}
    >
      {links.map((l) => (
        <Link
          key={l.href}
          href={l.href}
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: "0.25rem",
            fontSize: "0.75rem",
            color:
              path === l.href ? "var(--color-accent)" : "var(--color-text-muted)",
            textDecoration: "none",
            transition: "color 0.15s",
          }}
        >
          <span style={{ fontSize: "1.25rem" }}>{l.icon}</span>
          {l.label}
        </Link>
      ))}

      {user ? (
        <button
          onClick={logout}
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: "0.25rem",
            fontSize: "0.75rem",
            color: "var(--color-text-muted)",
            background: "none",
            border: "none",
            cursor: "pointer",
          }}
        >
          <span style={{ fontSize: "1.25rem" }}>🚪</span>
          Exit
        </button>
      ) : (
        <Link
          href="/login"
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: "0.25rem",
            fontSize: "0.75rem",
            color: path === "/login" ? "var(--color-accent)" : "var(--color-text-muted)",
            textDecoration: "none",
          }}
        >
          <span style={{ fontSize: "1.25rem" }}>🔑</span>
          Sign In
        </Link>
      )}
    </nav>
  );
}
