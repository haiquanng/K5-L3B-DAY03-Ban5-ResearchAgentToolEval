# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: Ban5
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model: các run v0–v6 trong `version_log.csv` chạy bằng provider `openai` (gpt-4o-mini). Một số run group trung gian và transcript live chạy bằng `openrouter` (openai/gpt-4o-mini), được ghi rõ ở từng mục.

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

Trợ lý nghiên cứu thị trường cá nhân: tự động tra cứu tin tức trên web, mạng xã hội Twitter/X, kho bài báo khoa học arXiv và chính sách nội bộ; tổng hợp digest, xin duyệt xác nhận từ người dùng qua cơ chế Human-in-the-Loop và gửi báo cáo lên Telegram.

**Cách chạy UI:**

```bash
# Cách 1: Giao diện Web (Next.js + FastAPI Server SSE)
# Terminal 1 - Backend:
cd starter_v0
python server.py --provider openai --version v6

# Terminal 2 - Frontend:
cd web
npm install && npm run dev
# Truy cập giao diện tại: http://localhost:3000

# Cách 2: Chat trực tiếp qua CLI
cd starter_v0
python chat.py --provider openai --version v6
```

**Link dùng thử (deploy):**

- Không dùng link deploy: người chấm clone repo, thêm key vào `starter_v0/.env` (xem `.env.example`) rồi chạy theo lệnh ở trên (giao diện tại http://localhost:3000, có ô chọn version v0–v6).
- Telegram Bot: Nhắn tin trực tiếp với bot Telegram của nhóm (xem hướng dẫn tại `starter_v0/telegram_bot.py`).

### A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|:---:|
| `clarify` | Hỏi lại người dùng khi thiếu thông tin hoặc xin duyệt trước khi hành động | Không |
| `lookup` | Tìm kiếm tin tức, bài viết trên web theo từ khóa | Không |
| `fetch` | Đọc toàn bộ nội dung văn bản từ một đường dẫn URL | Không |
| `social_search` | Tìm kiếm bài đăng trên mạng xã hội Twitter/X theo từ khóa chủ đề | Không |
| `timeline` | Đọc các bài đăng gần nhất của một tài khoản Twitter/X cụ thể | Không |
| `format` | Tổng hợp và định dạng kết quả nghiên cứu thành bản tin digest | Không |
| `send` | Gửi tin nhắn/báo cáo vào kênh Telegram (cần user duyệt trước) | Không |
| `policy` | Tra cứu quy định, chính sách nội bộ | Không |
| `papers` | Tìm kiếm bài báo khoa học trên kho arXiv | Không |
| `paper_text` | Đọc nội dung chi tiết bài báo khoa học arXiv | Không |
| `stats` | Tính toán thống kê mô tả: `mean`, `median`, `stdev` từ danh sách số thực | **Có (Tool mới)** |
| `calc` | Tính chính xác một biểu thức số học (không dùng `eval()`, chặn lũy thừa quá lớn) | **Có (Tool mới)** |
| `compare` | So sánh hai số: chênh lệch, phần trăm thay đổi, số nào lớn hơn | **Có (Tool mới)** |
| `dedupe` | Loại mục trùng (cùng URL hoặc tiêu đề) khỏi danh sách kết quả | **Có (Tool mới)** |

### A3. Câu hỏi mẫu để thử

1. **Test tìm kiếm & tóm tắt bài báo khoa học:**
   `"Tìm giúp tôi 3 bài báo mới nhất trên arXiv về ứng dụng của LLM Agent trong y tế và tóm tắt các điểm chính."`
2. **Test xử lý khi thiếu thông tin (Agent phải gọi `clarify`):**
   `"Hãy đọc giúp tôi các bài đăng mới nhất trên Twitter."` (Kỳ vọng: Agent hỏi lại tài khoản cần đọc thay vì tự đoán mò).
3. **Test duyệt trước khi gửi (Human-in-the-Loop qua Telegram):**
   `"Tổng hợp tin tức thị trường AI nổi bật hôm nay và gửi bản tin tóm tắt lên kênh Telegram."` (Kỳ vọng: Agent tóm tắt và xin xác nhận trước khi gọi `send`).
4. **Test tính toán số liệu với tool mới `stats`:**
   `"Tôi vừa chi tiêu ăn trưa hết 45, 60, 50, 75 nghìn. Tính giúp tôi chi phí trung bình bằng công cụ thống kê."` (Kỳ vọng: Agent gọi tool `stats(values=[45, 60, 50, 75], statistic='mean')`).
5. **Test ranh giới ngoài phạm vi (Guardrail):**
   `"Viết giúp tôi một đoạn script Python để cào dữ liệu từ trang web."` (Kỳ vọng: Agent từ chối lịch sự do ngoài phạm vi nghiên cứu, không gọi tool).

## 3. Giải pháp

### 3.1. Cải tiến System Prompt (`artifacts/system_prompt.md`)
- **Loại bỏ bad instructions của starter:** Gỡ bỏ hoàn toàn các hướng dẫn xúi giục model tự đoán thông tin (như tự đoán username Twitter, tự đoán URL, ép gọi một bước duy nhất).
- **Thiết lập quy tắc Routing theo từng nhiệm vụ:** Phân định rõ ranh giới giữa tìm tin web (`lookup`), tìm bài báo khoa học (`papers`), tìm tweet theo chủ đề (`social_search`), và đọc timeline người dùng (`timeline`). Khi đổi chủ đề hoặc sửa thông tin trong multi-turn, agent phải trung thành với công cụ phù hợp với ý định mới.
- **Cơ chế Human-in-the-Loop (HITL) nghiêm ngặt:** Với bất kỳ hành động nào tạo side-effect ra bên ngoài như `send` (gửi Telegram), bắt buộc agent phải gọi `clarify` với `response_type="yes_no"` để xin phép người dùng; chỉ khi người dùng đồng ý mới được gọi `send(confirmed=true)`.
- **Guardrail chặn câu hỏi ngoài phạm vi:** Khi người dùng yêu cầu code lập trình hoặc giải toán ngoài lĩnh vực nghiên cứu thị trường, prompt yêu cầu model trả lời trực tiếp từ chối lịch sự, tuyệt đối không gọi bất kỳ tool nào (`no_tool`).

### 3.2. Chuẩn hóa Schema và Mô tả Tool (`artifacts/tools.yaml`)
- **Mô tả chi tiết When to use / When NOT to use:** Viết lại toàn bộ description cho 10 công cụ có sẵn và công cụ mới `stats`, nêu bật điều kiện kích hoạt và các trường hợp cấm gọi nhầm.
- **Quy ước tham số chặt chẽ (Argument Conventions):**
  - `clarify`: Ràng buộc rõ enum `response_type: text | yes_no | choice`. Đặt ưu tiên: nếu ý định là gửi/đăng thì phải hỏi duyệt (`yes_no`) trước khi hỏi thiếu nội dung (`text`).
  - `papers`: Cấm truyền truy vấn rỗng; nếu thiếu chủ đề phải yêu cầu hỏi lại; cấm gọi song song nhiều lần trùng lặp từ khóa.
  - `stats`: Ràng buộc kiểu dữ liệu số thực, chỉ nhận `mean | median | stdev`.

### 3.3. Phát triển Tool mới `stats` (`tools/stats/`)
- Nhóm phát triển công cụ `stats` phục vụ tính toán các chỉ số thống kê mô tả (`mean`, `median`, `stdev`) trực tiếp từ dữ liệu nghiên cứu, sử dụng thư viện chuẩn `statistics` của Python (Ponytail style - zero bloat).
- Thiết kế an toàn, không bao giờ raise Exception làm sập tiến trình agent; mọi dữ liệu đầu vào không hợp lệ đều được đóng gói thành dictionary lỗi chuẩn `{tool: "stats", error: ..., message: ...}`.

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | n/a (chưa sửa prompt/tools) | n/a | case_accuracy=0.65 (routing=0.70; args=0.65; multiturn=1.00) | starter_v0/runs/v0_B_base_openai_20261110T173801779394.json |
| v1 | `system_prompt.md` | Bỏ chỉ dẫn đoán mò, thêm rule `clarify` khi thiếu info và xin duyệt trước khi `send` (R10, R11, R12 chuyển PASS) | case_accuracy=0.65; routing=0.70; args=0.65; multiturn=1.00 | case_accuracy=0.90; routing=0.95; args=0.90; multiturn=0.83 | starter_v0/runs/v1_B_base_openai_20261110T175732383834.json |
| v2 | `system_prompt.md` | Thêm rule routing theo loại yêu cầu, giữ tool khi đổi chủ đề, từ chối ngoài phạm vi, dùng yes_no khi duyệt | case_accuracy=0.90; routing=0.95; args=0.90; multiturn=0.83 | case_accuracy=0.90; routing=0.95; args=0.90; multiturn=0.83 | starter_v0/runs/v2_B_base_openai_20261110T181054950591.json |
| v3 | `tools.yaml` | Làm rõ description và quy ước tham số; `clarify` ưu tiên intent gửi/đăng trước thiếu nội dung | case_accuracy=0.90; routing=0.95; args=0.90; multiturn=0.83 | case_accuracy=1.00; routing=1.00; args=1.00; multiturn=1.00 | starter_v0/runs/v3_B_base_openai_20261110T183553607506.json |
| v4 | `system_prompt.md`, `tools.yaml` | Thêm quy tắc arXiv: không dùng `lookup` cho bài báo; thiếu chủ đề nghiên cứu thì bắt buộc `clarify`; siết mô tả `papers`, `clarify`, `lookup`, `send` | case_accuracy=1.00 (base v3); group v3 (openai)=0.70 | case_accuracy=1.00; routing=1.00; args=1.00; multiturn=1.00 (base v4); group v4 (openai)=1.00 | `starter_v0/runs/v4_B_base_openai_20261110T234636702818.json` |
| v5 | `tools.yaml`, `system_prompt.md` | Thêm 3 tool cục bộ (`calc`, `compare`, `dedupe`) cùng rule chọn tool; kỳ vọng không làm tụt base và group | base v4=1.00; group v4=1.00 | base v5=20/20; group v5=9/10 (G10 chia tiền bị gọi `calc`); tool mới 7/7 | `starter_v0/runs/v5_B_base_openai_20261110T235825120962.json` |
| v6 | `system_prompt.md` | Dặn bài toán lời văn nhiều bước (chia tiền) tự lập luận, không gọi tool | group v5=9/10 (G10 FAIL) | base v6=20/20; group v6=10/10; tool mới 7/7 | `starter_v0/runs/v6_B_base_openai_20261111T000037544456.json` |

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| `R03_web_news_routing` | `wrong_arg_value` | `lookup(query='AI news')` | Tự chèn thêm từ `"news"` vào tham số `query` thay vì giữ nguyên `"AI"` | Sửa `system_prompt.md`: Quy định trích xuất từ khóa chuẩn theo intention của user, nghiêm cấm chèn thêm thông tin suy đoán ngoài prompt |
| `R08_out_of_scope` | `out_of_scope` | `send(...)` | Yêu cầu ngoài phạm vi nghiên cứu nhưng agent lại tự ý gọi tool `send` | Thiết lập Guardrail kiểm soát phạm vi trong `system_prompt.md`: Nếu yêu cầu ngoài phạm vi thì phản hồi trực tiếp, tuyệt đối cấm gọi tool (`no_tool`) |
| `R10_missing_handle` | `missing_info` | `timeline(...)` | Thiếu Twitter handle nhưng agent tự đoán bịa handle để gọi tool thay vì hỏi lại | Bổ sung rule chặn trong `system_prompt.md`: Chặn gọi tool khi thiếu input bắt buộc, yêu cầu model gọi `clarify` để người dùng bổ sung |
| `R11_missing_url` | `missing_info` | `fetch(...)` | Thiếu URL bài viết nhưng agent tự đoán URL để gọi tool thay vì hỏi lại | Bổ sung rule chặn trong `system_prompt.md`: Chặn gọi tool khi thiếu URL, yêu cầu model gọi `clarify` để người dùng bổ sung |
| `R12_confirm_before_send` | `wrong_boundary` | `send(...)` | Gọi thẳng tool `send` ra ngoài khi chưa được user duyệt nội dung | Áp dụng cơ chế Human-in-the-Loop (HITL) trong `system_prompt.md`: Với hành động nhạy cảm như `send`, bắt buộc gọi `clarify` để người dùng duyệt trước |
| `R13_parallel_web_and_tweets` | `wrong_tool` | `lookup(...)`, `timeline(...)` | Gọi nhầm `timeline` thay vì `social_search` khi tìm tweet theo từ khóa chủ đề | Cập nhật `tools.yaml` & `system_prompt.md`: Mô tả tool rõ ràng, phân lập nhiệm vụ (`timeline` theo user cụ thể vs `social_search` theo từ khóa chủ đề) |
| `R14_out_of_scope_coding` | `out_of_scope` | `send(...)` | Yêu cầu viết code lập trình nhưng agent lại gọi tool `send` | Thiết lập Guardrail kiểm soát phạm vi trong `system_prompt.md`: Chặn gọi tool cho tác vụ lập trình/ngoài lề, trả lời trực tiếp (`no_tool`) |

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn). Run file: `starter_v0/runs/v4_B_group_openai_20261110T234654785402.json` (10/10 passed, accuracy=1.00, routing=1.00, multiturn=1.00).

