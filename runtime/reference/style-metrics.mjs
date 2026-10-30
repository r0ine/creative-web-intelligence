const RGB = /^rgba?\(\s*([\d.]+)[\s,]+([\d.]+)[\s,]+([\d.]+)(?:\s*[,/]\s*([\d.]+%?))?\s*\)$/i;

export function parseColor(value) {
  const match = RGB.exec(String(value ?? '').trim());
  if (!match) return null;
  const alphaText = match[4];
  const alpha = alphaText === undefined ? 1 : alphaText.endsWith('%') ? Number.parseFloat(alphaText) / 100 : Number(alphaText);
  return { r: Math.round(Number(match[1])), g: Math.round(Number(match[2])), b: Math.round(Number(match[3])), a: alpha };
}

export function toHex({ r, g, b }) {
  return `#${[r, g, b].map(channel => Math.max(0, Math.min(255, channel)).toString(16).padStart(2, '0')).join('')}`;
}

function linear(channel) {
  const value = channel / 255;
  return value <= 0.03928 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4;
}

export function relativeLuminance({ r, g, b }) {
  return 0.2126 * linear(r) + 0.7152 * linear(g) + 0.0722 * linear(b);
}

export function contrastRatio(first, second) {
  const [light, dark] = [relativeLuminance(first), relativeLuminance(second)].sort((a, b) => b - a);
  return (light + 0.05) / (dark + 0.05);
}

export function chroma({ r, g, b }) {
  return Math.max(r, g, b) - Math.min(r, g, b);
}

/** Alan ağırlıklı palet: ekranda en çok yer kaplayan renkler ve nötr/destek/vurgu alan oranı. */
export function areaPalette(samples, limit = 10) {
  const totals = new Map();
  let total = 0;
  for (const { color, area } of samples) {
    const parsed = typeof color === 'string' ? parseColor(color) : color;
    if (!parsed || parsed.a < 0.5 || !(area > 0)) continue;
    const hex = toHex(parsed);
    const entry = totals.get(hex) ?? { color: parsed, area: 0 };
    entry.area += area;
    totals.set(hex, entry);
    total += area;
  }
  const plan = { neutral: 0, support: 0, accent: 0 };
  if (!total) return { colors: [], plan };
  const colors = [...totals].sort((a, b) => b[1].area - a[1].area)
    .map(([hex, { color, area }]) => ({ hex, share: area / total, chroma: chroma(color) }));
  for (const { share, chroma: value } of colors) {
    plan[value < 25 ? 'neutral' : value < 90 ? 'support' : 'accent'] += share;
  }
  return { colors: colors.slice(0, limit).map(({ hex, share }) => ({ hex, share })), plan };
}

export function isLargeText(fontSizePx, fontWeight) {
  return fontSizePx >= 24 || (fontSizePx >= 18.66 && Number(fontWeight) >= 700);
}

/** WCAG AA: normal metin 4.5:1, büyük metin 3:1. */
export function contrastFindings(samples) {
  const findings = [];
  for (const sample of samples) {
    const fg = parseColor(sample.color);
    const bg = parseColor(sample.background);
    if (!fg || !bg) continue;
    const ratio = contrastRatio(fg, bg);
    const required = isLargeText(sample.fontSize, sample.fontWeight) ? 3 : 4.5;
    if (ratio < required) {
      findings.push({ ...sample, foreground: toHex(fg), backgroundHex: toHex(bg), ratio: Math.round(ratio * 100) / 100, required });
    }
  }
  return findings.sort((a, b) => a.ratio - b.ratio);
}

/** Fark haritasını bölgelere ayırır; satır 0 genelde menü ve ilk ekrana denk gelir. */
export function diffRegions(heatmap, width, height, rows = 3, columns = 3) {
  if (heatmap.length !== width * height * 4) throw new RangeError('Isı haritası ölçüsü uyuşmuyor.');
  const cells = Array.from({ length: rows * columns }, () => ({ different: 0, total: 0 }));
  for (let y = 0; y < height; y += 1) {
    const row = Math.min(rows - 1, Math.floor(y * rows / height));
    for (let x = 0; x < width; x += 1) {
      const cell = cells[row * columns + Math.min(columns - 1, Math.floor(x * columns / width))];
      cell.total += 1;
      if (heatmap[(y * width + x) * 4 + 3] > 0) cell.different += 1;
    }
  }
  const vertical = ['üst', 'orta', 'alt'];
  const horizontal = ['sol', 'orta', 'sağ'];
  return cells.map((cell, index) => ({
    row: Math.floor(index / columns),
    column: index % columns,
    label: rows === 3 && columns === 3 ? `${vertical[Math.floor(index / columns)]} ${horizontal[index % columns]}` : `${Math.floor(index / columns)}-${index % columns}`,
    percent: cell.total ? cell.different / cell.total * 100 : 0,
  })).sort((a, b) => b.percent - a.percent);
}
