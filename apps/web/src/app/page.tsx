"use client";

import { useEffect, useState } from "react";
import StoryCard from "@/components/StoryCard";

export default function Home() {
  const [stories, setStories] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/recordings")
      .then((r) => r.json())
      .then((data) => {
        setStories(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

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
        <h1 style={{ fontSize: "1.5rem", fontWeight: 600, margin: 0 }}>FirstVoice</h1>
        <p style={{ color: "var(--color-text-muted)", fontSize: "0.875rem", marginTop: "0.25rem" }}>
          Community-controlled digital heritage
        </p>
      </header>

      {loading && (
        <p style={{ textAlign: "center", color: "var(--color-text-muted)" }}>Loading stories...</p>
      )}

      {!loading && stories.length === 0 && (
        <div
          style={{
            textAlign: "center",
            padding: "2rem",
            background: "var(--color-surface)",
            borderRadius: "var(--radius)",
            border: "1px solid var(--color-border)",
          }}
        >
          <p style={{ color: "var(--color-text-muted)" }}>No stories yet.</p>
          <p style={{ color: "var(--color-text-muted)", fontSize: "0.875rem" }}>
            Tap the Record tab to add the first story.
          </p>
        </div>
      )}

      <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
        {stories.map((story) => (
          <StoryCard
            key={story.id}
            id={story.id}
            title={story.title}
            speaker={story.speaker_name}
            language={story.language}
            transcript={story.transcript}
            visibility={story.visibility}
          />
        ))}
      </div>
    </main>
  );
}