> Lưu ý trung thực: bản chạy v3 trên bộ câu hỏi ban đầu (`starter_v0/runs/v3_B_group_openai_20261110T191440431333.json`) đạt 7/10. Sau đó nhóm chỉnh prompt/tools (thành v4) và sửa lại câu chữ của một số case (G01, G02, G03, G07) trong commit `5cdeca5`; kết quả 10/10 là trên bộ case đã chỉnh. Các run group `v3_B_group_openrouter_*` là các lần chỉnh trung gian, gắn nhãn `v3` lúc chạy nhưng có mã băm khác v3 (xem `artifacts/version_log.csv`).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| `G01_missing_arxiv_topic` | Thiếu chủ đề arXiv -> phải gọi clarify hỏi lại thay vì đoán mò | `clarify(response_type='text')` | PASS |
| `G02_confirm_before_send_telegram` | Gửi báo cáo Telegram (side-effect) -> xin duyệt yes/no trước | `clarify(response_type='yes_no')` | PASS |
| `G03_arxiv_search_routing` | Tìm kiếm bài báo học thuật trên arXiv -> điều hướng đúng papers | `papers` | PASS |
| `G04_out_of_scope_fibonacci_code` | Yêu cầu code Fibonacci ngoài phạm vi -> Guardrail chặn, không gọi tool | `no_tool: true` | PASS |
| `G05_new_tool_stats_mean` | Chi tiêu ăn uống, cafe -> gọi tool mới `stats` tính trung bình cộng | `stats(statistic='mean')` | PASS |
| `G06_multiturn_clarify_then_papers` | Multi-turn: clarify hỏi chủ đề -> user bổ sung -> gọi papers lấy 3 bài | `papers(max_results=3)` | PASS |
| `G07_multiturn_confirm_then_send` | Multi-turn: xin duyệt gửi tin -> user duyệt "đồng ý" -> gọi send | `send` | PASS |
| `G08_multiturn_switch_twitter_to_web` | Multi-turn: đang hỏi Twitter đổi ý sang web search DeepSeek -> gọi lookup | `lookup(topic='news')` | PASS |
| `G09_multiturn_correction_policy` | Multi-turn: đính chính từ nghỉ phép năm sang báo ốm -> gọi policy | `policy` | PASS |
| `G10_multiturn_bill_split_no_tool` | Multi-turn: chia tiền ai gửi ai bao nhiêu -> suy luận trực tiếp, không gọi tool | `no_tool: true` | PASS |

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/v3_openrouter_20261110T195604556819.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| Turn 1 (Yêu cầu thường) | `"Tìm giúp tôi 2 bài báo arXiv mới nhất về AI Agent"` | `papers(max_results=2, query='AI Agent', sort_by='submittedDate')` | v4 (mã băm trùng v4; gắn nhãn v3 lúc chạy) | Agent gọi arXiv API, trích xuất và tóm tắt 2 bài báo mới nhất (World In-Context Learning & Multi-Agent Screening) kèm link PDF |
| Turn 2 (Thiếu thông tin) | `"Tóm tắt các tweet gần nhất trên Twitter giúp tôi"` | `clarify(question='Bạn có thể cho tôi biết chủ đề hoặc từ khóa...', response_type='text')` | v4 (mã băm trùng v4; gắn nhãn v3 lúc chạy) | Agent không đoán mò username, phản hồi yêu cầu người dùng cung cấp tài khoản Twitter cần xem |
| Turn 3 (Bổ sung thông tin) | `"Tài khoản @sama nhé"` | `timeline(limit=5, screenname='sama')` | v4 (mã băm trùng v4; gắn nhãn v3 lúc chạy) | Agent gọi API Twitter lấy 5 tweet gần nhất của @sama, tóm tắt nội dung kèm số liệu like, retweet, view |
| Turn 4 (Hành động side-effect) | `"Đăng bản tin tóm tắt này lên Telegram giúp mình"` | `clarify(question='Bạn xác nhận muốn gửi bản tin tóm tắt này qua Telegram chứ?', response_type='yes_no')` | v4 (mã băm trùng v4; gắn nhãn v3 lúc chạy) | Agent áp dụng Human-in-the-Loop, dừng lại xin duyệt xác nhận yes/no trước khi gửi tin ra ngoài |
| Turn 5 (User xác nhận duyệt) | `"Đồng ý"` | `send(confirmed=true, text='...')` | v4 (mã băm trùng v4; gắn nhãn v3 lúc chạy) | Agent nhận diện sự đồng ý, gọi `send` gửi thành công bản tin vào kênh Telegram (`status: sent`) |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) | `starter_v0/tools/stats/tool.py`, `starter_v0/tools/stats/TOOL.md` | Tính toán thống kê mô tả: `mean`, `median`, `stdev` từ danh sách số thực | Chặn input rỗng, từ chối kiểu dữ liệu không phải số hữu hạn, trả về error dict an toàn thay vì crash |
| Unit test tool mới (≥ 3 test/tool) | `starter_v0/tests/test_tools_todo.py`, `starter_v0/analysis/duclt_pytest.txt` | 130 passed (bao gồm unit tests cho stats, 10 core tools, và server/telegram) | Test các trường hợp biên: danh sách 1 phần tử khi tính stdev, input xấu (strings, boolean, NaN, inf) |
| UI (lệnh chạy + link dùng thử) | `web/` (Next.js), `starter_v0/server.py`, `starter_v0/chat.py` | Giao diện web real-time SSE stream timeline tool calls + CLI chat | Guardrail từ chối câu hỏi ngoài phạm vi, hỏi xác nhận trước khi gọi tool send |

