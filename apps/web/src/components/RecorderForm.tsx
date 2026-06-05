"use client";

import { useState, useRef, useCallback } from "react";

export default function RecorderForm() {
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [duration, setDuration] = useState(0);
  const [uploading, setUploading] = useState(false);
  const [title, setTitle] = useState("");
  const [language, setLanguage] = useState("cre");
  const [occasion, setOccasion] = useState("");
  const [visibility, setVisibility] = useState("sacred");
  const [speakerName, setSpeakerName] = useState("");

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  const startRecording = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mimeType = MediaRecorder.isTypeSupported("audio/webm;codecs=opus")
        ? "audio/webm;codecs=opus"
        : "audio/webm";
      const recorder = new MediaRecorder(stream, { mimeType });

      chunksRef.current = [];
      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data);
      };
      recorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: mimeType });
        setAudioBlob(blob);
        stream.getTracks().forEach((t) => t.stop());
      };

      recorder.start(1000);
      mediaRecorderRef.current = recorder;
      setIsRecording(true);
      setDuration(0);
      timerRef.current = setInterval(() => setDuration((d) => d + 1), 1000);
    } catch {
      alert("Microphone access denied.");
    }
  }, []);

  const stopRecording = useCallback(() => {
    if (mediaRecorderRef.current?.state === "recording") {
      mediaRecorderRef.current.stop();
    }
    if (timerRef.current) clearInterval(timerRef.current);
    setIsRecording(false);
  }, []);

  const upload = useCallback(async () => {
    if (!audioBlob) return;
    setUploading(true);

    const formData = new FormData();
    formData.append("audio", audioBlob, "recording.webm");
    formData.append("community_id", "00000000-0000-0000-0000-000000000000");
    formData.append("language", language);
    formData.append("title", title);
    formData.append("occasion", occasion);
    formData.append("visibility", visibility);
    formData.append("speaker_name", speakerName);

    try {
      const res = await fetch("/api/recordings", {
        method: "POST",
        body: formData,
        credentials: "include",
      });
      if (!res.ok) throw new Error(`Upload failed: ${res.status}`);
      const data = await res.json();
      alert(`Uploaded! Recording ID: ${data.id}`);
      setAudioBlob(null);
      setDuration(0);
      setTitle("");
      setOccasion("");
      setSpeakerName("");
    } catch (err) {
      alert("Upload failed. Will retry when online.");
      console.error(err);
    } finally {
      setUploading(false);
    }
  }, [audioBlob, language, title, occasion, visibility, speakerName]);

  const fmt = (s: number) => {
    const m = Math.floor(s / 60);
    const sec = s % 60;
    return `${m}:${sec.toString().padStart(2, "0")}`;
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1.25rem" }}>
      {/* Record button */}
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "1rem" }}>
        <button
          onClick={isRecording ? stopRecording : audioBlob ? upload : startRecording}
          disabled={uploading}
          style={{
            width: 120,
            height: 120,
            borderRadius: "50%",
            border: "none",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            background: isRecording
              ? "var(--color-danger)"
              : audioBlob
              ? "var(--color-success)"
              : "var(--color-accent)",
            color: "#fff",
            fontSize: "2rem",
            cursor: uploading ? "not-allowed" : "pointer",
            opacity: uploading ? 0.6 : 1,
            transition: "background 0.2s",
          }}
        >
          {isRecording ? "⏹" : audioBlob ? "⬆" : "🎙"}
        </button>
        <div style={{ fontVariantNumeric: "tabular-nums", fontSize: "1.1rem" }}>
          {isRecording
            ? `Recording… ${fmt(duration)}`
            : audioBlob
            ? `Ready: ${fmt(duration)}`
            : "Tap to record"}
        </div>
      </div>

      {audioBlob && (
        <>
          <audio
            controls
            src={URL.createObjectURL(audioBlob)}
            style={{ width: "100%", borderRadius: "var(--radius)" }}
          />

          <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
            <label style={{ display: "flex", flexDirection: "column", gap: "0.25rem", fontSize: "0.875rem" }}>
              Title
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Story of the Caribou"
                style={{
                  padding: "0.6rem 0.75rem",
                  borderRadius: "var(--radius)",
                  border: "1px solid var(--color-border)",
                  background: "var(--color-surface-raised)",
                  color: "inherit",
                  fontSize: "1rem",
                }}
              />
            </label>

            <label style={{ display: "flex", flexDirection: "column", gap: "0.25rem", fontSize: "0.875rem" }}>
              Language
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                style={{
                  padding: "0.6rem 0.75rem",
                  borderRadius: "var(--radius)",
                  border: "1px solid var(--color-border)",
                  background: "var(--color-surface-raised)",
                  color: "inherit",
                  fontSize: "1rem",
                }}
              >
                <option value="cre">Cree</option>
                <option value="iku">Inuktitut</option>
                <option value="oji">Ojibwe</option>
                <option value="den">Dene</option>
                <option value="mri">Māori</option>
              </select>
            </label>

            <label style={{ display: "flex", flexDirection: "column", gap: "0.25rem", fontSize: "0.875rem" }}>
              Occasion
              <input
                type="text"
                value={occasion}
                onChange={(e) => setOccasion(e.target.value)}
                placeholder="Winter Gathering"
                style={{
                  padding: "0.6rem 0.75rem",
                  borderRadius: "var(--radius)",
                  border: "1px solid var(--color-border)",
                  background: "var(--color-surface-raised)",
                  color: "inherit",
                  fontSize: "1rem",
                }}
              />
            </label>

            <label style={{ display: "flex", flexDirection: "column", gap: "0.25rem", fontSize: "0.875rem" }}>
              Speaker Name
              <input
                type="text"
                value={speakerName}
                onChange={(e) => setSpeakerName(e.target.value)}
                placeholder="Elder Mary"
                style={{
                  padding: "0.6rem 0.75rem",
                  borderRadius: "var(--radius)",
                  border: "1px solid var(--color-border)",
                  background: "var(--color-surface-raised)",
                  color: "inherit",
                  fontSize: "1rem",
                }}
              />
            </label>

            <div
              style={{
                display: "flex",
                gap: "0.5rem",
                alignItems: "center",
                padding: "0.75rem",
                borderRadius: "var(--radius)",
                border: "1px solid var(--color-border)",
                background: "var(--color-surface-raised)",
              }}
            >
              <input
                type="checkbox"
                id="public-toggle"
                checked={visibility === "public"}
                onChange={(e) => setVisibility(e.target.checked ? "public" : "sacred")}
              />
              <label htmlFor="public-toggle" style={{ fontSize: "0.875rem", cursor: "pointer" }}>
                Make Public (unchecked = Sacred)
              </label>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
