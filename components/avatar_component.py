# avatar_3d.py
def get_avatar_html(
    hairstyle="long_braid",
    hair_color="#1a1a1a",
    skin_tone="#D4A373",
    saree_color="#D32F2F",
    blouse_color="#C62828",
    border_color="#FFD700",
    lip_color="#C13C3C",  # Added this parameter
    pose="dance_pose"
):
    """
    Returns photorealistic 3D saree avatar matching reference image.
    
    Parameters:
    -----------
    hairstyle : str
        Hair style type ('long_braid', 'bun', 'wavy')
    hair_color : str
        Hex color for hair
    skin_tone : str
        Hex color for skin
    saree_color : str
        Hex color for saree fabric
    blouse_color : str
        Hex color for blouse
    border_color : str
        Hex color for saree border/zari
    lip_color : str
        Hex color for lips
    pose : str
        Avatar pose ('dance_pose', 'standing', 'namaste')
    
    Returns:
    --------
    str : Complete HTML string with Three.js 3D avatar
    """
    
    # Sanitize inputs to prevent XSS
    import html
    
    hairstyle = html.escape(str(hairstyle))
    hair_color = html.escape(str(hair_color))
    skin_tone = html.escape(str(skin_tone))
    saree_color = html.escape(str(saree_color))
    blouse_color = html.escape(str(blouse_color))
    border_color = html.escape(str(border_color))
    lip_color = html.escape(str(lip_color))
    pose = html.escape(str(pose))
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Fashion Avatar 3D</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      background: linear-gradient(180deg, #E0E0E0 0%, #BDBDBD 50%, #9E9E9E 100%);
      overflow: hidden;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    canvas {{ display: block; }}

    #controls-overlay {{
      position: absolute;
      bottom: 20px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      gap: 12px;
      z-index: 10;
    }}

    .ctrl-btn {{
      background: rgba(211,47,47,0.9);
      color: white;
      border: 2px solid rgba(255,215,0,0.6);
      padding: 10px 22px;
      border-radius: 25px;
      cursor: pointer;
      font-size: 13px;
      font-weight: 600;
      backdrop-filter: blur(8px);
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }}
    .ctrl-btn:hover {{ 
      background: rgba(211,47,47,1); 
      transform: translateY(-2px);
      box-shadow: 0 6px 16px rgba(0,0,0,0.4);
    }}

    #info-tag {{
      position: absolute;
      top: 20px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(211,47,47,0.25);
      border: 2px solid rgba(255,215,0,0.6);
      color: #fff;
      padding: 8px 24px;
      border-radius: 25px;
      font-size: 12px;
      font-weight: 600;
      letter-spacing: 3px;
      backdrop-filter: blur(10px);
      z-index: 10;
      text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }}

    #loading {{
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      color: white;
      font-size: 18px;
      font-weight: 600;
      z-index: 5;
      background: rgba(0,0,0,0.7);
      padding: 20px 40px;
      border-radius: 15px;
    }}

    .hidden {{ display: none !important; }}
  </style>
</head>
<body>

<div id="info-tag">✨ PHOTOREALISTIC SAREE AVATAR</div>
<div id="loading">Loading 3D Model...</div>

<div id="controls-overlay">
  <button class="ctrl-btn" onclick="resetView()">🎯 Reset</button>
  <button class="ctrl-btn" onclick="toggleRotation()">🔄 Auto Rotate</button>
  <button class="ctrl-btn" onclick="screenshot()">📸 Capture</button>
</div>

<!-- Three.js CDN -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

<script>
// ═══════════════════════════════════════════════════════════════════════
// CONFIGURATION PARAMETERS (Injected from Python)
// ═══════════════════════════════════════════════════════════════════════
const CONFIG = {{
  hairstyle: "{hairstyle}",
  hairColor: "{hair_color}",
  skinTone: "{skin_tone}",
  sareeColor: "{saree_color}",
  blouseColor: "{blouse_color}",
  borderColor: "{border_color}",
  lipColor: "{lip_color}",
  pose: "{pose}"
}};

