# Plant Water Buddy - Lite 프로젝트 완료 보고서

## ✅ 구현 완료 항목

### 1. 프로젝트 초기 설정
- ✅ Flutter 프로젝트 생성 (plant_water_buddy_lite)
- ✅ pubspec.yaml 의존성 설정 (Riverpod, Hive, AdMob, 알림 등)
- ✅ analysis_options.yaml 린트 규칙 적용
- ✅ Hive 어댑터 코드 생성 완료

### 2. 도메인 및 데이터 레이어
- ✅ `lib/domain/plant.dart` - Plant 모델 (Hive 타입 어댑터 포함)
  - id, name, imagePath, intervalDays, lastWateredAt, notifyHour/Minute, isActive
  - 계산 프로퍼티: nextWaterDate, dueOn(), isDueToday, isOverdue, daysUntilNextWater
  - JSON 변환 메서드

- ✅ `lib/data/plant_repo.dart` - PlantRepository
  - CRUD 기능
  - 정렬 옵션 (nearestDue, mostOverdue, nameAsc)
  - getTodayAndOverdue()
  - JSON 내보내기/가져오기 (병합 규칙 적용)
  - 주간 통계 (완료/밀림)
  - seedDemo() 데모 데이터

### 3. 코어 서비스
- ✅ `lib/core/notify/notification_service.dart` - 알림 서비스
  - timezone 초기화 (Asia/Seoul)
  - 권한 요청 (iOS/Android)
  - scheduleFor() - 다음 1회 알림 예약
  - cancelFor(), reconcileAll()
  - 알림 클릭 payload 처리

- ✅ `lib/core/ads/ad_service.dart` - 광고 서비스
  - 배너: Adaptive Banner
  - 인터스티셜: 25% 확률 + 60~90초 쿨다운
  - 가드: 로딩 직후/첫 실행/알림 클릭 직후 금지
  - 실제 AdMob ID 적용 (Android/iOS)

- ✅ `lib/core/utils/date_formats.dart` - 날짜 유틸리티
  - formatWithWeekday() - yyyy.MM.dd (E)
  - getDDayText() - D-day/+밀림 표기
  - getRelativeTimeText()

### 4. 상태 관리
- ✅ `lib/state/plant_controller.dart` - Riverpod StateNotifier
  - load(), add(), update(), delete()
  - toggleActive(), markWateredToday()
  - seedDemo(), reconcileNotifications()
  - exportJson(), importJson()

### 5. UI 레이어
- ✅ `lib/app/home_page.dart` - 홈 화면
  - 이번 주 통계 배지
  - 오늘/밀린 식물 리스트
  - "물 줬어요" 버튼
  - 하단 광고 배너
  - Empty 상태 처리

- ✅ `lib/app/plant_form_page.dart` - 식물 추가/수정
  - 이미지 선택 (image_picker)
  - 주기 프리셋 (3/7/10/14/30일) + 직접 입력
  - 마지막 물 준 날짜 선택
  - 알림 시간 설정
  - 활성화 스위치
  - 삭제 기능 (수정 모드)

- ✅ `lib/app/all_plants_page.dart` - 전체 식물 목록
  - 정렬 세그먼트 (가까운 순/밀린 순/이름순)
  - 전체 리스트 (편집 가능)

- ✅ `lib/app/settings_page.dart` - 설정
  - 알림 권한 요청
  - 알림 재설정
  - JSON 내보내기/가져오기
  - 앱 정보
  - 개인정보 처리방침
  - 오픈소스 라이선스
  - 데모 데이터 추가

- ✅ `lib/app/widgets/plant_card.dart` - 식물 카드
  - 아바타 (사진/이니셜)
  - D-day 뱃지
  - "물 줬어요" 버튼

- ✅ `lib/app/widgets/ad_banner.dart` - 배너 광고 위젯
- ✅ `lib/app/widgets/interstitial_guard.dart` - 전면 광고 가드

### 6. 플랫폼 설정
- ✅ `android/app/src/main/AndroidManifest.xml`
  - 인터넷, 알림, Wake Lock 권한
  - AdMob App ID: ca-app-pub-1444459980078427~7755592316

- ✅ `android/app/build.gradle.kts`
  - minSdk: 21
  - multiDexEnabled: true

- ✅ `ios/Runner/Info.plist`
  - GADApplicationIdentifier: ca-app-pub-1444459980078427~3620357446
  - 알림/사진 권한 설명

### 7. 앱 초기화
- ✅ `lib/main.dart`
  - Hive 초기화 및 어댑터 등록
  - 로케일 초기화 (ko_KR)
  - NotificationService 초기화
  - GoogleMobileAds 초기화
  - ProviderScope 설정
  - 라이트/다크 테마 구성

## 📊 프로젝트 통계

### 파일 구조
```
lib/
├── main.dart (1)
├── core/ (3)
│   ├── ads/ad_service.dart
│   ├── notify/notification_service.dart
│   └── utils/date_formats.dart
├── data/ (1)
│   └── plant_repo.dart
├── domain/ (2)
│   ├── plant.dart
│   └── plant.g.dart (생성됨)
├── state/ (1)
│   └── plant_controller.dart
└── app/ (8)
    ├── home_page.dart
    ├── plant_form_page.dart
    ├── all_plants_page.dart
    ├── settings_page.dart
    └── widgets/
        ├── ad_banner.dart
        ├── interstitial_guard.dart
        └── plant_card.dart

총 파일: 15개 (생성된 파일 제외)
```

