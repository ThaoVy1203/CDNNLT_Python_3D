/**
 * AnimationControls - Controls cho animation
 */
import { useGeometryStore } from '../../store/geometryStore';

export default function AnimationControls() {
  const geometryData = useGeometryStore(state => state.geometryData);
  const currentStep = useGeometryStore(state => state.currentStep);
  const isPlaying = useGeometryStore(state => state.isPlaying);
  
  const play = useGeometryStore(state => state.play);
  const pause = useGeometryStore(state => state.pause);
  const nextStep = useGeometryStore(state => state.nextStep);
  const prevStep = useGeometryStore(state => state.prevStep);
  const reset = useGeometryStore(state => state.reset);
  
  if (!geometryData) return null;
  
  const totalSteps = geometryData.steps.length;
  const currentStepData = geometryData.steps[currentStep];
  
  return (
    <div className="animation-controls">
      <h3>Animation Controls</h3>
      
      {/* Step info */}
      <div className="step-info">
        <div className="step-number">
          Bước {currentStep + 1} / {totalSteps}
        </div>
        <div className="step-description">
          {currentStepData?.description}
        </div>
      </div>
      
      {/* Progress bar */}
      <div className="progress-bar">
        <div 
          className="progress-fill"
          style={{ width: `${((currentStep + 1) / totalSteps) * 100}%` }}
        />
      </div>
      
      {/* Control buttons */}
      <div className="control-buttons">
        <button 
          className="btn-control"
          onClick={reset}
          title="Restart"
        >
          ⏮
        </button>
        
        <button 
          className="btn-control"
          onClick={prevStep}
          disabled={currentStep === 0}
          title="Previous"
        >
          ⏪
        </button>
        
        <button 
          className="btn-control btn-play"
          onClick={isPlaying ? pause : play}
          title={isPlaying ? 'Pause' : 'Play'}
        >
          {isPlaying ? '⏸' : '▶'}
        </button>
        
        <button 
          className="btn-control"
          onClick={nextStep}
          disabled={currentStep === totalSteps - 1}
          title="Next"
        >
          ⏩
        </button>
        
        <button 
          className="btn-control"
          onClick={() => useGeometryStore.getState().setCurrentStep(totalSteps - 1)}
          title="End"
        >
          ⏭
        </button>
      </div>
      
      {/* Steps list */}
      <div className="steps-list">
        <h4>Các bước dựng hình:</h4>
        {geometryData.steps.map((step, index) => (
          <div 
            key={index}
            className={`step-item ${index === currentStep ? 'active' : ''} ${index < currentStep ? 'done' : ''}`}
            onClick={() => useGeometryStore.getState().setCurrentStep(index)}
          >
            <div className="step-num">
              {index < currentStep ? '✓' : index + 1}
            </div>
            <div className="step-text">
              {step.description}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
