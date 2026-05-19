/**
 * Three.js Viewer - Vanilla JS version
 * Không dùng ES6 modules
 */

(function() {
  'use strict';
  
  // Check THREE is available
  if (typeof THREE === 'undefined') {
    console.error('THREE.js must be loaded before three-viewer.js');
    return;
  }

  class ThreeViewerManager {
    constructor() {
      this.scene = null;
      this.camera = null;
      this.renderer = null;
      this.controls = null;
      this.geometryData = null;
      this.currentStep = 0;
      this.isPlaying = false;
      this.playInterval = null;
      this.objects = new Map();
      this.annotations = null;
      this.grid = null;
      this.axes = null;
      this.animationId = null;
    }

    init(canvasId) {
      const canvas = document.getElementById(canvasId);
      if (!canvas) {
        console.error('Canvas not found:', canvasId);
        return;
      }

      console.log('Initializing viewer for canvas:', canvasId);
      console.log('Canvas element:', canvas);
      console.log('Canvas client dimensions:', canvas.clientWidth, 'x', canvas.clientHeight);
      console.log('Canvas width/height attributes:', canvas.width, 'x', canvas.height);

      // Ensure canvas has dimensions
      if (canvas.clientWidth === 0 || canvas.clientHeight === 0) {
        console.warn('Canvas has zero dimensions, using defaults');
        // Set default dimensions if not set
        if (!canvas.width) canvas.width = 800;
        if (!canvas.height) canvas.height = 400;
      }

      // Scene
      this.scene = new THREE.Scene();
      this.scene.background = new THREE.Color(0xf5f0e8);

      // Camera
      const width = canvas.clientWidth || canvas.width || 800;
      const height = canvas.clientHeight || canvas.height || 400;
      
      this.camera = new THREE.PerspectiveCamera(
        50,
        width / height,
        0.1,
        1000
      );
      this.camera.position.set(3, 3, 3);
      this.camera.lookAt(0, 0, 0);

      // Renderer
      this.renderer = new THREE.WebGLRenderer({
        canvas: canvas,
        antialias: true,
        alpha: true
      });
      this.renderer.setSize(width, height);
      this.renderer.setPixelRatio(window.devicePixelRatio);

      console.log('Renderer size set to:', width, 'x', height);

      // Lights
      const ambient = new THREE.AmbientLight(0xffffff, 0.6);
      this.scene.add(ambient);

      const directional = new THREE.DirectionalLight(0xffffff, 0.8);
      directional.position.set(5, 10, 5);
      this.scene.add(directional);

      // Controls - Enhanced for better user experience
      if (typeof THREE.OrbitControls !== 'undefined') {
        this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
        
        // Enable damping for smooth rotation
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;
        
        // Set distance limits
        this.controls.minDistance = 1;
        this.controls.maxDistance = 20;
        
        // Enable zoom
        this.controls.enableZoom = true;
        this.controls.zoomSpeed = 1.0;
        
        // Enable rotation
        this.controls.enableRotate = true;
        this.controls.rotateSpeed = 1.0;
        
        // Enable panning
        this.controls.enablePan = true;
        this.controls.panSpeed = 0.8;
        
        // Set key bindings
        this.controls.keys = {
          LEFT: 37,  // Arrow Left
          UP: 38,    // Arrow Up
          RIGHT: 39, // Arrow Right
          BOTTOM: 40 // Arrow Down
        };
        
        // Mouse buttons
        this.controls.mouseButtons = {
          LEFT: THREE.MOUSE.ROTATE,
          MIDDLE: THREE.MOUSE.DOLLY,
          RIGHT: THREE.MOUSE.PAN
        };
        
        console.log('✓ OrbitControls initialized with full interaction');
      } else {
        console.warn('⚠️ OrbitControls not available');
      }

      // Helpers
      this.grid = new THREE.GridHelper(10, 10, 0x8a7f6a, 0xb5ac98);
      this.scene.add(this.grid);

      this.axes = new THREE.AxesHelper(5);
      this.scene.add(this.axes);

      // Annotations group
      this.annotations = new THREE.Group();
      this.annotations.name = 'annotations';
      this.scene.add(this.annotations);

      // Handle resize
      const handleResize = () => {
        const newWidth = canvas.clientWidth || canvas.width;
        const newHeight = canvas.clientHeight || canvas.height;
        this.camera.aspect = newWidth / newHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(newWidth, newHeight);
      };
      
      window.addEventListener('resize', handleResize);

      // Start animation
      this.startAnimation();

      console.log('✓ ThreeViewerManager initialized for', canvasId);
    }

    startAnimation() {
      const animate = () => {
        this.animationId = requestAnimationFrame(animate);
        if (this.controls) {
          this.controls.update();
        }
        this.renderer.render(this.scene, this.camera);
      };
      animate();
    }

    loadGeometry(data) {
      this.geometryData = data;
      this.buildGeometry(data);
      this.currentStep = 0;
      this.goToStep(0);
    }

    buildGeometry(data) {
      this.clearObjects();

      // Build points
      Object.entries(data.points).forEach(([name, coords]) => {
        const point = this.createPoint(name, coords);
        this.objects.set(name, point);
        this.scene.add(point);
      });

      // Build edges
      data.edges.forEach((edge) => {
        const edgeName = edge.start + '-' + edge.end;
        const line = this.createEdge(
          data.points[edge.start],
          data.points[edge.end],
          edgeName,
          edge.style || 'solid'
        );
        this.objects.set(edgeName, line);
        this.scene.add(line);
      });

      // Build faces
      data.faces.forEach((face, index) => {
        const mesh = this.createFace(face.vertices.map(v => data.points[v]));
        this.objects.set('face_' + index, mesh);
        this.scene.add(mesh);
      });

      // Build annotations (ký hiệu hình học)
      if (data.annotations) {
        this.buildAnnotations(data.annotations, data.points);
      }

      this.fitCamera();
    }

    buildAnnotations(annotations, points) {
      console.log('🎨 Building annotations:', annotations);
      
      // Clear existing annotations
      this.clearAnnotations();
      
      // Edge labels (độ dài cạnh)
      if (annotations.edges && Array.isArray(annotations.edges)) {
        annotations.edges.forEach(edgeAnnotation => {
          const edge = edgeAnnotation.edge;
          const label = edgeAnnotation.label;
          const [start, end] = edge.split('-');
          
          if (points[start] && points[end]) {
            const labelSprite = this.createEdgeLabel(
              points[start],
              points[end],
              label
            );
            labelSprite.userData.annotationType = 'edge_label';
            labelSprite.userData.relatedEdge = edge;
            this.annotations.add(labelSprite);
          }
        });
      }
      
      // Perpendicular symbols (ký hiệu vuông góc)
      if (annotations.perpendicular && Array.isArray(annotations.perpendicular)) {
        annotations.perpendicular.forEach(perp => {
          const vertex = perp.vertex;
          const line1 = perp.line1;
          const line2 = perp.line2;

          if (points[vertex]) {
            // FIX: truyền tên vertex (string), không phải tọa độ.
            // Bên trong createPerpendicularSymbol so sánh `p1Start === vertex`
            // (tên cạnh "A" với tên đỉnh "A"). Nếu truyền coords, so sánh luôn fail.
            const perpSymbol = this.createPerpendicularSymbol(
              vertex,
              line1,
              line2,
              points
            );
            if (perpSymbol) {
              perpSymbol.visible = false;
              perpSymbol.userData.annotationType = 'perpendicular';
              perpSymbol.userData.relatedVertex = vertex;
              perpSymbol.userData.relatedLines = [line1, line2];
              this.annotations.add(perpSymbol);
            }
          }
        });
      }

      // Angle symbols (ký hiệu góc)
      if (annotations.angles && Array.isArray(annotations.angles)) {
        annotations.angles.forEach(angle => {
          const vertex = angle.vertex;
          const line1 = angle.line1;
          const line2 = angle.line2;
          const value = angle.angle || angle.value;

          if (points[vertex]) {
            // FIX: truyền tên vertex (string), không phải tọa độ.
            const angleSymbol = this.createAngleSymbol(
              vertex,
              line1,
              line2,
              value,
              points
            );
            if (angleSymbol) {
              angleSymbol.visible = false;
              angleSymbol.userData.annotationType = 'angle';
              angleSymbol.userData.relatedVertex = vertex;
              angleSymbol.userData.relatedLines = [line1, line2];
              this.annotations.add(angleSymbol);
            }
          }
        });
      }
      
      // Equal segments marks (dấu gạch cạnh bằng nhau)
      if (annotations.equal_segments && Array.isArray(annotations.equal_segments)) {
        annotations.equal_segments.forEach(equalSeg => {
          const segments = equalSeg.segments;
          const mark = equalSeg.mark; // 'single', 'double', 'triple'
          
          segments.forEach(segment => {
            const [start, end] = segment.split('-');
            if (points[start] && points[end]) {
              const markSymbol = this.createEqualSegmentMark(
                points[start],
                points[end],
                mark
              );
              if (markSymbol) {
                markSymbol.visible = false; // Hidden by default
                markSymbol.userData.annotationType = 'equal_segment';
                markSymbol.userData.relatedEdge = segment;
                this.annotations.add(markSymbol);
              }
            }
          });
        });
      }
      
      console.log('✅ Annotations built:', this.annotations.children.length, 'objects');
    }

    createEdgeLabel(start, end, text) {
      // Calculate midpoint
      const midpoint = [
        (start[0] + end[0]) / 2,
        (start[1] + end[1]) / 2,
        (start[2] + end[2]) / 2
      ];
      
      // Create label sprite with TRANSPARENT background
      const canvas = document.createElement('canvas');
      const context = canvas.getContext('2d');
      // Tăng kích thước canvas để chữ sắc nét hơn
      canvas.width = 512;
      canvas.height = 256;
      
      // Clear canvas (transparent background)
      context.clearRect(0, 0, canvas.width, canvas.height);
      
      // Set font - tăng size cho dễ đọc
      context.font = 'Bold 80px Arial';
      context.textAlign = 'center';
      context.textBaseline = 'middle';
      
      // Add white outline for better visibility
      context.strokeStyle = 'rgba(255, 255, 255, 0.95)';
      context.lineWidth = 12;
      context.strokeText(text, 256, 128);
      
      // Text in gold color
      context.fillStyle = '#a07840'; // Gold color
      context.fillText(text, 256, 128);
      
      const texture = new THREE.CanvasTexture(canvas);
      const material = new THREE.SpriteMaterial({
        map: texture,
        transparent: true,
        depthTest: false
      });
      const sprite = new THREE.Sprite(material);
      sprite.position.set(midpoint[0], midpoint[1] + 0.18, midpoint[2]);
      // Tăng scale để label to hơn trong cảnh 3D
      sprite.scale.set(0.7, 0.35, 1);
      sprite.visible = false; // Hidden by default, will show in steps
      
      // Store edge name for step-by-step display
      sprite.userData.edgeName = start + '-' + end;
      
      return sprite;
    }

    createPerpendicularSymbol(vertex, line1, line2, points) {
      // Ô vuông nhỏ thể hiện góc vuông tại vertex
      const size = 0.08;
      
      // Get direction vectors
      const [p1Start, p1End] = line1.split('-');
      const [p2Start, p2End] = line2.split('-');
      
      // Find directions from vertex (vertex is point name, not coords)
      let dir1, dir2;
      let vertexCoords = null;
      
      // Find vertex coordinates
      if (typeof vertex === 'string' && points[vertex]) {
        vertexCoords = points[vertex];
      } else if (Array.isArray(vertex)) {
        vertexCoords = vertex;
      }
      
      if (!vertexCoords) return null;
      
      if (p1Start === vertex && points[p1End]) {
        dir1 = new THREE.Vector3(
          points[p1End][0] - vertexCoords[0],
          points[p1End][1] - vertexCoords[1],
          points[p1End][2] - vertexCoords[2]
        ).normalize();
      } else if (p1End === vertex && points[p1Start]) {
        dir1 = new THREE.Vector3(
          points[p1Start][0] - vertexCoords[0],
          points[p1Start][1] - vertexCoords[1],
          points[p1Start][2] - vertexCoords[2]
        ).normalize();
      }
      
      if (p2Start === vertex && points[p2End]) {
        dir2 = new THREE.Vector3(
          points[p2End][0] - vertexCoords[0],
          points[p2End][1] - vertexCoords[1],
          points[p2End][2] - vertexCoords[2]
        ).normalize();
      } else if (p2End === vertex && points[p2Start]) {
        dir2 = new THREE.Vector3(
          points[p2Start][0] - vertexCoords[0],
          points[p2Start][1] - vertexCoords[1],
          points[p2Start][2] - vertexCoords[2]
        ).normalize();
      }
      
      if (!dir1 || !dir2) return null;
      
      // Create square geometry
      const p1 = new THREE.Vector3(vertexCoords[0], vertexCoords[1], vertexCoords[2]).add(dir1.clone().multiplyScalar(size));
      const p2 = p1.clone().add(dir2.clone().multiplyScalar(size));
      const p3 = new THREE.Vector3(vertexCoords[0], vertexCoords[1], vertexCoords[2]).add(dir2.clone().multiplyScalar(size));
      
      const geometry = new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3(vertexCoords[0], vertexCoords[1], vertexCoords[2]),
        p1,
        p2,
        p3,
        new THREE.Vector3(vertexCoords[0], vertexCoords[1], vertexCoords[2])
      ]);
      
      const material = new THREE.LineBasicMaterial({
        color: 0x2a7a62, // Teal color
        linewidth: 2
      });
      
      const line = new THREE.Line(geometry, material);
      return line;
    }

    createAngleSymbol(vertex, line1, line2, value, points) {
      // Create arc to show angle
      const radius = 0.15;
      
      // Find vertex coordinates
      let vertexCoords = null;
      if (typeof vertex === 'string' && points[vertex]) {
        vertexCoords = points[vertex];
      } else if (Array.isArray(vertex)) {
        vertexCoords = vertex;
      }
      
      if (!vertexCoords) return null;
      
      // Similar to perpendicular, get directions
      const [p1Start, p1End] = line1.split('-');
      const [p2Start, p2End] = line2.split('-');
      
      let dir1, dir2;
      
      if (p1Start === vertex && points[p1End]) {
        dir1 = new THREE.Vector3(
          points[p1End][0] - vertexCoords[0],
          points[p1End][1] - vertexCoords[1],
          points[p1End][2] - vertexCoords[2]
        ).normalize();
      } else if (p1End === vertex && points[p1Start]) {
        dir1 = new THREE.Vector3(
          points[p1Start][0] - vertexCoords[0],
          points[p1Start][1] - vertexCoords[1],
          points[p1Start][2] - vertexCoords[2]
        ).normalize();
      }
      
      if (p2Start === vertex && points[p2End]) {
        dir2 = new THREE.Vector3(
          points[p2End][0] - vertexCoords[0],
          points[p2End][1] - vertexCoords[1],
          points[p2End][2] - vertexCoords[2]
        ).normalize();
      } else if (p2End === vertex && points[p2Start]) {
        dir2 = new THREE.Vector3(
          points[p2Start][0] - vertexCoords[0],
          points[p2Start][1] - vertexCoords[1],
          points[p2Start][2] - vertexCoords[2]
        ).normalize();
      }
      
      if (!dir1 || !dir2) return null;
      
      // Create arc curve
      const arcPoints = [];
      const steps = 16;
      for (let i = 0; i <= steps; i++) {
        const t = i / steps;
        const dir = dir1.clone().lerp(dir2, t).normalize();
        const point = new THREE.Vector3(vertexCoords[0], vertexCoords[1], vertexCoords[2]).add(dir.multiplyScalar(radius));
        arcPoints.push(point);
      }
      
      const geometry = new THREE.BufferGeometry().setFromPoints(arcPoints);
      const material = new THREE.LineBasicMaterial({
        color: 0xa07840, // Gold color
        linewidth: 2
      });
      
      const arc = new THREE.Line(geometry, material);
      
      // Add label if value provided
      if (value) {
        const labelPos = dir1.clone().add(dir2).normalize().multiplyScalar(radius * 1.3);
        const label = this.createLabel(value + '°');
        label.position.set(
          vertexCoords[0] + labelPos.x,
          vertexCoords[1] + labelPos.y,
          vertexCoords[2] + labelPos.z
        );
        
        const group = new THREE.Group();
        group.add(arc);
        group.add(label);
        return group;
      }
      
      return arc;
    }

    createEqualSegmentMark(start, end, markType) {
      // Tick gạch vuông góc với cạnh, đặt ở midpoint của đoạn.
      const midpoint = new THREE.Vector3(
        (start[0] + end[0]) / 2,
        (start[1] + end[1]) / 2,
        (start[2] + end[2]) / 2
      );

      const edgeDir = new THREE.Vector3(
        end[0] - start[0],
        end[1] - start[1],
        end[2] - start[2]
      ).normalize();

      // Tìm hướng vuông góc với cạnh trong KHÔNG GIAN 3D bằng cross product
      // (perpDir = edgeDir × ref). Nếu cạnh gần song song với Y thì đổi ref.
      let ref = new THREE.Vector3(0, 1, 0);
      if (Math.abs(edgeDir.dot(ref)) > 0.95) {
        ref = new THREE.Vector3(1, 0, 0);
      }
      const perpDir = new THREE.Vector3().crossVectors(edgeDir, ref).normalize();

      const tickSize = 0.10;     // Nhỏ gọn để không che cạnh
      const tickSpacing = 0.05;
      const numTicks = markType === 'single' ? 1 : markType === 'double' ? 2 : 3;

      const group = new THREE.Group();
      const material = new THREE.LineBasicMaterial({
        color: 0xa07840, // gold
        linewidth: 3,
        depthTest: false
      });

      for (let i = 0; i < numTicks; i++) {
        const offset = (i - (numTicks - 1) / 2) * tickSpacing;
        const tickCenter = midpoint.clone().add(edgeDir.clone().multiplyScalar(offset));

        const p1 = tickCenter.clone().add(perpDir.clone().multiplyScalar(tickSize / 2));
        const p2 = tickCenter.clone().add(perpDir.clone().multiplyScalar(-tickSize / 2));

        const geometry = new THREE.BufferGeometry().setFromPoints([p1, p2]);
        const tick = new THREE.Line(geometry, material);
        tick.renderOrder = 999;
        group.add(tick);
      }

      return group;
    }

    clearAnnotations() {
      if (this.annotations) {
        this.annotations.children.forEach(child => {
          if (child.geometry) child.geometry.dispose();
          if (child.material) {
            if (Array.isArray(child.material)) {
              child.material.forEach(m => m.dispose());
            } else {
              child.material.dispose();
            }
          }
        });
        this.annotations.clear();
      }
    }

    createPoint(name, coords) {
      const group = new THREE.Group();
      group.name = name;

      // Cục điểm nhỏ gọn để không che lấp các cạnh / ký hiệu
      const geometry = new THREE.SphereGeometry(0.04, 16, 16);
      const material = new THREE.MeshStandardMaterial({
        color: 0x3d52a0,
        metalness: 0.3,
        roughness: 0.7,
      });
      const sphere = new THREE.Mesh(geometry, material);
      sphere.position.set(coords[0], coords[1], coords[2]);
      group.add(sphere);

      const label = this.createLabel(name);
      label.position.set(coords[0], coords[1] + 0.15, coords[2]);
      group.add(label);

      group.visible = false;

      return group;
    }

    createEdge(start, end, name, style) {
      const points = [
        new THREE.Vector3(start[0], start[1], start[2]),
        new THREE.Vector3(end[0], end[1], end[2])
      ];

      const geometry = new THREE.BufferGeometry().setFromPoints(points);
      let line;

      if (style === 'dashed') {
        const material = new THREE.LineDashedMaterial({
          color: 0x2c3e50,
          linewidth: 1,
          dashSize: 0.1,
          gapSize: 0.05
        });
        line = new THREE.Line(geometry, material);
        line.computeLineDistances();
      } else {
        const material = new THREE.LineBasicMaterial({
          color: 0x3d52a0,
          linewidth: 2,
        });
        line = new THREE.Line(geometry, material);
      }

      line.name = name;
      line.visible = false;

      return line;
    }

    createFace(vertices) {
      // Fan triangulation cho polygon n đỉnh (xem drawFace để biết chi tiết).
      const positions = new Float32Array(vertices.length * 3);
      vertices.forEach((v, i) => {
        positions[i * 3]     = v[0];
        positions[i * 3 + 1] = v[1];
        positions[i * 3 + 2] = v[2];
      });
      const indices = [];
      for (let i = 1; i < vertices.length - 1; i++) {
        indices.push(0, i, i + 1);
      }
      const geometry = new THREE.BufferGeometry();
      geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
      geometry.setIndex(indices);
      geometry.computeVertexNormals();

      const material = new THREE.MeshStandardMaterial({
        color: 0x3d52a0,
        transparent: true,
        opacity: 0.15,
        side: THREE.DoubleSide,
        metalness: 0.1,
        roughness: 0.8,
      });
      const mesh = new THREE.Mesh(geometry, material);
      mesh.visible = false;

      return mesh;
    }

    createLabel(text) {
      const canvas = document.createElement('canvas');
      const context = canvas.getContext('2d');
      canvas.width = 128;
      canvas.height = 128;

      context.clearRect(0, 0, canvas.width, canvas.height);
      context.font = 'Bold 48px Arial';
      context.textAlign = 'center';
      context.textBaseline = 'middle';

      context.strokeStyle = 'rgba(255, 255, 255, 0.9)';
      context.lineWidth = 4;
      context.strokeText(text, 64, 64);

      context.fillStyle = '#3d52a0';
      context.fillText(text, 64, 64);

      const texture = new THREE.CanvasTexture(canvas);
      const material = new THREE.SpriteMaterial({
        map: texture,
        transparent: true,
        depthTest: false
      });
      const sprite = new THREE.Sprite(material);
      sprite.scale.set(0.3, 0.3, 1);

      return sprite;
    }

    goToStep(step) {
      if (!this.geometryData) return;

      this.currentStep = step;

      // Hide all objects and annotations
      this.objects.forEach(obj => obj.visible = false);
      if (this.annotations) {
        this.annotations.children.forEach(annotation => {
          annotation.visible = false;
        });
      }

      // Show objects up to current step (cumulative)
      for (let i = 0; i <= step; i++) {
        const currentStep = this.geometryData.steps[i];
        if (!currentStep) continue;
        currentStep.objects.forEach(objName => {
          const obj = this.objects.get(objName);
          if (obj) obj.visible = true;
        });
      }

      // Sau khi đã set visibility cho objects, mới đánh giá annotations.
      // Một annotation chỉ hiện khi mọi object liên quan đã visible.
      this.updateAnnotationsVisibility();
    }

    updateAnnotationsVisibility() {
      if (!this.annotations) return;

      const isPointVisible = (name) => {
        const obj = this.objects.get(name);
        return !!(obj && obj.visible);
      };
      const isEdgeVisible = (edgeName) => {
        // Edge object trực tiếp visible thì OK
        const obj = this.objects.get(edgeName);
        if (obj && obj.visible) return true;
        // Hoặc khi đoạn không tồn tại như edge object riêng (VD: M nằm trên CD,
        // ta chỉ tạo cạnh C-D, không có C-M / M-D), thì coi visible khi 2 endpoint
        // đều đã visible.
        const [a, b] = (edgeName || '').split('-');
        return isPointVisible(a) && isPointVisible(b);
      };

      this.annotations.children.forEach(annotation => {
        const ud = annotation.userData || {};
        switch (ud.annotationType) {
          case 'edge_label': {
            annotation.visible = isEdgeVisible(ud.relatedEdge);
            break;
          }
          case 'equal_segment': {
            // Tick gạch trung điểm: hiện khi 2 endpoint đoạn đã visible
            // (kể cả khi đoạn đó không tồn tại như edge object riêng)
            const [a, b] = (ud.relatedEdge || '').split('-');
            annotation.visible = isPointVisible(a) && isPointVisible(b);
            break;
          }
          case 'perpendicular':
          case 'angle': {
            const vertexOk = isPointVisible(ud.relatedVertex);
            const linesOk = (ud.relatedLines || []).every(isEdgeVisible);
            annotation.visible = vertexOk && linesOk;
            break;
          }
          default:
            annotation.visible = true;
        }
      });
    }

    showAnnotationsForObject(_objName) {
      // Giữ method để tương thích, delegate sang updateAnnotationsVisibility
      this.updateAnnotationsVisibility();
    }

    nextStep() {
      if (!this.geometryData) return;
      if (this.currentStep < this.geometryData.steps.length - 1) {
        this.goToStep(this.currentStep + 1);
      }
    }

    prevStep() {
      if (this.currentStep > 0) {
        this.goToStep(this.currentStep - 1);
      }
    }

    togglePlay(interval) {
      interval = interval || 2000;
      
      if (this.isPlaying) {
        this.pause();
      } else {
        this.play(interval);
      }
    }

    play(interval) {
      if (this.isPlaying) return;

      this.isPlaying = true;
      this.playInterval = setInterval(() => {
        if (this.geometryData && this.currentStep < this.geometryData.steps.length - 1) {
          this.nextStep();
        } else {
          this.pause();
        }
      }, interval);
    }

    pause() {
      if (!this.isPlaying) return;

      this.isPlaying = false;
      if (this.playInterval !== null) {
        clearInterval(this.playInterval);
        this.playInterval = null;
      }
    }

    fitCamera() {
      const bbox = new THREE.Box3();
      this.objects.forEach(obj => {
        if (obj.visible) bbox.expandByObject(obj);
      });

      if (bbox.isEmpty()) {
        this.camera.position.set(3, 3, 3);
        this.camera.lookAt(0, 0, 0);
        return;
      }

      const center = bbox.getCenter(new THREE.Vector3());
      const size = bbox.getSize(new THREE.Vector3());

      const maxDim = Math.max(size.x, size.y, size.z);
      const fov = this.camera.fov * (Math.PI / 180);
      let cameraZ = Math.abs(maxDim / 2 / Math.tan(fov / 2));
      cameraZ *= 1.8;

      this.camera.position.set(
        center.x + cameraZ,
        center.y + cameraZ,
        center.z + cameraZ
      );
      this.camera.lookAt(center);
      if (this.controls) {
        this.controls.target.copy(center);
        this.controls.update();
      }
    }

    setShowGrid(show) {
      if (this.grid) this.grid.visible = show;
    }

    setShowAxes(show) {
      if (this.axes) this.axes.visible = show;
    }

    resetCamera() {
      // Reset camera to default position
      if (this.camera && this.controls) {
        this.camera.position.set(3, 3, 3);
        this.camera.lookAt(0, 0, 0);
        this.controls.target.set(0, 0, 0);
        this.controls.update();
        console.log('✓ Camera reset to default position');
      }
    }

    focusOnGeometry() {
      // Auto-focus camera on the geometry
      this.fitCamera();
    }

    enableControls(enable) {
      if (this.controls) {
        this.controls.enabled = enable;
        console.log(enable ? '✓ Controls enabled' : '⚠️ Controls disabled');
      }
    }

    clearObjects() {
      this.objects.forEach(obj => {
        this.scene.remove(obj);
        if (obj instanceof THREE.Mesh || obj instanceof THREE.Line) {
          obj.geometry.dispose();
          if (Array.isArray(obj.material)) {
            obj.material.forEach(m => m.dispose());
          } else {
            obj.material.dispose();
          }
        }
      });
      this.objects.clear();
      
      // Also clear annotations
      this.clearAnnotations();
    }

    dispose() {
      this.pause();
      if (this.animationId !== null) {
        cancelAnimationFrame(this.animationId);
        this.animationId = null;
      }
      this.clearObjects();
      this.clearAnnotations();
      if (this.renderer) {
        this.renderer.dispose();
      }
      if (this.controls && this.controls.dispose) {
        this.controls.dispose();
      }
    }

    // ═══════════════════════════════════════════════════════════
    // PUBLIC DRAW API — Gemini gọi các hàm này theo thứ tự
    // Mỗi hàm tự add object vào scene và đăng ký vào this.objects
    // để goToStep / updateAnnotationsVisibility hoạt động đúng.
    // ═══════════════════════════════════════════════════════════

    /**
     * Tải mảng lệnh vẽ và execute đến lệnh thứ `untilStep` (mặc định: hết).
     * Dùng cho việc xem đầy đủ mô hình.
     */
    loadCommands(commands) {
      this.commandList = Array.isArray(commands) ? commands : [];
      this.clearObjects();
      this.executeCommands(this.commandList);
      // Phục vụ UI: số bước = số lệnh không phải setCamera
      this.totalCommandSteps = this.commandList.filter(c => {
        const fn = (c || {}).fn;
        return fn && fn !== 'setCamera';
      }).length;
    }

    /**
     * Hiện hình ở bước `idx` (1-based, tính theo lệnh vẽ thực sự).
     * Cách làm: clear scene, execute lại commandList[0..k] với k là index lệnh
     * tương ứng (bỏ qua setCamera khi đếm để ăn khớp với UI).
     */
    goToCommandStep(idx) {
      if (!this.commandList) return;
      this.clearObjects();

      let drawCount = 0;
      const upTo = [];
      for (const cmd of this.commandList) {
        const fn = (cmd || {}).fn;
        // setCamera không tính vào step số, nhưng vẫn push để giữ camera
        if (fn === 'setCamera') {
          upTo.push(cmd);
          continue;
        }
        // Đã đủ số lệnh vẽ → dừng (KHÔNG push lệnh hiện tại)
        if (drawCount >= idx) break;
        upTo.push(cmd);
        drawCount++;
      }
      this.executeCommands(upTo);
      this.currentStep = idx;
    }

    /**
     * Vẽ một điểm trong không gian 3D.
     * @param {string} name   - Tên điểm, VD: "A", "B'", "M"
     * @param {number} x
     * @param {number} y
     * @param {number} z
     * @param {object} [opts]
     * @param {string} [opts.color]   - Hex string, VD: "#3d52a0"
     * @param {number} [opts.radius]  - Bán kính cầu (default 0.04)
     */
    drawPoint(name, x, y, z, opts = {}) {
      // Xóa điểm cũ nếu đã tồn tại
      if (this.objects.has(name)) {
        const old = this.objects.get(name);
        this.scene.remove(old);
        this.objects.delete(name);
      }

      const group = new THREE.Group();
      group.name = name;

      const radius = opts.radius || 0.02;
      const color = opts.color ? new THREE.Color(opts.color) : new THREE.Color(0x3d52a0);

      const sphere = new THREE.Mesh(
        new THREE.SphereGeometry(radius, 16, 16),
        new THREE.MeshStandardMaterial({ color, metalness: 0.3, roughness: 0.7 })
      );
      sphere.position.set(x, y, z);
      group.add(sphere);

      const label = this.createLabel(name);
      label.position.set(x, y + 0.15, z);
      group.add(label);

      group.visible = true;
      this.scene.add(group);
      this.objects.set(name, group);
      return group;
    }

    /**
     * Vẽ cạnh nối 2 điểm đã có trong scene.
     * @param {string} fromName  - Tên điểm đầu (phải đã drawPoint trước)
     * @param {string} toName    - Tên điểm cuối
     * @param {object} [opts]
     * @param {string} [opts.style]   - "solid" | "dashed" (default "solid")
     * @param {string} [opts.color]   - Hex string
     * @param {string} [opts.label]   - Nhãn độ dài hiển thị giữa cạnh (VD: "a", "a√2")
     * @param {number} [opts.linewidth]
     */
    drawEdge(fromName, toName, opts = {}) {
      const edgeName = `${fromName}-${toName}`;

      // Lấy tọa độ từ điểm đã vẽ
      const fromGroup = this.objects.get(fromName);
      const toGroup   = this.objects.get(toName);
      if (!fromGroup || !toGroup) {
        console.warn(`drawEdge: điểm "${fromName}" hoặc "${toName}" chưa được drawPoint`);
        return null;
      }

      // Lấy vị trí từ sphere con (children[0])
      const fromPos = fromGroup.children[0].position;
      const toPos   = toGroup.children[0].position;

      const style = opts.style || 'solid';
      const hexColor = opts.color
        ? new THREE.Color(opts.color).getHex()
        : (style === 'dashed' ? 0x2c3e50 : 0x3d52a0);

      const pts = [
        new THREE.Vector3(fromPos.x, fromPos.y, fromPos.z),
        new THREE.Vector3(toPos.x,   toPos.y,   toPos.z),
      ];
      const geo = new THREE.BufferGeometry().setFromPoints(pts);

      let line;
      if (style === 'dashed') {
        const mat = new THREE.LineDashedMaterial({
          color: hexColor,
          linewidth: opts.linewidth || 1,
          dashSize: 0.1,
          gapSize: 0.05,
        });
        line = new THREE.Line(geo, mat);
        line.computeLineDistances();
      } else {
        const mat = new THREE.LineBasicMaterial({
          color: hexColor,
          linewidth: opts.linewidth || 2,
        });
        line = new THREE.Line(geo, mat);
      }

      line.name = edgeName;
      line.visible = true;
      this.scene.add(line);
      this.objects.set(edgeName, line);

      // Gắn nhãn độ dài nếu có
      if (opts.label) {
        const sprite = this.createEdgeLabel(
          [fromPos.x, fromPos.y, fromPos.z],
          [toPos.x,   toPos.y,   toPos.z],
          opts.label
        );
        sprite.visible = true;
        sprite.userData.annotationType = 'edge_label';
        sprite.userData.relatedEdge = edgeName;
        this.annotations.add(sprite);
      }

      return line;
    }

    /**
     * Vẽ mặt phẳng (polygon) từ danh sách tên điểm.
     * @param {string[]} pointNames  - VD: ["A","B","C","D"]
     * @param {object}   [opts]
     * @param {number}   [opts.opacity]  - 0..1 (default 0.15)
     * @param {string}   [opts.color]    - Hex string
     */
    drawFace(pointNames, opts = {}) {
      const faceId = 'face_' + pointNames.join('');
      const coords = pointNames.map(n => {
        const g = this.objects.get(n);
        if (!g) { console.warn(`drawFace: điểm "${n}" chưa được drawPoint`); return null; }
        return g.children[0].position;
      }).filter(Boolean);

      if (coords.length < 3) return null;

      const color = opts.color ? new THREE.Color(opts.color) : new THREE.Color(0x3d52a0);
      const opacity = opts.opacity !== undefined ? opts.opacity : 0.15;

      // Build vertex buffer (Float32Array)
      const vertices = new Float32Array(coords.length * 3);
      coords.forEach((p, i) => {
        vertices[i * 3]     = p.x;
        vertices[i * 3 + 1] = p.y;
        vertices[i * 3 + 2] = p.z;
      });

      // Fan triangulation: chia polygon n đỉnh thành (n-2) tam giác,
      // mỗi tam giác lấy đỉnh 0 + 2 đỉnh kề tiếp theo.
      // VD n=4 (ABCD): [0,1,2], [0,2,3]
      // VD n=5 (ABCDE): [0,1,2], [0,2,3], [0,3,4]
      // VD n=6 (lục giác): [0,1,2], [0,2,3], [0,3,4], [0,4,5]
      // Hoạt động đúng với polygon lồi (convex). Polygon lõm hiếm gặp trong
      // hình học không gian giáo trình nên có thể bỏ qua.
      const indices = [];
      for (let i = 1; i < coords.length - 1; i++) {
        indices.push(0, i, i + 1);
      }

      const geo = new THREE.BufferGeometry();
      geo.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
      geo.setIndex(indices);
      geo.computeVertexNormals();

      const mat = new THREE.MeshStandardMaterial({
        color,
        transparent: true,
        opacity,
        side: THREE.DoubleSide,
        metalness: 0.1,
        roughness: 0.8,
      });
      const mesh = new THREE.Mesh(geo, mat);
      mesh.name = faceId;
      mesh.visible = true;
      this.scene.add(mesh);
      this.objects.set(faceId, mesh);
      return mesh;
    }

    /**
     * Vẽ nhãn văn bản tự do tại một vị trí 3D.
     * @param {string} text
     * @param {number} x
     * @param {number} y
     * @param {number} z
     * @param {object} [opts]
     * @param {string} [opts.color]   - Hex string
     * @param {number} [opts.scale]   - Scale của sprite (default 0.4)
     */
    drawLabel(text, x, y, z, opts = {}) {
      const labelId = `label_${text}_${x}_${y}_${z}`;
      const sprite = this.createLabel(text);

      if (opts.color) {
        // Tạo lại label với màu tùy chỉnh
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = 256; canvas.height = 128;
        ctx.clearRect(0, 0, 256, 128);
        ctx.font = 'Bold 60px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.strokeStyle = 'rgba(255,255,255,0.9)';
        ctx.lineWidth = 6;
        ctx.strokeText(text, 128, 64);
        ctx.fillStyle = opts.color;
        ctx.fillText(text, 128, 64);
        const tex = new THREE.CanvasTexture(canvas);
        sprite.material.map = tex;
        sprite.material.needsUpdate = true;
      }

      const scale = opts.scale || 0.4;
      sprite.scale.set(scale, scale / 2, 1);
      sprite.position.set(x, y, z);
      sprite.visible = true;
      this.scene.add(sprite);
      this.objects.set(labelId, sprite);
      return sprite;
    }

    /**
     * Vẽ ký hiệu vuông góc (ô vuông nhỏ) tại một đỉnh giữa 2 cạnh.
     * @param {string} vertexName  - Tên đỉnh (phải đã drawPoint)
     * @param {string} edge1       - Cạnh 1, VD: "S-A"
     * @param {string} edge2       - Cạnh 2, VD: "A-B"
     */
    drawRightAngle(vertexName, edge1, edge2) {
      const pts = this._collectPoints();
      const symbol = this.createPerpendicularSymbol(vertexName, edge1, edge2, pts);
      if (!symbol) return null;

      const symId = `perp_${vertexName}_${edge1}_${edge2}`;
      symbol.visible = true;
      symbol.userData.annotationType = 'perpendicular';
      symbol.userData.relatedVertex = vertexName;
      symbol.userData.relatedLines = [edge1, edge2];
      this.annotations.add(symbol);
      return symbol;
    }

    /**
     * Vẽ dấu gạch tick trên cạnh để ký hiệu các đoạn bằng nhau.
     * @param {string} fromName
     * @param {string} toName
     * @param {string} [mark]  - "single" | "double" | "triple" (default "single")
     */
    drawEqualMark(fromName, toName, mark = 'single') {
      const fromGroup = this.objects.get(fromName);
      const toGroup   = this.objects.get(toName);
      if (!fromGroup || !toGroup) return null;

      const fp = fromGroup.children[0].position;
      const tp = toGroup.children[0].position;

      const tickGroup = this.createEqualSegmentMark(
        [fp.x, fp.y, fp.z],
        [tp.x, tp.y, tp.z],
        mark
      );
      const segId = `${fromName}-${toName}`;
      tickGroup.visible = true;
      tickGroup.userData.annotationType = 'equal_segment';
      tickGroup.userData.relatedEdge = segId;
      this.annotations.add(tickGroup);
      return tickGroup;
    }

    /**
     * Vẽ cung góc tại đỉnh giữa 2 cạnh, kèm nhãn giá trị góc.
     * @param {string} vertexName
     * @param {string} edge1
     * @param {string} edge2
     * @param {number|string} [value]  - Giá trị góc, VD: 90 hoặc "60°"
     */
    drawAngle(vertexName, edge1, edge2, value) {
      const pts = this._collectPoints();
      const symbol = this.createAngleSymbol(vertexName, edge1, edge2, value, pts);
      if (!symbol) return null;

      symbol.visible = true;
      symbol.userData.annotationType = 'angle';
      symbol.userData.relatedVertex = vertexName;
      symbol.userData.relatedLines = [edge1, edge2];
      this.annotations.add(symbol);
      return symbol;
    }

    /**
     * Đặt vị trí camera nhìn vào hình.
     * @param {number} x
     * @param {number} y
     * @param {number} z
     * @param {number} [lx] - lookAt x (default 0)
     * @param {number} [ly] - lookAt y (default 0)
     * @param {number} [lz] - lookAt z (default 0)
     */
    setCamera(x, y, z, lx = 0, ly = 0, lz = 0) {
      if (!this.camera) return;
      this.camera.position.set(x, y, z);
      this.camera.lookAt(lx, ly, lz);
      if (this.controls) {
        this.controls.target.set(lx, ly, lz);
        this.controls.update();
      }
    }

    /**
     * Thực thi một mảng lệnh vẽ do Gemini sinh ra.
     * Mỗi lệnh có dạng: { fn, args }
     * VD: { fn: "drawPoint", args: { name: "A", x: 0, y: 0, z: 0 } }
     *
     * Danh sách fn hợp lệ:
     *   drawPoint(name, x, y, z, opts?)
     *   drawEdge(from, to, opts?)
     *   drawFace(points[], opts?)
     *   drawLabel(text, x, y, z, opts?)
     *   drawRightAngle(vertex, edge1, edge2)
     *   drawEqualMark(from, to, mark?)
     *   drawAngle(vertex, edge1, edge2, value?)
     *   setCamera(x, y, z, lx?, ly?, lz?)
     *
     * Lưu ý: Metadata "không vẽ" (khoảng cách, góc giữa, ...) KHÔNG đi qua
     * executeCommands. Chúng đã có sẵn trong DULIEUHINHHOC từ bước upload và
     * được route /render-3d trả về ở field `metadata` riêng.
     *
     * @param {Array<{fn: string, args: object}>} commands
     */
    executeCommands(commands) {
      if (!Array.isArray(commands)) {
        console.error('executeCommands: commands phải là mảng');
        return;
      }

      const ALLOWED = new Set([
        'drawPoint', 'drawEdge', 'drawFace', 'drawLabel',
        'drawRightAngle', 'drawEqualMark', 'drawAngle', 'setCamera',
      ]);

      commands.forEach((cmd, i) => {
        const { fn, args } = cmd || {};
        if (!fn || !ALLOWED.has(fn)) {
          console.warn(`executeCommands[${i}]: hàm "${fn}" không hợp lệ, bỏ qua`);
          return;
        }
        try {
          const a = args || {};
          switch (fn) {
            case 'drawPoint':
              this.drawPoint(a.name, a.x, a.y, a.z, a.opts);
              break;
            case 'drawEdge':
              this.drawEdge(a.from, a.to, a.opts);
              break;
            case 'drawFace':
              this.drawFace(a.points, a.opts);
              break;
            case 'drawLabel':
              this.drawLabel(a.text, a.x, a.y, a.z, a.opts);
              break;
            case 'drawRightAngle':
              this.drawRightAngle(a.vertex, a.edge1, a.edge2);
              break;
            case 'drawEqualMark':
              this.drawEqualMark(a.from, a.to, a.mark);
              break;
            case 'drawAngle':
              this.drawAngle(a.vertex, a.edge1, a.edge2, a.value);
              break;
            case 'setCamera':
              this.setCamera(a.x, a.y, a.z, a.lx, a.ly, a.lz);
              break;
          }
        } catch (err) {
          console.error(`executeCommands[${i}] "${fn}" lỗi:`, err);
        }
      });

      // Sau khi vẽ xong, fit camera nếu chưa setCamera
      const hasSetCamera = commands.some(c => c && c.fn === 'setCamera');
      if (!hasSetCamera) this.fitCamera();
    }

    // ─── Helper nội bộ ───────────────────────────────────────────

    /** Thu thập tọa độ tất cả điểm hiện có dưới dạng { name: [x,y,z] } */
    _collectPoints() {
      const pts = {};
      this.objects.forEach((obj, key) => {
        // Điểm là Group có children[0] là Sphere
        if (obj instanceof THREE.Group && obj.children[0] instanceof THREE.Mesh) {
          const p = obj.children[0].position;
          pts[key] = [p.x, p.y, p.z];
        }
      });
      return pts;
    }
  }

  // Export to global scope
  window.ThreeViewerManager = ThreeViewerManager;
  
  console.log('ThreeViewerManager loaded');

})();
