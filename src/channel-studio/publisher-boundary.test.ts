import { describe, expect, it } from 'vitest'
import {
  assertVerifiedDraft,
  buildCreateDraftInput,
  publisherAccessError,
  validateApprovalRegister,
  validateEdition,
  type DraftEdition,
} from '../../supabase/functions/channel-publisher/core'

const edition: DraftEdition = {
  platform: 'youtube',
  channelId: 'channel-youtube',
  title: 'A bounded capability',
  body: 'One action, one resource, one expiry, one limit.',
  mediaUrl: 'https://media.kernel.chat/canary.mp4',
  aiGenerated: false,
}

describe('channel publisher boundary', () => {
  it('requires a real admin user', () => {
    expect(publisherAccessError(null)).toEqual({ status: 401, error: 'Unauthorized.' })
    expect(publisherAccessError({ app_metadata: {} })).toEqual({ status: 403, error: 'Publisher access required.' })
    expect(publisherAccessError({ app_metadata: { is_admin: true } })).toBeNull()
  })

  it('requires every named approval instead of one aggregate boolean', () => {
    expect(() => validateApprovalRegister({ claims: true, rights: true, disclosure: true, previews: false }))
      .toThrow(/previews/)
    expect(validateApprovalRegister({ claims: true, rights: true, disclosure: true, previews: true }))
      .toEqual({ claims: true, rights: true, disclosure: true, previews: true })
  })

  it('never accepts Reddit at the broadcast boundary', () => {
    expect(() => validateEdition({ ...edition, platform: 'reddit' })).toThrow(/unsupported platform/i)
  })

  it.each([
    'http://media.kernel.chat/canary.mp4',
    'https://storage.example/canary.mp4?X-Amz-Signature=secret',
    'https://storage.example/canary.mp4?X-Goog-Signature=secret',
    'https://storage.example/canary.mp4?sv=1&se=tomorrow&sig=secret',
  ])('rejects unstable media URL %s', mediaUrl => {
    expect(() => validateEdition({ ...edition, mediaUrl })).toThrow(/stable https/i)
  })

  it('builds an explicitly draft-only Buffer mutation input', () => {
    const input = buildCreateDraftInput(edition)
    expect(input).toMatchObject({
      channelId: 'channel-youtube',
      schedulingType: 'automatic',
      mode: 'addToQueue',
      saveToDraft: true,
      source: 'kernel-channel-studio',
    })
    expect(input).not.toHaveProperty('dueAt')
  })

  it('reports success only for a verified draft status', () => {
    expect(assertVerifiedDraft({ id: 'post-1', text: edition.body, status: 'draft' }).id).toBe('post-1')
    expect(() => assertVerifiedDraft({ id: 'post-2', text: edition.body, status: 'buffer' }))
      .toThrow(/post-2.*open buffer and remove it/i)
    expect(() => assertVerifiedDraft({ id: 'post-3', text: edition.body }))
      .toThrow(/unknown.*not a draft/i)
  })
})
