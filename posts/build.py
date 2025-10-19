#!/usr/bin/env python3
"""
Simple build script: converts posts/*.md to posts/*.html and updates posts/posts.json
Usage: python posts\build.py
"""
import os
import json
from datetime import datetime
import markdown

ROOT = os.path.dirname(os.path.abspath(__file__))
POSTS_DIR = ROOT
OUT_JSON = os.path.join(ROOT, 'posts.json')
TEMPLATE = '''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{title} - 西急電鉄</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../styles.css">
</head>
<body>
  <header class="site-header">
    <div class="container header-inner">
      <a class="brand" href="../index.html" aria-label="ホームへ">
        <img src="../icon.png" alt="西急ロゴ" class="logo">
        <div>
          <h1 class="site-title">西急電鉄</h1>
          <p class="site-sub">お知らせ</p>
        </div>
      </a>

      <button id="menuToggle" class="menu-toggle" aria-expanded="false" aria-controls="main-nav">
        <span class="sr-only">メニューを開く</span>
      </button>

      <nav id="main-nav" class="main-nav" aria-label="メインナビゲーション" aria-hidden="true">
        <ul>
          <li><a href="../index.html">ホーム</a></li>
          <li><a href="../news.html">お知らせ</a></li>
          <li><a href="../network.html">運行情報</a></li>
          <li><a href="../company.html">会社情報</a></li>
        </ul>
      </nav>
    </div>
  </header>

  <main class="container">
    <article class="section">
      <h1>{title}</h1>
      <p class="meta">公開日: {date}</p>

      {content}

      <p><a href="../news.html">一覧に戻る</a></p>
    </article>
  </main>

  <footer class="site-footer">
    <div class="container footer-inner">
      <p>&copy; <span id="year"></span> 西急電鉄</p>
    </div>
  </footer>

  <script src="../script.js" defer></script>
</body>
</html>'''


def build():
    posts = []
    for fname in os.listdir(POSTS_DIR):
        if not fname.endswith('.md'):
            continue
        path = os.path.join(POSTS_DIR, fname)
        with open(path, 'r', encoding='utf-8') as f:
            md = f.read()
        # simple front matter: first line title: Title, second line date: YYYY-MM-DD, then blank
        lines = md.splitlines()
        title = None
        date = None
        body_lines = []
        i = 0
        while i < len(lines):
            ln = lines[i].strip()
            if ln.startswith('title:') and title is None:
                title = ln.split(':',1)[1].strip()
                i += 1
                continue
            if ln.startswith('date:') and date is None:
                date = ln.split(':',1)[1].strip()
                i += 1
                continue
            # skip first blank after header
            if title and date and ln == '':
                i += 1
                break
            i += 1
        body_lines = lines[i:]
        body_md = '\n'.join(body_lines)
        html = markdown.markdown(body_md, extensions=['fenced_code','tables'])
        outname = fname.rsplit('.',1)[0] + '.html'
        outpath = os.path.join(POSTS_DIR, outname)
        with open(outpath, 'w', encoding='utf-8') as f:
            f.write(TEMPLATE.format(title=title or '無題', date=date or '', content=html))
        posts.append({
            'id': fname.rsplit('.',1)[0],
            'title': title or '無題',
            'date': date or datetime.utcnow().strftime('%Y-%m-%d'),
            'summary': (body_lines[0][:80] if body_lines else ''),
            'path': outname
        })
    # sort posts by date desc
    posts.sort(key=lambda p: p.get('date',''), reverse=True)
    with open(OUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    print(f'Built {len(posts)} posts and updated posts.json')


if __name__ == '__main__':
    build()
