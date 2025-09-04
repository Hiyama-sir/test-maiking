from flask import Flask, render_template, request, jsonify
from openpyxl import load_workbook
import os

app = Flask(__name__)

def load_excel_data():
    """Excelファイルからデータを読み込む"""
    try:
        # Excelファイルを読み込み
        workbook = load_workbook('小テスト Retrieved from コーパス4500 4th Edition.xlsx')
        worksheet = workbook.active
        
        # A列（英単語）とB列（日本語）のデータを取得
        # A1行目から直接データを読み込み
        data = []
        row_num = 1
        
        for row in worksheet.iter_rows(min_row=1, values_only=True):
            if row[0] is not None and row[1] is not None:  # A列とB列の両方に値がある場合
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

@app.route('/')
def index():
    """メインページ"""
    data = load_excel_data()
    return render_template('index.html', data=data)


@app.route('/generate_test', methods=['POST'])
def generate_test():
    """指定された行番号のテストを生成"""
    try:
        data = request.get_json()
        selected_rows = data.get('selected_rows', [])
        
        if not selected_rows:
            return jsonify({'error': '行番号が選択されていません'}), 400
        
        # Excelデータを読み込み
        excel_data = load_excel_data()
        
        # 選択された行番号のデータを取得
        test_data = []
        for row_num in selected_rows:
            for item in excel_data:
                if item['row_number'] == row_num:
                    test_data.append(item)
                    break
        
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)

# Gunicorn用の設定
if __name__ != '__main__':
    # 本番環境用の設定
    pass
