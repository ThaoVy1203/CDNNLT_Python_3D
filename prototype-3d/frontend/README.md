# ⚛️ Frontend - React + Three.js

## Mục đích
Frontend render hình học 3D động từ dữ liệu backend, sử dụng React + vanilla Three.js.

## Cài đặt

```bash
cd frontend
npm install
```

## Chạy dev server

```bash
npm run dev
```

App chạy tại: http://localhost:5173

## Build production

```bash
npm run build
```

## Cấu trúc

```
frontend/
├── src/
│   ├── App.tsx
│   ├── main.tsx
│   ├── pages/
│   │   └── PrototypePage.tsx
│   ├── components/
│   │   ├── ui/                    # React UI components
│   │   │   ├── ControlPanel.tsx
│   │   │   ├── DataInput.tsx
│   │   │   └── AnimationControls.tsx
│   │   └── three/                 # React wrappers
│   │       ├── ThreeCanvas.tsx
│   │       └── useThreeScene.ts
│   ├── three/                     # Vanilla Three.js
│   │   ├── SceneManager.ts
│   │   ├── GeometryBuilder.ts
│   │   ├── AnimationController.ts
│   │   └── MaterialLibrary.ts
│   ├── store/
│   │   └── geometryStore.ts       # Zustand state
│   ├── services/
│   │   └── api.ts                 # API client
│   └── types/
│       └── geometry.ts            # TypeScript types
├── public/
│   └── mock-data/                 # Mock JSON files
├── package.json
├── tsconfig.json
└── vite.config.ts
```

## Tech Stack

- **React 18**: UI framework
- **TypeScript**: Type safety
- **Three.js**: 3D rendering (vanilla, không dùng R3F)
- **Zustand**: State management
- **Vite**: Build tool

## Kiến trúc

### React Layer
- Quản lý UI, state, data flow
- Components: Pages, Panels, Controls
- State: Zustand store

### Three.js Layer
- Vanilla Three.js (imperative)
- SceneManager: Quản lý scene, camera, renderer
- GeometryBuilder: Build objects từ JSON data
- AnimationController: Animation logic

### Communication
- React → Three.js: Qua props và refs
- Three.js → React: Qua callbacks

## Development

### Thêm component mới
1. Tạo file trong `src/components/ui/`
2. Import vào parent component
3. Update types nếu cần

### Thêm Three.js class mới
1. Tạo file trong `src/three/`
2. Export class
3. Import vào SceneManager hoặc GeometryBuilder

### Update state
1. Sửa `src/store/geometryStore.ts`
2. Thêm state và actions
3. Use trong components

## Testing

- Visual testing (manual)
- Test với mock data trong `public/mock-data/`
- Test animation flow

## Mock Data

Đặt file JSON trong `public/mock-data/`:
- `pyramid.json`
- `prism.json`
- `cube.json`

Format:
```json
{
  "points": { "A": [0,0,0], ... },
  "edges": [...],
  "faces": [...],
  "steps": [...]
}
```

## Troubleshooting

### Three.js không render
- Check canvas ref
- Check SceneManager initialization
- Check browser console

### Animation không hoạt động
- Check AnimationController
- Check Zustand store state
- Check step filtering logic

### Performance issues
- Reduce geometry complexity
- Use object pooling
- Check animation loop
