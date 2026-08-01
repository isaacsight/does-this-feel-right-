#!/usr/bin/env npx tsx
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'
import { z } from 'zod'
import {
  IMAGE_ENGINE, MEDIA_ENGINE, listProductionAssets, paidPost, requestJson, saveLocalImage,
} from './media-production-client.js'

const server = new McpServer({ name: 'kernel-production', version: '1.0.0' })
const ok = (value: unknown) => ({ content: [{ type: 'text' as const, text: JSON.stringify(value, null, 2) }] })
const fail = (error: unknown) => ({
  content: [{ type: 'text' as const, text: error instanceof Error ? error.message : 'Production operation failed' }],
  isError: true,
})
const run = async (operation: () => Promise<unknown>) => {
  try { return ok(await operation()) } catch (error) { return fail(error) }
}

server.tool(
  'production_status',
  'Check the local image and media engines, configured provider access, daily spend state, and tracked jobs. Read-only. Call this before planning a production.',
  {},
  async () => run(async () => {
    const [image, media] = await Promise.allSettled([
      requestJson(`${IMAGE_ENGINE}/health`), requestJson(`${MEDIA_ENGINE}/health`),
    ])
    return {
      image: image.status === 'fulfilled' ? image.value : { ok: false, error: image.reason?.message },
      media: media.status === 'fulfilled' ? media.value : { ok: false, error: media.reason?.message },
      start: { image: 'npm run image-server', media: 'npm run video-server' },
    }
  }),
)

server.tool(
  'production_catalog',
  'Browse available production models. Curated video models are inexpensive to query; catalog categories expose hosted text/image generation choices and pricing metadata. Read-only.',
  {
    category: z.enum(['video-models', 'text-to-video', 'image-to-video', 'text-to-image', 'image-to-image']),
  },
  async ({ category }) => run(async () => category === 'video-models'
    ? requestJson(`${MEDIA_ENGINE}/v1/models`)
    : requestJson(`${MEDIA_ENGINE}/v1/catalog?category=${category}`)),
)

server.tool(
  'production_generate_local_image',
  'Generate an image on this Mac with the local image model and save it under output/images. This is local and has no per-generation API charge. The image engine must be running.',
  {
    prompt: z.string().min(1).max(20_000),
    name: z.string().min(1).max(100).describe('Filesystem-safe deliverable name; unsafe characters are normalized'),
    width: z.number().int().min(512).max(1536).default(1024),
    height: z.number().int().min(512).max(1536).default(1024),
  },
  async ({ prompt, name, width, height }) => run(() => saveLocalImage(prompt, name, width, height)),
)

server.tool(
  'production_quote',
  'Create a signed, short-lived cost quote before any paid generation. This does not spend money. Show the returned USD cost to the user and obtain approval before calling production_submit.',
  {
    kind: z.enum(['video', 'hosted-image', 'voice', 'sound-effect']),
    prompt: z.string().max(20_000).optional(),
    text: z.string().max(100_000).optional(),
    model: z.string().max(200).optional(),
    endpoint: z.string().max(300).optional(),
    imageUrl: z.string().url().optional(),
    durationSeconds: z.number().positive().max(120).optional(),
    provider: z.string().max(100).optional(),
    voice: z.string().max(100).optional(),
    params: z.record(z.string(), z.union([z.string(), z.number(), z.boolean()])).optional(),
  },
  async (args) => run(async () => {
    const routes = {
      video: '/v1/videos/estimate', 'hosted-image': '/v1/images/estimate',
      voice: '/v1/audio/estimate', 'sound-effect': '/v1/audio/sfx/estimate',
    } as const
    const body = args.kind === 'voice' || args.kind === 'sound-effect'
      ? { ...args, text: args.text || args.prompt || '' }
      : args
    const quote = await requestJson(`${MEDIA_ENGINE}${routes[args.kind]}`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body),
    })
    return { kind: args.kind, ...quote, request: body, next: 'Obtain user approval, then pass this exact request and quoteToken to production_submit.' }
  }),
)

server.tool(
  'production_submit',
  'Submit a paid media job only after the user approved the exact quote from production_quote. This spends provider credits and writes the finished asset under output/. Never call speculatively.',
  {
    kind: z.enum(['video', 'hosted-image', 'voice', 'sound-effect']),
    approved: z.literal(true).describe('Affirms that the user approved the quoted cost'),
    quoteToken: z.string().min(20),
    prompt: z.string().max(20_000).optional(),
    text: z.string().max(100_000).optional(),
    model: z.string().max(200).optional(),
    endpoint: z.string().max(300).optional(),
    imageUrl: z.string().url().optional(),
    durationSeconds: z.number().positive().max(120).optional(),
    provider: z.string().max(100).optional(),
    voice: z.string().max(100).optional(),
    params: z.record(z.string(), z.union([z.string(), z.number(), z.boolean()])).optional(),
  },
  async ({ kind, approved: _approved, ...body }) => run(async () => {
    const routes = {
      video: '/v1/videos/generations', 'hosted-image': '/v1/images/fal',
      voice: '/v1/audio/speech', 'sound-effect': '/v1/audio/sfx',
    } as const
    const request = kind === 'voice' || kind === 'sound-effect'
      ? { ...body, text: body.text || body.prompt || '' }
      : body
    const result = await paidPost(routes[kind], request)
    return { kind, ...result, next: 'Poll production_job until status is done, then use the returned local asset URL/path.' }
  }),
)

server.tool(
  'production_job',
  'Poll a submitted image, video, voice, or sound-effect job. Completed jobs return a locally served URL and are persisted under output/. Read-only.',
  { jobId: z.string().uuid() },
  async ({ jobId }) => run(() => requestJson(`${MEDIA_ENGINE}/v1/videos/jobs/${jobId}`)),
)

server.tool(
  'production_assets',
  'List finished local images, video, and audio deliverables under output/, newest first. Read-only.',
  { limit: z.number().int().min(1).max(500).default(100) },
  async ({ limit }) => run(() => listProductionAssets(limit)),
)

await server.connect(new StdioServerTransport())
