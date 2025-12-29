# ClipboardTranslator v1.10 - History Dialog
import tkinter as tk
from tkinter import ttk, messagebox


def _center_window(window, width, height):
    """ウィンドウをモニター中央に配置"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def show_history_dialog(app):
    """翻訳履歴ダイアログを表示"""
    history_window = tk.Toplevel(app)
    history_window.title("翻訳履歴")
    _center_window(history_window, 600, 500)
    history_window.minsize(500, 400)
    history_window.transient(app)
    history_window.grab_set()

    # スタイル設定
    style = ttk.Style()
    default_font = ('Yu Gothic UI', 9)
    style.configure('Treeview', font=default_font)
    style.configure('Treeview.Heading', font=(default_font[0], default_font[1], 'bold'))

    # メインフレーム
    main_frame = ttk.Frame(history_window, padding=10)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # 検索フレーム
    search_frame = ttk.Frame(main_frame)
    search_frame.pack(fill=tk.X, pady=(0, 10))

    ttk.Label(search_frame, text="検索:").pack(side=tk.LEFT, padx=(0, 5))
    search_var = tk.StringVar()
    search_entry = ttk.Entry(search_frame, textvariable=search_var, width=30)
    search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

    # フィルタフレーム
    filter_frame = ttk.Frame(main_frame)
    filter_frame.pack(fill=tk.X, pady=(0, 10))

    ttk.Label(filter_frame, text="表示:").pack(side=tk.LEFT, padx=(0, 5))
    filter_var = tk.StringVar(value="all")

    ttk.Radiobutton(filter_frame, text="すべて", variable=filter_var, value="all").pack(side=tk.LEFT, padx=(0, 10))
    ttk.Radiobutton(filter_frame, text="通常翻訳", variable=filter_var, value="normal").pack(side=tk.LEFT, padx=(0, 10))
    ttk.Radiobutton(filter_frame, text="辞書検索", variable=filter_var, value="dictionary").pack(side=tk.LEFT)

    # ツリービュー
    tree_frame = ttk.Frame(main_frame)
    tree_frame.pack(fill=tk.BOTH, expand=True)

    columns = ('時間', '原文', '翻訳')
    tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

    for col in columns:
        tree.heading(col, text=col)

    tree.column('時間', width=120, stretch=False)
    tree.column('原文', width=200)
    tree.column('翻訳', width=200)

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.configure(yscrollcommand=scrollbar.set)

    # 詳細表示
    detail_frame = ttk.LabelFrame(main_frame, text="詳細", padding=5)
    detail_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

    detail_text = tk.Text(detail_frame, wrap=tk.WORD, height=5)
    detail_text.pack(fill=tk.BOTH, expand=True)

    # ボタンフレーム
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill=tk.X, pady=(10, 0))

    def load_history_to_tree():
        """履歴をツリービューに読み込む"""
        for item in tree.get_children():
            tree.delete(item)

        filter_type = filter_var.get()
        if filter_type == "all":
            filter_type = None

        search_query = search_var.get()
        if search_query:
            history_entries = app.history.search_history(search_query)
        else:
            history_entries = app.history.get_history(filter_type=filter_type)

        for entry in history_entries:
            tree.insert('', tk.END, values=(
                entry['timestamp'],
                entry['original_text'][:30] + ('...' if len(entry['original_text']) > 30 else ''),
                entry['translated_text'][:30] + ('...' if len(entry['translated_text']) > 30 else '')
            ), tags=(entry['translation_type'],))

        tree.tag_configure('normal', background='#f0f0ff')
        tree.tag_configure('dictionary', background='#f0fff0')
        tree.tag_configure('speech', background='#fff0f0')

    def show_detail(event):
        """詳細を表示"""
        selected_items = tree.selection()
        if not selected_items:
            return

        index = tree.index(selected_items[0])

        filter_type = filter_var.get()
        if filter_type == "all":
            filter_type = None

        search_query = search_var.get()
        if search_query:
            history_entries = app.history.search_history(search_query)
        else:
            history_entries = app.history.get_history(filter_type=filter_type)

        if index >= len(history_entries):
            return

        entry = history_entries[index]

        detail_text.config(state=tk.NORMAL)
        detail_text.delete(1.0, tk.END)
        detail_text.insert(tk.END, f"【翻訳タイプ】: {entry['translation_type']}\n")
        detail_text.insert(tk.END, f"【時間】: {entry['timestamp']}\n")
        detail_text.insert(tk.END, f"【原文 ({entry['source_lang']})】: {entry['original_text']}\n")
        detail_text.insert(tk.END, f"【翻訳 ({entry['target_lang']})】: {entry['translated_text']}\n")
        detail_text.config(state=tk.DISABLED)

    def on_search_filter_change(*args):
        load_history_to_tree()

    search_var.trace_add("write", on_search_filter_change)
    filter_var.trace_add("write", on_search_filter_change)

    tree.bind('<<TreeviewSelect>>', show_detail)

    def reuse_selected():
        """選択された翻訳を再利用"""
        selected_items = tree.selection()
        if not selected_items:
            return

        index = tree.index(selected_items[0])

        filter_type = filter_var.get()
        if filter_type == "all":
            filter_type = None

        search_query = search_var.get()
        if search_query:
            history_entries = app.history.search_history(search_query)
        else:
            history_entries = app.history.get_history(filter_type=filter_type)

        if index >= len(history_entries):
            return

        entry = history_entries[index]
        app.clipboard_clear()
        app.clipboard_append(entry['translated_text'])
        app.update_status('text_copied')
        app.log_message(f"履歴から再利用: {entry['translated_text'][:50]}...")

    def delete_selected():
        """選択を削除"""
        selected_items = tree.selection()
        if not selected_items:
            return

        index = tree.index(selected_items[0])

        filter_type = filter_var.get()
        if filter_type == "all":
            filter_type = None

        search_query = search_var.get()
        if search_query:
            history_entries = app.history.search_history(search_query)
        else:
            history_entries = app.history.get_history(filter_type=filter_type)

        if index >= len(history_entries):
            return

        entry = history_entries[index]
        app.history.history.remove(entry)
        app.history.save_history()
        load_history_to_tree()

    def clear_all_history():
        """すべての履歴をクリア"""
        if messagebox.askyesno("確認", "本当にすべての翻訳履歴をクリアしますか？"):
            app.history.clear_history()
            load_history_to_tree()

    ttk.Button(button_frame, text="再利用", command=reuse_selected).pack(side=tk.LEFT, padx=(0, 5))
    ttk.Button(button_frame, text="削除", command=delete_selected).pack(side=tk.LEFT, padx=(0, 5))
    ttk.Button(button_frame, text="すべてクリア", command=clear_all_history).pack(side=tk.LEFT)
    ttk.Button(button_frame, text="閉じる", command=history_window.destroy).pack(side=tk.RIGHT)

    load_history_to_tree()
