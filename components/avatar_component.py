def get_avatar_html(hairstyle="bun", hair_color="#1a1a1a",
                    skin_tone="#F5CBA7", outfit_color="#E91E8C",
                    lip_color="#C0392B"):
    """
    Returns a complete self-contained Three.js fashion avatar HTML string.
    Parameters are injected as JS variables for real-time customization.
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

    #screenshot-link {{
      display: none;
    }}
  </style>
</head>
<body>

<div id="info-tag">✨ FASHION AVATAR — DRAG TO ROTATE</div>

<div id="controls-overlay">
  <button class="ctrl-btn" onclick="resetCamera()">🎯 Reset View</button>
  <button class="ctrl-btn" onclick="toggleAutoRotate()">🔄 Auto Rotate</button>
  <button class="ctrl-btn" onclick="takeScreenshot()">📸 Screenshot</button>
</div>

<a id="screenshot-link" download="fashion_avatar.png"></a>

<!-- Three.js CDN -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

<script>
// ─── INJECTED PARAMETERS FROM PYTHON ──────────────────────────────────────
const HAIRSTYLE   = "{hairstyle}";
const HAIR_COLOR  = "{hair_color}";
const SKIN_TONE   = "{skin_tone}";
const OUTFIT_COLOR= "{outfit_color}";
const LIP_COLOR   = "{lip_color}";

// ─── SCENE SETUP ──────────────────────────────────────────────────────────
const scene    = new THREE.Scene();
scene.fog      = new THREE.FogExp2(0x0D0D0D, 0.035);

const W = window.innerWidth;
const H = window.innerHeight;

const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true, preserveDrawingBuffer: true }});
renderer.setSize(W, H);
renderer.setPixelRatio(window.devicePixelRatio);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type    = THREE.PCFSoftShadowMap;
renderer.toneMapping       = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
document.body.appendChild(renderer.domElement);

const camera = new THREE.PerspectiveCamera(42, W / H, 0.1, 100);
camera.position.set(0, 1.2, 5.5);
camera.lookAt(0, 0.8, 0);

// ─── LIGHTING (Fashion Studio Setup) ──────────────────────────────────────
// Soft ambient
const ambient = new THREE.AmbientLight(0xffffff, 0.4);
scene.add(ambient);

// Key light (top-left, warm)
const keyLight = new THREE.DirectionalLight(0xFFF5E1, 1.6);
keyLight.position.set(-3, 5, 4);
keyLight.castShadow = true;
keyLight.shadow.mapSize.width  = 2048;
keyLight.shadow.mapSize.height = 2048;
scene.add(keyLight);

// Fill light (right, cool)
const fillLight = new THREE.DirectionalLight(0xC9E8FF, 0.7);
fillLight.position.set(4, 2, 2);
scene.add(fillLight);

// Rim / back light (pink — fashion glow)
const rimLight = new THREE.PointLight(0xFF69B4, 1.5, 12);
rimLight.position.set(0, 3, -4);
scene.add(rimLight);

// Bottom bounce
const bounceLight = new THREE.PointLight(0xFFD700, 0.4, 8);
bounceLight.position.set(0, -3, 2);
scene.add(bounceLight);

// ─── FLOOR PLATFORM ───────────────────────────────────────────────────────
const floorGeo = new THREE.CylinderGeometry(1.4, 1.4, 0.08, 64);
const floorMat = new THREE.MeshStandardMaterial({{
  color: 0x1A1A2E,
  metalness: 0.6,
  roughness: 0.3,
}});
const floor = new THREE.Mesh(floorGeo, floorMat);
floor.position.y = -2.55;
floor.receiveShadow = true;
scene.add(floor);

// Floor glow ring
const ringGeo = new THREE.RingGeometry(1.3, 1.5, 64);
const ringMat = new THREE.MeshBasicMaterial({{
  color: new THREE.Color(OUTFIT_COLOR),
  side: THREE.DoubleSide,
  transparent: true,
  opacity: 0.5
}});
const ring = new THREE.Mesh(ringGeo, ringMat);
ring.rotation.x = -Math.PI / 2;
ring.position.y = -2.50;
scene.add(ring);

// ─── AVATAR GROUP ─────────────────────────────────────────────────────────
const avatar = new THREE.Group();
scene.add(avatar);

const skinMat = new THREE.MeshStandardMaterial({{
  color: new THREE.Color(SKIN_TONE),
  roughness: 0.55,
  metalness: 0.05,
}});

// ── HEAD ────────────────────────────────────────────────────────────────
const headGeo = new THREE.SphereGeometry(0.42, 64, 64);
const head    = new THREE.Mesh(headGeo, skinMat.clone());
head.position.y = 1.85;
head.castShadow = true;
avatar.add(head);

// ── FACE TEXTURE (Canvas drawn) ─────────────────────────────────────────
(function buildFace() {{
  const size = 512;
  const c    = document.createElement('canvas');
  c.width    = size; c.height = size;
  const ctx  = c.getContext('2d');

  // Base skin
  ctx.fillStyle = SKIN_TONE;
  ctx.fillRect(0, 0, size, size);

  // Subtle cheek blush
  const blush = ctx.createRadialGradient(160,300,10,160,300,70);
  blush.addColorStop(0,'rgba(255,100,100,0.25)');
  blush.addColorStop(1,'rgba(255,100,100,0)');
  ctx.fillStyle = blush;
  ctx.fillRect(0,0,size,size);
  const blush2 = ctx.createRadialGradient(352,300,10,352,300,70);
  blush2.addColorStop(0,'rgba(255,100,100,0.25)');
  blush2.addColorStop(1,'rgba(255,100,100,0)');
  ctx.fillStyle = blush2;
  ctx.fillRect(0,0,size,size);

  // Eyes (whites)
  ctx.fillStyle = 'white';
  ctx.beginPath(); ctx.ellipse(165,240,32,22,0,0,Math.PI*2); ctx.fill();
  ctx.beginPath(); ctx.ellipse(347,240,32,22,0,0,Math.PI*2); ctx.fill();

  // Iris
  ctx.fillStyle = '#3B2005';
  ctx.beginPath(); ctx.arc(165,240,16,0,Math.PI*2); ctx.fill();
  ctx.beginPath(); ctx.arc(347,240,16,0,Math.PI*2); ctx.fill();

  // Pupil
  ctx.fillStyle = '#000';
  ctx.beginPath(); ctx.arc(165,240,8,0,Math.PI*2); ctx.fill();
  ctx.beginPath(); ctx.arc(347,240,8,0,Math.PI*2); ctx.fill();

  // Eye shine
  ctx.fillStyle = 'rgba(255,255,255,0.9)';
  ctx.beginPath(); ctx.arc(170,235,4,0,Math.PI*2); ctx.fill();
  ctx.beginPath(); ctx.arc(352,235,4,0,Math.PI*2); ctx.fill();

  // Eyebrows
  ctx.strokeStyle = '#2C1A0E';
  ctx.lineWidth   = 7;
  ctx.lineCap     = 'round';
  ctx.beginPath(); ctx.moveTo(135,210); ctx.quadraticCurveTo(165,200,198,208); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(315,208); ctx.quadraticCurveTo(347,200,378,210); ctx.stroke();

  // Eyelashes (top)
  ctx.strokeStyle = '#111';
  ctx.lineWidth = 3;
  for(let i=0;i<5;i++){{
    ctx.beginPath();
    ctx.moveTo(133+i*13, 222);
    ctx.lineTo(130+i*13, 210);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(315+i*13, 222);
    ctx.lineTo(313+i*13, 210);
    ctx.stroke();
  }}

  // Nose
  ctx.strokeStyle = 'rgba(0,0,0,0.2)';
  ctx.lineWidth   = 4;
  ctx.beginPath(); ctx.moveTo(256,265); ctx.quadraticCurveTo(240,295,248,308); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(256,265); ctx.quadraticCurveTo(272,295,264,308); ctx.stroke();

  // Lips
  ctx.fillStyle = LIP_COLOR;
  ctx.beginPath();
  ctx.moveTo(210,338);
  ctx.quadraticCurveTo(256,322,302,338);
  ctx.quadraticCurveTo(280,360,256,362);
  ctx.quadraticCurveTo(232,360,210,338);
  ctx.fill();

  // Upper lip
  ctx.fillStyle = shadeColor(LIP_COLOR, -20);
  ctx.beginPath();
  ctx.moveTo(210,338);
  ctx.quadraticCurveTo(235,326,256,330);
  ctx.quadraticCurveTo(277,326,302,338);
  ctx.quadraticCurveTo(280,333,256,334);
  ctx.quadraticCurveTo(232,333,210,338);
  ctx.fill();

  // Lip gloss shine
  ctx.fillStyle = 'rgba(255,255,255,0.15)';
  ctx.beginPath();
  ctx.ellipse(256, 345, 30, 8, 0, 0, Math.PI*2);
  ctx.fill();

  const tex    = new THREE.CanvasTexture(c);
  head.material.map = tex;
  head.material.needsUpdate = true;
}})();

function shadeColor(color, percent) {{
  const num = parseInt(color.replace('#',''), 16);
  const r   = Math.min(255, Math.max(0,(num>>16)+percent));
  const g   = Math.min(255, Math.max(0,((num>>8)&0xFF)+percent));
  const b   = Math.min(255, Math.max(0,(num&0xFF)+percent));
  return '#'+((1<<24)+(r<<16)+(g<<8)+b).toString(16).slice(1);
}}

// ── NECK ────────────────────────────────────────────────────────────────
const neck = new THREE.Mesh(
  new THREE.CylinderGeometry(0.12, 0.14, 0.28, 32),
  skinMat.clone()
);
neck.position.y = 1.32;
neck.castShadow = true;
avatar.add(neck);

// ── TORSO — elegant tapered shape ──────────────────────────────────────
// Upper torso (shoulders)
const torsoUpper = new THREE.Mesh(
  new THREE.CylinderGeometry(0.52, 0.38, 0.60, 32),
  new THREE.MeshStandardMaterial({{ color: new THREE.Color(OUTFIT_COLOR), roughness:0.6, metalness:0.1 }})
);
torsoUpper.position.y = 0.88;
torsoUpper.castShadow = true;
avatar.add(torsoUpper);

// Lower torso (waist)
const torsoLower = new THREE.Mesh(
  new THREE.CylinderGeometry(0.38, 0.42, 0.50, 32),
  new THREE.MeshStandardMaterial({{ color: new THREE.Color(OUTFIT_COLOR), roughness:0.6, metalness:0.1 }})
);
torsoLower.position.y = 0.33;
torsoLower.castShadow = true;
avatar.add(torsoLower);

// ── SAREE DRAPE (decorative overlay on torso) ──────────────────────────
const sareeMat = new THREE.MeshStandardMaterial({{
  color: new THREE.Color(OUTFIT_COLOR),
  roughness: 0.4,
  metalness: 0.25,
  transparent: true,
  opacity: 0.88,
  side: THREE.DoubleSide
}});

// Pallu (draped fabric over left shoulder)
const palluGeo = new THREE.PlaneGeometry(0.55, 1.4, 8, 20);
// Add wave deformation to pallu vertices
const palluPos = palluGeo.attributes.position;
for(let i=0; i<palluPos.count; i++){{
  const y = palluPos.getY(i);
  const x = palluPos.getX(i);
  palluPos.setZ(i, Math.sin(y*3)*0.04 + Math.cos(x*4)*0.03);
}}
palluGeo.computeVertexNormals();
const pallu = new THREE.Mesh(palluGeo, sareeMat.clone());
pallu.position.set(-0.3, 0.55, 0.40);
pallu.rotation.z = 0.15;
avatar.add(pallu);

// Saree border stripe (gold)
const borderMat = new THREE.MeshStandardMaterial({{
  color: 0xFFD700,
  metalness: 0.8,
  roughness: 0.2
}});
const border = new THREE.Mesh(
  new THREE.PlaneGeometry(0.06, 1.4),
  borderMat
);
border.position.set(-0.58, 0.55, 0.41);
border.rotation.z = 0.15;
avatar.add(border);

// ── SKIRT (saree lower portion) ─────────────────────────────────────────
const skirtGeo  = new THREE.CylinderGeometry(0.58, 0.72, 1.65, 32, 8, true);
const skirtPos  = skirtGeo.attributes.position;
for(let i=0; i<skirtPos.count; i++){{
  const angle = Math.atan2(skirtPos.getX(i), skirtPos.getZ(i));
  skirtPos.setX(i, skirtPos.getX(i) + Math.sin(angle*6)*0.022);
}}
skirtGeo.computeVertexNormals();
const skirt = new THREE.Mesh(skirtGeo, new THREE.MeshStandardMaterial({{
  color: new THREE.Color(OUTFIT_COLOR),
  roughness: 0.5,
  metalness: 0.15,
  side: THREE.DoubleSide
}}));
skirt.position.y = -0.74;
skirt.castShadow = true;
avatar.add(skirt);

// Skirt gold hem
const hemGeo = new THREE.TorusGeometry(0.70, 0.025, 8, 64);
const hem    = new THREE.Mesh(hemGeo, borderMat.clone());
hem.position.y = -1.58;
avatar.add(hem);

// ── ARMS ────────────────────────────────────────────────────────────────
function makeArm(side) {{
  const armGroup = new THREE.Group();
  const x = side * 0.68;

  // Upper arm
  const upper = new THREE.Mesh(
    new THREE.CylinderGeometry(0.10, 0.09, 0.55, 16),
    skinMat.clone()
  );
  upper.position.set(x, 0.75, 0);
  upper.rotation.z = side * 0.22;
  upper.castShadow = true;
  armGroup.add(upper);

  // Lower arm
  const lower = new THREE.Mesh(
    new THREE.CylinderGeometry(0.08, 0.07, 0.48, 16),
    skinMat.clone()
  );
  lower.position.set(x * 1.12, 0.32, 0.05);
  lower.rotation.z = side * 0.38;
  lower.castShadow = true;
  armGroup.add(lower);

  // Hand
  const hand = new THREE.Mesh(
    new THREE.SphereGeometry(0.085, 16, 16),
    skinMat.clone()
  );
  hand.position.set(x * 1.22, 0.08, 0.08);
  hand.castShadow = true;
  armGroup.add(hand);

  // Bangle
  const bangle = new THREE.Mesh(
    new THREE.TorusGeometry(0.075, 0.015, 8, 32),
    new THREE.MeshStandardMaterial({{ color:0xFFD700, metalness:0.9, roughness:0.1 }})
  );
  bangle.position.set(x * 1.20, 0.14, 0.07);
  bangle.rotation.x = Math.PI/2;
  armGroup.add(bangle);

  avatar.add(armGroup);
}}
makeArm(1);
makeArm(-1);

// ── EARS ────────────────────────────────────────────────────────────────
[-1,1].forEach(s => {{
  const ear = new THREE.Mesh(
    new THREE.SphereGeometry(0.075, 16, 16),
    skinMat.clone()
  );
  ear.position.set(s*0.42, 1.85, 0);
  ear.scale.z = 0.5;
  avatar.add(ear);

  // Earring (gold drop)
  const earring = new THREE.Mesh(
    new THREE.SphereGeometry(0.04, 12, 12),
    new THREE.MeshStandardMaterial({{ color:0xFFD700, metalness:0.95, roughness:0.05 }})
  );
  earring.position.set(s*0.44, 1.72, 0);
  avatar.add(earring);
}});

// ── BINDI ────────────────────────────────────────────────────────────────
const bindi = new THREE.Mesh(
  new THREE.CircleGeometry(0.028, 32),
  new THREE.MeshStandardMaterial({{ color:0xFF0040, metalness:0.7, roughness:0.2 }})
);
bindi.position.set(0, 2.07, 0.418);
avatar.add(bindi);

// ─── HAIR STYLES ─────────────────────────────────────────────────────────
const hairMat = new THREE.MeshStandardMaterial({{
  color: new THREE.Color(HAIR_COLOR),
  roughness: 0.6,
  metalness: 0.05
}});

function buildHair() {{
  // Remove previous hair
  const old = avatar.getObjectByName('hairGroup');
  if(old) avatar.remove(old);

  const hairGroup = new THREE.Group();
  hairGroup.name  = 'hairGroup';

  if(HAIRSTYLE === 'bun') {{
    // ── BUN HAIRSTYLE ──
    // Base cap
    const cap = new THREE.Mesh(
      new THREE.SphereGeometry(0.44, 32, 32, 0, Math.PI*2, 0, Math.PI*0.52),
      hairMat.clone()
    );
    cap.position.y = 1.86;
    hairGroup.add(cap);

    // Bun sphere on top
    const bun = new THREE.Mesh(
      new THREE.SphereGeometry(0.17, 32, 32),
      hairMat.clone()
    );
    bun.position.set(0, 2.34, -0.1);
    hairGroup.add(bun);

    // Side hair strands
    [-1,1].forEach(s => {{
      const sideStrand = new THREE.Mesh(
        new THREE.SphereGeometry(0.15, 16, 16),
        hairMat.clone()
      );
      sideStrand.scale.set(0.6, 1.0, 0.5);
      sideStrand.position.set(s*0.42, 1.78, 0.05);
      hairGroup.add(sideStrand);
    }});

  }} else if(HAIRSTYLE === 'long') {{
    // ── LONG STRAIGHT HAIRSTYLE ──
    const cap = new THREE.Mesh(
      new THREE.SphereGeometry(0.44, 32, 32, 0, Math.PI*2, 0, Math.PI*0.52),
      hairMat.clone()
    );
    cap.position.y = 1.86;
    hairGroup.add(cap);

    // Long flowing panels
    const longGeo = new THREE.PlaneGeometry(0.82, 1.55, 6, 20);
    const longPos = longGeo.attributes.position;
    for(let i=0;i<longPos.count;i++){{
      const y = longPos.getY(i);
      longPos.setX(i, longPos.getX(i) + Math.sin(y*2.5)*0.04);
      longPos.setZ(i, longPos.getZ(i) - Math.abs(y)*0.06);
    }}
    longGeo.computeVertexNormals();
    const longHair = new THREE.Mesh(longGeo,
      new THREE.MeshStandardMaterial({{
        color: new THREE.Color(HAIR_COLOR),
        roughness:0.6,
        side: THREE.DoubleSide
      }})
    );
    longHair.position.set(0, 1.18, -0.38);
    hairGroup.add(longHair);

    // Side strands
    [-1,1].forEach(s => {{
      const sideGeo = new THREE.PlaneGeometry(0.28, 1.3, 4, 16);
      const sidePos = sideGeo.attributes.position;
      for(let i=0;i<sidePos.count;i++){{
        sidePos.setZ(i, sidePos.getZ(i) + Math.sin(sidePos.getY(i)*3)*0.03);
      }}
      sideGeo.computeVertexNormals();
      const side = new THREE.Mesh(sideGeo, hairMat.clone());
      side.position.set(s*0.48, 1.22, 0.05);
      side.rotation.y = s * 0.35;
      hairGroup.add(side);
    }});

  }} else if(HAIRSTYLE === 'wavy') {{
    // ── WAVY BOB HAIRSTYLE ──
    const cap = new THREE.Mesh(
      new THREE.SphereGeometry(0.44, 32, 32, 0, Math.PI*2, 0, Math.PI*0.52),
      hairMat.clone()
    );
    cap.position.y = 1.86;
    hairGroup.add(cap);

    // Wavy bob using LatheGeometry
    const points = [];
    for(let i=0; i<=12; i++){{
      const t = i/12;
      const rx = 0.44 + Math.sin(t*Math.PI)*0.18 + Math.sin(t*Math.PI*4)*0.04;
      points.push(new THREE.Vector2(rx, 1.86 - t*0.85));
    }}
    const lathe = new THREE.Mesh(
      new THREE.LatheGeometry(points, 32),
      new THREE.MeshStandardMaterial({{
        color: new THREE.Color(HAIR_COLOR),
        roughness: 0.65,
        side: THREE.DoubleSide
      }})
    );
    hairGroup.add(lathe);

    // Wavy front bangs
    const bangGeo = new THREE.PlaneGeometry(0.78, 0.32, 8, 6);
    const bangPos = bangGeo.attributes.position;
    for(let i=0;i<bangPos.count;i++){{
      bangPos.setZ(i, Math.sin(bangPos.getX(i)*5)*0.04 + 0.38);
      bangPos.setY(i, bangPos.getY(i) + Math.cos(bangPos.getX(i)*4)*0.03);
    }}
    bangGeo.computeVertexNormals();
    const bangs = new THREE.Mesh(bangGeo, hairMat.clone());
    bangs.position.set(0, 2.12, 0.02);
    hairGroup.add(bangs);
  }}

  avatar.add(hairGroup);
}}

buildHair();

// ─── PARTICLE SPARKLES ───────────────────────────────────────────────────
const sparkleGeo  = new THREE.BufferGeometry();
const sparkleCount= 120;
const positions   = new Float32Array(sparkleCount * 3);
for(let i=0; i<sparkleCount; i++){{
  positions[i*3]   = (Math.random()-0.5)*5;
  positions[i*3+1] = (Math.random()-0.5)*6;
  positions[i*3+2] = (Math.random()-0.5)*3 - 1;
}}
sparkleGeo.setAttribute('position', new THREE.BufferAttribute(positions,3));
const sparkleMat  = new THREE.PointsMaterial({{
  color: 0xFFD700,
  size: 0.04,
  transparent: true,
  opacity: 0.7
}});
const sparkles = new THREE.Points(sparkleGeo, sparkleMat);
scene.add(sparkles);

// ─── ORBIT CONTROLS (Manual Implementation) ──────────────────────────────
let isDragging   = false;
let prevMouse    = {{ x: 0, y: 0 }};
let rotationX    = 0;
let rotationY    = 0;
let autoRotate   = true;
let autoRotateSpeed = 0.005;

renderer.domElement.addEventListener('mousedown', e => {{
  isDragging = true;
  prevMouse  = {{ x: e.clientX, y: e.clientY }};
  autoRotate = false;
}});
renderer.domElement.addEventListener('mousemove', e => {{
  if(!isDragging) return;
  rotationY += (e.clientX - prevMouse.x) * 0.012;
  rotationX += (e.clientY - prevMouse.y) * 0.008;
  rotationX  = Math.max(-0.6, Math.min(0.6, rotationX));
  prevMouse  = {{ x: e.clientX, y: e.clientY }};
  avatar.rotation.y = rotationY;
  avatar.rotation.x = rotationX;
}});
renderer.domElement.addEventListener('mouseup',   () => {{ isDragging = false; }});
renderer.domElement.addEventListener('mouseleave',() => {{ isDragging = false; }});

// Touch support
renderer.domElement.addEventListener('touchstart', e => {{
  isDragging = true;
  prevMouse  = {{ x: e.touches[0].clientX, y: e.touches[0].clientY }};
  autoRotate = false;
}});
renderer.domElement.addEventListener('touchmove', e => {{
  if(!isDragging) return;
  rotationY += (e.touches[0].clientX - prevMouse.x) * 0.012;
  prevMouse  = {{ x: e.touches[0].clientX, y: e.touches[0].clientY }};
  avatar.rotation.y = rotationY;
}});
renderer.domElement.addEventListener('touchend', () => {{ isDragging = false; }});

function resetCamera() {{
  rotationX  = 0; rotationY = 0;
  avatar.rotation.set(0,0,0);
  autoRotate = true;
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
function animate() {{
  requestAnimationFrame(animate);
  const t = clock.getElapsedTime();

  if(autoRotate && !isDragging) {{
    avatar.rotation.y += autoRotateSpeed;
  }}

  // Gentle breathing animation on torso
  torsoUpper.scale.x = 1 + Math.sin(t*1.2)*0.008;
  torsoUpper.scale.z = 1 + Math.sin(t*1.2)*0.008;

  // Sparkle twinkle
  sparkleMat.opacity = 0.4 + Math.sin(t*2)*0.3;
  sparkles.rotation.y += 0.001;

  // Rim light color pulse
  rimLight.intensity = 1.2 + Math.sin(t*1.5)*0.3;

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
