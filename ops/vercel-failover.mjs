#!/usr/bin/env node
// Safe Vercel alias switch: read-only unless --apply with matching --expected-current.
import { pathToFileURL } from 'node:url';

export function parseArgs(argv) {
  const [action, ...rest] = argv;
  if (!['check', 'switch'].includes(action)) throw new Error('Use: check | switch');
  const options = { action, apply: false };
  for (let i = 0; i < rest.length; i++) {
    const arg = rest[i];
    if (arg === '--apply') { options.apply = true; continue; }
    if (!arg.startsWith('--') || !rest[i + 1] || rest[i + 1].startsWith('--')) throw new Error('Invalid argument: ' + arg);
    options[arg.slice(2)] = rest[++i];
  }
  if (!options.domain || !/^[a-z0-9][a-z0-9.-]*\.[a-z]{2,}$/i.test(options.domain)) throw new Error('--domain must be hostname only');
  if (action === 'switch' && (!options.target || !options['expected-current'] || !options.marker)) throw new Error('switch requires --target, --expected-current and --marker');
  const paths = (options.routes || '/,/login,/app').split(',').map(x => x.trim());
  if (paths.some(x => !x.startsWith('/') || x.startsWith('//'))) throw new Error('Routes must be absolute paths');
  return options;
}

export async function execute(options, { fetcher = fetch, token = process.env.VERCEL_TOKEN, teamId = process.env.VERCEL_TEAM_ID } = {}) {
  if (!token || !teamId) throw new Error('Set VERCEL_TOKEN and VERCEL_TEAM_ID');
  const query = '?teamId=' + encodeURIComponent(teamId);
  const headers = { authorization: 'Bearer ' + token, accept: 'application/json' };
  const api = async (path, init = {}) => {
    const response = await fetcher('https://api.vercel.com' + path + query, { ...init, headers: { ...headers, ...(init.headers || {}) }, signal: AbortSignal.timeout(10000) });
    const payload = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error('Vercel API HTTP ' + response.status + ': ' + (payload?.error?.message || 'request failed'));
    return payload;
  };
  const lookup = () => api('/v4/aliases/' + encodeURIComponent(options.domain));
  let alias = await lookup();
  const current = alias.deploymentId || alias.deployment?.id;
  if (!current) throw new Error('Alias has no deployment ID');
  const result = { domain: options.domain, previousDeploymentId: current, action: options.action };
  if (options.action === 'switch') {
    if (current !== options['expected-current']) throw new Error('Concurrency stop: actual ' + current + ', expected ' + options['expected-current']);
    const target = await api('/v13/deployments/' + encodeURIComponent(options.target));
    if (target.readyState !== 'READY' && target.state !== 'READY') throw new Error('Target not READY');
    if (alias.projectId && target.projectId && alias.projectId !== target.projectId) throw new Error('Target belongs to another project');
    result.targetDeploymentId = options.target;
    if (!options.apply) return { ...result, state: 'DRY_RUN', productionChanged: false };
    await api('/v2/deployments/' + encodeURIComponent(options.target) + '/aliases', {
      method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ alias: options.domain })
    });
    alias = await lookup();
    if ((alias.deploymentId || alias.deployment?.id) !== options.target) throw new Error('Alias did not confirm expected deployment');
    result.productionChanged = true;
  }
  const routes = (options.routes || '/,/login,/app').split(',').map(x => x.trim());
  if (routes.some(x => !x.startsWith('/') || x.startsWith('//'))) throw new Error('Routes must be absolute paths');
  const checks = [];
  for (const route of routes) {
    const res = await fetcher('https://' + options.domain + route, { redirect: 'manual', headers: { 'cache-control': 'no-cache' }, signal: AbortSignal.timeout(10000) });
    const html = await res.text();
    const markerFound = options.marker ? html.includes(options.marker) : null;
    const pass = res.status === 200 && (res.headers.get('content-type') || '').includes('text/html') && (!options.marker || markerFound);
    checks.push({ route, status: res.status, markerFound, pass });
  }
  result.checks = checks;
  result.frontendVerified = checks.every(x => x.pass);
  result.apiWritesBlocked = 'NOT_CHECKED';
  result.existingPwaSessions = 'NOT_CHECKED';
  result.state = result.frontendVerified ? 'FRONTEND_HTTP_VERIFIED' : 'HTTP_CHECK_FAILED';
  if (!result.frontendVerified) throw new Error('HTTP validation failed: ' + JSON.stringify(result));
  return result;
}

async function main() {
  try { process.stdout.write(JSON.stringify(await execute(parseArgs(process.argv.slice(2))), null, 2) + '\n'); }
  catch (error) { process.stderr.write(error.message + '\n'); process.exitCode = 1; }
}
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) await main();
