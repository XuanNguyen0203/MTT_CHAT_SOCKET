"""NGƯỜI PHỤ TRÁCH: C. Giao diện console: gõ không bị gián đoạn khi có tin đến (mục 4.3).

Phần lớn lấy NGUYÊN từ option_b_manual_redraw.py (get_key, setup/restore_terminal,
show_message, screen_lock). Phần đã sửa so với bản demo:
  - input_loop nhận callback on_line(text) thay vì tự xử lý lệnh.
  - on_line chạy NGOÀI screen_lock (gửi mạng chậm không được treo màn hình).

Mọi thread khác (UDP listener, TCP receiver, file sender) chỉ cần gọi show_message().
TODO(C, tùy chọn): hỗ trợ mũi tên trái/phải, lịch sử lệnh, dòng nhập dài hơn chiều rộng terminal.
"""
import os
import sys
import threading

# ---------------------------------------------------------------------------
# Đọc 1 phím không cần Enter (Windows + Linux/macOS) — copy từ demo
# ---------------------------------------------------------------------------
if os.name == "nt":
    import msvcrt

    os.system("")  # bật ANSI escape (\033[K) trong console Windows

    def get_key():
        ch = msvcrt.getwch()
        if ch in ("\x00", "\xe0"):     # phím mũi tên / chức năng gửi 2 mã
            msvcrt.getwch()
            return None
        return ch

    def setup_terminal():
        return None

    def restore_terminal(_):
        pass
else:
    import termios
    import tty

    def get_key():
        ch = sys.stdin.read(1)
        if ch == "\x1b":               # mũi tên: ESC [ A -> bỏ qua
            sys.stdin.read(2)
            return None
        return ch

    def setup_terminal():
        old = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        return old

    def restore_terminal(old):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old)


# ---------------------------------------------------------------------------
# Trạng thái màn hình
# ---------------------------------------------------------------------------
PROMPT = "> "
CLEAR_LINE = "\r\033[K"        # về đầu dòng + xóa đến cuối dòng

buffer = ""                    # chữ người dùng đã gõ dở
screen_lock = threading.Lock() # chỉ 1 thread được ghi màn hình tại một thời điểm


def show_message(line: str):
    """In `line` LÊN TRÊN dòng nhập rồi vẽ lại prompt + chữ gõ dở. Gọi được từ mọi thread."""
    with screen_lock:
        sys.stdout.write(CLEAR_LINE)          # 1. xóa dòng nhập
        sys.stdout.write(line + "\n")         # 2. in tin nhắn
        sys.stdout.write(PROMPT + buffer)     # 3. vẽ lại prompt + chữ gõ dở
        sys.stdout.flush()


def _redraw():
    with screen_lock:
        sys.stdout.write(CLEAR_LINE + PROMPT + buffer)
        sys.stdout.flush()


# TODO(C): hiển thị % tiến độ file trên 1 dòng cập nhật tại chỗ. show_message luôn xuống dòng
#          nên cần hàm riêng, ví dụ show_progress(text) dùng CLEAR_LINE + text + "\r" rồi vẽ lại prompt.


def input_loop(on_line):
    """Vòng đọc phím của MAIN thread. on_line(text) -> False thì thoát."""
    global buffer
    old_settings = setup_terminal()
    _redraw()
    try:
        while True:
            ch = get_key()
            if ch is None:
                continue

            if ch in ("\r", "\n"):                      # Enter -> xử lý dòng
                with screen_lock:
                    text = buffer
                    buffer = ""
                    sys.stdout.write(CLEAR_LINE)
                    sys.stdout.flush()
                if text.strip():
                    if on_line(text.strip()) is False:  # NGOÀI screen_lock
                        sys.stdout.write("\n")
                        break
                _redraw()
                continue

            with screen_lock:
                if ch in ("\b", "\x7f"):                # Backspace
                    if buffer:
                        buffer = buffer[:-1]
                        sys.stdout.write("\b \b")
                elif ch == "\x03":                      # Ctrl+C
                    sys.stdout.write("\n")
                    break
                elif ch.isprintable():                  # ký tự thường (có cả tiếng Việt)
                    buffer += ch
                    sys.stdout.write(ch)
                sys.stdout.flush()
    finally:
        restore_terminal(old_settings)
