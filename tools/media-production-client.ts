import { mkdir, readFile, readdir, writeFile } from 'node:fs/promises'
import { basename, extname, join, resolve } from 'node:path'
import { homedir } from 'node:os'

export const IMAGE_ENGINE = process.env.IMAGE_ENGINE_URL || 'http://127.0.0.1:5411'
export const MEDIA_ENGINE = process.env.MEDIA_ENGINE_URL || 'http://127.0.0.1:5412'
export const PROJECT_ROOT = process.cwd()
export const OUTPUT_ROOT = resolve(PROJECT_ROOT, 'output')

export type JsonRecord = Record<string, unknown>

export function safeAssetStem(value: string): string {
  const stem = value
    .normalize('NFKD')
    .replace(/[^a-zA-Z0-9_-]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 80)
  return stem || `asset-${Date.now()}`
}

export function outputPath(kind: 'images' | 'video' | 'audio', name: string, extension: string): string {
  const directory = resolve(OUTPUT_ROOT, kind)
  const path = resolve(directory, `${safeAssetStem(name)}.${extension.replace(/^\./, '')}`)
  if (!path.startsWith(`${directory}/`)) throw new Error('Unsafe output path')
  return path
}

export async function requestJson(url: string, init?: RequestInit): Promise<JsonRecord> {
  let response: Response
  try {
    response = await fetch(url, init)
  } catch {
    throw new Error(`Production engine offline at ${new URL(url).origin}`)
  }
  const payload = await response.json().catch(() => ({})) as JsonRecord
  if (!response.ok) throw new Error(String(payload.error || `Production engine error (${response.status})`))
  return payload
}

export async function engineToken(): Promise<string> {
  const tokenPath = process.env.ENGINE_TOKEN_PATH || join(homedir(), '.config', 'kernel', 'galley-engine-token')
  const token = (await readFile(tokenPath, 'utf8')).trim()
  if (!token) throw new Error('Production engine capability token is empty')
  return token
}

export async function paidPost(route: string, body: JsonRecord): Promise<JsonRecord> {
  const token = await engineToken()
  return requestJson(`${MEDIA_ENGINE}${route}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify(body),
  })
}

export async function saveLocalImage(prompt: string, name: string, width: number, height: number) {
  const payload = await requestJson(`${IMAGE_ENGINE}/v1/images/generations`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt, width, height }),
  })
  const data = payload.data as Array<{ b64_json?: string }> | undefined
  const encoded = data?.[0]?.b64_json
  if (!encoded) throw new Error('Local image engine returned no image')
  const path = outputPath('images', name, 'png')
  await mkdir(resolve(OUTPUT_ROOT, 'images'), { recursive: true })
  await writeFile(path, Buffer.from(encoded, 'base64'), { mode: 0o600 })
  return { path, backend: payload.backend, seconds: payload.seconds, width, height }
}

const MEDIA_EXTENSIONS = new Set(['.png', '.jpg', '.jpeg', '.webp', '.mp4', '.mov', '.mp3', '.wav'])

export async function listProductionAssets(limit = 100) {
  const assets: Array<{ kind: string; name: string; path: string; bytes: number; modifiedAt: string }> = []
  for (const kind of ['images', 'videos', 'video', 'audio'] as const) {
    const directory = resolve(OUTPUT_ROOT, kind)
    const entries = await readdir(directory, { withFileTypes: true }).catch(() => [])
    for (const entry of entries) {
      if (!entry.isFile() || !MEDIA_EXTENSIONS.has(extname(entry.name).toLowerCase())) continue
      const path = join(directory, basename(entry.name))
      const file = await import('node:fs/promises').then(fs => fs.stat(path))
      assets.push({ kind, name: entry.name, path, bytes: file.size, modifiedAt: file.mtime.toISOString() })
    }
  }
  return assets.sort((a, b) => b.modifiedAt.localeCompare(a.modifiedAt)).slice(0, limit)
}
