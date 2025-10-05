// frontend/static/app-axios.js
const API_BASE = "http://127.0.0.1:8000";
const api = axios.create({
  baseURL: `${API_BASE}/api`,
  headers: { "Content-Type": "application/json" }
});

function getTokens() {
  try { return JSON.parse(localStorage.getItem("tokens") || "{}"); } catch { return {}; }
}
function setTokens(tokens) { localStorage.setItem("tokens", JSON.stringify(tokens || {})); }
function clearTokens() { localStorage.removeItem("tokens"); }

api.interceptors.request.use((config) => {
  const { access } = getTokens();
  if (access) config.headers.Authorization = `Bearer ${access}`;
  return config;
});

let refreshing = null;
api.interceptors.response.use(
  (res) => res,
  async (err) => {
    const original = err.config;
    if (err.response && err.response.status === 401 && !original._retry) {
      const { refresh } = getTokens();
      if (!refresh) throw err;
      if (!refreshing) {
        refreshing = axios.post(`${API_BASE}/api/auth/refresh/`, { refresh })
          .then(r => {
            const access = r.data.access;
            const t = getTokens();
            setTokens({ ...t, access });
            return access;
          })
          .finally(() => refreshing = null);
      }
      const newAccess = await refreshing;
      original.headers.Authorization = `Bearer ${newAccess}`;
      original._retry = true;
      return api(original);
    }
    throw err;
  }
);

// Small helpers used by the auth page
async function registerUser(username, email, password, extraFields = []) {
  return api.post("/auth/register/", {
    username, email, password,
    extra_fields: extraFields  // <— send to backend
  });
}
async function loginUser(username, password) {
  const r = await axios.post(`${API_BASE}/api/auth/login/`, { username, password });
  setTokens(r.data); // {access, refresh}
  return r.data;
}
window.apiClient = {
  registerUser,
  loginUser,
  getTokens,
  setTokens,
  clearTokens
};


