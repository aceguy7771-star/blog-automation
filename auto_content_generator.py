#!/usr/bin/env python3
"""
자동 블로그 글 생성 및 발행 시스템
매일 오후 6시에 실행되어 고품질 글을 생성하고 WordPress에 발행합니다.
"""

import os
import json
import requests
import base64
from datetime import datetime
from dotenv import load_dotenv
import markdown

load_dotenv()

# 설정
WP_SITE_URL = os.getenv("WP_SITE_URL", "https://digital-income7771.com")
WP_EMAIL = os.getenv("WP_EMAIL", "aceguy7771@gmail.com")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD", "Dcvp yBWE 6aYf qAQU O1lf kSZO")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
COUPANG_AFFILIATE_ID = os.getenv("COUPANG_AFFILIATE_ID", "AF9889638")

# WordPress 인증 설정
def get_wp_auth_header():
    credentials = f"{WP_EMAIL}:{WP_APP_PASSWORD}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {encoded}"}

# Claude API로 글 생성
def generate_article_with_claude():
    """Claude API를 사용해 고품질 블로그 글 생성"""

    if not ANTHROPIC_API_KEY:
        print("[WARN] ANTHROPIC_API_KEY 없음 - 기본 글 생성")
        return generate_fallback_article()

    from anthropic import Anthropic

    client = Anthropic()

    prompt = """당신은 대한민국 직장인을 위한 금융 정보 전문가입니다.

오늘 날짜는 2026년 10월 10일입니다.

**미션**: 직장인이 꼭 알아야 할 실용적인 금융/재테크 정보를 작성하세요.

**요구사항**:
1. 제목: 명확하고 CTR 높은 제목 (예: "Title: 주제: 핵심 내용")
2. 구성:
   - 개요 (2-3문단)
   - 주요 내용 (3-5개 섹션, 각각 h2)
   - 주의사항 or 팁 (1-2문단)
   - 결론 (1문단)
3. 길이: 1500-2000자
4. 톤: 실용적, 정보 중심, 친근함
5. 한국어, 마크다운 형식

**금지**:
- 법적 조언 (대신 "국세청 기준" 등으로 표현)
- 투자 권유
- 개인 경험담

**주제 후보** (아무거나 선택):
- 2026년 하반기 세금 변화
- 프리랜서 원천징수 대비법
- 퇴직금 세금 절약
- 부동산 취득세 변화
- 건강보험료 절약법
- 신용카드 소득공제
- 휴직자 실업급여 대상 확인
- 근퇴공제금 활용법

글을 마크다운 형식으로 생성하세요. "Title: " 로 시작합니다."""

    try:
        message = client.messages.create(
            model="claude-opus-5-5",
            max_tokens=2048,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        content = message.content[0].text
        print("[OK] Claude API로 글 생성 완료")
        return content
    except Exception as e:
        print(f"[WARN] Claude API 오류: {e}")
        return generate_fallback_article()

def generate_fallback_article():
    """Claude API 없을 때 기본 글 생성"""
    today = datetime.now().strftime("%Y년 %m월 %d일")

    return f"""Title: 프리랜서 원천징수, 연말정산에서 100만원 돌려받는 법

**작성일**: {today}

## 개요

프리랜서나 부업이 있는 직장인이라면 '원천징수'라는 단어가 낯설지 않습니다. 하지만 많은 사람들이 이 세금이 연말정산에서 어떻게 처리되는지 정확히 알지 못합니다.

## 원천징수란 무엇인가?

원천징수는 일감을 준 회사나 플랫폼이 당신의 소득에서 미리 세금을 떼가는 제도입니다. 프리랜서의 경우 3.3~3.5%, 부업 수입의 경우 10% 정도가 떼집니다.

## 연말정산에서 돌려받기

떼인 원천징수액은 연말정산에서 환급받을 수 있습니다. 실제 세액보다 많이 떨어졌다면 돌려받는 것입니다.

**필요 서류**:
- 원천징수영수증 (플랫폼에서 발급)
- 부업 관련 증빙자료

## 주의사항

- 소득 신고 여부 확인 (지원금 받는 경우 중요)
- 배우자 소득과 함께 종합소득세 신고 필요
- 부업 소득이 ₩2,000,000 이상이면 사업자등록 고려

## 결론

프리랜서 수입도 성실하게 관리하면 세금 절약은 물론 신용도 향상됩니다. 연말정산을 제대로 챙겨 돌려받을 돈은 꼭 받으세요."""

# 이미지 선택
def select_image_for_topic(title):
    """제목 기반 적절한 이미지 URL 반환"""

    images = {
        "세금": "https://images.unsplash.com/photo-1554224311-beee415c15cb?w=1200&h=600&fit=crop",
        "재테크": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1200&h=600&fit=crop",
        "돈": "https://images.unsplash.com/photo-1579621970563-430f63602d4a?w=1200&h=600&fit=crop",
        "투자": "https://images.unsplash.com/photo-1460925895917-adf4e565a87d?w=1200&h=600&fit=crop",
        "부업": "https://images.unsplash.com/photo-1552664730-d307ca884978?w=1200&h=600&fit=crop",
        "정책": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1200&h=600&fit=crop",
    }

    # 제목에서 키워드 찾기
    for keyword, url in images.items():
        if keyword in title.lower():
            return url

    # 기본 이미지
    return "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1200&h=600&fit=crop"

# 마크다운을 HTML로 변환
def convert_md_to_html(md_content, image_url):
    """마크다운을 WordPress 호환 HTML로 변환"""

    # markdown 라이브러리 사용
    html = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

    # 이미지를 상단에 추가 (WordPress 이미지 블록 형식)
    image_html = f'<figure class="wp-block-image"><img src="{image_url}" alt="Article Image" width="1200" height="600" style="border-radius: 8px;" /></figure>'

    html = image_html + html

    return html

# WordPress에 발행
def post_to_wordpress(title, html_content, tags=[]):
    """WordPress에 글 발행"""

    auth_header = get_wp_auth_header()

    # 기본 카테고리 설정
    categories = [18]  # "재테크 기초" 카테고리 ID

    post_data = {
        "title": title,
        "content": html_content,
        "status": "publish",
        "categories": categories,
        "tags": tags,
        "author": 1,
    }

    try:
        response = requests.post(
            f"{WP_SITE_URL}/wp-json/wp/v2/posts",
            json=post_data,
            headers=auth_header,
            timeout=30
        )

        if response.status_code == 201:
            post = response.json()
            post_id = post['id']
            permalink = post['link']
            print(f"[OK] WordPress 발행 성공!")
            print(f"     ID: {post_id}")
            print(f"     URL: {permalink}\n")
            return post_id
        else:
            print(f"[FAIL] WordPress 발행 실패: {response.status_code}")
            print(f"       응답: {response.text}")
            return None

    except Exception as e:
        print(f"[ERROR] {e}")
        return None

# 메인 실행
def main():
    print("="*60)
    print("[AUTO] 자동 블로그 글 생성 및 발행 시스템")
    print(f"   시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")

    # Step 1: 글 생성
    print("[1/4] Claude API로 글 생성 중...")
    article_content = generate_article_with_claude()

    # 제목과 본문 분리
    lines = article_content.split('\n')
    title = ""
    md_content = article_content

    for line in lines:
        if line.startswith("Title: "):
            title = line.replace("Title: ", "").strip()
            md_content = article_content.replace(f"Title: {title}\n", "")
            break

    if not title:
        title = "금융 정보: 직장인을 위한 세금 절약 팁"

    print(f"   제목: {title}\n")

    # Step 2: 이미지 선택
    print("[2/4] 이미지 선택 중...")
    image_url = select_image_for_topic(title)
    print(f"   이미지: {image_url}\n")

    # Step 3: HTML 변환
    print("[3/4] 마크다운 → HTML 변환 중...")
    html_content = convert_md_to_html(md_content, image_url)
    print(f"   길이: {len(html_content)} 바이트\n")

    # Step 4: WordPress 발행
    print("[4/4] WordPress에 발행 중...")
    post_id = post_to_wordpress(title, html_content)

    if post_id:
        print("="*60)
        print(f"[OK] 완료! 글 ID: {post_id}")
        print(f"     제목: {title}")
        print("="*60)
        return True
    else:
        print("[FAIL] 발행 실패")
        return False

if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n[FATAL] {e}")
        import traceback
        traceback.print_exc()
        exit(1)