console.log('Avatar Config:', CONFIG);

// ═══════════════════════════════════════════════════════════════════════
// SCENE SETUP
// ═══════════════════════════════════════════════════════════════════════
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xC0C0C0);
scene.fog = new THREE.Fog(0xC0C0C0, 8, 20);

const camera = new THREE.PerspectiveCamera(
  35,
  window.innerWidth / window.innerHeight,
  0.1,
  100
);
camera.position.set(0, 1.5, 6);
camera.lookAt(0, 1, 0);

const renderer = new THREE.WebGLRenderer({{ 
  antialias: true, 
  alpha: true,
  preserveDrawingBuffer: true
}});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.3;
document.body.appendChild(renderer.domElement);

// ═══════════════════════════════════════════════════════════════════════
// LIGHTING SETUP
// ═══════════════════════════════════════════════════════════════════════
const hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444, 0.6);
hemiLight.position.set(0, 20, 0);
scene.add(hemiLight);

const keyLight = new THREE.DirectionalLight(0xffffff, 1.2);
keyLight.position.set(-5, 8, 6);
keyLight.castShadow = true;
keyLight.shadow.mapSize.width = 2048;
keyLight.shadow.mapSize.height = 2048;
scene.add(keyLight);

const fillLight = new THREE.DirectionalLight(0xE3F2FD, 0.5);
fillLight.position.set(6, 4, 4);
scene.add(fillLight);

const rimLight = new THREE.PointLight(0xFFE0B2, 1.5, 15);
rimLight.position.set(0, 5, -6);
scene.add(rimLight);

// ═══════════════════════════════════════════════════════════════════════
// FLOOR
// ═══════════════════════════════════════════════════════════════════════
const floorGeometry = new THREE.CircleGeometry(8, 64);
const floorMaterial = new THREE.MeshStandardMaterial({{
  color: 0xE0E0E0,
  roughness: 0.8,
  metalness: 0.1
}});
const floor = new THREE.Mesh(floorGeometry, floorMaterial);
floor.rotation.x = -Math.PI / 2;
floor.position.y = 0;
floor.receiveShadow = true;
scene.add(floor);

const platformGeometry = new THREE.CylinderGeometry(1.2, 1.3, 0.15, 64);
const platformMaterial = new THREE.MeshStandardMaterial({{
  color: 0xBDBDBD,
  roughness: 0.4,
  metalness: 0.6
}});
const platform = new THREE.Mesh(platformGeometry, platformMaterial);
platform.position.y = 0.075;
platform.castShadow = true;
platform.receiveShadow = true;
scene.add(platform);

// ═══════════════════════════════════════════════════════════════════════
// AVATAR GROUP
// ═══════════════════════════════════════════════════════════════════════
const avatar = new THREE.Group();
avatar.position.y = 0.15;
scene.add(avatar);

// Materials
const materials = {{
  skin: new THREE.MeshStandardMaterial({{
    color: new THREE.Color(CONFIG.skinTone),
    roughness: 0.6,
    metalness: 0.0
  }}),
  
  hair: new THREE.MeshStandardMaterial({{
    color: new THREE.Color(CONFIG.hairColor),
    roughness: 0.5,
    metalness: 0.1
  }}),
  
  saree: new THREE.MeshStandardMaterial({{
    color: new THREE.Color(CONFIG.sareeColor),
    roughness: 0.35,
    metalness: 0.05,
    side: THREE.DoubleSide,
    transparent: true,
    opacity: 0.95
  }}),
  
  blouse: new THREE.MeshStandardMaterial({{
    color: new THREE.Color(CONFIG.blouseColor),
    roughness: 0.4,
    metalness: 0.1
  }}),
  
  border: new THREE.MeshStandardMaterial({{
    color: new THREE.Color(CONFIG.borderColor),
    roughness: 0.15,
    metalness: 0.9,
    emissive: new THREE.Color(CONFIG.borderColor),
    emissiveIntensity: 0.2
  }}),
  
  jewelry: new THREE.MeshStandardMaterial({{
    color: 0xFFD700,
    roughness: 0.1,
    metalness: 1.0,
    emissive: 0xFFAA00,
    emissiveIntensity: 0.3
  }})
}};

