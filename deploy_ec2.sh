#!/bin/bash
# EC2インスタンスへのデプロイスクリプト

set -e

echo "=== EC2デプロイスクリプト ==="

# プロジェクトディレクトリ
PROJECT_DIR="/opt/quiz-generator"
REPO_URL="https://github.com/Hiyama-sir/test-maiking.git"

# 必要なパッケージのインストール
echo "1. 必要なパッケージをインストール中..."
sudo yum update -y
sudo yum install -y python3 python3-pip git

# プロジェクトディレクトリの作成
echo "2. プロジェクトディレクトリを作成中..."
sudo mkdir -p $PROJECT_DIR
sudo chown ec2-user:ec2-user $PROJECT_DIR

# リポジトリのクローンまたは更新
echo "3. リポジトリをクローン/更新中..."
if [ -d "$PROJECT_DIR/.git" ]; then
    cd $PROJECT_DIR
    git pull origin main
else
    cd /opt
    sudo -u ec2-user git clone $REPO_URL quiz-generator
fi

cd $PROJECT_DIR

# 仮想環境の作成/更新
echo "4. 仮想環境を作成中..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# 依存関係のインストール
echo "5. 依存関係をインストール中..."
pip install --upgrade pip
pip install -r requirements.txt

# systemdサービスの設定
echo "6. systemdサービスを設定中..."
sudo tee /etc/systemd/system/quiz-generator.service > /dev/null <<EOF
[Unit]
Description=Quiz Generator Flask Application
After=network.target

[Service]
Type=notify
User=ec2-user
Group=ec2-user
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 120 app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# サービスの有効化と起動
echo "7. サービスを起動中..."
sudo systemctl daemon-reload
sudo systemctl enable quiz-generator
sudo systemctl restart quiz-generator

# サービスの状態確認
echo "8. サービスの状態を確認中..."
sleep 2
sudo systemctl status quiz-generator --no-pager

echo ""
echo "=== デプロイ完了 ==="
echo "アプリケーションは http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8000 でアクセスできます"
echo ""
echo "サービス管理コマンド:"
echo "  起動: sudo systemctl start quiz-generator"
echo "  停止: sudo systemctl stop quiz-generator"
echo "  再起動: sudo systemctl restart quiz-generator"
echo "  状態確認: sudo systemctl status quiz-generator"
echo "  ログ確認: sudo journalctl -u quiz-generator -f"