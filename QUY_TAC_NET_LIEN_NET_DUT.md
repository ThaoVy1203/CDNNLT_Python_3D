# Quy tắc nét liền và nét đứt trong hình học không gian

## 🎯 Nguyên tắc cơ bản

**KHÔNG PHẢI** "nhìn thấy vs khuất" mà là **"cạnh thật vs đường phụ trợ"**

---

## ✅ NÉT LIỀN (solid) - Cạnh thật của hình

### 1. **Cạnh đáy**
Tất cả các cạnh tạo thành đáy của hình
- Hình vuông ABCD: AB, BC, CD, DA
- Tam giác ABC: AB, BC, CA
- **Luôn luôn nét liền**, dù nhìn thấy hay không

### 2. **Cạnh bên**
Các cạnh nối đỉnh với đáy
- Hình chóp S.ABCD: SA, SB, SC, SD
- Lăng trụ ABC.A'B'C': AA', BB', CC'
- **Luôn luôn nét liền**, dù nhìn thấy hay không

### 3. **Cạnh của khối đa diện**
Bất kỳ cạnh nào là biên của mặt phẳng
- Hình lập phương: 12 cạnh đều nét liền
- Tứ diện: 6 cạnh đều nét liền

---

## ⚡ NÉT ĐỨT (dashed) - Đường phụ trợ

### 1. **Đường chéo trong mặt phẳng**
Đường nối 2 đỉnh không kề nhau trong cùng một mặt
- Đường chéo đáy: AC, BD (để xác định tâm O)
- Đường chéo mặt bên: nếu cần thiết

**Mục đích**: Giúp xác định điểm đặc biệt (tâm, giao điểm)

### 2. **Đường cao**
Đường từ đỉnh xuống đáy (hoặc mặt phẳng)
- SH: từ S xuống đáy (ABCD)
- AH: từ A xuống mặt (SBC)

**Mục đích**: Thể hiện quan hệ vuông góc

### 3. **Đường nối điểm đặc biệt**
Đường nối các điểm không phải đỉnh của hình
- SM: từ S đến trung điểm M
- SO: từ S đến tâm O
- OM: từ tâm O đến trung điểm M

**Mục đích**: Đường cần tính toán trong bài toán

### 4. **Đường hình chiếu**
Đường từ điểm xuống mặt phẳng
- Hình chiếu của S lên (ABCD) là H → SH nét đứt

### 5. **Đường phân đoạn**
Khi điểm nằm trên cạnh, chia cạnh thành 2 phần
- M ∈ CD → CM và MD
- **Nếu M là trung điểm**: CM = MD, cả 2 đều nét đứt
- **Nếu M không phải trung điểm**: Phần ngắn hơn nét đứt, phần dài hơn nét liền

---

## 📋 Ví dụ cụ thể

### Ví dụ 1: Hình chóp S.ABCD, tâm đáy O

**NÉT LIỀN:**
- Cạnh đáy: AB, BC, CD, DA
- Cạnh bên: SA, SB, SC, SD

**NÉT ĐỨT:**
- Đường chéo: AC, BD (để xác định O)
- Đường cao: SO (nếu S ở trên O)

**Lý do**: AC và BD không phải cạnh của hình chóp, chỉ là đường phụ để tìm tâm O.

### Ví dụ 2: Hình chóp S.ABCD, M là trung điểm CD

**NÉT LIỀN:**
- Cạnh đáy: AB, BC, DA (CD bị chia thành CM và MD)
- Cạnh bên: SA, SB, SC, SD

**NÉT ĐỨT:**
- CM: từ C đến M (nửa cạnh CD)
- MD: từ M đến D (nửa cạnh CD)
- SM: từ S đến M (đường cần tính)

**Lý do**: 
- CD không còn là cạnh liền mạch vì có điểm M ở giữa
- CM và MD là các đoạn phụ trợ để thể hiện vị trí M
- SM là đường cần tính toán trong bài toán

### Ví dụ 3: Hình chóp S.ABC, SA ⊥ (ABC)

