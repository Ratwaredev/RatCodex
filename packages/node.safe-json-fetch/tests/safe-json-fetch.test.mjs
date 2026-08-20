import assert from "node:assert/strict";
import http from "node:http";
import test from "node:test";
import { HttpError, fetchJson } from "../templates/safe-json-fetch.mjs";

async function withServer(handler, run) {
  const server = http.createServer(handler);
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  const { port } = server.address();
  try {
    await run(`http://127.0.0.1:${port}`);
  } finally {
    await new Promise((resolve, reject) => server.close((error) => error ? reject(error) : resolve()));
  }
}

test("returns parsed JSON and sends Accept header", async () => {
  await withServer((req, res) => {
    assert.equal(req.headers.accept, "application/json");
    res.writeHead(200, { "content-type": "application/json; charset=utf-8" });
    res.end(JSON.stringify({ ok: true }));
  }, async (baseUrl) => {
    assert.deepEqual(await fetchJson(baseUrl), { ok: true });
  });
});

test("throws HttpError with bounded response body", async () => {
  await withServer((_req, res) => {
    res.writeHead(503, { "content-type": "text/plain" });
    res.end("down");
  }, async (baseUrl) => {
    await assert.rejects(() => fetchJson(baseUrl), (error) => {
      assert.ok(error instanceof HttpError);
      assert.equal(error.status, 503);
      assert.equal(error.body, "down");
      return true;
    });
  });
});

test("rejects non-JSON success responses", async () => {
  await withServer((_req, res) => {
    res.writeHead(200, { "content-type": "text/plain" });
    res.end("ok");
  }, async (baseUrl) => {
    await assert.rejects(() => fetchJson(baseUrl), /Expected application\/json/);
  });
});

test("times out slow responses", async () => {
  await withServer((_req, res) => {
    setTimeout(() => {
      if (!res.destroyed) {
        res.writeHead(200, { "content-type": "application/json" });
        res.end("{}");
      }
    }, 100);
  }, async (baseUrl) => {
    await assert.rejects(() => fetchJson(baseUrl, { timeoutMs: 20 }), (error) => error?.name === "TimeoutError");
  });
});
