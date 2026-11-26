"""NGƯỜI PHỤ TRÁCH: C (parser). Nhận 1 dòng người dùng gõ, gọi đúng module.

Text thường -> gửi cho partner hiện tại. Text bắt đầu bằng "/" -> lệnh (mục 4.1).
dispatch() trả False khi cần thoát chương trình (/quit).
"""
import config
import file_transfer
import state
import tcp_chat
import udp_discovery
import ui

HELP = (
    "Commands:\n"
    "  /list                    show online users\n"
    "  /chat <name|number>      open a chat\n"
    "  <text>                   send a message to the current partner\n"
    "  /send <file>             send a file to the current partner\n"
    "  /leave                   close the current chat\n"
    "  /status <online|away>    change your status\n"
    "  /help                    show this help\n"
    "  /quit                    exit"
)


def dispatch(line: str):
    if not line.startswith("/"):
        tcp_chat.send_text(line)
        return True

    cmd, _, arg = line.partition(" ")
    arg = arg.strip()

    if cmd == "/list":
        # TODO(C): in "  1. Minh   (192.168.1.12)  online" theo udp_discovery.list_peers()
        pass
    elif cmd == "/chat" and arg:
        tcp_chat.open_chat(arg)
    elif cmd == "/send" and arg:
        file_transfer.send_file_async(arg)
    elif cmd == "/leave":
        tcp_chat.leave_chat()
    elif cmd == "/status" and arg in config.STATUSES:
        udp_discovery.set_status(arg)
    elif cmd == "/help":
        ui.show_message(HELP)
    elif cmd == "/quit":
        return False
    else:
        ui.show_message("[!] Invalid command. Type /help")   # lệnh sai -> help ngắn (mục 5.3)
    return True
