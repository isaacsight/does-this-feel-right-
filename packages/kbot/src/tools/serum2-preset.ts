/**
 * serum2-preset.ts — Create Serum 2 presets programmatically
 *
 * Uses the reverse-engineered .SerumPreset format (XferJson + Zstandard CBOR)
 * via node-serum2-preset-packager to create, modify, and install presets.
 *
 * Tools:
 *   serum2_preset — Create a Serum 2 preset from a description
 */

import { registerTool } from './index.js'
import { execSync } from 'node:child_process'
import * as fs from 'node:fs'
import * as path from 'node:path'
import * as os from 'node:os'

function getSerumPresetsDir(): string {
  if (process.platform === 'darwin') {
    return '/Library/Audio/Presets/Xfer Records/Serum 2 Presets/Presets/User'
  }
  return path.join(os.homedir(), 'Documents', 'Xfer', 'Serum 2 Presets', 'Presets', 'User')
}

function ensurePresetPackager(): boolean {
  try {
    require.resolve('node-serum2-preset-packager')
    return true
  } catch {
    try {
      execSync('npm install node-serum2-preset-packager --no-save', {
        cwd: path.join(__dirname, '..', '..'),
        stdio: 'pipe',
      })
      return true
    } catch {
      return false
    }
  }
}

interface PresetParams {
  name: string
  type: 'lead' | 'bass' | 'pad' | 'keys' | 'pluck' | 'chord' | 'texture' | 'fx'
  oscA: { unison: number; detune: number; width: number }
  oscB: { enabled: boolean; volume: number; detune: number }
  env: { attack: number; decay: number; sustain: number; release: number }
  filter: { cutoff: number; resonance: number; drive: number }
  character: 'lush' | 'dark' | 'bright' | 'warm' | 'aggressive' | 'dreamy'
}

const PRESETS: Record<string, PresetParams> = {
  'emotional-drift': {
    name: 'kbot - Emotional Drift',
    type: 'lead',
    oscA: { unison: 9, detune: 0.16, width: 90 },
    oscB: { enabled: true, volume: -6, detune: 0.10 },
    env: { attack: 0.025, decay: 1.4, sustain: -2.5, release: 0.65 },
    filter: { cutoff: 0.72, resonance: 6, drive: 5 },
    character: 'lush',
  },
  'deep-gravity': {
    name: 'kbot - Deep Gravity',
    type: 'bass',
    oscA: { unison: 1, detune: 0, width: 0 },
    oscB: { enabled: false, volume: -100, detune: 0 },
    env: { attack: 0, decay: 2.2, sustain: -60, release: 0.45 },
    filter: { cutoff: 0.22, resonance: 0, drive: 15 },
    character: 'dark',
  },
  'silk-nebula': {
    name: 'kbot - Silk Nebula',
    type: 'pad',
    oscA: { unison: 12, detune: 0.22, width: 100 },
    oscB: { enabled: true, volume: -4, detune: 0.18 },
    env: { attack: 0.6, decay: 0.3, sustain: -1, release: 1.8 },
    filter: { cutoff: 0.65, resonance: 4, drive: 3 },
    character: 'dreamy',
  },
  'glass-memory': {
    name: 'kbot - Glass Memory',
    type: 'keys',
    oscA: { unison: 2, detune: 0.03, width: 50 },
    oscB: { enabled: true, volume: -10, detune: 0 },
    env: { attack: 0.002, decay: 1.6, sustain: -6, release: 0.5 },
    filter: { cutoff: 0.55, resonance: 5, drive: 6 },
    character: 'warm',
  },
  'crystal-rain': {
    name: 'kbot - Crystal Rain',
    type: 'pluck',
    oscA: { unison: 2, detune: 0.02, width: 40 },
    oscB: { enabled: true, volume: -12, detune: 0 },
    env: { attack: 0, decay: 0.3, sustain: -50, release: 0.2 },
    filter: { cutoff: 0.45, resonance: 10, drive: 4 },
    character: 'bright',
  },
  'velvet-stab': {
    name: 'kbot - Velvet Stab',
    type: 'chord',
    oscA: { unison: 4, detune: 0.05, width: 60 },
    oscB: { enabled: true, volume: -8, detune: 0.03 },
    env: { attack: 0.003, decay: 0.7, sustain: -5, release: 0.3 },
    filter: { cutoff: 0.58, resonance: 7, drive: 8 },
    character: 'warm',
  },
  'dust-and-haze': {
    name: 'kbot - Dust and Haze',
    type: 'texture',
    oscA: { unison: 16, detune: 0.35, width: 100 },
    oscB: { enabled: true, volume: -3, detune: 0.28 },
    env: { attack: 1.5, decay: 0.1, sustain: -0.5, release: 3.0 },
    filter: { cutoff: 0.28, resonance: 8, drive: 20 },
    character: 'dark',
  },
  'ethereal-dream': {
    name: 'kbot - Ethereal Dream',
    type: 'pad',
    oscA: { unison: 8, detune: 0.20, width: 100 },
    oscB: { enabled: true, volume: -3, detune: 0.15 },
    env: { attack: 2.0, decay: 0.5, sustain: -0.5, release: 5.0 },
    filter: { cutoff: 0.55, resonance: 3, drive: 2 },
    character: 'dreamy',
  },
  'midnight-aurora': {
    name: 'kbot - Midnight Aurora',
    type: 'pad',
    oscA: { unison: 12, detune: 0.25, width: 100 },
    oscB: { enabled: true, volume: -2, detune: 0.20 },
    env: { attack: 3.0, decay: 0.3, sustain: -0.2, release: 6.0 },
    filter: { cutoff: 0.45, resonance: 5, drive: 4 },
    character: 'lush',
  },
  'cloud-cathedral': {
    name: 'kbot - Cloud Cathedral',
    type: 'pad',
    oscA: { unison: 16, detune: 0.30, width: 100 },
    oscB: { enabled: true, volume: -1, detune: 0.22 },
    env: { attack: 4.0, decay: 0.2, sustain: -0.1, release: 8.0 },
    filter: { cutoff: 0.38, resonance: 6, drive: 1 },
    character: 'dreamy',
  },
}

