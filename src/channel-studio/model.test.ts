import { describe, expect, it } from 'vitest'
import { INITIAL_CHANNEL_PACKAGE, packageProgress, platformMatchesService, validateChannelPackage } from './model'

function completePackage() {
  return {
    ...INITIAL_CHANNEL_PACKAGE,
    mediaUrl: 'https://media.kernel.chat/press-run-001.mp4',
    approvals: { claims: true, rights: true, disclosure: true, previews: true },
    editions: INITIAL_CHANNEL_PACKAGE.editions.map(edition => ({
      ...edition,
      channelId: edition.delivery === 'buffer' ? `channel-${edition.platform}` : '',
    })),
  }
}

describe('channel studio model', () => {
  it('blocks an incomplete press run', () => {
    const problems = validateChannelPackage(INITIAL_CHANNEL_PACKAGE)
    expect(problems.some(problem => problem.includes('stable public HTTPS video URL'))).toBe(true)
    expect(problems.some(problem => problem.includes('approval register'))).toBe(true)
  })

  it('accepts a reviewed press run with connected channels', () => {
    expect(validateChannelPackage(completePackage())).toEqual([])
    expect(packageProgress(completePackage())).toBe(4)
  })

  it('rejects expiring signed media URLs', () => {
    const pkg = { ...completePackage(), mediaUrl: 'https://media.example/video.mp4?X-Amz-Signature=secret' }
    expect(validateChannelPackage(pkg).some(problem => problem.includes('signed or expiring'))).toBe(true)
  })

  it('does not count a manual-only Reddit selection as a connected press run', () => {
    const manualOnly = {
      ...completePackage(),
      editions: completePackage().editions.map(edition => ({
        ...edition,
        enabled: edition.platform === 'reddit',
      })),
    }
    expect(validateChannelPackage(manualOnly)).toContain('Select at least one Buffer edition.')
    expect(packageProgress(manualOnly)).toBe(2)
  })

  it('maps X to Buffer twitter channels', () => {
    expect(platformMatchesService('twitter', 'twitter')).toBe(true)
    expect(platformMatchesService('twitter', 'x')).toBe(true)
    expect(platformMatchesService('youtube', 'tiktok')).toBe(false)
  })
})
