const API = "http://127.0.0.1:8000/api";
let tokens = JSON.parse(localStorage.getItem("tokens") || "{}");

function setTokens(t){ tokens = t; localStorage.setItem("tokens", JSON.stringify(t)); }
async function api(path, {method="GET", body, json=true} = {}) {
  const headers = {"Content-Type":"application/json"};
  if (tokens?.access) headers["Authorization"] = `Bearer ${tokens.access}`;
  const res = await fetch(`${API}${path}`, {method, headers, body: body?JSON.stringify(body):undefined});
  if (res.status === 401 && tokens?.refresh) {
    // try refresh once
    const rr = await fetch(`${API}/auth/refresh/`, {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({refresh: tokens.refresh})});
    if (rr.ok) { const t = await rr.json(); setTokens({...tokens, access: t.access}); return api(path, {method, body, json}); }
  }
  if (!res.ok) throw new Error(await res.text());
  return json ? res.json() : res.text();
}
