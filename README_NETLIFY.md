Netlify CMS 導入手順（簡易）

目的: ブラウザから記事（お知らせ）を編集・作成し、Git リポジトリにコミットして自動デプロイする流れを作ります。

前提:
- サイトを GitHub（または GitLab）にプッシュしていること
- Netlify アカウントを持っていること

手順（概要）:
1. リポジトリを GitHub に push します（branch は `main` を想定）。
2. Netlify にログインし、New site -> Import from Git でリポジトリを選択。
3. Build command は不要（静的ファイルのみ）だが、ビルドが必要なら設定する。
4. Netlify の Site settings -> Identity を有効化（Enable Identity）。
5. Identity の Settings and usage -> Services -> Git Gateway を有効化して、Git provider（GitHub）と連携。
6. Netlify の Identity -> Invite users で管理者アカウントを招待するか、Local signup を使う。
7. ブラウザで https://<your-site>/admin/ を開くと Netlify CMS の管理画面が表示される（Identity でログイン）。

ファイルについて:
- `admin/index.html` と `admin/config.yml` を追加済み。`config.yml` の backend を必要に応じて編集してください（branch 名など）。
- `media_folder` は `static/uploads` に設定済み。Netlify の場合、このパスはリポジトリ内にコミットされます。
- CMS で記事を作成すると、`posts/` 以下に Markdown ファイルが生成される（または直接 HTML を生成する設定も可能）。

ローカルでのビルド（任意）:
- `posts/build.py` を追加しました。ローカルに Markdown を置いて HTML を生成し、`posts/posts.json` を更新するためのスクリプトです。
- 実行例（PowerShell）:

```powershell
python posts\build.py
python -m http.server 8000
```

サポートが必要なら、Netlify の設定（Identity / Git Gateway）や `config.yml` のカスタマイズ、CMS のプレビューテンプレート追加などを手伝います。