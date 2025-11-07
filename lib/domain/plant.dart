// lib/domain/plant.dart
import 'package:hive/hive.dart';

part 'plant.g.dart';

@HiveType(typeId: 0)
class Plant {
  @HiveField(0)
  final String id;

  @HiveField(1)
  final String name;

  @HiveField(2)
  final String? imagePath;

  @HiveField(3)
  final int intervalDays;

  @HiveField(4)
  final DateTime lastWateredAt;

  @HiveField(5)
  final int notifyHour;

  @HiveField(6)
  final int notifyMinute;

  @HiveField(7)
  final bool isActive;

  Plant({
    required this.id,
    required this.name,
    this.imagePath,
    required this.intervalDays,
    required this.lastWateredAt,
    this.notifyHour = 9,
    this.notifyMinute = 0,
    this.isActive = true,
  });

  // 다음 물주기 날짜 계산 (00:00 기준)
  DateTime get nextWaterDate {
    final lastWateredDate = DateTime(
      lastWateredAt.year,
      lastWateredAt.month,
      lastWateredAt.day,
    );
    return lastWateredDate.add(Duration(days: intervalDays));
  }

  // 특정 날짜가 물주기 날짜인지 확인
  bool dueOn(DateTime date) {
    final checkDate = DateTime(date.year, date.month, date.day);
    final nextDate = DateTime(
      nextWaterDate.year,
      nextWaterDate.month,
      nextWaterDate.day,
    );
    return checkDate.isAtSameMomentAs(nextDate);
  }

  // 오늘이 물주기 날짜인지 확인
  bool get isDueToday {
    return dueOn(DateTime.now());
  }

  // 밀렸는지 확인
  bool get isOverdue {
    final today = DateTime.now();
    final todayDate = DateTime(today.year, today.month, today.day);
    final nextDate = DateTime(
      nextWaterDate.year,
      nextWaterDate.month,
      nextWaterDate.day,
    );
    return todayDate.isAfter(nextDate);
  }

  // D-day 계산 (음수면 밀린 일수)
  int get daysUntilNextWater {
    final today = DateTime.now();
    final todayDate = DateTime(today.year, today.month, today.day);
    final nextDate = DateTime(
      nextWaterDate.year,
      nextWaterDate.month,
      nextWaterDate.day,
    );
    return nextDate.difference(todayDate).inDays;
  }

  // 복사 메서드
  Plant copyWith({
    String? id,
    String? name,
    String? imagePath,
    int? intervalDays,
    DateTime? lastWateredAt,
    int? notifyHour,
    int? notifyMinute,
    bool? isActive,
  }) {
    return Plant(
      id: id ?? this.id,
      name: name ?? this.name,
      imagePath: imagePath ?? this.imagePath,
      intervalDays: intervalDays ?? this.intervalDays,
      lastWateredAt: lastWateredAt ?? this.lastWateredAt,
      notifyHour: notifyHour ?? this.notifyHour,
      notifyMinute: notifyMinute ?? this.notifyMinute,
      isActive: isActive ?? this.isActive,
    );
  }

  // JSON 변환
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'imagePath': imagePath,
      'intervalDays': intervalDays,
      'lastWateredAt': lastWateredAt.toIso8601String(),
      'notifyHour': notifyHour,
      'notifyMinute': notifyMinute,
      'isActive': isActive,
    };
  }

  factory Plant.fromJson(Map<String, dynamic> json) {
    return Plant(
      id: json['id'] as String,
      name: json['name'] as String,
      imagePath: json['imagePath'] as String?,
      intervalDays: json['intervalDays'] as int,
      lastWateredAt: DateTime.parse(json['lastWateredAt'] as String),
      notifyHour: json['notifyHour'] as int? ?? 9,
      notifyMinute: json['notifyMinute'] as int? ?? 0,
      isActive: json['isActive'] as bool? ?? true,
    );
  }
}
