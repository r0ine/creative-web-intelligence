# Performance Budget Engine v6

Complex visual experiences consume bandwidth, GPU, CPU, and memory. Budgets prevent unchecked accumulation.

## Prime rule

**Budgets are per-project, not universal.** A marketing hero for a flagship product has a different budget than an editorial article page. Determine budgets from project type, expected devices, and network assumptions.

Sayısal bütçelerin kaynağı `data/v6/cinematic_profiles.json` içindeki `performance_budget_tiers` alanıdır. Aşağıdaki tablolar bu değerleri açıklar. Bir projede daha düşük bir sınır seçilebilir; katalog sınırını aşmak için katman seçimi ve gerekçesi yeniden değerlendirilir. KB ve MB ondalıktır: 1 KB = 1000 bayt, 1 MB = 1000 KB. Bir sınırın tam üzerindeki değer bütçe içindedir; yalnızca sınırı aşan değer ihlaldir.

## Project tiers

| Tier | Typical project | Initial media | Total page media | GPU expectation |
|:--|:--|:--|:--|:--|
| **Lean** | Editorial, blog, documentation | ≤ 500KB | ≤ 2MB | Integrated GPU / mobile |
| **Standard** | Marketing page, product site | ≤ 1.5MB | ≤ 5MB | Mid-range discrete / recent mobile |
| **Rich** | Product launch, portfolio | ≤ 3MB | ≤ 10MB | Discrete GPU / high-end mobile |
| **Cinematic** | Campaign hero, immersive experience | ≤ 5MB | ≤ 15MB | High-end desktop; mobile gets fallback |

Cinematic tier is rare and must be justified by the brief.

## Budget categories

### Transfer budgets (over the wire)

| Category | Lean | Standard | Rich | Cinematic |
|:--|:--|:--|:--|:--|
| Initial payload (above fold) | 500KB | 1.5MB | 3MB | 5MB |
| Frame sequences total | 0 | 1.5MB | 3MB | 5MB |
| 3D models (GLB) total | 0 | 0 | 2MB | 5MB |
| Textures (KTX2/compressed) | 0 | 0 | 1MB | 3MB |
| Video | 0 | 2MB | 4MB | 8MB |
| Images total | 500KB | 1.5MB | 3MB | 5MB |

`initial_payload_kb`, `total_page_media_mb`, `frame_sequences_kb` ve `glb_kb` katalog sınırlarıdır. Texture transferi, video ve görsel satırları planlama önerisidir; bağımsız ek harcama hakkı vermez. Tüm medya, sayfa toplamına da sığmalıdır. GLB içine gömülü texture dosyalarını sayfa transferinde ikinci kez saymayın. Harici texture dosyaları toplam medya transferine ayrıca eklenir.

### Runtime budgets

| Category | Lean | Standard | Rich | Cinematic |
|:--|:--|:--|:--|:--|
| Decoded image memory | 20MB | 40MB | 80MB | 120MB |
| Texture memory (GPU) | 0 | 0 | 32MB | 64MB |
| Draw calls per frame | 0 | 0 | 30 | 50 |
| Concurrent animations | 1 | 2 | 3 | 4 |
| Frame sequence cache | 0 | 30MB | 60MB | 80MB |
| WebGL contexts | 0 | 0 | 1 | 1 |

`texture_memory_mb`, `draw_calls` ve `concurrent_animations` diğer üç katalog sınırıdır. Sıfır sınırı olan katman, ilgili yükü kabul etmez: Standard veya Lean katmanda gerçek zamanlı 3D bulunamaz. Decoded image memory, frame sequence cache ve WebGL context satırları ek çalışma zamanı denetimleridir; ayrı ölçülür. Sequence başına sınır ile proje toplamı birlikte uygulanır ve daha dar sınır geçerlidir. Örneğin Rich katmanda bir sequence için 4 MB tavanı olsa da tüm sequence dosyaları toplamı 3 MB'yi aşamaz.

### Timing budgets

