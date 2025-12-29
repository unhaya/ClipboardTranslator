#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ClipboardTranslator v1.00
クリップボードの単語を自動的に翻訳・辞書検索・音声出力するデスクトップアプリケーション

使い方:
1. テキストをコピー (Ctrl+C)
2. Ctrl+Alt+D で翻訳
3. Ctrl+Alt+J で辞書検索
4. Ctrl+Alt+T で音声出力
"""

import os
import sys
import tkinter as tk
from tkinter import messagebox

# プロジェクトルートをパスに追加
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from ui.main_window import TranslationApp

# 重複起動防止用のミューテックス名
MUTEX_NAME = "ClipboardTranslator_v1.00_SingleInstance"


def check_single_instance():
    """
    重複起動をチェックする。
    既に起動している場合はFalseを返し、初回起動の場合はTrueを返す。
    """
    if sys.platform == 'win32':
        import ctypes
        from ctypes import wintypes

        # Windows API関数の定義
        kernel32 = ctypes.windll.kernel32

        # CreateMutex: ミューテックスを作成または開く
        kernel32.CreateMutexW.argtypes = [wintypes.LPVOID, wintypes.BOOL, wintypes.LPCWSTR]
        kernel32.CreateMutexW.restype = wintypes.HANDLE

        # GetLastError: 最後のエラーコードを取得
        ERROR_ALREADY_EXISTS = 183

        # ミューテックスを作成
        mutex = kernel32.CreateMutexW(None, True, MUTEX_NAME)
        last_error = kernel32.GetLastError()

        if last_error == ERROR_ALREADY_EXISTS:
            # 既にインスタンスが存在する
            return False

        # ミューテックスを保持するためにグローバルに保存
        global _mutex_handle
        _mutex_handle = mutex
        return True
    else:
        # 非Windows環境はロックファイルで対応
        import fcntl
        lock_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.lock')

        global _lock_file_handle
        _lock_file_handle = open(lock_file, 'w')

        try:
            fcntl.flock(_lock_file_handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return True
        except (IOError, OSError):
            return False


def main():
    """アプリケーションのエントリーポイント"""
    # 重複起動チェック
    if not check_single_instance():
        # 既に起動している場合はメッセージを表示して終了
        root = tk.Tk()
        root.withdraw()  # メインウィンドウを非表示
        messagebox.showwarning(
            "ClipTrans",
            "アプリケーションは既に起動しています。"
        )
        root.destroy()
        sys.exit(0)

    try:
        app = TranslationApp()

        # ウィンドウ位置を読み込み
        app.window_service.load_position()

        # メインループ開始
        app.mainloop()

    except Exception as e:
        print(f"アプリケーション起動エラー: {e}")
        # エラーウィンドウを表示
        error_window = tk.Tk()
        error_window.title("エラー")
        tk.Label(error_window, text=f"エラーが発生しました:\n{e}", padx=20, pady=20).pack()
        tk.Button(error_window, text="OK", command=error_window.destroy).pack(pady=10)
        error_window.mainloop()


if __name__ == "__main__":
    main()
