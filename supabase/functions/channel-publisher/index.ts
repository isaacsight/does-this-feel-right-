// Supabase Edge Function: channel-publisher
// A deliberately narrow Buffer boundary for the private Channel Studio.
// It discovers connected channels and creates drafts only. It never schedules,
// publishes, comments, or engages automatically.

import { serve } from 'https://deno.land/std@0.177.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'
import { corsHeaders, handlePreflight, SECURITY_HEADERS } from '../_shared/cors.ts'
import { requireContentType, requireJsonBody } from '../_shared/validate.ts'
import {
  assertVerifiedDraft,
  buildCreateDraftInput,
  publisherAccessError,
  serviceMatches,
  validateApprovalRegister,
  validateEdition,
  type BufferDraftPost,
  type DraftEdition,
} from './core.ts'

interface BufferOrganization {
  id: string
  name: string
  ownerEmail?: string
}

interface BufferChannel {
  id: string
  name: string
  displayName: string
  service: string
  avatar?: string
  isQueuePaused: boolean
}

const BUFFER_ENDPOINT = 'https://api.buffer.com'
const MAX_REQUEST_BYTES = 128 * 1024

function json(body: unknown, status: number, headers: Record<string, string>) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json', ...headers },
  })
}

async function bufferRequest<T>(apiKey: string, query: string, variables?: Record<string, unknown>): Promise<T> {
  const response = await fetch(BUFFER_ENDPOINT, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`,
    },
    body: JSON.stringify({ query, variables }),
  })

  const payload = await response.json().catch(() => null) as { data?: T; errors?: Array<{ message: string }> } | null
  if (!response.ok) throw new Error(`Buffer returned HTTP ${response.status}.`)
  if (!payload) throw new Error('Buffer returned an unreadable response.')
  if (payload.errors?.length) throw new Error(payload.errors.map(error => error.message).join(' '))
  if (!payload.data) throw new Error('Buffer returned no data.')
  return payload.data
}

async function discoverBuffer(apiKey: string) {
  const organizationData = await bufferRequest<{ account: { organizations: BufferOrganization[] } }>(apiKey, `
    query ChannelStudioOrganizations {
      account { organizations { id name ownerEmail } }
    }
  `)

  const organizations = organizationData.account.organizations
  const configuredId = Deno.env.get('BUFFER_ORGANIZATION_ID')
  const organization = organizations.find(item => item.id === configuredId) ?? organizations[0] ?? null
  if (!organization) return { organization: null, channels: [] as BufferChannel[] }

  const channelData = await bufferRequest<{ channels: BufferChannel[] }>(apiKey, `
    query ChannelStudioChannels($organizationId: OrganizationId!) {
      channels(input: { organizationId: $organizationId }) {
        id name displayName service avatar isQueuePaused
      }
    }
  `, { organizationId: organization.id })

  return { organization, channels: channelData.channels }
}

async function createDraft(apiKey: string, edition: DraftEdition) {
  const data = await bufferRequest<{
    createPost: { post?: BufferDraftPost; message?: string }
  }>(apiKey, `
    mutation ChannelStudioCreateDraft($input: CreatePostInput!) {
      createPost(input: $input) {
        ... on PostActionSuccess { post { id text status } }
        ... on MutationError { message }
      }
    }
  `, {
    input: buildCreateDraftInput(edition),
  })

  if (data.createPost.message) throw new Error(data.createPost.message)
  return assertVerifiedDraft(data.createPost.post)
}

serve(async (req: Request) => {
  if (req.method === 'OPTIONS') return handlePreflight(req)
  const headers = { ...corsHeaders(req), ...SECURITY_HEADERS }

  try {
    const contentTypeError = requireContentType(req)
    if (contentTypeError) return contentTypeError(headers)

    const token = req.headers.get('authorization')?.replace(/^Bearer\s+/i, '')
    if (!token) return json({ error: 'Missing authentication.' }, 401, headers)

    const authClient = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_ANON_KEY')!,
      { auth: { persistSession: false, autoRefreshToken: false } },
    )
    const { data: { user }, error: authError } = await authClient.auth.getUser(token)
    const accessError = publisherAccessError(authError ? null : user)
    if (accessError) return json({ error: accessError.error }, accessError.status, headers)

    const apiKey = Deno.env.get('BUFFER_API_KEY')
    const parsed = await requireJsonBody<{
      action?: string
      approvals?: unknown
      editions?: unknown[]
    }>(req, MAX_REQUEST_BYTES)
    if (parsed.error) return parsed.error(headers)
    const payload = parsed.body

    if (payload.action === 'discover') {
      if (!apiKey) return json({ configured: false, organization: null, channels: [] }, 200, headers)
      const discovery = await discoverBuffer(apiKey)
      return json({ configured: true, ...discovery }, 200, headers)
    }

    if (payload.action === 'create_drafts') {
      if (!apiKey) return json({ error: 'BUFFER_API_KEY is not configured.' }, 503, headers)
      try {
        validateApprovalRegister(payload.approvals)
      } catch (error) {
        return json({ error: error instanceof Error ? error.message : 'Invalid approval register.' }, 400, headers)
      }
      if (!Array.isArray(payload.editions) || payload.editions.length < 1 || payload.editions.length > 4) {
        return json({ error: 'Send between one and four editions.' }, 400, headers)
      }

      let editions: DraftEdition[]
      try {
        editions = payload.editions.map(validateEdition)
      } catch (error) {
        return json({ error: error instanceof Error ? error.message : 'Invalid platform edition.' }, 400, headers)
      }
      const discovery = await discoverBuffer(apiKey)
      const channelsById = new Map(discovery.channels.map(channel => [channel.id, channel]))

      for (const edition of editions) {
        const channel = channelsById.get(edition.channelId)
        if (!channel || !serviceMatches(edition.platform, channel.service)) {
          return json({ error: `${edition.platform}: channel is not connected to the configured Buffer organization.` }, 400, headers)
        }
      }

      const receipts: Array<Record<string, unknown>> = []
      for (const edition of editions) {
        try {
          const post = await createDraft(apiKey, edition)
          receipts.push({ platform: edition.platform, channelId: edition.channelId, postId: post.id, status: post.status, ok: true })
        } catch (error) {
          receipts.push({
            platform: edition.platform,
            channelId: edition.channelId,
            ok: false,
            error: error instanceof Error ? error.message : 'Buffer draft creation failed.',
          })
        }
      }

      return json({ receipts }, 200, headers)
    }

    return json({ error: 'Unsupported action.' }, 400, headers)
  } catch (error) {
    return json({ error: error instanceof Error ? error.message : 'Publishing boundary failed.' }, 500, headers)
  }
})
