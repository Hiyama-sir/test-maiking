# EC2への簡単デプロイ手順（手動）

EC2 Instance Connectで接続後、以下のコマンドを順番に実行してください。

## 1. 必要なパッケージをインストール

```bash
sudo yum update -y
sudo yum install -y python3 python3-pip git
```

## 2. プロジェクトをクローン

```bash
cd /opt
sudo mkdir -p quiz-generator
sudo chown ec2-user:ec2-user quiz-generator
git clone https://github.com/Hiyama-sir/test-maiking.git quiz-generator
cd quiz-generator
```

## 3. 仮想環境を作成

```bash
python3 -m venv venv
source venv/bin/activate
```

## 4. 依存関係をインストール

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 5. アプリケーションを起動（テスト用）

まずは手動で起動して動作確認：

```bash
gunicorn --bind 0.0.0.0:8000 app:app
```

バックグラウンドで実行する場合：
```bash
nohup gunicorn --bind 0.0.0.0:8000 app:app > /tmp/app.log 2>&1 &
```

## 6. アクセス確認

ブラウザで以下のURLにアクセス：
```
http://13.210.236.134:8000
```

（IPアドレスはEC2インスタンスのパブリックIPに置き換えてください）

---

## systemdサービスとして設定（常時起動）

上記で動作確認できたら、systemdサービスとして設定します：

### 1. サービスファイルを作成

```bash
sudo tee /etc/systemd/system/quiz-generator.service > /dev/null <<'EOF'
[Unit]
Description=Quiz Generator Flask Application
After=network.target

[Service]
Type=simple
User=ec2-user
Group=ec2-user
WorkingDirectory=/opt/quiz-generator
Environment="PATH=/opt/quiz-generator/venv/bin"
ExecStart=/opt/quiz-generator/venv/bin/gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 120 app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF
```

### 2. サービスを起動

```bash
sudo systemctl daemon-reload
sudo systemctl enable quiz-generator
sudo systemctl start quiz-generator
sudo systemctl status quiz-generator
```

### 3. ログ確認

```bash
# リアルタイムでログを確認
sudo journalctl -u quiz-generator -f

# 最新50行のログを確認
sudo journalctl -u quiz-generator -n 50
```

---

## セキュリティグループの設定

EC2のセキュリティグループでポート8000を開けてください：

1. EC2コンソールでインスタンスを選択
2. 「セキュリティ」タブをクリック
3. セキュリティグループ名をクリック
4. 「インバウンドルールを編集」をクリック
5. 「ルールを追加」をクリック
   - **タイプ**: カスタムTCP
   - **ポート範囲**: 8000
   - **ソース**: 0.0.0.0/0（または必要に応じて制限）
6. 「ルールを保存」をクリック

---

## トラブルシューティング

### アプリケーションが起動しない

```bash
# ログを確認
sudo journalctl -u quiz-generator -n 50

# ポートが使用中か確認
sudo netstat -tlnp | grep 8000

# 手動で起動してエラーを確認
cd /opt/quiz-generator
source venv/bin/activate
gunicorn --bind 0.0.0.0:8000 app:app
```

### アクセスできない

1. セキュリティグループでポート8000が開いているか確認
2. アプリケーションが起動しているか確認
   ```bash
   sudo systemctl status quiz-generator
   ```

### アプリケーションの更新

```bash
cd /opt/quiz-generator
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart quiz-generator
```