#!/usr/bin/env python3
import os
import requests
import json
from typing import Dict, Optional
from dotenv import load_dotenv
import base64

load_dotenv()

class WordPressPoster:
    def __init__(self):
        self.site_url = os.getenv("WP_SITE_URL", "https://digital-income7771.com")
        self.username = "aceguy7771@gmail.com"
        self.app_password = os.getenv("WP_APP_PASSWORD", "")
        self.rest_api_url = f"{self.site_url}/wp-json/wp/v2"
        self.auth = self._setup_auth()

    def _setup_auth(self):
        credentials = f"{self.username}:{self.app_password}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return {"Authorization": f"Basic {encoded}"}

    def post_article(self, title: str, content: str, category: str = "재테크", tags: list = None, status: str = "publish") -> Dict:
        category_id = self._get_category_id(category)
        if not category_id:
            print(f"[WARN] 카테고리 '{category}' 없음")
            category_id = 1

        tag_ids = []
        if tags:
            tag_ids = self._get_tag_ids(tags)

        post_data = {
            "title": title,
            "content": content,
            "status": status,
            "categories": [category_id],
            "tags": tag_ids,
            "excerpt": content[:200] if len(content) > 200 else content,
        }

        response = requests.post(
            f"{self.rest_api_url}/posts",
            json=post_data,
            headers=self.auth,
            timeout=30
        )

        if response.status_code in [200, 201]:
            post = response.json()
            return {
                "status": "[OK] 발행 성공",
                "post_id": post["id"],
                "post_url": post["link"],
                "title": post["title"]["rendered"],
                "published_at": post["date"]
            }
        else:
            return {
                "status": f"[FAIL] 발행 실패 (HTTP {response.status_code})",
                "error": response.text,
                "message": "WordPress REST API 연결 확인"
            }

    def _get_category_id(self, category_name: str) -> Optional[int]:
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
            print(f"[ERROR] 카테고리 조회 오류: {e}")
        return None

    def _get_tag_ids(self, tag_names: list) -> list:
        tag_ids = []
        for tag_name in tag_names:
            try:
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
                print(f"[ERROR] 태그 처리 오류 ({tag_name}): {e}")

        return tag_ids

    def validate_connection(self) -> bool:
        try:
            response = requests.get(
                f"{self.rest_api_url}/posts",
                headers=self.auth,
                timeout=10,
                params={"per_page": 1}
            )
            if response.status_code == 200:
                print("[OK] WordPress REST API 연결 성공")
                return True
            else:
                print(f"[FAIL] 연결 실패 (HTTP {response.status_code})")
                return False
        except Exception as e:
            print(f"[ERROR] 연결 오류: {e}")
            return False
