"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import Link from "next/link";
import StoryCard from "@/components/StoryCard";

export default function CommunityPage() {
  const params = useParams();
  const slug = params.slug as string;
  const [community, setCommunity] = useState<any>(null);
  const [recordings, setRecordings] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`/api/communities`)
      .then((r) => r.json())
      .then((data) => {
        const c = data.find((x: any) => x.slug === slug);
        setCommunity(c);
        if (c?.id) {
          fetch(`/api/recordings?community_id=${c.id}`)
            .then((r) => r.json())
            .then((recs) => {
              setRecordings(recs);
              setLoading(false);
            })
            .catch(() => setLoading(false));
        } else {
          setLoading(false);
        }
      })
      .catch(() => setLoading(false));
  }, [slug]);

  if (loading) return <p style={{ padding: "2rem", textAlign: "center" }}>Loading...</p>;
  if (!community) return <p style={{ padding: "2rem", textAlign: "center" }}>Community not found.</p>;

  const languageMap: Record<string, string> = {
    cre: "Cree · nehiyawewin",
    iku: "Inuktitut · ᐃᓄᒃᑎᑐᑦ",
    oji: "Ojibwe · Anishinaabemowin",
    mri: "Māori · te reo Māori",
    haw: "Hawaiian · ʻŌlelo Hawaiʻi",
  };

  const policyLabels: Record<string, string> = {
    restricted: "Restricted — Sacred data stays with elders",
    "community-review": "Community Review — Elders approve releases",
    open: "Open — Community shares with attribution",
  };

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
      <div>
        <Link
          href="/"
          style={{
            fontSize: "0.8rem",
            color: "var(--color-text-muted)",
            textDecoration: "none",
          }}
        >
          ← Back to Feed
        </Link>
      </div>

      <div
        style={{
          background: "var(--color-surface)",
          borderRadius: "var(--radius-lg)",
          padding: "1.5rem",
          border: "1px solid var(--color-border)",
        }}
      >
        <h1 style={{ fontSize: "1.5rem", fontWeight: 600, margin: "0 0 0.5rem" }}>
          {community.name}
        </h1>
        <p style={{ color: "var(--color-text-muted)", fontSize: "0.875rem", margin: "0 0 1rem" }}>
          {community.languages?.map((l: string) => languageMap[l] || l).join(" · ")}
        </p>
        <div
          style={{
            display: "inline-block",
            fontSize: "0.75rem",
            padding: "0.35rem 0.75rem",
            borderRadius: 999,
            background:
              community.data_policy === "restricted"
                ? "var(--color-danger-soft)"
                : community.data_policy === "community-review"
                ? "var(--color-accent-glow)"
                : "var(--color-success-soft)",
            color:
              community.data_policy === "restricted"
                ? "var(--color-danger)"
                : community.data_policy === "community-review"
                ? "var(--color-accent)"
                : "var(--color-success)",
            fontWeight: 500,
          }}
        >
          {policyLabels[community.data_policy] || community.data_policy}
        </div>
      </div>

      <div>
        <h2 style={{ fontSize: "1.1rem", fontWeight: 600, marginBottom: "1rem" }}>
          Recordings ({recordings.length})
        </h2>
        {recordings.length === 0 && (
          <p style={{ color: "var(--color-text-muted)", textAlign: "center", padding: "2rem" }}>
            No recordings yet.
          </p>
        )}
        <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
          {recordings.map((story) => (
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
      </div>
    </main>
  );
}
