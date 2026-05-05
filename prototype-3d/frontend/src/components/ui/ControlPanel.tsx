/**
 * ControlPanel - Panel chứa các controls
 */
import DataInput from './DataInput';
import AnimationControls from './AnimationControls';
import { useGeometryStore } from '../../store/geometryStore';

export default function ControlPanel() {
  const showGrid = useGeometryStore(state => state.showGrid);
  const showAxes = useGeometryStore(state => state.showAxes);
  const toggleGrid = useGeometryStore(state => state.toggleGrid);
  const toggleAxes = useGeometryStore(state => state.toggleAxes);
  
  return (
    <div className="control-panel">
      <div className="panel-header">
        <h2>🎮 Controls</h2>
      </div>
      
      <div className="panel-section">
        <DataInput />
      </div>
      
      <div className="panel-section">
        <AnimationControls />
      </div>
      
      <div className="panel-section">
        <h3>Hiển thị</h3>
        <label className="checkbox-label">
          <input 
            type="checkbox"
            checked={showGrid}
            onChange={toggleGrid}
          />
          Hiện lưới (Grid)
        </label>
        
        <label className="checkbox-label">
          <input 
            type="checkbox"
            checked={showAxes}
            onChange={toggleAxes}
          />
          Hiện trục tọa độ (Axes)
        </label>
      </div>
      
      <div className="panel-footer">
        <p className="hint">
          💡 Dùng chuột để xoay, zoom hình 3D
        </p>
      </div>
    </div>
  );
}