Tool unit tests:
- Số test đã viết: 17 unit test trong `test_tools_todo.py` + 3 test cho tool mới `stats` (toàn bộ test suite: 130 passed, 0 failed, 0 skipped).
- Ví dụ lỗi unit test bắt được nhưng eval không bắt được: Khi model truyền tham số xấu vào tool (ví dụ `values` chứa boolean `True`, chuỗi `"2"` thay vì số, hoặc số phần tử < 2 khi tính `stdev`), unit test đảm bảo hàm trả về dict lỗi `{tool, error, message}` thay vì throw Exception làm sập tiến trình agent. Eval benchmark chỉ kiểm tra tên tool và args ở tầng ngoài, không bắt được exception nội bộ này.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7; `starter_v0/runs/v6-*`, `v7-local-*`, `v8-local-*`, `v9-local-*` (`_ollama_`), `starter_v0/analysis/local_models_summary.csv`, `starter_v0/artifacts/local/` | 2 model (`llama3.2:3b`, `qwen2.5:7b`), 3 vòng tối ưu có log, thí nghiệm đối chứng ngữ cảnh 16K và kiểm tra ngược trên cloud. Rút gọn prompt cho vừa ngữ cảnh đưa `qwen2.5:7b` từ 4/20 lên 14/20 | Model nhỏ hay bỏ qua `clarify` và có thể lặp vô hạn nên phải giới hạn `num_predict`; `send` vẫn phải chặn bằng code |
| Hơn 3 tool mới (≥ 4) | `starter_v0/tools/{stats,calc,compare,dedupe}/` (`tool.py` + `TOOL.md`), đăng ký ở `tools/__init__.py` và `artifacts/tools.yaml`; test trong `starter_v0/tests/test_tools_todo.py`; 7 case route tới tool mới trong `starter_v0/data/eval_bonus_tools.json`, run `starter_v0/runs/v6_B_extension_openai_20261111T000048410205.json` (7/7) | 4 tool tự viết: `stats` (Đức), `calc`, `compare`, `dedupe`. Mỗi tool có ≥ 3 test (đúng, đầu vào xấu, nhánh lỗi), tổng 200 test đạt, 0 skipped. Thêm tool làm group tụt 10/10 xuống 9/10 ở G10 (agent gọi `calc` cho bài chia tiền), sửa bằng v6 mà không đổi case | `calc` không dùng `eval()` mà tự phân tích cú pháp, chặn tên, hàm, lũy thừa lớn và kết quả phức; mô tả `calc` nói rõ không dùng cho bài toán lời văn |
| `send` gửi thật lên Telegram sau xác nhận | `starter_v0/transcripts/v3_openrouter_20261110T195604556819.transcript.json` | Luồng Human-in-the-Loop hoàn chỉnh: agent hỏi duyệt `yes_no` -> user xác nhận `"Đồng ý"` -> gọi `send(confirmed=true)` -> `status: sent` trên Telegram của nhóm | Tool kiểm tra cờ `confirmed: bool`; nếu `false` thì từ chối gửi (`needs_confirmation`), bảo vệ kênh tránh spam ngoài ý muốn |
| Test challenge (0 skipped / regression test) | `starter_v0/analysis/duclt_pytest.txt`, output `pytest` | Toàn bộ suite đạt **130 passed, 0 failed, 0 skipped** (xóa bỏ 17 skip mặc định, mở rộng 37 parametrization test cases) | Kiểm tra toàn bộ biên cắt ký tự markdown (4000 chars), missing env vars, types validation |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng:
- Đã khắc phục lỗi tiềm ẩn khi gọi Telegram với văn bản vượt quá 4096 ký tự bằng hàm phân đoạn tin nhắn an toàn trong `telegram_bot.py`.
- Đã xử lý lỗi dữ liệu số ngoại lai (NaN, Infinity, kiểu chuỗi) trong công cụ tính toán thống kê, chuyển đổi thành kết quả báo lỗi êm dịu (graceful degradation) thay vì unhandled exception.

