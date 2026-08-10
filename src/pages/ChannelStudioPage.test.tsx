import { fireEvent, render, screen } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { ChannelStudioFolio } from './ChannelStudioPage'

vi.mock('../channel-studio/publisher', () => ({
  discoverPublisher: vi.fn(),
  createPublisherDrafts: vi.fn(),
}))

describe('ChannelStudioFolio', () => {
  beforeEach(() => window.localStorage.clear())

  it('renders every edition and keeps the press gate closed by default', () => {
    render(<ChannelStudioFolio />)
    expect(screen.getByRole('heading', { name: /one press run/i })).toBeInTheDocument()
    expect(screen.getByRole('tab', { name: /youtube shorts/i })).toBeInTheDocument()
    expect(screen.getByRole('tab', { name: /tiktok/i })).toBeInTheDocument()
    expect(screen.getByRole('tab', { name: /instagram reels/i })).toBeInTheDocument()
    expect(screen.getByRole('tab', { name: /\bX\b/ })).toBeInTheDocument()
    expect(screen.getByRole('tab', { name: /reddit/i })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /send to buffer drafts/i })).toBeDisabled()
  })

  it('opens the selected platform proof without hiding the register', () => {
    render(<ChannelStudioFolio />)
    fireEvent.click(screen.getByRole('tab', { name: /tiktok/i }))
    expect(screen.getByText('PROOF · TIKTOK')).toBeInTheDocument()
    expect(screen.getByRole('tab', { name: /youtube shorts/i })).toBeVisible()
  })
})
