import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest'
import { readStorage, writeStorage } from './safeStorage'

describe('safeStorage', () => {
  beforeEach(() => window.localStorage.clear())
  afterEach(() => vi.restoreAllMocks())

  it('round-trips a value through write then read', () => {
    expect(writeStorage('k', { a: 1 })).toBe(true)
    expect(readStorage('k', null)).toEqual({ a: 1 })
  })

  it('returns the fallback when the key is missing', () => {
    expect(readStorage('missing', 'fallback')).toBe('fallback')
  })

  it('returns the fallback instead of throwing on malformed JSON', () => {
    window.localStorage.setItem('bad', '{not json')
    expect(readStorage('bad', 42)).toBe(42)
  })

  it('returns false instead of throwing when a write is refused (quota/private mode)', () => {
    vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {
      throw new DOMException('QuotaExceededError')
    })
    expect(writeStorage('k', { big: 'x' })).toBe(false)
  })

  it('returns the fallback instead of throwing when a read is refused', () => {
    vi.spyOn(Storage.prototype, 'getItem').mockImplementation(() => {
      throw new DOMException('SecurityError')
    })
    expect(readStorage('k', 'safe')).toBe('safe')
  })
})
