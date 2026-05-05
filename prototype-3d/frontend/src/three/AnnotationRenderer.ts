/**
 * Annotation Renderer - Render ký hiệu hình học
 */
import * as THREE from 'three';
import {
  Annotations,
  AngleAnnotation,
  ParallelAnnotation,
  EqualAnnotation,
  ArcAnnotation,
  AxisAnnotation,
  DashedLineAnnotation,
  EdgeAnnotation,
  PointAnnotation,
  PerpendicularAnnotation
} from '../types/geometry';

export class AnnotationRenderer {
  private scene: THREE.Scene;
  private annotations: THREE.Group;
  private points: Record<string, [number, number, number]>;
  
  constructor(scene: THREE.Scene) {
    this.scene = scene;
    this.annotations = new THREE.Group();
    this.annotations.name = 'annotations';
    this.scene.add(this.annotations);
    this.points = {};
  }
  
  setPoints(points: Record<string, [number, number, number]>) {
    this.points = points;
  }
  
  renderAnnotations(data: Annotations) {
    this.clear();
    
    // Render axes (trục tọa độ)
    if (data.axes) {
      data.axes.forEach(annotation => {
        this.renderAxis(annotation);
      });
    }
    
    // Render dashed lines (đường đứt nét)
    if (data.dashedLines) {
      data.dashedLines.forEach(annotation => {
        this.renderDashedLine(annotation);
      });
    }
    
    // Render edge labels (độ dài cạnh)
    if (data.edges) {
      data.edges.forEach(annotation => {
        this.renderEdgeLabel(annotation);
      });
    }
    
    // Render point labels (trung điểm, điểm đặc biệt)
    if (data.points) {
      data.points.forEach(annotation => {
        this.renderPointLabel(annotation);
      });
    }
    
    // Render perpendicular symbols
    if (data.perpendicular) {
      data.perpendicular.forEach(annotation => {
        this.renderPerpendicularSymbol(annotation);
      });
    }
    
    // Render angle symbols
    if (data.angles) {
      data.angles.forEach(annotation => {
        this.renderAngleSymbol(annotation);
      });
    }
    
    // Render parallel symbols
    if (data.parallel) {
      data.parallel.forEach(annotation => {
        this.renderParallelSymbol(annotation);
      });
    }
    
    // Render equal marks
    if (data.equal) {
      data.equal.forEach(annotation => {
        this.renderEqualMark(annotation);
      });
    }
    
    // Render arc symbols (for angles)
    if (data.arcs) {
      data.arcs.forEach(annotation => {
        this.renderArcSymbol(annotation);
      });
    }
  }
  
  private renderEdgeLabel(annotation: EdgeAnnotation) {
    const [start, end] = annotation.edge.split('-');
    const startPos = this.points[start];
    const endPos = this.points[end];
    
    if (!startPos || !endPos) return;
    
    // Tính vị trí giữa cạnh
    const midPoint = new THREE.Vector3(
      (startPos[0] + endPos[0]) / 2,
      (startPos[1] + endPos[1]) / 2,
      (startPos[2] + endPos[2]) / 2
    );
    
    // Offset một chút để không trùng với cạnh
    midPoint.y += 0.15;
    
    const sprite = this.createTextSprite(annotation.label, '#a07840', 0.25);
    sprite.position.copy(midPoint);
    this.annotations.add(sprite);
  }
  
  private renderPointLabel(annotation: PointAnnotation) {
    const pos = this.points[annotation.point];
    if (!pos) return;
    
    const position = new THREE.Vector3(pos[0], pos[1], pos[2]);
    
    // Tạo label với tọa độ nếu cần
    let label = annotation.label;
    if (annotation.showCoordinates) {
      // Format: C(z=a√3)
      label = `${annotation.point}(${annotation.label})`;
    }
    
    position.y -= 0.25; // Đặt label phía dưới điểm
    
    const sprite = this.createTextSprite(label, '#2a7a62', 0.2);
    sprite.position.copy(position);
    this.annotations.add(sprite);
  }
  
