/**
 * Three Viewer - Main class để tích hợp vào solver.html
 */
import { SceneManager } from './SceneManager';
import { GeometryData } from './types';

export class ThreeViewer {
  private sceneManager: SceneManager | null = null;
  private canvas: HTMLCanvasElement | null = null;
  private currentStep: number = 0;
  private isPlaying: boolean = false;
  private playInterval: number | null = null;
  
  /**
   * Khởi tạo Three.js viewer
   * @param canvasId ID của canvas element
   */
  init(canvasId: string) {
    this.canvas = document.getElementById(canvasId) as HTMLCanvasElement;
    
    if (!this.canvas) {
      console.error(`Canvas with id "${canvasId}" not found`);
      return;
    }
    
    // Tạo scene manager
    this.sceneManager = new SceneManager(this.canvas);
    this.sceneManager.startAnimation();
    
    console.log('Three.js viewer initialized');
  }
  
  /**
   * Load geometry data từ API
   * @param data Geometry data từ backend
   */
  loadGeometry(data: GeometryData) {
    if (!this.sceneManager) {
      console.error('Scene manager not initialized');
      return;
    }
    
    this.sceneManager.updateGeometry(data);
    this.currentStep = 0;
    this.sceneManager.goToStep(0);
    
    console.log('Geometry loaded:', data);
  }
  
  /**
   * Chuyển đến step cụ thể
   * @param step Step number (0-based)
   */
  goToStep(step: number) {
    if (!this.sceneManager) return;
    
    this.currentStep = step;
    this.sceneManager.goToStep(step);
  }
  
  /**
   * Chuyển đến step tiếp theo
   */
  nextStep() {
    this.goToStep(this.currentStep + 1);
  }
  
  /**
   * Chuyển đến step trước đó
   */
  prevStep() {
    if (this.currentStep > 0) {
      this.goToStep(this.currentStep - 1);
    }
  }
  
  /**
   * Play animation tự động
   * @param interval Thời gian giữa các step (ms)
   */
  play(interval: number = 2000) {
    if (this.isPlaying) return;
    
    this.isPlaying = true;
    this.playInterval = window.setInterval(() => {
      this.nextStep();
    }, interval);
  }
  
  /**
   * Pause animation
   */
  pause() {
    if (!this.isPlaying) return;
    
    this.isPlaying = false;
    if (this.playInterval !== null) {
      clearInterval(this.playInterval);
      this.playInterval = null;
    }
  }
  
  /**
   * Toggle play/pause
   */
  togglePlay(interval: number = 2000) {
    if (this.isPlaying) {
      this.pause();
    } else {
      this.play(interval);
    }
  }
  
  /**
   * Hiển thị/ẩn grid
   */
  setShowGrid(show: boolean) {
    if (!this.sceneManager) return;
    this.sceneManager.setShowGrid(show);
  }
  
  /**
   * Hiển thị/ẩn axes
   */
  setShowAxes(show: boolean) {
    if (!this.sceneManager) return;
    this.sceneManager.setShowAxes(show);
  }
  
  /**
   * Lấy step hiện tại
   */
  getCurrentStep(): number {
    return this.currentStep;
  }
  
  /**
   * Kiểm tra đang play hay không
   */
  getIsPlaying(): boolean {
    return this.isPlaying;
  }
  
  /**
   * Cleanup
   */
  dispose() {
    this.pause();
    if (this.sceneManager) {
      this.sceneManager.dispose();
      this.sceneManager = null;
    }
  }
}

// Export singleton instance
export const threeViewer = new ThreeViewer();
