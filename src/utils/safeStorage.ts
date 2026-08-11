/**
 * safeStorage — localStorage that degrades instead of crashing.
 *
 * Bare `localStorage.getItem`/`setItem` throw in Safari private mode and
 * wherever storage is blocked or the quota is exceeded. When those calls sit
 * inside a `useEffect` or a debounced `setTimeout`, the throw escapes React's
 * render path and no `ErrorBoundary` can catch it — a whole page unmounts to
 * recover a non-essential write. These helpers make the read/write best-effort:
 * a blocked read returns the fallback, a blocked write is dropped.
 *
 * This is the pattern already proven in engine/AIEngine.ts; centralized here so
 * every call site shares one guard.
 */

export function readStorage<T>(key: string, fallback: T): T {
  if (typeof window === 'undefined') return fallback
  try {
    const raw = window.localStorage.getItem(key)
    return raw ? (JSON.parse(raw) as T) : fallback
  } catch {
    return fallback
  }
}

/** Best-effort write. Returns true if it landed, false if storage refused it. */
export function writeStorage(key: string, value: unknown): boolean {
  if (typeof window === 'undefined') return false
  try {
    window.localStorage.setItem(key, JSON.stringify(value))
    return true
  } catch {
    return false
  }
}