// ───────────────────────────────────────────────────────────────────────
// HEAD
// ───────────────────────────────────────────────────────────────────────
const headGeometry = new THREE.SphereGeometry(0.38, 64, 64);
const head = new THREE.Mesh(headGeometry, materials.skin.clone());
head.position.y = 1.75;
head.castShadow = true;
avatar.add(head);

// ───────────────────────────────────────────────────────────────────────
// NECK
// ───────────────────────────────────────────────────────────────────────
const neckGeometry = new THREE.CylinderGeometry(0.11, 0.13, 0.25, 32);
const neck = new THREE.Mesh(neckGeometry, materials.skin.clone());
neck.position.y = 1.38;
neck.castShadow = true;
avatar.add(neck);

// ───────────────────────────────────────────────────────────────────────
// TORSO & WAIST
// ───────────────────────────────────────────────────────────────────────
const torsoGeometry = new THREE.CylinderGeometry(0.28, 0.32, 0.45, 32);
const torso = new THREE.Mesh(torsoGeometry, materials.blouse.clone());
torso.position.y = 1.02;
torso.castShadow = true;
avatar.add(torso);

const waistGeometry = new THREE.CylinderGeometry(0.26, 0.30, 0.22, 32);
const waist = new THREE.Mesh(waistGeometry, materials.skin.clone());
waist.position.y = 0.69;
waist.castShadow = true;
avatar.add(waist);

// ───────────────────────────────────────────────────────────────────────
// ARMS (Extended Dance Pose)
// ───────────────────────────────────────────────────────────────────────
function createArm(side) {{
  const armGroup = new THREE.Group();
  const xOffset = side * 0.45;
  
  // Upper arm
  const upperArm = new THREE.Mesh(
    new THREE.CylinderGeometry(0.09, 0.08, 0.50, 24),
    materials.skin.clone()
  );
  upperArm.position.set(xOffset * 1.8, 0.95, 0.1);
  upperArm.rotation.z = side * (Math.PI / 3);
  upperArm.castShadow = true;
  armGroup.add(upperArm);
  
  // Forearm
  const forearm = new THREE.Mesh(
    new THREE.CylinderGeometry(0.07, 0.065, 0.45, 24),
    materials.skin.clone()
  );
  forearm.position.set(xOffset * 3.0, 0.85, 0.2);
  forearm.rotation.z = side * (Math.PI / 4);
  forearm.castShadow = true;
  armGroup.add(forearm);
  
  // Hand
  const hand = new THREE.Mesh(
    new THREE.SphereGeometry(0.075, 20, 20),
    materials.skin.clone()
  );
  hand.scale.set(1, 1.3, 0.8);
  hand.position.set(xOffset * 3.5, 1.0, 0.25);
  hand.rotation.z = side * 0.3;
  hand.castShadow = true;
  armGroup.add(hand);
  
  // Sleeve
  const sleeve = new THREE.Mesh(
    new THREE.CylinderGeometry(0.11, 0.09, 0.18, 24),
    materials.blouse.clone()
  );
  sleeve.position.set(xOffset * 1.3, 1.08, 0.05);
  sleeve.rotation.z = side * (Math.PI / 3);
  armGroup.add(sleeve);
  
  // Bangles
  for(let i = 0; i < 3; i++) {{
    const bangle = new THREE.Mesh(
      new THREE.TorusGeometry(0.07, 0.012, 16, 32),
      materials.jewelry.clone()
    );
    bangle.position.set(xOffset * 3.2, 0.82 + i * 0.03, 0.22);
    bangle.rotation.x = Math.PI / 2;
    bangle.rotation.z = side * (Math.PI / 4);
    armGroup.add(bangle);
  }}
  
  avatar.add(armGroup);
}}

createArm(1);
createArm(-1);

// ───────────────────────────────────────────────────────────────────────
// SAREE (Lower Skirt with Pleats)
// ───────────────────────────────────────────────────────────────────────
const skirtGeometry = new THREE.CylinderGeometry(0.48, 0.65, 1.3, 64, 20, true);
const skirtPositions = skirtGeometry.attributes.position;