  private renderPerpendicularSymbol(annotation: PerpendicularAnnotation) {
    // Lấy vertex (điểm giao của 2 cạnh vuông góc)
    const vertexPos = this.points[annotation.vertex];
    if (!vertexPos) return;
    
    const vertex = new THREE.Vector3(...vertexPos);
    
    // Lấy 2 cạnh vuông góc
    const [start1, end1] = annotation.line1.split('-');
    const [start2, end2] = annotation.line2.split('-');
    
    const start1Pos = this.points[start1];
    const end1Pos = this.points[end1];
    const start2Pos = this.points[start2];
    const end2Pos = this.points[end2];
    
    if (!start1Pos || !end1Pos || !start2Pos || !end2Pos) return;
    
    // Tính vector hướng của 2 cạnh (từ vertex ra ngoài)
    const dir1 = new THREE.Vector3(...end1Pos).sub(new THREE.Vector3(...start1Pos)).normalize();
    const dir2 = new THREE.Vector3(...end2Pos).sub(new THREE.Vector3(...start2Pos)).normalize();
    
    // Vẽ hình vuông nhỏ tại vertex
    if (annotation.showSquare !== false) {
      this.drawRightAngleSquare(vertex, dir1, dir2);
    }
  }
  
  private renderAxis(annotation: AxisAnnotation) {
    const origin = new THREE.Vector3(0, 0, 0);
    let direction = new THREE.Vector3();
    
    switch (annotation.name.toUpperCase()) {
      case 'X':
        direction.set(1, 0, 0);
        break;
      case 'Y':
        direction.set(0, 1, 0);
        break;
      case 'Z':
        direction.set(0, 0, 1);
        break;
    }
    
    const end = origin.clone().add(direction.multiplyScalar(annotation.length));
    
    // Vẽ trục
    const points = [origin, end];
    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    const material = new THREE.LineBasicMaterial({ 
      color: new THREE.Color(annotation.color),
      linewidth: 2
    });
    const line = new THREE.Line(geometry, material);
    this.annotations.add(line);
    
    // Vẽ mũi tên
    const arrowDir = direction.clone().normalize();
    const arrowLength = 0.2;
    const arrowHelper = new THREE.ArrowHelper(
      arrowDir,
      end.clone().add(arrowDir.clone().multiplyScalar(-arrowLength)),
      arrowLength,
      new THREE.Color(annotation.color),
      0.1,
      0.1
    );
    this.annotations.add(arrowHelper);
    
    // Label trục
    if (annotation.showLabel !== false) {
      const labelPos = end.clone().add(direction.clone().multiplyScalar(0.2));
      const sprite = this.createTextSprite(annotation.name, annotation.color, 0.3);
      sprite.position.copy(labelPos);
      this.annotations.add(sprite);
    }
  }
  
  private renderDashedLine(annotation: DashedLineAnnotation) {
    const startPos = this.points[annotation.start];
    const endPos = this.points[annotation.end];
    
    if (!startPos || !endPos) return;
    
    const start = new THREE.Vector3(...startPos);
    const end = new THREE.Vector3(...endPos);
    
    const points = [start, end];
    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    
    // Màu theo loại
    let color = 0x666666;
    if (annotation.type === 'height') color = 0x00aa00;
    else if (annotation.type === 'projection') color = 0x0066cc;
    
    const material = new THREE.LineDashedMaterial({
      color: color,
      linewidth: 1,
      dashSize: 0.1,
      gapSize: 0.05
    });
    
    const line = new THREE.Line(geometry, material);
    line.computeLineDistances();  // Cần thiết cho dashed line
    this.annotations.add(line);
  }
  
  private createTextSprite(text: string, color: string, scale: number): THREE.Sprite {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d')!;
    canvas.width = 256;
    canvas.height = 128;
    
    // Nền trong suốt
    context.clearRect(0, 0, canvas.width, canvas.height);
    
    // Text với viền để dễ đọc
    context.font = 'Bold 36px Arial';
    context.textAlign = 'center';
    context.textBaseline = 'middle';
    
    // Vẽ viền trắng cho text (để dễ đọc trên nền bất kỳ)
    context.strokeStyle = 'rgba(255, 255, 255, 0.9)';
    context.lineWidth = 4;
    context.strokeText(text, canvas.width / 2, canvas.height / 2);
    
    // Vẽ text chính
    context.fillStyle = color;
    context.fillText(text, canvas.width / 2, canvas.height / 2);
    
    const texture = new THREE.CanvasTexture(canvas);
    const material = new THREE.SpriteMaterial({ 
      map: texture,
      transparent: true,
      depthTest: false  // Luôn hiển thị phía trước
    });
    const sprite = new THREE.Sprite(material);
    sprite.scale.set(scale * 2, scale, 1);
    
    return sprite;
  }
  
