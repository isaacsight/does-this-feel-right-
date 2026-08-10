import { Suspense, useEffect, useMemo, useState } from 'react'
import { KernelLoading } from '../components/KernelLoading'
import { LoginGate } from '../components/LoginGate'
import { useAuthContext } from '../providers/AuthProvider'
import {
  INITIAL_CHANNEL_PACKAGE,
  PLATFORM_COPY,
  packageProgress,
  platformMatchesService,
  validateChannelPackage,
  type ChannelEdition,
  type ChannelPackage,
  type PublisherChannel,
} from '../channel-studio/model'
import { createPublisherDrafts, discoverPublisher, type DraftReceipt } from '../channel-studio/publisher'
import './ChannelStudioPage.css'

const STORAGE_KEY = 'kernel-channel-studio-v1'

function loadPackage(): ChannelPackage {
  try {
    const saved = window.localStorage.getItem(STORAGE_KEY)
    if (!saved) return structuredClone(INITIAL_CHANNEL_PACKAGE)
    const parsed = JSON.parse(saved) as ChannelPackage
    return parsed.id === INITIAL_CHANNEL_PACKAGE.id ? parsed : structuredClone(INITIAL_CHANNEL_PACKAGE)
  } catch {
    return structuredClone(INITIAL_CHANNEL_PACKAGE)
  }
}

function editionLabel(edition: ChannelEdition) {
  if (edition.status === 'drafted') return 'Buffer draft'
  if (edition.delivery === 'manual') return 'Manual edition'
  if (!edition.channelId) return 'Needs channel'
  return 'Ready for proof'
}

export function ChannelStudioPage() {
  const { isLoading, isAuthenticated, isAdmin } = useAuthContext()
  const isLocalDesignProof = import.meta.env.DEV
    && new URLSearchParams(window.location.search).get('proof') === 'folio'

  if (isLocalDesignProof) return <ChannelStudioFolio />
  if (isLoading) return <KernelLoading showLogo />
  if (!isAuthenticated) return <Suspense fallback={null}><LoginGate /></Suspense>
  if (!isAdmin) {
    return (
      <main className="cs-access-sheet">
        <p>PRIVATE PRESS · ACCESS REGISTER</p>
        <h1>This folio belongs to the publisher.</h1>
        <a href="/">Return to kernel.chat</a>
      </main>
    )
  }
  return <ChannelStudioFolio />
}

