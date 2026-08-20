import { describe, it, expect } from 'vitest'
import { ALL_ISSUES, LATEST_ISSUE, findIssue, INK_SEEDS, isPopeyeSafe } from './index'

describe('issue registry — catalog integrity', () => {
  const numbers = ALL_ISSUES.map((i) => Number(i.number))

  it('every issue number is a plain integer string', () => {
    for (const issue of ALL_ISSUES) {
      expect(issue.number).toMatch(/^\d+$/)
    }
  })

  it('issue numbers are unique', () => {
    expect(new Set(numbers).size).toBe(numbers.length)
  })

  /* PUBLISHING.md §VII: when another branch already claimed a number,
   * the later issue renumbers to the next free slot — so the registry
   * may carry a DECLARED gap until the other branch merges. Each entry
   * cites the off-branch claim; remove the entry when that issue lands. */
  const PENDING_OFF_BRANCH = [
    428, // claimed twice off-branch: e8b83bb2b (THE ONE PERCENT) + d8c89fb77 (NOTHING NEW WAS ADDED); 429 shipped around it
  ]

  it('issue numbers are ascending with no undeclared gaps (no reorder)', () => {
    for (let i = 1; i < numbers.length; i++) {
      expect(numbers[i], `expected a number above ${numbers[i - 1]}`).toBeGreaterThan(numbers[i - 1])
      for (let n = numbers[i - 1] + 1; n < numbers[i]; n++) {
        expect(PENDING_OFF_BRANCH, `gap at ${n} is not declared in PENDING_OFF_BRANCH`).toContain(n)
      }
    }
  })

  it('LATEST_ISSUE is the last and highest-numbered issue', () => {
    expect(LATEST_ISSUE).toBe(ALL_ISSUES[ALL_ISSUES.length - 1])
    expect(Number(LATEST_ISSUE.number)).toBe(Math.max(...numbers))
  })

  it('findIssue resolves a known number and rejects an unknown one', () => {
    expect(findIssue(LATEST_ISSUE.number)).toBe(LATEST_ISSUE)
    expect(findIssue('999999')).toBeUndefined()
  })
})

describe('issue registry — every issue is well-formed', () => {
  const REQUIRED = ['number', 'month', 'year', 'feature', 'featureJp', 'price', 'tagline'] as const

  it.each(ALL_ISSUES.map((i) => [i.number, i] as const))('ISSUE %s carries the required masthead fields', (_n, issue) => {
    for (const field of REQUIRED) {
      expect(typeof issue[field], field).toBe('string')
      expect((issue[field] as string).length, field).toBeGreaterThan(0)
    }
    const h = issue.headline
    expect(h.prefix.length, 'headline.prefix').toBeGreaterThan(0)
    expect(h.emphasis.length, 'headline.emphasis').toBeGreaterThan(0)
    expect(typeof h.suffix, 'headline.suffix').toBe('string')
    expect(typeof h.swash, 'headline.swash').toBe('string')
    expect(Array.isArray(issue.contents), 'contents').toBe(true)
    for (const c of issue.contents) {
      for (const field of ['n', 'en', 'jp', 'tag'] as const) {
        expect(typeof c[field], `contents.${field}`).toBe('string')
      }
    }
  })

  it.each(ALL_ISSUES.filter((i) => i.accent).map((i) => [i.number, i.accent!] as const))(
    'ISSUE %s declares a valid accent (named seed or POPEYE-safe hex)',
    (_n, accent) => {
      if (accent in INK_SEEDS) return // named seed — curated
      const verdict = isPopeyeSafe(accent) // raw hex must clear the guardrail
      expect(verdict.ok, `${accent}: ${verdict.reason}`).toBe(true)
    },
  )
})
