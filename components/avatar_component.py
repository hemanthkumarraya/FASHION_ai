<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Photorealistic Fashion Avatar</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=Syncopate:wght@400;700&display=swap');

  * { margin:0; padding:0; box-sizing:border-box; }

  body {
    background: #080808;
    overflow: hidden;
    font-family: 'Cormorant Garamond', serif;
    cursor: grab;
  }
  body:active { cursor: grabbing; }

  canvas { display:block; }

  /* ── TOP BAR ── */
  #brand {
    position: absolute;
    top: 24px; left: 50%;
    transform: translateX(-50%);
    font-family: 'Syncopate', sans-serif;
    font-size: 10px;
    letter-spacing: 6px;
    color: rgba(255,255,255,0.5);
    text-transform: uppercase;
    z-index: 20;
    pointer-events: none;
  }

  /* ── SIDE PANEL ── */
  #panel {
    position: absolute;
    right: 20px; top: 50%;
    transform: translateY(-50%);
    display: flex;
    flex-direction: column;
    gap: 10px;
    z-index: 20;
  }

  .section-label {
    font-family: 'Syncopate', sans-serif;
    font-size: 8px;
    letter-spacing: 3px;
    color: rgba(255,255,255,0.3);
    text-transform: uppercase;
    margin-bottom: 4px;
    margin-top: 10px;
  }

  .swatch-group {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .swatch {
    width: 28px; height: 28px;
    border-radius: 50%;
    cursor: pointer;
    border: 2px solid rgba(255,255,255,0.1);
    transition: all 0.25s;
    position: relative;
  }
  .swatch:hover, .swatch.active {
    border-color: rgba(255,255,255,0.8);
    transform: scale(1.15);
    box-shadow: 0 0 12px rgba(255,255,255,0.2);
  }

  .hair-btn {
    width: 28px; height: 28px;
    border-radius: 6px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.15);
    color: rgba(255,255,255,0.6);
    font-size: 14px;
    cursor: pointer;
    display: flex; align-items:center; justify-content:center;
    transition: all 0.2s;
  }
  .hair-btn:hover, .hair-btn.active {
    background: rgba(255,255,255,0.15);
    border-color: rgba(255,255,255,0.5);
    color: white;
  }

  /* ── BOTTOM CONTROLS ── */
  #controls {
    position: absolute;
    bottom: 24px; left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 12px;
    z-index: 20;
  }

  .ctrl {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.15);
    color: rgba(255,255,255,0.7);
    padding: 8px 20px;
    border-radius: 2px;
    font-family: 'Syncopate', sans-serif;
    font-size: 8px;
    letter-spacing: 2px;
    cursor: pointer;
    transition: all 0.2s;
    backdrop-filter: blur(10px);
  }
  .ctrl:hover {
    background: rgba(255,255,255,0.12);
    border-color: rgba(255,255,255,0.4);
    color: white;
  }

  /* ── LOADING ── */
  #loader {
    position: absolute; inset: 0;
    background: #080808;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 100;
    flex-direction: column;
    gap: 20px;
    transition: opacity 0.8s;
  }
  #loader.hide { opacity: 0; pointer-events: none; }

  .loader-text {
    font-family: 'Syncopate', sans-serif;
    font-size: 10px;
    letter-spacing: 6px;
    color: rgba(255,255,255,0.4);
  }

  .loader-bar {
    width: 200px; height: 1px;
    background: rgba(255,255,255,0.1);
    position: relative;
    overflow: hidden;
  }
  .loader-fill {
    height: 100%;
    background: linear-gradient(90deg, transparent, white, transparent);
    animation: scan 1.2s ease-in-out infinite;
  }
  @keyframes scan {
    from { transform: translateX(-100%); }
    to   { transform: translateX(200%); }
  }

  #screenshot-link { display:none; }
</style>
</head>
<body>

<div id="loader">
  <div class="loader-text">RENDERING AVATAR</div>
  <div class="loader-bar"><div class="loader-fill"></div></div>
</div>

<div id="brand">✦ COUTURE AVATAR STUDIO ✦</div>

<div id="panel">
  <div class="section-label">Skin</div>
  <div class="swatch-group" id="skin-swatches">
    <div class="swatch active" data-skin="#FDDBB4" style="background:#FDDBB4"></div>
    <div class="swatch" data-skin="#E8B88A" style="background:#E8B88A"></div>
    <div class="swatch" data-skin="#C68642" style="background:#C68642"></div>
    <div class="swatch" data-skin="#8D5524" style="background:#8D5524"></div>
    <div class="swatch" data-skin="#4A2912" style="background:#4A2912"></div>
  </div>

  <div class="section-label">Hair</div>
  <div class="swatch-group" id="hair-swatches">
    <div class="swatch active" data-hair="#1a0a00" style="background:#1a0a00"></div>
    <div class="swatch" data-hair="#4a2000" style="background:#4a2000"></div>
    <div class="swatch" data-hair="#8B6914" style="background:#8B6914"></div>
    <div class="swatch" data-hair="#D4AF37" style="background:#D4AF37"></div>
    <div class="swatch" data-hair="#C0392B" style="background:#C0392B"></div>
    <div class="swatch" data-hair="#2C3E50" style="background:#2C3E50"></div>
  </div>

  <div class="section-label">Style</div>
  <div class="swatch-group" id="hair-styles">
    <div class="hair-btn active" data-style="bun" title="Bun">🪢</div>
    <div class="hair-btn" data-style="long" title="Long">💇</div>
    <div class="hair-btn" data-style="wavy" title="Wavy">🌊</div>
    <div class="hair-btn" data-style="updo" title="Updo">👑</div>
  </div>

  <div class="section-label">Outfit</div>
  <div class="swatch-group" id="outfit-swatches">
    <div class="swatch active" data-outfit="#B71C8A" style="background:#B71C8A"></div>
    <div class="swatch" data-outfit="#1A237E" style="background:#1A237E"></div>
    <div class="swatch" data-outfit="#1B5E20" style="background:#1B5E20"></div>
    <div class="swatch" data-outfit="#B71C1C" style="background:#B71C1C"></div>
    <div class="swatch" data-outfit="#37474F" style="background:#37474F"></div>
    <div class="swatch" data-outfit="#880E4F" style="background:#880E4F"></div>
  </div>
</div>

<div id="controls">
  <button class="ctrl" onclick="resetCamera()">RESET VIEW</button>
  <button class="ctrl" onclick="toggleRotate()">AUTO ROTATE</button>
  <button class="ctrl" onclick="cycleEnv()">CHANGE ENV</button>
  <button class="ctrl" onclick="takeScreenshot()">CAPTURE</button>
