# Báo cáo cá nhân — 2A202604013_NguyenBaoTrung

## 1. Thông tin thành viên

- Họ tên: Nguyễn Bảo Trung
- MSSV: 2A202604013
- Email: nbtrungrhm@gmail.com
- Nhóm: Ban5 (Lớp L3B)

## 2. Phần việc phụ trách

- Xây dựng và hoàn thiện bộ test case đánh giá cho nhóm (`starter_v0/data/eval_group.json`) bao gồm cả single-turn và multi-turn.
- Phân tích nguyên nhân lỗi (Failure Analysis) của bản chạy baseline v0 và xây dựng giải pháp khắc phục (Bảng B2); chẩn đoán nguyên nhân lỗi dai dẳng của case R12 (cơ chế xác nhận yes/no trước khi gửi).
- Viết tài liệu giới thiệu agent (Phần A), hoàn thiện danh mục tool và soạn thảo các câu hỏi mẫu kiểm thử (A1, A2, A3).
- Cập nhật số liệu thực nghiệm v0, v1, v2, v3 vào các bảng B1, B3, B5a trong báo cáo nhóm.
- Chạy đánh giá bộ eval nhóm (`--suite group`), phân tích 3 case lỗi ban đầu (`G01`, `G03`, `G07`), cải tiến `system_prompt.md` và `tools.yaml` để đạt điểm tuyệt đối 10/10.
- Chạy kiểm tra hồi quy toàn diện 20 case Base Eval (`--suite base`) trên provider OpenRouter đạt 20/20 (100%).
- Quản lý đồng bộ git, xử lý merge conflict và tích hợp mã nguồn từ các thành viên trong nhóm (QuanNH, DucLT).

## 3. Đóng góp cụ thể

- **Thiết kế và tối ưu 10 test case nhóm (`eval_group.json`):**
  - 5 case single-turn: kiểm tra thiếu thông tin gọi `clarify`, kiểm tra cơ chế Human-in-the-Loop xin duyệt trước khi `send`, kiểm tra định tuyến tìm kiếm bài báo arXiv (`papers`), kiểm tra Guardrail từ chối tác vụ viết code (`no_tool: true`), và kiểm tra gọi tool mới `stats` của DucLT.
  - 5 case multi-turn: kiểm tra hỏi lại sau đó cung cấp đủ thông tin, kiểm tra sau khi user duyệt "đồng ý" thì thực sự gọi `send`, kiểm tra chuyển đổi tool từ Twitter sang web search giữ nguyên chủ đề, kiểm tra đính chính từ nghỉ phép sang báo ốm trong `policy`, và kiểm tra bài toán chia tiền logic không gọi tool thừa (`no_tool: true`).
  - *Chạy eval thực tế:* Đo lường ban đầu đạt 7/10; tiến hành phân tích sâu nguyên nhân gốc rễ (Root Cause Analysis) của 3 lỗi: `G01` (gọi rỗng/lookup khi thiếu chủ đề arXiv), `G03` (gọi lặp song song papers), và `G07` (chưa kích hoạt send khi user duyệt do thiếu bản nháp ngữ cảnh). Cùng tinh chỉnh `system_prompt.md` và `tools.yaml` đưa kết quả lên **10/10 PASS (100%)**.
- **Phân tích lỗi baseline v0 & case R12:** 
  - Rà soát và phân loại 7 case FAIL trong log `v0.csv`.
  - Phân tích nguyên nhân tại sao case `R12_confirm_before_send` ở v1 và v2 vẫn sai tham số (`response_type: text` thay vì `yes_no`): do xung đột giữa quy tắc "thiếu thông tin thì hỏi text" và "xin xác nhận trước khi gửi", cùng sự thiếu sót trong mô tả schema của `tools.yaml`.
- **Tích hợp và kiểm thử toàn diện:** 
  - Hợp nhất tool mới `stats` cùng 17 unit tests offline của DucLT vào nhánh làm việc, chạy toàn bộ test suite đạt **104 passed, 0 failed, 0 skipped**.
  - Thực hiện chạy lại bộ **20 case Base Eval** trên provider OpenRouter (`openai/gpt-4o-mini`), xác nhận **20/20 PASS (100% case_accuracy, 100% routing, 100% args, 100% multiturn)** không hề có lỗi hồi quy.

## 4. Bằng chứng

