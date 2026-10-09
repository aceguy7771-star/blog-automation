#!/usr/bin/env python3
import os
import markdown
from dotenv import load_dotenv
from scripts.wordpress_poster_no_emoji import WordPressPoster

load_dotenv()

articles = [
    ("article_연말정산_준비_2026-10-09.md", 305),
    ("article_절세팁_2026-10-09.md", 306),
    ("article_정부지원금_2026-10-09.md", 307),
    ("article_2027세금정책_2026-10-09.md", 308),
    ("article_부업돈버는법_2026-10-09.md", 309),
]

poster = WordPressPoster()
poster.app_password = os.getenv("WP_APP_PASSWORD", "Dcvp yBWE 6aYf qAQU O1lf kSZO")
poster.auth = poster._setup_auth()

print("[TEST] WordPress 연결 테스트...")
if not poster.validate_connection():
    print("[FAIL] 연결 실패")
    exit(1)

print("[OK] 연결 성공\n")

import requests
import base64

for filename, post_id in articles:
    filepath = f"C:\\blog-automation\\{filename}"

    if not os.path.exists(filepath):
        print(f"[SKIP] {filename} 없음")
        continue

    print(f"[CONVERT] {filename} 변환 중...")

    with open(filepath, "r", encoding="utf-8") as f:
        md_content = f.read()

    # 마크다운을 HTML로 변환
    html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

    # 제목 추출 (첫 번째 # 로 시작하는 줄)
    lines = md_content.split('\n')
    title = ""
    for line in lines:
        if line.startswith('# '):
            title = line.replace('# ', '').strip()
            break

    if not title:
        print(f"  [WARN] 제목 없음, 파일명 사용")
        title = filename.replace('.md', '')

    print(f"  [TITLE] {title}")
    print(f"  [ID] {post_id}")

    # WordPress에 업데이트
    print(f"  [UPDATE] 포스트 업데이트 중...")

    credentials = f"aceguy7771@gmail.com:Dcvp yBWE 6aYf qAQU O1lf kSZO"
    encoded = base64.b64encode(credentials.encode()).decode()
    auth_header = {"Authorization": f"Basic {encoded}"}

    update_data = {
        "title": title,
        "content": html_content,
    }

    response = requests.post(
        f"https://digital-income7771.com/wp-json/wp/v2/posts/{post_id}",
        json=update_data,
        headers=auth_header,
        timeout=30
    )

    if response.status_code == 200:
        print(f"  [OK] 업데이트 성공\n")
    else:
        print(f"  [FAIL] 업데이트 실패: {response.status_code}\n")

print("[SUMMARY] 마크다운 → HTML 변환 완료!")