</div>

<a id="screenshot-link" download="avatar.png"></a>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>

// ─── STATE ────────────────────────────────────────────────────────────────
let SKIN    = '#FDDBB4';
let HAIR    = '#1a0a00';
let OUTFIT  = '#B71C8A';
let STYLE   = 'bun';
let ENV_IDX = 0;

// ─── SCENE ────────────────────────────────────────────────────────────────
const scene = new THREE.Scene();
const W = window.innerWidth, H = window.innerHeight;

const renderer = new THREE.WebGLRenderer({
  antialias: true,
  alpha: false,
  preserveDrawingBuffer: true,
  logarithmicDepthBuffer: true
});
renderer.setSize(W, H);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.4;
renderer.outputEncoding = THREE.sRGBEncoding;
document.body.appendChild(renderer.domElement);

const camera = new THREE.PerspectiveCamera(38, W/H, 0.01, 100);
camera.position.set(0, 1.3, 5.8);
camera.lookAt(0, 0.9, 0);

// ─── ENVIRONMENT — Synthetic IBL via CubeCamera ─────────────────────────
// We generate a procedural gradient environment for reflections
const pmremGenerator = new THREE.PMREMGenerator ? new THREE.PMREMGenerator(renderer) : null;

function makeEnvTexture(topColor, midColor, botColor) {
  const size = 256;
  const canvas = document.createElement('canvas');
  canvas.width = size * 4; canvas.height = size * 3;
  const ctx = canvas.getContext('2d');

  // Fill all faces with gradient
  function drawFace(x, y, c1, c2) {
    const g = ctx.createLinearGradient(x, y, x, y + size);
    g.addColorStop(0, c1);
    g.addColorStop(1, c2);
    ctx.fillStyle = g;
    ctx.fillRect(x, y, size, size);
  }
  // +X, -X, +Y (top), -Y (bot), +Z, -Z
  drawFace(size*2, size,   midColor, botColor); // +X
  drawFace(0,      size,   midColor, botColor); // -X
  drawFace(size,   0,      topColor, topColor); // +Y
  drawFace(size,   size*2, botColor, botColor); // -Y
  drawFace(size,   size,   midColor, botColor); // +Z
  drawFace(size*3, size,   midColor, botColor); // -Z

  // Add studio highlights
  ctx.fillStyle = 'rgba(255,240,200,0.15)';
  ctx.fillRect(size*2, size, size/3, size);

  return new THREE.CanvasTexture(canvas);
}

const envConfigs = [
  // Studio
  { top:'#0a0a14', mid:'#141428', bot:'#0a0a0a', rimCol:0xFF69B4, rimInt:2.0, keyCol:0xFFF8F0, keyInt:2.2, fillCol:0xB0C8FF, fillInt:0.8 },
  // Golden hour
  { top:'#1a0a00', mid:'#3d1500', bot:'#080400', rimCol:0xFFAA00, rimInt:2.5, keyCol:0xFFCC66, keyInt:2.8, fillCol:0xFF7700, fillInt:0.5 },
  // Cool daylight
  { top:'#0a1525', mid:'#0f2040', bot:'#060d18', rimCol:0x00BFFF, rimInt:1.8, keyCol:0xE0F4FF, keyInt:2.0, fillCol:0x88CCFF, fillInt:0.7 },
  // Fashion runway
  { top:'#1a001a', mid:'#300030', bot:'#0d000d', rimCol:0xFF00AA, rimInt:3.0, keyCol:0xFFFFFF, keyInt:2.5, fillCol:0xFF88CC, fillInt:0.6 },
];

let currentEnv = 0;
function applyEnv(idx) {
  const e = envConfigs[idx];
  rimLight.color.setHex(e.rimCol);
  rimLight.intensity = e.rimInt;
  keyLight.color.setHex(e.keyCol);
  keyLight.intensity = e.keyInt;
  fillLight.color.setHex(e.fillCol);
  fillLight.intensity = e.fillInt;
  scene.background = new THREE.Color(e.top).lerp(new THREE.Color(e.bot), 0.5);
  scene.fog = new THREE.FogExp2(new THREE.Color(e.top), 0.025);
}

// ─── LIGHTS (photographic 3-point + rim + bounce) ─────────────────────────
const ambient = new THREE.AmbientLight(0xffffff, 0.15);
scene.add(ambient);

// KEY — main directional (slightly warm, top-left)
const keyLight = new THREE.DirectionalLight(0xFFF8F0, 2.2);
keyLight.position.set(-2.5, 5, 3.5);
keyLight.castShadow = true;
keyLight.shadow.mapSize.width  = 4096;
keyLight.shadow.mapSize.height = 4096;
keyLight.shadow.bias = -0.0002;
keyLight.shadow.camera.near = 0.5;
keyLight.shadow.camera.far  = 20;
keyLight.shadow.camera.left = keyLight.shadow.camera.bottom = -4;
keyLight.shadow.camera.right = keyLight.shadow.camera.top = 4;
scene.add(keyLight);

// FILL — softer, cool, opposite side
const fillLight = new THREE.DirectionalLight(0xB0C8FF, 0.8);
fillLight.position.set(3.5, 2, 2);
scene.add(fillLight);

// RIM / BACK — strong colored backlight (creates halo/separation)
const rimLight = new THREE.PointLight(0xFF69B4, 2.0, 15);
rimLight.position.set(0, 3.5, -4.5);
scene.add(rimLight);

// BOUNCE — simulates light bouncing from floor
const bounceLight = new THREE.PointLight(0xFFE0A0, 0.4, 6);
bounceLight.position.set(0, -4, 1.5);
scene.add(bounceLight);

// CATCH LIGHT — small, directly in front to create eye specular
const catchLight = new THREE.SpotLight(0xffffff, 0.5, 8, Math.PI/8, 0.5);
catchLight.position.set(0, 3, 4);
scene.add(catchLight);

applyEnv(0);

// ─── ENVIRONMENT MAP for reflections ─────────────────────────────────────
// CubeCamera to capture scene reflections dynamically
const cubeRenderTarget = new THREE.WebGLCubeRenderTarget(128, {
  format: THREE.RGBFormat,
  generateMipmaps: true,
  minFilter: THREE.LinearMipmapLinearFilter
});
const cubeCamera = new THREE.CubeCamera(0.1, 50, cubeRenderTarget);
scene.add(cubeCamera);

