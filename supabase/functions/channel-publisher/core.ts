export type Platform = 'youtube' | 'tiktok' | 'instagram' | 'twitter'

export interface ApprovalRegister {
  claims: boolean
  rights: boolean
  disclosure: boolean
  previews: boolean
}

export interface DraftEdition {
  platform: Platform
  channelId: string
  title: string
  body: string
  mediaUrl: string
  aiGenerated: boolean
}

export interface BufferDraftPost {
  id: string
  text: string
  status?: string
}

const ALLOWED_PLATFORMS = new Set<Platform>(['youtube', 'tiktok', 'instagram', 'twitter'])
const APPROVAL_KEYS: Array<keyof ApprovalRegister> = ['claims', 'rights', 'disclosure', 'previews']
const SIGNED_QUERY_NAMES = new Set([
  'signature', 'expires', 'token',
  'x-amz-signature', 'x-amz-credential', 'x-amz-expires', 'x-amz-security-token',
  'x-goog-signature', 'x-goog-credential', 'x-goog-expires',
  'sig', 'se', 'sp', 'sv',
])

export function publisherAccessError(user: unknown): { status: 401 | 403; error: string } | null {
  if (!user || typeof user !== 'object') return { status: 401, error: 'Unauthorized.' }
  const metadata = (user as { app_metadata?: Record<string, unknown> }).app_metadata
  if (metadata?.is_admin !== true) return { status: 403, error: 'Publisher access required.' }
  return null
}

export function serviceMatches(platform: Platform, service: string): boolean {
  const normalized = service.toLowerCase()
  if (platform === 'twitter') return normalized === 'twitter' || normalized === 'x'
  return platform === normalized
}

export function isStableHttpsMediaUrl(value: string): boolean {
  try {
    const url = new URL(value)
    if (url.protocol !== 'https:') return false
    return [...url.searchParams.keys()].every(name => !SIGNED_QUERY_NAMES.has(name.toLowerCase()))
  } catch {
    return false
  }
}

export function validateApprovalRegister(value: unknown): ApprovalRegister {
  if (!value || typeof value !== 'object') throw new Error('The complete approval register is required.')
  const approvals = value as Record<string, unknown>
  const missing = APPROVAL_KEYS.filter(key => approvals[key] !== true)
  if (missing.length) throw new Error(`Approval register incomplete: ${missing.join(', ')}.`)
  return approvals as unknown as ApprovalRegister
}

export function validateEdition(value: unknown): DraftEdition {
  if (!value || typeof value !== 'object') throw new Error('Each edition must be an object.')
  const edition = value as Record<string, unknown>
  const platform = String(edition.platform || '') as Platform
  const channelId = String(edition.channelId || '')
  const title = String(edition.title || '').trim()
  const body = String(edition.body || '').trim()
  const mediaUrl = String(edition.mediaUrl || '').trim()

  if (!ALLOWED_PLATFORMS.has(platform)) throw new Error(`Unsupported platform: ${platform || 'missing'}.`)
  if (!channelId || !body) throw new Error(`${platform}: channelId and body are required.`)
  if (platform === 'youtube' && !title) throw new Error('YouTube requires a title.')
  if (!isStableHttpsMediaUrl(mediaUrl)) {
    throw new Error(`${platform}: mediaUrl must be stable HTTPS without signed or expiring query parameters.`)
  }

  return { platform, channelId, title, body, mediaUrl, aiGenerated: edition.aiGenerated === true }
}

function platformMetadata(edition: DraftEdition): Record<string, unknown> | null {
  switch (edition.platform) {
    case 'youtube':
      return {
        youtube: {
          type: 'short',
          title: edition.title,
          privacy: 'public',
          categoryId: '28',
          license: 'youtube',
          notifySubscribers: true,
          embeddable: true,
          madeForKids: false,
          isAiGenerated: edition.aiGenerated,
        },
      }
    case 'instagram':
      return { instagram: { type: 'reel', shouldShareToFeed: true, isAiGenerated: edition.aiGenerated } }
    case 'tiktok':
      return { tiktok: { isAiGenerated: edition.aiGenerated } }
    case 'twitter':
      return null
  }
}

function videoAsset(edition: DraftEdition) {
  const metadata = edition.platform === 'instagram' || edition.platform === 'tiktok'
    ? { thumbnailOffset: 1000, title: edition.title || undefined }
    : edition.platform === 'youtube'
      ? { title: edition.title }
      : undefined

  return { video: { url: edition.mediaUrl, ...(metadata ? { metadata } : {}) } }
}

export function buildCreateDraftInput(edition: DraftEdition) {
  const metadata = platformMetadata(edition)
  return {
    text: edition.body,
    channelId: edition.channelId,
    schedulingType: 'automatic',
    mode: 'addToQueue',
    saveToDraft: true,
    source: 'kernel-channel-studio',
    aiAssisted: true,
    ...(metadata ? { metadata } : {}),
    assets: [videoAsset(edition)],
  }
}

export function assertVerifiedDraft(post: BufferDraftPost | undefined): BufferDraftPost {
  if (!post?.id) throw new Error('Buffer did not return a draft ID.')
  const status = String(post.status ?? '').toLowerCase()
  if (status !== 'draft') {
    throw new Error(`Buffer post ${post.id} came back as "${post.status ?? 'unknown'}", not a draft. Open Buffer and remove it — the boundary refuses to confirm an unverified draft.`)
  }
  return post
}
