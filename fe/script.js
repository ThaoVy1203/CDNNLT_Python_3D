function showTab(i) {
  document.querySelectorAll('.step-tab').forEach((t, j) => {
    t.classList.remove('active');
    if (j === i) t.classList.add('active');
  });
  document.querySelectorAll('.panel').forEach((p, j) => {
    p.classList.remove('active');
    if (j === i) p.classList.add('active');
  });
  const nav = document.querySelector('.step-nav');
  nav.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function simulateUpload() {
  const zone = document.querySelector('.upload-zone');
  const result = document.getElementById('recognized-result');
  zone.innerHTML = `
    <div class="upload-icon" style="background:var(--teal-bg);border-color:rgba(42,122,98,0.2)">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="var(--teal)" stroke-width="2">
        <polyline points="20 6 9 17 4 12"/>
      </svg>
    </div>
    <h3 style="color:var(--teal)">Đã nhận ảnh thành công</h3>
    <p>Đang phân tích đề bài bằng AI<span id="dots">...</span></p>
  `;
  let d = 0;
  const ti = setInterval(() => {
    const el = document.getElementById('dots');
    if (el) el.textContent = ['...', '·..', '..·', '...'][d++ % 4];
  }, 320);
  setTimeout(() => {
    clearInterval(ti);
    zone.innerHTML = `
      <div class="upload-icon" style="background:var(--teal-bg);border-color:rgba(42,122,98,0.2)">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="var(--teal)" stroke-width="2">
          <polyline points="20 6 9 17 4 12"/>
        </svg>
      </div>
      <h3 style="color:var(--teal)">Phân tích hoàn tất</h3>
      <p style="color:var(--teal);margin-bottom:0;font-size:13px;font-weight:400">AI đã nhận diện đề bài thành công</p>
    `;
    result.style.display = 'block';
    result.style.animation = 'fadeUp .35s ease';
  }, 1800);
}

let playing = false, progW = 60, progInt = null;
function togglePlay() {
  playing = !playing;
  const btn = document.getElementById('playBtn');
  if (playing) {
    btn.textContent = '⏸';
    progInt = setInterval(() => {
      progW = Math.min(100, progW + 0.35);
      const f = document.getElementById('progFill');
      if (f) f.style.width = progW + '%';
      if (progW >= 100) { playing = false; btn.textContent = '▶'; clearInterval(progInt); }
    }, 50);
  } else {
    btn.textContent = '▶';
    clearInterval(progInt);
  }
}

document.querySelectorAll('.ctrl').forEach(btn => {
  btn.addEventListener('click', function () {
    document.querySelectorAll('.ctrl').forEach(b => b.classList.remove('active'));
    this.classList.add('active');
  });
});
// ═══════════════════════════════════════════════════════════
// TAB NAVIGATION
// ═══════════════════════════════════════════════════════════
function showTab(index) {
  // Hide all panels
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.step-tab').forEach(t => {
    t.classList.remove('active');
  });
  
  // Show selected panel
  document.getElementById('panel-' + index).classList.add('active');
  document.getElementById('tab-' + index).classList.add('active');
  
  // Initialize 3D if needed
  if (index === 1 && !window.scene3d) {
    init3DScene();
  }
  if (index === 2 && !window.constructionScene) {
    initConstructionScene();
  }
  if (index === 4 && !window.resultScene) {
    initResultScene();
  }
}

// ═══════════════════════════════════════════════════════════
// UPLOAD SIMULATION
// ═══════════════════════════════════════════════════════════
function simulateUpload() {
  const card = document.getElementById('recognized-result');
  card.style.display = 'block';
  setTimeout(() => {
    card.style.animation = 'fadeUp 0.4s ease';
  }, 100);
}

// ═══════════════════════════════════════════════════════════
// TOGGLE FEATURES
// ═══════════════════════════════════════════════════════════
function toggleFeature(feature) {
  const toggle = document.getElementById('toggle-' + feature);
  toggle.classList.toggle('on');
}

function toggleView(mode) {
  document.querySelectorAll('.canvas-toolbar .ctrl').forEach(c => c.classList.remove('active'));
  event.target.classList.add('active');
}

function resetView() {
  if (window.camera3d && window.controls3d) {
    window.camera3d.position.set(5, 5, 5);
    window.controls3d.reset();
  }
}

function toggleWireframe() {
  event.target.classList.toggle('active');
}

function toggleAxes() {
  event.target.classList.toggle('active');
  if (window.axesHelper) {
    window.axesHelper.visible = !window.axesHelper.visible;
  }
}