// ─── MATERIALS — PBR Photorealistic ───────────────────────────────────────

function makeSkinMat(color, isFace = false) {
  // Simulate subsurface scattering via emissive + low metalness + high roughness variation
  const c = new THREE.Color(color);
  const subsurface = c.clone().multiplyScalar(0.12); // warm inner glow
  return new THREE.MeshStandardMaterial({
    color: c,
    roughness: isFace ? 0.62 : 0.70,
    metalness: 0.0,
    emissive: subsurface,
    emissiveIntensity: 0.18,
  });
}

function makeOutfitMat(color, metalness = 0.15, roughness = 0.45) {
  return new THREE.MeshStandardMaterial({
    color: new THREE.Color(color),
    roughness, metalness,
    envMapIntensity: 0.8,
  });
}

const goldMat = new THREE.MeshStandardMaterial({
  color: 0xFFD700,
  metalness: 0.95,
  roughness: 0.08,
  envMapIntensity: 2.0,
});

// ─── AVATAR GROUP ─────────────────────────────────────────────────────────
const avatar = new THREE.Group();
scene.add(avatar);

// ─── FACE CANVAS TEXTURE (high-res, realistic) ─────────────────────────
function buildFaceTexture(skinColor, lipColor='#C0392B') {
  const size = 1024;
  const c = document.createElement('canvas');
  c.width = c.height = size;
  const ctx = c.getContext('2d');

  const sc = new THREE.Color(skinColor);
  const skinHex = '#' + sc.getHexString();

  // ── Base skin with subtle pore texture ──
  ctx.fillStyle = skinHex;
  ctx.fillRect(0, 0, size, size);

  // Pore noise (very subtle)
  for(let i=0; i<2000; i++){
    ctx.fillStyle = `rgba(0,0,0,${Math.random()*0.02})`;
    ctx.beginPath();
    ctx.arc(Math.random()*size, Math.random()*size, Math.random()*1.5, 0, Math.PI*2);
    ctx.fill();
  }

  // ── Forehead highlight ──
  const fhGrad = ctx.createRadialGradient(512,200,20,512,200,200);
  fhGrad.addColorStop(0,'rgba(255,255,255,0.12)');
  fhGrad.addColorStop(1,'rgba(255,255,255,0)');
  ctx.fillStyle = fhGrad;
  ctx.fillRect(0,0,size,size);

  // ── Cheek blush (SSS simulation) ──
  const blushL = ctx.createRadialGradient(260,430,10,260,430,110);
  blushL.addColorStop(0,'rgba(220,90,80,0.22)');
  blushL.addColorStop(0.5,'rgba(220,90,80,0.10)');
  blushL.addColorStop(1,'rgba(220,90,80,0)');
  ctx.fillStyle = blushL; ctx.fillRect(0,0,size,size);

  const blushR = ctx.createRadialGradient(752,430,10,752,430,110);
  blushR.addColorStop(0,'rgba(220,90,80,0.22)');
  blushR.addColorStop(0.5,'rgba(220,90,80,0.10)');
  blushR.addColorStop(1,'rgba(220,90,80,0)');
  ctx.fillStyle = blushR; ctx.fillRect(0,0,size,size);

  // ── Temple shadow (depth) ──
  const shadL = ctx.createRadialGradient(100,300,0,100,300,180);
  shadL.addColorStop(0,'rgba(0,0,0,0.18)'); shadL.addColorStop(1,'rgba(0,0,0,0)');
  ctx.fillStyle=shadL; ctx.fillRect(0,0,size,size);
  const shadR = ctx.createRadialGradient(900,300,0,900,300,180);
  shadR.addColorStop(0,'rgba(0,0,0,0.18)'); shadR.addColorStop(1,'rgba(0,0,0,0)');
  ctx.fillStyle=shadR; ctx.fillRect(0,0,size,size);

  // ── EYES ── (highly detailed)
  function drawEye(cx, cy, flip) {
    // Eye socket shadow
    const sockSh = ctx.createRadialGradient(cx,cy+10,10,cx,cy+10,75);
    sockSh.addColorStop(0,'rgba(0,0,0,0.25)'); sockSh.addColorStop(1,'rgba(0,0,0,0)');
    ctx.fillStyle=sockSh; ctx.fillRect(0,0,size,size);

    // Sclera (white with subtle veins)
    ctx.save();
    ctx.translate(cx, cy);
    ctx.scale(1.6, 1);
    ctx.beginPath(); ctx.arc(0,0,38,0,Math.PI*2); ctx.restore();
    ctx.fillStyle = '#f5f0ee';
    ctx.save(); ctx.translate(cx,cy); ctx.scale(1.6,1);
    ctx.beginPath(); ctx.ellipse(0,0,38,28,0,0,Math.PI*2); ctx.restore();
    ctx.fill();

    // Iris base
    const irisGrad = ctx.createRadialGradient(cx,cy-4,2,cx,cy,24);
    irisGrad.addColorStop(0,'#4a2c0a');
    irisGrad.addColorStop(0.4,'#2a1505');
    irisGrad.addColorStop(0.8,'#1a0d02');
    irisGrad.addColorStop(1,'#000000');
    ctx.beginPath(); ctx.arc(cx,cy,24,0,Math.PI*2);
    ctx.fillStyle=irisGrad; ctx.fill();

    // Iris detail (radial lines)
    for(let a=0;a<360;a+=12){
      const rad = a*Math.PI/180;
      ctx.strokeStyle = `rgba(100,60,10,0.4)`;
      ctx.lineWidth = 0.8;
      ctx.beginPath();
      ctx.moveTo(cx + Math.cos(rad)*8, cy + Math.sin(rad)*8);
      ctx.lineTo(cx + Math.cos(rad)*22, cy + Math.sin(rad)*22);
      ctx.stroke();
    }

    // Limbal ring
    ctx.beginPath(); ctx.arc(cx,cy,24,0,Math.PI*2);
    ctx.strokeStyle='rgba(0,0,0,0.7)'; ctx.lineWidth=2; ctx.stroke();

    // Pupil
    const pupilGrad = ctx.createRadialGradient(cx-2,cy-2,0,cx,cy,13);
    pupilGrad.addColorStop(0,'#1a1a1a'); pupilGrad.addColorStop(1,'#000000');
    ctx.beginPath(); ctx.arc(cx,cy,13,0,Math.PI*2);
    ctx.fillStyle=pupilGrad; ctx.fill();

    // Catchlight (key light)
    ctx.beginPath(); ctx.ellipse(cx+6, cy-8, 7, 5, -0.5, 0, Math.PI*2);
    ctx.fillStyle='rgba(255,255,255,0.92)'; ctx.fill();

    // Secondary catchlight (fill)
    ctx.beginPath(); ctx.arc(cx-8, cy+5, 4, 0, Math.PI*2);
    ctx.fillStyle='rgba(255,255,255,0.35)'; ctx.fill();

    // Eyelid crease
    ctx.strokeStyle='rgba(0,0,0,0.15)'; ctx.lineWidth=5;
    ctx.beginPath();
    ctx.moveTo(cx-48, cy-12);
    ctx.quadraticCurveTo(cx, cy-48, cx+48, cy-12);
    ctx.stroke();

    // Lashes (upper — dense)
    ctx.strokeStyle='#0a0505'; ctx.lineWidth=2.5;
    for(let i=-5;i<=5;i++){
      const t = i/5;
      const lx = cx + t*44;
      const ly = cy - Math.sqrt(1-t*t)*26;
      const ang = Math.atan2(-(cy-20)-ly, lx-cx) + (flip?0.15:-0.15);
      ctx.beginPath();
      ctx.moveTo(lx, ly);
      ctx.lineTo(lx + Math.cos(ang)*11, ly + Math.sin(ang)*11);
      ctx.stroke();
    }

    // Lashes (lower — sparse)
    ctx.lineWidth=1.5;
    ctx.strokeStyle='rgba(10,5,5,0.6)';
    for(let i=-3;i<=3;i++){
      const t = i/3;
      const lx = cx + t*35;
      const ly = cy + Math.sqrt(1-t*t)*24;
      ctx.beginPath();
      ctx.moveTo(lx, ly);
      ctx.lineTo(lx, ly+6);
      ctx.stroke();
    }
  }

  drawEye(300, 380, false);
  drawEye(724, 380, true);

  // ── EYEBROWS (natural arch) ──
  function drawBrow(cx, cy, flip){
    ctx.save();
    ctx.strokeStyle='#1a0d05';
    ctx.lineWidth=9; ctx.lineCap='round';
    // Main arch
    ctx.beginPath();
    if(!flip){
      ctx.moveTo(cx-70,cy+8); ctx.quadraticCurveTo(cx-20,cy-18,cx+55,cy+5);
    } else {
      ctx.moveTo(cx-55,cy+5); ctx.quadraticCurveTo(cx+20,cy-18,cx+70,cy+8);
    }
    ctx.stroke();
    // Hair strokes
    ctx.lineWidth=2; ctx.strokeStyle='rgba(20,10,3,0.4)';
    for(let s=0;s<12;s++){
      const t = s/11;
      const bx = cx + (flip?1:-1)*(55*t-35);
      const by = cy + Math.sin(t*Math.PI)*(-18)+5;
      ctx.beginPath();
      ctx.moveTo(bx, by+5);
      ctx.lineTo(bx + (Math.random()-0.5)*4, by-8);
      ctx.stroke();
    }
    ctx.restore();
  }
  drawBrow(300, 310, false);
  drawBrow(724, 310, true);

  // ── NOSE (realistic shading) ──
  // Nose bridge shadow
  const noseSh = ctx.createLinearGradient(480,310,540,310);
  noseSh.addColorStop(0,'rgba(0,0,0,0.12)'); noseSh.addColorStop(1,'rgba(0,0,0,0)');
  ctx.fillStyle=noseSh;
  ctx.fillRect(450,300,150,200);

  // Nostrils
  ctx.fillStyle='rgba(0,0,0,0.25)';
  ctx.beginPath(); ctx.ellipse(450,530,22,12,0.4,0,Math.PI*2); ctx.fill();
  ctx.beginPath(); ctx.ellipse(562,530,22,12,-0.4,0,Math.PI*2); ctx.fill();

  // Nose tip highlight
  const noseTip = ctx.createRadialGradient(506,510,2,506,510,30);
  noseTip.addColorStop(0,'rgba(255,255,255,0.18)');
  noseTip.addColorStop(1,'rgba(255,255,255,0)');
  ctx.fillStyle=noseTip; ctx.fillRect(0,0,size,size);

  // Nose bridge highlight
  const bridgeHL = ctx.createLinearGradient(495,300,518,300);
  bridgeHL.addColorStop(0,'rgba(255,255,255,0)');
  bridgeHL.addColorStop(0.5,'rgba(255,255,255,0.15)');
  bridgeHL.addColorStop(1,'rgba(255,255,255,0)');
  ctx.fillStyle=bridgeHL; ctx.fillRect(490,300,35,180); // narrower

  // ── LIPS (full, realistic) ──
  const lipC = new THREE.Color(lipColor);
  const lipHex = '#'+lipC.getHexString();

  function shadeHex(hex, pct){
    const n=parseInt(hex.replace('#',''),16);
    const r=Math.min(255,Math.max(0,(n>>16)+pct));
    const g=Math.min(255,Math.max(0,((n>>8)&0xFF)+pct));
    const b=Math.min(255,Math.max(0,(n&0xFF)+pct));
    return '#'+((1<<24)+(r<<16)+(g<<8)+b).toString(16).slice(1);
  }

  // Lip shadow
  ctx.fillStyle='rgba(0,0,0,0.12)';
  ctx.beginPath();
  ctx.ellipse(512, 650, 120, 65, 0, 0, Math.PI*2);
  ctx.fill();

  // Lower lip
  ctx.fillStyle=lipHex;
  ctx.beginPath();
  ctx.moveTo(370,625);
  ctx.bezierCurveTo(420,600,480,595,512,598);
  ctx.bezierCurveTo(544,595,604,600,654,625);
  ctx.bezierCurveTo(640,670,580,700,512,702);
  ctx.bezierCurveTo(444,700,384,670,370,625);
  ctx.fill();

  // Upper lip (cupid's bow)
  ctx.fillStyle=shadeHex(lipHex,-20);
  ctx.beginPath();
  ctx.moveTo(370,625);
  ctx.bezierCurveTo(400,610,450,600,480,608);
  ctx.bezierCurveTo(496,612,506,605,512,604);
  ctx.bezierCurveTo(518,605,528,612,544,608);
  ctx.bezierCurveTo(574,600,624,610,654,625);
  ctx.bezierCurveTo(620,618,560,612,512,615);
  ctx.bezierCurveTo(464,612,404,618,370,625);
  ctx.fill();

  // Lip center line
  ctx.strokeStyle='rgba(0,0,0,0.2)';
  ctx.lineWidth=1.5;
  ctx.beginPath();
  ctx.moveTo(370,625); ctx.bezierCurveTo(440,622,490,620,512,619);
  ctx.bezierCurveTo(534,620,584,622,654,625); ctx.stroke();

  // Lip gloss highlight
  const gloss = ctx.createRadialGradient(512,648,5,512,648,55);
  gloss.addColorStop(0,'rgba(255,255,255,0.38)');
  gloss.addColorStop(0.5,'rgba(255,255,255,0.12)');
  gloss.addColorStop(1,'rgba(255,255,255,0)');
  ctx.fillStyle=gloss; ctx.fillRect(0,0,size,size);

  // Upper lip gloss
  const gloss2 = ctx.createRadialGradient(512,612,3,512,612,25);
  gloss2.addColorStop(0,'rgba(255,255,255,0.22)');
  gloss2.addColorStop(1,'rgba(255,255,255,0)');
  ctx.fillStyle=gloss2; ctx.fillRect(0,0,size,size);

  return new THREE.CanvasTexture(c);
}

