/**
 * Annotation Adapter - Chuyển đổi annotations từ backend sang frontend format
 */
import { Annotations, EdgeAnnotation, PointAnnotation, PerpendicularAnnotation, AngleAnnotation, EqualAnnotation } from './types';

export class AnnotationAdapter {
  /**
   * Chuyển đổi annotations từ backend format sang frontend format
   */
  static adapt(backendAnnotations: any): Annotations {
    const frontendAnnotations: Annotations = {};
    
    // 1. Edges - Độ dài cạnh
    if (backendAnnotations.edges && Array.isArray(backendAnnotations.edges)) {
      frontendAnnotations.edges = backendAnnotations.edges.map((edge: any) => ({
        edge: edge.edge,
        label: edge.label,
        type: 'length' as const,
        style: edge.style || 'solid'
      }));
    }
    
    // 2. Points - Ghi chú điểm
    if (backendAnnotations.points && Array.isArray(backendAnnotations.points)) {
      frontendAnnotations.points = backendAnnotations.points.map((point: any) => ({
        point: point.point,
        label: point.label,
        type: this.getPointType(point.description),
        showCoordinates: false
      }));
    }
    
    // 3. Perpendicular - Ký hiệu vuông góc
    if (backendAnnotations.perpendicular && Array.isArray(backendAnnotations.perpendicular)) {
      frontendAnnotations.perpendicular = backendAnnotations.perpendicular.map((perp: any) => ({
        vertex: perp.vertex,
        line1: perp.line1,
        line2: perp.line2,
        showSquare: true
      }));
    }
    
    // 4. Angles - Ký hiệu góc
    if (backendAnnotations.angles && Array.isArray(backendAnnotations.angles)) {
      frontendAnnotations.angles = backendAnnotations.angles.map((angle: any) => ({
        vertex: angle.vertex,
        angle: angle.angle?.toString() || '90',
        symbol: angle.symbol || '∟',
        type: angle.angle === 90 ? 'right_angle' as const : 'angle' as const
      }));
    }
    
    // 5. Equal segments - Chuyển đổi từ segments array sang edge pairs
    if (backendAnnotations.equal_segments && Array.isArray(backendAnnotations.equal_segments)) {
      frontendAnnotations.equal = [];
      
      backendAnnotations.equal_segments.forEach((equalGroup: any) => {
        const segments = equalGroup.segments || [];
        const marks = this.getMarksCount(equalGroup.mark);
        
        // Tạo pairs từ segments
        // Ví dụ: ["A-B", "B-C", "C-D", "D-A"] → [(A-B, B-C), (B-C, C-D), (C-D, D-A)]
        for (let i = 0; i < segments.length - 1; i++) {
          frontendAnnotations.equal!.push({
            edge1: segments[i],
            edge2: segments[i + 1],
            marks: marks
          });
        }
      });
    }
    
    return frontendAnnotations;
  }
  
  private static getPointType(description?: string): 'midpoint' | 'special' | 'projection' | 'intersection' {
    if (!description) return 'special';
    
    const desc = description.toLowerCase();
    if (desc.includes('trung điểm') || desc.includes('midpoint')) return 'midpoint';
    if (desc.includes('hình chiếu') || desc.includes('projection')) return 'projection';
    if (desc.includes('giao điểm') || desc.includes('intersection') || desc.includes('tâm')) return 'intersection';
    
    return 'special';
  }
  
  private static getMarksCount(mark: string): number {
    if (mark === 'single') return 1;
    if (mark === 'double') return 2;
    if (mark === 'triple') return 3;
    return 1;
  }
}
