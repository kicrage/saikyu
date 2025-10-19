from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    message = data.get('message', '').strip()
    if not name or not email or not message:
        return jsonify({'ok': False, 'error': '全ての項目を入力してください'}), 400

    # Save to a file (simple demo)
    timestamp = datetime.utcnow().isoformat().replace(':','-')
    filename = os.path.join(DATA_DIR, f'contact_{timestamp}.json')
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            import json
            json.dump({'name': name, 'email': email, 'message': message, 'received_at': timestamp}, f, ensure_ascii=False, indent=2)
    except Exception as e:
        return jsonify({'ok': False, 'error': '保存に失敗しました'}), 500

    return jsonify({'ok': True, 'message': '送信が完了しました。ありがとうございました。'})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