### 주요 기능 수
- 화면: 4개 (홈, 폼, 전체, 설정)
- 재사용 위젯: 3개
- 서비스: 3개 (알림, 광고, 날짜)
- 모델: 1개 (Plant)
- Provider: 3개

### 코드 라인 (추정)
- Domain/Data: ~400 줄
- Core Services: ~450 줄
- State Management: ~160 줄
- UI: ~1,000 줄
- 총 ~2,000 줄

## 🎯 AdMob 설정 (실제 ID 적용 완료)

### Android
- App ID: `ca-app-pub-1444459980078427~7755592316`
- 광고단위 ID: `ca-app-pub-1444459980078427/6451083653`

### iOS
- App ID: `ca-app-pub-1444459980078427~3620357446`
- 광고단위 ID: `ca-app-pub-1444459980078427/7676535416`

## 🔄 다음 단계

### 즉시 가능
1. ✅ `flutter run` - 디버그 실행
2. ✅ 데모 데이터로 기능 테스트
3. ✅ 알림 스케줄링 확인

### 릴리스 전 필수
1. ✅ 고유 applicationId 설정 (완료: com.ambrosia.plantwaterbuddy)
2. ⏳ 앱 아이콘 제작 (1024x1024)
3. ⏳ 스크린샷 촬영 (4장)
4. ⏳ 개인정보 처리방침 웹페이지 생성
5. ⏳ 릴리스 빌드 테스트 (`--dart-define=DEBUG_MODE=false`)

### 스토어 등록
1. ⏳ Google Play Console 계정 준비
2. ⏳ Apple Developer 계정 준비
3. ⏳ 스토어 등록 정보 작성
4. ⏳ 콘텐츠 등급 획득

## 📱 테스트 시나리오

### 기본 기능
- [x] 앱 실행 및 권한 요청
- [ ] 식물 추가 (사진 선택 포함)
- [ ] 물주기 주기 설정 (프리셋/직접입력)
- [ ] "물 줬어요" 완료 처리
- [ ] 다음 알림 자동 예약 확인
- [ ] 식물 수정/삭제

### 알림
- [ ] 정확한 시간에 알림 도착
- [ ] 알림 클릭 시 앱 진입
- [ ] 알림 권한 거부 시 동작
- [ ] 시간대 변경 후 재조정

### 광고
- [ ] 홈 화면 배너 표시
- [ ] 인터스티셜 25% 확률 확인
- [ ] 쿨다운 동작 확인
- [ ] 첫 실행 시 미노출 확인

### 데이터
- [ ] JSON 내보내기
- [ ] JSON 가져오기 (병합)
- [ ] 앱 재시작 후 데이터 유지
- [ ] 데모 데이터 생성

## 🐛 알려진 제한사항

1. **테스트 모드 기본값**: 현재 `DEBUG_MODE=true`가 기본값
   - 릴리스 빌드 시 `--dart-define=DEBUG_MODE=false` 필요

2. **플랫폼 감지**: ad_service.dart에서 Platform.isAndroid 사용
   - 정상 동작하지만 웹 빌드 시 에러 가능성

3. **파일 선택**: settings_page.dart에서 단순 텍스트 입력
   - file_picker 패키지 미사용 (의존성 줄이기 위해)

## 📝 스토어 등록 문구 (초안)

### 앱 이름
**한글**: 식물 물주기 알림 - Lite  
**영문**: Plant Water Buddy - Lite

### 한 줄 소개
식물마다 주기를 설정하면, 날짜에 맞춰 딱 알려줘요.

### 상세 설명
```
🌱 식물 물주기, 이제 잊지 마세요!

Plant Water Buddy - Lite는 각 식물에 맞는 물주기 주기를 설정하고,
정확한 시간에 알림으로 알려주는 간편한 식물 관리 앱입니다.

주요 기능:
✓ 식물별 맞춤 물주기 주기 설정
✓ 정시 알림으로 물주기 시간 알림
✓ 오늘 할 일 화면에서 한눈에 확인
✓ 밀린 식물 자동 감지
✓ 데이터 백업/복원 기능
✓ 라이트/다크 테마 지원

특징:
• 모든 데이터는 기기 내부에만 저장
• 간단하고 직관적인 인터페이스
• 가벼운 용량, 빠른 속도
• 광고 최소화 (배너만 기본 표시)

지금 바로 시작하세요!
```

### 키워드
식물, 물주기, 알림, 관리, 키우기, 화분, 반려식물, 가드닝

## ✅ 최종 체크리스트

### 코드
- [x] 모든 필수 파일 생성
- [x] Hive 어댑터 빌드 완료
- [x] 컴파일 에러 0개
- [x] 주요 lint 규칙 적용
- [x] AdMob ID 실제 값 적용

### 문서
- [x] README.md 작성
- [x] 주석 추가
- [x] To-Do 리스트 작성

### 플랫폼
- [x] Android 설정 완료
- [x] iOS 설정 완료
- [x] 권한 설명 추가

---

**프로젝트 생성일**: 2025년 11월 8일  
**상태**: ✅ 구현 완료 (테스트 단계)  
**다음**: 실기기 테스트 및 릴리스 준비
