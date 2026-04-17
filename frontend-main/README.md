# 강원대 핼스장 어플리케이션

## 프로젝트 개요

1. 헬스장 사용자들의 트래픽이 몰려 병목현상으로 인해 제대로 운동을 못하는 사람들이 있다.
2. 가끔 헬스장 오픈 시간이 정해진 시간과는 다른 시간일 때가 있다.

## 타깃 사용자

- 1차: 헬스장 사용을 원하는 사람들
- 2차: 헬스장을 사용하고 있는 사람들

### 주요 기능

- 헬스장을 현재 사용 중인 인원을 알려주는 기능

## Commit Type 종류

- `feat`: 새로운 기능 추가
- `fix`: 버그 수정
- `docs`: 문서 수정
- `style`: 코드 포맷팅, 세미콜론 누락 등 (동작 변경 없음)
- `refactor`: 코드 리팩토링
- `test`: 테스트 코드 추가/수정
- `chore`: 빌드 작업, 패키지 매니저 설정 등

## Git Flow 브랜치 전략

```
main (또는 master)     - 배포 가능한 상태
develop                 - 다음 배포를 위한 개발 브랜치
feature/*               - 새로운 기능 개발
hotfix/*                - 긴급 버그 수정
release/*               - 배포 준비
```

- `타입 / 이슈번호 - 작업요약` 형태로 작성
  - ex : `feat/#12-swipe-card`, `fix/#45-login-error`

## Architecture

```jsx
📦 src
 ┣ 📂 components           // UI를 구성하는 모든 컴포넌트
 ┃ ┣ 📜 Header.jsx
 ┃ ┣ 📜 Button.jsx
 ┃ ┗ 📜 LoginForm.jsx
 ┣ 📂 hooks                // 프로젝트에서 사용하는 커스텀 훅 (재사용 로직)
 ┃ ┣ 📜 useInput.js
 ┃ ┗ 📜 useToggle.js
 ┣ 📂 tests                // 모든 테스트 코드
 ┣ 📜 App.js
 ┗ 📜 index.js
```
