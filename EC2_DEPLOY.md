# EC2インスタンスへのデプロイ手順

このドキュメントでは、AWS EC2インスタンスにFlaskアプリケーションをデプロイする手順を説明します。

## 前提条件

- EC2インスタンスが起動している
- EC2 Instance Connect、SSH、またはSession Managerで接続できる
- セキュリティグループでポート8000（または任意のポート）が開いている

## デプロイ手順

### 方法1: デプロイスクリプトを使用（推奨）

1. **EC2インスタンスに接続**
   - AWS コンソールから「インスタンスに接続」をクリック
   - EC2 Instance Connectを選択して接続

2. **デプロイスクリプトをダウンロード**
   ```bash
   cd /tmp
   wget https://raw.githubusercontent.com/Hiyama-sir/test-maiking/main/deploy_ec2.sh
   chmod +x deploy_ec2.sh
   ```

3. **スクリプトを実行**
   ```bash
   ./deploy_ec2.sh
   ```

### 方法2: 手動デプロイ

1. **必要なパッケージをインストール**
   ```bash
   sudo yum update -y
   sudo yum install -y python3 python3-pip git
   ```

2. **プロジェクトディレクトリを作成**
   ```bash
   sudo mkdir -p /opt/quiz-generator
   sudo chown ec2-user:ec2-user /opt/quiz-generator
   cd /opt
   ```

3. **リポジトリをクローン**
   ```bash
   git clone https://github.com/Hiyama-sir/test-maiking.git quiz-generator
   cd quiz-generator
   ```

4. **仮想環境を作成**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

5. **依存関係をインストール**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

6. **systemdサービスファイルを作成**
   ```bash
   sudo nano /etc/systemd/system/quiz-generator.service
   ```
   
   以下を記述：
   ```ini
   [Unit]
   Description=Quiz Generator Flask Application
   After=network.target

   [Service]
   Type=notify
   User=ec2-user
   Group=ec2-user
   WorkingDirectory=/opt/quiz-generator
   Environment="PATH=/opt/quiz-generator/venv/bin"
   ExecStart=/opt/quiz-generator/venv/bin/gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 120 app:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

7. **サービスを起動**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable quiz-generator
   sudo systemctl start quiz-generator
   sudo systemctl status quiz-generator
   ```

## アプリケーションへのアクセス

デプロイ後、以下のURLでアクセスできます：
```
http://<EC2のパブリックIP>:8000
```

例：`http://13.210.236.134:8000`

## サービス管理コマンド

```bash
# サービスを起動
sudo systemctl start quiz-generator

# サービスを停止
sudo systemctl stop quiz-generator

# サービスを再起動
sudo systemctl restart quiz-generator

# サービスの状態を確認
sudo systemctl status quiz-generator

# ログを確認
sudo journalctl -u quiz-generator -f

# エラーログを確認
sudo journalctl -u quiz-generator -n 50
```

## アプリケーションの更新

アプリケーションを更新する場合：

```bash
cd /opt/quiz-generator
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart quiz-generator
```

## Nginxを使用したリバースプロキシ（オプション）

ポート80でアクセスできるようにする場合：

1. **Nginxをインストール**
   ```bash
   sudo yum install -y nginx
   ```

2. **Nginx設定ファイルを作成**
   ```bash
   sudo nano /etc/nginx/conf.d/quiz-generator.conf
   ```
   
   以下を記述：
   ```nginx
   server {
       listen 80;
       server_name _;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

3. **Nginxを起動**
   ```bash
   sudo systemctl enable nginx
   sudo systemctl start nginx
   ```

## セキュリティグループの設定

EC2のセキュリティグループで以下のポートを開ける必要があります：

- **ポート8000**: アプリケーション直接アクセス用（HTTP）
- **ポート80**: Nginx使用時（HTTP）
- **ポート443**: HTTPS使用時（SSL証明書が必要）

## 環境変数の設定

環境変数を設定する場合、systemdサービスファイルを編集：

```bash
sudo nano /etc/systemd/system/quiz-generator.service
```

`[Service]`セクションに環境変数を追加：
```ini
[Service]
...
Environment="CONTACT_EMAIL=your-email@example.com"
Environment="SMTP_USERNAME=your-smtp-username"
Environment="SMTP_PASSWORD=your-smtp-password"
...
```

編集後、再読み込み：
```bash
sudo systemctl daemon-reload
sudo systemctl restart quiz-generator
```

## トラブルシューティング

### アプリケーションが起動しない

1. ログを確認
   ```bash
   sudo journalctl -u quiz-generator -n 50
   ```

2. ポートが使用中か確認
   ```bash
   sudo netstat -tlnp | grep 8000
   ```

3. 仮想環境が正しくアクティブか確認
   ```bash
   cd /opt/quiz-generator
   source venv/bin/activate
   which python
   which gunicorn
   ```

### アクセスできない

1. セキュリティグループの設定を確認
2. アプリケーションが起動しているか確認
   ```bash
   sudo systemctl status quiz-generator
   ```
3. ファイアウォール設定を確認（必要に応じて）
   ```bash
   sudo firewall-cmd --list-all
   ```