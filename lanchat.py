"""Điểm vào chương trình.  Ví dụ:
    python lanchat.py --name Quan --port 5000
    python lanchat.py --name Minh --port 5001 --bcast 127.255.255.255   # test 1 máy, offline

File này chỉ ghép các module lại; mỗi module do 1 người phụ trách (xem README).
"""
import argparse

import commands
import config
import state
import tcp_chat
import udp_discovery
import ui


def main():
    p = argparse.ArgumentParser(description="LAN Chat & File Sharing")
    p.add_argument("--name", required=True, help="tên hiển thị của bạn")
    p.add_argument("--port", type=int, default=config.DEFAULT_TCP_PORT, help="cổng TCP lắng nghe")
    p.add_argument("--bcast", default=config.BROADCAST_ADDR, help="địa chỉ broadcast UDP")
    args = p.parse_args()

    with state.lock:
        state.my_name = args.name
        state.my_tcp_port = args.port

    tcp_chat.start(args.port)
    print(f"[*] Listening on TCP port {args.port}")
    udp_discovery.start(args.bcast)
    print(f"[*] Broadcasting presence on UDP port {config.UDP_PORT}")

    try:
        ui.input_loop(commands.dispatch)      # MAIN thread: đọc phím, chạy lệnh
    finally:
        state.running.clear()
        # TODO: gửi BYE cho các chat đang mở, đóng socket
        print("[*] Bye!")


if __name__ == "__main__":
    main()
