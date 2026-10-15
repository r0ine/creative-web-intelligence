# v7 release notes

This release turns the library's reference-first guidance into a runnable workflow and brings the mobile scroll, 3D, media, and validation work into the public repository.

- **Reference workflow:** A new site starts with brief interpretation, targeted questions, one small visual preview, and a short review note. The full implementation follows that direction rather than generating a new prototype for every section.
- **Visual comparison:** A local browser tool overlays source and implementation screenshots, shows a difference heatmap, and measures pixel differences at matching dimensions. It accepts PNG, JPG, and WebP. Pixel similarity does not verify interaction, accessibility, or motion.
- **Visual calibration:** A decision guide asks where colors and shapes come from and what each animation explains. A local CSS audit flags repeated boxed surfaces, dark hairline-heavy layouts, universal fade-ups, blanket transitions, and endless motion. The reference tool itself now uses a quiet paper-toned interface.
- **Mobile scroll and 3D:** The lamp example uses a live Three.js scene on desktop, 48 local WebP frames on mobile, and static images for reduced motion or data saving. The scroll and frame runtimes include bounded loading, cleanup, and reverse-scroll behavior.
- **Optional video workflow:** The media studio creates a prompt to paste into ChatGPT, previews a user-selected local video, and accepts a converted frame sequence. It does not require a model API. The video conversion tool needs FFmpeg only when used.
- **Source selection:** React Bits, 21st.dev, and other providers are cataloged with integration and license guidance. Their component code is not copied wholesale into this repository.
- **Validation:** Media-plan auditing, v7 catalog checks, Node and Python tests, and a GitHub Actions workflow cover the new runtime and guidance. Third-party components still require their own license and compatibility review.

Installation and usage: [English](docs/INSTALL_EN.md) · [Türkçe](docs/INSTALL_TR.md).