export function registerSerum2PresetTools() {
  registerTool({
    name: 'serum2_preset',
    description: 'List or install Serum 2 presets. Actions: "list" shows available kbot presets, "install" writes all kbot presets to the Serum 2 User folder and verifies each file landed. "create" (custom preset from parameters) is not yet wired to the serializer.',
    parameters: {
      action: { type: 'string', description: '"list", "install", or "create"', required: true },
      preset: { type: 'string', description: 'Preset name for create action (e.g. "emotional-drift")' },
    },
    tier: 'free',
    timeout: 30000,
    async execute(args) {
      const action = String(args.action).toLowerCase()

      if (action === 'list') {
        const lines = ['## kbot Serum 2 Presets', '']
        for (const [id, p] of Object.entries(PRESETS)) {
          lines.push(`- **${p.name}** (${p.type}) — ${p.character}`)
        }
        lines.push('', `Use \`serum2_preset install\` to install all to Serum 2.`)
        return lines.join('\n')
      }

      if (action === 'install') {
        const destDir = getSerumPresetsDir()
        if (!fs.existsSync(destDir)) {
          return `Serum 2 preset folder not found at ${destDir}. Is Serum 2 installed?`
        }
        if (!ensurePresetPackager()) {
          return [
            'Not installed. The .SerumPreset serializer (node-serum2-preset-packager,',
            'XferJson + Zstandard CBOR) is not available, so no files were written.',
            '',
            `Target folder: ${destDir}`,
            `Presets ready to serialize: ${Object.keys(PRESETS).length}`,
            '',
            'Add node-serum2-preset-packager as a dependency to enable install.',
          ].join('\n')
        }

        // Verify before reporting: only presets whose file actually lands on
        // disk are reported installed. A preset that fails to serialize is
        // named as failed, never silently counted as success.
        const { writeSerumPreset } = require('node-serum2-preset-packager')
        const installed: string[] = []
        const failed: string[] = []
        for (const [id, p] of Object.entries(PRESETS)) {
          const dest = path.join(destDir, `kbot - ${p.name}.SerumPreset`)
          try {
            writeSerumPreset(dest, p)
            if (fs.existsSync(dest)) installed.push(p.name)
            else failed.push(`${p.name} (no file written)`)
          } catch (e) {
            failed.push(`${p.name} (${(e as Error).message})`)
          }
        }

        const lines = [`Installed ${installed.length}/${Object.keys(PRESETS).length} presets to Serum 2 > User.`]
        if (installed.length) lines.push('', ...installed.map(n => `  ✓ ${n}`))
        if (failed.length) lines.push('', 'Failed:', ...failed.map(n => `  ✗ ${n}`))
        return lines.join('\n')
      }

      if (action === 'create') {
        return [
          'Not implemented. Custom preset creation from parameters is not wired',
          'to the serializer yet — nothing was written. Use `serum2_preset list`',
          'to see the presets that ship today, or `install` to write those.',
        ].join('\n')
      }

      return 'Unknown action. Use: list, install, or create'
    },
  })
}
