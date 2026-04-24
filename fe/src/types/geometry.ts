export type Point3D = [number, number, number];

export interface GeometryData {
  points: {
    A: Point3D;
    B: Point3D;
    C: Point3D;
    S: Point3D;
  };
}
