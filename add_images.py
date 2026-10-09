#!/usr/bin/env python3
import os
import re
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

# 각 글의 주제에 맞는 이미지
articles_with_images = [
    {
        "filename": "article_연말정산_준비_2026-10-09.md",
        "post_id": 305,
        "title": "연말정산 완벽 준비 가이드 2026: 지금부터 시작하면 10만원 절약",
        "image_alt": "연말정산 서류와 계산기",
        "image_url": "https://images.unsplash.com/photo-1554224311-beee415c15cb?w=1200&h=600&fit=crop"  # 세금/회계
    },
    {
        "filename": "article_절세팁_2026-10-09.md",
        "post_id": 306,
        "title": "절세 팁 Top 5: 직장인이 꼭 알아야 할 세금 절약 전략",
        "image_alt": "돈과 세금",
        "image_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&h=600&fit=crop"  # 돈/재무
    },
    {
        "filename": "article_정부지원금_2026-10-09.md",
        "post_id": 307,
        "title": "2026년 직장인이 받을 수 있는 정부 지원금 완벽 가이드",
        "image_alt": "정부 지원 정책",
        "image_url": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1200&h=600&fit=crop"  # 정책/문서
    },
    {
        "filename": "article_2027세금정책_2026-10-09.md",
        "post_id": 308,
        "title": "2027년 변경되는 세금 정책: 직장인이 알아야 할 5가지",
        "image_alt": "2027년 세금 정책 변화",
        "image_url": "https://images.unsplash.com/photo-1460925895917-adf4e565a87d?w=1200&h=600&fit=crop"  # 미래/분석
    },
    {
        "filename": "article_부업돈버는법_2026-10-09.md",
        "post_id": 309,
        "title": "직장인 부업 가이드 2026: 월 50-200만원 버는 실전 전략",
        "image_alt": "부업으로 돈 버는 방법",
        "image_url": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1200&h=600&fit=crop"  # 부업/재테크
    },
]

def add_image_to_html(html_content, image_url, image_alt):
    """HTML에 이미지를 상단에 추가"""
    # <p>로 시작하는 첫 번째 위치 찾기
    first_p = html_content.find('<p>')

    if first_p > 0:
        # 이미지 HTML 생성
        image_html = f'<p><img src="{image_url}" alt="{image_alt}" style="width:100%; max-width:800px; height:auto; border-radius:8px; margin:20px 0;"></p>'
        # 첫 번째 <p> 전에 이미지 삽입
        html_content = html_content[:first_p] + image_html + html_content[first_p:]

    return html_content

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

for article in articles_with_images:
    filename = article["filename"]
    post_id = article["post_id"]
    title = article["title"]
    image_url = article["image_url"]
    image_alt = article["image_alt"]

    filepath = f"C:\\blog-automation\\{filename}"

    if not os.path.exists(filepath):
        print(f"[SKIP] {filename} 없음")
        continue

    print(f"[ADD IMAGE] {filename} 이미지 추가 중...")

    with open(filepath, "r", encoding="utf-8") as f:
        md_content = f.read()

    # 간단한 마크다운 to HTML 변환
    html = md_content

    # 제목 변환
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)

    # 볼드/이탤릭
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)

    # 링크
    html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)

    # 단락
    html = html.replace('\n\n', '</p><p>')
    html = f'<p>{html}</p>'

    # 이미지 추가
    html = add_image_to_html(html, image_url, image_alt)

    print(f"  [TITLE] {title}")
    print(f"  [IMAGE] {image_alt}")
    print(f"  [ID] {post_id}")
    print(f"  [UPDATE] 포스트 업데이트 중...")

    update_data = {
        "title": title,
        "content": html,
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

print(f"[SUMMARY] {success}/{len(articles_with_images)} 성공!")
