import { describe, expect, it } from 'vitest'
import { OUTPUT_ROOT, outputPath, safeAssetStem } from './media-production-client'

describe('media production paths', () => {
  it('normalizes user-provided asset names', () => {
    expect(safeAssetStem('../../Hero shot: 01')).toBe('Hero-shot-01')
    expect(safeAssetStem('   ')).toMatch(/^asset-/)
  })

  it('keeps generated media inside output', () => {
    expect(outputPath('images', '../../outside', '.png')).toBe(`${OUTPUT_ROOT}/images/outside.png`)
  })
})