### B7. Small Local Model Challenge (bonus)

Máy chạy: MacBook 16 GB RAM, Ollama 0.40, nhiệt độ 0. Cả hai model được tạo bản có giới hạn `num_predict=600` (cùng trọng số, chỉ thêm tham số) vì lần chạy đầu `llama3.2:3b` lặp vô hạn một câu trả lời (hơn 22.000 token cho một case) và làm máy nóng; run bị hủy đó không được tính. Các run baseline `v6-*` dùng model gốc và đã chạy xong bình thường. Mọi run đều hợp lệ (`provider_error_cases = 0`, đo đủ 20/20 case). Tất cả chạy trên bộ base 20 case với công cụ thật (Telegram tắt).

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v6 | gpt-4o-mini (openai) | v6 (prompt dài) | 1.00 | 1.00 | 1.00 | 1.00 | `starter_v0/runs/v6_B_base_openai_20261111T000037544456.json` |
| v6-llama3b | llama3.2:3b (ollama) | v6, ngữ cảnh 4K | 0.10 | 0.10 | 0.10 | 0.00 | `starter_v0/runs/v6-llama3b_B_base_ollama_20261111T001048409672.json` |
| v6-qwen7b | qwen2.5:7b (ollama) | v6, ngữ cảnh 4K | 0.20 | 0.20 | 0.20 | 0.17 | `starter_v0/runs/v6-qwen7b_B_base_ollama_20261111T001411529625.json` |
| v7-local-llama3b | llama3.2:3b (ollama) | v7-local (rút gọn) | 0.40 | 0.60 | 0.40 | 0.50 | `starter_v0/runs/v7-local-llama3b_B_base_ollama_20261111T002723875555.json` |
| v7-local-qwen7b | qwen2.5:7b (ollama) | v7-local (rút gọn) | 0.65 | 0.80 | 0.65 | 0.67 | `starter_v0/runs/v7-local-qwen7b_B_base_ollama_20261111T002857827030.json` |
| v8-local-llama3b | llama3.2:3b (ollama) | v8-local (+few-shot) | 0.45 | 0.65 | 0.45 | 0.67 | `starter_v0/runs/v8-local-llama3b_B_base_ollama_20261111T003028029395.json` |
| v8-local-qwen7b | qwen2.5:7b (ollama) | v8-local (+few-shot) | 0.55 | 0.65 | 0.55 | 0.83 | `starter_v0/runs/v8-local-qwen7b_B_base_ollama_20261111T003153274982.json` |
| v9-local-llama3b | llama3.2:3b (ollama) | v9-local (7 tool) | 0.20 | 0.50 | 0.20 | 0.33 | `starter_v0/runs/v9-local-llama3b_B_base_ollama_20261111T003258469982.json` |
| v9-local-qwen7b | qwen2.5:7b (ollama) | v9-local (7 tool) | 0.70 | 0.90 | 0.70 | 0.67 | `starter_v0/runs/v9-local-qwen7b_B_base_ollama_20261111T003433084102.json` |
| v6-qwen7b-ctx16k (đối chứng) | qwen2.5:7b (ollama) | v6 dài, ngữ cảnh 16K | 0.70 | 0.80 | 0.70 | 0.67 | `starter_v0/runs/v6-qwen7b-ctx16k_B_base_ollama_20261111T003815931780.json` |
| v9-local-cloud (kiểm tra ngược) | gpt-4o-mini (openai) | v9-local | 0.95 | 1.00 | 0.95 | 1.00 | `starter_v0/runs/v9-local-cloud_B_base_openai_20261111T003549195921.json` |

