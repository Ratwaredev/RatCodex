# Node safe JSON fetch

Use this package for small Node.js clients that need JSON responses, bounded request time, caller cancellation, and useful HTTP failures without adding a dependency.

## Install

Copy `templates/safe-json-fetch.mjs`. It targets Node.js 18+ where `fetch`, `AbortController`, and `DOMException` are available globally.

## Behavior

`fetchJson(url, options)` sends `Accept: application/json`, enforces a configurable timeout, composes caller cancellation, rejects non-2xx responses with `HttpError`, limits captured error bodies to 4096 characters, requires a JSON content type, and parses the body.

It is intentionally small: retries, authentication policy, caching, and schema validation belong at a higher layer.

## Validation

`tests/safe-json-fetch.test.mjs` uses a real local HTTP server to verify JSON parsing, HTTP errors, content-type rejection, and timeout behavior. RatCodex CI reruns it before this package may remain `copyReady`.
