/**
 * Geometry Builder - Build Three.js objects từ geometry data
 */
import * as THREE from 'three';
import { GeometryData, Step } from '../types/geometry';
import { MaterialLibrary } from './MaterialLibrary';

export class GeometryBuilder {
  private scene: THREE.Scene;
  private objects: Map<string, THREE.Object3D>;
  private materials: MaterialLibrary;
  private geometryData: GeometryData | null = null;
  
  constructor(scene: THREE.Scene) {
    this.scene = scene;
    this.objects = new Map();
    this.materials = new MaterialLibrary();
  }
  
  buildFromData(data: GeometryData) {
    this.clear();
    this.geometryData = data;
    
    // Build points
    Object.entries(data.points).forEach(([name, coords]) => {
      const point = this.createPoint(name, coords);
      this.objects.set(name, point);
      this.scene.add(point);
    });
    
    // Build edges với tên chuẩn hóa và style
    data.edges.forEach((edge, index) => {
      const edgeName = `${edge.start}-${edge.end}`;
      const line = this.createEdge(
        data.points[edge.start],
        data.points[edge.end],
        edgeName,
        edge.style || 'solid'  // Mặc định là solid
      );
      this.objects.set(edgeName, line);
      this.scene.add(line);
    });
    
    // Build faces (optional)
    data.faces.forEach((face, index) => {
      const mesh = this.createFace(face.vertices.map(v => data.points[v]));
      this.objects.set(`face_${index}`, mesh);
      this.scene.add(mesh);
    });
  }
  
  private createPoint(name: string, coords: [number, number, number]): THREE.Group {
    const group = new THREE.Group();
    group.name = name;
    
    // Sphere
    const geometry = new THREE.SphereGeometry(0.08, 16, 16);
    const material = this.materials.getPointMaterial();
    const sphere = new THREE.Mesh(geometry, material);
    sphere.position.set(coords[0], coords[1], coords[2]);
    group.add(sphere);
    
    // Label
    const label = this.createLabel(name);
    label.position.set(coords[0], coords[1] + 0.2, coords[2]);
    group.add(label);
    
    // Initially hidden
    group.visible = false;
    
    return group;
  }
  
  private createEdge(
    start: [number, number, number],
    end: [number, number, number],
    name: string,
    style: 'solid' | 'dashed' | 'dotted' = 'solid'
  ): THREE.Line {
    const points = [
      new THREE.Vector3(start[0], start[1], start[2]),
      new THREE.Vector3(end[0], end[1], end[2])
    ];
    
    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    let line: THREE.Line;
    
    if (style === 'dashed') {
      const material = new THREE.LineDashedMaterial({
        color: 0x2c3e50,
        linewidth: 1,
        dashSize: 0.1,
        gapSize: 0.05
      });
      line = new THREE.Line(geometry, material);
      line.computeLineDistances();
    } else if (style === 'dotted') {
      const material = new THREE.LineDashedMaterial({
        color: 0x2c3e50,
        linewidth: 1,
        dashSize: 0.02,
        gapSize: 0.08
      });
      line = new THREE.Line(geometry, material);
      line.computeLineDistances();
    } else {
      const material = this.materials.getEdgeMaterial() as THREE.LineBasicMaterial;
      line = new THREE.Line(geometry, material);
    }
    
    line.name = name;
    line.visible = false;
    
    return line;
  }
  
  private createFace(vertices: [number, number, number][]): THREE.Mesh {
    // Simple face - just for visualization
    const points = vertices.map(v => new THREE.Vector3(v[0], v[1], v[2]));
    
    // Create shape (simplified - assumes planar)
    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    const material = this.materials.getFaceMaterial();
    const mesh = new THREE.Mesh(geometry, material);
    
    // Initially hidden
    mesh.visible = false;
    
    return mesh;
  }
  
  private createLabel(text: string): THREE.Sprite {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d')!;
    canvas.width = 128;
    canvas.height = 128;
    
    // Nền trong suốt
    context.clearRect(0, 0, canvas.width, canvas.height);
    
    context.font = 'Bold 48px Arial';
    context.textAlign = 'center';
    context.textBaseline = 'middle';
    
    // Viền trắng
    context.strokeStyle = 'rgba(255, 255, 255, 0.9)';
    context.lineWidth = 4;
    context.strokeText(text, 64, 64);
    
    // Text chính
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
  
  showObjectsForStep(step: number) {
    if (!this.geometryData) return;
    
    // Hide all first
    this.objects.forEach(obj => obj.visible = false);
    
    // Show objects from ALL steps up to current step (cumulative)
    for (let i = 0; i <= step; i++) {
      const currentStep = this.geometryData.steps[i];
      if (!currentStep) continue;
      
      currentStep.objects.forEach(objName => {
        const obj = this.objects.get(objName);
        if (obj) {
          obj.visible = true;
        }
      });
    }
  }
  
  getBoundingBox(): THREE.Box3 {
    const bbox = new THREE.Box3();
    this.objects.forEach(obj => {
      if (obj.visible) bbox.expandByObject(obj);
    });
    return bbox;
  }
  
  clear() {
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
  }
  
  dispose() {
    this.clear();
    this.materials.dispose();
  }
}
