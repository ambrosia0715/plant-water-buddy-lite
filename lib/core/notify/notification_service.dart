// lib/core/notify/notification_service.dart
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:timezone/data/latest_all.dart' as tz;
import 'package:timezone/timezone.dart' as tz;
import 'package:android_alarm_manager_plus/android_alarm_manager_plus.dart';
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

    // Android Alarm Manager 초기화 (Android만)
    try {
      await AndroidAlarmManager.initialize();
      print('✅ Android Alarm Manager 초기화 완료');
    } catch (e) {
      print('⚠️ Android Alarm Manager 초기화 실패 (iOS일 수 있음): $e');
    }

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
      importance: Importance.max,
      playSound: true,
      enableVibration: true,
      enableLights: true,
      showBadge: true,
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

  // 배터리 최적화 예외 요청 (Android)
  Future<void> requestBatteryOptimizationExemption() async {
    final androidImpl = _notifications
        .resolvePlatformSpecificImplementation<
            AndroidFlutterLocalNotificationsPlugin>();
    
    if (androidImpl != null) {
      // Android 시스템 설정으로 이동하여 배터리 최적화 해제
      // 사용자가 수동으로 설정해야 함
      print('배터리 최적화 예외 요청: 시스템 설정에서 수동 설정 필요');
      // Note: flutter_local_notifications는 직접 배터리 최적화 요청 API가 없음
      // 사용자에게 안내 메시지 표시 필요
    }
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
    final now = tz.TZDateTime.now(tz.local);
    if (scheduledTime.isBefore(now)) {
      print('⚠️ 알람 시간이 과거입니다: $scheduledTime (현재: $now)');
      return;
    }

    print('📅 알람 예약: ${plant.name} - $scheduledTime');
    print('   현재 시간: $now');
    print('   남은 시간: ${scheduledTime.difference(now)}');

    // Android Alarm Manager로 정확한 알람 설정 (Android에서만 작동)
    final alarmId = plant.id.hashCode;
    final milliseconds = scheduledTime.millisecondsSinceEpoch;
    
    try {
      await AndroidAlarmManager.oneShotAt(
        DateTime.fromMillisecondsSinceEpoch(milliseconds),
        alarmId,
        _fireNotification,
        exact: true,
        wakeup: true,
        rescheduleOnReboot: true,
        alarmClock: true, // 알람 시계 모드: Doze 모드 무시
        params: {
          'plantId': plant.id,
          'plantName': plant.name,
        },
      );
      print('✅ Android Alarm Manager로 알람 예약 완료');
    } catch (e) {
      print('⚠️ Android Alarm Manager 실패, 기본 방식 사용: $e');
    }

    // 백업으로 flutter_local_notifications도 사용
    const androidDetails = AndroidNotificationDetails(
      'water_ch',
      'Plant Water',
      channelDescription: '식물 물주기 알림',
      importance: Importance.max,
      priority: Priority.max,
      icon: '@mipmap/ic_launcher',
      playSound: true,
      enableVibration: true,
      enableLights: true,
      fullScreenIntent: true,
      category: AndroidNotificationCategory.alarm,
      visibility: NotificationVisibility.public,
      autoCancel: false,
      ongoing: false,
      channelShowBadge: true,
    );

    const iosDetails = DarwinNotificationDetails(
      presentAlert: true,
      presentBadge: true,
      presentSound: true,
      sound: 'default',
      badgeNumber: 1,
      interruptionLevel: InterruptionLevel.timeSensitive, // iOS 15+: 중요 알림
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
    
    print('✅ 알람 예약 완료: ${plant.name} (ID: ${plant.id.hashCode})');
  }

  // 즉시 테스트 알림 전송
  Future<void> showTestNotification() async {
    const androidDetails = AndroidNotificationDetails(
      'water_ch',
      'Plant Water',
      channelDescription: '식물 물주기 알림',
      importance: Importance.max,
      priority: Priority.max,
      icon: '@mipmap/ic_launcher',
      playSound: true,
      enableVibration: true,
      enableLights: true,
      fullScreenIntent: true,
      category: AndroidNotificationCategory.alarm,
      visibility: NotificationVisibility.public,
      autoCancel: false,
      ongoing: false,
      channelShowBadge: true,
    );

    const iosDetails = DarwinNotificationDetails(
      presentAlert: true,
      presentBadge: true,
      presentSound: true,
      sound: 'default',
      badgeNumber: 1,
      interruptionLevel: InterruptionLevel.timeSensitive,
    );

    const details = NotificationDetails(
      android: androidDetails,
      iOS: iosDetails,
    );

    await _notifications.show(
      999,
      '🌱 테스트 알림',
      '알림이 정상적으로 작동합니다!',
      details,
    );
    
    print('✅ 테스트 알림 전송 완료');
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

// Android Alarm Manager 콜백 함수 (top-level 함수여야 함)
@pragma('vm:entry-point')
void _fireNotification(int id, Map<String, dynamic> params) async {
  print('🔔 알람 콜백 실행: ID=$id');
  
  final plantName = params['plantName'] as String? ?? '식물';
  
  final notifications = FlutterLocalNotificationsPlugin();
  
  const androidDetails = AndroidNotificationDetails(
    'water_ch',
    'Plant Water',
    channelDescription: '식물 물주기 알림',
    importance: Importance.max,
    priority: Priority.max,
    icon: '@mipmap/ic_launcher',
    playSound: true,
    enableVibration: true,
    enableLights: true,
    fullScreenIntent: true,
    category: AndroidNotificationCategory.alarm,
    visibility: NotificationVisibility.public,
    autoCancel: false,
    ongoing: false,
    channelShowBadge: true,
  );

  const details = NotificationDetails(android: androidDetails);

  await notifications.show(
    id,
    '🌱 $plantName 물주기 시간이에요!',
    '오늘은 $plantName에게 물을 줄 날이에요.',
    details,
    payload: params['plantId'] as String?,
  );
  
  print('✅ 알람 알림 전송 완료');
}