// ═══════════════════════════════════════════════════════════
// 3D SCENE INITIALIZATION
// ═══════════════════════════════════════════════════════════
function init3DScene() {
  const canvas = document.getElementById('threejs-canvas');
  const container = document.getElementById('canvas3d');
  
  // Scene setup
  window.scene3d = new THREE.Scene();
  window.scene3d.background = new THREE.Color(0xf5f0e8);
  
  // Camera
  window.camera3d = new THREE.PerspectiveCamera(
    50,
    container.clientWidth / container.clientHeight,
    0.1,
    1000
  );
  window.camera3d.position.set(5, 5, 5);
  window.camera3d.lookAt(0, 0, 0);
  
  // Renderer
  window.renderer3d = new THREE.WebGLRenderer({ canvas, antialias: true });
  window.renderer3d.setSize(container.clientWidth, container.clientHeight);
  
  // Lights
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
  window.scene3d.add(ambientLight);
  
  const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
  directionalLight.position.set(5, 10, 5);
  window.scene3d.add(directionalLight);
  
  // Axes helper
  window.axesHelper = new THREE.AxesHelper(3);
  window.scene3d.add(window.axesHelper);
  
  // Grid
  const gridHelper = new THREE.GridHelper(6, 12, 0x8a7f6a, 0xb5ac98);
  gridHelper.position.y = 0;
  window.scene3d.add(gridHelper);
  
  // Build pyramid S.ABCD
  buildPyramid(window.scene3d);
  
  // Animation loop
  function animate() {
    requestAnimationFrame(animate);
    window.renderer3d.render(window.scene3d, window.camera3d);
  }
  animate();
  
  // Mouse controls (simple rotation)
  let isDragging = false;
  let previousMousePosition = { x: 0, y: 0 };
  
  canvas.addEventListener('mousedown', (e) => {
    isDragging = true;
    previousMousePosition = { x: e.clientX, y: e.clientY };
  });
  
  canvas.addEventListener('mousemove', (e) => {
    if (isDragging) {
      const deltaX = e.clientX - previousMousePosition.x;
      const deltaY = e.clientY - previousMousePosition.y;
      
      window.camera3d.position.x += deltaX * 0.01;
      window.camera3d.position.y -= deltaY * 0.01;
      window.camera3d.lookAt(0, 1, 0);
      
      previousMousePosition = { x: e.clientX, y: e.clientY };
    }
  });
  
  canvas.addEventListener('mouseup', () => {
    isDragging = false;
  });
  
  canvas.addEventListener('wheel', (e) => {
    e.preventDefault();
    const delta = e.deltaY * 0.001;
    window.camera3d.position.multiplyScalar(1 + delta);
  });
}

function buildPyramid(scene) {
  const a = 2; // Base side length
  const h = 2 * Math.sqrt(2); // Height SA
  
  // Define vertices
  const A = new THREE.Vector3(0, 0, 0);
  const B = new THREE.Vector3(a, 0, 0);
  const C = new THREE.Vector3(a, 0, a);
  const D = new THREE.Vector3(0, 0, a);
  const S = new THREE.Vector3(0, h, 0);
  const M = new THREE.Vector3(a/2, 0, 0); // Midpoint of AB
  
  // Material for edges
  const edgeMaterial = new THREE.LineBasicMaterial({ color: 0x3d52a0, linewidth: 2 });
  const highlightMaterial = new THREE.LineBasicMaterial({ color: 0xa07840, linewidth: 3 });
  const dashedMaterial = new THREE.LineDashedMaterial({ 
    color: 0x2a7a62, 
    linewidth: 1, 
    dashSize: 0.2, 
    gapSize: 0.1 
  });
  
  // Draw base ABCD
  const baseGeometry = new THREE.BufferGeometry().setFromPoints([A, B, C, D, A]);
  const baseLine = new THREE.Line(baseGeometry, edgeMaterial);
  scene.add(baseLine);
  
  // Draw base face
  const baseShape = new THREE.Shape();
  baseShape.moveTo(0, 0);
  baseShape.lineTo(a, 0);
  baseShape.lineTo(a, a);
  baseShape.lineTo(0, a);
  baseShape.lineTo(0, 0);
  
  const baseGeom = new THREE.ShapeGeometry(baseShape);
  const baseMesh = new THREE.Mesh(
    baseGeom,
    new THREE.MeshBasicMaterial({ 
      color: 0x3d52a0, 
      transparent: true, 
      opacity: 0.1,
      side: THREE.DoubleSide 
    })
  );
  baseMesh.rotation.x = -Math.PI / 2;
  scene.add(baseMesh);
  
  // Draw edges SA, SB, SC, SD
  const edges = [
    [S, A], [S, B], [S, C], [S, D]
  ];
  
  edges.forEach(([p1, p2]) => {
    const geom = new THREE.BufferGeometry().setFromPoints([p1, p2]);
    const line = new THREE.Line(geom, edgeMaterial);
    scene.add(line);
  });
  
  // Highlight SM
  const smGeometry = new THREE.BufferGeometry().setFromPoints([S, M]);
  const smLine = new THREE.Line(smGeometry, highlightMaterial);
  scene.add(smLine);
  
  // Draw AM (projection)
  const amGeometry = new THREE.BufferGeometry().setFromPoints([A, M]);
  const amLine = new THREE.Line(amGeometry, dashedMaterial);
  amLine.computeLineDistances();
  scene.add(amLine);
  
  // Add vertex spheres
  const vertices = [
    { pos: A, label: 'A', color: 0x3d52a0 },
    { pos: B, label: 'B', color: 0x3d52a0 },
    { pos: C, label: 'C', color: 0x3d52a0 },
    { pos: D, label: 'D', color: 0x3d52a0 },
    { pos: S, label: 'S', color: 0xa07840 },
    { pos: M, label: 'M', color: 0xa07840 }
  ];
  
  vertices.forEach(v => {
    const sphereGeom = new THREE.SphereGeometry(0.08, 16, 16);
    const sphereMat = new THREE.MeshBasicMaterial({ color: v.color });
    const sphere = new THREE.Mesh(sphereGeom, sphereMat);
    sphere.position.copy(v.pos);
    scene.add(sphere);
  });
}

