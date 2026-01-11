# Elastic Beanstalk用のエントリーポイント
from app import app

# Elastic Beanstalkは application 変数を探します
application = app

if __name__ == "__main__":
    application.run()