import { useState } from 'react'
import type { CSSProperties } from 'react'
import type { IssueRecord, CompareSpread } from '../content/issues'
import { resolveAccentHex } from '../content/issues/accents'
import './CompareFeature.css'
import './IssueAccent.css'

interface CompareFeatureProps {
  spread: CompareSpread
  issue: IssueRecord
}

/**
 * CompareFeature — a binary switch between two incommensurable
 * readings of one fact set.
 *
 * Editorial tool #8 in the IssueFeature family, and the magazine's
 * second interactive spread — the first to use a genuinely different
 * control shape from the Dial (instrument). Where the Dial holds N
 * ordered positions on one variable, Compare holds exactly two
 * irreducible lenses with no position between them: role="switch",
 * native Enter/Space activation, no roving tabindex needed because
 * there is nothing to rove between but on and off.
 *
 * The fact set stays identical under both lenses; only the reading
 * of each fact changes underneath the switch. Both readings for
 * every fact remain in the DOM at all times — screen hides the
 * inactive one, print stacks both side by side so the comparison
 * survives on paper as two labelled columns.
 */
export function CompareFeature({ spread, issue }: CompareFeatureProps) {
  const stockClass = `pop-stock-${spread.stock ?? 'ivory'}`
  const accentHex = resolveAccentHex(issue.accent, spread.type)
  const accentStyle = { '--issue-accent-base': accentHex } as CSSProperties

  const [lensA, lensB] = spread.lenses
  const [activeId, setActiveId] = useState(spread.defaultLens ?? lensA.id)
  const isB = activeId === lensB.id
  const activeLens = isB ? lensB : lensA

  const renderSections = (sections?: typeof spread.intro) =>
    sections?.map((section, i) => (
      <section key={i} className="pop-compare-section">
        <h3 className="pop-compare-section-heading">
          {section.heading}
          {section.headingJp && (
            <span className="pop-compare-section-heading-jp">{section.headingJp}</span>
          )}
        </h3>
        {section.paragraphs.map((p, pi) => (
          <p key={pi} className="pop-compare-paragraph">{p}</p>
        ))}
      </section>
    ))

  return (
    <section className={`pop-compare ${stockClass}`} style={accentStyle} aria-labelledby="pop-compare-title">
      <div className="pop-compare-inner">

        {/* ── Head ───────────────────────────────────────── */}
        <header className="pop-compare-header">
          <span className="pop-kicker pop-kicker--tomato">{spread.kicker}</span>
          <hr className="pop-rule pop-rule--short pop-rule--tomato" />
          <h2 id="pop-compare-title" className="pop-display pop-compare-title">
            {spread.title}
          </h2>
          <p className="pop-feature-jp pop-compare-title-jp">{spread.titleJp}</p>
          <p className="pop-swash pop-compare-deck">{spread.deck}</p>
          <p className="pop-folio pop-compare-byline">{spread.byline}</p>
        </header>

        {/* ── Intro prose ─────────────────────────────────── */}
        {spread.intro && (
          <article className="pop-compare-prose">{renderSections(spread.intro)}</article>
        )}

        <hr className="pop-rule pop-compare-rule" />

        {/* ── THE SWITCH ───────────────────────────────────── */}
        <div className="pop-compare-apparatus">
          <button
            type="button"
            role="switch"
            aria-checked={isB}
            aria-label={`Reading lens — ${activeLens.label}: ${activeLens.stance}`}
            className="pop-compare-switch"
            onClick={() => setActiveId(isB ? lensA.id : lensB.id)}
          >
            <span className={`pop-compare-switch-side${!isB ? ' pop-compare-switch-side--active' : ''}`}>
              <span className="pop-folio pop-compare-switch-label">{lensA.label}</span>
              {lensA.labelJp && <span className="pop-compare-switch-jp" aria-hidden="true">{lensA.labelJp}</span>}
            </span>
            <span className="pop-compare-switch-track" aria-hidden="true">
              <span className={`pop-compare-switch-knob${isB ? ' pop-compare-switch-knob--b' : ''}`} />
            </span>
            <span className={`pop-compare-switch-side${isB ? ' pop-compare-switch-side--active' : ''}`}>
              <span className="pop-folio pop-compare-switch-label">{lensB.label}</span>
              {lensB.labelJp && <span className="pop-compare-switch-jp" aria-hidden="true">{lensB.labelJp}</span>}
            </span>
          </button>

          <p className="pop-compare-stance" aria-live="polite">{activeLens.stance}</p>

          {/* Both readings stay in the DOM for every fact; screen
              hides the inactive lens's column, print shows both. */}
          <div className="pop-compare-facts">
            {spread.facts.map((row, i) => (
              <div key={i} className="pop-compare-fact">
                <p className="pop-compare-fact-text">{row.fact}</p>
                {row.factJp && <p className="pop-compare-fact-jp" aria-hidden="true">{row.factJp}</p>}
                <div className="pop-compare-readings">
                  <p
                    className={`pop-compare-reading pop-compare-reading--a${!isB ? ' pop-compare-reading--active' : ''}`}
                    aria-hidden={isB}
                  >
                    <span className="pop-folio pop-compare-reading-tag">{lensA.label}</span>
                    {row.readingA}
                  </p>
                  <p
                    className={`pop-compare-reading pop-compare-reading--b${isB ? ' pop-compare-reading--active' : ''}`}
                    aria-hidden={!isB}
                  >
                    <span className="pop-folio pop-compare-reading-tag">{lensB.label}</span>
                    {row.readingB}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <hr className="pop-rule pop-compare-rule" />

        {/* ── Verdict (optional) — the piece may decline to resolve ── */}
        {spread.verdict && (
          <p className="pop-compare-verdict">{spread.verdict}</p>
        )}

        {/* ── Outro prose ─────────────────────────────────── */}
        {spread.outro && (
          <article className="pop-compare-prose">{renderSections(spread.outro)}</article>
        )}

        {/* ── Pull quote (optional) ───────────────────────── */}
        {spread.pullQuote && (
          <blockquote className="pop-compare-pullquote">
            <p className="pop-compare-pullquote-text">{spread.pullQuote.text}</p>
            <cite className="pop-folio pop-compare-pullquote-cite">{spread.pullQuote.attribution}</cite>
          </blockquote>
        )}

        {/* ── Works cited (optional) ──────────────────────── */}
        {spread.references && (
          <aside className="pop-compare-refs" aria-label="Works cited">
            <header className="pop-compare-refs-head">
              <span className="pop-kicker pop-kicker--tomato">{spread.references.kicker}</span>
              {spread.references.note && (
                <p className="pop-compare-refs-note">{spread.references.note}</p>
              )}
            </header>
            <ol className="pop-compare-refs-list">
              {spread.references.items.map((ref, i) => (
                <li key={i} className="pop-compare-refs-item">
                  <span className="pop-compare-refs-n">{String(i + 1).padStart(2, '0')}</span>
                  <span className="pop-compare-refs-body">
                    <span className="pop-compare-refs-authors">{ref.authors}</span>
                    <span className="pop-compare-refs-year"> ({ref.year}). </span>
                    <span className="pop-compare-refs-title">{ref.title}</span>
                    {ref.journal && <span className="pop-compare-refs-journal">. {ref.journal}</span>}
                    <span className="pop-compare-refs-dot">.</span>
                  </span>
                </li>
              ))}
            </ol>
          </aside>
        )}

        {/* ── Sign-off ────────────────────────────────────── */}
        <footer className="pop-compare-signoff">
          <hr className="pop-rule pop-rule--short pop-rule--tomato" />
          <p className="pop-swash pop-compare-signoff-text">{spread.signoff}</p>
          <div className="pop-monument pop-compare-monument">
            <span>ISSUE</span>
            <strong>{issue.number}</strong>
            <span>{issue.month} {issue.year}</span>
          </div>
        </footer>

      </div>
    </section>
  )
}
