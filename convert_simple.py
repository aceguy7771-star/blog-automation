#!/usr/bin/env python3
import os
import re
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

articles = [
    ("article_연말정산_준비_2026-10-09.md", 305, "연말정산 완벽 준비 가이드 2026: 지금부터 시작하면 10만원 절약"),
    ("article_절세팁_2026-10-09.md", 306, "절세 팁 Top 5: 직장인이 꼭 알아야 할 세금 절약 전략"),
    ("article_정부지원금_2026-10-09.md", 307, "2026년 직장인이 받을 수 있는 정부 지원금 완벽 가이드"),
    ("article_2027세금정책_2026-10-09.md", 308, "2027년 변경되는 세금 정책: 직장인이 알아야 할 5가지"),
    ("article_부업돈버는법_2026-10-09.md", 309, "직장인 부업 가이드 2026: 월 50-200만원 버는 실전 전략"),
]

def convert_markdown_to_html(md_content):
    """간단한 마크다운을 HTML로 변환"""
    html = md_content

    # 제목 변환
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)

    # 볼드 변환
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'__(.*?)__', r'<strong>\1</strong>', html)

    # 이탤릭 변환
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)

    # 링크 변환
    html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)

    # 줄바꿈을 <br>로
    html = html.replace('\n\n', '</p><p>')
    html = f'<p>{html}</p>'

    # 테이블 변환 (간단히)
    html = html.replace('| ', '<td>').replace(' |', '</td>')

    return html

print("[TEST] WordPress 연결 테스트...")

credentials = f"aceguy7771@gmail.com:Dcvp yBWE 6aYf qAQU O1lf kSZO"
encoded = base64.b64encode(credentials.encode()).decode()
auth_header = {"Authorization": f"Basic {encoded}"}

try:
    response = requests.get(
        "https://digital-income7771.com/wp-json/wp/v2/posts?per_page=1",
        headers=auth_header,
        timeout=10
    )
    if response.status_code == 200:
        print("[OK] 연결 성공\n")
    else:
        print(f"[FAIL] 연결 실패 ({response.status_code})")
        exit(1)
except Exception as e:
    print(f"[FAIL] 연결 오류: {e}")
    exit(1)

success = 0

for filename, post_id, title in articles:
    filepath = f"C:\\blog-automation\\{filename}"

    if not os.path.exists(filepath):
        print(f"[SKIP] {filename} 없음")
        continue

    print(f"[CONVERT] {filename} 변환 중...")

    with open(filepath, "r", encoding="utf-8") as f:
        md_content = f.read()

    # 마크다운을 HTML로 변환
    html_content = convert_markdown_to_html(md_content)

    print(f"  [TITLE] {title}")
    print(f"  [ID] {post_id}")

    # WordPress에 업데이트
    print(f"  [UPDATE] 포스트 업데이트 중...")

    update_data = {
        "title": title,
        "content": html_content,
    }

    try:
        response = requests.post(
            f"https://digital-income7771.com/wp-json/wp/v2/posts/{post_id}",
            json=update_data,
            headers=auth_header,
            timeout=30
        )

        if response.status_code == 200:
            print(f"  [OK] 업데이트 성공\n")
            success += 1
        else:
            print(f"  [FAIL] 업데이트 실패: {response.status_code}\n")
    except Exception as e:
        print(f"  [ERROR] {e}\n")

print(f"[SUMMARY] {success}/{len(articles)} 성공!")
