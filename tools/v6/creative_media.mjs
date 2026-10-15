import { readFile, writeFile } from 'node:fs/promises';
import { buildVideoPrompts } from '../../runtime/media/video-prompt.mjs';
import { selectCreativeSources } from '../../runtime/media/source-selection.mjs';

async function main() {
  const [command, ...args] = process.argv.slice(2);
  if (command === 'sources') {
    if (args.length > 3) throw new Error('Kullanım: sources [rol] [react|vanilla] [project|library]');
    const catalog = JSON.parse(await readFile(new URL('../../data/v6/creative_sources.json', import.meta.url), 'utf8'));
    console.log(JSON.stringify(selectCreativeSources(catalog, { role: args[0], framework: args[1], scope: args[2] }), null, 2));
    return;
  }
  if (command === 'prompt' && args.length >= 1 && args.length <= 2) {
    const brief = JSON.parse(await readFile(args[0], 'utf8'));
    const prompts = buildVideoPrompts(brief);
    const output = `# Video brief’i\n\n## ChatGPT’ye ver\n\n${prompts.chatgpt}\n\n## Teslim ayarları\n\n${JSON.stringify(prompts.delivery, null, 2)}\n`;
    if (args[1]) await writeFile(args[1], output, { encoding: 'utf8', flag: 'wx' });
    else console.log(output);
    return;
  }
  throw new Error('Kullanım: node tools/v6/creative_media.mjs sources [rol] [react|vanilla] [project|library]\n         node tools/v6/creative_media.mjs prompt brief.json [yeni-prompt.md]');
}

main().catch(error => { console.error(error.message); process.exitCode = 2; });