// ─── HEAD ─────────────────────────────────────────────────────────────────
const headGeo = new THREE.SphereGeometry(0.42, 128, 128);
// Subtle head shape adjustment (less perfect sphere)
const headPos = headGeo.attributes.position;
for(let i=0; i<headPos.count; i++){
  const y = headPos.getY(i);
  const x = headPos.getX(i);
  const z = headPos.getZ(i);
  // Slightly flatten top, widen cheeks
  const lat = Math.asin(y / 0.42);
  const flatTop = y > 0.3 ? y - (y-0.3)*0.12 : y;
  const cheekWide = Math.abs(lat) < 0.4 ? 1.04 : 1.0;
  headPos.setXYZ(i, x*cheekWide, flatTop, z*cheekWide);
}
headGeo.computeVertexNormals();

const headMat = makeSkinMat(SKIN, true);
const head = new THREE.Mesh(headGeo, headMat);
head.position.y = 1.85;
head.castShadow = true;
avatar.add(head);

// Initial face texture
let faceTexture = buildFaceTexture(SKIN);
headMat.map = faceTexture;
headMat.needsUpdate = true;

// ─── NECK ─────────────────────────────────────────────────────────────────
const neckGeo = new THREE.CylinderGeometry(0.115, 0.14, 0.30, 64);
const neckMat = makeSkinMat(SKIN);
const neck = new THREE.Mesh(neckGeo, neckMat);
neck.position.y = 1.30;
neck.castShadow = true;
avatar.add(neck);

