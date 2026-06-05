"use client";

import { useState, useRef, useCallback, useEffect } from "react";

const DB_NAME = "firstvoice-offline";
const STORE_NAME = "recordings-queue";

function openDB(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, 1);
    req.onerror = () => reject(req.error);
    req.onsuccess = () => resolve(req.result);
    req.onupgradeneeded = () => {
      req.result.createObjectStore(STORE_NAME, { keyPath: "id", autoIncrement: true });
    };
  });
}

async function queueOffline(data: { blob: Blob; form: Record<string, string> }) {
  const db = await openDB();
  const tx = db.transaction(STORE_NAME, "readwrite");
  const store = tx.objectStore(STORE_NAME);
  await new Promise((resolve, reject) => {
    const req = store.add({ ...data, createdAt: Date.now() });
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
  db.close();
}

async function getQueueCount(): Promise<number> {
  try {
    const db = await openDB();
    const tx = db.transaction(STORE_NAME, "readonly");
    const store = tx.objectStore(STORE_NAME);
    const count = await new Promise<number>((resolve, reject) => {
      const req = store.count();
      req.onsuccess = () => resolve(req.result);
      req.onerror = () => reject(req.error);
    });
    db.close();
    return count;
  } catch {
    return 0;
  }
}

export default function RecorderForm() {
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [duration, setDuration] = useState(0);
  const [uploading, setUploading] = useState(false);
  const [offlineCount, setOfflineCount] = useState(0);
  const [title, setTitle] = useState("");
  const [language, setLanguage] = useState("cre");
  const [occasion, setOccasion] = useState("");
  const [visibility, setVisibility] = useState("sacred");
  const [speakerName, setSpeakerName] = useState("");
  const [communityId, setCommunityId] = useState("c8078d97-9ff1-46bb-945d-5baaae20b10c");

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  useEffect(() => {
    getQueueCount().then(setOfflineCount);
    fetch("/api/communities")
      .then((r) => r.json())
      .then((data) => {
        if (data?.[0]?.id) setCommunityId(data[0].id);
      })
      .catch(() => {});
  }, []);

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
    formData.append("community_id", communityId);
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
      setOfflineCount(0);
    } catch (err) {
      // Save to offline queue
      await queueOffline({
        blob: audioBlob,
        form: {
          community_id: communityId,
          language,
          title,
          occasion,
          visibility,
          speaker_name: speakerName,
        },
      });
      const count = await getQueueCount();
      setOfflineCount(count);
      alert(`Upload failed. Saved to offline queue (${count} pending).`);
    } finally {
      setUploading(false);
    }
  }, [audioBlob, language, title, occasion, visibility, speakerName, communityId]);

  const fmt = (s: number) => {
    const m = Math.floor(s / 60);
    const sec = s % 60;
    return `${m}:${sec.toString().padStart(2, "0")}`;
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1.25rem" }}>
      {offlineCount > 0 && (
        <div
          style={{
            background: "var(--color-accent)",
            color: "#0a0a0a",
            padding: "0.5rem 0.75rem",
            borderRadius: "var(--radius)",
            fontSize: "0.875rem",
            fontWeight: 500,
          }}
        >
          🔄 {offlineCount} recording(s) queued for sync when online
        </div>
      )}

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
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Title — e.g. Story of the Caribou"
              style={inputStyle}
            />

            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              style={inputStyle}
            >
              <option value="cre">Cree</option>
              <option value="iku">Inuktitut</option>
              <option value="oji">Ojibwe</option>
              <option value="den">Dene</option>
              <option value="mri">Māori</option>
            </select>

            <input
              type="text"
              value={occasion}
              onChange={(e) => setOccasion(e.target.value)}
              placeholder="Occasion — e.g. Winter Gathering"
              style={inputStyle}
            />

            <input
              type="text"
              value={speakerName}
              onChange={(e) => setSpeakerName(e.target.value)}
              placeholder="Speaker Name — e.g. Elder Mary"
              style={inputStyle}
            />

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

const inputStyle: React.CSSProperties = {
  padding: "0.6rem 0.75rem",
  borderRadius: "var(--radius)",
  border: "1px solid var(--color-border)",
  background: "var(--color-surface-raised)",
  color: "inherit",
  fontSize: "1rem",
  fontFamily: "inherit",
};
