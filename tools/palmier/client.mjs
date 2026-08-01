/**
 * Thin JSON-RPC client for Palmier Pro.
 *
 * Palmier exposes its MCP surface on 127.0.0.1:19789/mcp, which means the
 * house patterns can live in scripts instead of being hand-assembled by an
 * agent every film. That matters: the three shorts took 41 minutes of manual
 * timeline work and still shipped with a silent-audio bug and type grazing the
 * action rail. Both are the kind of thing a tested function does not do twice.
 */

const ENDPOINT = process.env.PALMIER_URL || 'http://127.0.0.1:19789/mcp'
let seq = 0

export async function call(tool, args = {}) {
  const res = await fetch(ENDPOINT, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json',
               Accept: 'application/json, text/event-stream' },
    body: JSON.stringify({
      jsonrpc: '2.0', id: ++seq,
      method: 'tools/call', params: { name: tool, arguments: args },
    }),
  })
  if (!res.ok) throw new Error(`palmier ${tool}: HTTP ${res.status}`)

  // The endpoint may answer as SSE even for a single response.
  const raw = await res.text()
  const body = raw.startsWith('data:')
    ? JSON.parse(raw.split('\n').find(l => l.startsWith('data:')).slice(5))
    : JSON.parse(raw)

  if (body.error) throw new Error(`palmier ${tool}: ${body.error.message}`)
  const content = body.result?.content?.[0]?.text
  if (!content) return body.result
  try { return JSON.parse(content) } catch { /* not JSON — fall through */ }
  // Palmier answers some failures with a bare string ("Editor not available")
  // rather than an rpc error. Returning it as data yields a String object that
  // quacks like a result and fails much later, so raise it here.
  if (/not available|no project|not open|failed|error/i.test(content)) {
    throw new Error(`palmier ${tool}: ${content}`)
  }
  return content
}

export async function isUp() {
  try {
    const r = await fetch(ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json',
                 Accept: 'application/json, text/event-stream' },
      body: JSON.stringify({ jsonrpc: '2.0', id: 0, method: 'tools/list' }),
    })
    return r.ok
  } catch { return false }
}

/**
 * Each JSON-RPC connection is its OWN Palmier session — opening a project via
 * the MCP tool in an agent session does not open it here. Every script must
 * open the project itself first or every call returns "Editor not available".
 */
export const open = path => call('manage_project', { action: 'open', path })
export const useTimeline = timelineId => call('set_active_timeline', { timelineId })

export const timeline = (a = {}) => call('get_timeline', a)
export const media    = (a = {}) => call('get_media', a)
export const transcript = (a = {}) => call('get_transcript', a)
