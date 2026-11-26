"""NGƯỜI PHỤ TRÁCH: A. Giao thức dùng chung (B và C đều import file này).

UDP : HELLO|<name>|<tcp_port>|<status>
TCP : MSG|<length>|<utf-8 text>
      FILE|<filename>|<size_in_bytes>|<raw file bytes>
      BYE|

TCP là byte stream, không có ranh giới message => luôn đọc đúng <length>/<size> byte.
Đề cho phép tự thiết kế giao thức; nếu đổi định dạng thì ghi vào báo cáo.
"""


# ---------------------------------------------------------------- UDP
def pack_hello(name: str, tcp_port: int, status: str) -> bytes:
    """Tạo gói presence: b'HELLO|Quan|5000|online'."""
    return f"HELLO|{name}|{tcp_port}|{status}".encode("utf-8")


def parse_hello(data: bytes):
    """Trả về (name, tcp_port, status) hoặc None nếu gói sai định dạng."""
    # TODO(A): split("|"), kiểm tra đủ 4 phần, parts[0] == "HELLO", port là số,
    #          status thuộc config.STATUSES. Gói lạ -> trả None, KHÔNG raise.
    raise NotImplementedError


# ---------------------------------------------------------------- TCP
def recv_exact(sock, n: int) -> bytes:
    """Đọc đúng n byte (lặp recv đến khi đủ). Peer đóng kết nối giữa chừng -> ConnectionError."""
    chunks = []
    remaining = n
    while remaining > 0:
        chunk = sock.recv(remaining)
        if not chunk:
            raise ConnectionError("peer closed the connection")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def send_msg(sock, text: str) -> None:
    """Gửi MSG|<length>|<utf-8 text>. length tính theo BYTE sau khi encode utf-8."""
    # TODO(A): encode text, ghép header, sock.sendall(...)
    raise NotImplementedError


def send_bye(sock) -> None:
    """Gửi BYE| trước khi đóng chat (/leave, /quit)."""
    # TODO(A)
    raise NotImplementedError


def send_file_header(sock, filename: str, size: int) -> None:
    """Gửi FILE|<filename>|<size>| (phần byte nội dung do file_transfer.py gửi tiếp)."""
    # TODO(A)
    raise NotImplementedError


def recv_frame(sock):
    """Đọc 1 frame từ socket. Trả về một trong:
        ("MSG", text)
        ("FILE", filename, size)   # header đã đọc xong; C đọc tiếp đúng `size` byte
        ("BYE",)
    Raise ConnectionError nếu peer đóng; ValueError nếu frame sai định dạng.
    Gợi ý: đọc từng byte đến khi gặp '|' để lấy type, rồi đọc tiếp theo từng loại.
    """
    # TODO(A)
    raise NotImplementedError
