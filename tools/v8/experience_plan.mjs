import { readFile, writeFile } from 'node:fs/promises';
import { buildExperiencePlan } from '../../runtime/media/experience-plan.mjs';

function asMarkdown(plan) {
  const lines = [
    '# Deneyim planı', '', `Amaç: ${plan.goal}`, '',
    '## Video olmadan tamamlanacak temel', '',
    ...plan.base.map(item => `- ${item}`), '',
    '## Etkileşim', '',
    `- Masaüstü: ${plan.interaction.desktop}`,
    `- Mobil: ${plan.interaction.mobile}`,
    `- Hareket sahibi: ${plan.interaction.owner}`, '',
    '## Video kararı', '',
    `Durum: ${plan.video.status}`, '',
  ];
  if (plan.video.integration) lines.push(plan.video.integration, '');
  if (plan.video.prompt) lines.push('### Üretim aracına verilecek prompt', '', plan.video.prompt, '');
  if (plan.questions.length) lines.push('## Kullanıcıya sor', '', ...plan.questions.map(item => `- ${item}`), '');
  lines.push('## Bitirme koşulu', '', plan.finish, '');
  return lines.join('\n');
}

async function main() {
  const [briefPath, outputPath, format = 'markdown'] = process.argv.slice(2);
  if (!briefPath || !['markdown', 'json'].includes(format) || process.argv.slice(2).length > 3) {
    throw new Error('Kullanım: node tools/v8/experience_plan.mjs brief.json [yeni-çıktı.md] [markdown|json]');
  }
  const brief = JSON.parse(await readFile(briefPath, 'utf8'));
  const plan = buildExperiencePlan(brief);
  const output = format === 'json' ? JSON.stringify(plan, null, 2) + '\n' : asMarkdown(plan);
  if (outputPath) await writeFile(outputPath, output, { encoding: 'utf8', flag: 'wx' });
  else console.log(output);
}

main().catch(error => { console.error(error.message); process.exitCode = 2; });
