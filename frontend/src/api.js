const API_BASE = "http://127.0.0.1:8000"; // backend

export async function getToken(userId) {
  const res = await fetch(`${API_BASE}/token/${userId}`);
  if (!res.ok) throw new Error("Failed to get token");
  return res.json();
}

export async function checkAuthorization(token, method, path) {
  const res = await fetch(`${API_BASE}/authorize`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ access_token: token, method, path }),
  });
  if (!res.ok) throw new Error("Authorization failed");
  return res.json();
}

export async function getUserPermissions(userId) {
  const res = await fetch(`${API_BASE}/users/${userId}/permissions`);
  if (!res.ok) throw new Error("Failed to fetch permissions");
  return res.json();
}

export async function addPermission(permission) {
  const res = await fetch(`${API_BASE}/permissions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(permission),
  });
  if (!res.ok) throw new Error("Failed to add permission");
  return res.json();
}
