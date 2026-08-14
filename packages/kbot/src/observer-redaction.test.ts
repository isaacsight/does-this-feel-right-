import { describe, it, expect } from 'vitest'
import { redactSecrets } from './observer.js'

// The observer logs tool calls verbatim, including full Bash command strings.
// A live Anthropic key sat in session.jsonl for 113 days because of exactly
// that. These tests pin the redaction so it cannot silently regress.

describe('redactSecrets', () => {
  it('redacts the real leak shape: a key assigned in a shell command', () => {
    // Fixture value is deliberately nonsense — never derive test secrets from
    // the shape of a real one, especially in a public repo.
    const cmd = 'NEW_KEY="sk-ant-api03-EXAMPLEONLYnotarealkey000000000000000000000"; echo "len=${#NEW_KEY}"'
    const out = redactSecrets(cmd)
    expect(out).not.toContain('EXAMPLEONLYnotarealkey')
    expect(out).toContain('REDACTED')
    // The surrounding command must survive so the trace stays useful.
    expect(out).toContain('echo')
  })

  it.each([
    ['anthropic', 'sk-ant-api03-' + 'a'.repeat(40)],
    ['openai', 'sk-proj-' + 'b'.repeat(40)],
    ['github pat', 'github_pat_' + 'c'.repeat(30)],
    ['github token', 'ghp_' + 'd'.repeat(36)],
    ['slack', 'xoxb-' + '1'.repeat(20)],
    ['aws key id', 'AKIA' + 'E'.repeat(16)],
    ['google', 'AIza' + 'f'.repeat(35)],
  ])('redacts a %s credential', (_label, secret) => {
    const out = redactSecrets(`curl -H "auth: ${secret}" https://example.com`)
    expect(out).not.toContain(secret)
    expect(out).toContain('REDACTED')
  })

  it('redacts a Discord webhook URL (the 2026-03 leak shape)', () => {
    const url = 'https://discord.com/api/webhooks/1234567890/AbCdEf_GhIjKlMnOpQrStUv'
    const out = redactSecrets(`curl -X POST ${url}`)
    expect(out).not.toContain('AbCdEf_GhIjKlMnOpQrStUv')
    expect(out).toContain('REDACTED:discord-webhook')
  })

  it('redacts multi-line private key blocks', () => {
    const pem = '-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA\nabc123\n-----END RSA PRIVATE KEY-----'
    const out = redactSecrets(`echo "${pem}" > id_rsa`)
    expect(out).not.toContain('MIIEowIBAAKCAQEA')
    expect(out).toContain('REDACTED:private-key')
  })

  it('redacts every occurrence, not just the first', () => {
    const k = 'sk-ant-api03-' + 'z'.repeat(40)
    const out = redactSecrets(`A=${k} B=${k}`)
    expect(out).not.toContain('z'.repeat(40))
  })

  // Over-redaction would destroy the traces that feed training, so the
  // negative cases matter as much as the positive ones.
  it('leaves ordinary commands untouched', () => {
    for (const cmd of [
      'git commit -m "fix: handle empty token list"',
      'npm run build && npx tsc --noEmit',
      'grep -rn "API_KEY" src/ --include="*.ts"',
      'ls -la ~/.kbot/observer/',
    ]) {
      expect(redactSecrets(cmd)).toBe(cmd)
    }
  })

  it('does not redact short values assigned to secret-shaped names', () => {
    // Too short to be a credential — redacting these would be noise.
    expect(redactSecrets('API_KEY=abc')).toBe('API_KEY=abc')
  })

  it('preserves the variable name while redacting its value', () => {
    const out = redactSecrets('export GITHUB_TOKEN="abcdefghijklmnop123456"')
    expect(out).toContain('GITHUB_TOKEN')
    expect(out).not.toContain('abcdefghijklmnop123456')
  })
})
