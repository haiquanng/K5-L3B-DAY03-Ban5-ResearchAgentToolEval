# Báo cáo cá nhân — Nguyễn Văn Hải Quân - 2A202603994

## 1. Thông tin thành viên

- Họ tên: Nguyễn Văn Hải Quân
- MSSV: 2A202603994
- Email: 26ai.quannvh@vinuni.edu.vn
- Vai trò: Lead / Full-stack Developer (Giao diện Web, Telegram Bot & Server API)

## 2. Phần việc phụ trách

- Quản lý repository GitHub nhóm, thiết lập môi trường mẫu và điều phối merge Pull Requests.
- Thiết kế và phát triển toàn bộ hệ thống giao diện Web người dùng (`web/`, Next.js 15, Tailwind CSS, shadcn/ui).
- Phát triển API backend (`starter_v0/server.py`, FastAPI) hỗ trợ Server-Sent Events (SSE) để truyền trực tiếp tiến trình suy luận và gọi tool theo thời gian thực.
- Xây dựng bot Telegram hai chiều (`starter_v0/telegram_bot.py`) có khả năng nhận lệnh, kích hoạt agent và gửi nút bấm Inline Keyboard xác nhận.
- Đóng gói và triển khai ứng dụng web lên nền tảng Vercel: `https://research-agent-ban5.vercel.app`.

## 3. Đóng góp cụ thể

- **Giao diện Web & Backend FastAPI**:
  - Xây dựng giao diện chat hiện đại, thân thiện, hỗ trợ markdown, timeline hiển thị chi tiết tham số, kết quả và thời gian phản hồi của từng tool call.
  - Tích hợp tính năng lựa chọn phiên bản agent (v0, v1, v2, v3) ngay trên giao diện mà không cần khởi động lại server (`starter_v0/artifacts/versions/`).
  - Hỗ trợ popup xác nhận duyệt tin (Human-in-the-Loop) khi agent chuẩn bị thực thi hành động nhạy cảm.
- **Telegram Bot Tương tác**:
  - Triển khai bot Telegram xử lý tin nhắn từ người dùng trong danh sách cho phép (`TELEGRAM_ALLOWED_CHAT_IDS`).
  - Hỗ trợ cơ chế Inline Keyboard: hiển thị nút bấm "Đồng ý" / "Hủy" khi agent gọi `clarify` dạng `yes_no`.
- **Bảo mật và Vận hành**:
  - Cơ chế tự động che giấu (redact) toàn bộ khóa bí mật, API key, bot token trước khi lưu vào transcript hoặc gửi về browser client.

## 4. Bằng chứng

- **Files**:
  - Thư mục `web/` (Next.js client)
  - `starter_v0/server.py`
  - `starter_v0/telegram_bot.py`
  - `starter_v0/tests/test_telegram_bot.py`
  - `starter_v0/tests/test_versions.py`
- **Commits**:
  - Commit `9bdc927`: feat: web UI (Next.js) and FastAPI server streaming agent tool calls
  - Commit `596bf37`: feat: chat with the agent from Telegram; log Vercel deployment
  - Commit `60e9dd2`: feat: version dropdown in the web UI with frozen v0-v3 prompt/tools
- **Deploy**:
  - Web UI: https://research-agent-ban5.vercel.app
- **Công cụ AI đã dùng**:
  - v0.dev & Cursor: Hỗ trợ sinh layout components và shadcn/ui boilerplate. Đã tự tinh chỉnh logic SSE client, state management và error boundaries.

## 5. Tự đánh giá

- Đã hoàn thành toàn bộ trách nhiệm lead nhóm và các deliverable giao diện (CP5).
- Đóng góp nổi bật: Xây dựng hoàn chỉnh cả Web UI (Next.js) lẫn Telegram Bot, triển khai production lên Vercel.
- Đánh giá: Xuất sắc (10/10).
