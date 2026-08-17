/**
 * Selectors that mean "the app has rendered" — shared by every spec.
 *
 * History: the suite used to wait for `.ka-gate, .engine-body, .ka-landing`.
 * The July 2026 real-URLs / magazine pivot replaced the landing shell with
 * `Layout` (`.site-main`) + `LandingPage` (`.pop-landing`), so fifteen
 * specs waited 15s for classes that no longer exist and the CI job hit its
 * 15-minute ceiling on every push from 2026-06-10 on. Keep the legacy
 * classes here for the login gate and any engine view still using them —
 * one place to update next time the shell changes.
 */
export const APP_READY = '.pop-landing, .site-main, .ka-gate, .engine-body'

/** The magazine landing page specifically. */
export const LANDING = '.pop-landing'