  private drawRightAngleSquare(vertex: THREE.Vector3, dir1: THREE.Vector3, dir2: THREE.Vector3) {
    const size = 0.15;  // Kích thước hình vuông
    
    // Vẽ hình vuông từ vertex theo 2 hướng vuông góc
    const points = [
      vertex.clone(),
      vertex.clone().add(dir1.clone().multiplyScalar(size)),
      vertex.clone().add(dir1.clone().multiplyScalar(size)).add(dir2.clone().multiplyScalar(size)),
      vertex.clone().add(dir2.clone().multiplyScalar(size)),
      vertex.clone()
    ];
    
    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    const material = new THREE.LineBasicMaterial({ 
      color: 0xd62828,  // Màu đỏ cho ký hiệu vuông góc
      linewidth: 2 
    });
    const line = new THREE.Line(geometry, material);
    this.annotations.add(line);
  }
  
  private renderAngleSymbol(annotation: AngleAnnotation) {
    const pos = this.points[annotation.vertex];
    if (!pos) return;
    
    const position = new THREE.Vector3(pos[0], pos[1], pos[2]);
    position.x += 0.2;
    position.y += 0.1;
    
    const label = annotation.symbol || annotation.angle;
    const color = annotation.type === 'right_angle' ? '#d62828' : '#f77f00';
    
    const sprite = this.createTextSprite(label, color, 0.25);
    sprite.position.copy(position);
    this.annotations.add(sprite);
  }
  
  private renderParallelSymbol(annotation: ParallelAnnotation) {
    const [start1, end1] = annotation.line1.split('-');
    const [start2, end2] = annotation.line2.split('-');
    
    const start1Pos = this.points[start1];
    const end1Pos = this.points[end1];
    const start2Pos = this.points[start2];
    const end2Pos = this.points[end2];
    
    if (!start1Pos || !end1Pos || !start2Pos || !end2Pos) return;
    
    this.drawParallelMarks(start1Pos, end1Pos, annotation.marks || 1);
    this.drawParallelMarks(start2Pos, end2Pos, annotation.marks || 1);
    
    const mid1 = new THREE.Vector3(
      (start1Pos[0] + end1Pos[0]) / 2,
      (start1Pos[1] + end1Pos[1]) / 2,
      (start1Pos[2] + end1Pos[2]) / 2
    );
    
    const sprite = this.createTextSprite(annotation.symbol, '#7209b7', 0.2);
    sprite.position.copy(mid1);
    sprite.position.y += 0.2;
    this.annotations.add(sprite);
  }
  
  private drawParallelMarks(start: [number, number, number], end: [number, number, number], marks: number) {
    const startVec = new THREE.Vector3(...start);
    const endVec = new THREE.Vector3(...end);
    const mid = new THREE.Vector3().addVectors(startVec, endVec).multiplyScalar(0.5);
    const direction = new THREE.Vector3().subVectors(endVec, startVec).normalize();
    const perpDir = new THREE.Vector3(-direction.z, 0, direction.x).normalize();
    
    const markLength = 0.08;
    const spacing = 0.05;
    
    for (let i = 0; i < marks; i++) {
      const offset = (i - (marks - 1) / 2) * spacing;
      const markStart = mid.clone().add(direction.clone().multiplyScalar(offset)).add(perpDir.clone().multiplyScalar(-markLength / 2));
      const markEnd = mid.clone().add(direction.clone().multiplyScalar(offset)).add(perpDir.clone().multiplyScalar(markLength / 2));
      
      const geometry = new THREE.BufferGeometry().setFromPoints([markStart, markEnd]);
      const material = new THREE.LineBasicMaterial({ color: 0x7209b7, linewidth: 2 });
      const line = new THREE.Line(geometry, material);
      this.annotations.add(line);
    }
  }
  
