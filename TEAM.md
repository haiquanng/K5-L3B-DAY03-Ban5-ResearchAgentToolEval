# Team

## Thông tin nhóm

- Tên nhóm: Ban5
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-Ban5-ResearchAgentToolEval` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt: https://github.com/haiquanng/K5-L3B-DAY03-Ban5-ResearchAgentToolEval, nhánh `main`, commit chốt: (điền khi nộp)

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Nguyễn Văn Hải Quân | 2A202603994 | 26ai.quannvh@vinuni.edu.vn | haiquanng | Developer |
|   2 | Lại Trọng Đức | 2A202604019 | | laitrongduc | Developer |
|   3 | Nguyễn Bảo Trung | 2A202604013 | nbtrungrhm@gmail.com | trungnb | Developer |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/2A202604013_NguyenBaoTrung.md`.

Sao chép mục dưới đây cho từng thành viên.

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
