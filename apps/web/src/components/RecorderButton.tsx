"use client";

import { useState, useRef, useCallback } from "react";

export default function RecorderButton() {
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [duration, setDuration] = useState(0);
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

      recorder.start(1000); // collect every 1s
      mediaRecorderRef.current = recorder;
      setIsRecording(true);
      setDuration(0);

      timerRef.current = setInterval(() => {
        setDuration((d) => d + 1);
      }, 1000);
    } catch (err) {
      alert("Microphone access denied or unavailable.");
      console.error(err);
    }
  }, []);

  const stopRecording = useCallback(() => {
    if (mediaRecorderRef.current?.state === "recording") {
      mediaRecorderRef.current.stop();
    }
    if (timerRef.current) clearInterval(timerRef.current);
    setIsRecording(false);
  }, []);

  const uploadRecording = useCallback(async () => {
    if (!audioBlob) return;

    const formData = new FormData();
    formData.append("audio", audioBlob, "recording.webm");
    formData.append("community_id", "00000000-0000-0000-0000-000000000000"); // placeholder
    formData.append("language", "cre"); // placeholder: Cree
    formData.append("visibility", "sacred");
    formData.append("uploaded_by", "00000000-0000-0000-0000-000000000000"); // placeholder

    try {
      const res = await fetch("/api/recordings", {
        method: "POST",
        body: formData,
      });
      if (!res.ok) throw new Error(`Upload failed: ${res.status}`);
      const data = await res.json();
      alert(`Uploaded! Recording ID: ${data.id}`);
      setAudioBlob(null);
      setDuration(0);
    } catch (err) {
      alert("Upload failed. Will retry when online.");
      // TODO: queue in IndexedDB for background sync
      console.error(err);
    }
  }, [audioBlob]);

  const formatTime = (s: number) => {
    const m = Math.floor(s / 60);
    const sec = s % 60;
    return `${m}:${sec.toString().padStart(2, "0")}`;
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1.5rem", alignItems: "center" }}>
      <div
        style={{
          width: 120,
          height: 120,
          borderRadius: "50%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          background: isRecording
            ? "var(--color-danger)"
            : audioBlob
            ? "var(--color-success)"
            : "var(--color-accent)",
          transition: "background 0.2s ease",
          cursor: "pointer",
        }}
        onClick={isRecording ? stopRecording : audioBlob ? uploadRecording : startRecording}
        role="button"
        aria-label={isRecording ? "Stop recording" : audioBlob ? "Upload recording" : "Start recording"}
      >
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          {isRecording ? (
            <rect x="6" y="6" width="12" height="12" fill="currentColor" />
          ) : audioBlob ? (
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12" />
          ) : (
            <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" fill="currentColor" />
          )}
        </svg>
      </div>

      <div style={{ fontVariantNumeric: "tabular-nums", fontSize: "1.25rem", fontWeight: 500 }}>
        {isRecording ? `Recording… ${formatTime(duration)}` : audioBlob ? `Ready: ${formatTime(duration)}` : "Tap to record"}
      </div>

      {audioBlob && (
        <audio controls src={URL.createObjectURL(audioBlob)} style={{ width: "100%" }} />
      )}
    </div>
  );
}
