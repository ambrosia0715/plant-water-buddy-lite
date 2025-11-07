// lib/app/widgets/interstitial_guard.dart
import '../../core/ads/ad_service.dart';

class InterstitialGuard {
  static final InterstitialGuard _instance = InterstitialGuard._internal();
  factory InterstitialGuard() => _instance;
  InterstitialGuard._internal();

  final _adService = AdService();

  // 상세 진입 시 인터스티셜 시도
  Future<void> maybeShowOnEnter(String contextKey) async {
    await _adService.maybeShowInterstitial();
  }
}
