# Requirements Document - Gemini File Search Integration

## Introduction

Tích hợp Gemini File Search API để sử dụng tài liệu hình học không gian trong thư mục `Documents/` làm context khi giải toán. Điều này giúp AI có thể tham khảo lý thuyết, công thức, và phương pháp giải từ tài liệu có sẵn, từ đó đưa ra lời giải chính xác và chi tiết hơn.

## Glossary

- **Gemini File Search**: API của Google Gemini cho phép upload files và search nội dung
- **File Index**: Chỉ mục chứa các file đã upload để search
- **Context**: Thông tin từ tài liệu được trích xuất để bổ sung vào prompt
- **Documents Folder**: Thư mục `D:\CDNNLT\Project_CK\Documents` chứa tài liệu PDF về hình học
- **Solve Problem Endpoint**: API endpoint `/geometry/solve-problem/{id}` để giải toán

## Requirements

### Requirement 1

**User Story:** Là một học sinh, tôi muốn AI giải toán dựa trên tài liệu lý thuyết có sẵn, để lời giải có căn cứ và chính xác hơn.

#### Acceptance Criteria

1. WHEN hệ thống khởi động THEN hệ thống SHALL tạo Gemini File Search index nếu chưa có
2. WHEN hệ thống khởi động THEN hệ thống SHALL upload tất cả PDF files từ thư mục Documents vào index
3. WHEN người dùng gọi API giải toán THEN hệ thống SHALL search các tài liệu liên quan dựa trên đề bài
4. WHEN tìm thấy tài liệu liên quan THEN hệ thống SHALL trích xuất nội dung và thêm vào prompt cho Gemini
5. WHEN Gemini giải toán THEN Gemini SHALL sử dụng context từ tài liệu để đưa ra lời giải chính xác

### Requirement 2

**User Story:** Là một developer, tôi muốn quản lý file index một cách hiệu quả, để tránh upload trùng lặp và tối ưu hiệu suất.

#### Acceptance Criteria

1. WHEN file đã tồn tại trong index THEN hệ thống SHALL không upload lại file đó
2. WHEN có file mới trong Documents THEN hệ thống SHALL tự động upload file mới vào index
3. WHEN file bị xóa khỏi Documents THEN hệ thống SHALL xóa file khỏi index
4. WHEN cần refresh index THEN hệ thống SHALL cung cấp API endpoint để refresh toàn bộ index
5. WHEN upload file THEN hệ thống SHALL log thông tin file (tên, kích thước, trạng thái)

### Requirement 3

**User Story:** Là một học sinh, tôi muốn biết lời giải có tham khảo từ tài liệu nào, để có thể đọc thêm chi tiết.

#### Acceptance Criteria

1. WHEN AI giải toán THEN response SHALL bao gồm danh sách tài liệu đã tham khảo
2. WHEN có tài liệu được sử dụng THEN response SHALL hiển thị tên file và đoạn trích liên quan
3. WHEN không tìm thấy tài liệu liên quan THEN hệ thống SHALL giải toán bình thường không dùng context
4. WHEN hiển thị lời giải THEN frontend SHALL hiển thị badge "📚 Tham khảo từ tài liệu"
5. WHEN user click vào badge THEN frontend SHALL hiển thị chi tiết tài liệu đã tham khảo

### Requirement 4

**User Story:** Là một admin, tôi muốn monitor việc sử dụng File Search API, để kiểm soát chi phí và hiệu suất.

#### Acceptance Criteria

1. WHEN upload file THEN hệ thống SHALL log số lượng files và tổng dung lượng
2. WHEN search file THEN hệ thống SHALL log số lượng queries và kết quả trả về
3. WHEN có lỗi API THEN hệ thống SHALL log chi tiết lỗi và retry nếu cần
4. WHEN vượt quota THEN hệ thống SHALL fallback về giải toán không dùng context
5. WHEN cần debug THEN hệ thống SHALL cung cấp endpoint để xem trạng thái index

### Requirement 5

**User Story:** Là một developer, tôi muốn cấu hình File Search linh hoạt, để dễ dàng bật/tắt và điều chỉnh tham số.

#### Acceptance Criteria

1. WHEN cấu hình trong .env THEN hệ thống SHALL đọc cấu hình USE_FILE_SEARCH (true/false)
2. WHEN USE_FILE_SEARCH=false THEN hệ thống SHALL không sử dụng File Search
3. WHEN cấu hình MAX_SEARCH_RESULTS THEN hệ thống SHALL giới hạn số lượng kết quả search
4. WHEN cấu hình DOCUMENTS_PATH THEN hệ thống SHALL đọc files từ đường dẫn đó
5. WHEN thay đổi cấu hình THEN hệ thống SHALL áp dụng ngay không cần restart
