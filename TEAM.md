# Team

## Thông tin nhóm

- Tên nhóm: Ban5
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-Ban5-ResearchAgentToolEval` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt: https://github.com/haiquanng/K5-L3B-DAY03-Ban5-ResearchAgentToolEval, nhánh `main`, commit chốt: (điền khi nộp)

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Nguyễn Văn Hải Quân | 2A202603994 | 26ai.quannvh@vinuni.edu.vn | haiquanng | Lead / Developer |
|   2 | Lại Trọng Đức | 2A202604019 | laitrongduc@vinuni.edu.vn | laitrongduc | Developer |
|   3 | Nguyễn Bảo Trung | 2A202604013 | nbtrungrhm@gmail.com | trungnb | Developer |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/2A202604013_NguyenBaoTrung.md`.

## Nguyễn Văn Hải Quân - 2A202603994

### Phần việc phụ trách

- Lead nhóm, quản lý repository, thiết lập pipeline và điều phối merge PR.
- Xây dựng giao diện web (`web/`, Next.js, shadcn/ui) và API backend (`starter_v0/server.py`, FastAPI).
- Tích hợp bot tương tác hai chiều qua Telegram (`starter_v0/telegram_bot.py`).
- Đóng gói và triển khai phiên bản web lên Vercel: `https://research-agent-ban5.vercel.app`.

### Đóng góp cụ thể

- Triển khai server FastAPI hỗ trợ Server-Sent Events (SSE) để truyền trực tiếp tiến trình suy luận và gọi tool của agent theo thời gian thực lên giao diện web.
- Tích hợp chức năng chọn version (v0, v1, v2, v3) ngay trên web UI mà không cần can thiệp code (`artifacts/versions/`).
- Triển khai cơ chế xác nhận duyệt tin trước khi gửi (`ask / confirm`) trên web và qua các nút bấm tương tác Inline Keyboard trên Telegram.

### Bằng chứng

- File và commit: `starter_v0/server.py`, `starter_v0/telegram_bot.py`, thư mục `web/`, commit `9bdc927`, `596bf37`, `60e9dd2`.
- Báo cáo cá nhân chi tiết: `report/team/2A202603994_NguyenVanHaiQuan.md`.

## Lại Trọng Đức - 2A202604019

### Phần việc phụ trách

- Phát triển công cụ mới `stats` (`starter_v0/tools/stats/`) phục vụ thống kê mô tả.
- Xây dựng tài liệu đặc tả `TOOL.md` và đăng ký tool trong `tools/__init__.py` và `artifacts/tools.yaml`.
- Viết 17 hàm unit test trong `starter_v0/tests/test_tools_todo.py`, xóa bỏ toàn bộ `pytest.skip` (đạt 0 skipped).
- Phối hợp tối ưu định nghĩa mô tả tool trong `tools.yaml` cho các vòng lặp v1-v3.

### Đóng góp cụ thể

- Hoàn thiện tool `stats` chuẩn Python stdlib (`statistics`), hỗ trợ `mean`, `median`, `stdev`, xử lý lỗi an toàn không gây crash agent.
- Mở rộng parametrization test suite lên 37 test cases, mock HTTP sạch sẽ, bao phủ toàn bộ các trường hợp biên của 10 công cụ trong hệ thống.
- Chạy kiểm thử tự động đạt 104/104 test passed (0 failed, 0 skipped), ghi nhận log tại `starter_v0/analysis/duclt_pytest.txt`.

### Bằng chứng

- File và commit: `starter_v0/tools/stats/tool.py`, `starter_v0/tools/stats/TOOL.md`, `starter_v0/tests/test_tools_todo.py`, `starter_v0/analysis/duclt_pytest.txt`, branch `feat/DucLT-tool-tests` (commit `0d4b517`, `b788f27`, `0e8ce8f`).
- Báo cáo cá nhân chi tiết: `report/team/2A202604019_LaiTrongDuc.md`.

## Nguyễn Bảo Trung - 2A202604013

### Phần việc phụ trách

- Xây dựng bộ test case đánh giá nhóm (`starter_v0/data/eval_group.json`) gồm 5 single-turn + 5 multi-turn.
- Phân tích lỗi (Failure Analysis) v0, giải pháp cho Bảng B2; chẩn đoán cơ chế Human-in-the-Loop case R12.
- Viết tài liệu Phần A (A1, A2, A3), cập nhật Bảng B1, B3, B5a trong `report/team/group_report.md`.
- Chạy benchmark bộ eval nhóm và kiểm tra hồi quy bộ base eval đạt 100% điểm tối đa; quản lý đồng bộ nhánh git.

### Đóng góp cụ thể

- Thiết kế 10 test cases nhóm (`eval_group.json`) bao quát các ranh giới: thiếu chủ đề arXiv, duyệt Telegram trước khi gửi, định tuyến paper, guardrail từ chối code, gọi tool mới `stats`, và hội thoại nhiều lượt.
- Thực nghiệm đo lường bộ eval nhóm: phân tích 3 lỗi ban đầu (`G01`, `G03`, `G07`), tối ưu `tools.yaml` và `system_prompt.md` đưa kết quả lên **10/10 PASS (100%)**.
- Chạy kiểm tra hồi quy 20 case Base Eval trên provider OpenRouter: đạt **20/20 PASS (100%)**.
- Tích hợp tool `stats` của DucLT, kiểm thử suite unit test đạt **104 passed, 0 failed, 0 skipped**.

### Bằng chứng

- File và commit: `data/eval_group.json` (commit `0cdeb72`, `5cdeca5`), `group_report.md` (commit `c35c322`, `0cdeb72`, `aeecc7a`, `5cdeca5`).
- Run JSON: `starter_v0/runs/v3_B_group_openrouter_20261110T191237962030.json` (10/10), `starter_v0/runs/v3_B_base_openrouter_20261110T191959929397.json` (20/20).
- Báo cáo cá nhân chi tiết: `report/team/2A202604013_NguyenBaoTrung.md`.