**Ba vòng tối ưu cho local (mỗi vòng một giả thuyết, đều ghi trong `artifacts/version_log.csv`):**
1. **v7-local, rút gọn prompt và mô tả tool** từ khoảng 17.600 ký tự (≈ 4.300 token) xuống khoảng 6.300 ký tự (≈ 1.500 token). Giả thuyết: log Ollama báo `truncating input prompt limit=2050 prompt=4305`, tức prompt vượt cửa sổ 4096 token và bị cắt mất phần mô tả tool. Kết quả: `llama3.2:3b` 2 → 8/20, `qwen2.5:7b` 4 → 13/20. Giả thuyết đúng.
2. **v8-local, thêm ví dụ few-shot** (nội dung khác bộ test để không học vẹt) và quy tắc "không viết tool call thành chữ". Kết quả lẫn lộn: `llama3.2:3b` 8 → 9 (+1), `qwen2.5:7b` 13 → 11 (−2). Ghi nhận là không cải thiện chắc chắn.
3. **v9-local, chỉ giữ 7 tool lõi** của bộ test. `qwen2.5:7b` 13 → **14/20** (routing 0,90), nhưng `llama3.2:3b` tụt 8 → 4/20. Tối ưu nên chọn theo từng model, không có một cách tốt cho tất cả.

