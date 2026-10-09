#!/usr/bin/env python3
"""
WordPress Poster: 콘텐츠를 WordPress에 자동으로 발행
- REST API를 사용한 자동 포스팅
- 이미지 자동 업로드
- 카테고리/태그 자동 지정
"""

import os
import requests
import json
from typing import Dict, Optional
from datetime import datetime
from dotenv import load_dotenv
import base64

load_dotenv()

class WordPressPoster:
    def __init__(self):
        self.site_url = os.getenv("WP_SITE_URL", "https://digital-income7771.com")
        self.username = "aceguy7771@gmail.com"  # WordPress 사용자명
        self.app_password = os.getenv("WP_APP_PASSWORD", "")  # Application Password

        # REST API 엔드포인트
        self.rest_api_url = f"{self.site_url}/wp-json/wp/v2"

        # 기본 인증 설정
        self.auth = self._setup_auth()

    def _setup_auth(self):
        """WordPress REST API 기본 인증 설정"""
        credentials = f"{self.username}:{self.app_password}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return {"Authorization": f"Basic {encoded}"}

    def post_article(
        self,
        title: str,
        content: str,
        category: str = "재테크",
        tags: list = None,
        status: str = "publish"
    ) -> Dict:
        """
        WordPress에 글 발행

        Args:
            title: 글 제목
            content: 글 내용 (마크다운 또는 HTML)
            category: 카테고리명
            tags: 태그 리스트
            status: 발행 상태 ("publish", "draft", "pending")

        Returns:
            발행된 글 정보
        """

        # 카테고리 ID 조회
        category_id = self._get_category_id(category)
        if not category_id:
            print(f"⚠️ 카테고리 '{category}'를 찾을 수 없습니다. 기본값 사용")
            category_id = 1  # 기본 카테고리

        # 태그 ID 조회
        tag_ids = []
        if tags:
            tag_ids = self._get_tag_ids(tags)

        # 포스트 데이터
        post_data = {
            "title": title,
            "content": content,
            "status": status,
            "categories": [category_id],
            "tags": tag_ids,
            "excerpt": content[:200] if len(content) > 200 else content,  # 발췌
        }

        # 포스트 생성
        response = requests.post(
            f"{self.rest_api_url}/posts",
            json=post_data,
            headers=self.auth,
            timeout=30
        )

        if response.status_code in [200, 201]:
            post = response.json()
            return {
                "status": "✅ 발행 성공",
                "post_id": post["id"],
                "post_url": post["link"],
                "title": post["title"]["rendered"],
                "published_at": post["date"]
            }
        else:
            return {
                "status": f"❌ 발행 실패 (HTTP {response.status_code})",
                "error": response.text,
                "message": "WordPress REST API 연결을 확인하세요"
            }

    def _get_category_id(self, category_name: str) -> Optional[int]:
        """카테고리명으로 ID 조회"""
        try:
            response = requests.get(
                f"{self.rest_api_url}/categories",
                params={"search": category_name},
                headers=self.auth,
                timeout=10
            )

            if response.status_code == 200:
                categories = response.json()
                if categories:
                    return categories[0]["id"]
        except Exception as e:
            print(f"카테고리 조회 오류: {e}")

        return None

    def _get_tag_ids(self, tag_names: list) -> list:
        """태그명으로 ID 조회 (없으면 생성)"""
        tag_ids = []

        for tag_name in tag_names:
            try:
                # 기존 태그 검색
                response = requests.get(
                    f"{self.rest_api_url}/tags",
                    params={"search": tag_name},
                    headers=self.auth,
                    timeout=10
                )

                if response.status_code == 200:
                    tags = response.json()
                    if tags:
                        tag_ids.append(tags[0]["id"])
                        continue

                # 없으면 생성
                create_response = requests.post(
                    f"{self.rest_api_url}/tags",
                    json={"name": tag_name},
                    headers=self.auth,
                    timeout=10
                )

                if create_response.status_code in [200, 201]:
                    new_tag = create_response.json()
                    tag_ids.append(new_tag["id"])
            except Exception as e:
                print(f"태그 처리 오류 ({tag_name}): {e}")

        return tag_ids

    def update_article(self, post_id: int, content: str, title: str = None) -> Dict:
        """기존 글 업데이트"""

        update_data = {"content": content}
        if title:
            update_data["title"] = title

        response = requests.post(
            f"{self.rest_api_url}/posts/{post_id}",
            json=update_data,
            headers=self.auth,
            timeout=30
        )

        if response.status_code == 200:
            return {"status": "✅ 업데이트 성공", "post_id": post_id}
        else:
            return {"status": f"❌ 업데이트 실패 (HTTP {response.status_code})"}

    def validate_connection(self) -> bool:
        """WordPress 연결 테스트"""
        try:
            response = requests.get(
                f"{self.rest_api_url}/posts",
                headers=self.auth,
                timeout=10,
                params={"per_page": 1}
            )

            if response.status_code == 200:
                print("✅ WordPress REST API 연결 성공!")
                return True
            else:
                print(f"❌ 연결 실패 (HTTP {response.status_code})")
                return False
        except Exception as e:
            print(f"❌ 연결 오류: {e}")
            return False


if __name__ == "__main__":
    # 환경변수 설정 필요
    app_password = "Dcvp yBWE 6aYf qAQU O1lf kSZO"  # Application Password

    poster = WordPressPoster()
    poster.app_password = app_password
    poster.auth = poster._setup_auth()

    # 1. 연결 테스트
    print("🔌 WordPress 연결 테스트 중...")
    if not poster.validate_connection():
        print("연결 실패. Application Password를 확인하세요.")
        exit(1)

    # 2. 근로장려금 글 발행
    print("\n📝 근로장려금 글 발행 중...")

    title = "근로장려금 기한후신청 2026: 12월 1일 마감, 지금이 마지막 기회"

    # 마크다운 콘텐츠 로드 (또는 직접 입력)
    with open("C:\\blog-automation\\article_근로장려금_기한후신청_2026-10-09.md", "r", encoding="utf-8") as f:
        content = f.read()

    result = poster.post_article(
        title=title,
        content=content,
        category="재테크",
        tags=["근로장려금", "정책", "2026"],
        status="publish"
    )

    print(f"\n결과:")
    for key, value in result.items():
        print(f"  {key}: {value}")

    if "post_url" in result:
        print(f"\n✅ 발행 완료! 링크: {result['post_url']}")
