// lib/core/notify/notification_service.dart
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:timezone/data/latest_all.dart' as tz;
import 'package:timezone/timezone.dart' as tz;
import '../../domain/plant.dart';

class NotificationService {
  static final NotificationService _instance = NotificationService._internal();
  factory NotificationService() => _instance;
  NotificationService._internal();

  final FlutterLocalNotificationsPlugin _notifications =
      FlutterLocalNotificationsPlugin();

  bool _initialized = false;

  // 초기화
  Future<void> init() async {
    if (_initialized) return;

    // 타임존 초기화
    tz.initializeTimeZones();
    tz.setLocalLocation(tz.getLocation('Asia/Seoul'));

    // Android 설정
    const androidSettings = AndroidInitializationSettings('@mipmap/ic_launcher');

    // iOS 설정
    const iosSettings = DarwinInitializationSettings(
      requestAlertPermission: true,
      requestBadgePermission: true,
      requestSoundPermission: true,
    );

    // macOS 설정
    const macOSSettings = DarwinInitializationSettings(
      requestAlertPermission: true,
      requestBadgePermission: true,
      requestSoundPermission: true,
    );

    const initSettings = InitializationSettings(
      android: androidSettings,
      iOS: iosSettings,
      macOS: macOSSettings,
    );

    await _notifications.initialize(
      initSettings,
      onDidReceiveNotificationResponse: _onNotificationTapped,
    );

    // Android 알림 채널 생성
    const androidChannel = AndroidNotificationChannel(
      'water_ch',
      'Plant Water',
      description: '식물 물주기 알림',
      importance: Importance.high,
      playSound: true,
      enableVibration: true,
    );

    await _notifications
        .resolvePlatformSpecificImplementation<
            AndroidFlutterLocalNotificationsPlugin>()
        ?.createNotificationChannel(androidChannel);

    _initialized = true;
  }

  // 알림 클릭 핸들러
  void _onNotificationTapped(NotificationResponse response) {
    final payload = response.payload;
    if (payload != null) {
      // TODO: 해당 식물 상세로 이동 (main.dart에서 처리)
      // 예: Navigator로 plantId를 받아서 상세 페이지로 이동
    }
  }

  // 권한 요청 (iOS + Android)
  Future<bool> requestPermission() async {
    // iOS 권한 요청
    final iosResult = await _notifications
        .resolvePlatformSpecificImplementation<
            IOSFlutterLocalNotificationsPlugin>()
        ?.requestPermissions(
          alert: true,
          badge: true,
          sound: true,
        );

    // Android 구현체 가져오기
    final androidImpl = _notifications
        .resolvePlatformSpecificImplementation<
            AndroidFlutterLocalNotificationsPlugin>();
    
    if (androidImpl != null) {
      // Android 13+ 알림 권한 요청
      await androidImpl.requestNotificationsPermission();
      
      // Android 12+ (API 31+) Exact Alarm 권한 요청
      final exactAlarmPermission = await androidImpl.requestExactAlarmsPermission();
      print('Exact alarm permission: $exactAlarmPermission');
    }

    return iosResult ?? true;
  }

  // 특정 식물 알림 예약
  Future<void> scheduleFor(Plant plant) async {
    if (!plant.isActive) {
      await cancelFor(plant);
      return;
    }

    final nextWaterDate = plant.nextWaterDate;
    final scheduledTime = tz.TZDateTime(
      tz.local,
      nextWaterDate.year,
      nextWaterDate.month,
      nextWaterDate.day,
      plant.notifyHour,
      plant.notifyMinute,
    );

    // 과거 시간이면 예약하지 않음
    if (scheduledTime.isBefore(tz.TZDateTime.now(tz.local))) {
      return;
    }

    const androidDetails = AndroidNotificationDetails(
      'water_ch',
      'Plant Water',
      channelDescription: '식물 물주기 알림',
      importance: Importance.high,
      priority: Priority.high,
      icon: '@mipmap/ic_launcher',
    );

    const iosDetails = DarwinNotificationDetails(
      presentAlert: true,
      presentBadge: true,
      presentSound: true,
    );

    const details = NotificationDetails(
      android: androidDetails,
      iOS: iosDetails,
    );

    await _notifications.zonedSchedule(
      plant.id.hashCode,
      '🌱 ${plant.name} 물주기 시간이에요!',
      '오늘은 ${plant.name}에게 물을 줄 날이에요.',
      scheduledTime,
      details,
      androidScheduleMode: AndroidScheduleMode.exactAllowWhileIdle,
      uiLocalNotificationDateInterpretation:
          UILocalNotificationDateInterpretation.absoluteTime,
      payload: plant.id,
    );
  }

  // 특정 식물 알림 취소
  Future<void> cancelFor(Plant plant) async {
    await _notifications.cancel(plant.id.hashCode);
  }

  // 전체 알림 재조정 (과거 예약 취소 + 누락 예약 보완)
  Future<void> reconcileAll(List<Plant> plants) async {
    // 기존 알림 전체 취소
    await _notifications.cancelAll();

    // 활성 식물들만 다시 예약
    for (final plant in plants) {
      if (plant.isActive) {
        await scheduleFor(plant);
      }
    }
  }

  // 전체 알림 취소
  Future<void> cancelAll() async {
    await _notifications.cancelAll();
  }

  // 대기 중인 알림 목록
  Future<List<PendingNotificationRequest>> getPendingNotifications() async {
    return await _notifications.pendingNotificationRequests();
  }
}
