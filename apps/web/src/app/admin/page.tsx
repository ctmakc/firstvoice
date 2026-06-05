"use client";

import { useEffect, useState } from "react";

export default function AdminPage() {
  const [recordings, setRecordings] = useState<any[]>([]);
  const [auditLog, setAuditLog] = useState<any[]>([]);
  const [communities, setCommunities] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<"pending" | "all" | "audit">("pending");
  const [message, setMessage] = useState("");

  useEffect(() => {
    loadData();
  }, []);

  const loadData = () => {
    Promise.all([
      fetch("/api/recordings", { credentials: "include" }).then((r) => r.json()),
      fetch("/api/admin/audit-log", { credentials: "include" }).then((r) => (r.ok ? r.json() : [])),
      fetch("/api/communities").then((r) => r.json()),
    ]).then(([recs, audits, comms]) => {
      setRecordings(recs);
      setAuditLog(audits);
      setCommunities(comms);
      setLoading(false);
    });
  };

  const handleApprove = async (id: string) => {
    try {
      const res = await fetch(`/api/recordings/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ visibility: "public" }),
      });
      if (!res.ok) throw new Error("Failed");
      setMessage("✅ Recording approved for public release");
      loadData();
      setTimeout(() => setMessage(""), 3000);
    } catch {
      setMessage("❌ Approval failed — insufficient privileges");
      setTimeout(() => setMessage(""), 3000);
    }
  };

  const handleMint = async (id: string) => {
    try {
      const res = await fetch("/api/provenance/mint", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ recording_id: id }),
      });
      if (!res.ok) throw new Error("Failed");
      const data = await res.json();
      setMessage(`⛓️ Provenance minted! Tx: ${data.tx_hash?.slice(0, 20)}...`);
      loadData();
      setTimeout(() => setMessage(""), 5000);
    } catch {
      setMessage("❌ Minting failed — check contract deployment");
      setTimeout(() => setMessage(""), 3000);
    }
  };

  if (loading) return <p style={{ padding: "2rem", textAlign: "center" }}>Loading...</p>;

  const pending = recordings.filter((r) => r.transcription_status === "pending");
  const sacred = recordings.filter((r) => r.visibility === "sacred");
  const publicRecs = recordings.filter((r) => r.visibility === "public");

  const communityMap: Record<string, string> = {};
  communities.forEach((c) => (communityMap[c.id] = c.name));

  const langMap: Record<string, string> = {
    cre: "Cree", iku: "Inuktitut", oji: "Ojibwe", mri: "Māori", haw: "Hawaiian", eng: "English",
  };

  return (
    <main
      style={{
        maxWidth: 960,
        margin: "0 auto",
        padding: "1.5rem",
        display: "flex",
        flexDirection: "column",
        gap: "1.5rem",
      }}
    >
      <h1 style={{ fontSize: "1.5rem", fontWeight: 600 }}>Admin Panel</h1>

      {message && (
        <div
          style={{
            padding: "0.75rem 1rem",
            background: "var(--color-accent-glow)",
            border: "1px solid var(--color-accent)",
            borderRadius: "var(--radius)",
            color: "var(--color-accent)",
            fontSize: "0.875rem",
            fontWeight: 500,
          }}
        >
          {message}
        </div>
      )}

      {/* Stats */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(120px, 1fr))",
          gap: "0.75rem",
        }}
      >
        {[
          { label: "Total", value: recordings.length },
          { label: "Pending", value: pending.length },
          { label: "Sacred", value: sacred.length },
          { label: "Public", value: publicRecs.length },
        ].map((s) => (
          <div
            key={s.label}
            style={{
              background: "var(--color-surface)",
              borderRadius: "var(--radius)",
              padding: "1rem",
              border: "1px solid var(--color-border)",
              textAlign: "center",
            }}
          >
            <div style={{ fontSize: "1.5rem", fontWeight: 700, color: "var(--color-accent)" }}>{s.value}</div>
            <div style={{ fontSize: "0.75rem", color: "var(--color-text-muted)", marginTop: "0.25rem" }}>
              {s.label}
            </div>
          </div>
        ))}
      </div>

      {/* Tabs */}
      <div style={{ display: "flex", gap: "0.5rem", borderBottom: "1px solid var(--color-border)" }}>
        {(["pending", "all", "audit"] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            style={{
              padding: "0.6rem 1rem",
              background: "none",
              border: "none",
              borderBottom: activeTab === tab ? "2px solid var(--color-accent)" : "2px solid transparent",
              color: activeTab === tab ? "var(--color-text)" : "var(--color-text-muted)",
              fontWeight: activeTab === tab ? 600 : 400,
              fontSize: "0.875rem",
              cursor: "pointer",
              fontFamily: "inherit",
            }}
          >
            {tab === "pending" && `Pending (${pending.length})`}
            {tab === "all" && "All Recordings"}
            {tab === "audit" && "Audit Log"}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      {activeTab === "pending" && (
        <section style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
          {pending.length === 0 && (
            <p style={{ color: "var(--color-text-muted)", textAlign: "center", padding: "2rem" }}>
              No pending recordings. 🎉
            </p>
          )}
          {pending.map((r) => (
            <AdminRecordingRow
              key={r.id}
              r={r}
              communityMap={communityMap}
              langMap={langMap}
              onApprove={handleApprove}
              onMint={handleMint}
            />
          ))}
        </section>
      )}

      {activeTab === "all" && (
        <section style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
          {recordings.map((r) => (
            <AdminRecordingRow
              key={r.id}
              r={r}
              communityMap={communityMap}
              langMap={langMap}
              onApprove={handleApprove}
              onMint={handleMint}
            />
          ))}
        </section>
      )}

      {activeTab === "audit" && (
        <section style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
          {auditLog.length === 0 && (
            <p style={{ color: "var(--color-text-muted)", textAlign: "center", padding: "2rem" }}>
              No audit entries yet.
            </p>
          )}
          {auditLog.slice(0, 50).map((log) => (
            <div
              key={log.id}
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                padding: "0.6rem 0.875rem",
                background: "var(--color-surface)",
                borderRadius: "var(--radius)",
                border: "1px solid var(--color-border)",
                fontSize: "0.8rem",
              }}
            >
              <span style={{ fontWeight: 500 }}>{log.action}</span>
              <span style={{ color: "var(--color-text-muted)" }}>
                {new Date(log.created_at).toLocaleString()}
              </span>
            </div>
          ))}
        </section>
      )}
    </main>
  );
}

function AdminRecordingRow({
  r,
  communityMap,
  langMap,
  onApprove,
  onMint,
}: {
  r: any;
  communityMap: Record<string, string>;
  langMap: Record<string, string>;
  onApprove: (id: string) => void;
  onMint: (id: string) => void;
}) {
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "flex-start",
        padding: "1rem",
        background: "var(--color-surface)",
        borderRadius: "var(--radius)",
        border: "1px solid var(--color-border)",
        gap: "1rem",
      }}
    >
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ fontWeight: 600, marginBottom: "0.25rem" }}>{r.title || "Untitled"}</div>
        <div
          style={{
            fontSize: "0.75rem",
            color: "var(--color-text-muted)",
            display: "flex",
            gap: "0.5rem",
            flexWrap: "wrap",
          }}
        >
          <span>{langMap[r.language] || r.language}</span>
          <span>·</span>
          <span>{communityMap[r.community_id] || "Unknown"}</span>
          <span>·</span>
          <span
            style={{
              color:
                r.visibility === "sacred"
                  ? "var(--color-danger)"
                  : r.visibility === "public"
                  ? "var(--color-success)"
                  : "var(--color-accent)",
              fontWeight: 500,
            }}
          >
            {r.visibility?.toUpperCase()}
          </span>
        </div>
        {r.transcript && (
          <p
            style={{
              fontSize: "0.8rem",
              color: "var(--color-text-dim)",
              marginTop: "0.5rem",
              lineHeight: 1.5,
              overflow: "hidden",
              textOverflow: "ellipsis",
              whiteSpace: "nowrap",
            }}
          >
            {r.transcript}
          </p>
        )}
      </div>

      <div style={{ display: "flex", gap: "0.5rem", flexShrink: 0 }}>
        {r.visibility === "sacred" && (
          <button
            onClick={() => onApprove(r.id)}
            style={{
              padding: "0.4rem 0.75rem",
              borderRadius: "var(--radius)",
              border: "none",
              background: "var(--color-success)",
              color: "#fff",
              fontSize: "0.75rem",
              fontWeight: 600,
              cursor: "pointer",
            }}
          >
            Approve
          </button>
        )}
        {!r.provenance_tx_hash && (
          <button
            onClick={() => onMint(r.id)}
            style={{
              padding: "0.4rem 0.75rem",
              borderRadius: "var(--radius)",
              border: "1px solid var(--color-accent)",
              background: "var(--color-accent-glow)",
              color: "var(--color-accent)",
              fontSize: "0.75rem",
              fontWeight: 600,
              cursor: "pointer",
            }}
          >
            Mint NFT
          </button>
        )}
        {r.provenance_tx_hash && (
          <span
            style={{
              fontSize: "0.7rem",
              color: "var(--color-text-dim)",
              padding: "0.4rem 0.75rem",
            }}
          >
            ⛓️ Minted
          </span>
        )}
      </div>
    </div>
  );
}
