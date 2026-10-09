#!/usr/bin/env python3
import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

articles_with_images = [
    {
        "post_id": 305,
        "title": "연말정산 완벽 준비 가이드 2026: 지금부터 시작하면 10만원 절약",
        "image_url": "https://images.unsplash.com/photo-1554224311-beee415c15cb?w=1200&h=600&fit=crop"
    },
    {
        "post_id": 306,
        "title": "절세 팁 Top 5: 직장인이 꼭 알아야 할 세금 절약 전략",
        "image_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&h=600&fit=crop"
    },
    {
        "post_id": 307,
        "title": "2026년 직장인이 받을 수 있는 정부 지원금 완벽 가이드",
        "image_url": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1200&h=600&fit=crop"
    },
    {
        "post_id": 308,
        "title": "2027년 변경되는 세금 정책: 직장인이 알아야 할 5가지",
        "image_url": "https://images.unsplash.com/photo-1460925895917-adf4e565a87d?w=1200&h=600&fit=crop"
    },
    {
        "post_id": 309,
        "title": "직장인 부업 가이드 2026: 월 50-200만원 버는 실전 전략",
        "image_url": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1200&h=600&fit=crop"
    },
]

credentials = f"aceguy7771@gmail.com:Dcvp yBWE 6aYf qAQU O1lf kSZO"
encoded = base64.b64encode(credentials.encode()).decode()
auth_header = {"Authorization": f"Basic {encoded}"}

print("[TEST] WordPress 연결 테스트...")
try:
    response = requests.get(
        "https://digital-income7771.com/wp-json/wp/v2/posts?per_page=1",
        headers=auth_header,
        timeout=10
    )
    if response.status_code == 200:
        print("[OK] 연결 성공\n")
    else:
        print(f"[FAIL] 연결 실패")
        exit(1)
except Exception as e:
    print(f"[FAIL] 오류: {e}")
    exit(1)

success = 0

for article in articles_with_images:
    post_id = article["post_id"]
    title = article["title"]
    image_url = article["image_url"]

    print(f"[GET] 포스트 {post_id} 조회 중...")

    # 기존 포스트 조회
    try:
        response = requests.get(
            f"https://digital-income7771.com/wp-json/wp/v2/posts/{post_id}",
            headers=auth_header,
            timeout=10
        )

        if response.status_code != 200:
            print(f"  [FAIL] 포스트 조회 실패")
            continue

        post = response.json()
        current_content = post['content']['rendered']

        # 이미지 블록 HTML 생성
        image_html = f'''<figure class="wp-block-image"><img src="{image_url}" alt="Article Image" width="1200" height="600" /></figure>'''

        # 기존 content 맨 앞에 이미지 추가
        new_content = image_html + current_content

        print(f"  [ADD] 이미지 추가 중...")
        print(f"  [TITLE] {title}")

        # 포스트 업데이트
        update_data = {
            "content": new_content
        }

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
