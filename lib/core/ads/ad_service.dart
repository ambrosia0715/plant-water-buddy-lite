// lib/core/ads/ad_service.dart
import 'dart:io';
import 'dart:math';
import 'package:flutter/foundation.dart' show kDebugMode;
import 'package:google_mobile_ads/google_mobile_ads.dart';

class AdService {
  static final AdService _instance = AdService._internal();
  factory AdService() => _instance;
  AdService._internal();

  // AdMob ID
  static const String _androidBannerId =
      'ca-app-pub-1444459980078427/2915794524';
  static const String _iosBannerId = 'ca-app-pub-1444459980078427/6021481775';
  static const String _androidInterstitialId =
      'ca-app-pub-1444459980078427/2915794524';
  static const String _iosInterstitialId =
      'ca-app-pub-1444459980078427/6021481775';

  // 배너 광고 ID
  static String get bannerAdUnitId {
    // 테스트 모드에서는 테스트 ID 사용
    if (_isTestMode) {
      return Platform.isAndroid
          ? 'ca-app-pub-3940256099942544/6300978111'
          : 'ca-app-pub-3940256099942544/2934735716';
    }
    return Platform.isAndroid ? _androidBannerId : _iosBannerId;
  }

  // 인터스티셜 광고 ID
  static String get interstitialAdUnitId {
    // 테스트 모드에서는 테스트 ID 사용
    if (_isTestMode) {
      return Platform.isAndroid
          ? 'ca-app-pub-3940256099942544/1033173712'
          : 'ca-app-pub-3940256099942544/4411468910';
    }
    return Platform.isAndroid ? _androidInterstitialId : _iosInterstitialId;
  }

  // 디버그 모드일 때만 테스트 광고 사용
  // 릴리스 빌드에서는 항상 실제 광고 사용
  static bool get _isTestMode => kDebugMode;

  // 인터스티셜 상태
  InterstitialAd? _interstitialAd;
  bool _isInterstitialReady = false;
  DateTime? _lastInterstitialShown;

  // 쿨다운 시간 (초)
  final int _minCooldownSeconds = 60;
  final int _maxCooldownSeconds = 90;

  // 가드 플래그 (로딩 직후/첫 실행/알림 클릭 직후)
  bool _isAppJustLaunched = true;
  bool _isFromNotification = false;

  // 초기화
  Future<void> init() async {
    // Google Play 가족 정책 준수를 위한 광고 설정
    // 가족 친화 콘텐츠만 표시하도록 설정
    final requestConfiguration = RequestConfiguration(
      // G 등급만 허용 (가족 친화)
      maxAdContentRating: MaxAdContentRating.g,
      // 아동 대상 콘텐츠로 태그
      tagForChildDirectedTreatment: TagForChildDirectedTreatment.yes,
      // 미성년자 동의 태그
      tagForUnderAgeOfConsent: TagForUnderAgeOfConsent.yes,
    );
    MobileAds.instance.updateRequestConfiguration(requestConfiguration);
    
    await MobileAds.instance.initialize();
    _loadInterstitial();
  }

  // 앱 실행 가드 해제 (일정 시간 후)
  void clearLaunchGuard() {
    Future.delayed(const Duration(seconds: 3), () {
      _isAppJustLaunched = false;
    });
  }

  // 알림 클릭 가드 설정
  void setFromNotification(bool value) {
    _isFromNotification = value;
    if (value) {
      // 알림 클릭 후 3초간 인터스티셜 금지
      Future.delayed(const Duration(seconds: 3), () {
        _isFromNotification = false;
      });
    }
  }

  // 배너 광고 생성
  BannerAd createBannerAd({
    required AdSize size,
    required void Function(Ad, LoadAdError) onAdFailedToLoad,
  }) {
    return BannerAd(
      adUnitId: bannerAdUnitId,
      size: size,
      request: const AdRequest(),
      listener: BannerAdListener(
        onAdLoaded: (ad) {},
        onAdFailedToLoad: onAdFailedToLoad,
      ),
    );
  }

  // 인터스티셜 로드
  void _loadInterstitial() {
    InterstitialAd.load(
      adUnitId: interstitialAdUnitId,
      request: const AdRequest(),
      adLoadCallback: InterstitialAdLoadCallback(
        onAdLoaded: (ad) {
          _interstitialAd = ad;
          _isInterstitialReady = true;

          ad.fullScreenContentCallback = FullScreenContentCallback(
            onAdDismissedFullScreenContent: (ad) {
              ad.dispose();
              _isInterstitialReady = false;
              _lastInterstitialShown = DateTime.now();
              _loadInterstitial();
            },
            onAdFailedToShowFullScreenContent: (ad, error) {
              ad.dispose();
              _isInterstitialReady = false;
              _loadInterstitial();
            },
          );
        },
        onAdFailedToLoad: (error) {
          _isInterstitialReady = false;
          // 재시도
          Future.delayed(const Duration(seconds: 30), _loadInterstitial);
        },
      ),
    );
  }

  // 인터스티셜 표시 시도 (25% 확률 + 쿨다운 + 가드)
  Future<bool> maybeShowInterstitial() async {
    // 가드 체크
    if (_isAppJustLaunched || _isFromNotification) {
      return false;
    }

    // 광고 준비 확인
    if (!_isInterstitialReady || _interstitialAd == null) {
      return false;
    }

    // 쿨다운 체크
    if (_lastInterstitialShown != null) {
      final cooldown =
          Random().nextInt(_maxCooldownSeconds - _minCooldownSeconds + 1) +
              _minCooldownSeconds;
      final elapsed =
          DateTime.now().difference(_lastInterstitialShown!).inSeconds;
      if (elapsed < cooldown) {
        return false;
      }
    }

    // 25% 확률
    if (Random().nextInt(100) >= 25) {
      return false;
    }

    // 광고 표시
    await _interstitialAd!.show();
    return true;
  }

  // 리소스 해제
  void dispose() {
    _interstitialAd?.dispose();
  }
}
