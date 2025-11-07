// lib/data/plant_repo.dart
import 'dart:convert';
import 'dart:io';
import 'package:hive/hive.dart';
import 'package:path_provider/path_provider.dart';
import 'package:share_plus/share_plus.dart';
import '../domain/plant.dart';

enum SortOption {
  nearestDue, // 가장 가까운 물주기 순
  mostOverdue, // 가장 밀린 순
  nameAsc, // 이름 오름차순
}

class PlantRepository {
  static const String _boxName = 'plants_box';
  Box<Plant>? _box;

  // Hive Box 열기
  Future<void> init() async {
    _box = await Hive.openBox<Plant>(_boxName);
  }

  Box<Plant> get _safeBox {
    if (_box == null) {
      // Box가 아직 열리지 않았다면 동기적으로 열기 시도
      try {
        _box = Hive.box<Plant>(_boxName);
      } catch (e) {
        throw Exception('PlantRepository not initialized. Call init() first.');
      }
    }
    if (!_box!.isOpen) {
      throw Exception('PlantRepository box is closed');
    }
    return _box!;
  }

  // 전체 식물 가져오기 (정렬 옵션)
  List<Plant> getAll({SortOption sort = SortOption.nearestDue}) {
    final plants = _safeBox.values.toList();

    switch (sort) {
      case SortOption.nearestDue:
        plants.sort((a, b) {
          if (!a.isActive && b.isActive) return 1;
          if (a.isActive && !b.isActive) return -1;
          return a.nextWaterDate.compareTo(b.nextWaterDate);
        });
        break;

      case SortOption.mostOverdue:
        plants.sort((a, b) {
          if (!a.isActive && b.isActive) return 1;
          if (a.isActive && !b.isActive) return -1;
          final aDays = a.daysUntilNextWater;
          final bDays = b.daysUntilNextWater;
          return aDays.compareTo(bDays);
        });
        break;

      case SortOption.nameAsc:
        plants.sort((a, b) {
          if (!a.isActive && b.isActive) return 1;
          if (a.isActive && !b.isActive) return -1;
          return a.name.compareTo(b.name);
        });
        break;
    }

    return plants;
  }

  // 오늘/밀린 식물만 가져오기
  List<Plant> getTodayAndOverdue() {
    final plants = _safeBox.values.where((p) {
      return p.isActive && (p.isDueToday || p.isOverdue);
    }).toList();

    // 밀린 순으로 정렬
    plants.sort((a, b) => a.daysUntilNextWater.compareTo(b.daysUntilNextWater));
    return plants;
  }

  // ID로 식물 가져오기
  Plant? getById(String id) {
    return _safeBox.get(id);
  }

  // 추가
  Future<void> add(Plant plant) async {
    await _safeBox.put(plant.id, plant);
  }

  // 업데이트
  Future<void> update(Plant plant) async {
    await _safeBox.put(plant.id, plant);
  }

  // 삭제
  Future<void> delete(String id) async {
    await _safeBox.delete(id);
  }

  // 전체 삭제
  Future<void> clear() async {
    await _safeBox.clear();
  }

  // JSON 내보내기
  Future<void> exportToJson() async {
    final plants = getAll();
    final jsonData = {
      'version': '1.0',
      'exportedAt': DateTime.now().toIso8601String(),
      'plants': plants.map((p) => p.toJson()).toList(),
    };

    final jsonString = const JsonEncoder.withIndent('  ').convert(jsonData);
    final tempDir = await getTemporaryDirectory();
    final file = File('${tempDir.path}/plant_water_buddy_backup.json');
    await file.writeAsString(jsonString);

    await Share.shareXFiles(
      [XFile(file.path)],
      subject: 'Plant Water Buddy 백업',
    );
  }

  // JSON 가져오기 (병합 규칙: 동일 ID면 최신 lastWateredAt 우선)
  Future<int> importFromJson(String jsonString) async {
    try {
      final data = jsonDecode(jsonString) as Map<String, dynamic>;
      final plantsList = data['plants'] as List<dynamic>;
      
      int importedCount = 0;
      
      for (final plantJson in plantsList) {
        final newPlant = Plant.fromJson(plantJson as Map<String, dynamic>);
        final existing = getById(newPlant.id);
        
        if (existing == null) {
          // 새 식물 추가
          await add(newPlant);
          importedCount++;
        } else {
          // 동일 ID: 더 최신 lastWateredAt 우선
          if (newPlant.lastWateredAt.isAfter(existing.lastWateredAt)) {
            await update(newPlant);
            importedCount++;
          }
        }
      }
      
      return importedCount;
    } catch (e) {
      throw Exception('JSON 파싱 실패: $e');
    }
  }

  // 이번 주 완료 개수 (지난 7일간 물 준 횟수)
  int getWeeklyCompletedCount() {
    final now = DateTime.now();
    final weekAgo = now.subtract(const Duration(days: 7));
    
    return _safeBox.values.where((p) {
      return p.lastWateredAt.isAfter(weekAgo);
    }).length;
  }

  // 이번 주 밀린 개수
  int getWeeklyOverdueCount() {
    return _safeBox.values.where((p) {
      return p.isActive && p.isOverdue;
    }).length;
  }

  // 데모 데이터 생성
  Future<void> seedDemo() async {
    final demos = [
      Plant(
        id: 'demo-1',
        name: '몬스테라',
        intervalDays: 7,
        lastWateredAt: DateTime.now().subtract(const Duration(days: 6)),
        notifyHour: 9,
        notifyMinute: 0,
      ),
      Plant(
        id: 'demo-2',
        name: '스킨답서스',
        intervalDays: 3,
        lastWateredAt: DateTime.now().subtract(const Duration(days: 4)),
        notifyHour: 9,
        notifyMinute: 0,
      ),
      Plant(
        id: 'demo-3',
        name: '산세베리아',
        intervalDays: 14,
        lastWateredAt: DateTime.now().subtract(const Duration(days: 10)),
        notifyHour: 9,
        notifyMinute: 0,
      ),
    ];

    for (final plant in demos) {
      await add(plant);
    }
  }
}
