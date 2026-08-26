// Stereoscope Monday brief — composition logic.
//
// One post, every Monday: how each shop did last week, plus the one
// thing to fix. Deterministic — every number in the post is arithmetic
// over the week file, so the brief can be trusted (and tested) without
// an LLM in the loop.
//
// Committed to James (Stereoscope ops) 2026-07-14 in Slack DM:
// "every monday, one post in this slack — how all 6 shops did last week
//  + the one thing to fix."

export interface LocationWeek {
  name: string
  /** Gross sales for the week, USD. */
  sales: number
  /** Same shop, prior week. Omit if unknown — deltas render as n/a. */
  prevSales?: number
  transactions: number
  prevTransactions?: number
  /** Total labor cost for the week, USD. Omit if not tracked yet. */
  laborCost?: number
  /** Manager-flagged items, passed through verbatim to the Watch list. */
  notes?: string[]
}

export interface WeekData {
  /** ISO date (YYYY-MM-DD), first day of the reported week. */
  weekStart: string
  /** ISO date (YYYY-MM-DD), last day of the reported week. */
  weekEnd: string
  /** Labor as a fraction of sales considered on-plan. Default 0.30. */
  laborTarget?: number
  locations: LocationWeek[]
}

export const DEFAULT_LABOR_TARGET = 0.3

interface Finding {
  /** Comparable across kinds; higher is worse. */
  severity: number
  shop: string
  /** Full sentence for "the one thing to fix". */
  headline: string
  /** Compressed form for the Watch list. */
  watchLine: string
}

// ── formatting ────────────────────────────────────────────────

export function money(n: number): string {
  const rounded = Math.round(n)
  return '$' + rounded.toLocaleString('en-US')
}

export function pct(fraction: number): string {
  const points = fraction * 100
  const sign = points > 0 ? '+' : ''
  return `${sign}${points.toFixed(1)}%`
}

function ratio(fraction: number): string {
  return `${(fraction * 100).toFixed(1)}%`
}

function shortDate(iso: string): string {
  const [y, m, d] = iso.split('-').map(Number)
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  if (!y || !m || !d || m < 1 || m > 12) return iso
  return `${months[m - 1]} ${d}`
}

// ── derived metrics ───────────────────────────────────────────

export function delta(current: number, previous?: number): number | undefined {
  if (previous === undefined || previous <= 0) return undefined
  return current / previous - 1
}

export function avgTicket(loc: LocationWeek): number | undefined {
  if (loc.transactions <= 0) return undefined
  return loc.sales / loc.transactions
}

export function laborPct(loc: LocationWeek): number | undefined {
  if (loc.laborCost === undefined || loc.sales <= 0) return undefined
  return loc.laborCost / loc.sales
}

// ── the one thing to fix ──────────────────────────────────────
//
// Severity is measured in "percentage points off plan", weighted by
// how directly the miss costs money. Labor overruns cost dollars the
// week they happen; sales declines might be weather; ticket declines
// are the softest signal.

const LABOR_WEIGHT = 1.5
const SALES_WEIGHT = 1.0
const TICKET_WEIGHT = 0.8
const SALES_DECLINE_FLOOR = 0.02 // ignore declines under 2%
const TICKET_DECLINE_FLOOR = 0.03 // ignore ticket drift under 3%