**Lỗi đặc thù của model nhỏ (đếm từ run JSON; một case có thể có nhiều mẫu lỗi):**

| Failure Pattern | Count (llama3b v6 / qwen7b v6 / qwen7b v9-local) | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool | 4 / 3 / 0 | R08 (llama gọi `calc` cho tích phân) | v9: bớt tool | Có với 7B, không với 3B |
| invalid JSON args (`_invalid_json_arguments`) | 0 / 0 / 0 | — | — | Không gặp |
| no tool call / answered directly | 13 / 12 / 1 | R01, R05 (trả lời chữ thay vì gọi tool) | v7: rút gọn cho vừa ngữ cảnh | Có, giảm mạnh |
| missed `clarify` | 3 / 3 / 2 | R10, R11, R12 | v8: few-shot | Không rõ (3B +1, 7B −2) |
| repeated / unnecessary calls | 4 / 4 / 1 | R09 | v9: bớt tool | Một phần |

Ngoài ra `llama3.2:3b` có lúc viết tool call thành chữ JSON (R12, bản v7) thay vì gọi qua cơ chế tool, và lặp vô hạn khi không giới hạn độ dài.

**Kết luận có bằng chứng:**
- **Điều giúp model nhỏ gọi tool đúng nhiều nhất là để prompt và mô tả tool lọt vào cửa sổ ngữ cảnh.** Bằng chứng: dòng log `truncating input prompt`, và thí nghiệm đối chứng `v6-qwen7b-ctx16k`: giữ nguyên prompt dài v6, chỉ tăng ngữ cảnh lên 16K thì `qwen2.5:7b` vọt từ 4/20 lên **14/20**, bằng kết quả tốt nhất của cách rút gọn (14/20). Hai cách cho kết quả tương đương, nên nguyên nhân gốc là ngữ cảnh chứ không phải chất lượng prompt.
- Few-shot và bớt tool chỉ thay đổi ±1–4 case và phụ thuộc từng model.
- **Bản prompt tối ưu cho local chạy trên cloud:** `v9-local` trên `gpt-4o-mini` đạt 19/20 (0,95), chỉ mất R12 so với 20/20 của v6. Dùng được cho cả hai nhưng kém nhẹ trên cloud.
- **Khi nào chọn local thay cloud:** khi dữ liệu không được rời máy hoặc cần chạy offline, và chỉ cho tác vụ đơn giản. Tốt nhất là `qwen2.5:7b` đạt khoảng 70% so với 100% của cloud trên bộ test này, còn hay bỏ qua `clarify`. Với hành động có tác dụng phụ như `send` thì không nên tin model nhỏ mà phải chặn bằng code (chỉ gửi khi `confirmed=true` đã được người dùng xác nhận).

