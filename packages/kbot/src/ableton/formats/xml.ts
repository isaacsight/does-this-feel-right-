/**
 * xml.ts — small, tolerant XML DOM for Ableton file formats.
 *
 * Ableton's .als / .adg / .adv files are gzip-compressed XML with a very
 * regular shape: elements, attributes, no mixed content, values carried in
 * `Value="..."` attributes. This module parses that dialect (and ordinary
 * XML) into a plain-object tree, lets callers query and patch it, and
 * serialises it back with Live's own conventions (tab indentation,
 * `<Tag Value="x" />` self-closing forms, single-quoted attributes when the
 * value contains a double quote — which is what Live emits for JSON blobs).
 *
 * Node stdlib only. No external dependency.
 */

export interface XmlNode {
  tag: string;
  attrs: Record<string, string>;
  children: XmlNode[];
  /** Only set on text nodes (tag === '#text'). */
  text?: string;
}

export interface XmlDoc {
  /** e.g. `<?xml version="1.0" encoding="UTF-8"?>` (without trailing newline). */
  declaration?: string;
  root: XmlNode;
}

export const TEXT_TAG = '#text';

// ---------------------------------------------------------------------------
// Entities
// ---------------------------------------------------------------------------

const NAMED_ENTITIES: Record<string, string> = {
  amp: '&',
  lt: '<',
  gt: '>',
  quot: '"',
  apos: "'",
};

export function decodeEntities(s: string): string {
  if (s.indexOf('&') === -1) return s;
  return s.replace(/&(#x[0-9a-fA-F]+|#[0-9]+|[a-zA-Z]+);/g, (m, body: string) => {
    if (body[0] === '#') {
      const code = body[1] === 'x' || body[1] === 'X'
        ? parseInt(body.slice(2), 16)
        : parseInt(body.slice(1), 10);
      if (Number.isFinite(code)) {
        try {
          return String.fromCodePoint(code);
        } catch {
          return m;
        }
      }
      return m;
    }
    const v = NAMED_ENTITIES[body];
    return v === undefined ? m : v;
  });
}

