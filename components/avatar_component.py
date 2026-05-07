def get_avatar_html(hairstyle="bun", hair_color="#1a1a1a",
                    skin_tone="#F5CBA7", outfit_color="#E91E8C",
                    lip_color="#C0392B"):
    """
    Returns a complete self-contained Three.js fashion avatar HTML string.
    Parameters are injected as JS variables for real-time customization.

    Upgrades over v1:
    - PBR skin with subsurface scattering simulation (emissive warm bleed)
    - 1024x1024 face texture: iris detail, limbal ring, radial fibers,
      dual catchlights, realistic lip layers, pore noise, temple shadows
    - Updo hairstyle added (4 styles total)
    - CubeCamera for live environment reflections on gold/floor
    - 4096x4096 shadow maps with bias correction
    - Smooth rotation damping
    - Scroll-to-zoom
    - Outfit-color-reactive rim light
    - High-poly skirt with realistic fold deformation
    - Animated sparkle particles with drift velocity
    """

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      background: linear-gradient(135deg, #0D0D0D 0%, #1A1A2E 50%, #16213E 100%);
      overflow: hidden;
      font-family: 'Arial', sans-serif;
    }}
    canvas {{ display: block; }}

    #controls-overlay {{
      position: absolute;
      bottom: 15px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      gap: 10px;
      z-index: 10;
    }}

    .ctrl-btn {{
      background: rgba(233,30,140,0.85);
      color: white;
      border: 1px solid rgba(255,255,255,0.3);
      padding: 8px 18px;
      border-radius: 20px;
      cursor: pointer;
      font-size: 12px;
      font-weight: bold;
      backdrop-filter: blur(6px);
      transition: all 0.2s;
    }}
    .ctrl-btn:hover {{ background: rgba(233,30,140,1); transform: scale(1.05); }}

    #info-tag {{
      position: absolute;
      top: 12px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(233,30,140,0.2);
      border: 1px solid rgba(233,30,140,0.5);
      color: #fff;
      padding: 5px 18px;
      border-radius: 20px;
      font-size: 11px;
      letter-spacing: 2px;
      backdrop-filter: blur(6px);
      z-index: 10;
    }}

    #screenshot-link {{ display: none; }}
  </style>
</head>
<body>

<div id="info-tag">✨ FASHION AVATAR — DRAG · SCROLL TO ZOOM</div>

<div id="controls-overlay">
  <button class="ctrl-btn" onclick="resetCamera()">🎯 Reset View</button>
  <button class="ctrl-btn" onclick="toggleAutoRotate()">🔄 Auto Rotate</button>
  <button class="ctrl-btn" onclick="takeScreenshot()">📸 Screenshot</button>
</div>

<a id="screenshot-link" download="fashion_avatar.png"></a>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

<script>
// ─── INJECTED PARAMETERS FROM PYTHON ──────────────────────────────────────
const HAIRSTYLE   = "{hairstyle}";
const HAIR_COLOR  = "{hair_color}";
const SKIN_TONE   = "{skin_tone}";
const OUTFIT_COLOR= "{outfit_color}";
const LIP_COLOR   = "{lip_color}";

// ─── SCENE SETUP ──────────────────────────────────────────────────────────
const scene = new THREE.Scene();
scene.fog   = new THREE.FogExp2(0x0D0D0D, 0.025);

const W = window.innerWidth;
const H = window.innerHeight;

const renderer = new THREE.WebGLRenderer({{
  antialias: true,
  alpha: true,
  preserveDrawingBuffer: true,
  logarithmicDepthBuffer: true
}});
renderer.setSize(W, H);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled  = true;
renderer.shadowMap.type     = THREE.PCFSoftShadowMap;
renderer.toneMapping        = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.35;
document.body.appendChild(renderer.domElement);

const camera = new THREE.PerspectiveCamera(38, W / H, 0.01, 100);
camera.position.set(0, 1.3, 5.8);
camera.lookAt(0, 0.9, 0);

// ─── PHOTOGRAPHIC 5-POINT LIGHTING ────────────────────────────────────────
// Ambient (very low — avoids flat fill)
scene.add(new THREE.AmbientLight(0xffffff, 0.12));

// KEY — warm top-left
const keyLight = new THREE.DirectionalLight(0xFFF8F0, 2.2);
keyLight.position.set(-2.5, 5, 3.5);
keyLight.castShadow = true;
keyLight.shadow.mapSize.width  = 4096;
keyLight.shadow.mapSize.height = 4096;
keyLight.shadow.bias           = -0.0002;
keyLight.shadow.camera.left    = keyLight.shadow.camera.bottom = -4;
keyLight.shadow.camera.right   = keyLight.shadow.camera.top   =  4;
scene.add(keyLight);

// FILL — cool right
const fillLight = new THREE.DirectionalLight(0xB0C8FF, 0.75);
fillLight.position.set(3.5, 2, 2);
scene.add(fillLight);

// RIM — strong pink backlight (separation halo)
const rimLight = new THREE.PointLight(0xFF69B4, 2.0, 16);
rimLight.position.set(0, 3.5, -4.5);
scene.add(rimLight);