- **File / commit / PR:**
  - `starter_v0/data/eval_group.json`: Thiết kế và chuẩn hóa 10 test cases nhóm (commit `0cdeb72`, `5cdeca5`).
  - `report/team/group_report.md`: Hoàn thiện Phần A, Bảng B1, B2, B3, B5a (commit `c35c322`, `0cdeb72`, `aeecc7a`, `5cdeca5`).
  - `starter_v0/runs/`:
    - Run Group Eval 10/10: `v3_B_group_openrouter_20261110T191237962030.json` (commit `5cdeca5`).
    - Run Base Eval 20/20: `v3_B_base_openrouter_20261110T191959929397.json` (commit `a8361ba`).
  - `starter_v0/analysis/`: `group.csv` (10 rows pass), `v3.csv` (20 rows pass).
  - `tasks/TrungNB.md` & `TEAM.md`: Cập nhật checklist và thông tin thành viên (commit `fa5c001`, `c35c322`).
  - Merge nhánh nhóm: commit `fa5c001`, `7618298`, `b788f27`, `0e8ce8f`.
  - Đẩy code lên remote: branch `2A202604013_NguyenBaoTrung` trên GitHub.
- **AI / công cụ đã dùng và cách tự kiểm tra kết quả:**
  - **Công cụ AI:** Google Antigravity Agent (Gemini 3.8 Flash High) đóng vai trò trợ lý lập trình cặp (pair programming) theo phương thức tương tác hỏi - đáp từng bước (không tự ý sinh mã bừa bãi, sinh viên quyết định từng nội dung kỹ thuật).
  - **Nội dung thực tế đã làm việc cùng AI qua các phiên:**
    1. *Xử lý conflict Git:* Phân tích nguyên nhân conflict ở file `TEAM.md` khi merge `origin/main`, giải quyết conflict giữ trọn vẹn thông tin 3 thành viên và mục cá nhân.
    2. *Phân tích 7 case lỗi baseline v0 (Bảng B2):* Rà soát log `v0.csv`, chuẩn hóa giải pháp chặn đoán mò, áp dụng Human-in-the-Loop và thiết lập Guardrail `no_tool`.
    3. *Phân tích chuyên sâu case R12:* Chỉ ra nguyên nhân tại sao prompt dặn `yes_no` nhưng model vẫn gọi `text` (do model ưu tiên hỏi nội dung thiếu trước, và schema `tools.yaml` chưa có bảng ưu tiên intent).
    4. *Thiết kế và chạy thử nghiệm Eval nhóm:*
       - Khởi tạo 10 test case trong `data/eval_group.json`.
       - Lần chạy đầu đạt 7/10: AI hỗ trợ phân tích log run JSON chỉ ra 3 lỗi bản chất:
         - `G01`: Model gọi `papers(query='')` hoặc `lookup` vì thiếu quy tắc chặn tìm bài báo khi không có chủ đề.
         - `G03`: Model gọi lặp song song 2 lần `papers` do câu hỏi ghép có từ "và".
         - `G07`: Model gọi tiếp `clarify` vì kịch bản chưa có đoạn text nháp được duyệt trước.
       - Cùng AI thảo luận giải pháp: siết chặt mô tả `papers` và `send` trong `tools.yaml`, bổ sung chỉ dẫn arXiv trong `system_prompt.md`, và tinh chỉnh câu lệnh query rõ nghĩa.
       - Chạy lại đạt **10/10 PASS**.
    5. *Chạy kiểm tra hồi quy Base Eval:* Chạy toàn bộ 20 case base trên OpenRouter, kiểm tra xác nhận **20/20 PASS**, parse log CSV và push đồng bộ lên GitHub.
  - **Cách tự kiểm tra kết quả (Verification):**
    - Kiểm tra schema JSON: Dùng Python `json.load()` xác thực `data/eval_group.json` và toàn bộ các file run JSON trong `starter_v0/runs/`.
    - Kiểm tra tính hợp lệ của benchmark: Mọi run file sử dụng làm bằng chứng đều thỏa mãn `provider_error_cases == 0` và `measured_cases == total_cases`.
    - Chạy Unit Test `pytest`: Toàn bộ suite **104 passed, 0 failed, 0 skipped**.
    - Kiểm tra bảo mật: Rà soát `git status`, `.gitignore` và `git diff` tuyệt đối không commit file `.env`, API key hay token Telegram.

## 5. Tự đánh giá

- Hoàn thành đầy đủ 100% các đầu việc được phân công đúng thời hạn và đảm bảo chất lượng kỹ thuật.
- Đánh giá đóng góp: Hoàn thành tốt nhiệm vụ (mức A).