  private renderEqualMark(annotation: EqualAnnotation) {
    const [start1, end1] = annotation.edge1.split('-');
    const [start2, end2] = annotation.edge2.split('-');
    
    const start1Pos = this.points[start1];
    const end1Pos = this.points[end1];
    const start2Pos = this.points[start2];
    const end2Pos = this.points[end2];
    
    if (!start1Pos || !end1Pos || !start2Pos || !end2Pos) return;
    
    this.drawEqualMarks(start1Pos, end1Pos, annotation.marks || 1);
    this.drawEqualMarks(start2Pos, end2Pos, annotation.marks || 1);
  }
  
  private drawEqualMarks(start: [number, number, number], end: [number, number, number], marks: number) {
    const startVec = new THREE.Vector3(...start);
    const endVec = new THREE.Vector3(...end);
    const mid = new THREE.Vector3().addVectors(startVec, endVec).multiplyScalar(0.5);
    const direction = new THREE.Vector3().subVectors(endVec, startVec).normalize();
    const perpDir = new THREE.Vector3(-direction.z, direction.y, direction.x).normalize();
    
    const markLength = 0.06;
    const spacing = 0.04;
    
    for (let i = 0; i < marks; i++) {
      const offset = (i - (marks - 1) / 2) * spacing;
      const markStart = mid.clone().add(direction.clone().multiplyScalar(offset)).add(perpDir.clone().multiplyScalar(-markLength / 2));
      const markEnd = mid.clone().add(direction.clone().multiplyScalar(offset)).add(perpDir.clone().multiplyScalar(markLength / 2));
      
      const geometry = new THREE.BufferGeometry().setFromPoints([markStart, markEnd]);
      const material = new THREE.LineBasicMaterial({ color: 0x06a77d, linewidth: 2 });
      const line = new THREE.Line(geometry, material);
      this.annotations.add(line);
    }
  }
  
  private renderArcSymbol(annotation: ArcAnnotation) {
    const vertexPos = this.points[annotation.vertex];
    const point1Pos = this.points[annotation.point1];
    const point2Pos = this.points[annotation.point2];
    
    if (!vertexPos || !point1Pos || !point2Pos) return;
    
    const vertex = new THREE.Vector3(...vertexPos);
    const p1 = new THREE.Vector3(...point1Pos);
    const p2 = new THREE.Vector3(...point2Pos);
    
    const dir1 = new THREE.Vector3().subVectors(p1, vertex).normalize();
    const dir2 = new THREE.Vector3().subVectors(p2, vertex).normalize();
    
    const radius = annotation.radius || 0.15;
    const segments = 20;
    const angle = Math.acos(dir1.dot(dir2));
    
    const points: THREE.Vector3[] = [];
    for (let i = 0; i <= segments; i++) {
      const t = i / segments;
      const currentAngle = t * angle;
      
      const axis = new THREE.Vector3().crossVectors(dir1, dir2).normalize();
      const rotatedDir = dir1.clone().applyAxisAngle(axis, currentAngle);
      
      points.push(vertex.clone().add(rotatedDir.multiplyScalar(radius)));
    }
    
    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    const material = new THREE.LineBasicMaterial({ color: 0xf77f00, linewidth: 2 });
    const arc = new THREE.Line(geometry, material);
    this.annotations.add(arc);
    
    if (annotation.label) {
      const midDir = new THREE.Vector3().addVectors(dir1, dir2).normalize();
      const labelPos = vertex.clone().add(midDir.multiplyScalar(radius + 0.15));
      
      const sprite = this.createTextSprite(annotation.label, '#f77f00', 0.2);
      sprite.position.copy(labelPos);
      this.annotations.add(sprite);
    }
  }
  
  clear() {
    while (this.annotations.children.length > 0) {
      const child = this.annotations.children[0];
      this.annotations.remove(child);
      
      if (child instanceof THREE.Sprite) {
        child.material.map?.dispose();
        child.material.dispose();
      }
    }
  }
  
  setVisible(visible: boolean) {
    this.annotations.visible = visible;
  }
  
  dispose() {
    this.clear();
    this.scene.remove(this.annotations);
  }
}
