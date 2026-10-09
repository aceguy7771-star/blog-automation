#!/usr/bin/env python3
"""
5개 글을 한 번에 WordPress에 자동 발행하는 스크립트
"""

import os
import glob
from dotenv import load_dotenv
from scripts.wordpress_poster import WordPressPoster

load_dotenv()

# 발행할 글 목록
articles = [
    ("article_연말정산_준비_2026-10-09.md", "연말정산 완벽 준비 가이드 2026: 지금부터 시작하면 10만원 절약", ["연말정산", "세금", "2026"]),
    ("article_절세팁_2026-10-09.md", "절세 팁 Top 5: 직장인이 꼭 알아야 할 세금 절약 전략", ["절세", "세금", "재테크"]),
    ("article_정부지원금_2026-10-09.md", "2026년 직장인이 받을 수 있는 정부 지원금 완벽 가이드", ["정부지원금", "지원", "정책"]),
    ("article_2027세금정책_2026-10-09.md", "2027년 변경되는 세금 정책: 직장인이 알아야 할 5가지", ["세금", "정책", "2027"]),
    ("article_부업돈버는법_2026-10-09.md", "직장인 부업 가이드 2026: 월 50-200만원 버는 실전 전략", ["부업", "재테크", "돈벌기"]),
]

def main():
    # WordPress 포스터 초기화
    poster = WordPressPoster()
    poster.app_password = os.getenv("WP_APP_PASSWORD", "Dcvp yBWE 6aYf qAQU O1lf kSZO")
    poster.auth = poster._setup_auth()

    # 연결 테스트
    print("🔌 WordPress 연결 테스트 중...")
    if not poster.validate_connection():
        print("❌ 연결 실패. Application Password를 확인하세요.")
        return

    print("✅ WordPress 연결 성공!\n")

    # 5개 글 발행
    results = []
    for filename, title, tags in articles:
        filepath = f"C:\\blog-automation\\{filename}"

        if not os.path.exists(filepath):
            print(f"⚠️ {filename} 파일 없음")
            continue

        # 마크다운 파일 읽기
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # 발행
        print(f"📝 발행 중: {title}...")
        result = poster.post_article(
            title=title,
            content=content,
            category="재테크",
            tags=tags,
            status="publish"
        )

        results.append({
            "file": filename,
            "title": title,
            "result": result
        })

        # 결과 출력
        if "post_id" in result:
            print(f"  ✅ 발행 성공 (ID: {result['post_id']})")
            print(f"  🔗 링크: {result['post_url']}\n")
        else:
            print(f"  ❌ 발행 실패: {result.get('error', '알 수 없는 오류')}\n")

    # 최종 결과
    print("\n" + "="*50)
    print("📊 최종 결과")
    print("="*50)

    success_count = sum(1 for r in results if "post_id" in r["result"])
    print(f"✅ 성공: {success_count}개")
    print(f"❌ 실패: {len(results) - success_count}개")

    if success_count == len(results):
        print("\n🎉 모든 글이 성공적으로 발행되었습니다!!")

    return results

if __name__ == "__main__":
    main()