export function findings(data: WeekData): Finding[] {
  const target = data.laborTarget ?? DEFAULT_LABOR_TARGET
  const out: Finding[] = []

  for (const loc of data.locations) {
    const labor = laborPct(loc)
    if (labor !== undefined && labor > target) {
      const overspend = (labor - target) * loc.sales
      out.push({
        severity: (labor - target) * 100 * LABOR_WEIGHT,
        shop: loc.name,
        headline:
          `${loc.name} — labor ran ${ratio(labor)} of sales against a ` +
          `${ratio(target)} plan. That is roughly ${money(overspend)} of labor ` +
          `above plan for the week. Worth a schedule pass before next weekend.`,
        watchLine: `${loc.name} labor at ${ratio(labor)} (plan ${ratio(target)})`,
      })
    }

    const salesDelta = delta(loc.sales, loc.prevSales)
    if (salesDelta !== undefined && salesDelta < -SALES_DECLINE_FLOOR) {
      out.push({
        severity: -salesDelta * 100 * SALES_WEIGHT,
        shop: loc.name,
        headline:
          `${loc.name} — sales came in ${pct(salesDelta)} vs the prior week ` +
          `(${money(loc.sales)} against ${money(loc.prevSales ?? 0)}). ` +
          `Worth a look at what changed: hours, staffing, weather, or a menu shift.`,
        watchLine: `${loc.name} sales ${pct(salesDelta)} vs prior week`,
      })
    }

    const ticket = avgTicket(loc)
    const prevTicket =
      loc.prevSales !== undefined && loc.prevTransactions !== undefined && loc.prevTransactions > 0
        ? loc.prevSales / loc.prevTransactions
        : undefined
    const ticketDelta = ticket !== undefined ? delta(ticket, prevTicket) : undefined
    if (ticketDelta !== undefined && ticketDelta < -TICKET_DECLINE_FLOOR) {
      out.push({
        severity: -ticketDelta * 100 * TICKET_WEIGHT,
        shop: loc.name,
        headline:
          `${loc.name} — average ticket slipped ${pct(ticketDelta)} vs the prior ` +
          `week. Traffic held but people are buying less per visit; check whether ` +
          `attach (pastry, retail, upsizes) changed.`,
        watchLine: `${loc.name} avg ticket ${pct(ticketDelta)} vs prior week`,
      })
    }
  }

  return out.sort((a, b) => b.severity - a.severity)
}

// ── the post ──────────────────────────────────────────────────

const MAX_WATCH_ITEMS = 4

export function composeBrief(data: WeekData): string {
  if (data.locations.length === 0) {
    throw new Error('composeBrief: week file has no locations')
  }

  const totalSales = data.locations.reduce((s, l) => s + l.sales, 0)
  const totalPrev = data.locations.every((l) => l.prevSales !== undefined)
    ? data.locations.reduce((s, l) => s + (l.prevSales ?? 0), 0)
    : undefined
  const totalTxns = data.locations.reduce((s, l) => s + l.transactions, 0)
  const totalDelta = delta(totalSales, totalPrev)
  const companyTicket = totalTxns > 0 ? totalSales / totalTxns : undefined

  const lines: string[] = []
  lines.push('*STEREOSCOPE — WEEK IN REVIEW*')
  lines.push(`${shortDate(data.weekStart)} – ${shortDate(data.weekEnd)}`)
  lines.push('')

  const totalBits = [
    `${money(totalSales)}${totalDelta !== undefined ? ` (${pct(totalDelta)} vs prior week)` : ''}`,
    `${totalTxns.toLocaleString('en-US')} transactions`,
  ]
  if (companyTicket !== undefined) totalBits.push(`avg ticket ${money100(companyTicket)}`)
  lines.push(`*All shops:* ${totalBits.join(' · ')}`)
  lines.push('')

  lines.push('*By shop*')
  for (const loc of [...data.locations].sort((a, b) => b.sales - a.sales)) {
    const bits: string[] = [money(loc.sales)]
    const d = delta(loc.sales, loc.prevSales)
    if (d !== undefined) bits.push(pct(d))
    const ticket = avgTicket(loc)
    if (ticket !== undefined) bits.push(`ticket ${money100(ticket)}`)
    const labor = laborPct(loc)
    if (labor !== undefined) bits.push(`labor ${ratio(labor)}`)
    lines.push(`• ${loc.name} — ${bits.join(' · ')}`)
  }
  lines.push('')

  const found = findings(data)
  lines.push('*The one thing to fix*')
  if (found.length > 0) {
    lines.push(found[0].headline)
  } else {
    lines.push('Nothing over the line this week. Clean week — worth saying out loud.')
  }

  const watch = found.slice(1, 1 + MAX_WATCH_ITEMS).map((f) => `• ${f.watchLine}`)
  for (const loc of data.locations) {
    for (const note of loc.notes ?? []) {
      if (watch.length >= MAX_WATCH_ITEMS + 2) break
      watch.push(`• ${loc.name}: ${note}`)
    }
  }
  if (watch.length > 0) {
    lines.push('')
    lines.push('*Watch*')
    lines.push(...watch)
  }

  lines.push('')
  lines.push('_Numbers computed from the weekly POS export. Reply in thread if something looks off._')

  return lines.join('\n')
}

/** Dollar amount with cents, for per-ticket figures. */
function money100(n: number): string {
  return '$' + n.toFixed(2)
}
