"""Hằng số dùng chung toàn chương trình (cả nhóm thống nhất, không tự đổi lẻ)."""

# --- UDP (đề: cổng cố định, ví dụ 9999) ---
UDP_PORT = 9999
BROADCAST_ADDR = "255.255.255.255"   # offline/1 máy: dùng "127.255.255.255"
HELLO_INTERVAL = 3                   # giây, chu kỳ broadcast (mục 3.1)
PEER_TIMEOUT = 10                    # giây, quá hạn thì xóa khỏi danh sách (mục 3.1)

# --- TCP ---
DEFAULT_TCP_PORT = 5000
CHUNK_SIZE = 4096                    # kích thước mỗi lần recv()/send() file

# --- Thư mục ---
DOWNLOAD_DIR = "downloads"           # file nhận được lưu ở đây (mục 3.4)

# --- Trạng thái hợp lệ ---
STATUSES = ("online", "away")
