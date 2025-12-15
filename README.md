# Plant Water Buddy - Lite

식물 물주기 알림 앱 - 가볍고 실용적인 식물 관리 도우미

## 📱 앱 소개

Plant Water Buddy - Lite는 식물별 물주기 주기를 관리하고, 정해진 날짜에 로컬 알림으로 알려주는 간편한 식물 관리 앱입니다.

### 주요 기능

- 🌱 **식물별 맞춤 관리**: 각 식물마다 다른 물주기 주기 설정
- ⏰ **스마트 알림**: 정해진 시간에 물주기 알림 전송
- 📊 **오늘 할 일**: 오늘/밀린 식물만 모아서 보기
- 💾 **로컬 저장**: 모든 데이터는 기기 내부에만 저장
- 📤 **백업/복원**: JSON 형식으로 데이터 내보내기/가져오기
- 🎨 **깔끔한 UI**: 라이트 테마 지원

## ⚠️ 알람이 안 울릴 때 (Android)

알람이 정확한 시간에 울리지 않는다면 다음 설정을 확인하세요:

### 1. 배터리 최적화 해제
- **설정 > 앱 > 물주기 알림_lite > 배터리**
- **제한 없음** 선택
- **백그라운드 사용 허용**

### 2. 제조사별 추가 설정

#### 삼성 (Samsung)
- 설정 > 배터리 및 디바이스 케어 > 배터리
- 백그라운드 사용 제한 > 제한 없음에 앱 추가
- 절전 모드에서 앱 제외

#### 샤오미 (Xiaomi)
- 설정 > 앱 > 권한 관리 > 자동 시작 > 허용
- 설정 > 배터리 및 성능 > 앱 배터리 세이버 > 제한 없음

#### 화웨이 (Huawei)
- 설정 > 배터리 > 앱 실행 > 수동 관리
- 자동 실행, 보조 실행, 백그라운드 실행 모두 허용

#### OPPO / Realme
- 설정 > 배터리 > 백그라운드 절전 > 앱 제외
- 설정 > 앱 관리 > 자동 시작 관리 > 허용

### 3. 앱 내 설정
- **설정 > 알림 권한 요청** 탭
- **설정 > 배터리 최적화 해제** 안내 확인
- **설정 > 예약된 알림 확인**으로 알람 등록 여부 확인

## 🚀 시작하기

### 필수 요구사항

- Flutter SDK 3.1.0 이상
- Dart 3.1.0 이상
- Android Studio / Xcode (플랫폼별)

### 설치 및 실행

1. **의존성 설치**
```bash
flutter pub get
```

2. **Hive 어댑터 생성**
```bash
dart run build_runner build --delete-conflicting-outputs
```

3. **디버그 실행**
```bash
flutter run
```

4. **릴리스 빌드**

Android:
```bash
flutter build appbundle
```

iOS:
```bash
flutter build ipa
```

## 📁 프로젝트 구조

```
lib/
├── main.dart                           # 앱 진입점
├── core/                               # 핵심 서비스
│   ├── ads/
│   │   └── ad_service.dart            # 광고 관리
│   ├── notify/
│   │   └── notification_service.dart  # 알림 관리
│   └── utils/
│       └── date_formats.dart          # 날짜 포맷팅
├── data/
│   └── plant_repo.dart                # 데이터 저장소
├── domain/
│   └── plant.dart                     # 식물 모델
├── state/
│   └── plant_controller.dart          # 상태 관리 (Riverpod)
└── app/
    ├── home_page.dart                 # 홈 화면
    ├── plant_form_page.dart           # 식물 추가/수정
    ├── all_plants_page.dart           # 전체 식물 목록
    ├── settings_page.dart             # 설정
    └── widgets/
        ├── ad_banner.dart             # 배너 광고
        ├── interstitial_guard.dart    # 전면 광고 가드
        └── plant_card.dart            # 식물 카드
```

## 🔧 기술 스택

