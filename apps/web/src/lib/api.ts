export async function fetchApi(path: string, options?: RequestInit) {
  // Relative path — rewrites to backend via Next.js
  const res = await fetch(`/api${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
    credentials: "include",
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`API ${res.status}: ${err}`);
  }
  return res.json();
}

export async function getHealth() {
  return fetchApi("/health");
}

export async function listCommunities() {
  return fetchApi("/communities");
}

export async function listRecordings(params?: { community_id?: string; language?: string }) {
  const qs = new URLSearchParams(params || {}).toString();
  return fetchApi(`/recordings?${qs}`);
}

export async function getRecording(id: string) {
  return fetchApi(`/recordings/${id}`);
}

export async function getAudioUrl(id: string) {
  return fetchApi(`/recordings/${id}/audio-url`);
}