// ═══════════════════════════════════════════════════════════
// CONSTRUCTION SCENE (Panel 2)
// ═══════════════════════════════════════════════════════════
let constructionStep = 0;
let isPlaying = false;
let playInterval = null;

function initConstructionScene() {
  const canvas = document.getElementById('construction-canvas');
  const container = document.getElementById('canvas-construction');
  
  window.constructionScene = new THREE.Scene();
  window.constructionScene.background = new THREE.Color(0xf5f0e8);
  
  const camera = new THREE.PerspectiveCamera(
    50,
    container.clientWidth / container.clientHeight,
    0.1,
    1000
  );
  camera.position.set(5, 5, 5);
  camera.lookAt(0, 0, 0);
  
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
  renderer.setSize(container.clientWidth, container.clientHeight);
  
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
  window.constructionScene.add(ambientLight);
  
  const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
  directionalLight.position.set(5, 10, 5);
  window.constructionScene.add(directionalLight);
  
  const gridHelper = new THREE.GridHelper(6, 12, 0x8a7f6a, 0xb5ac98);
  window.constructionScene.add(gridHelper);
  
  window.constructionRenderer = renderer;
  window.constructionCamera = camera;
  
  updateConstructionStep(0);
  
  function animate() {
    requestAnimationFrame(animate);
    renderer.render(window.constructionScene, camera);
  }
  animate();
}

function updateConstructionStep(step) {
  constructionStep = step;
  
  // Clear scene except lights and grid
  const objectsToRemove = [];
  window.constructionScene.children.forEach(child => {
    if (child.type !== 'AmbientLight' && 
        child.type !== 'DirectionalLight' && 
        child.type !== 'GridHelper') {
      objectsToRemove.push(child);
    }
  });
  objectsToRemove.forEach(obj => window.constructionScene.remove(obj));
  
  const a = 2;
  const h = 2 * Math.sqrt(2);
  
  const A = new THREE.Vector3(0, 0, 0);
  const B = new THREE.Vector3(a, 0, 0);
  const C = new THREE.Vector3(a, 0, a);
  const D = new THREE.Vector3(0, 0, a);
  const S = new THREE.Vector3(0, h, 0);
  const M = new THREE.Vector3(a/2, 0, 0);
  
  const edgeMaterial = new THREE.LineBasicMaterial({ color: 0x3d52a0, linewidth: 2 });
  const highlightMaterial = new THREE.LineBasicMaterial({ color: 0xa07840, linewidth: 3 });
  
  // Step 0: Base ABCD
  if (step >= 0) {
    const baseGeometry = new THREE.BufferGeometry().setFromPoints([A, B, C, D, A]);
    const baseLine = new THREE.Line(baseGeometry, edgeMaterial);
    window.constructionScene.add(baseLine);
    
    [A, B, C, D].forEach(v => {
      const sphere = new THREE.Mesh(
        new THREE.SphereGeometry(0.08, 16, 16),
        new THREE.MeshBasicMaterial({ color: 0x3d52a0 })
      );
      sphere.position.copy(v);
      window.constructionScene.add(sphere);
    });
  }
  
  // Step 1: Add SA
  if (step >= 1) {
    const saGeometry = new THREE.BufferGeometry().setFromPoints([S, A]);
    const saLine = new THREE.Line(saGeometry, highlightMaterial);
    window.constructionScene.add(saLine);
    
    const sphere = new THREE.Mesh(
      new THREE.SphereGeometry(0.08, 16, 16),
      new THREE.MeshBasicMaterial({ color: 0xa07840 })
    );
    sphere.position.copy(S);
    window.constructionScene.add(sphere);
  }
  
  // Step 2: Add M and SM
  if (step >= 2) {
    const sphere = new THREE.Mesh(
      new THREE.SphereGeometry(0.08, 16, 16),
      new THREE.MeshBasicMaterial({ color: 0xa07840 })
    );
    sphere.position.copy(M);
    window.constructionScene.add(sphere);
    
    const smGeometry = new THREE.BufferGeometry().setFromPoints([S, M]);
    const smLine = new THREE.Line(smGeometry, highlightMaterial);
    window.constructionScene.add(smLine);
  }
  
  // Step 3: Add other edges
  if (step >= 3) {
    [[S, B], [S, C], [S, D]].forEach(([p1, p2]) => {
      const geom = new THREE.BufferGeometry().setFromPoints([p1, p2]);
      const line = new THREE.Line(geom, edgeMaterial);
      window.constructionScene.add(line);
    });
  }
  
  // Step 4: Highlight angle
  if (step >= 4) {
    // Add angle arc visualization here if needed
  }
  
  // Update progress bar
  const progress = (step / 4) * 100;
  document.getElementById('progress-bar').style.width = progress + '%';
  
  // Update step items
  document.querySelectorAll('.step-item').forEach((item, idx) => {
    item.classList.remove('done', 'active', 'faded');
    if (idx < step) item.classList.add('done');
    else if (idx === step) item.classList.add('active');
    else item.classList.add('faded');
  });
}