function escapeText(s: string): string {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

/** Returns the attribute rendered with a quote style Live would pick. */
function renderAttr(name: string, value: string): string {
  const base = value.replace(/&/g, '&amp;').replace(/</g, '&lt;');
  if (value.indexOf('"') !== -1 && value.indexOf("'") === -1) {
    return `${name}='${base}'`;
  }
  return `${name}="${base.replace(/"/g, '&quot;')}"`;
}

// ---------------------------------------------------------------------------
// Parser
// ---------------------------------------------------------------------------

export class XmlParseError extends Error {
  constructor(message: string, public readonly offset: number) {
    super(`${message} (at offset ${offset})`);
    this.name = 'XmlParseError';
  }
}

function isNameChar(c: number): boolean {
  // letters, digits, '_', ':', '-', '.'
  return (
    (c >= 65 && c <= 90) ||
    (c >= 97 && c <= 122) ||
    (c >= 48 && c <= 57) ||
    c === 95 || c === 58 || c === 45 || c === 46 ||
    c > 127
  );
}

function isSpace(c: number): boolean {
  return c === 32 || c === 9 || c === 10 || c === 13;
}

/**
 * Parse an XML string into a document tree. Tolerant of:
 *  - single- or double-quoted attribute values,
 *  - unquoted attribute values (`a=b`),
 *  - comments, CDATA, processing instructions, DOCTYPE,
 *  - a BOM.
 * Whitespace-only text between elements is dropped (Live never emits
 * significant whitespace); other text is kept as `#text` nodes.
 */
export function parseXml(src: string): XmlDoc {
  let i = 0;
  const n = src.length;
  if (src.charCodeAt(0) === 0xfeff) i = 1;

  let declaration: string | undefined;
  const rootHolder: XmlNode = { tag: '#document', attrs: {}, children: [] };
  const stack: XmlNode[] = [rootHolder];

  const flushText = (start: number, end: number) => {
    if (end <= start) return;
    const raw = src.slice(start, end);
    // fast whitespace check
    let ws = true;
    for (let k = 0; k < raw.length; k++) {
      if (!isSpace(raw.charCodeAt(k))) { ws = false; break; }
    }
    if (ws) return;
    const parent = stack[stack.length - 1];
    parent.children.push({ tag: TEXT_TAG, attrs: {}, children: [], text: decodeEntities(raw) });
  };

  while (i < n) {
    const lt = src.indexOf('<', i);
    if (lt === -1) {
      flushText(i, n);
      break;
    }
    flushText(i, lt);
    i = lt;

    // Which construct?
    if (src.startsWith('<?', i)) {
      const end = src.indexOf('?>', i + 2);
      if (end === -1) throw new XmlParseError('unterminated processing instruction', i);
      const pi = src.slice(i, end + 2);
      if (/^<\?xml[\s?]/i.test(pi) && declaration === undefined) declaration = pi;
      i = end + 2;
      continue;
    }
    if (src.startsWith('<!--', i)) {
      const end = src.indexOf('-->', i + 4);
      if (end === -1) throw new XmlParseError('unterminated comment', i);
      i = end + 3;
      continue;
    }
    if (src.startsWith('<![CDATA[', i)) {
      const end = src.indexOf(']]>', i + 9);
      if (end === -1) throw new XmlParseError('unterminated CDATA', i);
      const parent = stack[stack.length - 1];
      parent.children.push({ tag: TEXT_TAG, attrs: {}, children: [], text: src.slice(i + 9, end) });
      i = end + 3;
      continue;
    }
    if (src.startsWith('<!', i)) {
      // DOCTYPE or other declaration: skip to matching '>' (handles one nesting level of [ ])
      let depth = 0;
      let k = i + 2;
      for (; k < n; k++) {
        const c = src.charCodeAt(k);
        if (c === 91) depth++;          // [
        else if (c === 93) depth--;     // ]
        else if (c === 62 && depth <= 0) break; // >
      }
      if (k >= n) throw new XmlParseError('unterminated declaration', i);
      i = k + 1;
      continue;
    }
    if (src.startsWith('</', i)) {
      const end = src.indexOf('>', i + 2);
      if (end === -1) throw new XmlParseError('unterminated closing tag', i);
      const name = src.slice(i + 2, end).trim();
      const top = stack[stack.length - 1];
      if (stack.length === 1 || top.tag !== name) {
        throw new XmlParseError(`mismatched closing tag </${name}> (open element is <${top.tag}>)`, i);
      }
      stack.pop();
      i = end + 1;
      continue;
    }

    // Opening tag
    let k = i + 1;
    const nameStart = k;
    while (k < n && isNameChar(src.charCodeAt(k))) k++;
    if (k === nameStart) throw new XmlParseError('expected element name', i);
    const tag = src.slice(nameStart, k);
    const attrs: Record<string, string> = {};
    let selfClosing = false;
    // attributes
    for (;;) {
      while (k < n && isSpace(src.charCodeAt(k))) k++;
      if (k >= n) throw new XmlParseError(`unterminated start tag <${tag}>`, i);
      const c = src.charCodeAt(k);
      if (c === 62) { // >
        k++;
        break;
      }
      if (c === 47) { // /
        if (src.charCodeAt(k + 1) !== 62) throw new XmlParseError(`expected '>' after '/' in <${tag}>`, k);
        selfClosing = true;
        k += 2;
        break;
      }
      const anStart = k;
      while (k < n && isNameChar(src.charCodeAt(k))) k++;
      if (k === anStart) throw new XmlParseError(`bad attribute in <${tag}>`, k);
      const aname = src.slice(anStart, k);
      while (k < n && isSpace(src.charCodeAt(k))) k++;
      if (src.charCodeAt(k) !== 61) { // '=' missing: boolean attribute (tolerated)
        attrs[aname] = '';
        continue;
      }
      k++;
      while (k < n && isSpace(src.charCodeAt(k))) k++;
      const q = src.charCodeAt(k);
      if (q === 34 || q === 39) {
        const close = src.indexOf(String.fromCharCode(q), k + 1);
        if (close === -1) throw new XmlParseError(`unterminated attribute value for ${aname}`, k);
        attrs[aname] = decodeEntities(src.slice(k + 1, close));
        k = close + 1;
      } else {
        const vs = k;
        while (k < n) {
          const cc = src.charCodeAt(k);
          if (isSpace(cc) || cc === 62 || cc === 47) break;
          k++;
        }
        attrs[aname] = decodeEntities(src.slice(vs, k));
      }
    }
    const node: XmlNode = { tag, attrs, children: [] };
    stack[stack.length - 1].children.push(node);
    if (!selfClosing) stack.push(node);
    i = k;
  }

  if (stack.length !== 1) {
    throw new XmlParseError(`unclosed element <${stack[stack.length - 1].tag}>`, n);
  }
  const roots = rootHolder.children.filter((c) => c.tag !== TEXT_TAG);
  if (roots.length !== 1) {
    throw new XmlParseError(`expected exactly one root element, found ${roots.length}`, 0);
  }
  return { declaration, root: roots[0] };
}

// ---------------------------------------------------------------------------
// Serializer
// ---------------------------------------------------------------------------

export interface SerializeOptions {
  /** Indent unit. Live uses a tab. */
  indent?: string;
  /** Emit the XML declaration (default: the doc's own, else the standard one). */
  declaration?: string | false;
  /** Newline. Live uses "\n". */
  newline?: string;
}

const DEFAULT_DECLARATION = '<?xml version="1.0" encoding="UTF-8"?>';

export function serializeXml(input: XmlDoc | XmlNode, opts: SerializeOptions = {}): string {
  const indent = opts.indent ?? '\t';
  const nl = opts.newline ?? '\n';
  const isDoc = (input as XmlDoc).root !== undefined && (input as XmlNode).tag === undefined;
  const root = isDoc ? (input as XmlDoc).root : (input as XmlNode);
  const parts: string[] = [];
  let decl: string | false | undefined = opts.declaration;
  if (decl === undefined) decl = isDoc ? ((input as XmlDoc).declaration ?? DEFAULT_DECLARATION) : false;
  if (decl) parts.push(decl + nl);
  writeNode(root, 0, parts, indent, nl);
  return parts.join('');
}

function writeNode(node: XmlNode, depth: number, out: string[], indent: string, nl: string): void {
  const pad = indent.repeat(depth);
  if (node.tag === TEXT_TAG) {
    out.push(pad + escapeText(node.text ?? '') + nl);
    return;
  }
  let open = pad + '<' + node.tag;
  for (const k of Object.keys(node.attrs)) open += ' ' + renderAttr(k, node.attrs[k]);
  if (node.children.length === 0) {
    out.push(open + ' />' + nl);
    return;
  }
  // Single text child: inline it (ordinary XML style).
  if (node.children.length === 1 && node.children[0].tag === TEXT_TAG) {
    out.push(open + '>' + escapeText(node.children[0].text ?? '') + '</' + node.tag + '>' + nl);
    return;
  }
  out.push(open + '>' + nl);
  for (const c of node.children) writeNode(c, depth + 1, out, indent, nl);
  out.push(pad + '</' + node.tag + '>' + nl);
}

// ---------------------------------------------------------------------------
// Tree helpers
// ---------------------------------------------------------------------------

export function el(tag: string, attrs: Record<string, string> = {}, children: XmlNode[] = []): XmlNode {
  return { tag, attrs: { ...attrs }, children };
}

/** `<Tag Value="v" />` — the most common Live leaf. */
export function valueEl(tag: string, value: string | number | boolean): XmlNode {
  return { tag, attrs: { Value: fmt(value) }, children: [] };
}

export function fmt(v: string | number | boolean): string {
  if (typeof v === 'boolean') return v ? 'true' : 'false';
  if (typeof v === 'number') return Number.isInteger(v) ? String(v) : String(v);
  return v;
}

export function clone(node: XmlNode): XmlNode {
  const c: XmlNode = { tag: node.tag, attrs: { ...node.attrs }, children: node.children.map(clone) };
  if (node.text !== undefined) c.text = node.text;
  return c;
}

export function elements(node: XmlNode): XmlNode[] {
  return node.children.filter((c) => c.tag !== TEXT_TAG);
}

export function child(node: XmlNode | undefined, tag: string): XmlNode | undefined {
  if (!node) return undefined;
  for (const c of node.children) if (c.tag === tag) return c;
  return undefined;
}

export function childrenOf(node: XmlNode | undefined, tag: string): XmlNode[] {
  if (!node) return [];
  return node.children.filter((c) => c.tag === tag);
}

/** Path lookup with '/' separators; each step is a tag name (first match). */
export function find(node: XmlNode | undefined, path: string): XmlNode | undefined {
  let cur = node;
  for (const step of path.split('/')) {
    if (!step) continue;
    cur = child(cur, step);
    if (!cur) return undefined;
  }
  return cur;
}

/** All matches for the last step of a path (earlier steps: first match). */
export function findAll(node: XmlNode | undefined, path: string): XmlNode[] {
  const steps = path.split('/').filter(Boolean);
  if (steps.length === 0) return node ? [node] : [];
  const parent = steps.length === 1 ? node : find(node, steps.slice(0, -1).join('/'));
  return childrenOf(parent, steps[steps.length - 1]);
}

/** Read the `Value` attribute at `path` (or of `node` itself when path is omitted). */
export function value(node: XmlNode | undefined, path?: string): string | undefined {
  const t = path === undefined ? node : find(node, path);
  return t?.attrs.Value;
}

export function numberValue(node: XmlNode | undefined, path?: string): number | undefined {
  const v = value(node, path);
  if (v === undefined) return undefined;
  const n = Number(v);
  return Number.isFinite(n) ? n : undefined;
}

export function boolValue(node: XmlNode | undefined, path?: string): boolean | undefined {
  const v = value(node, path);
  if (v === undefined) return undefined;
  return v === 'true';
}

/** Set (or create along the way) the `Value` attribute at `path`. */
export function setValue(node: XmlNode, path: string, v: string | number | boolean): XmlNode {
  const target = ensure(node, path);
  target.attrs.Value = fmt(v);
  return target;
}

/** Ensure the element at `path` exists (creating empty elements as needed). */
export function ensure(node: XmlNode, path: string): XmlNode {
  let cur = node;
  for (const step of path.split('/')) {
    if (!step) continue;
    let next = child(cur, step);
    if (!next) {
      next = el(step);
      cur.children.push(next);
    }
    cur = next;
  }
  return cur;
}

export function removeChildren(node: XmlNode, predicate?: (c: XmlNode) => boolean): void {
  if (!predicate) {
    node.children.length = 0;
    return;
  }
  node.children = node.children.filter((c) => !predicate(c));
}

/** Depth-first walk (pre-order). Return false from fn to skip a subtree. */
export function walk(node: XmlNode, fn: (n: XmlNode, parent: XmlNode | undefined, depth: number) => void | boolean, parent?: XmlNode, depth = 0): void {
  const r = fn(node, parent, depth);
  if (r === false) return;
  for (const c of node.children) walk(c, fn, node, depth + 1);
}

/** Collect the set of tag paths (relative to `node`) — handy for structural comparisons in tests. */
export function tagPaths(node: XmlNode, maxDepth = Infinity): Set<string> {
  const out = new Set<string>();
  const rec = (n: XmlNode, prefix: string, depth: number) => {
    for (const c of n.children) {
      if (c.tag === TEXT_TAG) continue;
      const p = prefix + '/' + c.tag;
      out.add(p);
      if (depth < maxDepth) rec(c, p, depth + 1);
    }
  };
  rec(node, '', 1);
  return out;
}
