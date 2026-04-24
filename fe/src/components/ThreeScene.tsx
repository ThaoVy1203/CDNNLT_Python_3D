import { Canvas } from "@react-three/fiber";
import { OrbitControls, Grid } from "@react-three/drei";
import Pyramid from "./Pyramid";
import { GeometryData } from "../types/geometry";

export default function ThreeScene({ data }: { data: GeometryData }) {
  return (
    <Canvas style={{ height: "100vh" }} camera={{ position: [5, 5, 5] }}>
      <ambientLight intensity={0.5} />
      <directionalLight position={[5, 5, 5]} intensity={1} />
      <Pyramid points={data.points} />
      <Grid args={[10, 10]} />
      <OrbitControls />
    </Canvas>
  );
}