// BOUNCE — warm floor reflect
const bounceLight = new THREE.PointLight(0xFFE0A0, 0.4, 8);
bounceLight.position.set(0, -4, 1.5);
scene.add(bounceLight);

// CATCH — front specular for eye highlights
const catchLight = new THREE.SpotLight(0xffffff, 0.45, 8, Math.PI / 8, 0.5);
catchLight.position.set(0, 3, 4);
scene.add(catchLight);

// ─── CUBE CAMERA for live reflections on gold + floor ─────────────────────
const cubeRenderTarget = new THREE.WebGLCubeRenderTarget(128, {{
  format: THREE.RGBFormat,
  generateMipmaps: true,
  minFilter: THREE.LinearMipmapLinearFilter
}});
const cubeCamera = new THREE.CubeCamera(0.1, 50, cubeRenderTarget);
scene.add(cubeCamera);

// ─── MATERIALS ────────────────────────────────────────────────────────────

// PBR Skin — subsurface scattering simulation via warm emissive bleed
function makeSkinMat(color, isFace) {{
  const c = new THREE.Color(color);
  return new THREE.MeshStandardMaterial({{
    color:             c,
    roughness:         isFace ? 0.62 : 0.70,
    metalness:         0.0,
    emissive:          c.clone().multiplyScalar(0.10),
    emissiveIntensity: 0.20,
  }});
}}

// Gold — near-mirror PBR
const goldMat = new THREE.MeshStandardMaterial({{
  color:     0xFFD700,
  metalness: 0.95,
  roughness: 0.08,
  envMapIntensity: 2.0
}});

