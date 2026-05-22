import fs from 'fs';
import path from 'path';
import yaml from 'js-yaml';

const workspaceRoot = process.cwd();
const ymlFolder = process.argv[2] || path.join(workspaceRoot, 'content-drupal');
const pagesRoot = path.join(workspaceRoot, 'src', 'pages');

function normalizeRoute(url) {
  if (!url || typeof url !== 'string') return [];
  const clean = url.replace(/^\/+|\/+$/g, '');
  return clean === '' ? [] : clean.split('/').filter(Boolean);
}

function safeImportPath(depth) {
  return '../'.repeat(depth + 1) + 'components/Layout.astro';
}

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function getYamlFiles(folder) {
  return fs.readdirSync(folder).filter((name) => name.endsWith('.yml') || name.endsWith('.yaml'));
}

function toPageFile(routeParts) {
  const pageDir = path.join(pagesRoot, ...routeParts);
  ensureDir(pageDir);
  return path.join(pageDir, 'index.astro');
}

function stripScriptTags(html) {
  return html.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, '');
}

function getBody(entry) {
  if (!entry?.custom_fields?.body) return '';
  const bodyArray = entry.custom_fields.body;
  if (!Array.isArray(bodyArray) || bodyArray.length === 0) return '';
  const raw = bodyArray[0]?.value || '';
  return stripScriptTags(raw);
}

function getTitle(entry) {
  return entry?.base_fields?.title || entry?.base_fields?.name || 'Untitled Page';
}

function getUrl(entry) {
  return entry?.base_fields?.url || entry?.base_fields?.path || '';
}

async function run() {
  const files = getYamlFiles(ymlFolder);
  if (!files.length) {
    console.error('No YAML files found in', ymlFolder);
    process.exit(1);
  }

  let generated = 0;
  for (const file of files) {
    const filePath = path.join(ymlFolder, file);
    const raw = fs.readFileSync(filePath, 'utf8');
    const entry = yaml.load(raw);
    if (!entry || !entry.base_fields) continue;
    if (!entry.base_fields.status) continue;

    const url = getUrl(entry);
    const routeParts = normalizeRoute(url);
    if (!routeParts.length) {
      console.warn(`Skipping page with empty URL: ${file}`);
      continue;
    }

    const pageFile = toPageFile(routeParts);
    if (fs.existsSync(pageFile)) {
      console.log(`Skipping existing page: ${pageFile}`);
      continue;
    }

    const depth = routeParts.length;
    const importPath = safeImportPath(depth);
    const title = getTitle(entry);
    const body = getBody(entry);

    const pageContents = `---\nimport Layout from '${importPath}';\nconst title = ${JSON.stringify(title)};\nconst body = ${JSON.stringify(body)};\n---\n<Layout title={title}>\n  <div set:html={body} />\n</Layout>\n`;
    fs.writeFileSync(pageFile, pageContents, 'utf8');
    generated += 1;
  }

  console.log(`Generated ${generated} Astro page(s) from YAML exports.`);
}

run().catch((err) => {
  console.error(err);
  process.exit(1);
});
