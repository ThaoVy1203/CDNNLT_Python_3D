import { Line } from "@react-three/drei";
import { GeometryData } from "../types/geometry";

export default function Pyramid({ points }: { points: GeometryData['points'] }) {
  const { A, B, C, S } = points;

  return (
    <>
      {/* Đáy tam giác ABC */}
      <Line points={[A, B]} color="white" lineWidth={2} />
      <Line points={[B, C]} color="white" lineWidth={2} />
      <Line points={[C, A]} color="white" lineWidth={2} />

      {/* Cạnh bên từ đỉnh S */}
      <Line points={[S, A]} color="yellow" lineWidth={2} />
      <Line points={[S, B]} color="yellow" lineWidth={2} />
      <Line points={[S, C]} color="yellow" lineWidth={2} />
    </>
  );
}
