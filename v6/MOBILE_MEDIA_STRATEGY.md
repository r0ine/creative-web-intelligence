# Mobile Media Strategy v6

Desktop and mobile must NOT automatically use the same cinematic implementation. Mobile is recomposed, not shrunk.

## Decision matrix

| Desktop medium | Mobile options (in order of preference) |
|:--|:--|
| Real-time 3D (interactive) | Mobil katman izin veriyorsa reduced-LOD 3D; aksi halde statik görsel + eşdeğer HTML kontrolleri |
| Real-time 3D (scroll-driven) | Reduced-frame pre-rendered sequence → static key visual |
| 180-frame sequence | 60–80 frame sequence at lower resolution |
| Scroll-controlled video | Statik poster; hareket ve veri tercihi izin veriyorsa kısa, kullanıcı kontrollü video |
| Shader background | CSS gradient or static → nothing |
| Large canvas animation | Reduced-complexity canvas → CSS → static |

## Rules

- Mobil bütçe masaüstünden en az bir katman aşağıdadır; Lean, Lean kalır. Standard ve Lean katmanlarda gerçek zamanlı 3D yoktur. Bkz. [Performance Budget Engine](PERFORMANCE_BUDGET_ENGINE.md).
- Touch replaces hover. Any hover-dependent 3D interaction must have a touch equivalent or be removed.
- Pinned scroll ranges are shorter on mobile (smaller viewports mean less comfortable sticky distance).
- `devicePixelRatio` is not doubled for sequences or textures — frame rate matters more than pixel density on mobile.
- Test on a real mid-range phone (e.g., 2-year-old mid-tier Android), not on the latest flagship.

### Tercih ve hata durumları

| Durum | Beklenen davranış |
|:--|:--|
| `prefers-reduced-motion: reduce` | Poster görünür; scrub, parallax, otomatik hareket ve boş pin mesafesi kaldırılır. |
| `navigator.connection?.saveData === true` | Poster kullanılır; sequence ön yüklemesi ve otomatik video indirmesi başlatılmaz. |
| Veri tercihi API'si yok | Bağlantı hızı bilinmiyor kabul edilir; mobil bütçe uygulanır. |
| Medya yüklenemiyor veya canvas açılamıyor | HTML içerik ve poster sayfada kalır; scroll bekletilmez. |
| Tercih açık sayfada değişiyor | Yeni medya işleri durur; bekleyen sonuçlar eski animasyonu geri açamaz. |

