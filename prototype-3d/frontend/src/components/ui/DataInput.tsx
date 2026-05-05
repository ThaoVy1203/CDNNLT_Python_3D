/**
 * DataInput - Component để chọn đề bài
 */
import { useState } from 'react';
import { apiService } from '../../services/api';
import { useGeometryStore } from '../../store/geometryStore';

// Đề bài mẫu
const PROBLEMS = [
  {
    id: 'pyramid-1',
    title: 'Bài 1: Hình chóp S.ABCD',
    description: 'Cho hình chóp S.ABCD có đáy ABCD là hình vuông cạnh a. SA vuông góc với mặt phẳng đáy và SA = a√2.',
    shapeType: 'pyramid',
  },
  {
    id: 'pyramid-special',
    title: 'Bài 2: Hình chóp S.ABCD với trung điểm M',
    description: 'Cho hình chóp S.ABCD có đáy ABCD là hình vuông cạnh a, cạnh bên SA vuông góc với mặt phẳng đáy. Gọi M là trung điểm của CD. Biết khoảng cách giữa hai đường thẳng BC và SM bằng a√3/4. Tính thể tích của khối chóp đã cho theo a.',
    shapeType: 'pyramid',
    hasSpecialPoints: true,
  },
  {
    id: 'prism-1',
    title: 'Bài 3: Lăng trụ tam giác ABC.A\'B\'C\'',
    description: 'Cho lăng trụ đứng ABC.A\'B\'C\' có đáy ABC là tam giác đều cạnh a và chiều cao h = a.',
    shapeType: 'prism',
  },
  {
    id: 'cube-1',
    title: 'Bài 4: Hình lập phương ABCD.A\'B\'C\'D\'',
    description: 'Cho hình lập phương ABCD.A\'B\'C\'D\' có cạnh bằng a.',
    shapeType: 'cube',
  },
];

export default function DataInput() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedProblem, setSelectedProblem] = useState(PROBLEMS[0].id);
  
  const setGeometryData = useGeometryStore(state => state.setGeometryData);
  
    const handleLoad = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const problem = PROBLEMS.find(p => p.id === selectedProblem);
      if (!problem) throw new Error('Không tìm thấy đề bài');
      
      // Nếu là bài có điểm đặc biệt, thêm flag
      const shapeType = problem.hasSpecialPoints 
        ? `${problem.shapeType}-special`
        : problem.shapeType;
      
      const data = await apiService.getMockData(shapeType);
      setGeometryData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load data');
      console.error('Load error:', err);
    } finally {
      setLoading(false);
    }
  };
  
  const selectedProblemData = PROBLEMS.find(p => p.id === selectedProblem);
  
  return (
    <div className="data-input">
      <h3>Chọn đề bài</h3>
      
      <div className="problem-selector">
        {PROBLEMS.map((problem) => (
          <label key={problem.id} className="problem-option">
            <input
              type="radio"
              value={problem.id}
              checked={selectedProblem === problem.id}
              onChange={(e) => setSelectedProblem(e.target.value)}
            />
            <div className="problem-content">
              <div className="problem-title">{problem.title}</div>
              <div className="problem-description">{problem.description}</div>
            </div>
          </label>
        ))}
      </div>
      
      {selectedProblemData && (
        <div className="problem-preview">
          <strong>Đề bài đã chọn:</strong>
          <p>{selectedProblemData.description}</p>
        </div>
      )}
      
      <button 
        className="btn-load"
        onClick={handleLoad}
        disabled={loading}
      >
        {loading ? 'Đang dựng hình...' : '🎨 Dựng hình 3D'}
      </button>
      
      {error && (
        <div className="error-message">
          ❌ {error}
        </div>
      )}
    </div>
  );
}
