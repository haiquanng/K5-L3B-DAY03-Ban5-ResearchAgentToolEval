# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: Ban5
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3: openrouter (openai/gpt-4o-mini)

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

Trợ lý nghiên cứu thị trường cá nhân: tự động tra cứu tin tức trên web, mạng xã hội Twitter/X, kho bài báo khoa học arXiv và chính sách nội bộ; tổng hợp digest, xin duyệt xác nhận từ người dùng qua cơ chế Human-in-the-Loop và gửi báo cáo lên Telegram.

**Cách chạy UI:**

```bash
# Cách 1: Giao diện Web (Next.js + FastAPI Server SSE)
# Terminal 1 - Backend:
cd starter_v0
python server.py --provider openrouter --version v3

# Terminal 2 - Frontend:
cd web
npm install && npm run dev
# Truy cập giao diện tại: http://localhost:3000

# Cách 2: Chat trực tiếp qua CLI
cd starter_v0
python chat.py --provider openrouter --version v3
```

**Link dùng thử (deploy):**

- Vercel Web UI: [https://research-agent-ban5.vercel.app](https://research-agent-ban5.vercel.app)
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

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn). Run file: `starter_v0/runs/v3_B_group_openrouter_20261110T191237962030.json` (10/10 passed, accuracy=1.00, routing=1.00, multiturn=1.00).

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
| Turn 1 (Yêu cầu thường) | `"Tìm giúp tôi 2 bài báo arXiv mới nhất về AI Agent"` | `papers(max_results=2, query='AI Agent', sort_by='submittedDate')` | v3 | Agent gọi arXiv API, trích xuất và tóm tắt 2 bài báo mới nhất (World In-Context Learning & Multi-Agent Screening) kèm link PDF |
| Turn 2 (Thiếu thông tin) | `"Tóm tắt các tweet gần nhất trên Twitter giúp tôi"` | `clarify(question='Bạn có thể cho tôi biết chủ đề hoặc từ khóa...', response_type='text')` | v3 | Agent không đoán mò username, phản hồi yêu cầu người dùng cung cấp tài khoản Twitter cần xem |
| Turn 3 (Bổ sung thông tin) | `"Tài khoản @sama nhé"` | `timeline(limit=5, screenname='sama')` | v3 | Agent gọi API Twitter lấy 5 tweet gần nhất của @sama, tóm tắt nội dung kèm số liệu like, retweet, view |
| Turn 4 (Hành động side-effect) | `"Đăng bản tin tóm tắt này lên Telegram giúp mình"` | `clarify(question='Bạn xác nhận muốn gửi bản tin tóm tắt này qua Telegram chứ?', response_type='yes_no')` | v3 | Agent áp dụng Human-in-the-Loop, dừng lại xin duyệt xác nhận yes/no trước khi gửi tin ra ngoài |
| Turn 5 (User xác nhận duyệt) | `"Đồng ý"` | `send(confirmed=true, text='...')` | v3 | Agent nhận diện sự đồng ý, gọi `send` gửi thành công bản tin vào kênh Telegram (`status: sent`) |

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
| Small Local Model | xem B7 | Chưa triển khai | Cần cấu hình GPU local |
| Hơn 3 tool mới (≥ 4) | N/A | Nhóm tập trung hoàn thiện sâu 1 tool `stats` chuẩn chỉ | |
| `send` gửi thật lên Telegram sau xác nhận | `starter_v0/transcripts/v3_openrouter_20261110T195604556819.transcript.json` | Luồng Human-in-the-Loop hoàn chỉnh: agent hỏi duyệt `yes_no` -> user xác nhận `"Đồng ý"` -> gọi `send(confirmed=true)` -> `status: sent` trên Telegram của nhóm | Tool kiểm tra cờ `confirmed: bool`; nếu `false` thì từ chối gửi (`needs_confirmation`), bảo vệ kênh tránh spam ngoài ý muốn |
| Test challenge (0 skipped / regression test) | `starter_v0/analysis/duclt_pytest.txt`, output `pytest` | Toàn bộ suite đạt **130 passed, 0 failed, 0 skipped** (xóa bỏ 17 skip mặc định, mở rộng 37 parametrization test cases) | Kiểm tra toàn bộ biên cắt ký tự markdown (4000 chars), missing env vars, types validation |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng:
- Đã khắc phục lỗi tiềm ẩn khi gọi Telegram với văn bản vượt quá 4096 ký tự bằng hàm phân đoạn tin nhắn an toàn trong `telegram_bot.py`.
- Đã xử lý lỗi dữ liệu số ngoại lai (NaN, Infinity, kiểu chuỗi) trong công cụ tính toán thống kê, chuyển đổi thành kết quả báo lỗi êm dịu (graceful degradation) thay vì unhandled exception.

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | openai/gpt-4o-mini (openrouter) | v3 | 1.00 | 1.00 | 1.00 | 1.00 | starter_v0/runs/v3_B_base_openrouter_20261110T191959929397.json |

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
