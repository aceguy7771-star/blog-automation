# 🚀 Blog Automation: AdSense 통과 + 수익화 시스템

Google AdSense 통과를 위한 **고품질 콘텐츠 자동화 시스템**입니다.
원본성 강화, 쿠팡 링크 자동화, SEO 최적화를 통해 월 70-150만원 수익을 목표합니다.

## 📊 목표

| 항목 | 목표 |
|------|------|
| **AdSense 승인** | 2026년 12월 (90일 후) |
| **월 트래픽** | 1000+ PV |
| **쿠팡 수익** | 월 20-50만원 |
| **AdSense 수익** | 월 50-100만원 |
| **총 수익** | 월 70-150만원 |

## 🎯 핵심 전략

### 1️⃣ 원본성 강화 (80% 이상 유지)
```
기존: AI 요약만 → 새로움: AI 요약 + 재작성 + 오리지널 분석
```
- 동일한 의미를 다양한 표현으로 작성
- 유사도 계산으로 검증 (80% 이상)
- 오리지널 분석 섹션 자동 추가 (200자+)

### 2️⃣ 콘텐츠 깊이 증대
- "전문가 분석" 섹션 자동 생성
- "주의사항" 및 "변경 예상사항" 추가
- FAQ 섹션 자동 생성 (5-10개)

### 3️⃣ 쿠팡 링크 통합
- 콘텐츠 분석 → 추천 상품 자동 매칭
- 카테고리별 추천 도서 자동 삽입
- 클릭 추적 및 수익 모니터링

### 4️⃣ Ads.txt 설정
- Google AdSense 기술적 요구사항 충족
- 광고 네트워크 명확히 등록
- 신뢰도 증대

### 5️⃣ 트래픽 확보
- Pinterest 자동 핀 생성
- 내부 링크 최적화
- SEO 메타 태그 자동 생성

## 📁 프로젝트 구조

```
blog-automation/
├── scripts/
│   ├── content_generator.py      # ⭐ 원본성 강화 AI
│   ├── coupang_linker.py         # 쿠팡 링크 자동화
│   ├── seo_optimizer.py          # SEO 최적화
│   ├── ads_txt_generator.py      # Ads.txt 자동 생성
│   ├── wordpress_poster.py       # WordPress 자동 발행
│   └── pinterest_pins.py         # Pinterest 자동 핀 생성
├── config/
│   ├── wordpress_config.json     # WordPress 설정
│   ├── adsense_config.json       # AdSense 설정
│   └── coupang_config.json       # 쿠팡 설정
├── templates/
│   └── content_templates.md      # 콘텐츠 템플릿
├── logs/
│   └── blog_automation.log       # 실행 로그
├── requirements.txt              # Python 의존성
├── .env.example                  # 환경변수 템플릿
└── README.md                     # 이 파일
```

## 🚀 빠른 시작

### 1단계: 설치

```bash
# 저장소 복제
git clone https://github.com/aceguy7771-star/blog-automation.git
cd blog-automation

# 환경 설정
cp .env.example .env
# .env 파일 편집해서 API 키 입력

# 의존성 설치
pip install -r requirements.txt
```

### 2단계: 환경 변수 설정

`.env` 파일을 편집해서 다음을 입력:

```env
# WordPress
WP_SITE_URL=https://your-blog.com
WP_USERNAME=your_username
WP_PASSWORD=your_password

# Claude API
CLAUDE_API_KEY=sk-ant-xxxxx

# AdSense
ADSENSE_PUBLISHER_ID=pub-xxxxxxxxxxxxxxxx

# Coupang
COUPANG_AFFILIATE_ID=your_affiliate_id

# 기타
DAILY_POST_COUNT=1
SIMILARITY_THRESHOLD=0.80
```

### 3단계: 자동화 실행

```bash
# 콘텐츠 생성 테스트
python scripts/content_generator.py

# Ads.txt 생성
python scripts/ads_txt_generator.py

# 쿠팡 링크 테스트
python scripts/coupang_linker.py
```

## 📊 각 스크립트 설명

### content_generator.py
**목적**: 원본성 강화된 고품질 콘텐츠 생성

