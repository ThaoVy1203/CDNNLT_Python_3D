/**
 * ThreeCanvas - React wrapper cho Three.js
 */
import { useEffect, useRef } from 'react';
import { SceneManager } from '../../three/SceneManager';
import { useGeometryStore } from '../../store/geometryStore';

export default function ThreeCanvas() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const sceneManagerRef = useRef<SceneManager | null>(null);
  
  const geometryData = useGeometryStore(state => state.geometryData);
  const currentStep = useGeometryStore(state => state.currentStep);
  const showGrid = useGeometryStore(state => state.showGrid);
  const showAxes = useGeometryStore(state => state.showAxes);
  
  // Init Three.js scene (chỉ chạy 1 lần)
  useEffect(() => {
    if (!canvasRef.current) return;
    
    const sceneManager = new SceneManager(canvasRef.current);
    sceneManagerRef.current = sceneManager;
    
    sceneManager.startAnimation();
    
    return () => {
      sceneManager.dispose();
    };
  }, []);
  
  // Update geometry khi data thay đổi
  useEffect(() => {
    if (!sceneManagerRef.current || !geometryData) return;
    
    sceneManagerRef.current.updateGeometry(geometryData);
  }, [geometryData]);
  
  // Update step khi currentStep thay đổi
  useEffect(() => {
    if (!sceneManagerRef.current) return;
    
    sceneManagerRef.current.goToStep(currentStep);
  }, [currentStep]);
  
  // Update grid visibility
  useEffect(() => {
    if (!sceneManagerRef.current) return;
    
    sceneManagerRef.current.setShowGrid(showGrid);
  }, [showGrid]);
  
  // Update axes visibility
  useEffect(() => {
    if (!sceneManagerRef.current) return;
    
    sceneManagerRef.current.setShowAxes(showAxes);
  }, [showAxes]);
  
  return (
    <div className="three-canvas-container">
      <canvas ref={canvasRef} />
    </div>
  );
}
