#!/usr/bin/env python3
"""
Hostinger Cron용 매일 자동 발행 스크립트
매일 오후 6시에 실행되어 새 글을 생성하고 WordPress에 발행합니다.
"""

import os
import sys
import requests
import base64
from datetime import datetime
import markdown

# WordPress 설정
WP_SITE_URL = "https://digital-income7771.com"
WP_EMAIL = "aceguy7771@gmail.com"
WP_APP_PASSWORD = "Dcvp yBWE 6aYf qAQU O1lf kSZO"

def log(message):
    """로그 출력"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def get_wp_auth_header():
    """WordPress 인증 헤더 생성"""
    credentials = f"{WP_EMAIL}:{WP_APP_PASSWORD}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {encoded}"}

def generate_fallback_article():
    """기본 글 생성"""
    today = datetime.now().strftime("%Y년 %m월 %d일")
    topics = [
        {
            "title": "프리랜서 원천징수, 연말정산에서 100만원 돌려받는 법",
            "content": f"""**작성일**: {today}

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
- 부업 소득이 2,000,000원 이상이면 사업자등록 고려

## 결론

프리랜서 수입도 성실하게 관리하면 세금 절약은 물론 신용도 향상됩니다. 연말정산을 제대로 챙겨 돌려받을 돈은 꼭 받으세요.""",
            "image": "https://images.unsplash.com/photo-1554224311-beee415c15cb?w=1200&h=600&fit=crop"
        },
        {
            "title": "2026년 11월 종합소득세 중간예납, 면제 기준이 달라졌다",
            "content": f"""**작성일**: {today}

11월은 종합소득세 중간예납 납부의 달입니다. 올해부터 소액부징수 기준이 50만원으로 상향되는 등 달라진 내용을 정리했습니다.

## 중간예납이란?

중간예납은 매년 11월에 예상 세액의 절반을 먼저 내는 제도입니다. 프리랜서나 사업소득이 있는 사람들이 대상입니다.

## 달라진 점 2026

- 소액부징수 기준: 30만원 → 50만원
- 납부 기한: 11월 30일
- 분할납부 가능

## 대상자 확인

- 전년도 종합소득세 신고자
- 부업 소득 2,000만원 이상
- 사업소득이 있는 사람

## 납부 방법

- 국세청 홈택스
- 은행 직접 납부
- 신용카드 납부 (수수료 발생)

미납시 가산세와 이자가 붙으므로 기한을 꼭 지키세요.""",
            "image": "https://images.unsplash.com/photo-1460925895917-adf4e565a87d?w=1200&h=600&fit=crop"
        },
        {
            "title": "해외 클라이언트에게 돈 받는 프리랜서, 와이즈·페이오니어 수수료를 숫자로 비교했다",
            "content": f"""**작성일**: {today}

해외 클라이언트에게 돈을 받는 프리랜서라면 와이즈와 페이오니어의 수수료 차이를 미리 알아두는 게 좋습니다. 실제 수치로 비교했습니다.

## 와이즈 (Wise)

- 환율: 시장 환율
- 수수료: 0.41-0.72% (금액에 따라 다름)
- 처리 시간: 1-3일
- 최소 송금액 제한 없음

## 페이오니어 (PayOneer)

- 환율: 시장 환율 기준
- 수수료: 2%
- 처리 시간: 1-2일
- 최소 송금액: 100달러

## 실제 비교 (1000달러 기준)

**와이즈**: 약 7-8달러 수수료
- 최종 수령: 992-993달러

**페이오니어**: 약 20달러 수수료
- 최종 수령: 980달러

## 결론

대부분의 경우 와이즈가 저렴합니다. 단, 페이오니어는 추가 기능(부업 관리 등)이 있습니다. 자신의 송금 패턴에 맞춰 선택하세요.""",
            "image": "https://images.unsplash.com/photo-1552664730-d307ca884978?w=1200&h=600&fit=crop"
        }
    ]

    import random
    topic = random.choice(topics)
    return topic["title"], topic["content"], topic["image"]

def convert_md_to_html(md_content, image_url):
    """마크다운을 HTML로 변환"""
    html = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
    image_html = f'<figure class="wp-block-image"><img src="{image_url}" alt="Article Image" width="1200" height="600" style="border-radius: 8px;" /></figure>'
    return image_html + html

def post_to_wordpress(title, html_content):
    """WordPress에 발행"""
    auth_header = get_wp_auth_header()

    post_data = {
        "title": title,
        "content": html_content,
        "status": "publish",
        "categories": [18],
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
            return True, post['id'], post['link']
        else:
            return False, None, response.text
    except Exception as e:
        return False, None, str(e)

def main():
    log("[START] 자동 블로그 발행 시작")

    try:
        # 글 생성
        log("[1/3] 글 생성 중...")
        title, md_content, image_url = generate_fallback_article()
        log(f"      제목: {title}")

        # HTML 변환
        log("[2/3] HTML 변환 중...")
        html_content = convert_md_to_html(md_content, image_url)

        # WordPress 발행
        log("[3/3] WordPress에 발행 중...")
        success, post_id, result = post_to_wordpress(title, html_content)

        if success:
            log(f"[OK] 발행 성공! ID: {post_id}")
            log(f"     URL: {result}")
            return 0
        else:
            log(f"[FAIL] 발행 실패: {result}")
            return 1

    except Exception as e:
        log(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
