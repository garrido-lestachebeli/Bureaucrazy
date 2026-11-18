async function request(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  const text = await response.text();
  const body = text ? JSON.parse(text) : null;
  if (!response.ok) {
    const detail = body && body.detail;
    const message = typeof detail === "string" ? detail : "The bureau could not complete that.";
    throw new Error(message);
  }
  return body;
}

export function startGame() {
  return request("/api/games", { method: "POST" });
}

export function getGame(gameId) {
  return request(`/api/games/${gameId}`);
}

export function getCase(gameId) {
  return request(`/api/games/${gameId}/case`);
}

export function decide(gameId, decision) {
  return request(`/api/games/${gameId}/decision`, {
    method: "POST",
    body: JSON.stringify({ decision }),
  });
}
