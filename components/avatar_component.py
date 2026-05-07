def get_avatar_html(
    hairstyle="long_braid",
    hair_color="#1a1a1a",
    skin_tone="#D4A373",
    saree_color="#D32F2F",  # Deep red
    blouse_color="#C62828",  # Darker red
    border_color="#FFD700",  # Gold
    pose="dance_pose"
):
    """
    Returns photorealistic 3D saree avatar matching reference image.
    Features: Realistic draping, dynamic pose, advanced materials.
    """
    
    html = f"""
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
      z-index: 5;
    }}

    .hidden {{ display: none; }}
  </style>
</head>
<body>

<div id="info-tag">✨ PHOTOREALISTIC SAREE AVATAR</div>
<div id="loading">Loading 3D Model...</div>

<div id="controls-overlay">
  <button class="ctrl-btn" onclick="resetView()">🎯 Reset</button>
  <button class="ctrl-btn" onclick="toggleRotation()">🔄 Auto Rotate</button>
  <button class="ctrl-btn" onclick="changePose()">💃 Change Pose</button>
  <button class="ctrl-btn" onclick="screenshot()">📸 Capture</button>
</div>

<!-- Three.js r152 (latest stable) -->
<script src="https://cdn.jsdelivr.net/npm/three@0.152.0/build/three.min.js"></script>

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
  pose: "{pose}"
}};

// ═══════════════════════════════════════════════════════════════════════
// SCENE SETUP
// ═══════════════════════════════════════════════════════════════════════
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xC0C0C0);
scene.fog = new THREE.Fog(0xC0C0C0, 8, 20);

const camera = new THREE.PerspectiveCamera(
  35,  // Narrower FOV for portrait
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
renderer.outputEncoding = THREE.sRGBEncoding;
document.body.appendChild(renderer.domElement);

// ═══════════════════════════════════════════════════════════════════════
// ADVANCED LIGHTING SETUP (Photorealistic)
// ═══════════════════════════════════════════════════════════════════════

// Hemisphere light (sky + ground bounce)
const hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444, 0.6);
hemiLight.position.set(0, 20, 0);
scene.add(hemiLight);

// Main key light (studio softbox simulation)
const keyLight = new THREE.DirectionalLight(0xffffff, 1.2);
keyLight.position.set(-5, 8, 6);
keyLight.castShadow = true;
keyLight.shadow.mapSize.width = 4096;
keyLight.shadow.mapSize.height = 4096;
keyLight.shadow.camera.near = 0.5;
keyLight.shadow.camera.far = 50;
keyLight.shadow.camera.left = -8;
keyLight.shadow.camera.right = 8;
keyLight.shadow.camera.top = 8;
keyLight.shadow.camera.bottom = -8;
keyLight.shadow.bias = -0.0001;
scene.add(keyLight);

// Fill light (right side, cooler tone)
const fillLight = new THREE.DirectionalLight(0xE3F2FD, 0.5);
fillLight.position.set(6, 4, 4);
scene.add(fillLight);

// Rim light (back, warm glow)
const rimLight = new THREE.SpotLight(0xFFE0B2, 1.5, 15, Math.PI/6, 0.5, 2);
rimLight.position.set(0, 5, -6);
scene.add(rimLight);

// Ground bounce light
const bounceLight = new THREE.PointLight(0xFFFFFF, 0.3, 10);
bounceLight.position.set(0, 0.5, 0);
scene.add(bounceLight);

// ═══════════════════════════════════════════════════════════════════════
// FLOOR / STUDIO PLATFORM
// ═══════════════════════════════════════════════════════════════════════
const floorGeometry = new THREE.CircleGeometry(8, 64);
const floorMaterial = new THREE.MeshStandardMaterial({{
  color: 0xE0E0E0,
  roughness: 0.8,
  metalness: 0.1,
  side: THREE.DoubleSide
}});
const floor = new THREE.Mesh(floorGeometry, floorMaterial);
floor.rotation.x = -Math.PI / 2;
floor.position.y = 0;
floor.receiveShadow = true;
scene.add(floor);

// Circular platform under avatar
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

// ───────────────────────────────────────────────────────────────────────
// MATERIALS LIBRARY
// ───────────────────────────────────────────────────────────────────────
const materials = {{
  skin: new THREE.MeshStandardMaterial({{
    color: new THREE.Color(CONFIG.skinTone),
    roughness: 0.6,
    metalness: 0.0,
    flatShading: false
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
// BODY PARTS (Enhanced Topology)
// ───────────────────────────────────────────────────────────────────────

// HEAD (higher detail)
const headGeometry = new THREE.SphereGeometry(0.38, 64, 64);
const head = new THREE.Mesh(headGeometry, materials.skin.clone());
head.position.y = 1.75;
head.castShadow = true;
avatar.add(head);

// NECK
const neckGeometry = new THREE.CylinderGeometry(0.11, 0.13, 0.25, 32);
const neck = new THREE.Mesh(neckGeometry, materials.skin.clone());
neck.position.y = 1.38;
neck.castShadow = true;
avatar.add(neck);

// TORSO (blouse) - fitted
const torsoGeometry = new THREE.CylinderGeometry(0.28, 0.32, 0.45, 32);
const torso = new THREE.Mesh(torsoGeometry, materials.blouse.clone());
torso.position.y = 1.02;
torso.castShadow = true;
avatar.add(torso);

// WAIST (exposed midriff)
const waistGeometry = new THREE.CylinderGeometry(0.26, 0.30, 0.22, 32);
const waist = new THREE.Mesh(waistGeometry, materials.skin.clone());
waist.position.y = 0.69;
waist.castShadow = true;
avatar.add(waist);

// ───────────────────────────────────────────────────────────────────────
// ARMS (Dynamic Pose - Extended)
// ───────────────────────────────────────────────────────────────────────
function createArm(side) {{
  const armGroup = new THREE.Group();
  const xOffset = side * 0.45;
  
  // Shoulder
  const shoulder = new THREE.Mesh(
    new THREE.SphereGeometry(0.12, 24, 24),
    materials.skin.clone()
  );
  shoulder.position.set(xOffset, 1.15, 0);
  armGroup.add(shoulder);
  
  // Upper arm
  const upperArm = new THREE.Mesh(
    new THREE.CylinderGeometry(0.09, 0.08, 0.50, 24),
    materials.skin.clone()
  );
  upperArm.position.set(xOffset * 1.8, 0.95, 0.1);
  upperArm.rotation.z = side * (Math.PI / 3);  // Extended outward
  upperArm.castShadow = true;
  armGroup.add(upperArm);
  
  // Elbow
  const elbow = new THREE.Mesh(
    new THREE.SphereGeometry(0.08, 20, 20),
    materials.skin.clone()
  );
  elbow.position.set(xOffset * 2.4, 0.75, 0.15);
  armGroup.add(elbow);
  
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
  
  // Blouse sleeve (short)
  const sleeve = new THREE.Mesh(
    new THREE.CylinderGeometry(0.11, 0.09, 0.18, 24),
    materials.blouse.clone()
  );
  sleeve.position.set(xOffset * 1.3, 1.08, 0.05);
  sleeve.rotation.z = side * (Math.PI / 3);
  armGroup.add(sleeve);
  
  // Bangle set (3 bangles)
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

createArm(1);   // Right arm
createArm(-1);  // Left arm

// ───────────────────────────────────────────────────────────────────────
// SAREE DRAPING (Complex Realistic Folds)
// ───────────────────────────────────────────────────────────────────────

// Lower saree (wrapped around waist with pleats)
function createSareeLower() {{
  const sareeGroup = new THREE.Group();
  
  // Main skirt cylinder with pleats
  const skirtGeometry = new THREE.CylinderGeometry(0.48, 0.65, 1.3, 64, 20, true);
  const skirtPositions = skirtGeometry.attributes.position;
  
  // Add realistic pleats (front pleats pattern)
  for(let i = 0; i < skirtPositions.count; i++) {{
    const x = skirtPositions.getX(i);
    const y = skirtPositions.getY(i);
    const z = skirtPositions.getZ(i);
    
    const angle = Math.atan2(x, z);
    const radius = Math.sqrt(x*x + z*z);
    
    // Front pleats (0 to PI/3 range)
    if(angle > -Math.PI/6 && angle < Math.PI/3) {{
      const pleatFreq = 12;
      const pleatDepth = 0.08;
      const pleat = Math.sin(angle * pleatFreq) * pleatDepth;
      const newRadius = radius + pleat * (1 - Math.abs(y / 0.65));
      
      skirtPositions.setX(i, Math.sin(angle) * newRadius);
      skirtPositions.setZ(i, Math.cos(angle) * newRadius);
    }}
    
    // Natural draping flow
    const flow = Math.sin(angle * 2 + y * 1.5) * 0.02;
    skirtPositions.setX(i, skirtPositions.getX(i) + flow);
  }}
  
  skirtGeometry.computeVertexNormals();
  const skirt = new THREE.Mesh(skirtGeometry, materials.saree.clone());
  skirt.position.y = 0.05;
  skirt.castShadow = true;
  skirt.receiveShadow = true;
  sareeGroup.add(skirt);
  
  // Gold border at bottom (zari)
  const borderGeometry = new THREE.TorusGeometry(0.64, 0.035, 16, 64);
  const borderMesh = new THREE.Mesh(borderGeometry, materials.border.clone());
  borderMesh.position.y = -0.60;
  borderMesh.rotation.x = Math.PI / 2;
  sareeGroup.add(borderMesh);
  
  avatar.add(sareeGroup);
}}

createSareeLower();

// Pallu (draped over shoulder with flowing fabric)
function createPallu() {{
  const palluGroup = new THREE.Group();
  
  // Main pallu fabric (complex curved surface)
  const palluGeometry = new THREE.PlaneGeometry(0.75, 1.8, 16, 32);
  const palluPositions = palluGeometry.attributes.position;
  
  // Create natural fabric draping curves
  for(let i = 0; i < palluPositions.count; i++) {{
    const x = palluPositions.getX(i);
    const y = palluPositions.getY(i);
    
    // Wave pattern for fabric flow
    const wave1 = Math.sin(y * 2.5 + x * 1.5) * 0.12;
    const wave2 = Math.cos(y * 3 - x * 2) * 0.08;
    const drape = Math.pow((y + 0.9) / 1.8, 2) * 0.15;  // Natural gravity drape
    
    palluPositions.setZ(i, wave1 + wave2 + drape);
  }}
  
  palluGeometry.computeVertexNormals();
  const pallu = new THREE.Mesh(palluGeometry, materials.saree.clone());
  pallu.position.set(-0.25, 0.85, 0.30);
  pallu.rotation.set(0.2, -0.3, 0.15);
  pallu.castShadow = true;
  palluGroup.add(pallu);
  
  // Pallu border (gold trim)
  const palluBorderGeometry = new THREE.PlaneGeometry(0.08, 1.8, 1, 32);
  const palluBorderPositions = palluBorderGeometry.attributes.position;
  
  // Match border to pallu curve
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
  palluGroup.add(palluBorder);
  
  // Decorative folds on pallu
  for(let i = 0; i < 4; i++) {{
    const fold = new THREE.Mesh(
      new THREE.CylinderGeometry(0.01, 0.01, 0.4, 8),
      materials.border.clone()
    );
    fold.position.set(-0.25 + i * 0.08, 0.5 - i * 0.25, 0.35 + i * 0.05);
    fold.rotation.set(0.5, -0.3 + i * 0.1, 0.3);
    palluGroup.add(fold);
  }}
  
  avatar.add(palluGroup);
}}

createPallu();

// ───────────────────────────────────────────────────────────────────────
// HAIR (Long Braid - Realistic Volume)
// ───────────────────────────────────────────────────────────────────────
function createHair() {{
  const hairGroup = new THREE.Group();
  hairGroup.name = 'hairGroup';
  
  // Hair cap (base volume)
  const capGeometry = new THREE.SphereGeometry(0.40, 48, 48, 0, Math.PI * 2, 0, Math.PI * 0.55);
  const cap = new THREE.Mesh(capGeometry, materials.hair.clone());
  cap.position.y = 1.76;
  cap.castShadow = true;
  hairGroup.add(cap);
  
  // Side hair volume (left and right)
  [-1, 1].forEach(side => {{
    const sideHairGeometry = new THREE.SphereGeometry(0.18, 24, 24);
    const sideHair = new THREE.Mesh(sideHairGeometry, materials.hair.clone());
    sideHair.scale.set(0.8, 1.2, 0.6);
    sideHair.position.set(side * 0.38, 1.70, 0.05);
    hairGroup.add(sideHair);
  }});
  
  // Long braid down the back
  const braidSegments = 18;
  const braidLength = 1.5;
  
  for(let i = 0; i < braidSegments; i++) {{
    const t = i / braidSegments;
    const segmentRadius = 0.06 - t * 0.02;  // Taper toward end
    
    const segment = new THREE.Mesh(
      new THREE.SphereGeometry(segmentRadius, 16, 16),
      materials.hair.clone()
    );
    
    // Braid curve (slight swing)
    const swingX = Math.sin(t * Math.PI * 3) * 0.08;
    const swingZ = -0.25 - t * 0.1;
    const yPos = 1.55 - t * braidLength;
    
    segment.position.set(swingX, yPos, swingZ);
    segment.scale.set(1.2, 0.8, 1);
    hairGroup.add(segment);
    
    // Braid texture (small crossing segments)
    if(i % 2 === 0 && i < braidSegments - 2) {{
      const cross = new THREE.Mesh(
        new THREE.CylinderGeometry(segmentRadius * 0.7, segmentRadius * 0.7, segmentRadius * 2, 8),
        materials.hair.clone()
      );
      cross.position.set(swingX, yPos, swingZ);
      cross.rotation.z = Math.PI / 2;
      hairGroup.add(cross);
    }}
  }}
  
  // Hair ornament (white flower - gajra)
  const ornament = new THREE.Mesh(
    new THREE.SphereGeometry(0.08, 16, 16),
    new THREE.MeshStandardMaterial({{ color: 0xFFFFF0, roughness: 0.3 }})
  );
  ornament.position.set(-0.32, 1.82, 0.12);
  hairGroup.add(ornament);
  
  // Flower petals
  for(let i = 0; i < 6; i++) {{
    const angle = (i / 6) * Math.PI * 2;
    const petal = new THREE.Mesh(
      new THREE.SphereGeometry(0.04, 12, 12),
      new THREE.MeshStandardMaterial({{ color: 0xFFFAFA, roughness: 0.2 }})
    );
    petal.scale.set(1.5, 0.5, 0.5);
    petal.position.set(
      -0.32 + Math.cos(angle) * 0.06,
      1.82,
      0.12 + Math.sin(angle) * 0.06
    );
    petal.rotation.y = angle;
    hairGroup.add(petal);
  }}
  
  avatar.add(hairGroup);
}}

createHair();

// ───────────────────────────────────────────────────────────────────────
// FACIAL FEATURES (Enhanced Realism)
// ───────────────────────────────────────────────────────────────────────
function createFace() {{
  const canvas = document.createElement('canvas');
  canvas.width = 1024;
  canvas.height = 1024;
  const ctx = canvas.getContext('2d');
  
  // Base skin tone
  ctx.fillStyle = CONFIG.skinTone;
  ctx.fillRect(0, 0, 1024, 1024);
  
  // Subtle contouring (cheekbones, nose bridge)
  const contour = ctx.createRadialGradient(512, 650, 50, 512, 650, 200);
  contour.addColorStop(0, 'rgba(0,0,0,0)');
  contour.addColorStop(1, 'rgba(139,90,43,0.12)');
  ctx.fillStyle = contour;
  ctx.fillRect(0, 0, 1024, 1024);
  
  // Blush (peach tone)
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
  
  // Eyes
  // Whites
  ctx.fillStyle = '#FFFFFF';
  ctx.beginPath();
  ctx.ellipse(340, 480, 55, 40, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.beginPath();
  ctx.ellipse(684, 480, 55, 40, 0, 0, Math.PI * 2);
  ctx.fill();
  
  // Iris (deep brown with gradient)
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
  
  // Eye highlights
  ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
  ctx.beginPath();
  ctx.arc(348, 472, 8, 0, Math.PI * 2);
  ctx.fill();
  ctx.beginPath();
  ctx.arc(692, 472, 8, 0, Math.PI * 2);
  ctx.fill();
  
  ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
  ctx.beginPath();
  ctx.arc(335, 485, 5, 0, Math.PI * 2);
  ctx.fill();
  ctx.beginPath();
  ctx.arc(679, 485, 5, 0, Math.PI * 2);
  ctx.fill();
  
  // Eyebrows (natural arch)
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
  
  // Eyelashes (upper)
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
  
  // Eyeliner (subtle wing)
  ctx.lineWidth = 6;
  ctx.beginPath();
  ctx.moveTo(285, 460);
  ctx.quadraticCurveTo(340, 455, 395, 470);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(629, 470);
  ctx.quadraticCurveTo(684, 455, 739, 460);
  ctx.stroke();
  
  // Nose (soft shading)
  ctx.strokeStyle = 'rgba(0, 0, 0, 0.15)';
  ctx.lineWidth = 8;
  ctx.beginPath();
  ctx.moveTo(512, 530);
  ctx.quadraticCurveTo(490, 580, 500, 610);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(512, 530);
  ctx.quadraticCurveTo(534, 580, 524, 610);
  ctx.stroke();
  
  // Nostrils
  ctx.fillStyle = 'rgba(0, 0, 0, 0.3)';
  ctx.beginPath();
  ctx.ellipse(495, 615, 8, 5, 0.3, 0, Math.PI * 2);
  ctx.fill();
  ctx.beginPath();
  ctx.ellipse(529, 615, 8, 5, -0.3, 0, Math.PI * 2);
  ctx.fill();
  
  // Lips (full, glossy)
  const lipColor = '#C13C3C';
  ctx.fillStyle = lipColor;
  
  // Upper lip
  ctx.beginPath();
  ctx.moveTo(420, 670);
  ctx.bezierCurveTo(470, 650, 554, 650, 604, 670);
  ctx.bezierCurveTo(570, 665, 454, 665, 420, 670);
  ctx.fill();
  
  // Lower lip
  ctx.beginPath();
  ctx.moveTo(420, 670);
  ctx.bezierCurveTo(454, 700, 570, 700, 604, 670);
  ctx.bezierCurveTo(580, 695, 444, 695, 420, 670);
  ctx.fill();
  
  // Lip contour (darker)
  ctx.strokeStyle = '#8B2D2D';
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(420, 670);
  ctx.bezierCurveTo(470, 650, 554, 650, 604, 670);
  ctx.stroke();
  
  // Lip gloss highlight
  const gloss = ctx.createLinearGradient(512, 675, 512, 690);
  gloss.addColorStop(0, 'rgba(255, 255, 255, 0.5)');
  gloss.addColorStop(1, 'rgba(255, 255, 255, 0)');
  ctx.fillStyle = gloss;
  ctx.beginPath();
  ctx.ellipse(512, 682, 60, 10, 0, 0, Math.PI * 2);
  ctx.fill();
  
  // Bindi (red dot on forehead)
  ctx.fillStyle = '#DC143C';
  ctx.beginPath();
  ctx.arc(512, 380, 15, 0, Math.PI * 2);
  ctx.fill();
  
  // Bindi shine
  ctx.fillStyle = 'rgba(255, 100, 100, 0.6)';
  ctx.beginPath();
  ctx.arc(515, 377, 6, 0, Math.PI * 2);
  ctx.fill();
  
  // Apply texture to head
  const texture = new THREE.CanvasTexture(canvas);
  texture.encoding = THREE.sRGBEncoding;
  head.material.map = texture;
  head.material.needsUpdate = true;
}}

createFace();

// ───────────────────────────────────────────────────────────────────────
// JEWELRY (Necklace, Earrings)
// ───────────────────────────────────────────────────────────────────────

// Necklace (gold chain with pendant)
const necklaceGeometry = new THREE.TorusGeometry(0.18, 0.008, 16, 64, Math.PI * 1.3);
const necklace = new THREE.Mesh(necklaceGeometry, materials.jewelry.clone());
necklace.position.set(0, 1.28, 0.12);
necklace.rotation.x = Math.PI / 2 + 0.2;
avatar.add(necklace);

// Pendant
const pendant = new THREE.Mesh(
  new THREE.SphereGeometry(0.035, 24, 24),
  materials.jewelry.clone()
);
pendant.scale.set(1, 1.5, 0.7);
pendant.position.set(0, 1.18, 0.18);
avatar.add(pendant);

// Earrings (jhumka style - dome shaped)
[-1, 1].forEach(side => {{
  // Ear
  const ear = new THREE.Mesh(
    new THREE.SphereGeometry(0.06, 24, 24),
    materials.skin.clone()
  );
  ear.scale.set(0.7, 1, 0.5);
  ear.position.set(side * 0.38, 1.75, 0.02);
  avatar.add(ear);
  
  // Earring top
  const earringTop = new THREE.Mesh(
    new THREE.SphereGeometry(0.03, 16, 16),
    materials.jewelry.clone()
  );
  earringTop.position.set(side * 0.40, 1.72, 0.05);
  avatar.add(earringTop);
  
  // Earring dome (jhumka)
  const jhumkaGeometry = new THREE.SphereGeometry(0.05, 20, 20, 0, Math.PI * 2, 0, Math.PI / 2);
  const jhumka = new THREE.Mesh(jhumkaGeometry, materials.jewelry.clone());
  jhumka.position.set(side * 0.40, 1.65, 0.06);
  jhumka.rotation.x = Math.PI;
  avatar.add(jhumka);
  
  // Small pearls on jhumka rim
  for(let i = 0; i < 6; i++) {{
    const angle = (i / 6) * Math.PI * 2;
    const pearl = new THREE.Mesh(
      new THREE.SphereGeometry(0.008, 12, 12),
      new THREE.MeshStandardMaterial({{ color: 0xFFFFF0, roughness: 0.2, metalness: 0.3 }})
    );
    pearl.position.set(
      side * 0.40 + Math.cos(angle) * 0.045,
      1.65,
      0.06 + Math.sin(angle) * 0.045
    );
    avatar.add(pearl);
  }}
}});

// ═══════════════════════════════════════════════════════════════════════
// AMBIENT PARTICLES (Subtle sparkle effect)
// ═══════════════════════════════════════════════════════════════════════
const particlesGeometry = new THREE.BufferGeometry();
const particleCount = 200;
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
// INTERACTION CONTROLS
// ═══════════════════════════════════════════════════════════════════════
let autoRotate = true;
let isDragging = false;
let previousMousePosition = {{ x: 0, y: 0 }};
let rotation = {{ x: 0, y: 0 }};

// Mouse controls
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

// Touch controls
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
  const deltaY = e.touches[0].clientY - previousMousePosition.y;
  
  rotation.y += deltaX * 0.01;
  rotation.x += deltaY * 0.01;
  rotation.x = Math.max(-0.5, Math.min(0.5, rotation.x));
  
  avatar.rotation.y = rotation.y;
  avatar.rotation.x = rotation.x;
  
  previousMousePosition = {{
    x: e.touches[0].clientX,
    y: e.touches[0].clientY
  }};
}});

renderer.domElement.addEventListener('touchend', () => {{
  isDragging = false;
}});

// Control functions
function resetView() {{
  rotation = {{ x: 0, y: 0 }};
  avatar.rotation.set(0, 0, 0);
  autoRotate = true;
}}

function toggleRotation() {{
  autoRotate = !autoRotate;
}}

let currentPose = 0;
function changePose() {{
  // Cycle through poses (placeholder - would need full pose system)
  currentPose = (currentPose + 1) % 3;
  console.log('Pose changed to:', currentPose);
  // TODO: Implement pose morphing
}}

function screenshot() {{
  renderer.render(scene, camera);
  const dataURL = renderer.domElement.toDataURL('image/png');
  const link = document.createElement('a');
  link.download = 'saree-avatar-' + Date.now() + '.png';
  link.href = dataURL;
  link.click();
}}

// ═══════════════════════════════════════════════════════════════════════
// ANIMATION LOOP
// ═══════════════════════════════════════════════════════════════════════
const clock = new THREE.Clock();

function animate() {{
  requestAnimationFrame(animate);
  
  const elapsed = clock.getElapsedTime();
  
  // Auto rotation
  if (autoRotate && !isDragging) {{
    avatar.rotation.y += 0.003;
  }}
  
  // Subtle breathing animation
  const breathScale = 1 + Math.sin(elapsed * 1.5) * 0.005;
  torso.scale.y = breathScale;
  waist.scale.y = breathScale;
  
  // Gentle saree flow animation
  const sareeFlow = Math.sin(elapsed * 0.8) * 0.01;
  avatar.children.forEach(child => {{
    if (child.material && child.material === materials.saree) {{
      child.rotation.y = sareeFlow;
    }}
  }});
  
  // Particle animation
  particles.rotation.y += 0.0005;
  particlesMaterial.opacity = 0.4 + Math.sin(elapsed * 2) * 0.2;
  
  // Jewelry glint
  materials.jewelry.emissiveIntensity = 0.3 + Math.sin(elapsed * 3) * 0.2;
  
  renderer.render(scene, camera);
}}

// Hide loading screen and start animation
document.getElementById('loading').classList.add('hidden');
animate();

// ═══════════════════════════════════════════════════════════════════════
// RESPONSIVE RESIZE
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
    return html
