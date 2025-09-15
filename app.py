from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from openpyxl import load_workbook
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # セッション用の秘密鍵

def load_excel_data(filename=None):
    """Excelファイルからデータを読み込む"""
    try:
        # デフォルトのファイル名を設定
        if filename is None:
            filename = '小テスト Retrieved from コーパス4500 4th Edition.xlsx'
        
        # Excelファイルを読み込み
        workbook = load_workbook(filename)
        worksheet = workbook.active
        
        # A列（英単語）とB列（日本語）のデータを取得
        # A1行目から直接データを読み込み
        data = []
        row_num = 1
        
        for row in worksheet.iter_rows(min_row=1, values_only=True):
            if row[0] is not None and row[1] is not None:  # A列とB列の両方に値がある場合
                # ヘッダー行（「単語名」など）を除外
                if str(row[0]).strip() not in ['単語名', 'word', 'Word', 'WORD'] and str(row[1]).strip() not in ['意味', 'meaning', 'Meaning', 'MEANING']:
                    data.append({
                        'row_number': row_num,
                        'word': str(row[0]),
                        'meaning': str(row[1])
                    })
                    row_num += 1
        
        return data
    except Exception as e:
        print(f"Excelファイルの読み込みエラー: {e}")
        return []

def get_available_files():
    """利用可能なExcelファイルのリストを取得"""
    files = []
    excel_files = [
        '小テスト Retrieved from コーパス4500 4th Edition.xlsx',
        'ターゲット1900.xlsx',
        'システム英単語.xlsx'
    ]
    
    for file in excel_files:
        if os.path.exists(file):
            if file == '小テスト Retrieved from コーパス4500 4th Edition.xlsx':
                display_name = 'コーパス4500'
            elif file == 'ターゲット1900.xlsx':
                display_name = 'ターゲット1900'
            elif file == 'システム英単語.xlsx':
                display_name = 'システム英単語'
            else:
                display_name = file.replace('.xlsx', '')
            
            files.append({
                'filename': file,
                'display_name': display_name
            })
        else:
            # ファイルが見つからない場合は、サンプルファイルの存在を確認
            sample_file = f'sample_data/{file.replace(".xlsx", "_sample.xlsx")}'
            if os.path.exists(sample_file):
                if file == '小テスト Retrieved from コーパス4500 4th Edition.xlsx':
                    display_name = 'コーパス4500 (サンプル)'
                elif file == 'ターゲット1900.xlsx':
                    display_name = 'ターゲット1900 (サンプル)'
                elif file == 'システム英単語.xlsx':
                    display_name = 'システム英単語 (サンプル)'
                else:
                    display_name = file.replace('.xlsx', '') + ' (サンプル)'
                
                files.append({
                    'filename': sample_file,
                    'display_name': display_name
                })
    
    return files

@app.route('/')
def index():
    """メインページ"""
    data = load_excel_data()
    available_files = get_available_files()
    return render_template('index.html', data=data, available_files=available_files)


@app.route('/generate_test', methods=['POST'])
def generate_test():
    """指定された行番号のテストを生成"""
    try:
        data = request.get_json()
        selected_rows = data.get('selected_rows', [])
        
        if not selected_rows:
            return jsonify({'error': '行番号が選択されていません'}), 400
        
        # 選択されたファイルのデータを読み込み
        selected_file = data.get('selected_file')
        if selected_file:
            excel_data = load_excel_data(selected_file)
        else:
            excel_data = load_excel_data()
        
        # 選択された行番号のデータを取得
        test_data = []
        print(f"選択された行番号: {selected_rows}")
        print(f"利用可能なデータ数: {len(excel_data)}")
        
        for row_num in selected_rows:
            found = False
            for item in excel_data:
                if item['row_number'] == row_num:
                    test_data.append(item)
                    print(f"行番号 {row_num}: {item['word']} - {item['meaning']}")
                    found = True
                    break
            if not found:
                print(f"警告: 行番号 {row_num} のデータが見つかりません")
        
        print(f"最終的なテストデータ数: {len(test_data)}")
        
        if not test_data:
            return jsonify({'error': '選択された行番号のデータが見つかりません'}), 400
        
        return jsonify({
            'success': True,
            'test_data': test_data
        })
        
    except Exception as e:
        return jsonify({'error': f'エラーが発生しました: {str(e)}'}), 500

