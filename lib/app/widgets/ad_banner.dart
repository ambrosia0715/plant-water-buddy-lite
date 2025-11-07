// lib/app/widgets/ad_banner.dart
import 'dart:io' show Platform;
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter/material.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';
import '../../core/ads/ad_service.dart';

class AdBannerWidget extends StatefulWidget {
  const AdBannerWidget({super.key});

  @override
  State<AdBannerWidget> createState() => _AdBannerWidgetState();
}

class _AdBannerWidgetState extends State<AdBannerWidget> {
  BannerAd? _bannerAd;
  bool _isLoaded = false;

  @override
  void initState() {
    super.initState();
    // Android/iOS에서만 광고 로드
    if (!kIsWeb && (Platform.isAndroid || Platform.isIOS)) {
      _loadAd();
    }
  }

  void _loadAd() {
    _bannerAd = AdService().createBannerAd(
      size: AdSize.banner,
      onAdFailedToLoad: (ad, error) {
        ad.dispose();
        setState(() {
          _isLoaded = false;
        });
      },
    );

    _bannerAd!.load().then((_) {
      setState(() {
        _isLoaded = true;
      });
    });
  }

  @override
  void dispose() {
    _bannerAd?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (!_isLoaded || _bannerAd == null) {
      return const SizedBox.shrink();
    }

    return Container(
      alignment: Alignment.center,
      width: _bannerAd!.size.width.toDouble(),
      height: _bannerAd!.size.height.toDouble(),
      child: AdWidget(ad: _bannerAd!),
    );
  }
}
