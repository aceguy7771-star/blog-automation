#!/usr/bin/env python3
"""
Ads.txt Generator: AdSense Ads.txt 자동 생성 및 관리
- 올바른 Ads.txt 포맷 생성
- WordPress에 배포
- 유효성 검증
"""

import os
import requests
from datetime import datetime
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

class AdsTxtGenerator:
    def __init__(self):
        self.publisher_id = os.getenv("ADSENSE_PUBLISHER_ID", "pub-xxxxxxxxxxxxxxxx")
        self.site_url = os.getenv("WP_SITE_URL", "https://digital-income7771.com")

    def generate_ads_txt_content(self) -> str:
        """
        AdSense 및 기타 광고 네트워크를 위한 Ads.txt 생성
        """
        content = f"""# Ads.txt 파일
# 생성 날짜: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# 사이트: {self.site_url}
#
# Ads.txt 파일 정보:
# https://support.google.com/adsense/answer/7674157
# https://iabtechlab.com/ads-txt/

# Google AdSense
google.com, {self.publisher_id}, DIRECT, f08c47fec0942fa0

# 추가 광고 네트워크 (필요시)
# Naver AD-stir (한국)
# adstir.com, {self.publisher_id}, RESELLER, 36cf47b9674efa64

# Other Networks (추후 추가)
# openx.com, xxxxxxxx, DIRECT, 6a698e4a02da1ea9

# 참고:
# DIRECT: 직접 판매 계약
# RESELLER: 재판매 (미디어 바이어를 통한)
# UNKNOWN: 관계가 확인되지 않은 광고주
"""
        return content

    def save_ads_txt(self, filepath: str) -> Dict:
        """
        Ads.txt 파일 저장
        """
        try:
            content = self.generate_ads_txt_content()

            # 파일 저장
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            return {
                "status": "✅ 성공",
                "filepath": filepath,
                "content_length": len(content),
                "message": f"Ads.txt 파일이 저장되었습니다: {filepath}"
            }
        except Exception as e:
            return {
                "status": "❌ 실패",
                "error": str(e),
                "message": f"Ads.txt 저장 실패: {e}"
            }

    def upload_to_wordpress(self, wp_url: str, wp_rest_key: str) -> Dict:
        """
        WordPress의 루트 디렉토리에 Ads.txt 업로드
        """
        try:
            content = self.generate_ads_txt_content()

            # WordPress REST API를 통해 파일 업로드
            # 실제로는 SFTP 또는 FTP를 사용하거나
            # WordPress 플러그인을 사용해야 함

            headers = {
                "Authorization": f"Bearer {wp_rest_key}"
            }

            # 예시 (실제로는 더 복잡한 구현 필요)
            response = requests.post(
                f"{wp_url}/wp-json/wp/v2/media",
                headers=headers,
                files={"file": ("ads.txt", content)}
            )

            if response.status_code == 201:
                return {
                    "status": "✅ 업로드 완료",
                    "message": "Ads.txt가 WordPress에 업로드되었습니다",
                    "url": f"{wp_url}/ads.txt"
                }
            else:
                return {
                    "status": "⚠️ 업로드 실패",
                    "message": f"WordPress 업로드 실패: {response.status_code}",
                    "recommendation": "호스팅어 파일 매니저를 통해 수동으로 업로드하세요"
                }
        except Exception as e:
            return {
                "status": "❌ 오류",
                "error": str(e),
                "recommendation": "호스팅어 파일 매니저를 통해 수동으로 업로드하세요"
            }

    def validate_ads_txt(self, url: str) -> Dict:
        """
        Ads.txt 파일의 유효성 검증
        """
        try:
            response = requests.get(f"{url}/ads.txt", timeout=10)

            if response.status_code == 200:
                content = response.text

                # 기본 포맷 검증
                is_valid = "google.com" in content and self.publisher_id in content

                return {
                    "status": "✅ 파일 존재",
                    "is_valid": is_valid,
                    "content_length": len(content),
                    "has_google": "google.com" in content,
                    "has_publisher_id": self.publisher_id in content,
                    "message": "Ads.txt 파일이 올바르게 설정되었습니다" if is_valid else "Ads.txt 포맷 오류"
                }
            else:
                return {
                    "status": f"❌ 파일 없음 ({response.status_code})",
                    "message": f"Ads.txt를 찾을 수 없습니다: {url}/ads.txt",
                    "recommendation": "호스팅어 파일 매니저에서 /public_html/ads.txt 생성 필요"
                }
        except Exception as e:
            return {
                "status": "❌ 검증 실패",
                "error": str(e),
                "message": f"Ads.txt 검증 불가: {e}"
            }

    def generate_setup_instructions(self) -> str:
        """
        Ads.txt 설정 지침 생성
        """
        instructions = f"""
# 🚀 Ads.txt 설정 가이드

## 1단계: 파일 생성
아래 내용으로 `ads.txt` 파일을 생성하세요:

```
{self.generate_ads_txt_content()}
```

## 2단계: 호스팅어에서 업로드
1. 호스팅어 계정 로그인
2. 파일 매니저 열기
3. `/public_html/` 폴더로 이동
4. `ads.txt` 파일 생성/업로드
5. 권한: 644 설정

## 3단계: 검증
브라우저에서 아래 주소 방문:
{self.site_url}/ads.txt

## 4단계: AdSense 등록
1. Google AdSense 로그인
2. 설정 > 사이트
3. "Ads.txt를 확인할 수 없습니다" 알림 확인
4. "문제 해결" 클릭
5. "Ads.txt 파일 다운로드" 후 재업로드

## ✅ 완료!
Ads.txt 설정이 완료되면 AdSense 재신청이 가능합니다.

## 📌 주의사항
- Ads.txt는 HTTPS로만 접근 가능
- UTF-8 인코딩 사용
- 매달 업데이트 권장
- 주석(#)으로 설명 추가 가능
"""
        return instructions


if __name__ == "__main__":
    generator = AdsTxtGenerator()

    # 1. Ads.txt 파일 생성
    print("📝 Ads.txt 생성 중...")
    result = generator.save_ads_txt("C:\\blog-automation\\ads.txt")
    print(result["message"])

    # 2. 설정 지침 출력
    print("\n" + generator.generate_setup_instructions())

    # 3. 검증 (실제 사이트의 경우)
    print("\n🔍 Ads.txt 검증 중...")
    validation = generator.validate_ads_txt("https://digital-income7771.com")
    print(f"상태: {validation['status']}")
    if 'message' in validation:
        print(f"메시지: {validation['message']}")