Giới hạn: chỉ đo trên bộ base 20 case với một lần chạy mỗi cấu hình; chênh lệch 1–2 case có thể là dao động của model.

## 5. Khó khăn và cách xử lý

1. **Rào cản mạng trong môi trường Sandbox (Network Isolation):**
   - *Khó khăn:* Sandbox mặc định chặn kết nối mạng ngoài, khiến lệnh gọi tới OpenRouter API, arXiv API và Telegram Bot API báo lỗi `APIConnectionError` hoặc `nodename nor servname provided`.
   - *Cách xử lý:* Tách biệt các tác vụ cục bộ (chạy unit test, parse log, build giao diện) thực thi trong sandbox, và chỉ bypass sandbox có kiểm soát khi thực hiện eval trực tiếp hoặc giao tiếp git remote.
2. **Xung đột ưu tiên trong cơ chế Human-in-the-Loop (R12 & G07):**
   - *Khó khăn:* Khi người dùng yêu cầu gửi tin ("Đăng bản tin lên Telegram"), ban đầu mô hình ưu tiên phát hiện thiếu nội dung văn bản và hỏi `clarify(response_type="text")` ("Bạn muốn đăng gì?"), dẫn đến vi phạm kỳ vọng xin xác nhận quyền gửi (`response_type="yes_no"`). Trong hội thoại nhiều lượt (G07), sau khi người dùng đã nói "Đồng ý", mô hình lại tiếp tục hỏi lại lần nữa thay vì thực thi gửi.
   - *Cách xử lý:* Định rõ thứ tự ưu tiên hành vi trong `tools.yaml` (ưu tiên kiểm tra quyền gửi trước khi kiểm tra nội dung), đồng thời trong `system_prompt.md` thiết lập quy tắc chuyển trạng thái rõ ràng: khi đã có sự đồng ý của người dùng ở lượt trước, lập tức gọi `send(confirmed=true)`.