for(let i = 0; i < skirtPositions.count; i++) {{
  const x = skirtPositions.getX(i);
  const y = skirtPositions.getY(i);
  const z = skirtPositions.getZ(i);
  
  const angle = Math.atan2(x, z);
  const radius = Math.sqrt(x*x + z*z);
  
  if(angle > -Math.PI/6 && angle < Math.PI/3) {{
    const pleat = Math.sin(angle * 12) * 0.08;
    const newRadius = radius + pleat * (1 - Math.abs(y / 0.65));
    
    skirtPositions.setX(i, Math.sin(angle) * newRadius);
    skirtPositions.setZ(i, Math.cos(angle) * newRadius);
  }}
  
  const flow = Math.sin(angle * 2 + y * 1.5) * 0.02;
  skirtPositions.setX(i, skirtPositions.getX(i) + flow);
}}

skirtGeometry.computeVertexNormals();
const skirt = new THREE.Mesh(skirtGeometry, materials.saree.clone());
skirt.position.y = 0.05;
skirt.castShadow = true;
skirt.receiveShadow = true;
avatar.add(skirt);

// Border
const borderGeometry = new THREE.TorusGeometry(0.64, 0.035, 16, 64);
const borderMesh = new THREE.Mesh(borderGeometry, materials.border.clone());
borderMesh.position.y = -0.60;
borderMesh.rotation.x = Math.PI / 2;
avatar.add(borderMesh);

// ───────────────────────────────────────────────────────────────────────
// PALLU (Draped Fabric)
// ───────────────────────────────────────────────────────────────────────
const palluGeometry = new THREE.PlaneGeometry(0.75, 1.8, 16, 32);
const palluPositions = palluGeometry.attributes.position;

for(let i = 0; i < palluPositions.count; i++) {{
  const x = palluPositions.getX(i);
  const y = palluPositions.getY(i);
  
  const wave1 = Math.sin(y * 2.5 + x * 1.5) * 0.12;
  const wave2 = Math.cos(y * 3 - x * 2) * 0.08;
  const drape = Math.pow((y + 0.9) / 1.8, 2) * 0.15;
  
  palluPositions.setZ(i, wave1 + wave2 + drape);
}}

palluGeometry.computeVertexNormals();
const pallu = new THREE.Mesh(palluGeometry, materials.saree.clone());
pallu.position.set(-0.25, 0.85, 0.30);
pallu.rotation.set(0.2, -0.3, 0.15);
pallu.castShadow = true;
avatar.add(pallu);

// Pallu border
const palluBorderGeometry = new THREE.PlaneGeometry(0.08, 1.8, 1, 32);
const palluBorderPositions = palluBorderGeometry.attributes.position;

for(let i = 0; i < palluBorderPositions.count; i++) {{
  const y = palluBorderPositions.getY(i);
  const wave1 = Math.sin(y * 2.5 - 0.6) * 0.12;
  const wave2 = Math.cos(y * 3 + 1) * 0.08;
  const drape = Math.pow((y + 0.9) / 1.8, 2) * 0.15;
  palluBorderPositions.setZ(i, wave1 + wave2 + drape + 0.01);
}}

palluBorderGeometry.computeVertexNormals();
const palluBorder = new THREE.Mesh(palluBorderGeometry, materials.border.clone());
palluBorder.position.set(-0.625, 0.85, 0.30);
palluBorder.rotation.set(0.2, -0.3, 0.15);
avatar.add(palluBorder);

// ───────────────────────────────────────────────────────────────────────
// HAIR (Long Braid)
// ───────────────────────────────────────────────────────────────────────
const hairGroup = new THREE.Group();

const capGeometry = new THREE.SphereGeometry(0.40, 48, 48, 0, Math.PI * 2, 0, Math.PI * 0.55);
const cap = new THREE.Mesh(capGeometry, materials.hair.clone());
cap.position.y = 1.76;
cap.castShadow = true;
hairGroup.add(cap);

