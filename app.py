from flask import Flask, render_template, request, jsonify
from openpyxl import load_workbook
import os

app = Flask(__name__)

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
        'ターゲット1900.xlsx'
    ]
    
    for file in excel_files:
        if os.path.exists(file):
            if file == '小テスト Retrieved from コーパス4500 4th Edition.xlsx':
                display_name = 'コーパス4500'
            elif file == 'ターゲット1900.xlsx':
                display_name = 'ターゲット1900'
            else:
                display_name = file.replace('.xlsx', '')
            
            files.append({
                'filename': file,
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)

# Gunicorn用の設定
if __name__ != '__main__':
    # 本番環境用の設定
    pass
