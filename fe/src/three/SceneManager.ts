/**
 * Scene Manager - Quản lý Three.js scene
 */
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { GeometryData } from './types';
import { GeometryBuilder } from './GeometryBuilder';
import { AnnotationRenderer } from './AnnotationRenderer';
import { AnnotationAdapter } from './AnnotationAdapter';

export class SceneManager {
  private scene: THREE.Scene;
  private camera: THREE.PerspectiveCamera;
  private renderer: THREE.WebGLRenderer;
  private controls: OrbitControls;
  private geometryBuilder: GeometryBuilder;
  private annotationRenderer: AnnotationRenderer;
  private geometryData: GeometryData | null = null;
  private grid: THREE.GridHelper | null = null;
  private axes: THREE.AxesHelper | null = null;
  private animationId: number | null = null;
  
  constructor(canvas: HTMLCanvasElement) {
    // Init scene
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0xf5f0e8);
    
    // Init camera
    this.camera = new THREE.PerspectiveCamera(
      50,
      canvas.clientWidth / canvas.clientHeight,
      0.1,
      1000
    );
    this.camera.position.set(3, 3, 3);
    this.camera.lookAt(0, 0, 0);
    
    // Init renderer
    this.renderer = new THREE.WebGLRenderer({
      canvas,
      antialias: true,
      alpha: true
    });
    this.renderer.setSize(canvas.clientWidth, canvas.clientHeight);
    this.renderer.setPixelRatio(window.devicePixelRatio);
    
    // Init lights
    this.initLights();
    
    // Init controls
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.05;
    this.controls.minDistance = 1;
    this.controls.maxDistance = 20;
    
    // Init geometry builder
    this.geometryBuilder = new GeometryBuilder(this.scene);
    
    // Init annotation renderer
    this.annotationRenderer = new AnnotationRenderer(this.scene);
    
    // Init helpers
    this.initHelpers();
    
    // Handle resize
    this.handleResize();
  }
  
  private initLights() {
    const ambient = new THREE.AmbientLight(0xffffff, 0.6);
    this.scene.add(ambient);
    
    const directional = new THREE.DirectionalLight(0xffffff, 0.8);
    directional.position.set(5, 10, 5);
    this.scene.add(directional);
  }
  
  private initHelpers() {
    // Grid
    this.grid = new THREE.GridHelper(10, 10, 0x8a7f6a, 0xb5ac98);
    this.scene.add(this.grid);
    
    // Axes
    this.axes = new THREE.AxesHelper(5);
    this.scene.add(this.axes);
  }
  
  updateGeometry(data: GeometryData) {
    this.geometryData = data;
    this.geometryBuilder.buildFromData(data);
    
    // Set points cho annotation renderer
    this.annotationRenderer.setPoints(data.points);
    
    // Render annotations nếu có
    if (data.annotations) {
      console.log('[SceneManager] Backend annotations:', data.annotations);
      
      // Chuyển đổi từ backend format sang frontend format
      const frontendAnnotations = AnnotationAdapter.adapt(data.annotations);
      console.log('[SceneManager] Frontend annotations:', frontendAnnotations);
      
      this.annotationRenderer.renderAnnotations(frontendAnnotations);
    }
    
    this.fitCamera();
  }
  
  goToStep(step: number) {
    if (!this.geometryData) return;
    
    // Hiển thị objects của step
    this.geometryBuilder.showObjectsForStep(step);
    
    // Hiển thị annotations tích lũy đến step hiện tại
    this.showAnnotationsUpToStep(step);
  }
  
  private showAnnotationsUpToStep(currentStep: number) {
    if (!this.geometryData) return;
    
    // Clear annotations hiện tại
    this.annotationRenderer.clear();
    
    // Tích lũy annotations từ tất cả các steps đến step hiện tại
    const cumulativeAnnotations: any = {
      edges: [],
      points: [],
      perpendicular: [],
      angles: []
    };
    
    // Duyệt qua tất cả steps từ 0 đến currentStep
    for (let i = 0; i <= currentStep; i++) {
      const step = this.geometryData.steps[i];
      if (!step || !step.annotations) continue;
      
      // Merge annotations
      if (step.annotations.edges) {
        cumulativeAnnotations.edges.push(...step.annotations.edges);
      }
      if (step.annotations.points) {
        cumulativeAnnotations.points.push(...step.annotations.points);
      }
      if (step.annotations.perpendicular) {
        cumulativeAnnotations.perpendicular.push(...step.annotations.perpendicular);
      }
      if (step.annotations.angles) {
        cumulativeAnnotations.angles.push(...step.annotations.angles);
      }
    }
    
    // Render tất cả annotations tích lũy
    if (Object.values(cumulativeAnnotations).some((arr: any) => arr.length > 0)) {
      this.annotationRenderer.renderAnnotations(cumulativeAnnotations);
    }
  }
  
  fitCamera() {
    const bbox = this.geometryBuilder.getBoundingBox();
    
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
    cameraZ *= 1.8; // Zoom out thêm
    
    this.camera.position.set(
      center.x + cameraZ,
      center.y + cameraZ,
      center.z + cameraZ
    );
    this.camera.lookAt(center);
    this.controls.target.copy(center);
    this.controls.update();
  }
  
  startAnimation() {
    const animate = () => {
      this.animationId = requestAnimationFrame(animate);
      this.controls.update();
      this.renderer.render(this.scene, this.camera);
    };
    animate();
  }
  
  stopAnimation() {
    if (this.animationId !== null) {
      cancelAnimationFrame(this.animationId);
      this.animationId = null;
    }
  }
  
  setShowGrid(show: boolean) {
    if (this.grid) this.grid.visible = show;
  }
  
  setShowAxes(show: boolean) {
    if (this.axes) this.axes.visible = show;
  }
  
  private handleResize() {
    window.addEventListener('resize', () => {
      const canvas = this.renderer.domElement;
      const width = canvas.clientWidth;
      const height = canvas.clientHeight;
      
      this.camera.aspect = width / height;
      this.camera.updateProjectionMatrix();
      this.renderer.setSize(width, height);
    });
  }
  
  dispose() {
    this.stopAnimation();
    this.renderer.dispose();
    this.controls.dispose();
    this.geometryBuilder.dispose();
    this.annotationRenderer.dispose();
    
    if (this.grid) this.scene.remove(this.grid);
    if (this.axes) this.scene.remove(this.axes);
  }
}
