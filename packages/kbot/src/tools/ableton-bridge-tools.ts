/**
 * ableton-bridge-tools.ts — Ableton Browser & Device Loading Tools
 *
 * Three-tier routing (each tool reports which plane answered):
 *   1. AbletonBridge (TCP 9001) — full browser API (optional; often not running)
 *   2. KBotBridge    (TCP 9997) — kbot's thin Remote Script
 *   3. AbletonOSC kbot handlers (UDP 11000) — /live/kbot/browser/search,
 *      /live/kbot/track/insert_device, /live/kbot/device/load_preset
 *      (kbot_ext.py inside AbletonOSC; replies are JSON read-backs)
 *
 * Tools:
 *   ableton_load_effect  — Load any Ableton native effect by name onto a track
 *   ableton_browse       — Search Ableton's browser (instruments, effects, presets, samples)
 *   ableton_load_preset  — Load a preset onto a device
 *   ableton_effect_chain — Apply a full chain of effects to a track in sequence
 */

import { registerTool } from './index.js'
import {
  AbletonBridgeClient,
  KBotRemoteClient,
  tryAbletonBridge,
  tryKBotRemote,
  getAvailableBridge,
  formatBridgeError,
  type BrowserItem,
} from '../integrations/ableton-bridge.js'
import { kbotTry, type KbotReply } from './ableton-lom.js'

// ── Helpers ─────────────────────────────────────────────────────────────

/** Convert 1-based user track to 0-based internal index. */
function userTrack(track: unknown): number {
  const n = Number(track)
  return Math.max(0, n - 1)
}

/** Category aliases for user convenience. */
const CATEGORY_ALIASES: Record<string, string> = {
  effects: 'audio_effects',
  effect: 'audio_effects',
  fx: 'audio_effects',
  audio_fx: 'audio_effects',
  midi_fx: 'midi_effects',
  midi: 'midi_effects',
  inst: 'instruments',
  instrument: 'instruments',
  drum: 'drums',
  kit: 'drums',
  sound: 'sounds',
  pack: 'packs',
  plugin: 'plugins',
  vst: 'plugins',
  au: 'plugins',
  sample: 'samples',
  preset: 'presets',
}

function resolveCategory(raw?: string): string | undefined {
  if (!raw) return undefined
  const lower = raw.toLowerCase().trim()
  return CATEGORY_ALIASES[lower] ?? lower
}

/** Format browser items for display. */
function formatBrowserItems(items: BrowserItem[], limit = 20): string {
  if (items.length === 0) return 'No results found.'

  const shown = items.slice(0, limit)
  const lines = shown.map((item) => {
    const tags: string[] = []
    if (item.isDevice) tags.push('device')
    if (item.isFolder) tags.push('folder')
    if (item.isLoadable) tags.push('loadable')
    const tagStr = tags.length > 0 ? ` [${tags.join(', ')}]` : ''
    return `- **${item.name}**${tagStr}\n  URI: \`${item.uri}\``
  })

  let result = lines.join('\n')
  if (items.length > limit) {
    result += `\n\n_...and ${items.length - limit} more results_`
  }
  return result
}

// ── Tier 3: AbletonOSC kbot handlers ─────────────────────────────────────

/** Map a /live/kbot/browser/search reply to BrowserItem[] (accepts items|results|any array field). */
export function browserItemsFromKbotReply(reply: KbotReply): BrowserItem[] {
  let list: unknown = reply.items ?? reply.results
  if (!Array.isArray(list)) {
    list = Object.values(reply).find((v) => Array.isArray(v)) ?? []
  }
  return (list as Array<Record<string, unknown>>).map((it) => ({
    name: String(it.name ?? ''),
    uri: String(it.uri ?? ''),
    isLoadable: Boolean(it.is_loadable ?? it.isLoadable ?? false),
    isDevice: Boolean(it.is_device ?? it.isDevice ?? false),
    isFolder: Boolean(it.is_folder ?? it.isFolder ?? false),
  }))
}

function oscUnavailableNote(reply: KbotReply): string {
  return `AbletonOSC kbot handler also failed: ${reply.error ?? 'no reply'}`
}