| Metric | Target | Hard limit |
|:--|:--|:--|
| First Contentful Paint | < 1.5s | 2.5s |
| Largest Contentful Paint | < 2.5s | 4.0s |
| First meaningful 3D frame | < 3s | 5s |
| Frame sequence poster visible | < 1.0s | 1.5s |
| Total Blocking Time | < 200ms | 500ms |
| Cumulative Layout Shift | < 0.1 | 0.25 |

## Downgrade chain

When a visual moment exceeds its budget, downgrade — do not optimize endlessly.

```
real-time 3D
  → pre-rendered frame sequence
    → compressed video (autoplay muted)
      → static image (poster frame / key visual)
```

```
high-fidelity frame sequence (180 frames AVIF)
  → reduced frame sequence (60 frames WebP)
    → compressed video
      → static image
```

```
shader / WebGL effect
  → CSS effect
    → static (no effect)
```

Each step is a valid design outcome, not a failure. The downgrade chain is designed as part of the creative direction, not patched after the fact.

## Mobile budget

Mobile is always **one tier below** desktop, minimum:

- Desktop Rich → Mobile Standard
- Desktop Cinematic → Mobile Rich (or Standard with static fallback for the most expensive moments)
- Desktop Standard → Mobile Lean

Lean, mobilde de Lean kalır. Mobil ölçümler masaüstü bütçesiyle değerlendirilmez. Örneğin Rich masaüstünde çalışan 3D, Standard mobil katmanda fotoğraf, video veya uygun bir sequence ile karşılanır; gerekli ürün kontrolleri HTML üzerinden kullanılabilir kalır.

See `v6/MOBILE_MEDIA_STRATEGY.md`.

## Measurement

Performance is measured, not estimated:

- **Transfer:** Chrome DevTools Network panel, or `performance.getEntriesByType('resource')`.
- **GPU belleği:** Texture boyutları, GPU formatı ve mip seviyeleri üzerinden hesaplayın; geometri ve render target tahsislerini de hesaba katın. `renderer.info.memory` nesne sayılarını verir, MB cinsinden bellek ölçümü değildir. Bu hesapları tahmin olarak etiketleyin.
- **Draw calls:** Three.js `renderer.info.render.calls`.
- **LCP / FCP / TBT:** Lighthouse, Web Vitals.
- **Frame rate:** `requestAnimationFrame` loop measuring frame time. Target: 60fps on desktop, 30fps minimum on mobile.

Ölçülmeyen alan sıfır kabul edilmez. Tahmin, ölçüm ve eksik kanıt ayrı tutulur; ölçüm olmadan bütçenin geçtiği söylenmez. Aşağıdaki çıktı biçimi bir rapor örneğidir. Çalıştırılabilir medya planının giriş ve komut sözleşmesi `tools/v6/README.md` içindedir.

## Output contract

```json
{
  "performance_budget_version": "6.0",
  "project_tier": "rich",
  "budgets": {
    "initial_payload_kb": 3000,
    "total_page_media_mb": 10,
    "frame_sequences_kb": 3000,
    "glb_kb": 2000,
    "texture_memory_mb": 32,
    "draw_calls": 30,
    "concurrent_animations": 3
  },
  "actual_measured": {
    "initial_payload_kb": 870,
    "total_page_media_mb": 4.7,
    "frame_sequences_kb": 2400,
    "glb_kb": 1800,
    "texture_memory_mb": 24,
    "draw_calls": 24,
    "concurrent_animations": 2,
    "lcp_ms": 2100,
    "tbt_ms": 150,
    "frame_rate_desktop_fps": 60,
    "frame_rate_mobile_fps": 42
  },
  "desktop_budget_status": "WITHIN",
  "mobile_tier": "standard",
  "mobile_budget_status": "NOT_MEASURED",
  "downgrade_decisions": [
    { "moment": "hero 3D", "desktop": "realtime Three.js", "mobile": "prerendered 30-frame WebP sequence" }
  ]
}
```
