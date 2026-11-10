# Báo cáo cá nhân — Nguyễn Văn Hải Quân - 2A202603994

## 1. Thông tin thành viên

- Họ tên: Nguyễn Văn Hải Quân
- MSSV: 2A202603994
- Email: 26ai.quannvh@vinuni.edu.vn

## 2. Phần việc phụ trách

Trưởng nhóm (GitHub `haiquanng`, nhật ký làm việc là `QuanNH`):
- Setup môi trường, chạy baseline v0 và phân tích lỗi (bảng B2).
- Vòng lặp prompt v1 và v2 (giả thuyết, chạy eval, ghi `version_log.csv`).
- Phân việc cho cả nhóm (thư mục `tasks/`) và review phần của hai bạn.
- Giao diện web (Next.js) và server FastAPI stream từng bước gọi tool; ô chọn version v0–v4.
- Bot Telegram để chat với agent; luồng xác nhận trước khi gửi.
- Kiểm tra tổng thể trước khi nộp: bằng chứng run, nhãn version, quét khóa bí mật.

## 3. Đóng góp cụ thể

- **Baseline v0 (13/20)** và phân loại lỗi từng case sai: tự đoán thay vì hỏi lại (R10, R11), gửi không xin phép (R12), việc ngoài phạm vi (R08, R14), chọn sai tool (R03, R13).
- **v1 (13 → 18/20):** gỡ chỉ dẫn xấu của bài mẫu (đoán mò, gửi ngay), thêm rule hỏi lại và xin xác nhận trước khi gửi. Giả thuyết đúng một phần; phát hiện thêm một lỗi mới (M02).
- **v2 (18/20, không tăng điểm):** thêm rule chọn công cụ và từ chối ngoài phạm vi. Ghi nhận trung thực: sửa được M02 nhưng làm hỏng M06, R12 vẫn sai.
- **Giao diện web + server:** chat thấy từng tool call (tên, tham số, kết quả, thời gian), hộp xác nhận cho `send`, lưu transcript cùng định dạng `chat.py`, che khóa bí mật trước khi ghi.
- **Bot Telegram** (`telegram_bot.py`): chat riêng với bot, chỉ các chat nằm trong danh sách cho phép mới dùng được; có 10 test không cần mạng.
- **Ô chọn version:** bản prompt và `tools.yaml` của từng version được đóng băng từ lịch sử git, có test so mã băm với `version_log.csv`.
- **Rà soát chất lượng bằng chứng:** phát hiện nhiều run gắn nhãn "v3" nhưng khác mã băm, nên đề xuất ghi nhận chính thức là v4 và chạy lại bằng provider `openai` (base 20/20, group 10/10). Chạy `--suite group` cho v3 trên bộ câu hỏi ban đầu: 7/10.
- **Bonus ≥ 4 tool mới:** thêm `calc`, `compare`, `dedupe` (cùng `stats` của Đức là 4 tool), mỗi tool có `TOOL.md`, đăng ký, test ba nhánh và tình huống eval riêng. Thêm tool làm group tụt 10/10 xuống 9/10 (G10), tôi ghi nhận trung thực (v5) rồi sửa bằng một dòng prompt (v6, group 10/10) mà không đổi tình huống của nhóm.
- **Bonus model local (Ollama):** chạy `llama3.2:3b` và `qwen2.5:7b` trên bộ base, tối ưu ba vòng (rút gọn prompt, few-shot, bớt tool) và đối chứng ngữ cảnh. Tìm ra từ log Ollama rằng prompt dài bị cắt do cửa sổ ngữ cảnh 4096 token; rút gọn đưa `qwen2.5:7b` từ 4/20 lên 14/20. Cũng xử lý sự cố model lặp vô hạn bằng cách giới hạn độ dài trả lời, và ghi nhận các vòng không cải thiện (few-shot làm tụt model 7B, bớt tool làm tụt model 3B).
- **Lỗi thật tìm được khi dùng thử:** agent gọi `send` thiếu `confirmed=true` rồi báo "đã gửi" sai; agent gọi `papers` với truy vấn rỗng (arXiv trả 400). Hai lỗi này được ghi trong `CHANGED_LOGS.md`.

## 4. Bằng chứng

- File/commit/PR (nhánh `main`): `c2242bf` (phân việc), `7907b76` (v0), `fcbf17b` (v1), `04eeefb` (v2), `9bdc927` (web + server), `596bf37` (bot Telegram), `60e9dd2` (chọn version), `26c929b` (run group v3), cùng commit v4 cuối cùng.
- Run: `starter_v0/runs/v0_B_base_openai_…`, `v1_…`, `v2_…`, `v4_B_base_openai_20261110T234636702818.json`, `v4_B_group_openai_20261110T234654785402.json`; nhật ký tổng hợp ở `CHANGED_LOGS.md`.
- Kiểm tra: `pytest` đạt 131 test, 0 lỗi, 0 skipped.
- AI/công cụ đã dùng và cách tự kiểm tra kết quả:
  - Công cụ: **Claude Code** (Anthropic), mô hình Sonnet. Dùng để viết và chỉnh code (`server.py`, `web/`, `telegram_bot.py`, test), đọc và phân tích log run, soạn tài liệu.
  - Cách tự kiểm tra: không tin lời giải thích của AI mà đối chiếu với dữ liệu: chạy lại eval và `pytest`; so mã băm file với `version_log.csv`; đọc transcript để xem tool thật sự được gọi gì; quét toàn bộ repo bằng giá trị thật của khóa trong `.env` để chắc không lộ khóa; thử cùng một câu hỏi trên v0 và v3 để thấy khác biệt.
  - Bài học về bảo mật: token bot Telegram từng bị dán vào khung chat với công cụ AI nên phải coi là đã lộ và cần thu hồi bằng `/revoke` rồi thay token mới.

## 5. Tự đánh giá

- **Làm tốt:** làm việc dựa trên bằng chứng (mỗi version có run, giả thuyết, mã băm); báo cáo trung thực cả khi version không tăng điểm (v2) và khi phát hiện nhãn version bị dùng sai; giao diện và bot dùng được để demo.
- **Hạn chế:** lỗi `papers` nhận truy vấn rỗng chưa được sửa ở mức tool và chưa có test hồi quy; bộ câu hỏi group đã được chỉnh câu chữ sau khi chạy v3 nên 10/10 của v4 cần đọc kèm ghi chú trong báo cáo nhóm.
- **Bài học:** điểm cao trên bộ eval cố định không đồng nghĩa agent hiểu mọi cách diễn đạt (ví dụ "đăng" so với "đưa" lên Telegram); nên đo lại bằng nhiều cách nói và ghi rõ bộ đề nào đã đổi.
