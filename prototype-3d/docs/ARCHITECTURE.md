# 🏗️ KIẾN TRÚC HỆ THỐNG

## Tổng quan 3 lớp

```
┌─────────────────────────────────────────────────────────┐
│  LAYER 1: REACT (UI & State Management)                │
│  - Components: Pages, Panels, Controls                 │
│  - State: Zustand store                                │
│  - Routing: React Router (optional)                    │
└────────────────┬────────────────────────────────────────┘
                 │ HTTP API
┌────────────────▼────────────────────────────────────────┐
│  LAYER 2: GEOMETRY ENGINE (Backend - Python)           │
│  - SymPy: Giải hệ phương trình ràng buộc               │
│  - Constraint Solver: Tính tọa độ chính xác            │
│  - Steps Generator: Tạo thứ tự dựng hình               │
└────────────────┬────────────────────────────────────────┘
                 │ JSON Response
┌────────────────▼────────────────────────────────────────┐
│  LAYER 3: THREE.JS RENDERER (Frontend - Vanilla)       │
│  - SceneManager: Quản lý scene                         │
│  - GeometryBuilder: Build objects từ data              │
│  - AnimationController: Animation logic                │
└─────────────────────────────────────────────────────────┘
```

## Data Flow

```
User input (mock data hoặc JSON file)
  ↓
Backend API: /api/solve
  ↓
SymPy Solver tính toán
  ↓
JSON Response:
{
  "points": { "A": [0,0,0], "B": [1,0,0], ... },
  "edges": [{ "start": "A", "end": "B" }, ...],
  "faces": [{ "vertices": ["A","B","C"] }, ...],
  "steps": [
    { "order": 1, "description": "...", "objects": [...] }
  ]
}
  ↓
React state (Zustand)
  ↓
ThreeCanvas component
  ↓
SceneManager.updateGeometry()
  ↓
GeometryBuilder.buildFromData()
  ↓
Three.js render
```

## Component Hierarchy (Frontend)

```
<App>
  └── <PrototypePage>
      ├── <ControlPanel>
      │   ├── <DataInput>         # Upload JSON hoặc select mock
      │   └── <AnimationControls> # Play/Pause/Step controls
      │
      └── <ThreeCanvas>           # React wrapper
          └── SceneManager        # Vanilla Three.js
              ├── Scene
              ├── Camera
              ├── Renderer
              ├── Lights
              ├── Controls (OrbitControls)
              └── GeometryBuilder
                  ├── Points
                  ├── Edges
                  └── Faces
```

## Backend Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI app
│   ├── api/
│   │   └── routes.py           # API endpoints
│   ├── solver/
│   │   ├── sympy_solver.py     # SymPy constraint solver
│   │   ├── steps_generator.py  # Generate construction steps
│   │   └── geometry_types.py   # Shape definitions
│   └── models/
│       └── schemas.py          # Pydantic models
├── tests/
│   └── test_solver.py          # Unit tests
├── mock_data/
│   ├── pyramid.json            # Mock data hình chóp
│   ├── prism.json              # Mock data lăng trụ
│   └── cube.json               # Mock data hình lập phương
└── requirements.txt
```

## Frontend Structure

```
frontend/
├── src/
│   ├── App.tsx
│   ├── main.tsx
│   ├── pages/
│   │   └── PrototypePage.tsx
│   ├── components/
│   │   ├── ui/
│   │   │   ├── ControlPanel.tsx
│   │   │   ├── DataInput.tsx
│   │   │   └── AnimationControls.tsx
│   │   └── three/
│   │       ├── ThreeCanvas.tsx      # React wrapper
│   │       └── useThreeScene.ts     # Custom hook
│   ├── three/                       # Vanilla Three.js
│   │   ├── SceneManager.ts
│   │   ├── GeometryBuilder.ts
│   │   ├── AnimationController.ts
│   │   └── MaterialLibrary.ts
│   ├── store/
│   │   └── geometryStore.ts         # Zustand store
│   ├── services/
│   │   └── api.ts                   # API client
│   └── types/
│       └── geometry.ts              # TypeScript types
├── public/
│   └── mock-data/                   # Mock JSON files
├── package.json
├── tsconfig.json
└── vite.config.ts
```

## API Endpoints

### POST /api/solve
**Input**:
```json
{
  "shape_type": "pyramid",
  "constraints": {
    "base": { "type": "square", "side": 1 },
    "apex": { "height": 1.414, "perpendicular": true }
  }
}
```

**Output**:
```json
{
  "points": { "A": [0,0,0], "B": [1,0,0], ... },
  "edges": [...],
  "faces": [...],
  "steps": [...]
}
```

## State Management (Zustand)

```typescript
interface GeometryStore {
  // Data
  geometryData: GeometryData | null;
  
  // Animation
  currentStep: number;
  isPlaying: boolean;
  
  // Actions
  setGeometryData: (data: GeometryData) => void;
  play: () => void;
  pause: () => void;
  nextStep: () => void;
  prevStep: () => void;
}
```

## Three.js Classes

### SceneManager
- Quản lý scene, camera, renderer
- Init lights, controls
- Animation loop
- Public methods: updateGeometry(), goToStep(), fitCamera()

### GeometryBuilder
- Build Three.js objects từ JSON data
- Methods: createPoint(), createEdge(), createFace()
- Quản lý visibility theo step
- Tính bounding box

### AnimationController
- Quản lý timeline
- Methods: play(), pause(), nextStep(), prevStep()
- Trigger callbacks khi step thay đổi

## Testing Strategy

### Backend
- Unit tests cho SymPy solver
- Test với 10 bài toán mẫu
- Verify tọa độ output

### Frontend
- Visual testing (manual)
- Test với mock data
- Test animation flow

## Performance Considerations

- Dùng `useMemo` cho expensive calculations
- Three.js object pooling nếu cần
- Debounce resize events
- Lazy load mock data
