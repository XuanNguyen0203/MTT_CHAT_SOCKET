"""NGƯỜI PHỤ TRÁCH: A. UDP discovery + trạng thái (mục 3.1, 3.2).

Thread:
  - broadcaster : mỗi HELLO_INTERVAL giây gửi HELLO|<name>|<tcp_port>|<status>
  - listener    : nhận gói, cập nhật state.peers, xóa peer quá PEER_TIMEOUT giây,
                  báo online/offline bằng ui.show_message(...)
"""
import socket
import threading
import time

import config
import protocol
import state
import ui


def make_socket():
    """Lấy nguyên từ udp_broadcast_demo.py: nhiều tiến trình dùng chung cổng UDP."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Phải đặt TRƯỚC bind
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if hasattr(socket, "SO_REUSEPORT"):          # cần cho macOS/BSD
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except OSError:
            pass
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind(("", config.UDP_PORT))                # "" = mọi interface
    return s


def broadcaster(bcast_addr: str = config.BROADCAST_ADDR):
    """Thread: gửi presence định kỳ. Đọc state.my_name/my_tcp_port/my_status MỖI VÒNG
    (có lock) để /status đổi được ngay."""
    # TODO(A):
    #   s = make_socket()
    #   while state.running.is_set():
    #       with state.lock: lấy name, port, status
    #       s.sendto(protocol.pack_hello(...), (bcast_addr, config.UDP_PORT))
    #       time.sleep(config.HELLO_INTERVAL)
    raise NotImplementedError


def listener():
    """Thread: nhận HELLO từ người khác (bỏ qua gói của chính mình).
    - Peer mới -> thêm vào state.peers + ui.show_message("[*] <name> is online")
    - Peer cũ  -> cập nhật last_seen, status
    - Peer im lặng quá config.PEER_TIMEOUT giây -> xóa + ui.show_message("[*] <name> went offline")
    Gợi ý: s.settimeout(1) để định kỳ quét timeout dù không có gói đến.
    """
    # TODO(A)
    raise NotImplementedError


def start(bcast_addr: str = config.BROADCAST_ADDR):
    """Khởi động 2 thread (daemon). Gọi từ lanchat.py."""
    threading.Thread(target=broadcaster, args=(bcast_addr,), daemon=True).start()
    threading.Thread(target=listener, daemon=True).start()


def list_peers():
    """Cho lệnh /list: trả về danh sách [(số, name, ip, status)], đã sắp xếp ổn định."""
    # TODO(A)
    raise NotImplementedError


def set_status(status: str) -> bool:
    """Cho lệnh /status <online|away>. Trả False nếu status không hợp lệ."""
    # TODO(A): kiểm tra config.STATUSES, ghi state.my_status trong lock
    raise NotImplementedError
