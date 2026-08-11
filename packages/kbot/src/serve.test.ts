import { describe, it, expect } from 'vitest'
import { isAllowedOrigin, isLoopbackHost } from './serve.js'

describe('serve — CORS origin allow-list', () => {
  it('allows the kernel.chat site and localhost dev origins', () => {
    expect(isAllowedOrigin('https://kernel.chat')).toBe(true)
    expect(isAllowedOrigin('https://www.kernel.chat')).toBe(true)
    expect(isAllowedOrigin('http://localhost:5173')).toBe(true)
    expect(isAllowedOrigin('http://127.0.0.1:7437')).toBe(true)
  })

  it('rejects arbitrary sites — the cross-site RCE vector', () => {
    expect(isAllowedOrigin('https://evil.com')).toBe(false)
    expect(isAllowedOrigin('https://kernel.chat.evil.com')).toBe(false)
    expect(isAllowedOrigin('http://notkernel.chat')).toBe(false)
  })

  it('rejects a missing or malformed Origin (no wildcard fallback)', () => {
    expect(isAllowedOrigin(undefined)).toBe(false)
    expect(isAllowedOrigin('')).toBe(false)
    expect(isAllowedOrigin('not-a-url')).toBe(false)
    expect(isAllowedOrigin('file:///etc/passwd')).toBe(false)
  })
})

describe('serve — loopback bind detection', () => {
  it('treats loopback interfaces as safe to bind without a token', () => {
    for (const h of ['127.0.0.1', '::1', 'localhost', '127.0.0.53']) {
      expect(isLoopbackHost(h)).toBe(true)
    }
  })

  it('treats routable interfaces as requiring a token', () => {
    for (const h of ['0.0.0.0', '192.168.1.10', '10.0.0.5', '100.64.0.1']) {
      expect(isLoopbackHost(h)).toBe(false)
    }
  })
})
