let csrf = "";
export const setCsrf = (token) => {
  csrf = token;
};

function errorMessage(data) {
  if (!data) return "خطای ناشناخته";
  if (typeof data === "string") return data;
  if (data.detail) return data.detail;
  return Object.values(data).flat().join(" ");
}

export async function api(path, { method = "GET", body } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (method !== "GET") headers["X-CSRFToken"] = csrf;

  const res = await fetch(`/api${path}`, {
    method,
    headers,
    credentials: "same-origin",
    body: body ? JSON.stringify(body) : undefined,
  });

  let data = null;
  try {
    data = await res.json();
  } catch {
    /* بدنه خالی */
  }
  if (!res.ok) {
    const expired = res.status === 401 || res.status === 403;
    const err = new Error(expired ? "نشست شما منقضی شده است؛ دوباره وارد شوید." : errorMessage(data));
    err.status = res.status;
    throw err;
  }
  return data;
}