export function ChannelStudioFolio() {
  const [channelPackage, setChannelPackage] = useState<ChannelPackage>(() => loadPackage())
  const [channels, setChannels] = useState<PublisherChannel[]>([])
  const [selectedPlatform, setSelectedPlatform] = useState(channelPackage.editions[0].platform)
  const [connectionNote, setConnectionNote] = useState('Buffer has not been inspected in this session.')
  const [working, setWorking] = useState(false)
  const [receipts, setReceipts] = useState<DraftReceipt[]>([])

  const selectedEdition = channelPackage.editions.find(edition => edition.platform === selectedPlatform) ?? channelPackage.editions[0]
  const problems = useMemo(() => validateChannelPackage(channelPackage), [channelPackage])
  const progress = packageProgress(channelPackage)

  useEffect(() => {
    document.title = 'Channel Studio · kernel.chat'
  }, [])

  useEffect(() => {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(channelPackage))
  }, [channelPackage])

  const updateEdition = (platform: ChannelEdition['platform'], patch: Partial<ChannelEdition>) => {
    setChannelPackage(current => ({
      ...current,
      editions: current.editions.map(edition => edition.platform === platform ? { ...edition, ...patch } : edition),
    }))
  }

  const inspectPress = async () => {
    setWorking(true)
    setConnectionNote('Inspecting the private publishing boundary…')
    try {
      const discovery = await discoverPublisher()
      setChannels(discovery.channels)
      setConnectionNote(discovery.organization
        ? `${discovery.organization.name}: ${discovery.channels.length} connected channels found.`
        : 'Buffer is configured, but no organization was returned.')

      setChannelPackage(current => ({
        ...current,
        editions: current.editions.map(edition => {
          if (edition.delivery !== 'buffer' || edition.channelId) return edition
          const candidates = discovery.channels.filter(channel => platformMatchesService(edition.platform, channel.service))
          return candidates.length === 1 ? { ...edition, channelId: candidates[0].id } : edition
        }),
      }))
    } catch (error) {
      setConnectionNote(error instanceof Error ? error.message : 'Buffer inspection failed.')
    } finally {
      setWorking(false)
    }
  }

  const sendToProofDesk = async () => {
    if (problems.length) return
    const approved = window.confirm('Create private Buffer drafts for every enabled edition? Nothing will publish yet.')
    if (!approved) return

    setWorking(true)
    setReceipts([])
    try {
      const editions = channelPackage.editions
        .filter((edition): edition is ChannelEdition & { platform: Exclude<ChannelEdition['platform'], 'reddit'> } => edition.enabled && edition.delivery === 'buffer' && edition.platform !== 'reddit')
        .map(edition => ({
          platform: edition.platform,
          channelId: edition.channelId,
          title: edition.title,
          body: edition.body,
          mediaUrl: channelPackage.mediaUrl,
          aiGenerated: channelPackage.aiGenerated,
        }))
      const result = await createPublisherDrafts(editions, channelPackage.approvals)
      setReceipts(result.receipts)
      setChannelPackage(current => ({
        ...current,
        editions: current.editions.map(edition => {
          const receipt = result.receipts.find(item => item.platform === edition.platform)
          if (!receipt) return edition
          return { ...edition, status: receipt.ok ? 'drafted' : 'failed', receipt: receipt.postId ?? receipt.error }
        }),
      }))
    } catch (error) {
      setReceipts([{ platform: 'press', channelId: '', ok: false, error: error instanceof Error ? error.message : 'Draft creation failed.' }])
    } finally {
      setWorking(false)
    }
  }

  return (
    <main className="cs-shell">
      <header className="cs-running-head">
        <a href="/" className="cs-masthead">kernel.chat</a>
        <p><span>CHANNEL STUDIO</span><span>PRIVATE PRESS</span><span>{channelPackage.folio}</span></p>
      </header>

      <section className="cs-threshold">
        <div className="cs-title-lockup">
          <p className="cs-kicker">ONE MANUSCRIPT · FIVE EDITIONS</p>
          <h1>One press run.<br /><em>Everywhere it belongs.</em></h1>
        </div>
        <div className="cs-job-ticket" aria-label="Press run progress">
          <span>JOB № 001</span>
          <strong>{progress}/4</strong>
          <p>production gates cleared</p>
          <div className="cs-progress-rule" aria-label={`${progress} of 4 production gates cleared`}>
            {Array.from({ length: 4 }, (_, index) => <i key={index} className={index < progress ? 'is-clear' : ''} />)}
          </div>
        </div>
      </section>

      <section className="cs-orientation">
        <div>
          <p className="cs-section-no">I · MANUSCRIPT</p>
          <label>
            <span>Working title</span>
            <input value={channelPackage.title} onChange={event => setChannelPackage(current => ({ ...current, title: event.target.value }))} />
          </label>
        </div>
        <label className="cs-thesis-field">
          <span>Editorial sentence</span>
          <textarea value={channelPackage.thesis} onChange={event => setChannelPackage(current => ({ ...current, thesis: event.target.value }))} />
        </label>
        <div className="cs-source-slip">
          <span>SOURCE REGISTER</span>
          <p>{channelPackage.sourceNote}</p>
        </div>
      </section>

      <section className="cs-media-register">
        <div>
          <p className="cs-section-no">II · MASTER</p>
          <h2>The clean export</h2>
          <p>One direct HTTPS video file. No watermark. No expiring signature. Buffer must be able to fetch it when the scheduled hour arrives.</p>
        </div>
        <label>
          <span>Stable public media URL</span>
          <input
            type="url"
            placeholder="https://media.kernel.chat/press-run-001.mp4"
            value={channelPackage.mediaUrl}
            onChange={event => setChannelPackage(current => ({ ...current, mediaUrl: event.target.value }))}
          />
        </label>
        <label className="cs-check-line">
          <input type="checkbox" checked={channelPackage.aiGenerated} onChange={event => setChannelPackage(current => ({ ...current, aiGenerated: event.target.checked }))} />
          <span>Contains realistic AI-generated or materially altered media</span>
        </label>
      </section>

      <section className="cs-edition-register">
        <div className="cs-edition-heading">
          <div>
            <p className="cs-section-no">III · EDITIONS</p>
            <h2>Same evidence.<br />Native reading.</h2>
          </div>
          <div className="cs-connection-copy">
            <p>{connectionNote}</p>
            <button type="button" onClick={inspectPress} disabled={working}>{working ? 'Inspecting…' : 'Inspect Buffer'}</button>
          </div>
        </div>

        <div className="cs-edition-table" role="tablist" aria-label="Platform editions">
          {channelPackage.editions.map((edition, index) => {
            const copy = PLATFORM_COPY[edition.platform]
            return (
              <button
                key={edition.platform}
                type="button"
                role="tab"
                aria-label={`${copy.label}: ${editionLabel(edition)}`}
                aria-selected={edition.platform === selectedPlatform}
                className={edition.platform === selectedPlatform ? 'is-selected' : ''}
                onClick={() => setSelectedPlatform(edition.platform)}
              >
                <span className="cs-edition-index">{String(index + 1).padStart(2, '0')}</span>
                <strong>{copy.mark}</strong>
                <span className="cs-edition-name">{copy.label}<small>{copy.note}</small></span>
                <span className={`cs-edition-state is-${edition.status}`}>{editionLabel(edition)}</span>
              </button>
            )
          })}
        </div>

        <article className="cs-proof-sheet" aria-live="polite">
          <div className="cs-proof-meta">
            <p>PROOF · {PLATFORM_COPY[selectedEdition.platform].label.toUpperCase()}</p>
            <label className="cs-toggle-line">
              <input
                type="checkbox"
                checked={selectedEdition.enabled}
                onChange={event => updateEdition(selectedEdition.platform, { enabled: event.target.checked })}
              />
              <span>{selectedEdition.delivery === 'manual' ? 'Prepare community draft' : 'Include in press run'}</span>
            </label>
          </div>
          <div className="cs-proof-fields">
            <label>
              <span>{selectedEdition.platform === 'youtube' ? 'Video title' : 'Editorial label'}</span>
              <input value={selectedEdition.title} onChange={event => updateEdition(selectedEdition.platform, { title: event.target.value, status: 'copy' })} />
            </label>
            <label>
              <span>Platform copy</span>
              <textarea value={selectedEdition.body} onChange={event => updateEdition(selectedEdition.platform, { body: event.target.value, status: 'copy' })} />
            </label>
          </div>
          <div className="cs-proof-binding">
            {selectedEdition.delivery === 'manual' ? (
              <p>Reddit stays outside the broadcast machine. Check the community rules, disclose the affiliation, and post this edition by hand.</p>
            ) : (
              <label>
                <span>Connected Buffer channel</span>
                <select value={selectedEdition.channelId} onChange={event => updateEdition(selectedEdition.platform, { channelId: event.target.value, status: 'ready' })}>
                  <option value="">Choose a channel</option>
                  {channels.filter(channel => platformMatchesService(selectedEdition.platform, channel.service)).map(channel => (
                    <option key={channel.id} value={channel.id}>{channel.displayName || channel.name}{channel.isQueuePaused ? ' · paused' : ''}</option>
                  ))}
                </select>
              </label>
            )}
            {selectedEdition.receipt && <p className="cs-receipt">Receipt: {selectedEdition.receipt}</p>}
          </div>
        </article>
      </section>

      <section className="cs-approval-register">
        <div>
          <p className="cs-section-no">IV · SIGN-OFF</p>
          <h2>The press does not move without a signature.</h2>
        </div>
        <div className="cs-approval-lines">
          {([
            ['claims', 'Every factual claim has a primary source.'],
            ['rights', 'The footage, voice, music, and type are owned or licensed.'],
            ['disclosure', 'AI and affiliation disclosures are accurate.'],
            ['previews', 'Every title, crop, caption, and call to action was reviewed.'],
          ] as const).map(([key, copy], index) => (
            <label key={key}>
              <span>{String(index + 1).padStart(2, '0')}</span>
              <input
                type="checkbox"
                checked={channelPackage.approvals[key]}
                onChange={event => setChannelPackage(current => ({
                  ...current,
                  approvals: { ...current.approvals, [key]: event.target.checked },
                }))}
              />
              <strong>{copy}</strong>
            </label>
          ))}
        </div>
      </section>

      <section className="cs-press-gate">
        <div>
          <p className="cs-section-no">V · PROOF DESK</p>
          {problems.length ? (
            <>
              <h2>{problems.length} {problems.length === 1 ? 'matter' : 'matters'} before press.</h2>
              <ol>{problems.map(problem => <li key={problem}>{problem}</li>)}</ol>
            </>
          ) : (
            <>
              <h2>Ready to make private drafts.</h2>
              <p>Buffer receives one draft per enabled edition. Nothing publishes until those drafts are scheduled.</p>
            </>
          )}
        </div>
        <button type="button" disabled={Boolean(problems.length) || working} onClick={sendToProofDesk}>
          {working ? 'Setting type…' : 'Send to Buffer drafts'}
        </button>
        {receipts.length > 0 && (
          <div className="cs-receipt-ledger" aria-live="polite">
            {receipts.map(receipt => <p key={`${receipt.platform}-${receipt.channelId}`} className={receipt.ok ? 'is-ok' : 'is-error'}>{receipt.platform}: {receipt.ok ? `${receipt.status ?? 'draft'} ${receipt.postId}` : receipt.error}</p>)}
          </div>
        )}
      </section>

      <footer className="cs-colophon">
        <span>★ KERNEL.CHAT PRIVATE PRESS</span>
        <span>Draft-first · human-approved · no automatic engagement</span>
        <a href="/palmier-suite">Production suite →</a>
      </footer>
    </main>
  )
}