### 상태 관리
- **flutter_riverpod** ^2.5.1

### 로컬 저장
- **hive** ^2.2.3
- **hive_flutter** ^1.1.0

### 알림
- **flutter_local_notifications** ^17.2.1
- **timezone** ^0.9.2

### 광고
- **google_mobile_ads** ^5.1.0

### 기타
- **intl** ^0.20.2 (다국어/날짜 포맷)
- **image_picker** ^1.1.2 (사진 선택)
- **share_plus** ^10.0.2 (공유 기능)

## 📋 주요 설정

### Android 설정

`android/app/src/main/AndroidManifest.xml`:
- 인터넷 권한 (광고용)
- 알림 권한 (Android 13+)
- AdMob App ID: ca-app-pub-1444459980078427~7755592316

`android/app/build.gradle.kts`:
- minSdk: 21
- targetSdk: 최신
- multiDexEnabled: true

### iOS 설정

`ios/Runner/Info.plist`:
- GADApplicationIdentifier: ca-app-pub-1444459980078427~3620357446
- NSUserNotificationUsageDescription (알림 권한 설명)
- NSPhotoLibraryUsageDescription (사진 라이브러리 접근)

## 💡 사용 가이드

### 1. 첫 실행
- 알림 권한 요청에 동의
- "데모 데이터로 시작하기" 또는 직접 식물 추가

### 2. 식물 추가
- 하단 FAB 버튼 클릭
- 식물 이름, 사진, 물주기 주기 입력
- 마지막 물 준 날짜 및 알림 시간 설정

### 3. 물주기 완료
- 홈 화면에서 "물 줬어요" 버튼 클릭
- 자동으로 다음 알림 재예약

### 4. 데이터 백업
- 설정 > 데이터 내보내기
- JSON 파일로 공유 또는 저장

### 5. 데이터 복원
- 설정 > 데이터 가져오기
- JSON 텍스트 붙여넣기

## 🎯 광고 정책

### 배너 광고
- 홈 화면 하단 고정
- Adaptive Banner 사용
- Android 광고단위: ca-app-pub-1444459980078427/6451083653
- iOS 광고단위: ca-app-pub-1444459980078427/7676535416

### 전면 광고 (인터스티셜)
- 상세 진입 시 25% 확률로 표시
- 60~90초 쿨다운 적용
- 다음 경우 표시 금지:
  - 앱 실행 직후 3초
  - 알림 클릭 후 3초
  - 마지막 광고 노출 후 쿨다운 시간 내

## 🔐 개인정보 처리

- 모든 데이터는 **로컬 기기에만 저장**
- 외부 서버로 전송되지 않음
- 광고는 Google AdMob 정책 준수
- 앱 삭제 시 모든 데이터 함께 삭제

## ✅ QA 체크리스트

- [ ] 첫 실행 시 알림 권한 요청 정상 작동
- [ ] 식물 추가/수정/삭제 기능 정상
- [ ] D-day 계산 정확성
- [ ] "물 줬어요" 클릭 시 lastWateredAt 갱신 및 알림 재예약
- [ ] 시간대 변경 후 알림 재조정 동작
- [ ] 인터스티셜 광고 쿨다운 및 가드 동작
- [ ] JSON 내보내기/가져오기 (병합 규칙 확인)
- [ ] 라이트/다크 테마 전환

## 📝 다음으로 할 일 (To-Do)

### 릴리스 전 필수 작업

1. **AdMob 설정 검증**
   - [x] Android AdMob ID 적용 완료
   - [x] iOS AdMob ID 적용 완료
   - [ ] 실기기에서 광고 노출 확인
   - [ ] 릴리스 빌드 시 테스트 모드 비활성화 (`--dart-define=DEBUG_MODE=false`)

2. **플랫폼 설정**
   - [x] Android: 고유한 applicationId 설정 (완료: com.ambrosia.plantwaterbuddy)
   - [ ] iOS: Bundle Identifier 설정
   - [ ] 앱 아이콘 제작 및 적용 (1024x1024)
   - [ ] 스플래시 스크린 커스터마이징

