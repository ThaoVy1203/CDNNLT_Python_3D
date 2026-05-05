/**
 * Material Library - Quản lý materials cho Three.js
 */
import * as THREE from 'three';

export class MaterialLibrary {
  private materials: Map<string, THREE.Material>;
  
  constructor() {
    this.materials = new Map();
    this.initMaterials();
  }
  
  private initMaterials() {
    // Point material
    this.materials.set('point', new THREE.MeshStandardMaterial({
      color: 0x3d52a0,
      metalness: 0.3,
      roughness: 0.7,
    }));
    
    this.materials.set('point-highlight', new THREE.MeshStandardMaterial({
      color: 0xa07840,
      metalness: 0.3,
      roughness: 0.7,
      emissive: 0xa07840,
      emissiveIntensity: 0.3,
    }));
    
    // Edge material
    this.materials.set('edge', new THREE.LineBasicMaterial({
      color: 0x0000ff,
      linewidth: 2,
    }));
    
    this.materials.set('edge-highlight', new THREE.LineBasicMaterial({
      color: 0xa07840,
      linewidth: 3,
    }));
    
    // Face material
    this.materials.set('face', new THREE.MeshStandardMaterial({
      color: 0x00ff00,
      transparent: true,
      opacity: 0.3,
      side: THREE.DoubleSide,
      metalness: 0.1,
      roughness: 0.8,
    }));
  }
  
  getPointMaterial(highlighted: boolean = false): THREE.Material {
    return highlighted 
      ? this.materials.get('point-highlight')!.clone()
      : this.materials.get('point')!.clone();
  }
  
  getEdgeMaterial(highlighted: boolean = false): THREE.Material {
    return highlighted
      ? this.materials.get('edge-highlight')!.clone()
      : this.materials.get('edge')!.clone();
  }
  
  getFaceMaterial(): THREE.Material {
    return this.materials.get('face')!.clone();
  }
  
  dispose() {
    this.materials.forEach(material => material.dispose());
    this.materials.clear();
  }
}