@app.route('/get_all_data')
def get_all_data():
    """全データを取得"""
    data = load_excel_data()
    return jsonify(data)

@app.route('/load_file', methods=['POST'])
def load_file():
    """指定されたファイルのデータを読み込み"""
    try:
        data = request.get_json()
        filename = data.get('filename')
        
        if not filename:
            return jsonify({'error': 'ファイル名が指定されていません'}), 400
        
        file_data = load_excel_data(filename)
        
        if not file_data:
            return jsonify({'error': 'ファイルの読み込みに失敗しました'}), 400
        
        return jsonify({
            'success': True,
            'data': file_data
        })
        
    except Exception as e:
        return jsonify({'error': f'エラーが発生しました: {str(e)}'}), 500

@app.route('/get_available_files')
def get_available_files_api():
    """利用可能なファイル一覧を取得"""
    files = get_available_files()
    return jsonify(files)

@app.route('/contact')
def contact():
    """問い合わせフォームページ"""
    return render_template('contact.html')

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    """問い合わせフォームの送信処理"""
    try:
        name = request.form.get('name', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        
        # バリデーション
        if not name or not subject or not message:
            flash('すべての項目を入力してください。', 'error')
            return redirect(url_for('contact'))
        
        # メール送信（実際の送信は環境変数で設定）
        send_contact_email(name, subject, message)
        
        flash('お問い合わせありがとうございます。内容を確認次第、ご連絡いたします。', 'success')
        return redirect(url_for('contact'))
        
    except Exception as e:
        flash(f'エラーが発生しました: {str(e)}', 'error')
        return redirect(url_for('contact'))

def send_contact_email(name, subject, message):
    """問い合わせメールを送信"""
    try:
        # メール設定（環境変数から取得、なければデフォルト値）
        smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        smtp_username = os.environ.get('SMTP_USERNAME', '')
        smtp_password = os.environ.get('SMTP_PASSWORD', '')
        contact_email = os.environ.get('CONTACT_EMAIL', 'contact@example.com')
        
        # デバッグ情報を出力
        print(f"=== メール送信デバッグ情報 ===")
        print(f"SMTP_SERVER: {smtp_server}")
        print(f"SMTP_PORT: {smtp_port}")
        print(f"SMTP_USERNAME: {'設定済み' if smtp_username else '未設定'}")
        print(f"SMTP_PASSWORD: {'設定済み' if smtp_password else '未設定'}")
        print(f"CONTACT_EMAIL: {contact_email}")
        print(f"===============================")
        
        # メール内容
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = contact_email
        msg['Subject'] = f'[テスト問題ジェネレーター] {subject}'
        
        body = f"""
新しい英単語帳の追加要望が届きました。

送信者名: {name}
件名: {subject}

メッセージ:
{message}

---
このメールはテスト問題ジェネレーターの問い合わせフォームから送信されました。
        """
        
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # メール送信（SMTP設定がある場合のみ）
        if smtp_username and smtp_password:
            print("SMTP設定が検出されました。メール送信を試行します...")
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            text = msg.as_string()
            server.sendmail(smtp_username, contact_email, text)
            server.quit()
            print("メール送信が完了しました。")
        else:
            # SMTP設定がない場合はログに出力
            print("SMTP設定が不完全です。メール送信をスキップします。")
            print(f"問い合わせメール（送信設定なし）:")
            print(f"送信者: {name}")
            print(f"件名: {subject}")
            print(f"メッセージ: {message}")
            
    except Exception as e:
        print(f"メール送信エラー: {e}")
        print(f"エラーの詳細: {type(e).__name__}")
        # エラーが発生してもアプリケーションは継続

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)

# Gunicorn用の設定
if __name__ != '__main__':
    # 本番環境用の設定
    pass
