/**
 * API Service - Gọi backend API
 */
import { GeometryData, SolveRequest } from '../types/geometry';

const API_BASE_URL = 'http://localhost:8001/api';

export const apiService = {
  /**
   * Giải bài toán hình học
   */
  async solve(request: SolveRequest): Promise<GeometryData> {
    const response = await fetch(`${API_BASE_URL}/solve`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }
    
    return response.json();
  },
  
  /**
   * Lấy mock data
   */
  async getMockData(shapeType: string): Promise<GeometryData> {
    const response = await fetch(`${API_BASE_URL}/mock/${shapeType}`);
    
    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }
    
    return response.json();
  },
};
