# 🔧 FIX LOG - Sửa lỗi vẽ từng bước

## ❌ VẤN ĐỀ

Khi demo, các cạnh bên không hiển thị ở bước 3 "Nối các cạnh bên".

## 🔍 NGUYÊN NHÂN

1. **Backend**: `StepsGenerator` tạo tên cạnh không chuẩn
   - Ví dụ: `"SA"`, `"SB"` (không có dấu `-`)
   
2. **Frontend**: `GeometryBuilder` lưu cạnh với tên khác
   - Ví dụ: `"edge_0"`, `"edge_1"` (không match với tên từ backend)

3. **Logic matching**: Không tìm được cạnh vì tên không khớp

## ✅ GIẢI PHÁP

### 1. Sửa `steps_generator.py`

**Thay đổi**:
- Tên cạnh đáy: `"A-B"`, `"B-C"`, `"C-D"`, `"D-A"` (có dấu `-`)
- Tên cạnh bên: `"S-A"`, `"S-B"`, `"S-C"`, `"S-D"` (có dấu `-`)

**Code**:
```python
# Tạo tên cạnh đáy
base_edges = []
for i in range(len(base_points)):
    p1 = base_points[i]
    p2 = base_points[(i+1) % len(base_points)]
    base_edges.append(f"{p1}-{p2}")

# Tạo tên cạnh bên
side_edges = [f"{apex}-{p}" for p in base_points]
```

### 2. Sửa `GeometryBuilder.ts`

**Thay đổi**:
- Lưu cạnh với key là `"A-B"` thay vì `"edge_0"`
- Đơn giản hóa logic `showObjectsForStep()`

**Code**:
```typescript
// Build edges với tên chuẩn hóa
data.edges.forEach((edge, index) => {
  const edgeName = `${edge.start}-${edge.end}`;
  const line = this.createEdge(
    data.points[edge.start],
    data.points[edge.end],
    edgeName
  );
  this.objects.set(edgeName, line);  // ← Key là "A-B"
  this.scene.add(line);
});

// Show objects - đơn giản hơn
showObjectsForStep(step: number) {
  currentStep.objects.forEach(objName => {
    const obj = this.objects.get(objName);  // ← Tìm trực tiếp
    if (obj) {
      obj.visible = true;
    }
  });
}
```

## 📊 KẾT QUẢ

### Trước khi sửa:
```
Bước 1: ✅ Vẽ đáy ABCD (4 điểm + 4 cạnh)
Bước 2: ✅ Dựng đỉnh S (1 điểm)
Bước 3: ❌ Nối các cạnh bên (không hiện)
Bước 4: ✅ Hoàn thiện (tất cả)
```

### Sau khi sửa:
```
Bước 1: ✅ Vẽ đáy ABCD (4 điểm + 4 cạnh)
Bước 2: ✅ Dựng đỉnh S (1 điểm)
Bước 3: ✅ Nối các cạnh bên (4 cạnh SA, SB, SC, SD)
Bước 4: ✅ Hoàn thiện (tất cả)
```

## 🧪 TEST

### Hình chóp (Pyramid)
- ✅ Bước 1: Đáy ABCD xuất hiện
- ✅ Bước 2: Đỉnh S xuất hiện
- ✅ Bước 3: 4 cạnh bên xuất hiện (S-A, S-B, S-C, S-D)
- ✅ Bước 4: Toàn bộ hình

### Lăng trụ (Prism)
- ✅ Bước 1: Đáy ABC xuất hiện
- ✅ Bước 2: Đỉnh A'B'C' xuất hiện
- ✅ Bước 3: 3 cạnh bên xuất hiện (A-A', B-B', C-C')
- ✅ Bước 4: Toàn bộ hình

### Hình lập phương (Cube)
- ✅ Tương tự lăng trụ

## 📝 NOTES

- Tên cạnh phải **nhất quán** giữa backend và frontend
- Format chuẩn: `"A-B"` (có dấu `-`)
- Key trong Map phải match với tên trong `steps.objects`

## ✅ STATUS

**FIXED** - Đã test thành công với cả 3 dạng hình.

---

**Ngày sửa**: 2026-05-05  
**Files thay đổi**:
- `backend/app/solver/steps_generator.py`
- `frontend/src/three/GeometryBuilder.ts`
