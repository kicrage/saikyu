# ローカル問い合わせサーバ

このプロジェクトには簡易問い合わせ受信サーバ（Flask）を同梱しています。開発環境でフォームの送信を受け取り、`data/` フォルダにJSONで保存します。

セットアップ手順（Windows PowerShell）:

```powershell
cd "c:\Users\kicra\Documents\saikyu website"
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

サーバはデフォルトで `http://127.0.0.1:5000` で起動します。

注意: これは開発用のデモサーバです。本番では適切な認証、入力検証、TLS を必ず導入してください。