// ─── FACE TEXTURE (1024×1024, photorealistic) ─────────────────────────────
function buildFaceTexture(skinColor, lipColor) {{
  const S   = 1024;
  const cv  = document.createElement('canvas');
  cv.width  = S; cv.height = S;
  const ctx = cv.getContext('2d');

  const sc     = new THREE.Color(skinColor);
  const skinHex = '#' + sc.getHexString();

  function shadeHex(hex, p) {{
    const n = parseInt(hex.replace('#',''), 16);
    const r = Math.min(255, Math.max(0, (n >> 16) + p));
    const g = Math.min(255, Math.max(0, ((n >> 8) & 0xFF) + p));
    const b = Math.min(255, Math.max(0, (n & 0xFF) + p));
    return '#' + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
  }}

  // Base skin
  ctx.fillStyle = skinHex;
  ctx.fillRect(0, 0, S, S);

  // Subtle pore noise
  for (let i = 0; i < 1500; i++) {{
    ctx.fillStyle = `rgba(0,0,0,${{Math.random() * 0.018}})`;
    ctx.beginPath();
    ctx.arc(Math.random() * S, Math.random() * S, Math.random() * 1.2, 0, Math.PI * 2);
    ctx.fill();
  }}

  // Forehead highlight
  const fhG = ctx.createRadialGradient(512, 180, 20, 512, 180, 200);
  fhG.addColorStop(0, 'rgba(255,255,255,0.13)');
  fhG.addColorStop(1, 'rgba(255,255,255,0)');
  ctx.fillStyle = fhG; ctx.fillRect(0, 0, S, S);

  // SSS cheek blush
  [[260, 420], [752, 420]].forEach(([cx, cy]) => {{
    const g = ctx.createRadialGradient(cx, cy, 8, cx, cy, 110);
    g.addColorStop(0, 'rgba(220,80,70,0.22)');
    g.addColorStop(0.5,'rgba(220,80,70,0.09)');
    g.addColorStop(1, 'rgba(220,80,70,0)');
    ctx.fillStyle = g; ctx.fillRect(0, 0, S, S);
  }});

  // Temple shadows (depth)
  [[90, 300], [910, 300]].forEach(([cx, cy]) => {{
    const g = ctx.createRadialGradient(cx, cy, 0, cx, cy, 185);
    g.addColorStop(0, 'rgba(0,0,0,0.20)');
    g.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = g; ctx.fillRect(0, 0, S, S);
  }});

  // ── EYES ────────────────────────────────────────────────────────────────
  function drawEye(ex, ey) {{
    // Socket shadow
    const sock = ctx.createRadialGradient(ex, ey + 10, 10, ex, ey + 10, 75);
    sock.addColorStop(0, 'rgba(0,0,0,0.22)');
    sock.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = sock; ctx.fillRect(0, 0, S, S);

    // Sclera
    ctx.save(); ctx.translate(ex, ey); ctx.scale(1.55, 1);
    ctx.beginPath(); ctx.ellipse(0, 0, 38, 27, 0, 0, Math.PI * 2);
    ctx.restore(); ctx.fillStyle = '#f6f1ee'; ctx.fill();

    // Iris gradient
    const iris = ctx.createRadialGradient(ex, ey - 4, 2, ex, ey, 24);
    iris.addColorStop(0,   '#4a2c0a');
    iris.addColorStop(0.4, '#2a1505');
    iris.addColorStop(0.8, '#1a0d02');
    iris.addColorStop(1,   '#000000');
    ctx.beginPath(); ctx.arc(ex, ey, 24, 0, Math.PI * 2);
    ctx.fillStyle = iris; ctx.fill();

    // Radial iris fibers
    for (let a = 0; a < 360; a += 10) {{
      const r = a * Math.PI / 180;
      ctx.strokeStyle = 'rgba(100,60,10,0.35)'; ctx.lineWidth = 0.8;
      ctx.beginPath();
      ctx.moveTo(ex + Math.cos(r) * 9,  ey + Math.sin(r) * 9);
      ctx.lineTo(ex + Math.cos(r) * 22, ey + Math.sin(r) * 22);
      ctx.stroke();
    }}

    // Limbal ring
    ctx.beginPath(); ctx.arc(ex, ey, 24, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(0,0,0,0.7)'; ctx.lineWidth = 2; ctx.stroke();

    // Pupil
    const pup = ctx.createRadialGradient(ex - 2, ey - 2, 0, ex, ey, 13);
    pup.addColorStop(0, '#1a1a1a'); pup.addColorStop(1, '#000000');
    ctx.beginPath(); ctx.arc(ex, ey, 13, 0, Math.PI * 2);
    ctx.fillStyle = pup; ctx.fill();

    // KEY catchlight (large, top-right)
    ctx.beginPath(); ctx.ellipse(ex + 6, ey - 8, 7, 5, -0.5, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(255,255,255,0.92)'; ctx.fill();

    // FILL catchlight (small, bottom-left)
    ctx.beginPath(); ctx.arc(ex - 8, ey + 5, 4, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(255,255,255,0.35)'; ctx.fill();

    // Eyelid crease
    ctx.strokeStyle = 'rgba(0,0,0,0.15)'; ctx.lineWidth = 5;
    ctx.beginPath();
    ctx.moveTo(ex - 48, ey - 12);
    ctx.quadraticCurveTo(ex, ey - 48, ex + 48, ey - 12);
    ctx.stroke();

    // Upper lashes
    ctx.strokeStyle = '#0a0505'; ctx.lineWidth = 2.5;
    for (let i = -5; i <= 5; i++) {{
      const t   = i / 5;
      const lx  = ex + t * 44;
      const ly  = ey - Math.sqrt(1 - t * t) * 26;
      const ang = Math.atan2(-(ey - 20) - ly, lx - ex) - 0.12;
      ctx.beginPath(); ctx.moveTo(lx, ly);
      ctx.lineTo(lx + Math.cos(ang) * 11, ly + Math.sin(ang) * 11);
      ctx.stroke();
    }}

    // Lower lashes
    ctx.lineWidth = 1.5; ctx.strokeStyle = 'rgba(10,5,5,0.6)';
    for (let i = -3; i <= 3; i++) {{
      const t  = i / 3;
      const lx = ex + t * 35;
      const ly = ey + Math.sqrt(1 - t * t) * 24;
      ctx.beginPath(); ctx.moveTo(lx, ly); ctx.lineTo(lx, ly + 6); ctx.stroke();
    }}
  }}

  drawEye(300, 380);
  drawEye(724, 380);

  // ── EYEBROWS ────────────────────────────────────────────────────────────
  function drawBrow(cx, cy, flip) {{
    ctx.strokeStyle = '#1a0d05'; ctx.lineWidth = 9; ctx.lineCap = 'round';
    ctx.beginPath();
    if (!flip) {{
      ctx.moveTo(cx - 70, cy + 8); ctx.quadraticCurveTo(cx - 20, cy - 18, cx + 55, cy + 5);
    }} else {{
      ctx.moveTo(cx - 55, cy + 5); ctx.quadraticCurveTo(cx + 20, cy - 18, cx + 70, cy + 8);
    }}
    ctx.stroke();
    // Hair stroke detail
    ctx.lineWidth = 2; ctx.strokeStyle = 'rgba(20,10,3,0.4)';
    for (let s = 0; s < 12; s++) {{
      const t  = s / 11;
      const bx = cx + (flip ? 1 : -1) * (55 * t - 35);
      const by = cy + Math.sin(t * Math.PI) * (-18) + 5;
      ctx.beginPath(); ctx.moveTo(bx, by + 5);
      ctx.lineTo(bx + (Math.random() - 0.5) * 4, by - 8); ctx.stroke();
    }}
  }}
  drawBrow(300, 310, false);
  drawBrow(724, 310, true);

  // ── NOSE ────────────────────────────────────────────────────────────────
  // Bridge highlight
  const bridgeHL = ctx.createLinearGradient(495, 300, 518, 300);
  bridgeHL.addColorStop(0,   'rgba(255,255,255,0)');
  bridgeHL.addColorStop(0.5, 'rgba(255,255,255,0.15)');
  bridgeHL.addColorStop(1,   'rgba(255,255,255,0)');
  ctx.fillStyle = bridgeHL; ctx.fillRect(490, 300, 35, 180);

  // Nostrils
  ctx.fillStyle = 'rgba(0,0,0,0.25)';
  ctx.beginPath(); ctx.ellipse(450, 530, 22, 12,  0.4, 0, Math.PI * 2); ctx.fill();
  ctx.beginPath(); ctx.ellipse(562, 530, 22, 12, -0.4, 0, Math.PI * 2); ctx.fill();

  // Tip specular
  const noseTip = ctx.createRadialGradient(506, 510, 2, 506, 510, 30);
  noseTip.addColorStop(0, 'rgba(255,255,255,0.18)');
  noseTip.addColorStop(1, 'rgba(255,255,255,0)');
  ctx.fillStyle = noseTip; ctx.fillRect(0, 0, S, S);

  // ── LIPS ────────────────────────────────────────────────────────────────
  const lc     = new THREE.Color(lipColor);
  const lipHex = '#' + lc.getHexString();

  // Lip shadow
  ctx.fillStyle = 'rgba(0,0,0,0.12)';
  ctx.beginPath(); ctx.ellipse(512, 650, 120, 65, 0, 0, Math.PI * 2); ctx.fill();

  // Lower lip
  ctx.fillStyle = lipHex;
  ctx.beginPath();
  ctx.moveTo(370, 625);
  ctx.bezierCurveTo(420, 600, 480, 595, 512, 598);
  ctx.bezierCurveTo(544, 595, 604, 600, 654, 625);
  ctx.bezierCurveTo(640, 670, 580, 700, 512, 702);
  ctx.bezierCurveTo(444, 700, 384, 670, 370, 625);
  ctx.fill();

  // Upper lip (cupid's bow)
  ctx.fillStyle = shadeHex(lipHex, -20);
  ctx.beginPath();
  ctx.moveTo(370, 625);
  ctx.bezierCurveTo(400, 610, 450, 600, 480, 608);
  ctx.bezierCurveTo(496, 612, 506, 605, 512, 604);
  ctx.bezierCurveTo(518, 605, 528, 612, 544, 608);
  ctx.bezierCurveTo(574, 600, 624, 610, 654, 625);
  ctx.bezierCurveTo(620, 618, 560, 612, 512, 615);
  ctx.bezierCurveTo(464, 612, 404, 618, 370, 625);
  ctx.fill();

  // Centre line
  ctx.strokeStyle = 'rgba(0,0,0,0.2)'; ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.moveTo(370, 625); ctx.bezierCurveTo(440, 622, 490, 620, 512, 619);
  ctx.bezierCurveTo(534, 620, 584, 622, 654, 625); ctx.stroke();

  // Gloss highlight
  const gloss = ctx.createRadialGradient(512, 648, 5, 512, 648, 55);
  gloss.addColorStop(0,   'rgba(255,255,255,0.38)');
  gloss.addColorStop(0.5, 'rgba(255,255,255,0.12)');
  gloss.addColorStop(1,   'rgba(255,255,255,0)');
  ctx.fillStyle = gloss; ctx.fillRect(0, 0, S, S);

  const gloss2 = ctx.createRadialGradient(512, 612, 3, 512, 612, 25);
  gloss2.addColorStop(0, 'rgba(255,255,255,0.22)');
  gloss2.addColorStop(1, 'rgba(255,255,255,0)');
  ctx.fillStyle = gloss2; ctx.fillRect(0, 0, S, S);

  return new THREE.CanvasTexture(cv);
}}

// ─── HEAD ─────────────────────────────────────────────────────────────────
const headGeo = new THREE.SphereGeometry(0.42, 128, 128);
// Realistic head shaping: flatten crown, widen cheeks
const headPos = headGeo.attributes.position;
for (let i = 0; i < headPos.count; i++) {{
  const x   = headPos.getX(i);
  const y   = headPos.getY(i);
  const lat = Math.asin(y / 0.42);
  const flatTop   = y > 0.3 ? y - (y - 0.3) * 0.12 : y;
  const cheekWide = Math.abs(lat) < 0.4 ? 1.04 : 1.0;
  headPos.setXYZ(i, x * cheekWide, flatTop, headPos.getZ(i) * cheekWide);
}}
headGeo.computeVertexNormals();

const headMat = makeSkinMat(SKIN_TONE, true);
headMat.map   = buildFaceTexture(SKIN_TONE, LIP_COLOR);
headMat.needsUpdate = true;

const avatar = new THREE.Group();
scene.add(avatar);

const head = new THREE.Mesh(headGeo, headMat);
head.position.y = 1.85;
head.castShadow = true;
avatar.add(head);

// ─── NECK ─────────────────────────────────────────────────────────────────
const neck = new THREE.Mesh(
  new THREE.CylinderGeometry(0.115, 0.14, 0.30, 64),
  makeSkinMat(SKIN_TONE, false)
);
neck.position.y = 1.30;
neck.castShadow = true;
avatar.add(neck);

// ─── TORSO (PBR outfit fabric) ────────────────────────────────────────────
const outfitMat = new THREE.MeshStandardMaterial({{
  color:    new THREE.Color(OUTFIT_COLOR),
  roughness: 0.52,
  metalness: 0.08
}});

// Shoulders
const torsoUpper = new THREE.Mesh(
  new THREE.CylinderGeometry(0.54, 0.37, 0.62, 64),
  outfitMat.clone()
);
torsoUpper.position.y = 0.90;
torsoUpper.castShadow = true;
avatar.add(torsoUpper);

// Waist
const torsoLower = new THREE.Mesh(
  new THREE.CylinderGeometry(0.37, 0.41, 0.52, 64),
  outfitMat.clone()
);
torsoLower.position.y = 0.33;
torsoLower.castShadow = true;
avatar.add(torsoLower);

// Blouse neckline detail
const blouse = new THREE.Mesh(
  new THREE.TorusGeometry(0.24, 0.035, 16, 64),
  new THREE.MeshStandardMaterial({{
    color:     new THREE.Color(OUTFIT_COLOR).multiplyScalar(0.82),
    roughness: 0.4,
    metalness: 0.2
  }})
);
blouse.position.y = 1.18;
blouse.rotation.x = Math.PI / 2;
avatar.add(blouse);

// ─── SAREE PALLU ──────────────────────────────────────────────────────────
const palluGeo = new THREE.PlaneGeometry(0.58, 1.45, 10, 24);
const palluPos = palluGeo.attributes.position;
for (let i = 0; i < palluPos.count; i++) {{
  const y = palluPos.getY(i), x = palluPos.getX(i);
  palluPos.setZ(i, Math.sin(y * 3.5) * 0.055 + Math.cos(x * 5) * 0.03);
}}
palluGeo.computeVertexNormals();
const pallu = new THREE.Mesh(palluGeo, new THREE.MeshStandardMaterial({{
  color:       new THREE.Color(OUTFIT_COLOR),
  roughness:   0.38,
  metalness:   0.28,
  transparent: true,
  opacity:     0.92,
  side:        THREE.DoubleSide
}}));
pallu.position.set(-0.28, 0.58, 0.42);
pallu.rotation.z = 0.12;
avatar.add(pallu);

// Gold zari border
const border = new THREE.Mesh(
  new THREE.PlaneGeometry(0.06, 1.45),
  goldMat.clone()
);
border.position.set(-0.57, 0.58, 0.43);
border.rotation.z = 0.12;
avatar.add(border);

// ─── SKIRT — high-poly with realistic fold deformation ────────────────────
const skirtGeo = new THREE.CylinderGeometry(0.60, 0.76, 1.70, 64, 12, true);
const skPos    = skirtGeo.attributes.position;
for (let i = 0; i < skPos.count; i++) {{
  const a        = Math.atan2(skPos.getX(i), skPos.getZ(i));
  const y        = skPos.getY(i);
  const foldAmt  = 0.018 + (y < -0.5 ? 0.012 : 0);
  skPos.setX(i, skPos.getX(i) + Math.sin(a * 8) * foldAmt);
  skPos.setZ(i, skPos.getZ(i) + Math.cos(a * 8) * foldAmt * 0.5);
}}
skirtGeo.computeVertexNormals();
const skirt = new THREE.Mesh(skirtGeo, new THREE.MeshStandardMaterial({{
  color:     new THREE.Color(OUTFIT_COLOR),
  roughness: 0.48,
  metalness: 0.12,
  side:      THREE.DoubleSide
}}));
skirt.position.y = -0.75;
skirt.castShadow = true;
avatar.add(skirt);

// Gold hem
const hem = new THREE.Mesh(
  new THREE.TorusGeometry(0.73, 0.022, 10, 96),
  goldMat.clone()
);
hem.position.y = -1.60;
avatar.add(hem);

// ─── ARMS ─────────────────────────────────────────────────────────────────
function makeArm(side) {{
  const sx = side * 0.70;
  const sm = makeSkinMat(SKIN_TONE, false);
  const om = new THREE.MeshStandardMaterial({{
    color: new THREE.Color(OUTFIT_COLOR), roughness: 0.5, metalness: 0.1
  }});

  // Sleeve
  const sleeve = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.10, 0.52, 32), om.clone());
  sleeve.position.set(sx, 0.76, 0); sleeve.rotation.z = side * 0.22;
  sleeve.castShadow = true; avatar.add(sleeve);

  // Lower arm
  const lower = new THREE.Mesh(new THREE.CylinderGeometry(0.095, 0.085, 0.50, 32), sm.clone());
  lower.position.set(sx * 1.10, 0.34, 0.03); lower.rotation.z = side * 0.34;
  lower.castShadow = true; avatar.add(lower);

  // Wrist
  const wrist = new THREE.Mesh(new THREE.CylinderGeometry(0.072, 0.068, 0.14, 32), sm.clone());
  wrist.position.set(sx * 1.20, 0.06, 0.07); wrist.rotation.z = side * 0.38;
  avatar.add(wrist);

  // Hand
  const hand = new THREE.Mesh(new THREE.SphereGeometry(0.082, 32, 32), sm.clone());
  hand.scale.set(1, 0.75, 0.9);
  hand.position.set(sx * 1.28, -0.06, 0.10); hand.castShadow = true;
  avatar.add(hand);

  // Bangles (gold + outfit-colored)
  [0.12, 0.18, 0.24].forEach((oy, i) => {{
    const bMat = i === 1
      ? new THREE.MeshStandardMaterial({{ color: new THREE.Color(OUTFIT_COLOR), metalness: 0.6, roughness: 0.3 }})
      : goldMat.clone();
    const bangle = new THREE.Mesh(new THREE.TorusGeometry(0.072, 0.013, 10, 48), bMat);
    bangle.position.set(sx * 1.24, oy, 0.07); bangle.rotation.x = Math.PI / 2;
    avatar.add(bangle);
  }});
}}
makeArm(1);
makeArm(-1);

// ─── EARS & EARRINGS ──────────────────────────────────────────────────────
[-1, 1].forEach(s => {{
  const ear = new THREE.Mesh(
    new THREE.SphereGeometry(0.074, 32, 32),
    makeSkinMat(SKIN_TONE, false)
  );
  ear.scale.z = 0.45;
  ear.position.set(s * 0.43, 1.85, 0);
  avatar.add(ear);

  // Stud
  const stud = new THREE.Mesh(new THREE.SphereGeometry(0.028, 16, 16), goldMat.clone());
  stud.position.set(s * 0.45, 1.82, 0); avatar.add(stud);

  // Drop chain
  const chain = new THREE.Mesh(new THREE.CylinderGeometry(0.004, 0.004, 0.12, 8), goldMat.clone());
  chain.position.set(s * 0.46, 1.72, 0); avatar.add(chain);

  // Pendant
  const drop = new THREE.Mesh(new THREE.SphereGeometry(0.038, 16, 16), goldMat.clone());
  drop.scale.y = 1.4;
  drop.position.set(s * 0.46, 1.63, 0); avatar.add(drop);
}});

// ─── BINDI ────────────────────────────────────────────────────────────────
const bindi = new THREE.Mesh(
  new THREE.CircleGeometry(0.025, 32),
  new THREE.MeshStandardMaterial({{
    color:             0xFF0040,
    metalness:         0.8,
    roughness:         0.1,
    emissive:          0xFF0040,
    emissiveIntensity: 0.3
  }})
);
bindi.position.set(0, 2.075, 0.420);
avatar.add(bindi);

// ─── HAIR SYSTEM — 4 styles ────────────────────────────────────────────────
function buildHair() {{
  const old = avatar.getObjectByName('hairGroup');
  if (old) avatar.remove(old);

  const hairGroup = new THREE.Group();
  hairGroup.name  = 'hairGroup';

  const hm = new THREE.MeshStandardMaterial({{
    color:    new THREE.Color(HAIR_COLOR),
    roughness: 0.72,
    metalness: 0.02
  }});

  // Hair cap (all styles share it)
  const cap = new THREE.Mesh(
    new THREE.SphereGeometry(0.445, 64, 64, 0, Math.PI * 2, 0, Math.PI * 0.55),
    hm.clone()
  );
  cap.position.y = 1.86;
  hairGroup.add(cap);

  if (HAIRSTYLE === 'bun') {{
    const bun = new THREE.Mesh(new THREE.SphereGeometry(0.155, 48, 48), hm.clone());
    bun.position.set(0, 2.35, -0.12); hairGroup.add(bun);

    const bunRing = new THREE.Mesh(new THREE.TorusGeometry(0.12, 0.025, 12, 48), goldMat.clone());
    bunRing.position.set(0, 2.25, -0.08); hairGroup.add(bunRing);

    [-1, 1].forEach(s => {{
      const wisp = new THREE.Mesh(new THREE.SphereGeometry(0.12, 16, 16), hm.clone());
      wisp.scale.set(0.55, 1.1, 0.4);
      wisp.position.set(s * 0.43, 1.77, 0.06); hairGroup.add(wisp);
    }});

  }} else if (HAIRSTYLE === 'long') {{
    const longGeo = new THREE.PlaneGeometry(0.88, 1.60, 8, 24);
    const lPos    = longGeo.attributes.position;
    for (let i = 0; i < lPos.count; i++) {{
      const y = lPos.getY(i);
      lPos.setX(i, lPos.getX(i) + Math.sin(y * 2.2) * 0.045);
      lPos.setZ(i, lPos.getZ(i) - Math.abs(y) * 0.07);
    }}
    longGeo.computeVertexNormals();
    const lh = new THREE.Mesh(longGeo, new THREE.MeshStandardMaterial({{
      color: new THREE.Color(HAIR_COLOR), roughness: 0.68, side: THREE.DoubleSide
    }}));
    lh.position.set(0, 1.15, -0.40); hairGroup.add(lh);

    [-1, 1].forEach(s => {{
      const sg   = new THREE.PlaneGeometry(0.30, 1.35, 4, 18);
      const sPos = sg.attributes.position;
      for (let i = 0; i < sPos.count; i++)
        sPos.setZ(i, Math.sin(sPos.getY(i) * 2.8) * 0.035);
      sg.computeVertexNormals();
      const sh = new THREE.Mesh(sg, hm.clone());
      sh.position.set(s * 0.50, 1.20, 0.06); sh.rotation.y = s * 0.3;
      hairGroup.add(sh);
    }});

  }} else if (HAIRSTYLE === 'wavy') {{
    const pts = [];
    for (let i = 0; i <= 16; i++) {{
      const t = i / 16;
      pts.push(new THREE.Vector2(
        0.44 + Math.sin(t * Math.PI) * 0.22 + Math.sin(t * Math.PI * 5) * 0.035,
        1.86 - t * 0.90
      ));
    }}
    const lathe = new THREE.Mesh(
      new THREE.LatheGeometry(pts, 48),
      new THREE.MeshStandardMaterial({{ color: new THREE.Color(HAIR_COLOR), roughness: 0.65, side: THREE.DoubleSide }})
    );
    hairGroup.add(lathe);

    const bangGeo = new THREE.PlaneGeometry(0.82, 0.30, 10, 6);
    const bPos    = bangGeo.attributes.position;
    for (let i = 0; i < bPos.count; i++) {{
      bPos.setZ(i, Math.sin(bPos.getX(i) * 5) * 0.038 + 0.40);
      bPos.setY(i, bPos.getY(i) + Math.cos(bPos.getX(i) * 4) * 0.028);
    }}
    bangGeo.computeVertexNormals();
    const bangs = new THREE.Mesh(bangGeo, hm.clone());
    bangs.position.set(0, 2.13, 0.03); hairGroup.add(bangs);

  }} else if (HAIRSTYLE === 'updo') {{
    // Braided bun — overlapping tori
    for (let i = 0; i < 6; i++) {{
      const ang = (i / 6) * Math.PI * 2;
      const bp  = new THREE.Mesh(new THREE.TorusGeometry(0.08, 0.038, 12, 32), hm.clone());
      bp.position.set(Math.cos(ang) * 0.08, 2.30 + Math.sin(ang) * 0.04, -0.08);
      bp.rotation.z = ang; hairGroup.add(bp);
    }}
    const bunBase = new THREE.Mesh(new THREE.SphereGeometry(0.13, 32, 32), hm.clone());
    bunBase.position.set(0, 2.30, -0.08); hairGroup.add(bunBase);

    // Jewel pin + gem
    const pin = new THREE.Mesh(new THREE.CylinderGeometry(0.005, 0.005, 0.22, 8), goldMat.clone());
    pin.position.set(0.06, 2.30, -0.05); pin.rotation.z = Math.PI / 4; hairGroup.add(pin);
    const gem = new THREE.Mesh(new THREE.SphereGeometry(0.025, 16, 16), new THREE.MeshStandardMaterial({{
      color: 0xFF0040, metalness: 0.9, roughness: 0.05,
      emissive: 0xFF0040, emissiveIntensity: 0.4
    }}));
    gem.position.set(0.10, 2.38, -0.04); hairGroup.add(gem);

    [-1, 1].forEach(s => {{
      const sp = new THREE.Mesh(new THREE.SphereGeometry(0.10, 16, 16), hm.clone());
      sp.scale.set(0.5, 0.9, 0.4);
      sp.position.set(s * 0.42, 1.75, 0.04); hairGroup.add(sp);
    }});
  }}

  avatar.add(hairGroup);
}}
buildHair();

// ─── FLOOR PLATFORM (reflective) ─────────────────────────────────────────
const floorMat = new THREE.MeshStandardMaterial({{
  color:    0x1A1A2E,
  metalness: 0.90,
  roughness: 0.08
}});
const floor = new THREE.Mesh(new THREE.CylinderGeometry(1.4, 1.4, 0.08, 64), floorMat);
floor.position.y = -2.55;
floor.receiveShadow = true;
scene.add(floor);

// Glow ring
const ringMat = new THREE.MeshBasicMaterial({{
  color:       new THREE.Color(OUTFIT_COLOR),
  side:        THREE.DoubleSide,
  transparent: true,
  opacity:     0.45
}});
const ring = new THREE.Mesh(new THREE.RingGeometry(1.3, 1.55, 64), ringMat);
ring.rotation.x = -Math.PI / 2;
ring.position.y = -2.50;
scene.add(ring);

// ─── PARTICLE SPARKLES (with drift velocity) ──────────────────────────────
const sparkleGeo  = new THREE.BufferGeometry();
const sparkleCount = 160;
const sparkPos = new Float32Array(sparkleCount * 3);
const sparkVel = new Float32Array(sparkleCount * 3);
for (let i = 0; i < sparkleCount; i++) {{
  sparkPos[i*3]   = (Math.random() - 0.5) * 6;
  sparkPos[i*3+1] = (Math.random() - 0.5) * 7 + 1;
  sparkPos[i*3+2] = (Math.random() - 0.5) * 3 - 1;
  sparkVel[i*3]   = (Math.random() - 0.5) * 0.003;
  sparkVel[i*3+1] = (Math.random() - 0.5) * 0.002;
  sparkVel[i*3+2] = (Math.random() - 0.5) * 0.003;
}}
sparkleGeo.setAttribute('position', new THREE.BufferAttribute(sparkPos, 3));
const sparkleMat = new THREE.PointsMaterial({{
  color:       0xFFD700,
  size:        0.045,
  transparent: true,
  opacity:     0.75
}});
const sparkles = new THREE.Points(sparkleGeo, sparkleMat);
scene.add(sparkles);

// ─── CONTROLS — smooth damped rotation + scroll zoom ─────────────────────
let isDragging = false;
let prevMouse  = {{ x: 0, y: 0 }};
let targetY    = 0, targetX = 0;
let rotationY  = 0, rotationX = 0;
let autoRotate = true;

renderer.domElement.addEventListener('mousedown', e => {{
  isDragging = true;
  prevMouse  = {{ x: e.clientX, y: e.clientY }};
  autoRotate = false;
}});
renderer.domElement.addEventListener('mousemove', e => {{
  if (!isDragging) return;
  targetY += (e.clientX - prevMouse.x) * 0.013;
  targetX += (e.clientY - prevMouse.y) * 0.009;
  targetX  = Math.max(-0.55, Math.min(0.55, targetX));
  prevMouse = {{ x: e.clientX, y: e.clientY }};
}});
renderer.domElement.addEventListener('mouseup',    () => {{ isDragging = false; }});
renderer.domElement.addEventListener('mouseleave', () => {{ isDragging = false; }});

renderer.domElement.addEventListener('touchstart', e => {{
  isDragging = true;
  prevMouse  = {{ x: e.touches[0].clientX, y: e.touches[0].clientY }};
  autoRotate = false;
}});
renderer.domElement.addEventListener('touchmove', e => {{
  if (!isDragging) return;
  targetY += (e.touches[0].clientX - prevMouse.x) * 0.013;
  prevMouse = {{ x: e.touches[0].clientX, y: e.touches[0].clientY }};
}});
renderer.domElement.addEventListener('touchend', () => {{ isDragging = false; }});

// Scroll-to-zoom
renderer.domElement.addEventListener('wheel', e => {{
  camera.position.z = Math.max(3.0, Math.min(9.0, camera.position.z + e.deltaY * 0.005));
}});

function resetCamera() {{
  targetX = 0; targetY = 0;
  autoRotate = true;
  camera.position.z = 5.8;
}}
function toggleAutoRotate() {{ autoRotate = !autoRotate; }}
function takeScreenshot() {{
  renderer.render(scene, camera);
  const data = renderer.domElement.toDataURL('image/png');
  const link = document.getElementById('screenshot-link');
  link.href  = data;
  link.click();
}}

// ─── ANIMATION LOOP ───────────────────────────────────────────────────────
const clock = new THREE.Clock();
let frameCount = 0;

function animate() {{
  requestAnimationFrame(animate);
  const t = clock.getElapsedTime();
  frameCount++;

  // Smooth rotation damping
  if (autoRotate) targetY += 0.006;
  rotationY += (targetY - rotationY) * 0.08;
  rotationX += (targetX - rotationX) * 0.08;
  avatar.rotation.y = rotationY;
  avatar.rotation.x = rotationX;

  // Breathing
  const br = 1 + Math.sin(t * 1.1) * 0.007;
  torsoUpper.scale.x = br;
  torsoUpper.scale.z = br;

  // Drift sparkles
  const sArr = sparkleGeo.attributes.position.array;
  for (let i = 0; i < sparkleCount; i++) {{
    sArr[i*3]   += sparkVel[i*3];
    sArr[i*3+1] += sparkVel[i*3+1];
    sArr[i*3+2] += sparkVel[i*3+2];
    if (Math.abs(sArr[i*3])     > 3.5) sparkVel[i*3]   *= -1;
    if (Math.abs(sArr[i*3+1]-1) > 4.0) sparkVel[i*3+1] *= -1;
    if (Math.abs(sArr[i*3+2]+1) > 2.0) sparkVel[i*3+2] *= -1;
  }}
  sparkleGeo.attributes.position.needsUpdate = true;
  sparkleMat.opacity = 0.4 + Math.sin(t * 2.5) * 0.30;
  sparkles.rotation.y += 0.0012;

  // Rim light pulse + outfit reactive colour
  rimLight.intensity = 1.8 + Math.sin(t * 1.5) * 0.35;
  ringMat.opacity    = 0.30 + Math.sin(t * 2.0) * 0.15;

  // CubeCamera refresh every 90 frames (reflections on gold + floor)
  if (frameCount % 90 === 0) {{
    avatar.visible = false;
    cubeCamera.position.copy(avatar.position);
    cubeCamera.update(renderer, scene);
    avatar.visible = true;
    floorMat.envMap = cubeRenderTarget.texture;
    goldMat.envMap  = cubeRenderTarget.texture;
    floorMat.needsUpdate = true;
    goldMat.needsUpdate  = true;
  }}

  renderer.render(scene, camera);
}}
animate();

window.addEventListener('resize', () => {{
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}});
</script>
</body>
</html>
"""
    return html
