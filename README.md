# LAN Chat & File Sharing (Command-Line)

Ứng dụng chat P2P trên console: **UDP** để phát hiện peer và trạng thái, **TCP** để chat và truyền file.
Dùng Socket API gốc của Python (`socket`, `threading`), không dùng thư viện mạng bên ngoài.

## Cấu trúc thư mục

```
lanchat/
├── lanchat.py          Điểm vào, chỉ ghép module (cả nhóm)
├── config.py           Hằng số dùng chung: cổng UDP, chu kỳ 3s, timeout 10s, downloads/
├── state.py            Dữ liệu dùng chung + lock: peers, conns, history, unread, partner
├── protocol.py         [A] Đóng/mở gói UDP, framing TCP (MSG/FILE/BYE), recv_exact
├── udp_discovery.py    [A] Broadcaster + listener, danh sách online, /list, /status
├── tcp_chat.py         [B] Acceptor, receiver mỗi connection, /chat, /leave, unread, lỗi kết nối
├── ui.py               [C] Đọc phím, vẽ lại dòng nhập, screen_lock, show_message
├── commands.py         [C] Parser lệnh /list /chat /send /leave /status /help /quit
├── file_transfer.py    [C] /send, tiến độ %, lưu vào downloads/, xóa file dở khi lỗi
├── requirements.txt    Chỉ cần nếu dùng prompt_toolkit
├── downloads/          File nhận được (đề yêu cầu)
├── docs/               Báo cáo 5–10 trang (kiến trúc, thread, giao thức, vấn đề và cách giải quyết)
└── wireshark/          Ảnh chụp UDP broadcast và TCP three-way handshake + giải thích ngắn
```

Phân công module và điểm số: xem bản "Phân công nhiệm vụ" của nhóm.
Mỗi file `.py` đã có sẵn khung hàm, chú thích `TODO(người phụ trách)` và hướng dẫn tái sử dụng code demo.

## Thread model (đề mục 5.1)

| Thread | Module | Việc |
| --- | --- | --- |
| Main | ui.py | Đọc phím, chạy lệnh |
| UDP broadcaster | udp_discovery.py | Gửi HELLO mỗi 3s |
| UDP listener | udp_discovery.py | Cập nhật danh sách online, timeout 10s |
| TCP acceptor | tcp_chat.py | Nhận kết nối mới, tạo receiver |
| TCP receiver (mỗi connection) | tcp_chat.py | Chat: hiển thị tin. File: lưu file |
| File sender (mỗi lần gửi) | file_transfer.py | Gửi file, không chặn chat |

Quy tắc dùng chung: mọi truy cập `state.*` phải giữ `state.lock`; mọi ghi màn hình đi qua `ui.show_message()`.

## Giao thức

```
UDP:  HELLO|<name>|<tcp_port>|<status>        vd HELLO|Quan|5000|online
TCP:  MSG|<length>|<utf-8 text>
      FILE|<filename>|<size_in_bytes>|<raw file bytes>
      BYE|
```

Ghi chú thiết kế: mục 5.1 của đề cho phép "TCP receiver (one per connection)" với *chat connection* và *file connection*.
Gửi file trên một kết nối TCP riêng giúp byte của file không lẫn với tin nhắn đang chat. Nhóm cần chốt cách làm này trước khi B và C code.

## Cài đặt và chạy

Yêu cầu: Python 3.8+. Không cần cài thêm gì (trừ khi chọn `prompt_toolkit`: `pip install -r requirements.txt`).

```
python lanchat.py --name Quan --port 5000
```

Nhiều instance trên **một máy** (khác `--port`; offline thì broadcast vào loopback):

```
python lanchat.py --name Quan --port 5001 --bcast 127.255.255.255
python lanchat.py --name Minh --port 5002 --bcast 127.255.255.255
python lanchat.py --name Lan  --port 5003 --bcast 127.255.255.255
```

Nhiều **máy** cùng LAN/Wi-Fi: chạy mỗi máy một lệnh với `--name` khác nhau, bỏ `--bcast`.
Windows: cho phép Python qua Windows Firewall, nếu không sẽ không nhận được broadcast.

## Cách test

- Milestone 1: TCP echo client/server và UDP send/receive (có thể dùng `netcat`: `nc -u -l 9999`).
- `/list` thấy peer xuất hiện, và biến mất sau khoảng 10s khi tắt một instance.
- `/chat` hai chiều; tin từ người khác partner hiện tại hiện "(n unread)".
- Gõ dở một dòng rồi chờ tin đến: chữ gõ dở không được mất.
- `/send` file lớn trong khi vẫn chat được; kiểm tra file trong `downloads/`.
- Lỗi: tắt đột ngột một peer giữa lúc chat và gửi file, `/chat` người đã offline, `/send` file không tồn tại, gõ lệnh sai.

## Checklist nộp bài

- [ ] Source code + README này (cập nhật lại phần chạy/test cho đúng thực tế)
- [ ] Báo cáo 5–10 trang trong `docs/`
- [ ] Ảnh Wireshark trong `wireshark/` (UDP broadcast + TCP three-way handshake, có giải thích)
- [ ] Demo trực tiếp 10 phút trên ít nhất 2 máy