function togglePlay() {
  isPlaying = !isPlaying;
  const btn = document.getElementById('play-btn');
  
  if (isPlaying) {
    btn.innerHTML = '⏸';
    playInterval = setInterval(() => {
      if (constructionStep < 4) {
        updateConstructionStep(constructionStep + 1);
      } else {
        togglePlay();
      }
    }, 1500);
  } else {
    btn.innerHTML = '▶';
    if (playInterval) clearInterval(playInterval);
  }
}

function constructionRestart() {
  updateConstructionStep(0);
  if (isPlaying) togglePlay();
}

function constructionPrev() {
  if (constructionStep > 0) {
    updateConstructionStep(constructionStep - 1);
  }
}

function constructionNext() {
  if (constructionStep < 4) {
    updateConstructionStep(constructionStep + 1);
  }
}

function seekConstruction(event) {
  const rect = event.target.getBoundingClientRect();
  const x = event.clientX - rect.left;
  const percent = x / rect.width;
  const step = Math.floor(percent * 5);
  updateConstructionStep(Math.min(step, 4));
}

// ═══════════════════════════════════════════════════════════
// RESULT SCENE (Panel 4)
// ═══════════════════════════════════════════════════════════
function initResultScene() {
  const canvas = document.getElementById('result-canvas');
  const container = canvas.parentElement;
  
  window.resultScene = new THREE.Scene();
  window.resultScene.background = new THREE.Color(0xf5f0e8);
  
  const camera = new THREE.PerspectiveCamera(
    50,
    container.clientWidth / container.clientHeight,
    0.1,
    1000
  );
  camera.position.set(4, 4, 4);
  camera.lookAt(0, 1, 0);
  
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
  renderer.setSize(container.clientWidth, container.clientHeight);
  
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
  window.resultScene.add(ambientLight);
  
  const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
  directionalLight.position.set(5, 10, 5);
  window.resultScene.add(directionalLight);
  
  buildPyramid(window.resultScene);
  
  function animate() {
    requestAnimationFrame(animate);
    window.resultScene.rotation.y += 0.005;
    renderer.render(window.resultScene, camera);
  }
  animate();
}

// ═══════════════════════════════════════════════════════════
// EXPORT FUNCTIONS
// ═══════════════════════════════════════════════════════════
function exportPDF() {
  alert('Chức năng xuất PDF đang được phát triển!');
}

function saveImage() {
  alert('Chức năng lưu hình ảnh đang được phát triển!');
}

function shareResult() {
  alert('Chức năng chia sẻ đang được phát triển!');
}

// ═══════════════════════════════════════════════════════════
// WINDOW RESIZE HANDLER
// ═══════════════════════════════════════════════════════════
window.addEventListener('resize', () => {
  if (window.renderer3d && window.camera3d) {
    const container = document.getElementById('canvas3d');
    window.camera3d.aspect = container.clientWidth / container.clientHeight;
    window.camera3d.updateProjectionMatrix();
    window.renderer3d.setSize(container.clientWidth, container.clientHeight);
  }
});

// ═══════════════════════════════════════════════════════════
// INITIALIZE ON LOAD
// ═══════════════════════════════════════════════════════════
window.addEventListener('DOMContentLoaded', () => {
  console.log('Geo3D initialized');
});
