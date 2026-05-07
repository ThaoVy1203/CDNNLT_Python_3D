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
            const perpSymbol = this.createPerpendicularSymbol(
              points[vertex],
              line1,
              line2,
              points
            );
            if (perpSymbol) {
              perpSymbol.visible = false; // Hidden by default
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
            const angleSymbol = this.createAngleSymbol(
              points[vertex],
              line1,
              line2,
              value,
              points
            );
            if (angleSymbol) {
              angleSymbol.visible = false; // Hidden by default
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
      canvas.width = 256;
      canvas.height = 128;
      
      // Clear canvas (transparent background)
      context.clearRect(0, 0, canvas.width, canvas.height);
      
      // Set font
      context.font = 'Bold 36px Arial';
      context.textAlign = 'center';
      context.textBaseline = 'middle';
      
      // Add white outline for better visibility
      context.strokeStyle = 'rgba(255, 255, 255, 0.8)';
      context.lineWidth = 6;
      context.strokeText(text, 128, 64);
      
      // Text in gold color
      context.fillStyle = '#a07840'; // Gold color
      context.fillText(text, 128, 64);
      
      const texture = new THREE.CanvasTexture(canvas);
      const material = new THREE.SpriteMaterial({
        map: texture,
        transparent: true,
        depthTest: false
      });
      const sprite = new THREE.Sprite(material);
      sprite.position.set(midpoint[0], midpoint[1] + 0.15, midpoint[2]);
      sprite.scale.set(0.4, 0.2, 1);
      sprite.visible = false; // Hidden by default, will show in steps
      
      // Store edge name for step-by-step display
      sprite.userData.edgeName = start + '-' + end;
      
      return sprite;
    }

    createPerpendicularSymbol(vertex, line1, line2, points) {
      // Create small square symbol at vertex
      const size = 0.1;
      
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
      // Create tick marks on edge to show equal segments
      const midpoint = new THREE.Vector3(
        (start[0] + end[0]) / 2,
        (start[1] + end[1]) / 2,
        (start[2] + end[2]) / 2
      );
      
      // Direction perpendicular to edge
      const edgeDir = new THREE.Vector3(
        end[0] - start[0],
        end[1] - start[1],
        end[2] - start[2]
      ).normalize();
      
      // Get perpendicular direction (simplified)
      const perpDir = new THREE.Vector3(-edgeDir.y, edgeDir.x, 0).normalize();
      
      const tickSize = 0.08;
      const tickSpacing = 0.04;
      const numTicks = markType === 'single' ? 1 : markType === 'double' ? 2 : 3;
      
      const group = new THREE.Group();
      
      for (let i = 0; i < numTicks; i++) {
        const offset = (i - (numTicks - 1) / 2) * tickSpacing;
        const tickCenter = midpoint.clone().add(edgeDir.clone().multiplyScalar(offset));
        
        const p1 = tickCenter.clone().add(perpDir.clone().multiplyScalar(tickSize / 2));
        const p2 = tickCenter.clone().add(perpDir.clone().multiplyScalar(-tickSize / 2));
        
        const geometry = new THREE.BufferGeometry().setFromPoints([p1, p2]);
        const material = new THREE.LineBasicMaterial({
          color: 0x3d52a0,
          linewidth: 2
        });
        
        const tick = new THREE.Line(geometry, material);
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

      const geometry = new THREE.SphereGeometry(0.08, 16, 16);
      const material = new THREE.MeshStandardMaterial({
        color: 0x3d52a0,
        metalness: 0.3,
        roughness: 0.7,
      });
      const sphere = new THREE.Mesh(geometry, material);
      sphere.position.set(coords[0], coords[1], coords[2]);
      group.add(sphere);

      const label = this.createLabel(name);
      label.position.set(coords[0], coords[1] + 0.2, coords[2]);
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
      const points = vertices.map(v => new THREE.Vector3(v[0], v[1], v[2]));
      const geometry = new THREE.BufferGeometry().setFromPoints(points);
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

      // Show objects and annotations up to current step (cumulative)
      for (let i = 0; i <= step; i++) {
        const currentStep = this.geometryData.steps[i];
        if (!currentStep) continue;

        // Show geometry objects
        currentStep.objects.forEach(objName => {
          const obj = this.objects.get(objName);
          if (obj) {
            obj.visible = true;
            
            // Also show related annotations for this object
            this.showAnnotationsForObject(objName);
          }
        });
      }
    }

    showAnnotationsForObject(objName) {
      if (!this.annotations) return;
      
      // Show annotations related to this object
      this.annotations.children.forEach(annotation => {
        const userData = annotation.userData;
        
        // Show edge labels when edge is visible
        if (userData.annotationType === 'edge_label') {
          if (userData.relatedEdge === objName) {
            annotation.visible = true;
          }
        }
        
        // Show perpendicular symbols when vertex is visible
        if (userData.annotationType === 'perpendicular') {
          if (objName === userData.relatedVertex) {
            annotation.visible = true;
          }
          // Also show when related lines are visible
          if (userData.relatedLines) {
            const allLinesVisible = userData.relatedLines.every(line => {
              return this.objects.get(line)?.visible;
            });
            if (allLinesVisible) {
              annotation.visible = true;
            }
          }
        }
        
        // Show angle symbols when vertex is visible
        if (userData.annotationType === 'angle') {
          if (objName === userData.relatedVertex) {
            annotation.visible = true;
          }
          // Also show when related lines are visible
          if (userData.relatedLines) {
            const allLinesVisible = userData.relatedLines.every(line => {
              return this.objects.get(line)?.visible;
            });
            if (allLinesVisible) {
              annotation.visible = true;
            }
          }
        }
        
        // Show equal segment marks when edge is visible
        if (userData.annotationType === 'equal_segment') {
          if (userData.relatedEdge === objName) {
            annotation.visible = true;
          }
        }
      });
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
  }

  // Export to global scope
  window.ThreeViewerManager = ThreeViewerManager;
  
  console.log('ThreeViewerManager loaded');

})();
