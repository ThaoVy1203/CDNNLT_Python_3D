# Cập nhật: Annotations Theo Từng Bước Dựng Hình

## Tổng quan

Hệ thống giờ đây hiển thị **ký hiệu hình học theo từng bước** trong quá trình dựng hình, thay vì hiển thị tất cả cùng lúc.

## Thay đổi chính

### 1. Backend - Steps Generator

**File:** `backend/app/solver/steps_generator.py`

#### Thêm method `distribute_annotations()`
```python
def distribute_annotations(steps, all_annotations):
    """Phân bổ annotations vào từng step dựa trên objects"""
    for step in steps:
        step_objects = set(step["objects"])
        step_annotations = {}
        
        # Chỉ thêm annotations cho objects trong step này
        for edge_ann in all_annotations["edges"]:
            if edge_ann["edge"] in step_objects:
                step_annotations["edges"].append(edge_ann)
        
        # Tương tự cho points, perpendicular, angles
        
        if step_annotations:
            step["annotations"] = step_annotations
```

#### Cập nhật `generate_pyramid_steps()`
- Thêm parameter `annotations` từ geometry_data
- Gọi `distribute_annotations()` trước khi return
- Điều chỉnh steps để SA xuất hiện ở bước 2 (cùng với đỉnh S)

**Trước:**
```python
Bước 1: Vẽ đáy ABCD
Bước 2: Dựng đỉnh S
Bước 3: Nối các cạnh bên (SA, SB, SC, SD)
```

**Sau:**
```python
Bước 1: Vẽ đáy ABCD → annotations: độ dài cạnh đáy
Bước 2: Dựng S và SA → annotations: độ dài SA, ký hiệu ⊥
Bước 3: Nối cạnh bên còn lại → annotations: (nếu có)
Bước 4: Điểm M → annotations: label trung điểm
Bước 5: Nối SM → annotations: (nếu có)
```

### 2. Frontend - Types

**File:** `frontend/src/types/geometry.ts`

#### Thêm `annotations` vào Step interface
```typescript
export interface Step {
  order: number;
  description: string;
  objects: string[];
  highlight?: string[];
  annotations?: Annotations;  // ← MỚI
}
```

### 3. Frontend - Scene Manager

**File:** `frontend/src/three/SceneManager.ts`

#### Thêm properties
```typescript
private annotationRenderer: AnnotationRenderer;
private geometryData: GeometryData | null = null;
```

#### Cập nhật `goToStep()`
```typescript
goToStep(step: number) {
  // Hiển thị objects
  this.geometryBuilder.showObjectsForStep(step);
  
  // Hiển thị annotations tích lũy
  this.showAnnotationsUpToStep(step);
}
```

#### Thêm method `showAnnotationsUpToStep()`
```typescript
private showAnnotationsUpToStep(currentStep: number) {
  // Clear annotations hiện tại
  this.annotationRenderer.clear();
  
  // Tích lũy annotations từ step 0 đến currentStep
  const cumulative = { edges: [], points: [], perpendicular: [], angles: [] };
  
  for (let i = 0; i <= currentStep; i++) {
    const step = this.geometryData.steps[i];
    if (step?.annotations) {
      cumulative.edges.push(...step.annotations.edges || []);
      cumulative.points.push(...step.annotations.points || []);
      cumulative.perpendicular.push(...step.annotations.perpendicular || []);
      cumulative.angles.push(...step.annotations.angles || []);
    }
  }
  
  // Render tất cả annotations tích lũy
  this.annotationRenderer.renderAnnotations(cumulative);
}
```

## Luồng hoạt động

### 1. Backend parse đề bài
```
Đề bài: "AB = 3, BC = 4, SA = 6, SA ⊥ đáy, M là trung điểm AB"
    ↓
sympy_solver.parse_annotations_from_description()
    ↓
Annotations: {
  edges: [{edge: "A-B", label: "3"}, {edge: "B-C", label: "4"}, ...],
  points: [{point: "M", label: "trung điểm AB"}],
  perpendicular: [{line: "S-A", symbol: "⊥"}],
  angles: [{vertex: "B", symbol: "∟"}]
}
```

