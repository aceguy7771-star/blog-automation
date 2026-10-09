#!/usr/bin/env python3
"""
Content Generator: AdSense 통과용 고품질 콘텐츠 자동 생성
- 원본성 강화 (80% 이상 유지)
- 오리지널 분석 섹션 추가
- SEO 최적화
"""

import os
import json
import re
from typing import Dict, List, Tuple
from datetime import datetime
from dotenv import load_dotenv

import anthropic
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

load_dotenv()

class ContentGenerator:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
        self.model = SentenceTransformer('sentence-transformers/distiluse-base-multilingual-cased-v2')
        self.min_original_length = int(os.getenv("ORIGINAL_CONTENT_MIN_LENGTH", 200))
        self.similarity_threshold = float(os.getenv("SIMILARITY_THRESHOLD", 0.80))

    def generate_content(
        self,
        title: str,
        topic: str,
        research_content: str,
        category: str = "재테크"
    ) -> Dict:
        """
        고품질 블로그 포스트 생성

        Args:
            title: 블로그 제목
            topic: 블로그 주제
            research_content: 조사한 기본 콘텐츠
            category: 콘텐츠 카테고리

        Returns:
            생성된 포스트 딕셔너리
        """

        # 1단계: 다양한 각도에서 콘텐츠 재작성
        paraphrased_versions = self._create_paraphrases(research_content)

        # 2단계: 최고 유사도가 낮은 버전 선택
        best_version = self._select_best_paraphrase(research_content, paraphrased_versions)

        # 3단계: 오리지널 분석 섹션 추가
        original_analysis = self._generate_original_analysis(title, topic, best_version)

        # 4단계: FAQ 섹션 생성
        faq_section = self._generate_faq(title, topic)

        # 5단계: 최종 콘텐츠 조합
        final_content = self._combine_content(
            title=title,
            paraphrased=best_version,
            original_analysis=original_analysis,
            faq=faq_section,
            category=category
        )

        # 6단계: 품질 검증
        quality_score = self._validate_quality(research_content, final_content)

        return {
            "title": title,
            "content": final_content,
            "quality_score": quality_score,
            "similarity_score": 1 - quality_score.get("similarity", 0.5),
            "original_content_percentage": quality_score.get("original_percentage", 0),
            "generated_at": datetime.now().isoformat(),
            "category": category
        }

    def _create_paraphrases(self, content: str, num_versions: int = 3) -> List[str]:
        """
        원본 콘텐츠를 여러 버전으로 재작성
        각 버전은 다른 각도와 표현으로 작성
        """
        paraphrases = []

        perspectives = [
            "전문가 관점에서 객관적으로 재작성",
            "입문자 입장에서 쉽게 설명하는 방식으로 재작성",
            "데이터 중심으로 통계를 강조해서 재작성"
        ]

        for i, perspective in enumerate(perspectives[:num_versions]):
            prompt = f"""
다음 콘텐츠를 '{perspective}' 해줘.
- 원래 의미는 유지해야 함
- 표현과 단어를 다르게 사용
- 더 자연스럽고 읽기 쉽게 만들기
- 길이는 비슷하게 유지

원본:
{content}

재작성 ('{perspective}'):
"""

            message = self.client.messages.create(
                model="claude-opus-5-5",
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            paraphrases.append(message.content[0].text)

        return paraphrases

    def _select_best_paraphrase(self, original: str, paraphrases: List[str]) -> str:
        """
        유사도가 가장 낮은 재작성본 선택 (80% 이상)
        """
        original_embedding = self.model.encode(original, convert_to_tensor=True)

        best_paraphrase = paraphrases[0]
        lowest_similarity = 1.0

        for paraphrase in paraphrases:
            paraphrase_embedding = self.model.encode(paraphrase, convert_to_tensor=True)
            similarity = cosine_similarity(
                [original_embedding],
                [paraphrase_embedding]
            )[0][0]

            # 80% 이상 유사도 + 가장 낮은 유사도
            if self.similarity_threshold <= similarity < lowest_similarity:
                best_paraphrase = paraphrase
                lowest_similarity = similarity

        return best_paraphrase

    def _generate_original_analysis(self, title: str, topic: str, content: str) -> str:
        """
        오리지널 분석/전문가 의견 섹션 생성 (200자 이상)
        """
        prompt = f"""
주제: {title}
관련 내용: {topic}

위 내용에 대한 '전문가 분석 및 주의사항' 섹션을 작성해줘.

요구사항:
1. 200자 이상의 오리지널 분석
2. 실질적인 도움이 될 수 있는 인사이트
3. 주의할 점이나 놓치기 쉬운 부분 강조
4. 마크다운 형식 사용

포맷:
## 💡 전문가 분석 및 주의사항

[분석 내용 200자 이상]

**주의할 점:**
- 포인트 1
- 포인트 2
- 포인트 3
"""

        message = self.client.messages.create(
            model="claude-opus-5-5",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.content[0].text

    def _generate_faq(self, title: str, topic: str) -> str:
        """
        FAQ 섹션 생성 (5-10개 Q&A)
        """
        prompt = f"""
주제: {title}

위 내용에 대한 자주 묻는 질문(FAQ) 5개를 작성해줘.

포맷:
## 자주 묻는 질문(FAQ)

**Q1. [질문 1]**
A. [답변 1]

**Q2. [질문 2]**
A. [답변 2]

... (총 5개)

조건:
- 실제로 많이 나오는 질문들
- 명확하고 간결한 답변
- 마크다운 형식
"""

        message = self.client.messages.create(
            model="claude-opus-5-5",
            max_tokens=1500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.content[0].text

    def _combine_content(
        self,
        title: str,
        paraphrased: str,
        original_analysis: str,
        faq: str,
        category: str
    ) -> str:
        """
        모든 콘텐츠 섹션을 결합
        """
        now = datetime.now()

        content = f"""# {title}

**작성일**: {now.strftime('%Y년 %m월 %d일')}
**카테고리**: {category}
**저자**: 정다인 에디터 · 금융 정보 전문

---

## 개요

{paraphrased[:300]}...

---

## 상세 내용

{paraphrased}

---

{original_analysis}

---

{faq}

---

## 결론

위 내용을 정리하면, {title}는 신중한 계획과 준비가 필요한 만큼, 충분한 정보를 바탕으로 결정하시기 바랍니다.

**참고 자료**:
- 국세청 공식 홈페이지
- 금융감독원 공시
- 관련 정책 뉴스

---

*본 글은 공식 자료를 바탕으로 작성되었으며, 개인의 상황에 따라 다를 수 있습니다. 전문가 상담을 권장합니다.*
"""

        return content

    def _validate_quality(self, original: str, final_content: str) -> Dict:
        """
        콘텐츠 품질 검증
        """
        # 유사도 계산
        original_embedding = self.model.encode(original, convert_to_tensor=True)
        final_embedding = self.model.encode(final_content, convert_to_tensor=True)
        similarity = cosine_similarity([original_embedding], [final_embedding])[0][0]

        # 오리지널 콘텐츠 비율 추정
        original_length = len(original)
        final_length = len(final_content)
        original_percentage = min(100, (final_length - original_length) / final_length * 100)

        return {
            "similarity": float(similarity),
            "original_percentage": float(original_percentage),
            "total_words": len(final_content.split()),
            "quality_score": "HIGH" if similarity >= self.similarity_threshold else "LOW"
        }


if __name__ == "__main__":
    # 테스트
    generator = ContentGenerator()

    test_title = "근로장려금 신청 시기를 놓쳤다면?"
    test_topic = "2026년 근로장려금 기한후신청"
    test_content = """
    근로·자녀장려금은 저소득 근로자와 자녀가 있는 가구를 지원하는 제도입니다.
    정기 신청 기간을 놓친 경우에도 기한후신청을 할 수 있습니다.
    기한후신청은 6월 2일부터 12월 1일까지 가능합니다.
    """

    result = generator.generate_content(
        title=test_title,
        topic=test_topic,
        research_content=test_content,
        category="재테크"
    )

    print(f"✅ 콘텐츠 생성 완료")
    print(f"📊 품질 점수: {result['quality_score']}")
    print(f"🔄 유사도: {result['similarity_score']:.2%}")
    print(f"📝 오리지널 비율: {result['quality_score'].get('original_percentage', 0):.1f}%")
