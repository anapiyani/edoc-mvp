const API_BASE = "";

export async function getHealth() {
  const res = await fetch(`${API_BASE}/api/health/`);
  if (!res.ok) throw new Error("Health check failed");
  return res.json();
}
