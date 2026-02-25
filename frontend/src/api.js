import { useQuery } from "@tanstack/react-query";

const API_BASE = "/api";
const POLL_INTERVAL = 10_000; // 10 seconds

function getAuthHeaders() {
  const credentials = localStorage.getItem("dashboard_credentials");
  if (!credentials) return {};
  return { Authorization: `Basic ${credentials}` };
}

export function setCredentials(username, password) {
  const encoded = btoa(`${username}:${password}`);
  localStorage.setItem("dashboard_credentials", encoded);
}

export function clearCredentials() {
  localStorage.removeItem("dashboard_credentials");
}

export function hasCredentials() {
  return !!localStorage.getItem("dashboard_credentials");
}

async function apiFetch(path) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: getAuthHeaders(),
  });
  if (response.status === 401) {
    clearCredentials();
    window.location.reload();
    throw new Error("Unauthorized");
  }
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  return response.json();
}

export function useBots() {
  return useQuery({
    queryKey: ["bots"],
    queryFn: () => apiFetch("/bots"),
    refetchInterval: POLL_INTERVAL,
  });
}

export function useBotDetail(botId) {
  return useQuery({
    queryKey: ["bot", botId],
    queryFn: () => apiFetch(`/bots/${botId}`),
    refetchInterval: POLL_INTERVAL,
    enabled: !!botId,
  });
}
