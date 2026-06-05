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
  const [isHovered, setIsHovered] = useState(false);

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
        borderRadius: "var(--radius-lg)",
        padding: "1.5rem",
        border: "1px solid var(--color-border)",
        textDecoration: "none",
        color: "inherit",
        transition: "border-color var(--transition-fast), transform var(--transition-fast), box-shadow var(--transition-fast)",
        transform: isHovered ? "translateY(-2px)" : "translateY(0)",
        boxShadow: isHovered ? "var(--shadow-md)" : "none",
      }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "flex-start",
          marginBottom: "0.75rem",
          gap: "0.75rem",
        }}
      >
        <h3
          style={{
            fontSize: "1.1rem",
            fontWeight: 600,
            lineHeight: 1.3,
            margin: 0,
            overflow: "hidden",
            textOverflow: "ellipsis",
            display: "-webkit-box",
            WebkitLineClamp: 2,
            WebkitBoxOrient: "vertical",
          }}
        >
          {title || "Untitled Story"}
        </h3>
        {visibility === "sacred" && (
          <span
            style={{
              fontSize: "0.65rem",
              background: "var(--color-danger-soft)",
              color: "var(--color-danger)",
              padding: "0.2rem 0.5rem",
              borderRadius: 4,
              fontWeight: 700,
              letterSpacing: "0.05em",
              textTransform: "uppercase",
              flexShrink: 0,
            }}
          >
            Sacred
          </span>
        )}
      </div>

      {audioUrl && (
        <audio
          controls
          src={audioUrl}
          style={{ width: "100%", marginBottom: "0.75rem", borderRadius: "var(--radius)" }}
          preload="none"
          onClick={(e) => e.stopPropagation()}
        />
      )}

      <p
        style={{
          fontSize: "0.875rem",
          color: "var(--color-text-muted)",
          lineHeight: 1.6,
          margin: "0 0 0.75rem",
          display: "-webkit-box",
          WebkitLineClamp: 3,
          WebkitBoxOrient: "vertical",
          overflow: "hidden",
        }}
      >
        {transcript || "No transcript available yet. The AI is processing..."}
      </p>

      <div
        style={{
          display: "flex",
          gap: "0.75rem",
          flexWrap: "wrap",
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
              border: "1px solid var(--color-border)",
            }}
          >
            {language.toUpperCase()}
          </span>
        )}
        {speaker && <span>🎙 {speaker}</span>}
      </div>
    </Link>
  );
}
