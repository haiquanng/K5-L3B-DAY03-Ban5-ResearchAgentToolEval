# Team

## Thông tin nhóm

- Tên nhóm: Ban5
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-Ban5-ResearchAgentToolEval` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt: https://github.com/haiquanng/K5-L3B-DAY03-Ban5-ResearchAgentToolEval, nhánh `main`, commit chốt: `33e6047`

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Nguyễn Văn Hải Quân | 2A202603994 | 26ai.quannvh@vinuni.edu.vn | haiquanng | Developer |
|   2 | Lại Trọng Đức | 2A202604019 | 26ai.duclt2@vinuni.edu.vn | laitrongduc | Developer |
|   3 | Nguyễn Bảo Trung | 2A202604013 | nbtrungrhm@gmail.com | trungnb | Developer |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/2A202604013_NguyenBaoTrung.md`.

Sao chép mục dưới đây cho từng thành viên.

## Nguyễn Văn Hải Quân - 2A202603994

### Phần việc phụ trách

- Trưởng nhóm: phân việc (`tasks/`), setup, chạy baseline v0, vòng lặp prompt v1 và v2, review và kiểm tra bằng chứng toàn nhóm.
- Giao diện web (Next.js) và server FastAPI stream từng bước gọi tool; ô chọn version v0–v6; bot Telegram để chat với agent.
- Bonus: ba tool mới `calc`, `compare`, `dedupe` và thử nghiệm model local qua Ollama.

### Đóng góp cụ thể

- Baseline v0 đạt 13/20, phân loại lỗi từng case sai (bảng B2). v1: 13 → 18/20 (bỏ chỉ dẫn xấu, thêm rule hỏi lại và xin xác nhận). v2: 18/20, không tăng điểm, ghi nhận trung thực.
- Giao diện web có timeline tool call, hộp xác nhận trước khi `send`, lưu transcript và che khóa bí mật; bot Telegram chỉ cho các chat được phép; bản prompt và tools của từng version được đóng băng, có test so mã băm với `version_log.csv`.
- Rà soát bằng chứng: phát hiện nhiều run gắn nhãn "v3" nhưng khác mã băm, ghi nhận bản hiện tại là v4 và chạy lại bằng provider `openai` (base 20/20, group 10/10); chạy group cho v3 trên đề gốc (7/10).
- Bonus 3 tool mới (cùng `stats` của Đức là 4 tool): 52 test mới, 200 test đạt, 0 skipped; v5 (thêm tool, group tụt 9/10 do G10) rồi v6 (sửa bằng một dòng prompt, group 10/10).
- Bonus model local: `llama3.2:3b` và `qwen2.5:7b`, ba vòng tối ưu; phát hiện prompt dài bị Ollama cắt do cửa sổ ngữ cảnh 4096 token; `qwen2.5:7b` từ 4/20 lên 14/20; đối chứng với ngữ cảnh 16K và kiểm tra ngược trên cloud (19/20).

### Bằng chứng

- Commit: `7907b76` (v0), `fcbf17b` (v1), `04eeefb` (v2), `9bdc927` (web và server), `596bf37` (bot Telegram), `60e9dd2` (chọn version), `26c929b` (run group v3), `e1d36ac` (v4), `e1b17cf` (3 tool mới, v5, v6), `33e6047` (model local).
- Run: `starter_v0/runs/v0_…`, `v1_…`, `v2_…`, `v4_B_*_openai_…`, `v5_…`, `v6_…`, `*_ollama_…`; nhật ký tổng hợp [CHANGED_LOGS.md](CHANGED_LOGS.md).
- Báo cáo cá nhân: [2A202603994_NguyenVanHaiQuan.md](report/team/2A202603994_NguyenVanHaiQuan.md).

## Lại Trọng Đức - 2A202604019

### Phần việc phụ trách

- Unit test cho tool có sẵn, phát triển tool mới `stats` và kiểm tra contract giữa khai báo với code.
- Tối ưu mô tả tool và quy ước tham số trong `tools.yaml` cho v3; phân tích lỗi, chạy eval và lưu bằng chứng đo lường.
- Viết tài liệu phương pháp trong changelog và báo cáo cá nhân.

### Đóng góp cụ thể

- Hoàn thành 17 hàm test: 14 cho tool có sẵn và 3 cho `stats`, mở rộng thành 37 trường hợp bằng parametrization. Test chạy offline với HTTP/key giả; toàn suite đạt **104 passed, 0 failed, 0 skipped**, bao gồm contract test.
- Viết tool local `stats` tính mean, median, độ lệch chuẩn mẫu; bổ sung `TOOL.md`, đăng ký trong `tools/__init__.py` và `artifacts/tools.yaml`; kiểm tra dữ liệu không hợp lệ và nhánh lỗi trả error dict.
- Viết lại description và quy ước tham số của 11 tool, giữ nguyên prompt v2, code, schema, bộ eval và model `gpt-4o-mini`. Làm rõ `clarify` dùng `yes_no` để xác nhận ý định gửi trước khi hỏi nội dung; `social_search` không được gọi khi người dùng đã bỏ Twitter.
- Phân tích R12/M06 từ tool call thực tế. Base eval v3 từ lần đầu 19/20 lên **20/20** sau khi làm rõ thứ tự ưu tiên và ví dụ trong description của `clarify`; đo đủ 20 case, 0 lỗi provider. R12/M06 đều PASS, không làm hỏng các case từng PASS ở v1/v2. Kết quả v2 dùng làm mốc là 18/20, do QuanNH thực hiện.
- Xuất `analysis/v3.csv`, cập nhật dòng v3 trong `version_log.csv` và mục v3 trong `CHANGED_LOGS.md`; giữ run đầu và run cuối để truy vết. Viết báo cáo cá nhân, ghi rõ hỗ trợ từ Codex và cách kiểm chứng.
- Đã push các commit dưới đây lên `feat/DucLT-tool-tests`. Chưa có bằng chứng xác nhận PR/merge; chưa có eval nhóm/chat riêng chứng minh routing tới `stats`, chưa hoàn thành bảng tổng hợp riêng v0–v3 theo loại lỗi.

### Bằng chứng

- Test: [test_tools_todo.py](starter_v0/tests/test_tools_todo.py), [log pytest](starter_v0/analysis/duclt_pytest.txt).
- Tool mới: [stats/tool.py](starter_v0/tools/stats/tool.py), [stats/TOOL.md](starter_v0/tools/stats/TOOL.md), [registry](starter_v0/tools/__init__.py), [tools.yaml](starter_v0/artifacts/tools.yaml).
- Eval v3: [run đầu 19/20](starter_v0/runs/v3_B_base_openai_20261110T182541886906.json), [run cuối 20/20](starter_v0/runs/v3_B_base_openai_20261110T183553607506.json), [bảng từng case](starter_v0/analysis/v3.csv), [version log](starter_v0/artifacts/version_log.csv).
- Tài liệu: [phương pháp v3 trong changelog](CHANGED_LOGS.md), [báo cáo cá nhân](report/team/2A202604019_LaiTrongDuc.md).
- Commit: [fefb019 — test và stats](https://github.com/haiquanng/K5-L3B-DAY03-Ban5-ResearchAgentToolEval/commit/fefb019), [0d4b517 — v3 và bằng chứng eval](https://github.com/haiquanng/K5-L3B-DAY03-Ban5-ResearchAgentToolEval/commit/0d4b517), [bef3bb9 — báo cáo cá nhân](https://github.com/haiquanng/K5-L3B-DAY03-Ban5-ResearchAgentToolEval/commit/bef3bb9).

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
