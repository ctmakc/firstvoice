"use client";

import { useEffect, useState } from "react";

export default function AdminPage() {
  const [recordings, setRecordings] = useState<any[]>([]);
  const [auditLog, setAuditLog] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch("/api/recordings").then((r) => r.json()),
      fetch("/api/admin/audit-log").then((r) => (r.ok ? r.json() : [])),
    ]).then(([recs, audits]) => {
      setRecordings(recs);
      setAuditLog(audits);
      setLoading(false);
    });
  }, []);

  if (loading) return <p style={{ padding: "2rem", textAlign: "center" }}>Loading...</p>;

  const pending = recordings.filter((r) => r.transcription_status === "pending");

  return (
    <main
      style={{
        maxWidth: 960,
        margin: "0 auto",
        padding: "1.5rem",
        display: "flex",
        flexDirection: "column",
        gap: "2rem",
      }}
    >
      <h1 style={{ fontSize: "1.5rem", fontWeight: 600 }}>Admin Panel</h1>

      {/* Pending Recordings */}
      <section
        style={{
          background: "var(--color-surface)",
          borderRadius: "var(--radius)",
          padding: "1.25rem",
          border: "1px solid var(--color-border)",
        }}
      >
        <h2 style={{ fontSize: "1.1rem", marginBottom: "1rem" }}>
          Pending Recordings ({pending.length})
        </h2>
        {pending.length === 0 && (
          <p style={{ color: "var(--color-text-muted)", fontSize: "0.875rem" }}>No pending recordings.</p>
        )}
        <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
          {pending.map((r) => (
            <div
              key={r.id}
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                padding: "0.75rem",
                background: "var(--color-surface-raised)",
                borderRadius: "var(--radius)",
              }}
            >
              <div>
                <div style={{ fontWeight: 500 }}>{r.title || "Untitled"}</div>
                <div style={{ fontSize: "0.75rem", color: "var(--color-text-muted)" }}>
                  {r.language?.toUpperCase()} — {r.transcription_status}
                </div>
              </div>
              <span
                style={{
                  fontSize: "0.7rem",
                  background: "var(--color-accent)",
                  color: "#0a0a0a",
                  padding: "0.2rem 0.5rem",
                  borderRadius: 4,
                  fontWeight: 600,
                }}
              >
                PENDING
              </span>
            </div>
          ))}
        </div>
      </section>

      {/* Audit Log */}
      <section
        style={{
          background: "var(--color-surface)",
          borderRadius: "var(--radius)",
          padding: "1.25rem",
          border: "1px solid var(--color-border)",
        }}
      >
        <h2 style={{ fontSize: "1.1rem", marginBottom: "1rem" }}>Audit Log</h2>
        {auditLog.length === 0 && (
          <p style={{ color: "var(--color-text-muted)", fontSize: "0.875rem" }}>No audit entries.</p>
        )}
        <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
          {auditLog.slice(0, 20).map((log) => (
            <div
              key={log.id}
              style={{
                display: "flex",
                justifyContent: "space-between",
                padding: "0.5rem 0.75rem",
                background: "var(--color-surface-raised)",
                borderRadius: "var(--radius)",
                fontSize: "0.8rem",
              }}
            >
              <span style={{ fontWeight: 500 }}>{log.action}</span>
              <span style={{ color: "var(--color-text-muted)" }}>
                {new Date(log.created_at).toLocaleString()}
              </span>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
