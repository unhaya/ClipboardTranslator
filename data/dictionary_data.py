# 基本的な単語データ
COMMON_JA_WORDS = {
    '保存': 'save', '開く': 'open', '閉じる': 'close', '終了': 'exit', '削除': 'delete',
    'ファイル': 'file', 'フォルダ': 'folder', '設定': 'settings', '編集': 'edit',
    'コピー': 'copy', '貼り付け': 'paste', '切り取り': 'cut', '元に戻す': 'undo',
    'やり直し': 'redo', '検索': 'search', '置換': 'replace', '選択': 'select',
    'すべて': 'all', '新規': 'new', '印刷': 'print', '表示': 'display',
    'ヘルプ': 'help', 'ツール': 'tools', 'ウィンドウ': 'window', '確認': 'confirm',
    'キャンセル': 'cancel', 'はい': 'yes', 'いいえ': 'no', '適用': 'apply',

    '名前を付けて保存': 'save as', '上書き保存': 'overwrite save', '最近使ったファイル': 'recent files',
    '復元': 'restore', '破棄': 'discard', '同期': 'sync', '非同期': 'async',
    '圧縮': 'compress', '解凍': 'extract', '暗号化': 'encrypt', '復号': 'decrypt',
    'スクリーンショット': 'screenshot', 'クリップボード': 'clipboard', '選択範囲': 'selection',
    'すべて選択': 'select all', '部分選択': 'select partial', '複製': 'duplicate',
    'ドラッグ': 'drag', 'ドロップ': 'drop', 'スクロール': 'scroll',
    'ズームイン': 'zoom in', 'ズームアウト': 'zoom out', 'リサイズ': 'resize',
    'リネーム': 'rename', 'フォーマット': 'format', 'プロパティ': 'properties',
    'プレビュー': 'preview', 'アップロード': 'upload', 'ダウンロード': 'download',
    'エクスポート': 'export', 'インポート': 'import', 'リストア': 'restore',
    'バックアップ': 'backup', 'アーカイブ': 'archive', '削除済み': 'deleted',
    'ゴミ箱': 'trash', '復元ポイント': 'restore point', '履歴': 'history',
    '再試行': 'retry', 'スキップ': 'skip', '適用する': 'apply changes',
    '初期化': 'initialize', 'デフォルトに戻す': 'reset to default',
    '設定を保存': 'save settings', '設定を適用': 'apply settings', '設定をリセット': 'reset settings',
    '変更を保存': 'save changes', '変更を適用': 'apply changes', '変更を破棄': 'discard changes',
    '編集モード': 'edit mode', 'ビュー': 'view', 'レイアウト': 'layout',
    'ウィンドウサイズ': 'window size', 'ウィンドウを最大化': 'maximize window',
    'ウィンドウを最小化': 'minimize window', 'ウィンドウを閉じる': 'close window',
    '全画面表示': 'fullscreen', 'ウィンドウを復元': 'restore window',
    'アクティブウィンドウ': 'active window', '非アクティブウィンドウ': 'inactive window',
    'タブを開く': 'open tab', 'タブを閉じる': 'close tab', 'タブを複製': 'duplicate tab',
    '新しいタブ': 'new tab', '前のタブ': 'previous tab', '次のタブ': 'next tab',
    'ページを更新': 'refresh page', 'ページの履歴': 'page history',
    'ページを閉じる': 'close page', 'ページを拡大': 'zoom in page',
    'ページを縮小': 'zoom out page', 'スクロールアップ': 'scroll up',
    'スクロールダウン': 'scroll down', 'スクロールをリセット': 'reset scroll',
    
    # コンピューター関連の単語を拡張
    'デバイス': 'device', 'ネットワーク': 'network', 'インターネット': 'internet', 'サーバー': 'server',
    'クラウド': 'cloud', 'ダウンロード': 'download', 'アップロード': 'upload', 'ストレージ': 'storage',
    'アカウント': 'account', 'ログイン': 'login', 'ログアウト': 'logout', 'パスワード': 'password',
    'セキュリティ': 'security', '暗号化': 'encryption', 'バックアップ': 'backup', '復元': 'restore',

    'ワイヤレス': 'wireless', '有線': 'wired', 'ルーター': 'router', 'スイッチ': 'switch',
    'IPアドレス': 'IP address', 'サブネット': 'subnet', 'DNS': 'DNS', 'ゲートウェイ': 'gateway',
    'ファイアウォール': 'firewall', 'VPN': 'VPN', 'プロキシ': 'proxy', 'LAN': 'LAN', 'WAN': 'WAN',
    'SSID': 'SSID', 'Wi-Fi': 'Wi-Fi', 'Bluetooth': 'Bluetooth', 'NFC': 'NFC',

    'ホスト': 'host', 'クライアント': 'client', 'サーバークライアント': 'server-client',
    'データセンター': 'data center', '仮想化': 'virtualization', 'クラスタリング': 'clustering',
    'ロードバランサー': 'load balancer', 'CDN': 'CDN', 'データ転送': 'data transfer',

    'ファイルシステム': 'file system', 'ディレクトリ': 'directory', 'パーティション': 'partition',
    'フォーマット': 'format', 'RAID': 'RAID', 'ハードディスク': 'hard disk', 'SSD': 'SSD',
    'RAM': 'RAM', 'ROM': 'ROM', 'キャッシュ': 'cache', 'ページング': 'paging',

    'セッション': 'session', 'クッキー': 'cookie', 'トークン': 'token', 'ハッシュ': 'hash',
    '認証': 'authentication', '多要素認証': 'multi-factor authentication', 'OAuth': 'OAuth',
    'SSO': 'SSO', 'APIキー': 'API key', '電子署名': 'digital signature', 'バイオメトリクス': 'biometrics',

    'オペレーティングシステム': 'operating system', 'Windows': 'Windows', 'Linux': 'Linux',
    'MacOS': 'MacOS', 'Android': 'Android', 'iOS': 'iOS', 'Unix': 'Unix',

    'プロセス': 'process', 'スレッド': 'thread', 'メモリ管理': 'memory management',
    'タスクマネージャー': 'task manager', 'リソースモニター': 'resource monitor',

    'ソフトウェア': 'software', 'ハードウェア': 'hardware', 'ドライバー': 'driver',
    'ファームウェア': 'firmware', 'アップデート': 'update', 'パッチ': 'patch',
    'オープンソース': 'open source', 'プロプライエタリ': 'proprietary',

    'プログラミング言語': 'programming language', 'コンパイラ': 'compiler',
    'インタープリタ': 'interpreter', 'スクリプト': 'script', 'ライブラリ': 'library',
    'フレームワーク': 'framework', 'データベース': 'database', 'SQL': 'SQL',
    'NoSQL': 'NoSQL', 'クエリ': 'query', 'インデックス': 'index',

    'クラウドストレージ': 'cloud storage', '分散コンピューティング': 'distributed computing',
    '仮想マシン': 'virtual machine', 'コンテナ': 'container', 'Docker': 'Docker',
    'Kubernetes': 'Kubernetes', 'サーバーレス': 'serverless',

    'マルウェア': 'malware', 'ウイルス': 'virus', 'スパイウェア': 'spyware',
    'ランサムウェア': 'ransomware', 'フィッシング': 'phishing', 'ゼロデイ攻撃': 'zero-day attack',
    'エクスプロイト': 'exploit', 'ペネトレーションテスト': 'penetration test',

    'IoT': 'IoT', 'スマートホーム': 'smart home', 'ウェアラブル': 'wearable',

    '人工知能': 'artificial intelligence', '機械学習': 'machine learning',
    'ディープラーニング': 'deep learning', 'ニューラルネットワーク': 'neural network',
    'データマイニング': 'data mining', 'ビッグデータ': 'big data', 'クラスタ分析': 'cluster analysis',

    # ビジネス・オフィス関連の単語を拡張
    '会議': 'meeting', '議事録': 'minutes', 'スケジュール': 'schedule', 'カレンダー': 'calendar',
    '経理': 'accounting', '予算': 'budget', '請求書': 'invoice', '契約': 'contract',
    '売上': 'sales', '利益': 'profit', '支出': 'expense', '取引': 'transaction',

    '商談': 'business negotiation', '交渉': 'negotiation', 'プレゼンテーション': 'presentation',
    '報告書': 'report', '提案書': 'proposal', '稟議書': 'approval request', '会議室': 'conference room',
    '取締役会': 'board meeting', '決算': 'settlement of accounts', '財務諸表': 'financial statement',

    '請求': 'billing', '支払期限': 'payment deadline', '未払い': 'outstanding payment',
    '売掛金': 'accounts receivable', '買掛金': 'accounts payable', '入金': 'deposit',
    '出金': 'withdrawal', '送金': 'remittance', '資産': 'asset', '負債': 'liability',

    'マーケティング': 'marketing', '広告': 'advertisement', '販促': 'promotion',
    'ブランディング': 'branding', '市場調査': 'market research', 'ターゲット市場': 'target market',
    '売上目標': 'sales target', '顧客管理': 'customer management', 'CRM': 'CRM',
    'リード': 'lead', 'コンバージョン率': 'conversion rate',

    '従業員': 'employee', '人事': 'human resources', '採用': 'recruitment',
    '面接': 'interview', '履歴書': 'resume', '雇用契約': 'employment contract',
    '昇進': 'promotion', '昇給': 'salary increase', '退職': 'resignation',
    '福利厚生': 'employee benefits', '有給休暇': 'paid leave', '勤怠管理': 'attendance management',

    'プロジェクト管理': 'project management', 'タスク': 'task', 'ガントチャート': 'Gantt chart',
    '進捗': 'progress', '期限': 'deadline', '納期': 'delivery date',
    'リスク管理': 'risk management', '優先順位': 'priority', 'チームワーク': 'teamwork',
    'リーダーシップ': 'leadership', 'スキル': 'skill', 'キャリアパス': 'career path',

    'オフィス': 'office', 'デスクワーク': 'desk work', 'リモートワーク': 'remote work',
    '在宅勤務': 'telecommuting', '出張': 'business trip', '出勤': 'going to work',
    '退勤': 'leaving work', '会計年度': 'fiscal year', '売上報告': 'sales report',
    '経費精算': 'expense reimbursement', '財務管理': 'financial management',
    '経営戦略': 'business strategy', '投資': 'investment', '株式': 'stocks',

    '商標': 'trademark', '特許': 'patent', '著作権': 'copyright', '知的財産': 'intellectual property',
    '法務': 'legal affairs', '規約': 'terms and conditions', 'コンプライアンス': 'compliance',
    '個人情報保護': 'data protection', '監査': 'audit', 'ガバナンス': 'governance',
    '内部統制': 'internal control', 'リスクアセスメント': 'risk assessment',

    'クライアント': 'client', '顧客': 'customer', '取引先': 'business partner',
    '契約書': 'contract document', '発注': 'order', '納品': 'delivery', '返品': 'return',
    'クレーム': 'complaint', '苦情処理': 'grievance handling', '品質管理': 'quality control',
    'アフターサービス': 'after-sales service', 'サポートセンター': 'support center',

    '会員': 'member', '会費': 'membership fee', '定期購読': 'subscription',
    'キャンペーン': 'campaign', 'プロモーション': 'promotion', 'スポンサー': 'sponsor',
    '寄付': 'donation', 'ボランティア': 'volunteer',

    '電子契約': 'electronic contract', 'クラウド会計': 'cloud accounting',
    '電子請求書': 'electronic invoice', 'デジタルサイン': 'digital signature',

    # プログラミング関連の単語を拡張
    'コード': 'code', 'デバッグ': 'debug', 'エラー': 'error', '変数': 'variable',
    '関数': 'function', 'クラス': 'class', 'オブジェクト': 'object', 'ループ': 'loop',
    '条件': 'condition', '例外': 'exception', 'モジュール': 'module', 'ライブラリ': 'library',

    'フレームワーク': 'framework', 'スクリプト': 'script', 'パラメータ': 'parameter',
    '引数': 'argument', '戻り値': 'return value', 'ポインタ': 'pointer', '参照': 'reference',
    'コンストラクタ': 'constructor', 'デストラクタ': 'destructor', 'インターフェース': 'interface',
    '継承': 'inheritance', 'ポリモーフィズム': 'polymorphism', 'カプセル化': 'encapsulation',

    'コンパイル': 'compile', 'コンパイラ': 'compiler', 'インタープリタ': 'interpreter',
    'バグ': 'bug', 'パッチ': 'patch', 'リファクタリング': 'refactoring', 'リリース': 'release',
    'ビルド': 'build', 'デプロイ': 'deploy', 'バージョン管理': 'version control',
    'リポジトリ': 'repository', 'コミット': 'commit', 'プルリクエスト': 'pull request',
    'マージ': 'merge', 'ブランチ': 'branch', 'タグ': 'tag', 'チェックアウト': 'checkout',

    'シンタックス': 'syntax', '構文解析': 'parsing', 'AST': 'abstract syntax tree',
    'コンパイルエラー': 'compile error', '実行時エラー': 'runtime error',
    'セグメンテーションフォルト': 'segmentation fault', 'メモリリーク': 'memory leak',

    'アルゴリズム': 'algorithm', 'データ構造': 'data structure', 'スタック': 'stack',
    'キュー': 'queue', '配列': 'array', 'リスト': 'list', '連結リスト': 'linked list',
    '辞書': 'dictionary', 'ハッシュテーブル': 'hash table', 'グラフ': 'graph',
    'ツリー': 'tree', 'バイナリツリー': 'binary tree', '探索': 'search',
    'ソート': 'sort', 'バブルソート': 'bubble sort', 'クイックソート': 'quick sort',

    'データベース': 'database', 'SQL': 'SQL', 'NoSQL': 'NoSQL', 'クエリ': 'query',
    'トランザクション': 'transaction', 'ACID': 'ACID', '正規化': 'normalization',
    'インデックス': 'index', 'キャッシュ': 'cache', 'キー': 'key',

    'API': 'API', 'REST': 'REST', 'GraphQL': 'GraphQL', 'WebSocket': 'WebSocket',
    'マイクロサービス': 'microservices', 'サーバーレス': 'serverless',

    'フロントエンド': 'frontend', 'バックエンド': 'backend', 'フルスタック': 'full stack',
    'レンダリング': 'rendering', 'レスポンシブデザイン': 'responsive design',

    'シェルスクリプト': 'shell script', 'バッチファイル': 'batch file',
    '正規表現': 'regular expression', 'コマンドライン': 'command line',
    'オートメーション': 'automation', 'CI/CD': 'CI/CD', 'コンテナ': 'container',
    'Docker': 'Docker', 'Kubernetes': 'Kubernetes',

    'マルチスレッド': 'multithreading', '並列処理': 'parallel processing',
    '非同期処理': 'asynchronous processing', 'イベント駆動': 'event-driven',

    # デザイン・クリエイティブ関連の単語を拡張
    '画像': 'image', '写真': 'photo', '解像度': 'resolution', 'フォント': 'font',
    'レイヤー': 'layer', 'フィルター': 'filter', '編集': 'edit', 'アート': 'art',
    'イラスト': 'illustration', 'デザイン': 'design', 'ポスター': 'poster',
    'グラフィック': 'graphic', 'ビジュアル': 'visual', 'タイポグラフィ': 'typography',
    'カラーパレット': 'color palette', 'グリッド': 'grid', 'レイアウト': 'layout',
    'コンポジション': 'composition', 'アイコン': 'icon', 'ピクトグラム': 'pictogram',
    'シンボル': 'symbol', 'ロゴ': 'logo', 'トリミング': 'trimming', 'クリッピング': 'clipping',
    'マスキング': 'masking', 'ベクター': 'vector', 'ラスター': 'raster',

    '3Dモデリング': '3D modeling', 'レンダリング': 'rendering', 'テクスチャ': 'texture',
    'ライティング': 'lighting', 'シェーディング': 'shading', 'リギング': 'rigging',
    'アニメーション': 'animation', 'フレームレート': 'frame rate', 'キーフレーム': 'keyframe',
    'パーティクル': 'particle', 'スカルプティング': 'sculpting', 'マテリアル': 'material',

    '印刷': 'printing', 'CMYK': 'CMYK', 'RGB': 'RGB', 'DPI': 'DPI', 'ピクセル': 'pixel',
    'ビットマップ': 'bitmap', 'アンチエイリアス': 'anti-aliasing', 'シャープネス': 'sharpness',
    'コントラスト': 'contrast', '明るさ': 'brightness', '彩度': 'saturation',
    'グラデーション': 'gradient', 'ハイライト': 'highlight', 'シャドウ': 'shadow',

    '背景': 'background', '透明度': 'transparency', 'オーバーレイ': 'overlay',
    'ブレンドモード': 'blend mode', 'パターン': 'pattern', 'テクスチャマッピング': 'texture mapping',
    'ストローク': 'stroke', 'アウトライン': 'outline', 'ドロップシャドウ': 'drop shadow',
    'エンボス': 'emboss', 'レタッチ': 'retouch', 'ノイズ': 'noise',

    'UIデザイン': 'UI design', 'UXデザイン': 'UX design', 'ワイヤーフレーム': 'wireframe',
    'プロトタイピング': 'prototyping', 'インターフェース': 'interface',
    'レスポンシブデザイン': 'responsive design', 'ユーザビリティ': 'usability',

    '広告デザイン': 'advertisement design', 'パッケージデザイン': 'package design',
    'フライヤー': 'flyer', 'バナー': 'banner', 'ブックカバー': 'book cover',
    'ブランドアイデンティティ': 'brand identity', 'CI': 'corporate identity',

    'デジタルペイント': 'digital painting', 'ブラシ': 'brush', 'ペンツール': 'pen tool',
    'レイヤーマスク': 'layer mask', 'クリッピングマスク': 'clipping mask',
    'スマートオブジェクト': 'smart object', '非破壊編集': 'non-destructive editing',

    # 日常会話・コミュニケーション関連の単語を拡張
    'こんにちは': 'hello', 'ありがとう': 'thank you', 'おめでとう': 'congratulations', 
    'すみません': 'excuse me', '大丈夫': 'okay', '気をつけて': 'take care',
    'おはよう': 'good morning', 'こんばんは': 'good evening', 'さようなら': 'goodbye',
    'またね': 'see you', 'いってきます': 'I’m leaving', 'いってらっしゃい': 'take care (when leaving)',
    'ただいま': 'I’m home', 'おかえり': 'welcome back', 'おやすみ': 'good night',
    'お世話になります': 'thank you for your support', 'よろしくお願いします': 'nice to meet you',
    'ごめんなさい': 'I’m sorry', '申し訳ありません': 'I sincerely apologize',
    '失礼します': 'excuse me (formal)', 'お疲れ様です': 'thank you for your work',
    'ご協力ありがとうございます': 'thank you for your cooperation',

    'いくらですか': 'how much is this?', 'これは何ですか': 'what is this?',
    'どこですか': 'where is it?', 'どうすればいいですか': 'what should I do?',
    '何時ですか': 'what time is it?', 'トイレはどこですか': 'where is the restroom?',
    '英語を話せますか': 'can you speak English?', '日本語を話せますか': 'can you speak Japanese?',
    'もう一度お願いします': 'please say it again', 'ゆっくり話してください': 'please speak slowly',

    '好きです': 'I like it', '嫌いです': 'I don’t like it', '楽しい': 'fun',
    '悲しい': 'sad', '疲れた': 'tired', '嬉しい': 'happy', '腹が立つ': 'angry',
    'お腹が空いた': 'I’m hungry', '喉が渇いた': 'I’m thirsty', '眠い': 'sleepy',
    '痛い': 'it hurts', '寒い': 'cold', '暑い': 'hot', '気持ちいい': 'feels good',

    'よろしく': 'cheers', '乾杯': 'cheers (drinking)', 'がんばって': 'good luck',
    '気にしないで': 'don’t worry', 'それは良かった': 'that’s great', 'それは残念': 'that’s unfortunate',
    '本当ですか': 'is it true?', '冗談です': 'just kidding', 'なんでもない': 'it’s nothing',

    '久しぶり': 'long time no see', '元気ですか': 'how are you?', '私は元気です': 'I’m fine',
    'どこに住んでいますか': 'where do you live?', 'お名前は何ですか': 'what’s your name?',
    '何歳ですか': 'how old are you?', '職業は何ですか': 'what’s your job?',

    '手伝いましょうか': 'shall I help you?', 'お手伝いしましょうか': 'can I assist you?',
    '大変ですね': 'that’s tough', 'すごい': 'amazing', '素晴らしい': 'wonderful',
    '面白い': 'interesting', 'つまらない': 'boring', '危ない': 'dangerous',

    '電話をかけます': 'I’ll make a call', 'メールを送ります': 'I’ll send an email',
    'メッセージを受け取りました': 'I received your message', '返信します': 'I will reply',

    '問題ありません': 'no problem', '準備できました': 'I’m ready', '確認しました': 'I checked it',
    'ちょっと待ってください': 'please wait a moment', '助かります': 'that helps',

    'お願いします': 'please', 'どうぞ': 'go ahead', 'どういたしまして': 'you’re welcome',
    'おめでとうございます': 'congratulations (formal)', 'お気をつけください': 'please be careful',

    # 旅行・移動関連の単語を拡張
    '空港': 'airport', '飛行機': 'airplane', 'ホテル': 'hotel', '予約': 'reservation',
    '電車': 'train', '地下鉄': 'subway', 'タクシー': 'taxi', 'チケット': 'ticket',
    '搭乗券': 'boarding pass', 'ゲート': 'gate', 'チェックイン': 'check-in',
    '手荷物': 'baggage', '手荷物検査': 'security check', '預け荷物': 'checked baggage',
    '荷物受取所': 'baggage claim', '直行便': 'direct flight', '乗り継ぎ': 'transit',
    '遅延': 'delay', '出発': 'departure', '到着': 'arrival', '入国審査': 'immigration',
    '税関': 'customs', 'パスポート': 'passport', 'ビザ': 'visa',

    'レンタカー': 'rental car', '駐車場': 'parking lot', 'バス': 'bus', 'フェリー': 'ferry',
    'バス停': 'bus stop', '改札口': 'ticket gate', '切符売り場': 'ticket office',
    '片道': 'one-way', '往復': 'round-trip', '乗り換え': 'transfer', '終点': 'last stop',
    '車両': 'carriage', '窓側': 'window seat', '通路側': 'aisle seat',

    '観光': 'sightseeing', '地図': 'map', 'ガイド': 'guide', 'ツアー': 'tour',
    '観光地': 'tourist attraction', '入場券': 'admission ticket', '土産': 'souvenir',
    '旅行保険': 'travel insurance', '両替': 'currency exchange', 'ATM': 'ATM',
    '道順': 'directions', '徒歩': 'on foot', '宿泊': 'accommodation', 'チェックアウト': 'check-out',

    # 買い物・支払い関連の単語
    '値段': 'price', 'クレジットカード': 'credit card', '支払い': 'payment',
    '割引': 'discount', '返品': 'return',
    'レシート': 'receipt', '請求書': 'invoice', '現金': 'cash', '小銭': 'coins',
    'お釣り': 'change', 'クーポン': 'coupon', '特売': 'special sale', '免税': 'duty-free',
    '両替所': 'money exchange', '電子マネー': 'electronic money', 'ポイントカード': 'point card',
    '会員割引': 'membership discount', '領収書': 'receipt', '支払方法': 'payment method',
    'カード決済': 'card payment', '分割払い': 'installment payment', '即日払い': 'same-day payment',
    '商品': 'product', '在庫': 'stock', '品切れ': 'out of stock', '数量': 'quantity',
    'サイズ': 'size', 'カラー': 'color', '試着': 'fitting', '試食': 'sampling',
    '特価': 'special price', 'バーゲン': 'bargain', 'セール': 'sale',
    '期間限定': 'limited time offer', '送料無料': 'free shipping', '代引き': 'cash on delivery',
    '配送': 'delivery', '宅配便': 'courier', '追跡番号': 'tracking number', '配送時間': 'delivery time',
    '返品ポリシー': 'return policy', '返金': 'refund', '交換': 'exchange', '保証': 'warranty',
    '修理': 'repair', 'カート': 'cart', 'レジ': 'checkout', '会計': 'checkout',
    '注文': 'order', '予約注文': 'pre-order', 'オンラインショップ': 'online shop',
    'ショッピングモール': 'shopping mall', '店舗': 'store', 'フロア': 'floor',
    'レジ袋': 'shopping bag', 'マイバッグ': 'eco bag', 'ギフト包装': 'gift wrapping',
    '値札': 'price tag', 'タグ': 'tag', '陳列': 'display', '新商品': 'new product',
    '人気商品': 'popular item', 'おすすめ商品': 'recommended item', '売れ筋': 'best seller',
    'ランキング': 'ranking', 'レビュー': 'review', '口コミ': 'word of mouth',
    '店員': 'store clerk', '接客': 'customer service', 'お会計': 'payment',
    '袋は必要ですか': 'do you need a bag?', 'カードは使えますか': 'can I use a card?',
    '返品できますか': 'can I return this?', 'ポイントを使えますか': 'can I use points?',
    '割引はありますか': 'is there a discount?', '領収書をください': 'please give me a receipt',
    # その他の重要単語
    '赤': 'red', '青': 'blue', '黄色': 'yellow', '緑': 'green',
    '一': 'one', '二': 'two', '三': 'three', '四': 'four',
    '朝': 'morning', '昼': 'afternoon', '夜': 'night', '今': 'now',

    # 拡張単語（色）
    '橙色': 'orange', '紫': 'purple', 'ピンク': 'pink', '黒': 'black', '白': 'white',
    '灰色': 'gray', '茶色': 'brown', '金色': 'gold', '銀色': 'silver',

    # 拡張単語（数字）
    '五': 'five', '六': 'six', '七': 'seven', '八': 'eight', '九': 'nine', '十': 'ten',
    '百': 'hundred', '千': 'thousand', '万': 'ten thousand', '億': 'hundred million',

    # 拡張単語（時間）
    '秒': 'second', '分': 'minute', '時間': 'hour', '日': 'day', '週': 'week', 
    '月': 'month', '年': 'year', '昨日': 'yesterday', '今日': 'today', '明日': 'tomorrow',
    '今週': 'this week', '来週': 'next week', '先週': 'last week', '午前': 'morning (AM)',
    '午後': 'afternoon (PM)', '深夜': 'midnight', '正午': 'noon',

    # 拡張単語（方向・位置）
    '上': 'up', '下': 'down', '左': 'left', '右': 'right', '前': 'front', '後ろ': 'back',
    '内側': 'inside', '外側': 'outside', '中央': 'center', '端': 'edge',

    # 拡張単語（頻度）
    'いつも': 'always', 'たまに': 'sometimes', 'よく': 'often', 'まれに': 'rarely',
    '一度': 'once', '二度': 'twice', '毎日': 'every day', '毎週': 'every week',
    '毎月': 'every month', '毎年': 'every year',

    # 拡張単語（単位）
    'キログラム': 'kilogram', 'グラム': 'gram', 'メートル': 'meter', 'センチメートル': 'centimeter',
    'リットル': 'liter', 'ミリリットル': 'milliliter', 'ワット': 'watt', 'ヘルツ': 'hertz',

    # 拡張単語（状態・程度）
    '大きい': 'big', '小さい': 'small', '高い': 'high', '低い': 'low', '長い': 'long',
    '短い': 'short', '速い': 'fast', '遅い': 'slow', '強い': 'strong', '弱い': 'weak',
    '明るい': 'bright', '暗い': 'dark', '暑い': 'hot', '寒い': 'cold',

    # 拡張単語（形状）
    '丸い': 'round', '四角い': 'square', '三角形': 'triangle', '長方形': 'rectangle',
    '楕円形': 'oval', '星形': 'star-shaped', 'ハート形': 'heart-shaped',

    # 拡張単語（感情・状態）
    '楽しい': 'fun', '悲しい': 'sad', '嬉しい': 'happy', '怒っている': 'angry',
    '疲れた': 'tired', '興奮している': 'excited', '緊張している': 'nervous',

    # 拡張単語（基本動詞）
    '行く': 'go', '来る': 'come', '見る': 'see', '聞く': 'hear', '話す': 'speak',
    '食べる': 'eat', '飲む': 'drink', '寝る': 'sleep', '起きる': 'wake up',

}