**NÉT LIỀN:**
- Cạnh đáy: AB, BC, CA
- Cạnh bên: SA, SB, SC

**NÉT ĐỨT:**
- Không có (nếu không có điểm đặc biệt)

**Lý do**: Tất cả đều là cạnh thật của hình chóp.

### Ví dụ 4: Hình chóp S.ABCD, H là hình chiếu của S lên (ABCD)

**NÉT LIỀN:**
- Cạnh đáy: AB, BC, CD, DA
- Cạnh bên: SA, SB, SC, SD

**NÉT ĐỨT:**
- SH: đường cao từ S xuống H
- AH, BH, CH, DH: đường nối H với các đỉnh (nếu cần)

**Lý do**: SH là đường phụ trợ thể hiện quan hệ vuông góc.

---

## 🔧 Quy tắc implementation

### 1. **Xác định cạnh thật**
```python
# Cạnh đáy
base_edges = ["A-B", "B-C", "C-D", "D-A"]  # Hình vuông
base_edges = ["A-B", "B-C", "C-A"]         # Tam giác

# Cạnh bên
apex_edges = ["S-A", "S-B", "S-C", "S-D"]  # Hình chóp

# TẤT CẢ đều style="solid"
```

### 2. **Xác định đường phụ trợ**
```python
# Đường chéo (để xác định tâm)
if "O" in points:
    auxiliary_edges = ["A-C", "B-D"]  # style="dashed"

# Đường nối điểm đặc biệt
if "M" in points:
    auxiliary_edges.append("S-M")  # style="dashed"

# Đường cao
if has_height:
    auxiliary_edges.append("S-H")  # style="dashed"
```

### 3. **Xử lý điểm nằm trên cạnh**
```python
# M là trung điểm CD
if "M" in points and M is midpoint of "CD":
    # KHÔNG vẽ CD nét liền
    # Thay vào đó:
    edges.append({"start": "C", "end": "M", "style": "dashed"})
    edges.append({"start": "M", "end": "D", "style": "dashed"})
    edges.append({"start": "S", "end": "M", "style": "dashed", "color": "gold"})
```

### 4. **Màu sắc**
```python
# Cạnh thật
solid_edges: color = "black" (default)

# Đường phụ trợ
dashed_edges: color = "gray" (mặc định)
special_edges: color = "gold" (SM), "purple" (SO), "teal" (đường cao)
```

---

## ⚠️ Lỗi thường gặp

### ❌ Lỗi 1: Vẽ cạnh khuất bằng nét đứt
```python
# SAI
if is_hidden(edge):
    style = "dashed"
```
**Sửa**: Tất cả cạnh thật đều nét liền, dù khuất hay không.

### ❌ Lỗi 2: Vẽ đường chéo bằng nét liền
```python
# SAI
edges.append({"start": "A", "end": "C", "style": "solid"})
```
**Sửa**: Đường chéo AC là đường phụ trợ, phải nét đứt.

### ❌ Lỗi 3: Vẽ cả CD và CM, MD
```python
# SAI - Trùng lặp
edges.append({"start": "C", "end": "D", "style": "solid"})
edges.append({"start": "C", "end": "M", "style": "dashed"})
edges.append({"start": "M", "end": "D", "style": "dashed"})
```
**Sửa**: Chỉ vẽ CM và MD, không vẽ CD.

### ❌ Lỗi 4: Không vẽ đường chéo khi có tâm O
```python
# SAI - Không thể hiện O là giao điểm AC và BD
if "O" in points:
    # Chỉ vẽ điểm O, không vẽ AC, BD
```
**Sửa**: Phải vẽ AC và BD (nét đứt) để thể hiện O là giao điểm.

---

## 📊 Bảng tổng hợp

