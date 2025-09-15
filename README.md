# テスト問題ジェネレーター

FlaskアプリケーションでExcelファイルから単語を選択してテストを作成できます。

## 機能

- 3つの単語集から選択可能（コーパス4500、ターゲット1900、システム英単語）
- 個別選択、範囲選択、ランダム選択
- 大きな解答欄（400px × 100px）
- 問題用紙と回答用紙の分離印刷
- 1列全幅レイアウト

## セットアップ

### ローカル環境

1. リポジトリをクローン
```bash
git clone https://github.com/Hiyama-sir/test-maiking.git
cd test-maiking
```

2. 仮想環境を作成・有効化
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 依存関係をインストール
```bash
pip install -r requirements.txt
```

4. Excelファイルを配置
以下のファイルをプロジェクトルートに配置してください：
- `小テスト Retrieved from コーパス4500 4th Edition.xlsx`
- `ターゲット1900.xlsx`
- `システム英単語.xlsx`

5. アプリケーションを起動
```bash
python app.py
```

### Renderデプロイ

1. GitHubリポジトリをRenderに接続
2. 環境変数を設定（問い合わせフォーム機能を使用する場合）:
   - `CONTACT_EMAIL`: 問い合わせ先メールアドレス
   - `SMTP_USERNAME`: SMTPユーザー名
   - `SMTP_PASSWORD`: SMTPパスワード
   - `SMTP_SERVER`: SMTPサーバー（デフォルト: smtp.gmail.com）
   - `SMTP_PORT`: SMTPポート（デフォルト: 587）
3. デプロイ後、サンプルファイルが利用可能

## 使用方法

1. ファイル選択ドロップダウンで単語集を選択
2. 単語を選択（個別、範囲、ランダム）
3. 「選択した単語でテスト作成」をクリック
4. 問題用紙または回答用紙を印刷

## ファイル構成

```
test-maiking/
├── app.py                 # メインアプリケーション
├── templates/
│   └── index.html        # フロントエンド
├── sample_data/          # サンプルファイル（Gitに含まれる）
├── requirements.txt      # 依存関係
├── .gitignore           # Git除外設定
└── README.md            # このファイル
```

## 環境変数設定

問い合わせフォーム機能を使用する場合は、以下の環境変数を設定してください：

```bash
# 問い合わせ先メールアドレス
CONTACT_EMAIL=your-email@example.com

# SMTP設定（Gmailの場合）
SMTP_USERNAME=your-gmail@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

### Gmail設定の注意事項
- Gmailを使用する場合は、アプリパスワードを設定してください
- 通常のパスワードではなく、2段階認証のアプリパスワードが必要です
- アプリパスワードは Googleアカウント設定 > セキュリティ > 2段階認証 > アプリパスワード で生成できます

## 注意事項

- 実際のExcelファイルは`.gitignore`で除外されています
- ローカル環境では実際のファイルを配置してください
- Renderではサンプルファイルが利用可能です
- 環境変数は本番環境でのみ設定し、Gitには含めないでください