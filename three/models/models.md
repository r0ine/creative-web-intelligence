# 3D / Models

Entries: **15**

- **3D-006 Prefer glTF/GLB for web models** — Use GLTFLoader and standard compression paths for production assets. _(tags: models)_
- **3D-007 Support Draco when assets use it** — Loader pipeline should accept DRACO compressed geometry. _(tags: models)_
- **3D-008 Support KTX2 compressed textures** — Use KTX2 paths where projects ship compressed GPU textures. _(tags: models)_
- **3D-009 Support Meshopt** — Asset pipeline should accept meshopt-decoded glTF when used. _(tags: models)_
- **3D-010 Cache loaded assets** — Avoid duplicate model/texture loads across scenes/routes. _(tags: models)_
- **3D-056 Exploded view needs authored transforms** — Parts should separate along meaningful axes or explicit target transforms. _(tags: models)_
- **3D-057 Exploded view should reassemble** — Store origin transforms so the model can return precisely. _(tags: models)_
- **3D-058 Part metadata matters** — Name model parts and attach semantic IDs for features/hotspots. _(tags: models)_
- **3D-059 Model transitions need normalized progress** — Assembly/disassembly should expose 0..1 for scroll/timeline binding. _(tags: models)_
- **3D-060 Morph targets need safe ranges** — Validate model-specific morph target indexes and limits. _(tags: models)_
- **3D-061 Animation clips need state control** — Do not autoplay all clips; map clips to scene/story states. _(tags: models)_
- **3D-062 Model bounds utilities are essential** — Center/fit/framing helpers reduce repeated setup work. _(tags: models)_
- **3D-063 Asset manager needs errors** — Missing model/texture should produce clear fallback, not blank canvas. _(tags: models)_
- **3D-083 3D configurator needs state schema** — Variant, material, camera and selected-part states should be serializable. _(tags: configurator)_
- **3D-084 Configurator changes should not reload the world** — Swap material/mesh variants efficiently. _(tags: configurator)_