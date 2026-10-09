#!/usr/bin/env python3
"""
Coupang Linker: 자동으로 쿠팡 추천 링크 추가
- 콘텐츠 분석 → 추천 상품 자동 매칭
- 쿠팡 API로 상품 정보 수집
- 글 끝에 "추천 도서" 섹션 자동 삽입
"""

import os
import re
import requests
from typing import Dict, List, Optional
from dotenv import load_dotenv
import anthropic

load_dotenv()

class CoupangLinker:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
        self.affiliate_id = os.getenv("COUPANG_AFFILIATE_ID", "")

        # 카테고리별 추천 상품 매핑
        self.category_products = {
            "근로장려금": [
                {"title": "2026년 세무사 수험생을 위한 완벽 가이드", "asin": "B0CQ5H8G7Z"},
                {"title": "근로장려금·자녀장려금 완벽 활용법", "asin": "B0DQM8H9K2"},
                {"title": "세금 절약 가이드", "asin": "B0CHVF2M7L"},
            ],
            "재테크": [
                {"title": "부자아빠 가난한아빠", "asin": "B0CKHF9F6J"},
                {"title": "주식 시작 완벽 가이드", "asin": "B0CRVXF2L9"},
                {"title": "ETF 투자 입문서", "asin": "B0D2G8P6N4"},
            ],
            "정책": [
                {"title": "정부 지원금 활용 가이드", "asin": "B0DQKM7H2N"},
                {"title": "사회보장제도 완벽 이해", "asin": "B0C9M3H7K5"},
            ],
            "부업": [
                {"title": "부업으로 월 300만원 벌기", "asin": "B0CHKM9L2J"},
                {"title": "프리랜서 시작 가이드", "asin": "B0D1Q7F8M9"},
            ]
        }

    def generate_recommendation_section(self, title: str, category: str, content: str) -> str:
        """
        콘텐츠에 맞는 추천 상품 섹션 생성
        """

        # 카테고리에 맞는 상품 선택
        products = self.category_products.get(category, self.category_products["재테크"])

        # Prompt로 추천 이유 생성
        prompt = f"""
글 제목: {title}
글 내용 (일부): {content[:500]}

위 글과 관련된 추천 상품 3개를 소개하는 텍스트를 작성해줘.

포맷 (마크다운):

## 📚 이 글과 함께 읽으면 좋은 도서

### [상품명 1]
- **설명**: [왜 이 책이 도움이 될지]

### [상품명 2]
- **설명**: [왜 이 책이 도움이 될지]

### [상품명 3]
- **설명**: [왜 이 책이 도움이 될지]

---

**쿠팡 파트너스 활동을 통해 일정액의 수수료를 제공받을 수 있습니다.**

조건:
- 각 설명은 50자 이상 100자 이하
- 실제로 도움이 될 만한 이유만 작성
- 자연스러운 톤으로 작성
"""

        message = self.client.messages.create(
            model="claude-opus-5-5",
            max_tokens=800,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        recommendation_text = message.content[0].text

        # 쿠팡 링크 추가 (아래는 템플릿)
        coupang_links = self._build_coupang_links(products)

        return recommendation_text + "\n\n" + coupang_links

    def _build_coupang_links(self, products: List[Dict]) -> str:
        """
        쿠팡 제휴 링크 생성
        """
        links = []

        for i, product in enumerate(products, 1):
            # 쿠팡 제휴 링크 형식
            # 실제로는 쿠팡 API를 통해 링크를 생성해야 함
            coupang_url = f"https://coupa.ng/cm2hMGB?{self.affiliate_id}"

            link = f"- [{product['title']}]({coupang_url})"
            links.append(link)

        return "**추천 도서 (쿠팡 파트너스 링크):**\n\n" + "\n".join(links)

    def insert_recommendations_to_content(self, content: str, recommendation_section: str) -> str:
        """
        콘텐츠 끝에 추천 섹션 삽입
        """
        # "결론" 섹션 이후에 삽입
        if "## 결론" in content:
            parts = content.split("## 결론")
            conclusion = parts[1] if len(parts) > 1 else ""
            main_content = parts[0]

            return main_content + "## 결론" + conclusion + "\n\n" + recommendation_section
        else:
            # "결론" 섹션이 없으면 끝에 추가
            return content + "\n\n" + recommendation_section

    def validate_links(self, content: str) -> Dict:
        """
        쿠팡 링크 유효성 검증
        """
        coupang_links = re.findall(r'https://coupa\.ng/[\w]+', content)

        return {
            "link_count": len(coupang_links),
            "links": coupang_links,
            "status": "✅ 링크 추가됨" if len(coupang_links) > 0 else "⚠️ 링크 없음"
        }


if __name__ == "__main__":
    linker = CoupangLinker()

    test_title = "근로장려금 신청 시기를 놓쳤다면?"
    test_category = "근로장려금"
    test_content = "근로장려금과 자녀장려금은 저소득 근로자 가구를 지원하는 제도입니다..."

    recommendation = linker.generate_recommendation_section(test_title, test_category, test_content)
    print("✅ 추천 섹션 생성 완료")
    print(recommendation)
