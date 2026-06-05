"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

export default function StoryDetailPage() {
  const params = useParams();
  const id = params.id as string;
  const [story, setStory] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`/api/recordings/${id}`)
      .then((r) => r.json())
      .then((data) => {
        setStory(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [id]);

  if (loading) return <p style={{ padding: "2rem", textAlign: "center" }}>Loading...</p>;
  if (!story) return <p style={{ padding: "2rem", textAlign: "center" }}>Story not found.</p>;

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
      <h1 style={{ fontSize: "1.5rem", fontWeight: 600, margin: 0 }}>
        {story.title || "Untitled Story"}
      </h1>

      <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap" }}>
        <span
          style={{
            background: "var(--color-surface-raised)",
            padding: "0.2rem 0.5rem",
            borderRadius: 4,
            fontSize: "0.75rem",
          }}
        >
          {story.language?.toUpperCase()}
        </span>
        {story.speaker_name && (
          <span style={{ fontSize: "0.75rem", color: "var(--color-text-muted)" }}>
            Speaker: {story.speaker_name}
          </span>
        )}
        <span
          style={{
            fontSize: "0.75rem",
            background:
              story.visibility === "sacred" ? "var(--color-danger)" : "var(--color-success)",
            color: "#fff",
            padding: "0.15rem 0.4rem",
            borderRadius: 4,
          }}
        >
          {story.visibility?.toUpperCase()}
        </span>
      </div>

      {story.transcript && (
        <div
          style={{
            background: "var(--color-surface)",
            borderRadius: "var(--radius)",
            padding: "1.25rem",
            border: "1px solid var(--color-border)",
            lineHeight: 1.7,
            fontSize: "1rem",
          }}
        >
          {story.transcript}
        </div>
      )}

      {story.translations && (
        <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
          {Object.entries(story.translations).map(([lang, text]: [string, any]) => (
            <div
              key={lang}
              style={{
                background: "var(--color-surface)",
                borderRadius: "var(--radius)",
                padding: "1rem",
                border: "1px solid var(--color-border)",
              }}
            >
              <div
                style={{
                  fontSize: "0.75rem",
                  color: "var(--color-accent)",
                  fontWeight: 600,
                  textTransform: "uppercase",
                  marginBottom: "0.5rem",
                }}
              >
                {lang}
              </div>
              <div style={{ fontSize: "0.9rem", lineHeight: 1.6 }}>{text}</div>
            </div>
          ))}
        </div>
      )}

      {story.entities?.length > 0 && (
        <div style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem" }}>
          {story.entities.map((ent: any, i: number) => (
            <span
              key={i}
              style={{
                background: "var(--color-surface-raised)",
                padding: "0.3rem 0.6rem",
                borderRadius: 999,
                fontSize: "0.75rem",
                border: "1px solid var(--color-border)",
              }}
            >
              {ent.type}: {ent.text}
            </span>
          ))}
        </div>
      )}
    </main>
  );
}