// ─── TORSO (PBR fabric) ────────────────────────────────────────────────────
let torsoMats = [];

function makeTorso(outfitColor) {
  // Remove old
  ['torsoU','torsoL','pallu','border','skirt','hem','blouse'].forEach(n=>{
    const o=avatar.getObjectByName(n); if(o) avatar.remove(o);
  });
  torsoMats = [];

  const oc = new THREE.MeshStandardMaterial({
    color: new THREE.Color(outfitColor),
    roughness: 0.52, metalness: 0.08,
    envMapIntensity: 0.6,
  });
  torsoMats.push(oc);

  // Shoulders with realistic curve
  const shoulderGeo = new THREE.CylinderGeometry(0.54, 0.37, 0.62, 64);
  const tu = new THREE.Mesh(shoulderGeo, oc.clone());
  tu.name = 'torsoU'; tu.position.y = 0.90; tu.castShadow = true;
  avatar.add(tu);

  // Waist
  const waistGeo = new THREE.CylinderGeometry(0.37, 0.41, 0.52, 64);
  const tl = new THREE.Mesh(waistGeo, oc.clone());
  tl.name = 'torsoL'; tl.position.y = 0.33; tl.castShadow = true;
  avatar.add(tl);

  // Blouse detail — neckline
  const blouseGeo = new THREE.TorusGeometry(0.24, 0.035, 16, 64);
  const blouseMat = new THREE.MeshStandardMaterial({
    color: new THREE.Color(outfitColor).multiplyScalar(0.85),
    roughness:0.4, metalness:0.2
  });
  const blouse = new THREE.Mesh(blouseGeo, blouseMat);
  blouse.name='blouse'; blouse.position.y=1.18; blouse.rotation.x=Math.PI/2;
  avatar.add(blouse);

  // Saree pallu with wave deformation
  const palluGeo = new THREE.PlaneGeometry(0.58, 1.45, 10, 24);
  const palluPos = palluGeo.attributes.position;
  for(let i=0;i<palluPos.count;i++){
    const y=palluPos.getY(i), x=palluPos.getX(i);
    palluPos.setZ(i, Math.sin(y*3.5)*0.055 + Math.cos(x*5)*0.03);
  }
  palluGeo.computeVertexNormals();
  const sareeMat = new THREE.MeshStandardMaterial({
    color: new THREE.Color(outfitColor),
    roughness:0.38, metalness:0.28,
    transparent:true, opacity:0.92,
    side:THREE.DoubleSide,
    envMapIntensity: 1.0
  });
  const pallu = new THREE.Mesh(palluGeo, sareeMat);
  pallu.name='pallu'; pallu.position.set(-0.28,0.58,0.42); pallu.rotation.z=0.12;
  avatar.add(pallu);

  // Gold zari border
  const border = new THREE.Mesh(new THREE.PlaneGeometry(0.06,1.45), goldMat.clone());
  border.name='border'; border.position.set(-0.57,0.58,0.43); border.rotation.z=0.12;
  avatar.add(border);

  // Skirt — high-poly with folds
  const skirtGeo = new THREE.CylinderGeometry(0.60, 0.76, 1.7, 64, 12, true);
  const skPos = skirtGeo.attributes.position;
  for(let i=0;i<skPos.count;i++){
    const a=Math.atan2(skPos.getX(i),skPos.getZ(i));
    const y=skPos.getY(i);
    const foldAmt = 0.018 + (y<-0.5?0.012:0);
    skPos.setX(i, skPos.getX(i)+Math.sin(a*8)*foldAmt);
    skPos.setZ(i, skPos.getZ(i)+Math.cos(a*8)*foldAmt*0.5);
  }
  skirtGeo.computeVertexNormals();
  const skirtMat = new THREE.MeshStandardMaterial({
    color: new THREE.Color(outfitColor),
    roughness:0.48, metalness:0.12,
    side:THREE.DoubleSide,
    envMapIntensity:0.5
  });
  const skirt=new THREE.Mesh(skirtGeo,skirtMat);
  skirt.name='skirt'; skirt.position.y=-0.75; skirt.castShadow=true;
  avatar.add(skirt);

  // Gold hem
  const hem=new THREE.Mesh(new THREE.TorusGeometry(0.73,0.022,10,96),goldMat.clone());
  hem.name='hem'; hem.position.y=-1.60;
  avatar.add(hem);
}
makeTorso(OUTFIT);

