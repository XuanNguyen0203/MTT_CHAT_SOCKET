"""Dữ liệu dùng chung giữa các thread. Mọi truy cập PHẢI giữ `lock` (yêu cầu mục 5.1).

Ví dụ:
    with state.lock:
        state.peers[name] = Peer(...)
"""
import threading
import time
from dataclasses import dataclass, field


@dataclass
class Peer:
    name: str
    ip: str
    tcp_port: int
    status: str = "online"
    last_seen: float = field(default_factory=time.time)


# Một lock bảo vệ tất cả dữ liệu bên dưới (RLock để gọi lồng nhau không bị treo).
lock = threading.RLock()

my_name: str = ""
my_tcp_port: int = 0
my_status: str = "online"            # A: /status đổi giá trị này

peers: dict = {}                     # name -> Peer            (A ghi, B đọc)
conns: dict = {}                     # name -> socket TCP chat (B ghi)
history: dict = {}                   # name -> list[str]       (B ghi)
unread: dict = {}                    # name -> int             (B ghi)
current_partner: str = ""            # tên partner hiện tại, "" nếu chưa chat

running = threading.Event()          # đặt khi chương trình chạy; /quit thì clear
running.set()
