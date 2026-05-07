/**
 * TypeScript types cho geometry 3D rendering
 */

export interface Point3D {
  x: number;
  y: number;
  z: number;
}

export interface Edge {
  start: string;
  end: string;
  style?: 'solid' | 'dashed' | 'dotted';
  type?: 'main' | 'auxiliary' | 'height' | 'projection';
}

export interface Face {
  vertices: string[];
}

export interface Step {
  order: number;
  description: string;
  objects: string[];
  highlight?: string[];
  annotations?: Annotations;
}

export interface EdgeAnnotation {
  edge: string;
  label: string;
  type: 'length' | 'special';
  style?: 'solid' | 'dashed' | 'dotted';
}

export interface PointAnnotation {
  point: string;
  label: string;
  type: 'midpoint' | 'special' | 'projection' | 'intersection';
  showCoordinates?: boolean;
}

export interface PerpendicularAnnotation {
  vertex: string;
  line1: string;
  line2: string;
  showSquare?: boolean;
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
  name: string;
  color: string;
  length: number;
  showLabel?: boolean;
}

export interface DashedLineAnnotation {
  start: string;
  end: string;
  type: 'height' | 'projection' | 'auxiliary';
}

export interface Annotations {
  edges?: EdgeAnnotation[];
  points?: PointAnnotation[];
  perpendicular?: PerpendicularAnnotation[];
  angles?: AngleAnnotation[];
  parallel?: ParallelAnnotation[];
  equal?: EqualAnnotation[];
  arcs?: ArcAnnotation[];
  axes?: AxisAnnotation[];
  dashedLines?: DashedLineAnnotation[];
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
