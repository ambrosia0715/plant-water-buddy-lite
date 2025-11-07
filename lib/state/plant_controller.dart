// lib/state/plant_controller.dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:uuid/uuid.dart';
import '../domain/plant.dart';
import '../data/plant_repo.dart';
import '../core/notify/notification_service.dart';

// PlantRepository Provider
final plantRepositoryProvider = Provider<PlantRepository>((ref) {
  final repo = PlantRepository();
  // 초기화는 main에서 이미 완료됨
  return repo;
});

// NotificationService Provider
final notificationServiceProvider = Provider<NotificationService>((ref) {
  return NotificationService();
});

// PlantController Provider
final plantControllerProvider =
    StateNotifierProvider<PlantController, AsyncValue<List<Plant>>>((ref) {
  return PlantController(
    ref.read(plantRepositoryProvider),
    ref.read(notificationServiceProvider),
  );
});

class PlantController extends StateNotifier<AsyncValue<List<Plant>>> {
  PlantController(this._repo, this._notificationService)
      : super(const AsyncValue.loading()) {
    load();
  }

  final PlantRepository _repo;
  final NotificationService _notificationService;
  final _uuid = const Uuid();

  // 로드
  Future<void> load() async {
    state = const AsyncValue.loading();
    try {
      final plants = _repo.getAll();
      state = AsyncValue.data(plants);
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }

  // 추가
  Future<void> add(Plant plant) async {
    try {
      final newPlant = plant.copyWith(id: _uuid.v4());
      await _repo.add(newPlant);
      await _notificationService.scheduleFor(newPlant);
      await load();
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }

  // 업데이트
  Future<void> update(Plant plant) async {
    try {
      await _repo.update(plant);
      await _notificationService.scheduleFor(plant);
      await load();
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }

  // 삭제
  Future<void> delete(String id) async {
    try {
      final plant = _repo.getById(id);
      if (plant != null) {
        await _notificationService.cancelFor(plant);
      }
      await _repo.delete(id);
      await load();
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }

  // 활성화/비활성화 토글
  Future<void> toggleActive(String id) async {
    try {
      final plant = _repo.getById(id);
      if (plant != null) {
        final updated = plant.copyWith(isActive: !plant.isActive);
        await _repo.update(updated);
        await _notificationService.scheduleFor(updated);
        await load();
      }
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }

  // 오늘 물 줬어요 (완료 처리)
  Future<void> markWateredToday(String id) async {
    try {
      final plant = _repo.getById(id);
      if (plant != null) {
        final now = DateTime.now();
        final updated = plant.copyWith(lastWateredAt: now);
        await _repo.update(updated);
        // 다음 알림 재예약
        await _notificationService.scheduleFor(updated);
        await load();
      }
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }

  // 데모 데이터 생성
  Future<void> seedDemo() async {
    try {
      await _repo.seedDemo();
      final plants = _repo.getAll();
      await _notificationService.reconcileAll(plants);
      await load();
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }

  // 전체 알림 재조정
  Future<void> reconcileNotifications() async {
    try {
      final plants = _repo.getAll();
      await _notificationService.reconcileAll(plants);
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }

  // JSON 내보내기
  Future<void> exportJson() async {
    try {
      await _repo.exportToJson();
    } catch (e) {
      // 에러 처리
      rethrow;
    }
  }

  // JSON 가져오기
  Future<int> importJson(String jsonString) async {
    try {
      final count = await _repo.importFromJson(jsonString);
      final plants = _repo.getAll();
      await _notificationService.reconcileAll(plants);
      await load();
      return count;
    } catch (e) {
      rethrow;
    }
  }

  // 오늘/밀린 식물 가져오기
  List<Plant> getTodayAndOverdue() {
    return _repo.getTodayAndOverdue();
  }

  // 이번 주 통계
  Map<String, int> getWeeklyStats() {
    return {
      'completed': _repo.getWeeklyCompletedCount(),
      'overdue': _repo.getWeeklyOverdueCount(),
    };
  }
}
