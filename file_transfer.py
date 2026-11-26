"""NGƯỜI PHỤ TRÁCH: C. Truyền file qua TCP (mục 3.4).

Gửi : /send <file> -> mỗi lần gửi chạy 1 thread riêng (không chặn chat), hiện % tiến độ.
Nhận: được tcp_chat.receiver gọi khi gặp frame FILE; lưu vào config.DOWNLOAD_DIR.
Lỗi : file không tồn tại, truyền bị gián đoạn -> báo lỗi và XÓA file dở (mục 5.3).
"""
import os
import socket
import threading

import config
import protocol
import state
import ui


def send_file_async(path: str):
    """Cho /send <file>. Kiểm tra file tồn tại NGAY (báo lỗi nếu không), rồi tạo thread
    chạy _send_file. Gửi cho state.current_partner; chưa chat -> báo lỗi ngắn."""
    # TODO(C)
    raise NotImplementedError


def _send_file(path: str, sock: socket.socket):
    """Thread gửi: protocol.send_file_header(...), rồi gửi từng khối config.CHUNK_SIZE byte.
    Tiến độ: tính % = đã gửi / size. Gợi ý: dùng 1 kết nối TCP riêng cho file để
    byte của file không lẫn với frame MSG đang chat (xem phần giải thích trong README)."""
    # TODO(C)
    raise NotImplementedError


def receive_file(sock: socket.socket, filename: str, size: int):
    """Nhận đúng `size` byte (protocol.recv_exact hoặc vòng recv) và ghi vào downloads/.
    - Dùng os.path.basename(filename) để chống đường dẫn lạ (ví dụ ../../x).
    - Lỗi giữa chừng -> xóa file dở + ui.show_message báo lỗi."""
    # TODO(C)
    raise NotImplementedError
