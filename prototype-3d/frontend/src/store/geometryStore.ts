/**
 * Zustand Store - Quản lý state
 */
import { create } from 'zustand';
import { GeometryData } from '../types/geometry';

interface GeometryStore {
  // Data
  geometryData: GeometryData | null;
  
  // Animation state
  currentStep: number;
  isPlaying: boolean;
  playbackSpeed: number;
  
  // UI state
  showLabels: boolean;
  showGrid: boolean;
  showAxes: boolean;
  
  // Actions
  setGeometryData: (data: GeometryData) => void;
  setCurrentStep: (step: number) => void;
  play: () => void;
  pause: () => void;
  nextStep: () => void;
  prevStep: () => void;
  reset: () => void;
  toggleLabels: () => void;
  toggleGrid: () => void;
  toggleAxes: () => void;
}

let playInterval: NodeJS.Timeout | null = null;

export const useGeometryStore = create<GeometryStore>((set, get) => ({
  // Initial state
  geometryData: null,
  currentStep: 0,
  isPlaying: false,
  playbackSpeed: 1,
  showLabels: true,
  showGrid: true,
  showAxes: true,
  
  // Actions
  setGeometryData: (data) => set({ 
    geometryData: data,
    currentStep: 0,
    isPlaying: false
  }),
  
  setCurrentStep: (step) => {
    const { geometryData } = get();
    if (!geometryData) return;
    
    const maxStep = geometryData.steps.length - 1;
    const clampedStep = Math.max(0, Math.min(step, maxStep));
    set({ currentStep: clampedStep });
  },
  
  play: () => {
    const { geometryData, playbackSpeed } = get();
    if (!geometryData) return;
    
    set({ isPlaying: true });
    
    if (playInterval) clearInterval(playInterval);
    
    playInterval = setInterval(() => {
      const { currentStep, geometryData } = get();
      if (!geometryData) return;
      
      if (currentStep >= geometryData.steps.length - 1) {
        get().pause();
        return;
      }
      
      set({ currentStep: currentStep + 1 });
    }, 1500 / playbackSpeed);
  },
  
  pause: () => {
    set({ isPlaying: false });
    if (playInterval) {
      clearInterval(playInterval);
      playInterval = null;
    }
  },
  
  nextStep: () => {
    const { currentStep, geometryData } = get();
    if (!geometryData) return;
    
    const maxStep = geometryData.steps.length - 1;
    if (currentStep < maxStep) {
      set({ currentStep: currentStep + 1 });
    }
  },
  
  prevStep: () => {
    const { currentStep } = get();
    if (currentStep > 0) {
      set({ currentStep: currentStep - 1 });
    }
  },
  
  reset: () => {
    get().pause();
    set({ currentStep: 0 });
  },
  
  toggleLabels: () => set((state) => ({ showLabels: !state.showLabels })),
  toggleGrid: () => set((state) => ({ showGrid: !state.showGrid })),
  toggleAxes: () => set((state) => ({ showAxes: !state.showAxes })),
}));
