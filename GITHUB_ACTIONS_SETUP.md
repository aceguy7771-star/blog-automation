# GitHub Actions 자동화 설정 가이드

## 완료 항목 ✅

- ✅ `daily_post.py` - 자동 글 생성 및 발행 스크립트
- ✅ `.github/workflows/daily-post.yml` - GitHub Actions 워크플로우
- ✅ `.env.example` - 환경변수 템플릿
- ✅ `.gitignore` - Git 무시 파일
- ✅ `README.md` - 프로젝트 설명

---

## 단계별 설정

### 1단계: GitHub 저장소 생성

#### A. GitHub 웹사이트에서
1. https://github.com/new 접속
2. 로그인 (aceguy7771@gmail.com)
3. Repository name: `blog-automation`
4. Description: `자동화된 WordPress 블로그 글 생성 및 발행 시스템`
5. Public/Private: **Private** 선택 (비공개)
6. "Create repository" 클릭

#### B. 로컬에서 GitHub에 푸시

```bash
cd C:\blog-automation
git init
git add .
git commit -m "Initial commit: automated blog posting system"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/blog-automation.git
git push -u origin main
```

**주의**: `YOUR_USERNAME`을 실제 GitHub 사용자명으로 바꾸세요!

---

### 2단계: GitHub Secrets 설정

1. **GitHub 저장소 접속**
   - https://github.com/YOUR_USERNAME/blog-automation

2. **Settings 탭 클릭**
   - 상단 메뉴 → Settings

3. **Secrets and variables 선택**
   - 왼쪽 메뉴 → Secrets and variables → Actions

4. **Repository secrets 생성**
   
   "New repository secret" 클릭하고 다음 3개 추가:

   **Secret 1: WP_SITE_URL**
   - Name: `WP_SITE_URL`
   - Value: `https://digital-income7771.com`
   - Add secret 클릭

   **Secret 2: WP_EMAIL**
   - Name: `WP_EMAIL`
   - Value: `aceguy7771@gmail.com`
   - Add secret 클릭

   **Secret 3: WP_APP_PASSWORD**
   - Name: `WP_APP_PASSWORD`
   - Value: `Dcvp yBWE 6aYf qAQU O1lf kSZO`
   - Add secret 클릭

---

### 3단계: 자동 실행 확인

1. **Actions 탭 클릭**
   - 저장소 → Actions

2. **"Daily Blog Post" 워크플로우 확인**
   - 좌측에 "Daily Blog Post" 표시

3. **수동 테스트** (선택사항)
   - "Run workflow" 클릭
   - "Run workflow" 다시 클릭
   - 실행 대기 (1-2분)
   - 로그 확인

---

## 자동 실행 일정

```
매일 오후 6시 (한국 시간)
= UTC 9:00 AM
```

**일정 표**:
| 지역 | 시간 |
|------|------|
| 한국 (KST) | 오후 6시 |
| 일본 (JST) | 오후 6시 |
| UTC | 오전 9시 |
| 영국 (GMT) | 오전 9시 |
| 미국 동부 (EST) | 오전 4시 (동절기) |
| 미국 서부 (PST) | 오전 1시 (동절기) |

---

## 작동 원리

### 매일 오후 6시 자동 실행:

1. GitHub Actions가 워크플로우 시작
2. Ubuntu 서버에서 실행
3. Python 3.11 환경 준비
4. 의존성 설치 (requests, markdown 등)
5. `daily_post.py` 실행
   - 글 생성
   - 이미지 선택
   - WordPress에 발행
6. 완료 (1-2분)

---

## 수동 실행 방법

### 방법 1: GitHub 웹사이트에서

1. 저장소 → Actions
2. "Daily Blog Post" 선택
3. "Run workflow" 드롭다운 클릭
4. "Run workflow" 버튼 클릭
5. 1-2분 대기
6. 로그 확인

### 방법 2: GitHub CLI (gcloud)

```bash
gh workflow run daily-post.yml --repo YOUR_USERNAME/blog-automation
```

---

## 실행 로그 확인

1. 저장소 → Actions
2. 최근 실행 선택
3. "Run daily post script" 단계 클릭
4. 출력 로그 확인

**예상 로그**:
```
[2026-10-10 18:00:00] [START] 자동 블로그 발행 시작
[2026-10-10 18:00:01] [1/3] 글 생성 중...
[2026-10-10 18:00:02] [2/3] HTML 변환 중...
[2026-10-10 18:00:03] [3/3] WordPress에 발행 중...
[2026-10-10 18:00:05] [OK] 발행 성공! ID: 331
```

---

## 문제 해결

### 1. 워크플로우가 실행되지 않음

**확인 사항**:
1. `.github/workflows/daily-post.yml` 파일 존재 확인
2. main 브랜치에 파일이 푸시됨 확인
3. Actions 탭에서 "Daily Blog Post" 보임 확인

**해결**:
```bash
git add .github/workflows/daily-post.yml
git commit -m "Add GitHub Actions workflow"
git push origin main
```

### 2. "401 Unauthorized" 오류

**원인**: GitHub Secrets 설정 오류

**해결**:
1. Settings → Secrets 확인
2. WP_SITE_URL, WP_EMAIL, WP_APP_PASSWORD 모두 있는지 확인
3. 값 앞뒤 공백 제거
4. 오류 발생 시 secret 삭제 후 다시 생성

### 3. "ModuleNotFoundError"

**원인**: Python 패키지 누락

**해결**: 이미 자동으로 설치됩니다. requirements.txt 확인하세요.

### 4. 글이 발행되지 않음

**로컬에서 테스트**:
```bash
# 로컬에서 스크립트 실행
python daily_post.py
```

**오류 메시지 확인**:
- 콘솔 출력 보기
- WordPress REST API 활성화 확인

---

## GitHub Actions 요금

- ✅ **공개 저장소**: 무제한 무료
- ✅ **비공개 저장소**: 월 2,000분 무료 (충분함!)

당신의 저장소는 비공개이므로, 매일 2-3분 실행해도 월 60-90분만 사용됩니다.

---

## 다음 단계

1. ✅ GitHub 저장소 생성
2. ✅ GitHub Secrets 설정
3. ✅ 워크플로우 확인
4. ⏳ 매일 오후 6시 자동 실행 시작
5. ⏳ 24시간 후 블로그에서 새 글 확인
6. ⏳ 기존 글 개선 (이미지 추가, 원본성 강화)
7. ⏳ AdSense 재신청 준비 (90일 후)

---

## 유용한 링크

- GitHub Actions 문서: https://docs.github.com/actions
- 워크플로우 문법: https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions
- Cron 표현식: https://crontab.guru/

---

## 시간대 변경

**한국시간 오후 6시에서 다른 시간으로 변경하려면**:

`.github/workflows/daily-post.yml` 파일에서:
```yaml
on:
  schedule:
    - cron: '0 9 * * *'  # ← 이 숫자를 수정
```

**Cron 시간 변환**:
- 오전 6시 KST = `0 21 * * *` (UTC 기준)
- 오후 12시 KST = `0 3 * * *`
- 자정 KST = `0 15 * * *`

[Crontab Guru](https://crontab.guru/)에서 시간대 확인 가능합니다.

---

**설정 완료!** ✅

이제 매일 오후 6시에 자동으로 블로그 글이 생성되고 발행됩니다! 🎉
