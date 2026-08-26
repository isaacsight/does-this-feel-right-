import { describe, it, expect } from 'vitest'
import {
  composeBrief,
  findings,
  delta,
  avgTicket,
  laborPct,
  money,
  pct,
  type WeekData,
  type LocationWeek,
} from './brief'

function loc(overrides: Partial<LocationWeek> = {}): LocationWeek {
  return {
    name: 'Test Shop',
    sales: 10000,
    prevSales: 10000,
    transactions: 800,
    prevTransactions: 800,
    laborCost: 2500,
    ...overrides,
  }
}

function week(locations: LocationWeek[], laborTarget?: number): WeekData {
  return { weekStart: '2026-08-17', weekEnd: '2026-08-23', laborTarget, locations }
}

describe('derived metrics', () => {
  it('computes deltas against the prior week', () => {
    expect(delta(110, 100)).toBeCloseTo(0.1)
    expect(delta(90, 100)).toBeCloseTo(-0.1)
  })

  it('returns undefined when there is no usable prior value', () => {
    expect(delta(100, undefined)).toBeUndefined()
    expect(delta(100, 0)).toBeUndefined()
  })

  it('guards ticket and labor against zero denominators', () => {
    expect(avgTicket(loc({ transactions: 0 }))).toBeUndefined()
    expect(laborPct(loc({ sales: 0 }))).toBeUndefined()
    expect(laborPct(loc({ laborCost: undefined }))).toBeUndefined()
  })

  it('formats money and percentages', () => {
    expect(money(41230.4)).toBe('$41,230')
    expect(pct(0.036)).toBe('+3.6%')
    expect(pct(-0.042)).toBe('-4.2%')
  })
})

describe('findings', () => {
  it('flags labor over target', () => {
    const f = findings(week([loc({ name: 'Hollywood', laborCost: 3400 })]))
    expect(f).toHaveLength(1)
    expect(f[0].shop).toBe('Hollywood')
    expect(f[0].headline).toContain('labor ran 34.0%')
    expect(f[0].headline).toContain('$400')
  })

  it('flags a sales decline beyond the floor but ignores noise', () => {
    const noisy = findings(week([loc({ sales: 9850 })]))
    expect(noisy).toHaveLength(0)
    const real = findings(week([loc({ sales: 9000, laborCost: 2600 })]))
    expect(real.some((f) => f.watchLine.includes('sales -10.0%'))).toBe(true)
  })

  it('ranks a large labor overrun above a small sales dip', () => {
    const f = findings(
      week([
        loc({ name: 'Dipper', sales: 9700, laborCost: 2400, prevSales: 10000 }),
        loc({ name: 'Overspender', laborCost: 3500 }),
      ]),
    )
    expect(f[0].shop).toBe('Overspender')
  })

  it('respects a custom labor target', () => {
    const f = findings(week([loc({ laborCost: 2900 })], 0.28))
    expect(f).toHaveLength(1)
    expect(f[0].headline).toContain('28.0% plan')
  })
})

describe('composeBrief', () => {
  it('renders totals, per-shop lines, and the one thing to fix', () => {
    const brief = composeBrief(
      week([
        loc({ name: 'Newport Beach', sales: 41230, prevSales: 39800, transactions: 3120, prevTransactions: 3050 }),
        loc({ name: 'Hollywood', sales: 21540, prevSales: 21100, transactions: 1890, prevTransactions: 1850, laborCost: 7190 }),
      ]),
    )
    expect(brief).toContain('*STEREOSCOPE — WEEK IN REVIEW*')
    expect(brief).toContain('Aug 17 – Aug 23')
    expect(brief).toContain('*All shops:* $62,770')
    expect(brief).toContain('• Newport Beach —')
    expect(brief).toContain('*The one thing to fix*')
    expect(brief).toContain('Hollywood — labor ran 33.4%')
  })

  it('sorts shops by sales, largest first', () => {
    const brief = composeBrief(
      week([loc({ name: 'Small', sales: 5000 }), loc({ name: 'Big', sales: 50000, laborCost: 14000 })]),
    )
    expect(brief.indexOf('• Big')).toBeLessThan(brief.indexOf('• Small'))
  })

  it('says so plainly when the week is clean', () => {
    const brief = composeBrief(week([loc()]))
    expect(brief).toContain('Nothing over the line this week')
  })

  it('carries manager notes into the Watch list verbatim', () => {
    const brief = composeBrief(week([loc({ notes: ['Burrs due for replacement'] })]))
    expect(brief).toContain('*Watch*')
    expect(brief).toContain('• Test Shop: Burrs due for replacement')
  })

  it('omits deltas and labor when the data is not tracked yet', () => {
    const bare = composeBrief(
      week([{ name: 'New Shop', sales: 12000, transactions: 900 }]),
    )
    expect(bare).toContain('• New Shop — $12,000 · ticket $13.33')
    expect(bare).not.toContain('labor')
    expect(bare).not.toContain('vs prior week)')
  })

  it('refuses an empty week file', () => {
    expect(() => composeBrief(week([]))).toThrow('no locations')
  })
})
