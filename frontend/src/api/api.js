const API_BASE = "";

export async function getDocumentByToken(token) {
  const res = await fetch(
    `${API_BASE}/api/public/documents/${encodeURIComponent(token)}/`,
  );
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || "Document not found");
  }
  return res.json();
}

export function getDocumentFileUrl(token) {
  return `${API_BASE}/api/public/documents/${encodeURIComponent(token)}/file/`;
}

export async function submitDecision(token, decision) {
  const res = await fetch(
    `${API_BASE}/api/public/documents/${encodeURIComponent(token)}/decision/`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ decision }),
    },
  );
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(data.error || `Request failed: ${res.status}`);
  }
  return data;
}