### 2. Steps Generator phân bổ annotations
```
Step 1: objects = ["A", "B", "C", "A-B", "B-C", "C-A"]
    ↓
distribute_annotations() → Tìm annotations cho A-B, B-C, C-A, B
    ↓
Step 1 annotations: {
  edges: [{edge: "A-B", label: "3"}, {edge: "B-C", label: "4"}],
  angles: [{vertex: "B", symbol: "∟"}]
}

Step 2: objects = ["S", "S-A"]
    ↓
distribute_annotations() → Tìm annotations cho S-A
    ↓
Step 2 annotations: {
  edges: [{edge: "S-A", label: "6"}],
  perpendicular: [{line: "S-A", symbol: "⊥"}]
}

Step 4: objects = ["M"]
    ↓
distribute_annotations() → Tìm annotations cho M
    ↓
Step 4 annotations: {
  points: [{point: "M", label: "trung điểm AB"}]
}
```

### 3. Frontend hiển thị theo step
```
User chuyển đến Step 2
    ↓
goToStep(2)
    ↓
showAnnotationsUpToStep(2)
    ↓
Tích lũy annotations từ Step 0, 1, 2
    ↓
Render: {
  edges: ["3" trên AB, "4" trên BC, "6" trên SA],
  angles: ["∟" tại B],
  perpendicular: ["⊥" tại SA]
}
```

## Ví dụ cụ thể

### Bài 2: Hình chóp S.ABC với M

#### Step 0 (Initial)
- Objects: []
- Annotations: []

#### Step 1: Vẽ đáy ABC
- Objects: A, B, C, A-B, B-C, C-A
- Annotations hiển thị:
  - "3" trên AB
  - "4" trên BC
  - "∟" tại B

#### Step 2: Dựng S và SA
- Objects: S, S-A
- Annotations hiển thị (tích lũy):
  - "3" trên AB (từ step 1)
  - "4" trên BC (từ step 1)
  - "∟" tại B (từ step 1)
  - "6" trên SA (mới)
  - "⊥" tại SA (mới)

#### Step 3: Nối cạnh bên
- Objects: S-B, S-C
- Annotations: (tích lũy từ step 1, 2)

#### Step 4: Điểm M
- Objects: M
- Annotations hiển thị (tích lũy):
  - Tất cả từ step 1, 2, 3
  - "trung điểm AB" tại M (mới)

#### Step 5: Nối SM
- Objects: S-M
- Annotations: (tích lũy tất cả)

## Files đã thay đổi

### Backend
1. ✅ `backend/app/solver/steps_generator.py`
   - Thêm `distribute_annotations()`
   - Cập nhật `generate_pyramid_steps()`
   - Cập nhật `generate_prism_steps()`

### Frontend
1. ✅ `frontend/src/types/geometry.ts`
   - Thêm `annotations?: Annotations` vào `Step`

2. ✅ `frontend/src/three/SceneManager.ts`
   - Thêm `annotationRenderer` và `geometryData`
   - Cập nhật `goToStep()`
   - Thêm `showAnnotationsUpToStep()`

## Test

Xem file `TEST_STEP_BY_STEP_ANNOTATIONS.md` để test chi tiết.

Hoặc test nhanh với `DEMO_STEP_ANNOTATIONS.md`.

## Lợi ích

✅ **Trực quan hơn:** Annotations xuất hiện đúng lúc objects được vẽ  
✅ **Dễ hiểu hơn:** Học sinh thấy rõ ký hiệu nào thuộc về phần nào  
✅ **Logic hơn:** Ký hiệu ⊥ xuất hiện khi vẽ cạnh vuông góc  
✅ **Tích lũy:** Annotations cũ vẫn hiển thị, không bị mất  

## Mở rộng

Có thể thêm:
- Animation khi annotations xuất hiện
- Highlight annotations mới trong step hiện tại
- Fade out annotations cũ
- Tooltip giải thích ký hiệu
