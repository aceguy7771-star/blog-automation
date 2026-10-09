#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv
from scripts.wordpress_poster_no_emoji import WordPressPoster

load_dotenv()

articles = [
    ("article_연말정산_준비_2026-10-09.md", "연말정산 완벽 준비 가이드 2026: 지금부터 시작하면 10만원 절약", ["연말정산", "세금", "2026"]),
    ("article_절세팁_2026-10-09.md", "절세 팁 Top 5: 직장인이 꼭 알아야 할 세금 절약 전략", ["절세", "세금", "재테크"]),
    ("article_정부지원금_2026-10-09.md", "2026년 직장인이 받을 수 있는 정부 지원금 완벽 가이드", ["정부지원금", "지원", "정책"]),
    ("article_2027세금정책_2026-10-09.md", "2027년 변경되는 세금 정책: 직장인이 알아야 할 5가지", ["세금", "정책", "2027"]),
    ("article_부업돈버는법_2026-10-09.md", "직장인 부업 가이드 2026: 월 50-200만원 버는 실전 전략", ["부업", "재테크", "돈벌기"]),
]

poster = WordPressPoster()
poster.app_password = os.getenv("WP_APP_PASSWORD", "Dcvp yBWE 6aYf qAQU O1lf kSZO")
poster.auth = poster._setup_auth()

print("[TEST] WordPress 연결 테스트 중...")
if not poster.validate_connection():
    print("[FAIL] 연결 실패")
    sys.exit(1)

print("[OK] 연결 성공\n")

success = 0
for filename, title, tags in articles:
    filepath = f"C:\\blog-automation\\{filename}"

    if not os.path.exists(filepath):
        print(f"[SKIP] {filename} 없음")
        continue

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    print(f"[POST] {title}")
    result = poster.post_article(
        title=title,
        content=content,
        category="재테크",
        tags=tags,
        status="publish"
    )

    if "post_id" in result:
        print(f"  [OK] ID={result['post_id']}")
        success += 1
    else:
        print(f"  [FAIL] {result.get('error', 'unknown')}")

print(f"\n[SUMMARY] {success}/{len(articles)} 성공")
