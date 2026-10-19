import { test } from 'node:test';
import assert from 'node:assert/strict';
import { parseArgs, execute } from './vercel-failover.mjs';

test('writes require target, compare-and-swap and expected HTML marker', () => {
  assert.throws(() => parseArgs(['switch', '--domain', 'test.example.com', '--target', 'dpl_new']), /expected-current/);
  assert.throws(() => parseArgs(['switch', '--domain', 'test.example.com', '--target', 'dpl_new', '--expected-current', 'dpl_old']), /marker/);
  assert.throws(() => parseArgs(['switch', '--domain', 'test.example.com', '--target', 'dpl_new', '--expected-current', 'dpl_old', '--marker', 'maintenance', '--routes', '//evil']), /Routes must/);
});

test('concurrent alias change is rejected without mutation', async () => {
  const opts = parseArgs(['switch','--domain','test.example.com','--target','dpl_new','--expected-current','dpl_old','--marker','maintenance','--apply']);
  const calls = [];
  const fetcher = async (url, init) => {
    calls.push({ url, method: init.method || 'GET' });
    return { ok: true, json: async () => ({ deploymentId: 'dpl_concurrent', projectId: 'prj_1' }) };
  };
  await assert.rejects(execute(opts, { fetcher, token: 'test', teamId: 'team_1' }), /Concurrency stop/);
  assert.equal(calls.length, 1);
});

test('default operation is dry run and does not write', async () => {
  const opts = parseArgs(['switch','--domain','test.example.com','--target','dpl_new','--expected-current','dpl_old','--marker','maintenance']);
  const calls = [];
  const fetcher = async (url, init) => {
    calls.push(init.method || 'GET');
    return { ok: true, json: async () => url.includes('/v4/aliases/') ? { deploymentId: 'dpl_old', projectId: 'prj_1' } : { readyState: 'READY', projectId: 'prj_1' } };
  };
  const result = await execute(opts, { fetcher, token: 'test', teamId: 'team_1' });
  assert.equal(result.state, 'DRY_RUN');
  assert.deepEqual(calls, ['GET', 'GET']);
});

test('success verifies all frontend routes but does not claim API/PWA shutdown', async () => {
  const opts = parseArgs(['switch','--domain','test.example.com','--target','dpl_new','--expected-current','dpl_old','--marker','maintenance','--apply','--routes','/,/login,/app']);
  let switched = false;
  const fetcher = async (url) => {
    if (url.includes('/v4/aliases/')) return { ok: true, json: async () => ({ deploymentId: switched ? 'dpl_new' : 'dpl_old', projectId: 'prj_1' }) };
    if (url.includes('/v13/deployments/')) return { ok: true, json: async () => ({ readyState: 'READY', projectId: 'prj_1' }) };
    if (url.includes('/v2/deployments/')) { switched = true; return { ok: true, json: async () => ({}) }; }
    return { status: 200, headers: { get: () => 'text/html; charset=utf-8' }, text: async () => '<title>maintenance</title>' };
  };
  const result = await execute(opts, { fetcher, token: 'test', teamId: 'team_1' });
  assert.equal(result.state, 'FRONTEND_HTTP_VERIFIED');
  assert.equal(result.apiWritesBlocked, 'NOT_CHECKED');
  assert.equal(result.existingPwaSessions, 'NOT_CHECKED');
  assert.equal(result.checks.length, 3);
});