/** Device names from a /live/kbot/track/insert_device read-back (`devices` may hold strings or {name}). */
function deviceNamesFromReply(reply: KbotReply): string[] {
  const list = reply.devices
  if (!Array.isArray(list)) return []
  return list.map((d) => (typeof d === 'string' ? d : String((d as Record<string, unknown>)?.name ?? '')))
}

/**
 * Did the kbot track/insert_device read-back actually show a new device? `added` is the
 * device-count delta Live reported; when it is missing, fall back to the device list.
 * Never trust `ok` alone: browser.load_item can hot-swap or load nothing and still be ok.
 */
export function insertDeviceConfirmed(reply: KbotReply, requestedName: string): boolean {
  if (!reply.ok) return false
  if (typeof reply.added === 'number') return reply.added >= 1
  const want = requestedName.trim().toLowerCase()
  return deviceNamesFromReply(reply).some((n) => n.toLowerCase().includes(want))
}

const OSC_TIER_HINT =
  '**Option 3 — AbletonOSC kbot handlers (UDP 11000)**\n' +
  '  kbot_ext.py registered inside AbletonOSC (send /live/api/reload after install).\n' +
  '  Verify: ableton_lom action=ping'

// ── Tool Registration ───────────────────────────────────────────────────

export function registerAbletonBridgeTools(): void {

  // ─── 1. Load Effect ───────────────────────────────────────────────────

  registerTool({
    name: 'ableton_load_effect',
    description:
      'Load any Ableton native audio effect by name onto a track. ' +
      'This is the primary tool for adding effects like Saturator, Reverb, Compressor, EQ Eight, Auto Filter, etc. ' +
      'Routes through AbletonBridge (9001), then KBotBridge (9997), then the AbletonOSC kbot handler ' +
      '/live/kbot/track/insert_device (UDP 11000); the output states which plane answered and, on the OSC plane, ' +
      'Live\'s read-back device list. Supports position control to place the effect before or after existing devices.',
    parameters: {
      track: { type: 'number', description: 'Track number (1-based)', required: true },
      name: { type: 'string', description: 'Effect name (e.g. "Saturator", "Reverb", "Compressor", "EQ Eight", "Auto Filter", "Chorus-Ensemble")', required: true },
      position: {
        type: 'string',
        description: 'Where to place the effect: "before" (start of chain), "after" (after last device), "end" (same as after). Default: "end"',
      },
    },
    tier: 'free',
    timeout: 45_000, // bridge probes + up to 20 s for /live/kbot/track/insert_device
    async execute(args) {
      const t = userTrack(args.track)
      const name = String(args.name).trim()
      const position = String(args.position ?? 'end').toLowerCase()

      try {
        // Try AbletonBridge first (full browser API)
        const ab = await tryAbletonBridge()
        if (ab) {
          // Search specifically in audio_effects category
          const items = await ab.searchBrowser(name, 'audio_effects')

          // Find exact name match first, then partial match
          const exactMatch = items.find(
            (item) => item.isLoadable && item.name.toLowerCase() === name.toLowerCase()
          )
          const partialMatch = items.find(
            (item) => item.isLoadable && item.name.toLowerCase().includes(name.toLowerCase())
          )
          const target = exactMatch ?? partialMatch

          if (!target) {
            // Try broader search without category filter
            const broadItems = await ab.searchBrowser(name)
            const broadMatch = broadItems.find(
              (item) => item.isLoadable && (item.isDevice || item.name.toLowerCase().includes(name.toLowerCase()))
            )
            if (broadMatch) {
              await ab.loadDevice(t, broadMatch.uri)
              return `Loaded **${broadMatch.name}** on track ${args.track} (via AbletonBridge browser search)`
            }
            return `Effect "${name}" not found in Ableton's browser. Check the exact name (e.g. "EQ Eight" not "EQ8").`
          }

          await ab.loadDevice(t, target.uri)

          // Handle position if not "end" — move device within chain
          if (position === 'before') {
            const chain = await ab.getEffectChain(t)
            if (chain.length > 1) {
              // The newly loaded device is at the end — note this for the user
              return `Loaded **${target.name}** on track ${args.track} (via AbletonBridge; at end of chain — ${chain.length} devices total). Note: position reordering requires manual adjustment in Ableton.`
            }
          }

          return `Loaded **${target.name}** on track ${args.track} (via AbletonBridge)`
        }

        // Fallback to KBotBridge Remote Script
        const kb = await tryKBotRemote()
        if (kb) {
          const ok = await kb.loadDevice(t, name)
          if (ok) {
            return `Loaded **${name}** on track ${args.track} (via KBotBridge)`
          }
          return `KBotBridge could not load "${name}". The device may not be found in the browser.`
        }

        // Tier 3: AbletonOSC kbot handler — insert by name, position 0 = start of chain
        const oscArgs: (number | string)[] = position === 'before' ? [t, name, 0] : [t, name]
        const osc = await kbotTry('track/insert_device', ...oscArgs)
        if (osc.ok) {
          if (insertDeviceConfirmed(osc, name)) {
            return `Loaded **${name}** on track ${args.track} (via AbletonOSC kbot handler /live/kbot/track/insert_device). Live read-back:\n${JSON.stringify(osc, null, 2)}`
          }
          return `NOT confirmed: sent "${name}" to track ${args.track} via /live/kbot/track/insert_device but Live's read-back shows no new device ` +
            `(added=${String(osc.added ?? 'n/a')}, devices=${JSON.stringify(deviceNamesFromReply(osc))}). Live read-back:\n${JSON.stringify(osc, null, 2)}`
        }

        // No plane available
        return `${oscUnavailableNote(osc)}\n\n${formatBridgeError()}\n\n${OSC_TIER_HINT}`
      } catch (err) {
        return `Failed to load effect: ${(err as Error).message}\n\n${formatBridgeError()}\n\n${OSC_TIER_HINT}`
      }
    },
  })

  // ─── 2. Browse ────────────────────────────────────────────────────────

  registerTool({
    name: 'ableton_browse',
    description:
      'Search Ableton\'s browser for instruments, effects, presets, samples, packs, and plugins. ' +
      'Returns matching items with their URIs for loading. ' +
      'Routes through AbletonBridge (9001), then KBotBridge (9997), then the AbletonOSC kbot handler ' +
      '/live/kbot/browser/search (UDP 11000); the header states which plane answered. ' +
      'Use category to narrow results: "instruments", "audio_effects", "midi_effects", "drums", "sounds", "packs", "plugins", "samples", "presets".',
    parameters: {
      query: { type: 'string', description: 'Search query (e.g. "reverb", "piano", "808")', required: true },
      category: {
        type: 'string',
        description: 'Category filter: instruments, audio_effects (or "fx"), midi_effects (or "midi_fx"), drums, sounds, packs, plugins (or "vst"), samples, presets',
      },
    },
    tier: 'free',
    timeout: 45_000, // bridge probes + up to 20 s for /live/kbot/browser/search
    async execute(args) {
      const query = String(args.query).trim()
      const category = resolveCategory(args.category as string | undefined)

      try {
        // Try AbletonBridge first
        const ab = await tryAbletonBridge()
        if (ab) {
          const items = await ab.searchBrowser(query, category)
          const header = category
            ? `## Browser Search: "${query}" in ${category} (via AbletonBridge)`
            : `## Browser Search: "${query}" (via AbletonBridge)`
          return `${header}\n\n${formatBrowserItems(items)}`
        }

        // Fallback to KBotBridge
        const kb = await tryKBotRemote()
        if (kb) {
          const items = await kb.searchBrowser(query)
          return `## Browser Search: "${query}" (via KBotBridge)\n\n${formatBrowserItems(items)}`
        }

        // Tier 3: AbletonOSC kbot handler
        const oscArgs: (number | string)[] = category ? [query, category] : [query]
        const osc = await kbotTry('browser/search', ...oscArgs)
        if (osc.ok) {
          const items = browserItemsFromKbotReply(osc)
          const header = category
            ? `## Browser Search: "${query}" in ${category} (via AbletonOSC kbot handler)`
            : `## Browser Search: "${query}" (via AbletonOSC kbot handler)`
          return `${header}\n\n${formatBrowserItems(items)}`
        }

        return `${oscUnavailableNote(osc)}\n\n${formatBridgeError()}\n\n${OSC_TIER_HINT}`
      } catch (err) {
        return `Browse failed: ${(err as Error).message}\n\n${formatBridgeError()}\n\n${OSC_TIER_HINT}`
      }
    },
  })

  // ─── 3. Load Preset ───────────────────────────────────────────────────

  registerTool({
    name: 'ableton_load_preset',
    description:
      'Load a preset onto a device on a track. Searches available presets for the device and loads the best match. ' +
      'Routes through AbletonBridge (9001); when it is not running, falls back to the AbletonOSC kbot handler ' +
      '/live/kbot/device/load_preset (UDP 11000) which answers with a JSON read-back; the output states which plane answered. ' +
      'Use ableton_browse first to find the device URI if needed.',
    parameters: {
      track: { type: 'number', description: 'Track number (1-based)', required: true },
      device: { type: 'number', description: 'Device index on the track (0-based, first device = 0)', required: true },
      preset_name: { type: 'string', description: 'Preset name to search for (e.g. "Warm Pad", "Clean Lead")', required: true },
    },
    tier: 'free',
    timeout: 45_000, // bridge probe + up to 20 s for /live/kbot/device/load_preset
    async execute(args) {
      const t = userTrack(args.track)
      const deviceIdx = Number(args.device)
      const presetName = String(args.preset_name).trim()

      try {
        const ab = await tryAbletonBridge()
        if (!ab) {
          // KBotBridge (9997) has no preset API; go straight to the AbletonOSC kbot handler.
          const osc = await kbotTry('device/load_preset', t, deviceIdx, presetName)
          if (osc.ok) {
            return `Loaded preset **${presetName}** onto device ${deviceIdx} on track ${args.track} (via AbletonOSC kbot handler /live/kbot/device/load_preset). Live read-back:\n${JSON.stringify(osc, null, 2)}`
          }
          return `Preset loading needs AbletonBridge (port 9001) or the AbletonOSC kbot handler. ${oscUnavailableNote(osc)}\n\n${formatBridgeError()}\n\n${OSC_TIER_HINT}`
        }

        // Get the device chain to find the device URI
        const chain = await ab.getEffectChain(t)
        if (chain.length === 0) {
          return `No devices on track ${args.track}. Load a device first with ableton_load_effect.`
        }
        if (deviceIdx >= chain.length) {
          return `Track ${args.track} has ${chain.length} device(s) (indices 0-${chain.length - 1}). Device index ${deviceIdx} is out of range.`
        }

        const device = chain[deviceIdx]

        // Search for presets matching the device + preset name
        const presetItems = await ab.searchBrowser(`${device.name} ${presetName}`, 'presets')

        // Try to find a matching preset
        const exactMatch = presetItems.find(
          (p) => p.isLoadable && p.name.toLowerCase() === presetName.toLowerCase()
        )
        const partialMatch = presetItems.find(
          (p) => p.isLoadable && p.name.toLowerCase().includes(presetName.toLowerCase())
        )
        const target = exactMatch ?? partialMatch ?? presetItems.find((p) => p.isLoadable)

        if (!target) {
          // List available presets for the device
          const devicePresets = await ab.searchBrowser(device.name, 'presets')
          if (devicePresets.length > 0) {
            const presetList = devicePresets
              .filter((p) => p.isLoadable)
              .slice(0, 10)
              .map((p) => `  - ${p.name}`)
              .join('\n')
            return `No preset matching "${presetName}" for ${device.name}.\n\nAvailable presets:\n${presetList}`
          }
          return `No presets found for "${presetName}" on ${device.name} (device ${deviceIdx}).`
        }

        await ab.loadPreset(t, deviceIdx, target.uri)
        return `Loaded preset **${target.name}** onto **${device.name}** (track ${args.track}, device ${deviceIdx}) (via AbletonBridge)`
      } catch (err) {
        return `Failed to load preset: ${(err as Error).message}`
      }
    },
  })

  // ─── 4. Effect Chain ──────────────────────────────────────────────────

  registerTool({
    name: 'ableton_effect_chain',
    description:
      'Apply a full chain of audio effects to a track in sequence. ' +
      'Loads each effect one by one from Ableton\'s browser. ' +
      'Routes through AbletonBridge (9001), then KBotBridge (9997), then the AbletonOSC kbot handler ' +
      '/live/kbot/track/insert_device (UDP 11000); the summary line states which plane answered. ' +
      'Great for setting up standard chains like "Compressor → EQ Eight → Saturator → Reverb".',
    parameters: {
      track: { type: 'number', description: 'Track number (1-based)', required: true },
      chain: {
        type: 'array',
        description: 'Array of effect names to load in order (e.g. ["Compressor", "EQ Eight", "Saturator", "Reverb"])',
        required: true,
        items: { type: 'string' },
      },
    },
    tier: 'free',
    timeout: 120_000, // one insert_device round trip (up to 20 s) per effect
    async execute(args) {
      const t = userTrack(args.track)
      const chain = args.chain as string[]

      if (!Array.isArray(chain) || chain.length === 0) {
        return 'Error: `chain` must be an array of effect names (e.g. ["Compressor", "EQ Eight", "Reverb"]).'
      }

      const results: string[] = [`## Effect Chain → Track ${args.track}`, '']
      let loaded = 0
      let failed = 0

      try {
        // Try AbletonBridge first
        const ab = await tryAbletonBridge()
        if (ab) {
          for (const effectName of chain) {
            const name = String(effectName).trim()
            try {
              const items = await ab.searchBrowser(name, 'audio_effects')
              const exactMatch = items.find(
                (item) => item.isLoadable && item.name.toLowerCase() === name.toLowerCase()
              )
              const partialMatch = items.find(
                (item) => item.isLoadable && item.name.toLowerCase().includes(name.toLowerCase())
              )
              const target = exactMatch ?? partialMatch

              if (target) {
                await ab.loadDevice(t, target.uri)
                results.push(`- **${target.name}** loaded`)
                loaded++
              } else {
                results.push(`- **${name}** — not found in browser`)
                failed++
              }
            } catch (err) {
              results.push(`- **${name}** — error: ${(err as Error).message}`)
              failed++
            }
          }

          results.push('')
          results.push(`**${loaded}** loaded, **${failed}** failed out of ${chain.length} effects (via AbletonBridge).`)
          return results.join('\n')
        }

        // Fallback to KBotBridge — try loading each effect
        const kb = await tryKBotRemote()
        if (kb) {
          for (const effectName of chain) {
            const name = String(effectName).trim()
            try {
              const ok = await kb.loadDevice(t, name)
              if (ok) {
                results.push(`- **${name}** loaded`)
                loaded++
              } else {
                results.push(`- **${name}** — not found`)
                failed++
              }
            } catch (err) {
              results.push(`- **${name}** — error: ${(err as Error).message}`)
              failed++
            }
          }

          results.push('')
          results.push(`**${loaded}** loaded, **${failed}** failed out of ${chain.length} effects (via KBotBridge).`)
          return results.join('\n')
        }

        // Tier 3: AbletonOSC kbot handler — insert each device by name, read back
        const first = await kbotTry('track/insert_device', t, String(chain[0]).trim())
        if (first.ok || !/timeout|not connected|Could not connect/i.test(first.error ?? '')) {
          const outcomes: KbotReply[] = [first]
          for (let i = 1; i < chain.length; i++) {
            outcomes.push(await kbotTry('track/insert_device', t, String(chain[i]).trim()))
          }
          outcomes.forEach((r, i) => {
            const name = String(chain[i]).trim()
            if (r.ok && insertDeviceConfirmed(r, name)) {
              results.push(`- **${name}** loaded`)
              loaded++
            } else if (r.ok) {
              results.push(`- **${name}** — NOT confirmed (read-back shows no new device; added=${String(r.added ?? 'n/a')})`)
              failed++
            } else {
              results.push(`- **${name}** — ${r.error ?? 'error'}`)
              failed++
            }
          })
          const last = [...outcomes].reverse().find((r) => r.ok)
          results.push('')
          results.push(`**${loaded}** loaded, **${failed}** failed out of ${chain.length} effects (via AbletonOSC kbot handler).`)
          if (last) results.push(`Live read-back after last successful insert:\n${JSON.stringify(last, null, 2)}`)
          return results.join('\n')
        }

        return `${oscUnavailableNote(first)}\n\n${formatBridgeError()}\n\n${OSC_TIER_HINT}`
      } catch (err) {
        return `Effect chain failed: ${(err as Error).message}\n\n${formatBridgeError()}\n\n${OSC_TIER_HINT}`
      }
    },
  })
}
