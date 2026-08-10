export type ChannelPlatform = 'youtube' | 'tiktok' | 'instagram' | 'twitter' | 'reddit'
export type EditionStatus = 'copy' | 'ready' | 'drafted' | 'manual' | 'failed'

export interface ChannelEdition {
  platform: ChannelPlatform
  title: string
  body: string
  enabled: boolean
  channelId: string
  delivery: 'buffer' | 'manual'
  status: EditionStatus
  receipt?: string
}

export interface ApprovalRegister {
  claims: boolean
  rights: boolean
  disclosure: boolean
  previews: boolean
}

export interface ChannelPackage {
  id: string
  folio: string
  title: string
  thesis: string
  sourceNote: string
  mediaUrl: string
  aiGenerated: boolean
  approvals: ApprovalRegister
  editions: ChannelEdition[]
}

export interface PublisherChannel {
  id: string
  name: string
  displayName: string
  service: string
  avatar?: string
  isQueuePaused: boolean
}

export const PLATFORM_COPY: Record<ChannelPlatform, { label: string; mark: string; note: string }> = {
  youtube: { label: 'YouTube Shorts', mark: 'YT', note: 'Searchable title · clean proof · related long-form' },
  tiktok: { label: 'TikTok', mark: 'TT', note: 'Conversational opening · original audio · native context' },
  instagram: { label: 'Instagram Reels', mark: 'IG', note: 'Editorial cover · saveable argument · restrained copy' },
  twitter: { label: 'X', mark: 'X', note: 'Thesis in the post · evidence visible without the player' },
  reddit: { label: 'Reddit', mark: 'R/', note: 'Community-specific draft · affiliation disclosed · manual post' },
}

export const INITIAL_CHANNEL_PACKAGE: ChannelPackage = {
  id: 'm01-capability-tokens',
  folio: 'PRESS RUN 001',
  title: 'Do not give an agent your account',
  thesis: 'Give an agent one bounded capability, with a resource, an expiry, and a limit.',
  sourceNote: 'agent-os capability-token implementation and kernel.chat month-one source packet',
  mediaUrl: '',
  aiGenerated: false,
  approvals: { claims: false, rights: false, disclosure: false, previews: false },
  editions: [
    {
      platform: 'youtube',
      title: 'The safer way to give an AI agent access',
      body: 'A broad API key says “act as me.” A capability token says: perform this action, on this resource, until this time, within this limit. Better agent security begins with smaller authority.',
      enabled: true,
      channelId: '',
      delivery: 'buffer',
      status: 'copy',
    },
    {
      platform: 'tiktok',
      title: 'Capability tokens',
      body: 'Don’t give an AI agent your account. Give it one action, one resource, one deadline, and one spending limit. If the credential leaks, its authority is already small.',
      enabled: true,
      channelId: '',
      delivery: 'buffer',
      status: 'copy',
    },
    {
      platform: 'instagram',
      title: 'Bound the capability',
      body: 'The safest credential is not merely hidden. It is deliberately unable to do much damage. One action. One resource. One expiry. One limit.',
      enabled: true,
      channelId: '',
      delivery: 'buffer',
      status: 'copy',
    },
    {
      platform: 'twitter',
      title: 'Authority should narrow at every handoff',
      body: 'A broad API key says “act as me.” A capability token says “perform this action, on this resource, until this time, within this limit.” Agent security is an authority-design problem before it is a model problem.',
      enabled: true,
      channelId: '',
      delivery: 'buffer',
      status: 'copy',
    },
    {
      platform: 'reddit',
      title: 'How are you downscoping credentials for agents?',
      body: 'I work on kernel.chat and agent-os, so this is directly related to our own implementation. We found that hiding a broad key was the wrong abstraction: the useful boundary was a short-lived capability limited to one action and resource. I would be interested in how others are handling revocation and delegated authority. I will add implementation details only where the community rules allow them.',
      enabled: false,
      channelId: '',
      delivery: 'manual',
      status: 'manual',
    },
  ],
}

export function platformMatchesService(platform: ChannelPlatform, service: string): boolean {
  const normalized = service.toLowerCase()
  if (platform === 'twitter') return normalized === 'twitter' || normalized === 'x'
  return normalized === platform
}

const SIGNED_MEDIA_QUERY_NAMES = new Set([
  'signature', 'expires', 'token',
  'x-amz-signature', 'x-amz-credential', 'x-amz-expires', 'x-amz-security-token',
  'x-goog-signature', 'x-goog-credential', 'x-goog-expires',
  'sig', 'se', 'sp', 'sv',
])

function isStableHttpsMediaUrl(value: string): boolean {
  try {
    const url = new URL(value)
    return url.protocol === 'https:'
      && [...url.searchParams.keys()].every(name => !SIGNED_MEDIA_QUERY_NAMES.has(name.toLowerCase()))
  } catch {
    return false
  }
}

export function validateChannelPackage(channelPackage: ChannelPackage): string[] {
  const problems: string[] = []
  const automated = channelPackage.editions.filter(edition => edition.enabled && edition.delivery === 'buffer')

  if (!automated.length) problems.push('Select at least one Buffer edition.')
  if (!isStableHttpsMediaUrl(channelPackage.mediaUrl)) problems.push('Add a stable public HTTPS video URL without signed or expiring query parameters.')

  for (const edition of automated) {
    if (!edition.channelId) problems.push(`Connect ${PLATFORM_COPY[edition.platform].label}.`)
    if (!edition.body.trim()) problems.push(`${PLATFORM_COPY[edition.platform].label} needs publication copy.`)
    if (edition.platform === 'youtube' && !edition.title.trim()) problems.push('YouTube needs a title.')
  }

  const missingApprovals = Object.entries(channelPackage.approvals)
    .filter(([, approved]) => !approved)
    .map(([name]) => name)
  if (missingApprovals.length) problems.push(`Complete the approval register: ${missingApprovals.join(', ')}.`)

  return problems
}

export function packageProgress(channelPackage: ChannelPackage): number {
  const automated = channelPackage.editions.filter(edition => edition.enabled && edition.delivery === 'buffer')
  const checks = [
    isStableHttpsMediaUrl(channelPackage.mediaUrl),
    automated.length > 0,
    automated.length > 0 && automated.every(edition => Boolean(edition.channelId)),
    Object.values(channelPackage.approvals).every(Boolean),
  ]
  return checks.filter(Boolean).length
}
