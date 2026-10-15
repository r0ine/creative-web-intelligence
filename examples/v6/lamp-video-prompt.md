# Video brief’i

## ChatGPT’ye ver

Aşağıdaki brief için web sitesinde kullanılacak 3D video hazırla. Bu oturumda video üretim aracı varsa brief’i uygula; yoksa video ürettiğini iddia etmeden, video aracına yapıştırabileceğim son promptu ve storyboard’u ver. Model veya hesap erişimi varsayma. Masaüstü ve mobil için ayrı kompozisyon kullan. Referans görsel sağlarsam nesnenin kimliğini koru.

Masaüstü çekimi:
Create a silent, 8-second, authored 3D product film for a website.

Subject: A sculptural desk lamp with a clay-colored curved shade, a slender brass stem and a wide weighted base
Visual purpose: Reveal how the shade, inner light socket and base connect, then show the finished lamp emitting warm light
Materials: Matte fired ceramic shade and base, brushed brass stem, frosted glass bulb; preserve realistic roughness
Palette: Warm ivory background #f2efe8, clay #a85c42, muted brass #ae8b59; no additional accent colors
Lighting: Large softbox at upper left, gentle contact shadows, warm practical light in the final state

Framing: 16:9. Place the object in the right half, leaving the left 40% calm and low-contrast for HTML copy. Keep all moving parts within the safe frame.
One continuous shot, no cuts. Motion must read when scrubbed both forwards and backwards. The final working state is the ending; do not reset to the opening shot.

Shot progression:
0–1.44s: Hold the complete object in a readable three-quarter view.
1.44–3.84s: Separate its main parts slowly along their assembly axes; keep every part visible.
3.84–5.76s: Use a small camera arc to reveal the inner connection and material detail.
5.76–8s: Reassemble precisely, reveal the final working state, then settle into a still composition.

Keep the object identity, number of parts and proportions constant. Use physically plausible contact, stable shadows and restrained reflections. No text, logos, UI, HUD, particles, camera shake, rapid zooms, flicker, warping, melting geometry or invented parts. All website text will be real HTML placed over or beside the film.

Desired delivery: 16:9 video, clean high-quality export, no audio. Duration and resolution must also be set in the generator controls if they are available; this prompt does not enforce technical settings. Inspect the exported clip for temporal errors before using it.

Mobil çekimi:
Create a silent, 8-second, authored 3D product film for a website.

Subject: A sculptural desk lamp with a clay-colored curved shade, a slender brass stem and a wide weighted base
Visual purpose: Reveal how the shade, inner light socket and base connect, then show the finished lamp emitting warm light
Materials: Matte fired ceramic shade and base, brushed brass stem, frosted glass bulb; preserve realistic roughness
Palette: Warm ivory background #f2efe8, clay #a85c42, muted brass #ae8b59; no additional accent colors
Lighting: Large softbox at upper left, gentle contact shadows, warm practical light in the final state

Framing: 9:16. Recompose the shot for portrait; do not crop the landscape result. Keep the full object and every separated part in the central 70%; leave the top quarter calm for HTML copy.
One continuous shot, no cuts. Motion must read when scrubbed both forwards and backwards. The final working state is the ending; do not reset to the opening shot.

Shot progression:
0–1.44s: Hold the complete object in a readable three-quarter view.
1.44–3.84s: Separate its main parts slowly along their assembly axes; keep every part visible.
3.84–5.76s: Use a small camera arc to reveal the inner connection and material detail.
5.76–8s: Reassemble precisely, reveal the final working state, then settle into a still composition.

Keep the object identity, number of parts and proportions constant. Use physically plausible contact, stable shadows and restrained reflections. No text, logos, UI, HUD, particles, camera shake, rapid zooms, flicker, warping, melting geometry or invented parts. All website text will be real HTML placed over or beside the film.

Desired delivery: 9:16 video, clean high-quality export, no audio. Duration and resolution must also be set in the generator controls if they are available; this prompt does not enforce technical settings. Inspect the exported clip for temporal errors before using it.

## Teslim ayarları

{
  "desktopAspect": "16:9",
  "mobileAspect": "9:16",
  "playback": "frame-sequence",
  "reducedMotion": "poster",
  "saveData": "poster",
  "frameSelection": "Math.round(progress * (frameCount - 1))",
  "requiresTemporalReview": true
}
