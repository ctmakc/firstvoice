const API_BASE = process.env.API_URL || "http://localhost:8000/api/v1";

export async function fetchApi(path: string, options?: RequestInit) {
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
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