// ─── ARMS ─────────────────────────────────────────────────────────────────
function makeArms(skinColor, outfitColor) {
  ['armL','armR'].forEach(n=>{ const o=avatar.getObjectByName(n); if(o) avatar.remove(o); });

  function arm(side){
    const g=new THREE.Group();
    g.name = side>0 ? 'armR' : 'armL';
    const sx=side*0.70;
    const sm=makeSkinMat(skinColor);
    const om=makeOutfitMat(outfitColor, 0.1, 0.5);

    // Sleeve (upper arm)
    const sleeve=new THREE.Mesh(new THREE.CylinderGeometry(0.11,0.10,0.52,32), om.clone());
    sleeve.position.set(sx,0.76,0); sleeve.rotation.z=side*0.22; g.add(sleeve);

    // Upper arm skin (visible at wrist)
    const ua=new THREE.Mesh(new THREE.CylinderGeometry(0.095,0.085,0.50,32),sm.clone());
    ua.position.set(sx*1.10,0.34,0.03); ua.rotation.z=side*0.34; ua.castShadow=true; g.add(ua);

    // Wrist
    const wrist=new THREE.Mesh(new THREE.CylinderGeometry(0.072,0.068,0.14,32),sm.clone());
    wrist.position.set(sx*1.20,0.06,0.07); wrist.rotation.z=side*0.38; g.add(wrist);

    // Hand (more detailed)
    const hand=new THREE.Mesh(new THREE.SphereGeometry(0.082,32,32),sm.clone());
    hand.scale.set(1,0.75,0.9);
    hand.position.set(sx*1.28,-0.06,0.10); hand.castShadow=true; g.add(hand);

    // Bangles (3 gold + 1 colored)
    [0.12,0.18,0.24].forEach((oy,i)=>{
      const b=new THREE.Mesh(new THREE.TorusGeometry(0.072,0.013,10,48),i===1?new THREE.MeshStandardMaterial({color:new THREE.Color(outfitColor),metalness:0.6,roughness:0.3}):goldMat.clone());
      b.position.set(sx*1.24,oy,0.07); b.rotation.x=Math.PI/2; g.add(b);
    });

    avatar.add(g);
  }
  arm(1); arm(-1);
}
makeArms(SKIN, OUTFIT);

// ─── EARS & EARRINGS ──────────────────────────────────────────────────────
[-1,1].forEach(s=>{
  const earGeo = new THREE.SphereGeometry(0.074, 32, 32);
  const ear = new THREE.Mesh(earGeo, makeSkinMat(SKIN));
  ear.scale.z=0.45; ear.position.set(s*0.43,1.85,0); avatar.add(ear);

  // Earring stud
  const stud=new THREE.Mesh(new THREE.SphereGeometry(0.028,16,16),goldMat.clone());
  stud.position.set(s*0.45,1.82,0); avatar.add(stud);

  // Drop chain
  const chainGeo=new THREE.CylinderGeometry(0.004,0.004,0.12,8);
  const chain=new THREE.Mesh(chainGeo,goldMat.clone());
  chain.position.set(s*0.46,1.72,0); avatar.add(chain);

  // Teardrop pendant
  const drop=new THREE.Mesh(new THREE.SphereGeometry(0.038,16,16),goldMat.clone());
  drop.scale.y=1.4; drop.position.set(s*0.46,1.63,0); avatar.add(drop);
});

// ─── BINDI ─────────────────────────────────────────────────────────────────
const bindi=new THREE.Mesh(new THREE.CircleGeometry(0.025,32),new THREE.MeshStandardMaterial({color:0xFF0040,metalness:0.8,roughness:0.1,emissive:0xFF0040,emissiveIntensity:0.3}));
bindi.position.set(0,2.075,0.420); avatar.add(bindi);

// ─── HAIR SYSTEM ──────────────────────────────────────────────────────────
let hairGroup = null;