// Side hair
[-1, 1].forEach(side => {{
  const sideHair = new THREE.Mesh(
    new THREE.SphereGeometry(0.18, 24, 24),
    materials.hair.clone()
  );
  sideHair.scale.set(0.8, 1.2, 0.6);
  sideHair.position.set(side * 0.38, 1.70, 0.05);
  hairGroup.add(sideHair);
}});

// Braid
const braidSegments = 18;
for(let i = 0; i < braidSegments; i++) {{
  const t = i / braidSegments;
  const segmentRadius = 0.06 - t * 0.02;
  
  const segment = new THREE.Mesh(
    new THREE.SphereGeometry(segmentRadius, 16, 16),
    materials.hair.clone()
  );
  
  const swingX = Math.sin(t * Math.PI * 3) * 0.08;
  const swingZ = -0.25 - t * 0.1;
  const yPos = 1.55 - t * 1.5;
  
  segment.position.set(swingX, yPos, swingZ);
  segment.scale.set(1.2, 0.8, 1);
  hairGroup.add(segment);
}}

avatar.add(hairGroup);

// ───────────────────────────────────────────────────────────────────────
// FACE TEXTURE
// ───────────────────────────────────────────────────────────────────────
const canvas = document.createElement('canvas');
canvas.width = 1024;
canvas.height = 1024;
const ctx = canvas.getContext('2d');

// Base skin
ctx.fillStyle = CONFIG.skinTone;
ctx.fillRect(0, 0, 1024, 1024);

// Blush
const blush1 = ctx.createRadialGradient(320, 580, 20, 320, 580, 100);
blush1.addColorStop(0, 'rgba(255,160,122,0.35)');
blush1.addColorStop(1, 'rgba(255,160,122,0)');
ctx.fillStyle = blush1;
ctx.fillRect(0, 0, 1024, 1024);

const blush2 = ctx.createRadialGradient(704, 580, 20, 704, 580, 100);
blush2.addColorStop(0, 'rgba(255,160,122,0.35)');
blush2.addColorStop(1, 'rgba(255,160,122,0)');
ctx.fillStyle = blush2;
ctx.fillRect(0, 0, 1024, 1024);

// Eyes - Whites
ctx.fillStyle = '#FFFFFF';
ctx.beginPath();
ctx.ellipse(340, 480, 55, 40, 0, 0, Math.PI * 2);
ctx.fill();
ctx.beginPath();
ctx.ellipse(684, 480, 55, 40, 0, 0, Math.PI * 2);
ctx.fill();

// Iris
const irisGrad1 = ctx.createRadialGradient(340, 480, 0, 340, 480, 35);
irisGrad1.addColorStop(0, '#6B4423');
irisGrad1.addColorStop(0.6, '#4A2511');
irisGrad1.addColorStop(1, '#2C1810');
ctx.fillStyle = irisGrad1;
ctx.beginPath();
ctx.arc(340, 480, 35, 0, Math.PI * 2);
ctx.fill();

const irisGrad2 = ctx.createRadialGradient(684, 480, 0, 684, 480, 35);
irisGrad2.addColorStop(0, '#6B4423');
irisGrad2.addColorStop(0.6, '#4A2511');
irisGrad2.addColorStop(1, '#2C1810');
ctx.fillStyle = irisGrad2;
ctx.beginPath();
ctx.arc(684, 480, 35, 0, Math.PI * 2);
ctx.fill();

// Pupils
ctx.fillStyle = '#000000';
ctx.beginPath();
ctx.arc(340, 480, 16, 0, Math.PI * 2);
ctx.fill();
ctx.beginPath();
ctx.arc(684, 480, 16, 0, Math.PI * 2);
ctx.fill();

// Highlights
ctx.fillStyle = 'rgba(255,255,255,0.9)';
ctx.beginPath();
ctx.arc(348, 472, 8, 0, Math.PI * 2);
ctx.fill();
ctx.beginPath();
ctx.arc(692, 472, 8, 0, Math.PI * 2);
ctx.fill();

