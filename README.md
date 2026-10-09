# Blog Automation System

자동화된 WordPress 블로그 글 생성 및 발행 시스템입니다.

**상태**: ✅ GitHub Actions로 자동화 중

---

## 기능

- ✅ 매일 자동 글 생성
- ✅ 주제별 이미지 자동 선택
- ✅ 마크다운 → HTML 자동 변환
- ✅ WordPress REST API로 자동 발행
- ✅ GitHub Actions로 24시간 자동 운영

---

## 빠른 시작

### 1. GitHub 저장소 생성

```bash
cd C:\blog-automation
git init
git add .
git commit -m "Initial commit: blog automation"
git remote add origin https://github.com/YOUR_USERNAME/blog-automation.git
git branch -M main
git push -u origin main
```

### 2. GitHub Secrets 설정

저장소 → Settings → Secrets and variables → Actions

다음 secrets 추가:
- `WP_SITE_URL`: https://digital-income7771.com
- `WP_EMAIL`: aceguy7771@gmail.com
- `WP_APP_PASSWORD`: (WordPress Application Password)

### 3. 자동 실행 시작

GitHub Actions가 매일 오후 6시에 자동 실행됩니다!

---

## 파일

- `daily_post.py` - 메인 자동 발행 스크립트
- `.github/workflows/daily-post.yml` - GitHub Actions 워크플로우
- `requirements.txt` - Python 의존성

---

## 일정

- **실행 시간**: 매일 오후 6시 (한국 시간)
- **자동화 플랫폼**: GitHub Actions
- **배포**: 24/7 자동 운영

---

**상태**: ✅ 운영 중
