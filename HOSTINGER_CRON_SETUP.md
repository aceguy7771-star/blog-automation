# Hostinger Cron 자동 발행 설정 가이드

## 단계 1: Hostinger 제어판 접속

1. https://hpanel.hostinger.com 접속
2. 로그인
3. "웹사이트" → "digital-income7771.com" 선택

## 단계 2: Cron Jobs 섹션 찾기

**방법 A: 도구 메뉴에서**
- 웹사이트 카드 하단의 "도구" 드롭다운 클릭
- "Cron Jobs" 또는 "Advanced" 섹션 찾기

**방법 B: 직접 URL 접속**
다음 URL로 직접 접속하면 cPanel에 접근할 수 있습니다:
```
https://hpanel.hostinger.com/websites/digital-income7771.com/tools
```

**방법 C: cPanel 직접 접속**
Hostinger 제어판에서 cPanel 직접 접근:
1. 호스팅 설정 → Advanced 또는 Tools
2. cPanel/WHM 링크 클릭
3. "Cron Jobs" 찾기

## 단계 3: 새 Cron Job 추가

### 옵션 1: Python 스크립트 직접 실행

**파일 경로**: `/home/username/public_html/daily_post.py`

**시간 설정**: 매일 오후 6시 (18:00)
```
0 18 * * *
```

**명령어**:
```bash
cd /home/username/public_html && python daily_post.py >> /home/username/cron_logs/daily_post.log 2>&1
```

### 옵션 2: PHP/Bash를 통한 호출

**시간 설정**: 매일 오후 6시
```
0 18 * * *
```

**명령어**:
```bash
cd /home/username/public_html && /usr/bin/python3 daily_post.py
```

## 단계 4: 로그 폴더 생성 (선택사항)

실행 결과를 확인하려면 로그 폴더를 생성합니다:

```bash
mkdir -p /home/username/cron_logs
chmod 755 /home/username/cron_logs
```

## 단계 5: 테스트

1. Cron 설정 저장 후
2. 로그 폴더에서 일일 로그 확인
3. 블로그에서 새 글이 발행되었는지 확인

---

## Cron 시간 표현식 설명

```
분  시간  일  월  요일
0   18   *   *   *
↑   ↑   ↑  ↑   ↑
|   |   |  |   └─ 요일 (0=일, 1=월, ..., 6=토)
|   |   |  └────── 월 (1-12)
|   |   └───────── 일 (1-31)
|   └──────────── 시간 (0-23)
└─────────────── 분 (0-59)
```

**예시**:
- `0 18 * * *` = 매일 오후 6시
- `0 6 * * *` = 매일 오전 6시
- `*/30 * * * *` = 매 30분마다

---

## 명령어 최적화

더 효율적인 명령어:

```bash
python3 /home/username/public_html/daily_post.py > /dev/null 2>&1
```

또는 로그 보관:

```bash
python3 /home/username/public_html/daily_post.py >> /home/username/public_html/logs/cron.log 2>&1
```

---

## 문제 해결

### 1. 스크립트가 실행되지 않음

**확인 사항**:
- Python 경로 확인: `which python3`
- 스크립트 권한: `chmod +x daily_post.py`
- 의존성 설치: `pip install -r requirements.txt`

### 2. WordPress 연결 오류

**확인 사항**:
- WP_SITE_URL, WP_EMAIL, WP_APP_PASSWORD 확인
- WordPress REST API 활성화 확인

### 3. 로그 파일에서 오류 확인

```bash
# 로그 파일 확인
cat /home/username/cron_logs/daily_post.log

# 최근 로그만 확인
tail -f /home/username/cron_logs/daily_post.log
```

---

## 자동 백업

매주 스크립트를 백업하려면:

```bash
0 0 * * 0 cd /home/username/public_html && tar -czf backups/blog_$(date +\%Y\%m\%d).tar.gz *.py && find backups -name "blog_*.tar.gz" -mtime +30 -delete
```

---

## 다음 단계

1. Cron 설정 완료
2. 24시간 대기 후 블로그 확인
3. 글 자동 발행 확인
4. 기존 글 개선 (이미지 추가, 원본성 강화)
5. AdSense 재신청 준비
