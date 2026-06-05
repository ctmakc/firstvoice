"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

interface StoryCardProps {
  id: string;
  title?: string;
  speaker?: string;
  language?: string;
  transcript?: string;
  visibility?: string;
}

export default function StoryCard({
  id,
  title,
  speaker,
  language,
  transcript,
  visibility,
}: StoryCardProps) {
  const [audioUrl, setAudioUrl] = useState<string | null>(null);

  useEffect(() => {
    fetch(`/api/recordings/${id}/audio-url`, { credentials: "include" })
      .then((r) => (r.ok ? r.json() : null))
      .then((data) => data && setAudioUrl(data.audio_url))
      .catch(() => {});
  }, [id]);

  return (
    <Link
      href={`/story/${id}`}
      style={{
        display: "block",
        background: "var(--color-surface)",
        borderRadius: "var(--radius)",
        padding: "1.25rem",
        border: "1px solid var(--color-border)",
        textDecoration: "none",
        color: "inherit",
        transition: "border-color 0.15s",
      }}
      onMouseEnter={(e) =>
        (e.currentTarget.style.borderColor = "var(--color-accent)")
      }
      onMouseLeave={(e) =>
        (e.currentTarget.style.borderColor = "var(--color-border)")
      }
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "flex-start",
          marginBottom: "0.75rem",
        }}
      >
        <h3
          style={{
            fontSize: "1.1rem",
            fontWeight: 600,
            lineHeight: 1.3,
            margin: 0,
          }}
        >
          {title || "Untitled Story"}
        </h3>
        {visibility === "sacred" && (
          <span
            style={{
              fontSize: "0.7rem",
              background: "var(--color-danger)",
              color: "#fff",
              padding: "0.15rem 0.4rem",
              borderRadius: 4,
              fontWeight: 600,
            }}
          >
            SACRED
          </span>
        )}
      </div>

      {audioUrl && (
        <audio
          controls
          src={audioUrl}
          style={{ width: "100%", marginBottom: "0.75rem" }}
          preload="none"
        />
      )}

      <p
        style={{
          fontSize: "0.875rem",
          color: "var(--color-text-muted)",
          lineHeight: 1.5,
          margin: "0 0 0.75rem",
          display: "-webkit-box",
          WebkitLineClamp: 3,
          WebkitBoxOrient: "vertical",
          overflow: "hidden",
        }}
      >
        {transcript || "No transcript available."}
      </p>

      <div
        style={{
          display: "flex",
          gap: "0.75rem",
          fontSize: "0.75rem",
          color: "var(--color-text-muted)",
        }}
      >
        {language && (
          <span
            style={{
              background: "var(--color-surface-raised)",
              padding: "0.2rem 0.5rem",
              borderRadius: 4,
            }}
          >
            {language.toUpperCase()}
          </span>
        )}
        {speaker && <span>Speaker: {speaker}</span>}
      </div>
    </Link>
  );
}