3. **스토어 준비**
   - [ ] 스크린샷 4장 촬영:
     - 홈 화면 (오늘 할 일)
     - 식물 추가 화면
     - 완료 처리 화면
     - 전체 식물 목록
   - [ ] 앱 설명 작성 (한국어/영어)
   - [ ] 개인정보 처리방침 웹페이지 생성
   - [ ] 프로모션 이미지 제작

4. **실기기 테스트**
   - [ ] Android 다양한 버전 테스트 (API 21, 28, 33+)
   - [ ] iOS 다양한 버전 테스트 (iOS 13+)
   - [ ] 알림 정확성 장기 테스트 (최소 3일)
   - [ ] 광고 노출 빈도 및 UX 검증
   - [ ] 메모리 누수 확인
   - [ ] 배터리 소모 테스트

5. **코드 정리**
   - [ ] 불필요한 주석 제거
   - [ ] TODO 주석 처리
   - [ ] console.log/print 제거 (release 빌드)
   - [ ] 미사용 import 정리

6. **법적 준비**
   - [ ] Google Play Console 개발자 계정 준비
   - [ ] Apple Developer 계정 준비
   - [ ] 콘텐츠 등급 분류 (한국: 전체이용가)
   - [ ] 개인정보 처리방침 게시

### 향후 개선 사항 (선택)

- [ ] 홈 위젯 구현 (home_widget 활용)
- [ ] 식물별 메모/일지 기능
- [ ] 물주기 히스토리 그래프
- [ ] 식물 카테고리/태그
- [ ] 클라우드 백업 옵션 (Firebase)
- [ ] 다양한 알림 사운드
- [ ] 식물 정보 온라인 검색 (API 연동)
- [ ] 다국어 지원 확대 (영어, 일본어, 중국어)

## 🐛 알려진 이슈

현재 알려진 이슈 없음

## ⚠️ iOS 알림 주의사항

### iOS에서 알림이 안 울리는 경우

1. **집중 모드 / 수면 모드 확인**
   - 설정 > 집중 모드 > 수면/방해금지 모드 OFF
   - 또는 해당 앱을 예외 앱으로 추가

2. **알림 권한 확인**
   - 설정 > 알림 > 물주기 알림_lite
   - "알림 허용" ON
   - "시간 제한 알림" 또는 "심각한 알림" 활성화

3. **저전력 모드**
   - iOS 저전력 모드에서는 백그라운드 작업이 제한됨
   - 중요한 알림은 정상 작동하지만 약간 지연될 수 있음

4. **배경 앱 새로고침**
   - 설정 > 일반 > 배경 앱 새로고침 ON
   - 앱별 설정에서 "물주기 알림_lite" ON

5. **iOS 제한사항**
   - iOS는 앱이 완전히 종료되면 로컬 알림에만 의존
   - Android보다 알림 신뢰성이 약간 낮을 수 있음
   - iOS 15+ "Time Sensitive Notifications" 적용됨

### 테스트 방법
1. 설정 > 테스트 알림 보내기 (즉시 알림)
2. 식물 추가 > 2-3분 후 알람 설정
3. 앱 백그라운드로 이동 (홈 버튼)
4. 알람 시간까지 대기

**권장**: iOS 사용자는 앱을 완전히 종료하지 말고 백그라운드에 두는 것이 좋습니다.

## 📄 라이선스

이 프로젝트는 개인 사용 목적으로 제작되었습니다.

## 🙏 오픈소스 라이선스

사용된 주요 패키지:
- Flutter & Dart - BSD License
- Riverpod - MIT License
- Hive - Apache License 2.0
- Google Mobile Ads - Google License
- Flutter Local Notifications - BSD License

---

**문의**: 앱 스토어 리뷰를 통해 문의해주세요.

**버전**: 1.0.0  
**최종 업데이트**: 2025년 11월 8일