// Eyebrows
ctx.strokeStyle = '#1a1a1a';
ctx.lineWidth = 10;
ctx.lineCap = 'round';
ctx.beginPath();
ctx.moveTo(270, 410);
ctx.quadraticCurveTo(320, 390, 390, 405);
ctx.stroke();
ctx.beginPath();
ctx.moveTo(634, 405);
ctx.quadraticCurveTo(704, 390, 754, 410);
ctx.stroke();

// Eyelashes
ctx.lineWidth = 4;
for(let i = 0; i < 8; i++) {{
  ctx.beginPath();
  ctx.moveTo(285 + i * 14, 455);
  ctx.lineTo(280 + i * 14, 435);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(630 + i * 14, 455);
  ctx.lineTo(628 + i * 14, 435);
  ctx.stroke();
}}

// Nose
ctx.strokeStyle = 'rgba(0,0,0,0.15)';
ctx.lineWidth = 8;
ctx.beginPath();
ctx.moveTo(512, 530);
ctx.quadraticCurveTo(490, 580, 500, 610);
ctx.stroke();
ctx.beginPath();
ctx.moveTo(512, 530);
ctx.quadraticCurveTo(534, 580, 524, 610);
ctx.stroke();

// Lips
ctx.fillStyle = CONFIG.lipColor;
ctx.beginPath();
ctx.moveTo(420, 670);
ctx.bezierCurveTo(470, 650, 554, 650, 604, 670);
ctx.bezierCurveTo(570, 665, 454, 665, 420, 670);
ctx.fill();

ctx.beginPath();
ctx.moveTo(420, 670);
ctx.bezierCurveTo(454, 700, 570, 700, 604, 670);
ctx.bezierCurveTo(580, 695, 444, 695, 420, 670);
ctx.fill();

// Lip gloss
const gloss = ctx.createLinearGradient(512, 675, 512, 690);
gloss.addColorStop(0, 'rgba(255,255,255,0.5)');
gloss.addColorStop(1, 'rgba(255,255,255,0)');
ctx.fillStyle = gloss;
ctx.beginPath();
ctx.ellipse(512, 682, 60, 10, 0, 0, Math.PI * 2);
ctx.fill();

// Bindi
ctx.fillStyle = '#DC143C';
ctx.beginPath();
ctx.arc(512, 380, 15, 0, Math.PI * 2);
ctx.fill();

const texture = new THREE.CanvasTexture(canvas);
head.material.map = texture;
head.material.needsUpdate = true;

// ───────────────────────────────────────────────────────────────────────
// JEWELRY
// ───────────────────────────────────────────────────────────────────────

// Necklace
const necklaceGeometry = new THREE.TorusGeometry(0.18, 0.008, 16, 64, Math.PI * 1.3);
const necklace = new THREE.Mesh(necklaceGeometry, materials.jewelry.clone());
necklace.position.set(0, 1.28, 0.12);
necklace.rotation.x = Math.PI / 2 + 0.2;
avatar.add(necklace);

// Earrings
[-1, 1].forEach(side => {{
  const ear = new THREE.Mesh(
    new THREE.SphereGeometry(0.06, 24, 24),
    materials.skin.clone()
  );
  ear.scale.set(0.7, 1, 0.5);
  ear.position.set(side * 0.38, 1.75, 0.02);
  avatar.add(ear);
  
  const earring = new THREE.Mesh(
    new THREE.SphereGeometry(0.04, 16, 16),
    materials.jewelry.clone()
  );
  earring.position.set(side * 0.40, 1.68, 0.05);
  avatar.add(earring);
}});

// ═══════════════════════════════════════════════════════════════════════
// PARTICLES
// ═══════════════════════════════════════════════════════════════════════
const particlesGeometry = new THREE.BufferGeometry();
const particleCount = 150;
const positions = new Float32Array(particleCount * 3);

for(let i = 0; i < particleCount; i++) {{
  positions[i * 3] = (Math.random() - 0.5) * 8;
  positions[i * 3 + 1] = Math.random() * 5;
  positions[i * 3 + 2] = (Math.random() - 0.5) * 8;
}}

particlesGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

const particlesMaterial = new THREE.PointsMaterial({{
  color: 0xFFD700,
  size: 0.03,
  transparent: true,
  opacity: 0.6,
  blending: THREE.AdditiveBlending
}});

const particles = new THREE.Points(particlesGeometry, particlesMaterial);
scene.add(particles);

// ═══════════════════════════════════════════════════════════════════════
// CONTROLS
// ═══════════════════════════════════════════════════════════════════════
let autoRotate = true;
let isDragging = false;
let previousMousePosition = {{ x: 0, y: 0 }};
let rotation = {{ x: 0, y: 0 }};

renderer.domElement.addEventListener('mousedown', (e) => {{
  isDragging = true;
  autoRotate = false;
  previousMousePosition = {{ x: e.clientX, y: e.clientY }};
}});

renderer.domElement.addEventListener('mousemove', (e) => {{
  if (!isDragging) return;
  
  const deltaX = e.clientX - previousMousePosition.x;
  const deltaY = e.clientY - previousMousePosition.y;
  
  rotation.y += deltaX * 0.01;
  rotation.x += deltaY * 0.01;
  rotation.x = Math.max(-0.5, Math.min(0.5, rotation.x));
  
  avatar.rotation.y = rotation.y;
  avatar.rotation.x = rotation.x;
  
  previousMousePosition = {{ x: e.clientX, y: e.clientY }};
}});

renderer.domElement.addEventListener('mouseup', () => {{
  isDragging = false;
}});

renderer.domElement.addEventListener('touchstart', (e) => {{
  isDragging = true;
  autoRotate = false;
  previousMousePosition = {{
    x: e.touches[0].clientX,
    y: e.touches[0].clientY
  }};
}});

renderer.domElement.addEventListener('touchmove', (e) => {{
  if (!isDragging) return;
  
  const deltaX = e.touches[0].clientX - previousMousePosition.x;
  rotation.y += deltaX * 0.01;
  avatar.rotation.y = rotation.y;
  
  previousMousePosition = {{
    x: e.touches[0].clientX,
    y: e.touches[0].clientY
  }};
}});

renderer.domElement.addEventListener('touchend', () => {{
  isDragging = false;
}});

function resetView() {{
  rotation = {{ x: 0, y: 0 }};
  avatar.rotation.set(0, 0, 0);
  autoRotate = true;
}}

function toggleRotation() {{
  autoRotate = !autoRotate;
}}

function screenshot() {{
  try {{
    renderer.render(scene, camera);
    const dataURL = renderer.domElement.toDataURL('image/png');
    const link = document.createElement('a');
    link.download = 'saree-avatar-' + Date.now() + '.png';
    link.href = dataURL;
    link.click();
  }} catch(e) {{
    console.error('Screenshot failed:', e);
    alert('Screenshot failed. Please try again.');
  }}
}}

// ═══════════════════════════════════════════════════════════════════════
// ANIMATION LOOP
// ═══════════════════════════════════════════════════════════════════════
const clock = new THREE.Clock();

function animate() {{
  requestAnimationFrame(animate);
  
  const elapsed = clock.getElapsedTime();
  
  if (autoRotate && !isDragging) {{
    avatar.rotation.y += 0.003;
  }}
  
  const breathScale = 1 + Math.sin(elapsed * 1.5) * 0.005;
  torso.scale.y = breathScale;
  waist.scale.y = breathScale;
  
  particles.rotation.y += 0.0005;
  particlesMaterial.opacity = 0.4 + Math.sin(elapsed * 2) * 0.2;
  
  materials.jewelry.emissiveIntensity = 0.3 + Math.sin(elapsed * 3) * 0.2;
  
  renderer.render(scene, camera);
}}

document.getElementById('loading').classList.add('hidden');
animate();

// ═══════════════════════════════════════════════════════════════════════
// RESPONSIVE
// ═══════════════════════════════════════════════════════════════════════
window.addEventListener('resize', () => {{
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}});

</script>
</body>
</html>
"""
    return html_content
