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

# プロジェクトルートをパスに追加
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from ui.main_window import TranslationApp


def main():
    """アプリケーションのエントリーポイント"""
    try:
        app = TranslationApp()

        # ウィンドウ位置を読み込み
        app.load_window_position()

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
