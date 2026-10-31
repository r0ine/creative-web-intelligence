import { readdir, readFile, stat } from 'node:fs/promises';
import { resolve, extname, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

function lineAt(source, offset) {
  return source.slice(0, offset).split('\n').length;
}

export function inspectVisualDefaults(css, file = '<style>') {
  const rules = [];
  const withoutComments = css.replace(/\/\*[\s\S]*?\*\//g, match => match.replace(/[^\n]/g, ' '));
  const rulePattern = /([^{}]+)\{([^{}]*)\}/g;
  let match;

  while ((match = rulePattern.exec(withoutComments))) {
    const selector = match[1].trim();
    const declarations = new Map();
    for (const entry of match[2].split(';')) {
      const colon = entry.indexOf(':');
      if (colon < 0) continue;
      declarations.set(entry.slice(0, colon).trim().toLowerCase(), entry.slice(colon + 1).trim().toLowerCase());
    }
    rules.push({ selector, declarations, line: lineAt(css, match.index) });
  }

  const findings = [];
  const add = (rule, code, message) => findings.push({ file, line: rule.line, code, message });
  const boxed = [];
  const fadeUps = [];
  let darkSurface = false;
  let borderCount = 0;

  for (const rule of rules) {
    const get = name => rule.declarations.get(name) ?? '';
    const background = get('background') || get('background-color');
    const border = get('border') || get('border-top') || get('border-bottom') || get('border-left') || get('border-right');
    const rootColors = [...rule.declarations.entries()]
      .filter(([name]) => /^--(?:paper|background|surface|canvas)/.test(name))
      .map(([, value]) => value);
    if (/:root|^body\b|^html\b/.test(rule.selector)
      && [background, ...rootColors].some(value => /#[012][0-9a-f]{5}\b/.test(value))) darkSurface = true;
    if (border && !/^(?:0(?:\s|$)|none\b)/.test(border)) borderCount += 1;

    if (border && background && get('padding') && !get('border-radius')) boxed.push(rule);
    if (get('opacity') === '0' && /translatey\s*\(/.test(get('transform'))) fadeUps.push(rule);
    if (/\ball\b/.test(get('transition'))) add(rule, 'transition-all', 'Tüm özellikleri animasyona bağlama; değişen durumu açıkça seç.');
    if (/\binfinite\b/.test(get('animation') + ' ' + get('animation-iteration-count'))) add(rule, 'infinite-motion', 'Sürekli hareketin bilgi görevi ve durma koşulu olmalı.');
    if ((get('background-clip') === 'text' || get('-webkit-background-clip') === 'text')
      && /gradient\s*\(/.test(background)) add(rule, 'gradient-text', 'Başlığı gradyanla taşımak yerine tipografiyi ve renk kaynağını düzelt.');
    if (/blur\s*\(/.test(get('filter')) && /from|to|\d+%/.test(rule.selector)) add(rule, 'blur-entrance', 'Giriş bulanıklığını ancak odak düzlemi değişiyorsa kullan.');
  }

  if (boxed.length >= 3) add(boxed[0], 'repeated-boxes', `${boxed.length} çerçeveli yüzey aynı biçimde tekrar ediyor; içerik hiyerarşisi ve köşe dilini yeniden incele.`);
  if (fadeUps.length >= 2) add(fadeUps[0], 'repeated-fade-up', 'Birden fazla opacity + translateY girişi var; sayfa genelindeki tekrarları kaldır.');
  if (darkSurface && borderCount >= 5) add(rules[0], 'dark-hairlines', 'Koyu zemin üzerinde çok sayıda çizgi var; yüzey kararını ve çizgilerin görevini yeniden incele.');

  return findings;
}

async function styleFiles(path) {
  const details = await stat(path);
  if (details.isFile()) return [path];
  const entries = await readdir(path, { withFileTypes: true });
  const children = await Promise.all(entries.filter(entry => !entry.name.startsWith('.') && entry.name !== 'node_modules' && !entry.isSymbolicLink())
    .map(entry => styleFiles(resolve(path, entry.name))));
  return children.flat();
}

export async function auditVisualDefaults(path) {
  const files = await styleFiles(resolve(path));
  const findings = [];
  for (const file of files) {
    const extension = extname(file).toLowerCase();
    if (extension !== '.css' && extension !== '.html') continue;
    const content = await readFile(file, 'utf8');
    if (extension === '.css') findings.push(...inspectVisualDefaults(content, relative(process.cwd(), file)));
    else {
      for (const block of content.matchAll(/<style[^>]*>([\s\S]*?)<\/style>/gi)) {
        const offset = lineAt(content, block.index + block[0].indexOf(block[1])) - 1;
        findings.push(...inspectVisualDefaults(block[1], relative(process.cwd(), file))
          .map(finding => ({ ...finding, line: finding.line + offset })));
      }
    }
  }
  return findings;
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const target = process.argv[2];
  if (!target) {
    console.error('Kullanım: node tools/v7/audit_visual_defaults.mjs <site-klasörü>');
    process.exitCode = 2;
  } else {
    try {
      const findings = await auditVisualDefaults(target);
      for (const finding of findings) console.log(`${finding.file}:${finding.line} [${finding.code}] ${finding.message}`);
      console.log(`${findings.length} görsel kalıp incelemesi.`);
      console.log('Kapsam: CSS/HTML içinde transition:all, sonsuz animasyon, gradyan metin, giriş bulanıklığı, eş kutu şablonu, koyu zemin + çok çizgi. Bakmaz: aşmalı eğri (CF-008 → analyze_reference), kontrast, erişilebilirlik, gerçek render. Sıfır bulgu kalite kanıtı değildir.');
      if (findings.length) process.exitCode = 1;
    } catch (error) {
      console.error(error instanceof Error ? error.message : 'Dosyalar okunamadı.');
      process.exitCode = 2;
    }
  }
}
