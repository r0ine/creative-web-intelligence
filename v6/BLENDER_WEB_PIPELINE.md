# Blender → Web Pipeline v6

## Pipeline

```
Blender scene
  → scene audit (topology, materials, textures, animation)
  → optimization (decimation, UV, texture resize, mesh merge)
  → animation baking (constraints → keyframes, drivers → values)
  → material conversion (Blender nodes → glTF PBR)
  → texture optimization (resize, compress, atlas)
  → GLB export (Draco or Meshopt compression)
  → KTX2 texture compression (where supported)
  → web integration test (Three.js / R3F / model-viewer)
  → performance validation (draw calls, texture memory, file size)
  → mobile variant (reduced LOD, smaller textures, or prerender)
```

## Optimization rules

### Geometry
- Remove interior faces, doubles, zero-area faces.
- Decimate non-hero geometry. Target: under 100K triangles for a single product model, under 250K for a scene.
- Apply modifiers before export. No subdivision surface modifiers left at runtime.
- Merge meshes that share the same material where animation does not require separation.

### Textures
- PBR metallic-roughness workflow only. No Blender Principled BSDF tricks that do not translate.
- Pack roughness (G), metallic (B), and AO (R) into a single ORM texture.
- Resize: 2K max for hero surfaces, 1K for secondary, 512 for background.
- Export as PNG for the GLB, then compress to KTX2/Basis for delivery.

### Animation
- Bake all animations to keyframes at 30fps. No constraints, drivers, or NLA strips at runtime.
- Name clips descriptively: `idle`, `approach`, `explode`, `assemble`.
- Remove redundant keyframes after baking (Blender: Decimate Keyframes).

### Export
- GLB (binary glTF). Single-file, self-contained.
- Draco compression for geometry. Meshopt for skinned/animated meshes.
- Verify export: open in https://gltf-viewer.donmccurdy.com/ or Three.js editor.

### Performance targets

| Metric | Target | Hard limit |
|:--|:--|:--|
| GLB file size | < 2MB | 5MB |
| Texture memory | < 32MB | 64MB |
| Draw calls | < 30 | 50 |
| Triangle count | < 100K | 250K |
| Animation clips | < 5 | 10 |