function buildHair(style, hairColor) {
  if(hairGroup) avatar.remove(hairGroup);
  hairGroup = new THREE.Group();
  hairGroup.name='hairGroup';

  const hm = new THREE.MeshStandardMaterial({
    color: new THREE.Color(hairColor),
    roughness: 0.72,
    metalness: 0.02,
    envMapIntensity: 0.3,
  });

  // Hair cap (always present)
  const capGeo = new THREE.SphereGeometry(0.445, 64, 64, 0, Math.PI*2, 0, Math.PI*0.55);
  const cap = new THREE.Mesh(capGeo, hm.clone());
  cap.position.y = 1.86;
  hairGroup.add(cap);

  if(style === 'bun') {
    // Bun on top-back
    const bun=new THREE.Mesh(new THREE.SphereGeometry(0.155,48,48),hm.clone());
    bun.position.set(0,2.35,-0.12); hairGroup.add(bun);
    // Bun ring
    const bunRing=new THREE.Mesh(new THREE.TorusGeometry(0.12,0.025,12,48),goldMat.clone());
    bunRing.position.set(0,2.25,-0.08); hairGroup.add(bunRing);
    // Side wisps
    [-1,1].forEach(s=>{
      const wisp=new THREE.Mesh(new THREE.SphereGeometry(0.12,16,16),hm.clone());
      wisp.scale.set(0.55,1.1,0.4);
      wisp.position.set(s*0.43,1.77,0.06); hairGroup.add(wisp);
    });

  } else if(style === 'long') {
    // Long straight
    const longGeo = new THREE.PlaneGeometry(0.88, 1.6, 8, 24);
    const lPos=longGeo.attributes.position;
    for(let i=0;i<lPos.count;i++){
      const y=lPos.getY(i);
      lPos.setX(i,lPos.getX(i)+Math.sin(y*2.2)*0.045);
      lPos.setZ(i,lPos.getZ(i)-Math.abs(y)*0.07);
    }
    longGeo.computeVertexNormals();
    const lh=new THREE.Mesh(longGeo,new THREE.MeshStandardMaterial({color:new THREE.Color(hairColor),roughness:0.68,side:THREE.DoubleSide}));
    lh.position.set(0,1.15,-0.40); hairGroup.add(lh);
    // Side strands
    [-1,1].forEach(s=>{
      const sg=new THREE.PlaneGeometry(0.30,1.35,4,18);
      const sPos=sg.attributes.position;
      for(let i=0;i<sPos.count;i++) sPos.setZ(i,Math.sin(sPos.getY(i)*2.8)*0.035);
      sg.computeVertexNormals();
      const sh=new THREE.Mesh(sg,hm.clone());
      sh.position.set(s*0.50,1.20,0.06); sh.rotation.y=s*0.3; hairGroup.add(sh);
    });

  } else if(style === 'wavy') {
    // Wavy bob via lathe
    const pts=[];
    for(let i=0;i<=16;i++){
      const t=i/16;
      pts.push(new THREE.Vector2(0.44+Math.sin(t*Math.PI)*0.22+Math.sin(t*Math.PI*5)*0.035, 1.86-t*0.90));
    }
    const lathe=new THREE.Mesh(new THREE.LatheGeometry(pts,48),new THREE.MeshStandardMaterial({color:new THREE.Color(hairColor),roughness:0.65,side:THREE.DoubleSide}));
    hairGroup.add(lathe);
    // Bangs
    const bangGeo=new THREE.PlaneGeometry(0.82,0.30,10,6);
    const bPos=bangGeo.attributes.position;
    for(let i=0;i<bPos.count;i++){
      bPos.setZ(i,Math.sin(bPos.getX(i)*5)*0.038+0.40);
      bPos.setY(i,bPos.getY(i)+Math.cos(bPos.getX(i)*4)*0.028);
    }
    bangGeo.computeVertexNormals();
    const bangs=new THREE.Mesh(bangGeo,hm.clone());
    bangs.position.set(0,2.13,0.03); hairGroup.add(bangs);

  } else if(style === 'updo') {
    // Updo with braided bun
    // Twisted bun (multiple overlapping tori)
    for(let i=0;i<6;i++){
      const ang=i/6*Math.PI*2;
      const bp=new THREE.Mesh(new THREE.TorusGeometry(0.08,0.038,12,32),hm.clone());
      bp.position.set(Math.cos(ang)*0.08,2.30+Math.sin(ang)*0.04,-0.08);
      bp.rotation.z=ang; hairGroup.add(bp);
    }
    const bunBase=new THREE.Mesh(new THREE.SphereGeometry(0.13,32,32),hm.clone());
    bunBase.position.set(0,2.30,-0.08); hairGroup.add(bunBase);
    // Jewel pin
    const pin=new THREE.Mesh(new THREE.CylinderGeometry(0.005,0.005,0.22,8),goldMat.clone());
    pin.position.set(0.06,2.30,-0.05); pin.rotation.z=Math.PI/4; hairGroup.add(pin);
    const gem=new THREE.Mesh(new THREE.SphereGeometry(0.025,16,16),new THREE.MeshStandardMaterial({color:0xFF0040,metalness:0.9,roughness:0.05,emissive:0xFF0040,emissiveIntensity:0.4}));
    gem.position.set(0.10,2.38,-0.04); hairGroup.add(gem);
    // Side pulls
    [-1,1].forEach(s=>{
      const sp=new THREE.Mesh(new THREE.SphereGeometry(0.10,16,16),hm.clone());
      sp.scale.set(0.5,0.9,0.4); sp.position.set(s*0.42,1.75,0.04); hairGroup.add(sp);
    });
  }

  avatar.add(hairGroup);
}
buildHair(STYLE, HAIR);

// ─── FLOOR & STAGE ─────────────────────────────────────────────────────────
// Reflective floor platform
const floorMat = new THREE.MeshStandardMaterial({
  color: 0x0a0a14,
  metalness: 0.95,
  roughness: 0.05,
  envMapIntensity: 2.0,
});
const floor = new THREE.Mesh(new THREE.CylinderGeometry(1.6,1.6,0.06,128), floorMat);
floor.position.y = -2.56; floor.receiveShadow = true; scene.add(floor);

// Subtle floor reflection (mirror plane)
const mirrorFloor = new THREE.Mesh(
  new THREE.CircleGeometry(1.58, 128),
  new THREE.MeshStandardMaterial({ color:0x050510, metalness:1.0, roughness:0.02 })
);
mirrorFloor.rotation.x=-Math.PI/2; mirrorFloor.position.y=-2.52; scene.add(mirrorFloor);

// Glow ring
const ringMat=new THREE.MeshBasicMaterial({color:new THREE.Color(OUTFIT),side:THREE.DoubleSide,transparent:true,opacity:0.45});
const ring=new THREE.Mesh(new THREE.RingGeometry(1.4,1.62,128),ringMat);
ring.rotation.x=-Math.PI/2; ring.position.y=-2.50; scene.add(ring);

// ─── PARTICLE SYSTEM (sparkles) ────────────────────────────────────────────
const sparkGeo = new THREE.BufferGeometry();
const sparkN   = 200;
const sparkPos = new Float32Array(sparkN*3);
const sparkVel = new Float32Array(sparkN*3);
for(let i=0;i<sparkN;i++){
  sparkPos[i*3]   = (Math.random()-0.5)*7;
  sparkPos[i*3+1] = (Math.random()-0.5)*8 + 1;
  sparkPos[i*3+2] = (Math.random()-0.5)*4 - 1;
  sparkVel[i*3]   = (Math.random()-0.5)*0.003;
  sparkVel[i*3+1] = (Math.random()-0.5)*0.002;
  sparkVel[i*3+2] = (Math.random()-0.5)*0.003;
}
sparkGeo.setAttribute('position', new THREE.BufferAttribute(sparkPos,3));
const sparkMat=new THREE.PointsMaterial({color:0xFFD700,size:0.05,transparent:true,opacity:0.8,sizeAttenuation:true});
const sparks=new THREE.Points(sparkGeo,sparkMat);
scene.add(sparks);

// ─── CONTROLS ─────────────────────────────────────────────────────────────
let isDragging=false, prevMouse={x:0,y:0}, rotY=0, rotX=0, autoRot=true;
let targetY=0, targetX=0; // smooth damping

