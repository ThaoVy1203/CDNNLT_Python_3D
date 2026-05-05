/**
 * TypeScript types cho geometry data
 */

export interface Point3D {
  x: number;
  y: number;
  z: number;
}

export interface Edge {
  start: string;
  end: string;
  style?: 'solid' | 'dashed' | 'dotted';  // Kiểu đường: liền, đứt, chấm
  type?: 'main' | 'auxiliary' | 'height' | 'projection';  // Loại cạnh
}

export interface Face {
  vertices: string[];
}

export interface Step {
  order: number;
  description: string;
  objects: string[];
  highlight?: string[];
  annotations?: Annotations;  // Annotations cho step này
}

export interface EdgeAnnotation {
  edge: string;
  label: string;
  type: 'length' | 'special';
  style?: 'solid' | 'dashed' | 'dotted';  // Kiểu đường: liền, đứt, chấm
}

export interface PointAnnotation {
  point: string;
  label: string;
  type: 'midpoint' | 'special' | 'projection' | 'intersection';
  showCoordinates?: boolean;  // Hiển thị tọa độ như C(z=a√3)
}

export interface PerpendicularAnnotation {
  vertex: string;        // Điểm giao của 2 cạnh vuông góc
  line1: string;         // Cạnh thứ nhất
  line2: string;         // Cạnh thứ hai (vuông góc với line1)
  showSquare?: boolean;  // Hiển thị hình vuông nhỏ tại góc vuông
}

export interface AngleAnnotation {
  vertex: string;
  angle: string;
  symbol?: string;
  type: 'right_angle' | 'angle';
}

export interface ParallelAnnotation {
  line1: string;
  line2: string;
  symbol: string;
  marks?: number;
}

export interface EqualAnnotation {
  edge1: string;
  edge2: string;
  marks?: number;
}

export interface ArcAnnotation {
  vertex: string;
  point1: string;
  point2: string;
  label?: string;
  radius?: number;
}

export interface AxisAnnotation {
  name: string;  // 'X', 'Y', 'Z'
  color: string;  // Màu trục
  length: number;
  showLabel?: boolean;
}

export interface DashedLineAnnotation {
  start: string;
  end: string;
  type: 'height' | 'projection' | 'auxiliary';  // Đường cao, hình chiếu, phụ
}

export interface Annotations {
  edges?: EdgeAnnotation[];
  points?: PointAnnotation[];
  perpendicular?: PerpendicularAnnotation[];
  angles?: AngleAnnotation[];
  parallel?: ParallelAnnotation[];
  equal?: EqualAnnotation[];
  arcs?: ArcAnnotation[];
  axes?: AxisAnnotation[];  // Trục tọa độ
  dashedLines?: DashedLineAnnotation[];  // Đường đứt nét
}

export interface GeometryData {
  points: Record<string, [number, number, number]>;
  edges: Edge[];
  faces: Face[];
  steps: Step[];
  annotations?: Annotations;
  camera?: {
    position: [number, number, number];
    lookAt: [number, number, number];
  };
}

export interface SolveRequest {
  shape_type: string;
  constraints: Record<string, any>;
  description?: string;  // Mô tả đề bài để parse annotations
}
