export default function OfflinePage() {
  return (
    <main
      style={{
        minHeight: "100dvh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "2rem",
        textAlign: "center",
        gap: "1rem",
      }}
    >
      <h1 style={{ fontSize: "1.5rem", fontWeight: 600 }}>You are offline</h1>
      <p style={{ color: "var(--color-text-muted)", maxWidth: 400 }}>
        FirstVoice works offline. Your recordings are saved locally and will sync
        when you reconnect.
      </p>
      <button
        onClick={() => window.location.reload()}
        style={{
          padding: "0.75rem 1.5rem",
          borderRadius: "var(--radius)",
          border: "none",
          background: "var(--color-accent)",
          color: "#0a0a0a",
          fontWeight: 600,
          cursor: "pointer",
        }}
      >
        Retry Connection
      </button>
    </main>
  );
}