# 逆引き辞書を自動生成
COMMON_EN_WORDS = {v: k for k, v in COMMON_JA_WORDS.items()}

# dictionary_data.pyに以下の関数を追加
def get_dictionary_size():
    """辞書のサイズを返す関数"""
    return {
        'ja': len(COMMON_JA_WORDS),
        'en': len(COMMON_EN_WORDS),
        'total': len(COMMON_JA_WORDS) + len(COMMON_EN_WORDS)
    }

# NGSLの辞書を取得する関数
def get_ngsl_dictionary():
    """NGSL辞書を返す関数"""
    # グローバル変数として定義されていなければ空の辞書を返す
    global NGSL_DICTIONARY
    if 'NGSL_DICTIONARY' not in globals():
        NGSL_DICTIONARY = {}
    return NGSL_DICTIONARY

# NGSL辞書をロードする関数
def load_ngsl_data(file_path):
    """NGSL辞書をCSVファイルから読み込む関数"""
    try:
        import csv
        global NGSL_DICTIONARY
        if 'NGSL_DICTIONARY' not in globals():
            NGSL_DICTIONARY = {}
        
        count = 0
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'entry' in row and 'meaning' in row:
                    english_word = row['entry'].strip().lower()
                    japanese_meaning = row['meaning'].strip()
                    if english_word and japanese_meaning:
                        NGSL_DICTIONARY[english_word] = japanese_meaning
                        count += 1
        return count
    except Exception as e:
        print(f"NGSL辞書の読み込みに失敗しました: {e}")
        return 0