| Loại đường | Nét | Màu | Ví dụ | Mục đích |
|-----------|-----|-----|-------|----------|
| Cạnh đáy | Liền | Đen | AB, BC, CD, DA | Cạnh thật của hình |
| Cạnh bên | Liền | Đen | SA, SB, SC, SD | Cạnh thật của hình |
| Đường chéo | Đứt | Xám | AC, BD | Xác định tâm, giao điểm |
| Đường cao | Đứt | Teal | SH, AH | Thể hiện vuông góc |
| Đường nối điểm đặc biệt | Đứt | Gold/Purple | SM, SO | Đường cần tính toán |
| Đường phân đoạn | Đứt | Xám | CM, MD (khi M ∈ CD) | Thể hiện vị trí điểm |

---

## 🎨 Màu sắc gợi ý

```python
COLORS = {
    "solid_edge": "black",           # Cạnh thật
    "diagonal": "gray",              # Đường chéo
    "height": "teal",                # Đường cao
    "special_line": "gold",          # SM, AM...
    "center_line": "purple",         # SO, AO...
    "segment": "gray",               # CM, MD...
}
```

---

## ✅ Checklist khi vẽ hình

- [ ] Tất cả cạnh đáy đều nét liền?
- [ ] Tất cả cạnh bên đều nét liền?
- [ ] Đường chéo (nếu có) đều nét đứt?
- [ ] Đường cao (nếu có) đều nét đứt?
- [ ] Đường nối điểm đặc biệt đều nét đứt?
- [ ] Không có cạnh thật nào bị vẽ nét đứt?
- [ ] Không có đường phụ nào bị vẽ nét liền?
- [ ] Khi có điểm trên cạnh, cạnh đó đã bị chia thành 2 đoạn nét đứt?

---

## 🔍 Ví dụ code đúng

```python
def _solve_pyramid(self, constraints: Dict) -> Dict[str, Any]:
    # ... tính toán points ...
    
    edges = []
    
    # 1. Cạnh đáy - NÉT LIỀN
    if "D" in points:
        # Kiểm tra xem có điểm nào nằm trên cạnh không
        if "M" in points and self._is_on_edge(points["M"], "C", "D", points):
            # M nằm trên CD → chia CD thành CM và MD (nét đứt)
            edges.extend([
                {"start": "A", "end": "B", "style": "solid"},
                {"start": "B", "end": "C", "style": "solid"},
                {"start": "C", "end": "M", "style": "dashed", "color": "gray"},
                {"start": "M", "end": "D", "style": "dashed", "color": "gray"},
                {"start": "D", "end": "A", "style": "solid"}
            ])
        else:
            # Không có điểm đặc biệt → vẽ bình thường
            edges.extend([
                {"start": "A", "end": "B", "style": "solid"},
                {"start": "B", "end": "C", "style": "solid"},
                {"start": "C", "end": "D", "style": "solid"},
                {"start": "D", "end": "A", "style": "solid"}
            ])
    
    # 2. Cạnh bên - NÉT LIỀN
    edges.extend([
        {"start": "S", "end": "A", "style": "solid", "color": "teal"},
        {"start": "S", "end": "B", "style": "solid"},
        {"start": "S", "end": "C", "style": "solid"},
        {"start": "S", "end": "D", "style": "solid"}
    ])
    
    # 3. Đường phụ trợ - NÉT ĐỨT
    
    # Đường chéo (để xác định tâm O)
    if "O" in points:
        edges.extend([
            {"start": "A", "end": "C", "style": "dashed", "color": "gray"},
            {"start": "B", "end": "D", "style": "dashed", "color": "gray"}
        ])
    
    # Đường nối điểm đặc biệt
    if "M" in points:
        edges.append({
            "start": "S",
            "end": "M",
            "style": "dashed",
            "color": "gold",
            "label": "SM"
        })
    
    return {"points": points, "edges": edges, ...}
```

---

## 📝 Tóm tắt

**Quy tắc vàng**: 
1. **Cạnh thật của hình → NÉT LIỀN** (dù nhìn thấy hay khuất)
2. **Đường phụ trợ → NÉT ĐỨT** (đường chéo, đường cao, đường nối điểm đặc biệt)
3. **Khi có điểm trên cạnh → Chia cạnh thành 2 đoạn NÉT ĐỨT**

Mục đích: Giúp người xem hiểu cấu trúc hình, phân biệt cạnh thật và đường phụ trợ.
