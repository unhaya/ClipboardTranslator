# ClipboardTranslator v1.00 - Vocabulary Dialog
import tkinter as tk
from tkinter import ttk, messagebox


def show_vocabulary_dialog(app):
    """単語帳ダイアログを表示"""
    if not hasattr(app, 'vocab_manager'):
        messagebox.showwarning("警告", "単語帳機能が初期化されていません")
        return

    vocab_window = tk.Toplevel(app)
    vocab_window.title("単語帳")
    vocab_window.geometry("700x500")
    vocab_window.minsize(600, 400)
    vocab_window.transient(app)

    # スタイル設定
    style = ttk.Style()
    default_font = ('Yu Gothic UI', 9)
    style.configure('Treeview', font=default_font)
    style.configure('Treeview.Heading', font=(default_font[0], default_font[1], 'bold'))

    # メインフレーム
    main_frame = ttk.Frame(vocab_window, padding=10)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # フィルタフレーム
    filter_frame = ttk.Frame(main_frame)
    filter_frame.pack(fill=tk.X, pady=(0, 10))

    ttk.Label(filter_frame, text="カテゴリ:").pack(side=tk.LEFT, padx=(0, 5))
    category_var = tk.StringVar(value="すべて")
    categories = ["すべて"] + app.vocab_manager.vocabulary.get('categories', [])
    category_combo = ttk.Combobox(filter_frame, textvariable=category_var, values=categories, width=15, state="readonly")
    category_combo.pack(side=tk.LEFT, padx=(0, 10))

    ttk.Label(filter_frame, text="言語:").pack(side=tk.LEFT, padx=(0, 5))
    lang_var = tk.StringVar(value="すべて")
    lang_combo = ttk.Combobox(filter_frame, textvariable=lang_var, values=["すべて", "EN", "JA"], width=10, state="readonly")
    lang_combo.pack(side=tk.LEFT)

    # ツリービュー
    tree_frame = ttk.Frame(main_frame)
    tree_frame.pack(fill=tk.BOTH, expand=True)

    columns = ('単語', '意味', 'カテゴリ', '言語', 'テスト回数', '正答率')
    tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

    for col in columns:
        tree.heading(col, text=col)

    tree.column('単語', width=120)
    tree.column('意味', width=200)
    tree.column('カテゴリ', width=80)
    tree.column('言語', width=50)
    tree.column('テスト回数', width=80)
    tree.column('正答率', width=80)

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.configure(yscrollcommand=scrollbar.set)

    # 統計フレーム
    stats_frame = ttk.LabelFrame(main_frame, text="統計", padding=5)
    stats_frame.pack(fill=tk.X, pady=(10, 0))

    stats_label = ttk.Label(stats_frame, text="")
    stats_label.pack(anchor=tk.W)

    # ボタンフレーム
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill=tk.X, pady=(10, 0))

    def load_words():
        """単語をツリービューに読み込む"""
        for item in tree.get_children():
            tree.delete(item)

        category = category_var.get()
        if category == "すべて":
            category = None

        lang = lang_var.get()
        if lang == "すべて":
            lang = None

        words = app.vocab_manager.get_words(category=category, source_lang=lang)

        for word in words:
            test_count = word.get('test_count', 0)
            correct_count = word.get('correct_count', 0)
            accuracy = f"{(correct_count / test_count * 100):.0f}%" if test_count > 0 else "-"

            tree.insert('', tk.END, values=(
                word['word'],
                word['meaning'][:50] + ('...' if len(word['meaning']) > 50 else ''),
                word.get('category', '-'),
                word.get('source_lang', '-'),
                test_count,
                accuracy
            ))

        # 統計を更新
        stats = app.vocab_manager.get_statistics()
        stats_label.config(text=f"総単語数: {stats['total']}  |  習得済み: {stats['mastered']}  |  テスト済み: {stats['tested']}  |  未テスト: {stats['not_tested']}")

    def delete_selected():
        """選択された単語を削除"""
        selected_items = tree.selection()
        if not selected_items:
            return

        if not messagebox.askyesno("確認", "選択した単語を削除しますか？"):
            return

        for item in selected_items:
            values = tree.item(item, 'values')
            word = values[0]
            app.vocab_manager.remove_word(word)

        load_words()

    def add_new_word():
        """新しい単語を追加するダイアログ"""
        add_window = tk.Toplevel(vocab_window)
        add_window.title("単語を追加")
        add_window.geometry("400x300")
        add_window.transient(vocab_window)
        add_window.grab_set()

        add_frame = ttk.Frame(add_window, padding=15)
        add_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(add_frame, text="単語:").pack(anchor=tk.W)
        word_entry = ttk.Entry(add_frame, width=40)
        word_entry.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(add_frame, text="意味:").pack(anchor=tk.W)
        meaning_text = tk.Text(add_frame, height=3, width=40)
        meaning_text.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(add_frame, text="言語:").pack(anchor=tk.W)
        new_lang_var = tk.StringVar(value="EN")
        lang_frame = ttk.Frame(add_frame)
        lang_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Radiobutton(lang_frame, text="英語", variable=new_lang_var, value="EN").pack(side=tk.LEFT)
        ttk.Radiobutton(lang_frame, text="日本語", variable=new_lang_var, value="JA").pack(side=tk.LEFT)

        ttk.Label(add_frame, text="カテゴリ:").pack(anchor=tk.W)
        new_category_var = tk.StringVar(value="基本")
        category_combo = ttk.Combobox(add_frame, textvariable=new_category_var,
                                      values=app.vocab_manager.vocabulary.get('categories', []), width=15)
        category_combo.pack(anchor=tk.W, pady=(0, 10))

        def save_word():
            word = word_entry.get().strip()
            meaning = meaning_text.get("1.0", tk.END).strip()

            if not word:
                messagebox.showwarning("警告", "単語を入力してください")
                return

            if not meaning:
                messagebox.showwarning("警告", "意味を入力してください")
                return

            source_lang = new_lang_var.get()
            target_lang = "JA" if source_lang == "EN" else "EN"

            app.vocab_manager.add_word(word, meaning, source_lang, target_lang, category=new_category_var.get())
            messagebox.showinfo("完了", f"単語「{word}」を追加しました")
            add_window.destroy()
            load_words()

        btn_frame = ttk.Frame(add_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Button(btn_frame, text="追加", command=save_word).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="キャンセル", command=add_window.destroy).pack(side=tk.RIGHT)

    # フィルタ変更時に再読み込み
    category_var.trace_add("write", lambda *args: load_words())
    lang_var.trace_add("write", lambda *args: load_words())

    ttk.Button(button_frame, text="追加", command=add_new_word).pack(side=tk.LEFT, padx=(0, 5))
    ttk.Button(button_frame, text="削除", command=delete_selected).pack(side=tk.LEFT, padx=(0, 5))
    ttk.Button(button_frame, text="閉じる", command=vocab_window.destroy).pack(side=tk.RIGHT)

    load_words()
