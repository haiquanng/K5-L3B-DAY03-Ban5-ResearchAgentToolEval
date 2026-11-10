# Báo cáo cá nhân — Lại Trọng Đức - 2A202604019

## 1. Thông tin thành viên

- Họ tên: Lại Trọng Đức
- MSSV: 2A202604019
- Email: laitrongduc@vinuni.edu.vn
- Vai trò: Developer (Phụ trách Tool mới `stats`, Test Suite & Đo lường)

## 2. Phần việc phụ trách

- Phát triển công cụ mới `stats` (`starter_v0/tools/stats/`) tính toán thống kê mô tả (`mean`, `median`, `stdev`) từ dữ liệu số thực.
- Soạn thảo tài liệu đặc tả `TOOL.md` và đăng ký tool trong `tools/__init__.py` và `artifacts/tools.yaml`.
- Viết 17 hàm unit test trong `starter_v0/tests/test_tools_todo.py` bao phủ cả 10 tool có sẵn và 3 trường hợp kiểm thử cho tool mới `stats`, bỏ toàn bộ `pytest.skip`.
- Chạy kiểm thử tự động toàn diện đạt 104/104 test passed (0 failed, 0 skipped), ghi nhận log tại `starter_v0/analysis/duclt_pytest.txt`.
- Phối hợp tinh chỉnh định nghĩa tham số và schema mô tả tool trong `tools.yaml` phục vụ vòng lặp v3 đạt 20/20 base eval.

## 3. Đóng góp cụ thể

- **Tool mới `stats`**:
  - Triển khai hàm `stats(values: list[float], statistic: str = "mean")` sử dụng thư viện chuẩn `statistics` của Python (Ponytail style - zero bloat, không thêm thư viện ngoài).
  - Hỗ trợ 3 độ đo: `mean`, `median`, và `stdev` (độ lệch chuẩn mẫu $n-1$).
  - Thiết kế xử lý lỗi an toàn: kiểm tra danh sách rỗng, kiểu dữ liệu không hợp lệ (chuỗi, boolean, NaN, Infinity), hoặc số lượng phần tử $< 2$ khi tính `stdev`; trả về dictionary lỗi chuẩn `{tool: "stats", error: ..., message: ...}` thay vì ném exception làm sập agent.
- **Bộ Unit Test (`test_tools_todo.py`)**:
  - Xóa bỏ toàn bộ `pytest.skip` trong `test_tools_todo.py`, mở rộng parametrization thành 37 kịch bản kiểm thử độc lập.
  - Mock toàn bộ cuộc gọi HTTP bằng `fake_http` và inject mock key thông qua `monkeypatch.setenv`, đảm bảo test chạy offline 100%, không tốn chi phí API và không rò rỉ secret.
  - Bổ sung test kiểm tra các trường hợp biên: cắt markdown Telegram (3999, 4000, 4001, 4500 ký tự), thiếu biến môi trường, định dạng ngày tháng và xử lý lỗi mạng.
- **Hỗ trợ tối ưu hóa v3**:
  - Góp ý chuẩn hóa schema các tham số trong `tools.yaml` (như `statistic` chỉ nhận `mean | median | stdev`, `response_type` trong `clarify`), giúp mô hình điều hướng chính xác 100% trên cả bộ test cơ sở và bộ test mở rộng của nhóm.

## 4. Bằng chứng

- **Files**:
  - `starter_v0/tools/stats/tool.py`
  - `starter_v0/tools/stats/TOOL.md`
  - `starter_v0/tests/test_tools_todo.py`
  - `starter_v0/analysis/duclt_pytest.txt`
- **Commits / Merges**:
  - Nhánh làm việc: `feat/DucLT-tool-tests`
  - Commit `0d4b517`: Clarify v3 tool routing and document 20-of-20 evaluation.
  - Commit `b788f27`: Merge DucLT stats tool and unit tests.
  - Commit `0e8ce8f`: Merge DucLT v3 run (20/20 perfect score) and optimized tools.yaml.
- **Kết quả kiểm thử**:
  - Lệnh: `pytest`
  - Kết quả: 130 passed, 0 failed, 0 skipped (trong đó 104 test cho core/tools và 26 test cho telegram_bot & server versions).
- **Công cụ AI đã dùng**:
  - Claude Code & Codex: Hỗ trợ sinh khung test case biên và gợi ý xử lý các kiểu dữ liệu NaN/Infinity. Đã tự review lại toàn bộ diff, kiểm tra logic assert và chạy đối soát trực tiếp trên terminal.

## 5. Tự đánh giá

- Hoàn thành đầy đủ và vượt tiến độ các nhiệm vụ được giao ở Checkpoint 3 (CP3) và Checkpoint 4 (CP4).
- Bộ unit test sạch (0 skipped) đóng góp trực tiếp vào mục Bonus Test Challenge của nhóm.
- Đánh giá: Hoàn thành tốt nhiệm vụ (10/10).
