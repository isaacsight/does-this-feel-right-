import { supabase } from '../engine/SupabaseClient'
import type { ApprovalRegister, ChannelPlatform, PublisherChannel } from './model'

export interface PublisherDiscovery {
  configured: boolean
  organization: { id: string; name: string } | null
  channels: PublisherChannel[]
}

export interface DraftEditionInput {
  platform: Exclude<ChannelPlatform, 'reddit'>
  channelId: string
  title: string
  body: string
  mediaUrl: string
  aiGenerated: boolean
}

export interface DraftReceipt {
  platform: string
  channelId: string
  postId?: string
  status?: string
  ok: boolean
  error?: string
}

async function invokePublisher<T>(body: Record<string, unknown>): Promise<T> {
  const { data, error } = await supabase.functions.invoke('channel-publisher', { body })
  if (error) throw new Error(error.message || 'The publishing boundary did not respond.')
  if (data?.error) throw new Error(String(data.error))
  return data as T
}

export function discoverPublisher(): Promise<PublisherDiscovery> {
  return invokePublisher<PublisherDiscovery>({ action: 'discover' })
}

export function createPublisherDrafts(
  editions: DraftEditionInput[],
  approvals: ApprovalRegister,
): Promise<{ receipts: DraftReceipt[] }> {
  return invokePublisher<{ receipts: DraftReceipt[] }>({
    action: 'create_drafts',
    approvals,
    editions,
  })
}
