# ClipboardTranslator v1.20 - TextDisplay Component
"""
テキスト表示エリアUIコンポーネント（Markdown対応）
"""
import tkinter as tk
import tkinter.font as tkfont
import re
from typing import Callable, Optional
from config.constants import MESSAGES
from config.settings import config


class TextDisplay(tk.Text):
    """テキスト表示エリアコンポーネント（Markdown対応）"""

    # タグ定義
    TAGS = {
        'input_tag': '#9597f7',
        'translated_tag': '#9597f7',
        'dict_tag': '#95f797',
        'offline_tag': '#f7d195',
        'error_tag': '#ff6b6b',
        'speech_tag': '#f79595',
        'tutor_user_tag': '#87CEEB',
        'tutor_ai_tag': '#98FB98',
    }

    # Markdown用タグ定義
    MD_TAGS = {
        'md_bold': {'foreground': '#ffffff'},
        'md_italic': {'foreground': '#cccccc'},
        'md_code': {'foreground': '#f7d195', 'background': '#444444'},
        'md_code_block': {'foreground': '#f7d195', 'background': '#2a2a2a'},
        'md_h1': {'foreground': '#87CEEB'},
        'md_h2': {'foreground': '#87CEEB'},
        'md_h3': {'foreground': '#98FB98'},
        'md_list': {'foreground': '#ffffff'},
        'md_bullet': {'foreground': '#95f797'},
        'md_table_header': {'foreground': '#87CEEB'},
        'md_table_cell': {'foreground': '#ffffff'},
        'md_table_border': {'foreground': '#666666'},
    }

    def __init__(self, parent: tk.Widget, on_font_size_change: Optional[Callable] = None, **kwargs):
        """
        初期化

        Parameters:
            parent: 親ウィジェット
            on_font_size_change: フォントサイズ変更時のコールバック(new_size: int)
        """
        super().__init__(
            parent,
            wrap=tk.WORD,
            bg='#333333',
            padx=12,
            pady=8,
            fg='white',
            font=('Segoe UI Emoji', 11),
            spacing1=2,
            spacing2=8,
            spacing3=8,
            **kwargs
        )

        self.configure(state='disabled')
        self._on_font_size_change = on_font_size_change
        self._last_font_change_time = 0

        # タグを設定
        for tag_name, color in self.TAGS.items():
            self.tag_configure(tag_name, foreground=color)

        # Markdownタグを設定
        self._setup_markdown_tags()

        # マウスホイールでフォントサイズ変更
        self.bind("<MouseWheel>", self._handle_mouse_wheel)

    def _setup_markdown_tags(self):
        """Markdown用のタグを設定"""
        base_font = self.cget("font")
        if isinstance(base_font, str):
            font_parts = base_font.split()
            font_family = font_parts[0] if font_parts else 'Segoe UI Emoji'
            try:
                font_size = int(font_parts[1]) if len(font_parts) > 1 else 11
            except ValueError:
                font_size = 11
        else:
            font_family = base_font[0] if len(base_font) > 0 else 'Segoe UI Emoji'
            font_size = base_font[1] if len(base_font) > 1 else 11

        # 太字
        bold_font = tkfont.Font(family=font_family, size=font_size, weight='bold')
        self.tag_configure('md_bold', font=bold_font, foreground='#ffffff')

        # イタリック
        italic_font = tkfont.Font(family=font_family, size=font_size, slant='italic')
        self.tag_configure('md_italic', font=italic_font, foreground='#cccccc')

        # インラインコード
        code_font = tkfont.Font(family='Consolas', size=font_size)
        self.tag_configure('md_code', font=code_font, foreground='#f7d195', background='#444444')

        # コードブロック
        self.tag_configure('md_code_block', font=code_font, foreground='#f7d195', background='#2a2a2a')

        # 見出し
        h1_font = tkfont.Font(family=font_family, size=font_size + 4, weight='bold')
        h2_font = tkfont.Font(family=font_family, size=font_size + 2, weight='bold')
        h3_font = tkfont.Font(family=font_family, size=font_size + 1, weight='bold')
        self.tag_configure('md_h1', font=h1_font, foreground='#87CEEB')
        self.tag_configure('md_h2', font=h2_font, foreground='#87CEEB')
        self.tag_configure('md_h3', font=h3_font, foreground='#98FB98')

        # リスト
        self.tag_configure('md_bullet', foreground='#95f797')

        # テーブル
        self.tag_configure('md_table_header', font=bold_font, foreground='#87CEEB')
        self.tag_configure('md_table_cell', foreground='#ffffff')
        self.tag_configure('md_table_border', foreground='#666666')

    def _render_markdown(self, text: str) -> None:
        """Markdown形式のテキストをレンダリングして表示"""
        lines = text.split('\n')
        in_code_block = False
        code_block_content = []
        table_rows = []
        in_table = False

        for i, line in enumerate(lines):
            # コードブロックの開始/終了
            if line.strip().startswith('```'):
                if in_code_block:
                    # コードブロック終了
                    code_text = '\n'.join(code_block_content)
                    if code_text:
                        self.insert(tk.END, code_text + '\n', 'md_code_block')
                    code_block_content = []
                    in_code_block = False
                else:
                    # コードブロック開始
                    in_code_block = True
                continue

            if in_code_block:
                code_block_content.append(line)
                continue

            # テーブル行の検出
            if '|' in line and line.strip().startswith('|'):
                # セパレータ行（|---|---| など）をスキップ
                if re.match(r'^\|[\s\-:]+\|', line.strip()):
                    continue
                table_rows.append(line)
                in_table = True
                continue
            elif in_table:
                # テーブル終了
                self._render_table(table_rows)
                table_rows = []
                in_table = False

            # 見出し
            if line.startswith('### '):
                self.insert(tk.END, line[4:] + '\n', 'md_h3')
                continue
            elif line.startswith('## '):
                self.insert(tk.END, line[3:] + '\n', 'md_h2')
                continue
            elif line.startswith('# '):
                self.insert(tk.END, line[2:] + '\n', 'md_h1')
                continue

            # リスト項目（Markdown形式: -, *, +）
            list_match = re.match(r'^(\s*)[-*+]\s+(.*)$', line)
            if list_match:
                indent = list_match.group(1)
                content = list_match.group(2)
                self.insert(tk.END, indent + '- ', 'md_bullet')
                self._render_inline_markdown(content)
                self.insert(tk.END, '\n')
                continue

            # AIが出力する既存のビュレットリスト（•で始まる行）
            bullet_match = re.match(r'^(\s*)•\s*(.*)$', line)
            if bullet_match:
                indent = bullet_match.group(1)
                content = bullet_match.group(2)
                self.insert(tk.END, indent + '- ', 'md_bullet')
                self._render_inline_markdown(content)
                self.insert(tk.END, '\n')
                continue

            # 番号付きリスト（セクション番号も含む: 1. 2. 等）
            num_list_match = re.match(r'^(\s*)(\d+)\.\s*(.*)$', line)
            if num_list_match:
                indent = num_list_match.group(1)
                num = num_list_match.group(2)
                content = num_list_match.group(3)
                self.insert(tk.END, indent + num + '. ', 'md_bullet')
                self._render_inline_markdown(content)
                self.insert(tk.END, '\n')
                continue

            # 通常の行（インラインMarkdownを処理）
            if line.strip():
                self._render_inline_markdown(line)
                self.insert(tk.END, '\n')
            else:
                self.insert(tk.END, '\n')

        # 最後にテーブルが残っていたらレンダリング
        if table_rows:
            self._render_table(table_rows)

    def _render_table(self, rows: list) -> None:
        """Markdownテーブルを見やすいリスト形式でレンダリング"""
        if not rows:
            return

        # 各行をパースしてセルを取得
        parsed_rows = []
        for row in rows:
            # 先頭と末尾の | を除去してセルを分割
            cells = [cell.strip() for cell in row.strip().strip('|').split('|')]
            parsed_rows.append(cells)

        if not parsed_rows:
            return

        # ヘッダー行を取得
        headers = parsed_rows[0] if parsed_rows else []
        data_rows = parsed_rows[1:] if len(parsed_rows) > 1 else []

        # 2列の場合：キー: 値 形式で表示
        if len(headers) == 2 and data_rows:
            # ヘッダー表示
            self.insert(tk.END, f"[{headers[0]}] -> [{headers[1]}]\n", 'md_table_header')
            self.insert(tk.END, '-' * 30 + '\n', 'md_table_border')

            for data_row in data_rows:
                if len(data_row) >= 2:
                    self.insert(tk.END, '* ', 'md_bullet')
                    self.insert(tk.END, data_row[0], 'md_table_header')
                    self.insert(tk.END, '\n  ', 'md_table_border')
                    self.insert(tk.END, data_row[1] + '\n', 'md_table_cell')
            self.insert(tk.END, '\n')

        # 3列以上の場合：各行をカード形式で表示
        elif len(headers) >= 3 and data_rows:
            for data_row in data_rows:
                self.insert(tk.END, '+' + '-' * 25 + '\n', 'md_table_border')
                for i, cell in enumerate(data_row):
                    if i < len(headers):
                        self.insert(tk.END, f'| {headers[i]}: ', 'md_table_header')
                        self.insert(tk.END, f'{cell}\n', 'md_table_cell')
                self.insert(tk.END, '+' + '-' * 25 + '\n', 'md_table_border')

        # データ行がない場合（ヘッダーのみ）
        else:
            for i, header in enumerate(headers):
                self.insert(tk.END, f'• {header}', 'md_table_header')
                if i < len(headers) - 1:
                    self.insert(tk.END, ' | ', 'md_table_border')
            self.insert(tk.END, '\n')

    def _render_inline_markdown(self, text: str) -> None:
        """インラインMarkdown（太字、イタリック、コード）をレンダリング"""
        # パターン: **bold**, *italic*, `code`
        patterns = [
            (r'\*\*(.+?)\*\*', 'md_bold'),      # **bold**
            (r'\*(.+?)\*', 'md_italic'),         # *italic*
            (r'`(.+?)`', 'md_code'),             # `code`
        ]

        # 全てのマッチを見つけて位置とタイプを記録
        matches = []
        for pattern, tag in patterns:
            for match in re.finditer(pattern, text):
                matches.append({
                    'start': match.start(),
                    'end': match.end(),
                    'content': match.group(1),
                    'tag': tag
                })

        # 位置でソート
        matches.sort(key=lambda x: x['start'])

        # 重複を除去（より長いマッチを優先）
        filtered_matches = []
        last_end = 0
        for m in matches:
            if m['start'] >= last_end:
                filtered_matches.append(m)
                last_end = m['end']

        # テキストをレンダリング
        pos = 0
        for m in filtered_matches:
            # マッチ前のテキスト
            if m['start'] > pos:
                self.insert(tk.END, text[pos:m['start']])
            # マッチしたテキスト
            self.insert(tk.END, m['content'], m['tag'])
            pos = m['end']

        # 残りのテキスト
        if pos < len(text):
            self.insert(tk.END, text[pos:])

    def _get_message(self, key: str, **kwargs) -> str:
        """設定された言語に基づいてメッセージを取得"""
        response_language = config.get('Settings', 'response_language', fallback='JA')
        message = MESSAGES.get(response_language, MESSAGES['JA']).get(key, key)

        if kwargs:
            message = message.format(**kwargs)

        return message

    def _handle_mouse_wheel(self, event) -> Optional[str]:
        """マウスホイールでフォントサイズを変更（Ctrl+ホイール）"""
        if event.state & 0x0004:  # Ctrl押下時
            import time

            current_time = time.time()
            if current_time - self._last_font_change_time < 0.1:  # 100msスロットル
                return "break"

            self._last_font_change_time = current_time

            current_font = self.cget("font")
            if isinstance(current_font, str):
                font_parts = current_font.split()
                font_family = font_parts[0]
                try:
                    font_size = int(font_parts[1])
                except (IndexError, ValueError):
                    font_size = 11
            else:
                font_family = current_font[0] if len(current_font) > 0 else 'Segoe UI Emoji'
                font_size = current_font[1] if len(current_font) > 1 else 11

            new_size = font_size + (1 if event.delta > 0 else -1)
            new_size = max(8, min(24, new_size))

            self.config(font=(font_family, new_size))

            if self._on_font_size_change:
                self._on_font_size_change(new_size)

            return "break"

        return None

    def _has_markdown(self, text: str) -> bool:
        """テキストにMarkdown記法が含まれているか判定"""
        md_patterns = [
            r'\*\*.+?\*\*',      # **bold**
            r'(?<!\*)\*(?!\*).+?(?<!\*)\*(?!\*)',  # *italic* (not **)
            r'`.+?`',            # `code`
            r'^#{1,3}\s',        # # heading
            r'^[-*+]\s',         # - list
            r'^\d+\.\s',         # 1. numbered list
            r'```',              # code block
            r'^\|.+\|$',         # | table |
            r'^•\s',             # • bullet (AI output pattern)
        ]
        for pattern in md_patterns:
            if re.search(pattern, text, re.MULTILINE):
                return True
        return False

    def log_message(self, message: str, use_markdown: bool = True) -> None:
        """ログメッセージを表示（Markdown対応）"""
        self.configure(state='normal')

        input_label = self._get_message('input_label')
        translated_label = self._get_message('translated_label')
        dict_meaning_label = self._get_message('dict_meaning_label')
        local_dict_label = self._get_message('local_dict_label')
        claude_api_error = self._get_message('claude_api_error')

        if claude_api_error in message or ("API" in message and ("エラー" in message or "error" in message.lower())):
            self.insert(tk.END, message, 'error_tag')
        elif input_label in message:
            parts = message.split(input_label, 1)
            self.insert(tk.END, parts[0])
            self.insert(tk.END, input_label, 'input_tag')
            self.insert(tk.END, parts[1] if len(parts) > 1 else "")
        elif translated_label in message:
            parts = message.split(translated_label, 1)
            self.insert(tk.END, parts[0])
            self.insert(tk.END, translated_label, 'translated_tag')
            self.insert(tk.END, parts[1] if len(parts) > 1 else "")
        elif dict_meaning_label in message:
            parts = message.split(dict_meaning_label, 1)
            self.insert(tk.END, parts[0])
            self.insert(tk.END, dict_meaning_label, 'dict_tag')
            # 辞書の内容はMarkdownでレンダリング
            content = parts[1] if len(parts) > 1 else ""
            if use_markdown and self._has_markdown(content):
                self._render_markdown(content)
            else:
                self.insert(tk.END, content)
        elif local_dict_label in message:
            parts = message.split(local_dict_label, 1)
            self.insert(tk.END, parts[0])
            self.insert(tk.END, local_dict_label, 'offline_tag')
            self.insert(tk.END, parts[1] if len(parts) > 1 else "")
        else:
            # 一般メッセージでMarkdownが含まれていればレンダリング
            if use_markdown and self._has_markdown(message):
                self._render_markdown(message)
            else:
                self.insert(tk.END, message)

        self.insert(tk.END, '\n')
        self.configure(state='disabled')
        self.see(tk.END)

    def log_tutor_message(self, message: str, is_user: bool = True) -> None:
        """家庭教師モードのメッセージを表示（Markdown対応）"""
        self.configure(state='normal')

        if is_user:
            self.insert(tk.END, "\n[あなた] ", 'tutor_user_tag')
            self.insert(tk.END, message + "\n")
        else:
            self.insert(tk.END, "\n[先生] ", 'tutor_ai_tag')
            # AIの返答はMarkdownでレンダリング
            if self._has_markdown(message):
                self._render_markdown(message)
            else:
                self.insert(tk.END, message + "\n")

        self.configure(state='disabled')
        self.see(tk.END)

    def copy_selected(self, clipboard_clear: Callable, clipboard_append: Callable) -> bool:
        """選択されたテキストをコピー"""
        self.configure(state='normal')
        try:
            selected_text = self.get(tk.SEL_FIRST, tk.SEL_LAST)
            if selected_text:
                clipboard_clear()
                clipboard_append(selected_text)
                return True
        except tk.TclError:
            pass
        finally:
            self.configure(state='disabled')
        return False

    def select_all(self) -> None:
        """テキストをすべて選択"""
        self.configure(state='normal')
        self.tag_add(tk.SEL, "1.0", tk.END)
        self.mark_set(tk.INSERT, "1.0")
        self.see(tk.INSERT)
        self.configure(state='disabled')

    def clear(self) -> None:
        """テキストエリアをクリア"""
        self.configure(state='normal')
        self.delete("1.0", tk.END)
        self.configure(state='disabled')
