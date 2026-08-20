export class HttpError extends Error {
  constructor(status, statusText, body) {
    super(`HTTP ${status}${statusText ? ` ${statusText}` : ""}`);
    this.name = "HttpError";
    this.status = status;
    this.statusText = statusText;
    this.body = body;
  }
}

export async function fetchJson(url, options = {}) {
  const {
    timeoutMs = 10_000,
    headers,
    signal,
    ...fetchOptions
  } = options;

  if (!Number.isFinite(timeoutMs) || timeoutMs <= 0) {
    throw new TypeError("timeoutMs must be a positive finite number");
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(new DOMException("Request timed out", "TimeoutError")), timeoutMs);
  const abortFromCaller = () => controller.abort(signal.reason);
  if (signal) {
    if (signal.aborted) abortFromCaller();
    else signal.addEventListener("abort", abortFromCaller, { once: true });
  }

  try {
    const response = await fetch(url, {
      ...fetchOptions,
      headers: { Accept: "application/json", ...headers },
      signal: controller.signal,
    });

    const text = await response.text();
    if (!response.ok) {
      throw new HttpError(response.status, response.statusText, text.slice(0, 4096));
    }

    const contentType = response.headers.get("content-type") ?? "";
    if (!contentType.toLowerCase().includes("application/json")) {
      throw new TypeError(`Expected application/json, got ${contentType || "unknown content type"}`);
    }

    return text ? JSON.parse(text) : null;
  } finally {
    clearTimeout(timeout);
    signal?.removeEventListener("abort", abortFromCaller);
  }
}
