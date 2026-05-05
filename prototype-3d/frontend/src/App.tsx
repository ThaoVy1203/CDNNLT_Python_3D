/**
 * Main App Component
 */
import ThreeCanvas from './components/three/ThreeCanvas';
import ControlPanel from './components/ui/ControlPanel';
import './App.css';

export default function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>🧪 Prototype: Dựng hình 3D</h1>
        <p>React + Geometry Engine + Three.js</p>
      </header>
      
      <div className="app-content">
        <aside className="sidebar">
          <ControlPanel />
        </aside>
        
        <main className="canvas-area">
          <ThreeCanvas />
        </main>
      </div>
      
      <footer className="app-footer">
        <p>Backend: <a href="http://localhost:8001/docs" target="_blank">http://localhost:8001/docs</a></p>
      </footer>
    </div>
  );
}