**작동 원리**:
1. WebSearch로 기본 정보 수집
2. Claude AI로 다양한 각도의 요약 생성
3. 유사도 검사 (80% 이상 유지)
4. 오리지널 분석 섹션 자동 추가
5. FAQ 섹션 생성
6. 최종 품질 검증

**사용법**:
```python
from scripts.content_generator import ContentGenerator

generator = ContentGenerator()
result = generator.generate_content(
    title="블로그 제목",
    topic="주제",
    research_content="수집한 콘텐츠",
    category="재테크"
)
print(result['content'])
print(f"유사도: {result['similarity_score']:.2%}")
```

### coupang_linker.py
**목적**: 자동으로 쿠팡 추천 링크 추가

**작동 원리**:
1. 콘텐츠 카테고리 분석
2. 카테고리별 추천 상품 매칭
3. 추천 이유 자동 생성
4. 쿠팡 제휴 링크 삽입

**사용법**:
```python
from scripts.coupang_linker import CoupangLinker

linker = CoupangLinker()
recommendation = linker.generate_recommendation_section(
    title="블로그 제목",
    category="근로장려금",
    content="블로그 내용"
)
```

### ads_txt_generator.py
**목적**: Ads.txt 파일 자동 생성 및 관리

**작동 원리**:
1. 올바른 Ads.txt 포맷 생성
2. Google AdSense Publisher ID 등록
3. 파일 유효성 검증
4. 설정 지침 자동 생성

**사용법**:
```python
from scripts.ads_txt_generator import AdsTxtGenerator

generator = AdsTxtGenerator()
result = generator.save_ads_txt("path/to/ads.txt")
print(result['message'])

# 검증
validation = generator.validate_ads_txt("https://your-blog.com")
```

## 📈 예상 효과

### Phase별 수익 예상

| Phase | 기간 | 예상 수익 | 누적 수익 |
|-------|------|----------|---------|
| 1-2주 | 콘텐츠 개선 | 0원 | 0원 |
| 3주 | 쿠팡 링크 | 월 5-20만원 | 월 5-20만원 |
| 4-6주 | Pinterest | 월 10-30만원 | 월 15-50만원 |
| 90일 후 | AdSense 재신청 | 월 50-100만원 | 월 70-150만원 |

### 성공 요인

✅ **원본성 강화**: AI만의 느낌 제거, 신뢰도 증대
✅ **깊이 있는 콘텐츠**: 오리지널 분석, FAQ 추가
✅ **기술적 요구사항**: Ads.txt 설정으로 신뢰도 향상
✅ **다중 수익 채널**: 쿠팡 + AdSense 병행
✅ **지속적 개선**: 매일 새로운 고품질 콘텐츠

## 🔧 문제 해결

### Q: "저품질 콘텐츠" 거절이 계속되면?
A: 콘텐츠 생성 시 original percentage를 50% 이상으로 높이세요.
```python
# content_generator.py에서
ORIGINAL_CONTENT_MIN_LENGTH = 300  # 더 큰 오리지널 섹션
```

### Q: Ads.txt 파일이 안 보이면?
A: 호스팅어 파일 매니저에서 `/public_html/ads.txt` 확인:
1. 권한: 644로 설정
2. HTTPS로 접근 (HTTP 아님)
3. 캐시 삭제 후 재접근

### Q: 쿠팡 링크에서 클릭이 안 나오면?
A: 다음을 확인하세요:
1. 쿠팡 API 토큰 유효성
2. 추천 상품이 현재 판매 중인지
3. 링크 형식 검증

## 📚 참고 자료

- [Google AdSense 정책](https://support.google.com/adsense)
- [Ads.txt 가이드](https://iabtechlab.com/ads-txt)
- [WordPress REST API](https://developer.wordpress.org/rest-api/)
- [Claude API 문서](https://docs.anthropic.com)

## 🤝 기여

개선 사항이나 버그 리포트는 Issue를 통해 제출해주세요.

## 📄 라이센스

MIT License - 자유롭게 사용하세요!

## 📞 지원

문제가 있으면 다음을 확인하세요:
1. `.env` 파일의 API 키 설정
2. `requirements.txt` 의존성 설치
3. Python 3.10+ 버전
4. 인터넷 연결

---

**최종 목표**: AdSense 승인 + 월 100만원 수익화 🎉

다른 질문이 있으면 GitHub Issues에 등록해주세요!
