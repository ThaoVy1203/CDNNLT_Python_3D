import ThreeScene from "./components/ThreeScene";
import { GeometryData } from "./types/geometry";

const mockData: GeometryData = {
  points: {
    A: [-2, 0, -2],
    B: [2, 0, -2],
    C: [0, 0, 2],
    S: [0, 3, 0],
  },
};

export default function App() {
  return <ThreeScene data={mockData} />;
}
