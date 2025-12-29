# ClipboardTranslator v1.10 - TutorController
"""
家庭教師（RAGチャット）処理を担当するコントローラー
"""
from typing import Callable


class TutorController:
    """家庭教師処理コントローラー"""

    def __init__(
        self,
        tutor_handler,
        on_log_tutor: Callable[[str, bool], None],
        on_status: Callable[[str], None],
        on_status_text: Callable[[str], None]
    ):
        """
        初期化

        Parameters:
            tutor_handler: TutorChatHandler インスタンス
            on_log_tutor: 家庭教師メッセージ表示コールバック (message, is_user)
            on_status: ステータス更新コールバック
            on_status_text: ステータステキスト直接設定コールバック
        """
        self.tutor_handler = tutor_handler
        self._on_log_tutor = on_log_tutor
        self._on_status = on_status
        self._on_status_text = on_status_text

    def process_message(self, message: str) -> None:
        """
        家庭教師モードのメッセージを処理

        Parameters:
            message: ユーザーからのメッセージ
        """
        def on_success(response: str) -> None:
            self._on_log_tutor(response, False)
            self._on_status('待機中...')

        def on_error(error_msg: str) -> None:
            self._on_log_tutor(error_msg, False)
            self._on_status('error_occurred')

        def on_search_info(metadata: dict) -> None:
            """検索情報をステータスに表示"""
            count = metadata.get('count', 0)
            dates = metadata.get('dates', [])

            if count > 0 and dates:
                date_str = ', '.join(dates[:2])
                if len(dates) > 2:
                    date_str += '等'
                status_text = f"履歴{count}件を参照中 ({date_str})"
            elif count > 0:
                status_text = f"履歴{count}件を参照中..."
            else:
                status_text = "考え中..."

            self._on_status_text(status_text)

        self.tutor_handler.process_message(
            message,
            on_success=on_success,
            on_error=on_error,
            on_search_info=on_search_info
        )