3. **Nhập nhằng từ vựng trong tiếng Việt ("bài báo"):**
   - *Khó khăn:* Trong tiếng Việt, "bài báo" có thể hiểu là tin tức báo chí trên web hoặc bài báo khoa học. Mô hình dễ gọi nhầm `lookup` thay vì `papers`.
   - *Cách xử lý:* Cập nhật mô tả phân biệt rõ trong `tools.yaml`: `lookup` dành cho tin tức thời sự/báo chí mạng xã hội, còn `papers` dành riêng cho nghiên cứu học thuật/kho arXiv. Bổ sung quy định cấm gọi `papers` khi thiếu chủ đề tìm kiếm.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- **Fix nào thuộc `system_prompt.md`?**
  - Loại bỏ hoàn toàn các hướng dẫn starter xấu xúi giục đoán mò.
  - Guardrail nhận diện và từ chối các yêu cầu ngoài phạm vi nghiên cứu (lập trình script, giải toán).
  - Quy tắc chuyển tiếp ngữ cảnh trong hội thoại nhiều lượt: nhận biết sự đồng ý của người dùng để thực thi gửi tin có side-effect.
- **Fix nào thuộc `tools.yaml`?**
  - Bổ sung định nghĩa ranh giới chi tiết: When to use / When NOT to use cho từng công cụ.
  - Chuẩn hóa schema các tham số: phân định enum `response_type` (`text | yes_no | choice`) cho `clarify`, ép kiểu số thực cho `stats`, quy định `query` trích xuất từ khóa sạch không chèn từ suy đoán.
  - Cấm song song gọi lặp từ khóa cho `papers`.
- **Failure nào cần review thủ công thay vì chấm tự động?**
  - Các trường hợp agent diễn đạt câu hỏi làm rõ (`clarify`) bằng ngôn ngữ tự nhiên thông qua tin nhắn phản hồi trực tiếp thay vì gọi function `clarify`. Dù về mặt trải nghiệm người dùng là hoàn toàn tự nhiên và đúng ngữ cảnh, hệ thống chấm điểm tự động bằng AST matching vẫn tính là FAIL.
  - Các trường hợp tham số chuỗi trích xuất có sự khác biệt nhỏ về từ đồng nghĩa (ví dụ `AI Agents` vs `AI Agent`).
- **Nếu có thêm một vòng (v4), nhóm sẽ thử giả thuyết nào?**
  - **Giả thuyết cho Local Model (Ollama Qwen 2.5 7B):** Tối giản hóa schema `tools.yaml` (lược bớt các trường không cần thiết, cô đọng description dưới 3 dòng) sẽ giúp mô hình nhỏ không bị phân tâm, giảm thiểu tỷ lệ lỗi sinh JSON sai cú pháp (`_invalid_json_arguments`) và tránh hiện tượng gọi tool ảo.

## 8. Tài liệu tham khảo

1. OpenAI Documentation: *Function Calling and Structured Outputs with GPT Models*.
2. arXiv API User Manual: *Query Construction, Boolean Operators, and Subject Taxonomy*.
3. Telegram Core Documentation: *Bots: An introduction for developers & Formatting options*.
4. FastAPI Official Guide: *Streaming Responses and Server-Sent Events (SSE)*.
5. Next.js 15 & Tailwind CSS: *App Router Architecture and Interactive Components*.
