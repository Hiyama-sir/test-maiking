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
2. 環境変数は設定不要
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

## 注意事項

- 実際のExcelファイルは`.gitignore`で除外されています
- ローカル環境では実際のファイルを配置してください
- Renderではサンプルファイルが利用可能です