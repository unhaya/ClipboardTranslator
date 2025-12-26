# ClipboardTranslator v1.00 - Network Utilities
import socket


def is_connected():
    """インターネット接続を確認"""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        pass
    return False
