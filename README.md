## 구글 검색 결과 피싱사이트 탐지 시스템

### 동작
- `scikit-image의 SSIM(Structural Similarity Index)` 이용
- 정상 서비스에 접속하여 메인페이지 및 로그인 페이지 스크린샷을 찍음
- 모든 스크린샷 이미지는 gary로 저장
- 검색 결과 100개까지의 URL 수집
    - 한글, 영어 모두 검색
- 수집한 URL에 하나씩 접속하여 스크린샷을 찍음
- 정상 서비스의 스크린샷과 비교하여 유사도(ssim)를 측정
- 정상 서비스의 스크린샷과 비교하여 평균제곱오차(mse)를 측정(오탐을 줄이기위해 추가)
    - ssim score가 95.5이상 & mse score가 300이하인 경우 slack알람
- user-agent로 mobile 페이지 확인
