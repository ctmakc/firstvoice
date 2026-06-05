import RecorderButton from "@/components/RecorderButton";

export default function Home() {
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
        gap: "2rem",
      }}
    >
      <header style={{ maxWidth: 640 }}>
        <h1
          style={{
            fontSize: "clamp(2rem, 6vw, 3.5rem)",
            fontWeight: 700,
            lineHeight: 1.1,
            marginBottom: "1rem",
          }}
        >
          FirstVoice
        </h1>
        <p
          style={{
            fontSize: "1.125rem",
            color: "var(--color-text-muted)",
            maxWidth: 520,
            margin: "0 auto",
          }}
        >
          Community-controlled digital heritage. Record, preserve, and revive
          the voices of your ancestors.
        </p>
      </header>

      <section
        style={{
          background: "var(--color-surface)",
          borderRadius: "var(--radius)",
          padding: "2rem",
          width: "100%",
          maxWidth: 480,
          border: "1px solid var(--color-border)",
        }}
      >
        <RecorderButton />
      </section>

      <footer style={{ color: "var(--color-text-muted)", fontSize: "0.875rem" }}>
        <p>OCAP-by-design · Open Source · No extraction</p>
      </footer>
    </main>
  );
}
