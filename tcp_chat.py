"""NGƯỜI PHỤ TRÁCH: B. Chat qua TCP + xử lý lỗi kết nối (mục 3.3, 5.3).

Thread:
  - acceptor        : accept() kết nối mới, mỗi connection tạo 1 receiver thread
  - receiver (mỗi connection, mô hình "one per connection" đề cho phép từ 09/11/2026):
        dùng protocol.recv_frame(sock)
          MSG  -> hiển thị (hoặc lưu + tăng unread nếu không phải partner hiện tại)
          FILE -> giao cho file_transfer.receive_file(sock, filename, size)
          BYE  -> đóng chat, báo "[*] <name> left the chat"
        Mất kết nối giữa chừng -> báo và quay về prompt, KHÔNG crash.
"""
import socket
import threading

import config
import protocol
import state
import ui


def acceptor(listen_sock):
    """Thread: vòng accept(); mỗi connection -> threading.Thread(target=receiver, ...)."""
    # TODO(B)
    raise NotImplementedError


def receiver(sock, addr):
    """Thread của 1 connection. Cần biết tên peer: gợi ý là gói đầu tiên trên connection
    mới chứa tên người gọi (hoặc tra state.peers theo IP) — chốt cách làm với A."""
    # TODO(B)
    raise NotImplementedError


def start(tcp_port: int):
    """Tạo socket lắng nghe + chạy acceptor. Trả về listen socket."""
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("", tcp_port))
    srv.listen()
    threading.Thread(target=acceptor, args=(srv,), daemon=True).start()
    return srv


def open_chat(target: str) -> bool:
    """Cho /chat <name|number>: tra peer (tên hoặc số trong /list), connect() TCP,
    đặt state.current_partner, in các tin chưa đọc rồi reset unread.
    Peer offline / từ chối kết nối -> show_message lỗi, trả False, không crash."""
    # TODO(B)
    raise NotImplementedError


def send_text(text: str) -> bool:
    """Gửi 1 dòng cho partner hiện tại. Chưa chat với ai -> báo lỗi ngắn."""
    # TODO(B): protocol.send_msg(sock, text); lỗi gửi -> báo + đóng chat
    raise NotImplementedError


def leave_chat():
    """Cho /leave: gửi BYE, đóng socket, state.current_partner = ""."""
    # TODO(B)
    raise NotImplementedError