renderer.domElement.addEventListener('mousedown',e=>{isDragging=true;prevMouse={x:e.clientX,y:e.clientY};autoRot=false;});
renderer.domElement.addEventListener('mousemove',e=>{
  if(!isDragging)return;
  targetY+=(e.clientX-prevMouse.x)*0.014;
  targetX+=(e.clientY-prevMouse.y)*0.009;
  targetX=Math.max(-0.55,Math.min(0.55,targetX));
  prevMouse={x:e.clientX,y:e.clientY};
});
renderer.domElement.addEventListener('mouseup',()=>isDragging=false);
renderer.domElement.addEventListener('mouseleave',()=>isDragging=false);
renderer.domElement.addEventListener('touchstart',e=>{isDragging=true;prevMouse={x:e.touches[0].clientX,y:e.touches[0].clientY};autoRot=false;});
renderer.domElement.addEventListener('touchmove',e=>{
  if(!isDragging)return;
  targetY+=(e.touches[0].clientX-prevMouse.x)*0.014;
  prevMouse={x:e.touches[0].clientX,y:e.touches[0].clientY};
});
renderer.domElement.addEventListener('touchend',()=>isDragging=false);

// Scroll zoom
renderer.domElement.addEventListener('wheel',e=>{
  camera.position.z=Math.max(3,Math.min(9,camera.position.z+e.deltaY*0.005));
});

function resetCamera(){targetX=0;targetY=0;autoRot=true;camera.position.z=5.8;}
function toggleRotate(){autoRot=!autoRot;}
function cycleEnv(){currentEnv=(currentEnv+1)%envConfigs.length;applyEnv(currentEnv);}
function takeScreenshot(){renderer.render(scene,camera);const d=renderer.domElement.toDataURL('image/png');const l=document.getElementById('screenshot-link');l.href=d;l.click();}

// ─── UI SWATCH LOGIC ──────────────────────────────────────────────────────
document.querySelectorAll('#skin-swatches .swatch').forEach(s=>{
  s.addEventListener('click',()=>{
    document.querySelectorAll('#skin-swatches .swatch').forEach(x=>x.classList.remove('active'));
    s.classList.add('active');
    SKIN = s.dataset.skin;
    // Update all skin materials
    head.material.color.set(SKIN);
    const ss = new THREE.Color(SKIN).multiplyScalar(0.12);
    head.material.emissive.set(ss);
    head.material.map = buildFaceTexture(SKIN);
    head.material.needsUpdate = true;
    neck.material.color.set(SKIN);
    makeArms(SKIN, OUTFIT);
  });
});

document.querySelectorAll('#hair-swatches .swatch').forEach(s=>{
  s.addEventListener('click',()=>{
    document.querySelectorAll('#hair-swatches .swatch').forEach(x=>x.classList.remove('active'));
    s.classList.add('active');
    HAIR = s.dataset.hair;
    buildHair(STYLE, HAIR);
  });
});

document.querySelectorAll('#hair-styles .hair-btn').forEach(b=>{
  b.addEventListener('click',()=>{
    document.querySelectorAll('#hair-styles .hair-btn').forEach(x=>x.classList.remove('active'));
    b.classList.add('active');
    STYLE = b.dataset.style;
    buildHair(STYLE, HAIR);
  });
});

document.querySelectorAll('#outfit-swatches .swatch').forEach(s=>{
  s.addEventListener('click',()=>{
    document.querySelectorAll('#outfit-swatches .swatch').forEach(x=>x.classList.remove('active'));
    s.classList.add('active');
    OUTFIT = s.dataset.outfit;
    makeTorso(OUTFIT);
    makeArms(SKIN, OUTFIT);
    ring.material.color.set(new THREE.Color(OUTFIT));
    rimLight.color.setHex(parseInt(OUTFIT.replace('#',''),16));
  });
});

// ─── ANIMATION ────────────────────────────────────────────────────────────
const clock = new THREE.Clock();
let loaded = false;

function animate() {
  requestAnimationFrame(animate);
  const t = clock.getElapsedTime();

  // Hide loader after first frame
  if(!loaded){ loaded=true; setTimeout(()=>document.getElementById('loader').classList.add('hide'),600); }

  // Smooth rotation damping
  if(autoRot) targetY += 0.006;
  rotY += (targetY - rotY) * 0.08;
  rotX += (targetX - rotX) * 0.08;
  avatar.rotation.y = rotY;
  avatar.rotation.x = rotX;

  // Breathing
  const br = 1 + Math.sin(t*1.1)*0.007;
  const torsoU = avatar.getObjectByName('torsoU');
  if(torsoU){ torsoU.scale.x=br; torsoU.scale.z=br; }

  // Gentle arm sway
  const armR = avatar.getObjectByName('armR');
  const armL = avatar.getObjectByName('armL');
  if(armR) armR.rotation.z = Math.sin(t*0.8)*0.018;
  if(armL) armL.rotation.z = Math.sin(t*0.8+Math.PI)*0.018;

  // Sparkle animation
  const sPos = sparkGeo.attributes.position.array;
  for(let i=0;i<sparkN;i++){
    sPos[i*3]   += sparkVel[i*3];
    sPos[i*3+1] += sparkVel[i*3+1];
    sPos[i*3+2] += sparkVel[i*3+2];
    // Bounds reset
    if(Math.abs(sPos[i*3])>3.5) sparkVel[i*3]*=-1;
    if(Math.abs(sPos[i*3+1]-1)>4) sparkVel[i*3+1]*=-1;
    if(Math.abs(sPos[i*3+2]+1)>2) sparkVel[i*3+2]*=-1;
  }
  sparkGeo.attributes.position.needsUpdate = true;
  sparkMat.opacity = 0.4 + Math.sin(t*2.5)*0.3;
  sparks.rotation.y += 0.0012;

  // Rim light pulse
  rimLight.intensity = envConfigs[currentEnv].rimInt * (0.85 + Math.sin(t*1.8)*0.15);

  // Glow ring pulse
  ring.material.opacity = 0.3 + Math.sin(t*2)*0.15;

  // Update cube camera for reflections (every 60 frames)
  if(Math.round(t*60)%60===0){
    avatar.visible=false;
    cubeCamera.position.copy(avatar.position);
    cubeCamera.update(renderer, scene);
    avatar.visible=true;
    // Apply env map to reflective materials
    floorMat.envMap = cubeRenderTarget.texture;
    goldMat.envMap  = cubeRenderTarget.texture;
    floorMat.needsUpdate=true;
    goldMat.needsUpdate=true;
  }

  renderer.render(scene, camera);
}
animate();

window.addEventListener('resize',()=>{
  camera.aspect=window.innerWidth/window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth,window.innerHeight);
});
</script>
</body>
</html>