`saveData` desteği her tarayıcıda yoktur; `false` değeri de hızlı bağlantı kanıtı değildir. Bu tabloda poster seçimi kütüphanenin veri tasarrufu politikasıdır. [MDN: saveData](https://developer.mozilla.org/en-US/docs/Web/API/NetworkInformation/saveData)

### Mobil yerleşim

Mobilde metin ve kontroller normal belge akışında kalır. Sticky görsel sığmıyorsa pin kaldırılır; yatay hikâye dikey bölümlere dönüşür. Tarayıcı çubuğu, yön değişimi ve ekran klavyesi kontrolleri örtmemelidir. Ölçüm ve kabul adımları: [Mobile Scroll Recomposition](../scroll/v3_1/MOBILE_SCROLL_RECOMPOSITION.md).

---

# Cinematic Accessibility v6

Every cinematic experience must work without the cinematic part.

## Non-negotiable

### `prefers-reduced-motion`

- **Frame sequences:** show the poster frame. No scrubbing. Optionally, show a static filmstrip of 3–5 key frames.
- **3D animation:** static pose at the final camera position. Model visible, not animated.
- **Scroll-controlled video:** show a static poster frame or the first frame.
- **Shader effects:** disabled; show the content behind them.
- **Auto-playing video:** paused at first frame.
- **Parallax, camera drift, continuous animation:** all disabled.

Tercihi yalnız açılışta okumayın; `matchMedia('(prefers-reduced-motion: reduce)')` değişimini izleyin. Poster moduna geçince medya için ayrılmış uzun scroll alanını da kaldırın. [MDN: prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion)

### Screen readers

- Anlam taşıyan statik canvas görseline `role="img"` ve açıklayıcı `aria-label` verin. Aynı bilgiyi HTML zaten açıklıyorsa yinelenen dekoratif canvas `aria-hidden="true"` olabilir; içinde odaklanabilir kontrol bulunmaz.
- No essential content exists only inside animation/video/3D. All text is HTML.
- Interactive 3D controls get `aria-label` descriptions.

### Keyboard

- PageDown, PageUp, Space, Home ve End sayfanın doğal kaydırmasını sürdürür. Animasyon tamamlanmadan bölümden çıkma engellenmez; odak sırası belge sırasını izler.
- Etkileşimli 3D için klavyeyle çalışan kontroller veya aynı işlemleri sunan HTML arayüz sağlayın. Etiket eklemek kontrolü erişilebilir yapmaz; işlevi olan sahne erişim eksikliğini gizlemek için dekoratif sayılamaz. [W3C: Keyboard](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html)

### Flashing

- No more than three flashes per second (WCAG 2.3.1).
- Frame sequences with rapid light changes must be reviewed frame-by-frame.

### Essential information

> If content exists only inside an animation, video, or 3D scene, the architecture is wrong.

HTML carries content. Media illustrates and enhances. This is not a guideline — it is a structural requirement.

---

# Scroll Experience Director v6

Upgrades the existing scroll system (`directors/scroll/SCROLL_DIRECTOR.md`) with cinematic medium awareness.

## Scroll modes

| Mode | Description | Default? |
|:--|:--|:--|
| **Normal document scroll** | Content flows naturally. The default and most common. | Yes |
| **Scroll-triggered event** | An element changes state when it enters/exits viewport. | Selective |
| **Scroll-scrubbed animation** | İlerleme scroll konumuna bağlanır; pin zorunlu değildir. | Rare |
| **Sticky storytelling** | A pinned visual updates as the user scrolls through text/chapters beside it. | Rare |
| **Frame sequence** | Canvas karesi scroll ilerlemesine bağlanır; mesafe anlatı ve kare sayısına göre seçilir. | Rare |
| **Camera progression** | Kamera scroll ilerlemesine bağlanır; normal akışta veya gerekçeli sticky sahnede çalışır. | Rare |
| **Horizontal scroll** | Content moves horizontally within a pinned container. Use with extreme caution. | Very rare |

### Native scroll is the default

Never hijack scrolling. Native scroll behavior is correct until proven otherwise. Pinned sequences, scroll-scrubbed animations, and horizontal scroll are exceptions that must be justified by narrative purpose.

### Pinned section limits

- Maximum one pinned section per page (rare: two with strong justification).
- Pinned scroll range should not exceed 400vh (desktop) or 300vh (mobile).
- Between pinned sections, at least one full viewport of flowing content.
- Rest zones (v5) apply: after an intense scroll experience, the next section is calm.

Bu değerler kütüphanenin tasarım sınırlarıdır. Mesafe ölçüsünü açık yazın: `scroll_duration_vh: 300`, üç viewport yüksekliği kadar **hareket mesafesidir**; sticky sahnenin kendi yüksekliği bu mesafeye ayrıca eklenir. Mobil varsayılan normal akıştır; 300vh hedef değildir.

### Scroll technology selection

| Need | Technology |
|:--|:--|
| Simple in-view triggers | `IntersectionObserver` (native) |
| Scroll progress for CSS | `animation-timeline: scroll()` (native, progressive enhancement) |
| Complex timelines with pinning | GSAP ScrollTrigger |
| Programatik kaydırma veya bölüm bağlantısı | İsteğe bağlı CSS `scroll-behavior: smooth`; reduced-motion durumunda `auto` |
| Özel scroll fiziği | Lenis, yalnız gerekçeli ve mobil/klavye davranışı ayrıca doğrulanmışsa |
| 3D camera mapping | Custom scroll-to-progress → Three.js camera lerp |
| Frame sequence mapping | Custom scroll-to-progress → canvas drawImage |

Tek bir görünürlük tetikleyicisi için GSAP gerekmez. CSS `scroll-behavior`, dokunma veya tekerlek girdisine özel fizik eklemez; bağlantı ve programatik kaydırmanın davranışını seçer.

---

# Implementation Intelligence v6

The library knows WHEN to use each technology. Technology follows the design requirement.

| Need | First choice | When to upgrade |
|:--|:--|:--|
| Simple hover/focus transition | CSS transition | — |
| State animation (toggle, tab) | CSS animation or Web Animations API | Complex choreography → GSAP |
| Scroll in-view trigger | `IntersectionObserver` | — |
| Scroll-mapped animation | `animation-timeline: scroll()` | Browser support gap → GSAP ScrollTrigger |
| Authored vector animation | Lottie (dotLottie) | Interactive state machine → Rive |
| Interactive state animation | Rive | — |
| Frame sequence canvas | Vanilla JS + `<canvas>` | — |
| Single model viewer | `<model-viewer>` | Custom camera/interaction → Three.js |
| Custom 3D scene | Three.js | React project with 3D state → R3F |
| Data visualization | D3 + SVG | Real-time particles/large datasets → Canvas/WebGL |
| Smooth scrolling | CSS `scroll-behavior: smooth` | Physics-based → Lenis |
| Custom shader effect | Three.js ShaderMaterial | Compute-heavy → WebGPU (progressive) |

**Rule:** do not install a library for one use. If the project needs a single GSAP tween, use CSS. If it needs a full scroll timeline with pinning, GSAP earns its place.

---

# Media Storyboard v6

Before implementing complex media, create an internal storyboard. This prevents random effects.

## For each major visual moment, define:

```json
{
  "moment_id": "hero-product-reveal",
  "purpose": "content — show the product assembling from components",
  "medium": "pre-rendered 3D frame sequence",
  "start_state": "components separated in exploded view",
  "end_state": "assembled product in hero framing",
  "user_control": "scroll scrub forward/backward",
  "scroll_relationship": "pinned canvas over 350vh scroll range",
  "camera_choreography": "approach + orbit 60° + settle",
  "desktop_spec": "120 frames AVIF 1920w",
  "mobile_spec": "50 frames WebP 960w",
  "fallback": "static poster of assembled product",
  "reduced_motion": "poster frame only",
  "performance_cost": {
    "transfer_kb": 2400,
    "decoded_memory_mb": 45,
    "gpu_impact": "ölçülmedi; Canvas 2D çizim ve birleştirme maliyeti tarayıcıya bağlı"
  },
  "rest_zone_after": true,
  "accessibility": {
    "aria_label": "Product assembly animation showing components coming together",
    "essential_text_in_media": false,
    "keyboard_scrollable": true
  }
}
```

Every complex visual moment gets a storyboard entry before implementation begins. If the storyboard entry cannot justify the medium, the medium downgrades or the moment is removed.

---

# Asset Pipeline v6

Standardized directory structure for project assets:

```
assets/
  images/
    editorial/       — curated photography and illustrations
    product/         — product shots, screenshots
    generated/       — AI-generated originals (with provenance)
    icons/           — SVG icon set
  video/
    source/          — raw/original video files
    optimized/       — web-compressed versions
    posters/         — poster frames for each video
  sequences/
    {name}/          — one directory per frame sequence
      manifest.json  — frame count, formats, dimensions, loading strategy
      poster.avif    — poster frame
      frame-{n}.avif — individual frames
      mobile/        — mobile-resolution variant
  models/
    source/          — original Blender/FBX/OBJ files
    optimized/       — web-ready GLB files
    textures/        — compressed textures (KTX2, WebP)
    provenance.json  — source, license, optimization status per model
  animations/
    lottie/          — .lottie / .json Lottie files
    rive/            — .riv Rive files
  shaders/           — GLSL/WGSL shader files
```

### Provenance manifest

Every asset directory includes a provenance file:

```json
{
  "assets": [
    {
      "filename": "hero-product.glb",
      "source": "custom-modeled in Blender from client CAD",
      "license": "project-owned",
      "optimization": "draco compressed, textures KTX2, 87K triangles",
      "mobile_variant": "hero-product-mobile.glb (reduced LOD, 32K triangles)",
      "fallback": "hero-product-poster.avif",
      "estimated_cost_kb": 1800,
      "created": "2026-09-01",
      "last_optimized": "2026-09-10"
    }
  ]
}
```
