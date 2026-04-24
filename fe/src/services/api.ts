import { GeometryData } from "../types/geometry";

export async function getGeometry(): Promise<GeometryData> {
  const res = await fetch("http://localhost:8000/solve");
  return res.json();
}
