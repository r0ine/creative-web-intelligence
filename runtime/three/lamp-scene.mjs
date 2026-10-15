import * as THREE from '../vendor/three/three.module.min.js';
import { sampleLampMotion } from './lamp-motion.mjs';

const finishes = { clay: '#b85e43', forest: '#354a3b', chalk: '#d7d1c3' };

export function createLampScene({ canvas, compact = false, onError = () => {} }) {
  if (!canvas?.getContext) throw new TypeError('3D sahne için bir canvas gerekli.');
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: !compact, alpha: false, powerPreference: 'low-power' });
  renderer.setPixelRatio(Math.min(canvas.ownerDocument.defaultView.devicePixelRatio || 1, compact ? 1 : 1.5));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.1;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFShadowMap;

  const scene = new THREE.Scene();
  scene.background = new THREE.Color('#f2efe8');
  const camera = new THREE.PerspectiveCamera(34, 1, 0.1, 80);
  const lamp = new THREE.Group();
  scene.add(lamp);
  const geometries = new Set();
  const materials = new Set();
  const textures = new Set();
  const segments = compact ? 32 : 64;
  let progress = 0;
  let finish = 'clay';
  let viewAngle = 0;
  let disposed = false;
  let contextLost = false;
  let width = 1;
  let height = 1;
  let renderCount = 0;

  function material(properties) {
    const surface = new THREE.MeshStandardMaterial(properties);
    materials.add(surface);
    return surface;
  }

  function mesh(geometry, surface, parent = lamp, y = 0) {
    geometries.add(geometry);
    const part = new THREE.Mesh(geometry, surface);
    part.position.y = y;
    part.castShadow = false;
    part.receiveShadow = true;
    parent.add(part);
    return part;
  }

  function ring(radius, tube, surface, parent, y) {
    const part = mesh(new THREE.TorusGeometry(radius, tube, 8, segments), surface, parent, y);
    part.rotation.x = Math.PI / 2;
    return part;
  }

  const coating = material({ color: finishes.clay, roughness: 0.37, metalness: 0.22, envMapIntensity: 0.55 });
  const lining = material({ color: '#f2e8d6', roughness: 0.57, metalness: 0.06, side: THREE.BackSide });
  const brass = material({ color: '#b39760', roughness: 0.34, metalness: 0.72 });
  const ceramic = material({ color: '#e4dfd3', roughness: 0.75 });
  const rubber = material({ color: '#302f29', roughness: 0.92 });
  const bulbSurface = material({ color: '#fff2d8', roughness: 0.30, emissive: '#ffb45b', emissiveIntensity: 0.04 });

  const base = new THREE.Group();
  lamp.add(base);
  const baseProfile = [[0, 0.025], [0.84, 0.025], [0.93, 0.045], [0.97, 0.09], [0.97, 0.15], [0.93, 0.21], [0.84, 0.25], [0, 0.25]];
  mesh(new THREE.LatheGeometry(baseProfile.map(([radius, y]) => new THREE.Vector2(radius, y)), segments), coating, base).castShadow = true;
  mesh(new THREE.CylinderGeometry(0.81, 0.81, 0.025, segments), rubber, base, 0.025);
  const switchCollar = mesh(new THREE.CylinderGeometry(0.13, 0.13, 0.025, 24), brass, base, 0.244);
  switchCollar.position.set(0.52, 0.244, 0.42);
  const powerSwitch = mesh(new THREE.CylinderGeometry(0.087, 0.087, 0.038, 24), rubber, base, 0.265);
  powerSwitch.position.set(0.52, 0.265, 0.42);

  const stem = new THREE.Group();
  lamp.add(stem);
  mesh(new THREE.CylinderGeometry(0.115, 0.125, 2.03, segments), coating, stem, 1.255).castShadow = true;
  mesh(new THREE.CylinderGeometry(0.158, 0.158, 0.08, segments), brass, stem, 0.29);
  mesh(new THREE.CylinderGeometry(0.084, 0.084, 0.18, segments), brass, stem, 2.32);
  ring(0.116, 0.014, brass, stem, 2.24);

  const socket = new THREE.Group();
  lamp.add(socket);
  mesh(new THREE.CylinderGeometry(0.17, 0.135, 0.20, segments), brass, socket, 2.38).castShadow = true;
  mesh(new THREE.CylinderGeometry(0.17, 0.17, 0.13, segments), ceramic, socket, 2.53).castShadow = true;
  for (let thread = 0; thread < 3; thread++) ring(0.172, 0.012, brass, socket, 2.43 + thread * 0.039);
  mesh(new THREE.SphereGeometry(0.285, segments, compact ? 16 : 24), bulbSurface, socket, 2.79).castShadow = true;

  const shade = new THREE.Group();
  shade.position.y = 2.49;
  lamp.add(shade);
  const domeProfile = Array.from({ length: 25 }, (_, index) => {
    const angle = (index / 24) * Math.PI / 2;
    return new THREE.Vector2(1.38 * Math.cos(angle), 1.08 * Math.sin(angle));
  });
  const innerProfile = domeProfile.map(point => new THREE.Vector2(Math.max(0, point.x - 0.035), point.y - 0.026));
  mesh(new THREE.LatheGeometry(domeProfile, segments), coating, shade).castShadow = true;
  mesh(new THREE.LatheGeometry(innerProfile, segments), lining, shade).castShadow = true;
  ring(1.362, 0.025, coating, shade, -0.008);
  mesh(new THREE.CylinderGeometry(0.065, 0.09, 0.06, 24), brass, shade, 1.09);

  const cordPath = new THREE.CatmullRomCurve3([
    new THREE.Vector3(-0.15, 0.09, -0.85),
    new THREE.Vector3(-0.32, 0.025, -1.07),
    new THREE.Vector3(-0.75, 0.025, -1.22),
    new THREE.Vector3(-1.32, 0.025, -1.25),
    new THREE.Vector3(-1.62, 0.025, -1.60),
  ]);
  mesh(new THREE.TubeGeometry(cordPath, 30, 0.018, 6, false), rubber);

  scene.add(new THREE.HemisphereLight('#fff8ec', '#a69b85', 2.1));
  const key = new THREE.DirectionalLight('#fff6e7', 3.5);
  key.position.set(-2, 9, 3);
  key.castShadow = true;
  key.shadow.mapSize.set(compact ? 512 : 1024, compact ? 512 : 1024);
  Object.assign(key.shadow.camera, { left: -5, right: 5, top: 6, bottom: -5, near: 0.5, far: 18 });
  key.shadow.normalBias = 0.025;
  key.shadow.bias = -0.0002;
  key.shadow.radius = 4;
  scene.add(key);
  const rim = new THREE.DirectionalLight('#e4e9ee', 2.25);
  rim.position.set(4, 5, -4);
  scene.add(rim);

  const glow = new THREE.PointLight('#ffbd72', 0, 5, 2);
  socket.add(glow);
  glow.position.y = 2.76;
  const pool = new THREE.SpotLight('#ffc57e', 0, 5, 0.71, 1, 2);
  pool.position.set(0, 2.35, 0);
  pool.target.position.set(0, 0, 0);
  scene.add(pool, pool.target);

  const shadowSurface = new THREE.ShadowMaterial({ color: '#5e4936', opacity: 0.12 });
  materials.add(shadowSurface);
  const shadowFloor = mesh(new THREE.PlaneGeometry(200, 200), shadowSurface, scene, 0.002);
  shadowFloor.rotation.x = -Math.PI / 2;
  shadowFloor.castShadow = false;

  const contactCanvas = canvas.ownerDocument.createElement('canvas');
  contactCanvas.width = contactCanvas.height = 128;
  const contactContext = contactCanvas.getContext('2d');
  const contactGradient = contactContext.createRadialGradient(64, 64, 20, 64, 64, 64);
  contactGradient.addColorStop(0, 'rgba(63, 48, 32, 0.24)');
  contactGradient.addColorStop(0.4, 'rgba(63, 48, 32, 0.13)');
  contactGradient.addColorStop(1, 'rgba(63, 48, 32, 0)');
  contactContext.fillStyle = contactGradient;
  contactContext.fillRect(0, 0, 128, 128);
  const contactTexture = new THREE.CanvasTexture(contactCanvas);
  contactTexture.colorSpace = THREE.SRGBColorSpace;
  textures.add(contactTexture);
  const contactSurface = new THREE.MeshBasicMaterial({ map: contactTexture, transparent: true, depthWrite: false, toneMapped: false });
  materials.add(contactSurface);
  const contact = mesh(new THREE.PlaneGeometry(3.6, 3.6), contactSurface, scene, 0.007);
  contact.rotation.x = -Math.PI / 2;
  contact.castShadow = false;
  contact.receiveShadow = false;

  const poolCanvas = canvas.ownerDocument.createElement('canvas');
  poolCanvas.width = poolCanvas.height = 128;
  const poolContext = poolCanvas.getContext('2d');
  const poolGradient = poolContext.createRadialGradient(64, 64, 5, 64, 64, 64);
  poolGradient.addColorStop(0, 'rgba(255, 188, 92, 0.60)');
  poolGradient.addColorStop(0.5, 'rgba(255, 198, 117, 0.30)');
  poolGradient.addColorStop(1, 'rgba(255, 209, 146, 0)');
  poolContext.fillStyle = poolGradient;
  poolContext.fillRect(0, 0, 128, 128);
  const poolTexture = new THREE.CanvasTexture(poolCanvas);
  poolTexture.colorSpace = THREE.SRGBColorSpace;
  textures.add(poolTexture);
  const poolSurface = new THREE.MeshBasicMaterial({ map: poolTexture, transparent: true, depthWrite: false, toneMapped: false, opacity: 0 });
  materials.add(poolSurface);
  const lightPool = mesh(new THREE.PlaneGeometry(4.7, 4.7), poolSurface, scene, 0.009);
  lightPool.rotation.x = -Math.PI / 2;
  lightPool.castShadow = false;
  lightPool.receiveShadow = false;

  function render() {
    if (disposed || contextLost) return;
    const motion = sampleLampMotion(progress);
    shade.position.y = 2.49 + motion.shadeY;
    stem.position.y = motion.stemY;
    socket.position.y = motion.bulbY;
    lamp.rotation.y = motion.lampRotation;
    bulbSurface.emissiveIntensity = 0.04 + motion.lightIntensity * 1.25;
    glow.intensity = motion.lightIntensity * 6;
    pool.intensity = motion.lightIntensity * 10;
    poolSurface.opacity = motion.lightIntensity * 0.75;
    const orbit = motion.orbit + THREE.MathUtils.degToRad(viewAngle);
    const narrowScale = Math.max(1, 0.86 / camera.aspect);
    const distance = motion.cameraRadius * narrowScale;
    camera.position.set(Math.sin(orbit) * distance, motion.cameraHeight, Math.cos(orbit) * distance);
    camera.lookAt(0, motion.targetY, 0);
    try {
      renderer.render(scene, camera);
      renderCount++;
    } catch (error) {
      contextLost = true;
      onError(error);
    }
  }

  function loseContext(event) {
    event.preventDefault();
    if (disposed || contextLost) return;
    contextLost = true;
    onError(new Error('3D bağlantısı kesildi.'));
  }

  canvas.addEventListener('webglcontextlost', loseContext);

  return {
    setProgress(value) {
      const next = sampleLampMotion(value).progress;
      if (next === progress || disposed) return;
      progress = next;
      render();
    },
    setFinish(value) {
      if (!Object.hasOwn(finishes, value)) throw new RangeError('Kaplama clay, forest veya chalk olmalı.');
      if (value === finish || disposed) return;
      finish = value;
      coating.color.set(finishes[value]);
      render();
    },
    setView(degrees = 0) {
      if (!Number.isFinite(degrees)) throw new TypeError('Bakış açısı sonlu bir sayı olmalı.');
      const next = Math.max(-25, Math.min(25, degrees));
      if (viewAngle === next || disposed) return;
      viewAngle = next;
      render();
    },
    resize(nextWidth, nextHeight) {
      if (![nextWidth, nextHeight].every(value => Number.isFinite(value) && value > 0)) {
        throw new RangeError('Sahne genişliği ve yüksekliği pozitif olmalı.');
      }
      if (disposed) return;
      width = Math.max(1, Math.round(nextWidth));
      height = Math.max(1, Math.round(nextHeight));
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height, false);
      render();
    },
    get stats() {
      return {
        drawCalls: renderer.info.render.calls,
        triangles: renderer.info.render.triangles,
        geometries: renderer.info.memory.geometries,
        textures: renderer.info.memory.textures,
        progress, finish, viewAngle, renderCount, width, height,
        pixelRatio: renderer.getPixelRatio(),
        disposed, contextLost,
      };
    },
    destroy() {
      if (disposed) return;
      disposed = true;
      canvas.removeEventListener('webglcontextlost', loseContext);
      for (const geometry of geometries) geometry.dispose();
      for (const surface of materials) surface.dispose();
      for (const texture of textures) texture.dispose();
      key.shadow.dispose();
      scene.clear();
      renderer.renderLists.dispose();
      renderer.dispose();
      renderer.forceContextLoss();
    },
  };
}
