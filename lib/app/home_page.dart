// lib/app/home_page.dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../state/plant_controller.dart';
import 'widgets/plant_card.dart';
import 'widgets/ad_banner.dart';
import 'plant_form_page.dart';
import 'all_plants_page.dart';
import 'settings_page.dart';

class HomePage extends ConsumerWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final plantsAsync = ref.watch(plantControllerProvider);
    final controller = ref.read(plantControllerProvider.notifier);

    return Scaffold(
      appBar: AppBar(
        title: const Text('🌱 오늘 할 일'),
        backgroundColor: Colors.green,
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: const Icon(Icons.list),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const AllPlantsPage()),
              );
            },
          ),
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const SettingsPage()),
              );
            },
          ),
        ],
      ),
      body: Column(
        children: [
          // 이번 주 통계 배지
          _buildWeeklyStats(controller),
          
          // 식물 리스트
          Expanded(
            child: plantsAsync.when(
              data: (plants) {
                final todayPlants = controller.getTodayAndOverdue();
                
                if (todayPlants.isEmpty) {
                  return _buildEmptyState(context, controller);
                }
                
                return ListView.builder(
                  itemCount: todayPlants.length,
                  itemBuilder: (context, index) {
                    final plant = todayPlants[index];
                    return PlantCard(
                      plant: plant,
                      onWatered: () async {
                        await controller.markWateredToday(plant.id);
                        if (context.mounted) {
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(
                              content: Text('${plant.name}에 물을 줬어요! 💧'),
                              backgroundColor: Colors.green,
                            ),
                          );
                        }
                      },
                      onTap: () {
                        // 상세 페이지로 이동 (추후 구현)
                      },
                    );
                  },
                );
              },
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (error, stack) => Center(
                child: Text('오류 발생: $error'),
              ),
            ),
          ),
          
          // 하단 광고 배너
          const AdBannerWidget(),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => const PlantFormPage()),
          );
        },
        icon: const Icon(Icons.add),
        label: const Text('식물 추가'),
        backgroundColor: Colors.green,
        foregroundColor: Colors.white,
      ),
    );
  }

  Widget _buildWeeklyStats(PlantController controller) {
    final stats = controller.getWeeklyStats();
    final completed = stats['completed'] ?? 0;
    final overdue = stats['overdue'] ?? 0;

    return Container(
      padding: const EdgeInsets.all(16),
      color: Colors.green.shade50,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          _buildStatBadge(
            icon: Icons.check_circle,
            label: '이번 주 완료',
            count: completed,
            color: Colors.green,
          ),
          _buildStatBadge(
            icon: Icons.warning,
            label: '밀린 할 일',
            count: overdue,
            color: Colors.red,
          ),
        ],
      ),
    );
  }

  Widget _buildStatBadge({
    required IconData icon,
    required String label,
    required int count,
    required Color color,
  }) {
    return Column(
      children: [
        Row(
          children: [
            Icon(icon, color: color, size: 20),
            const SizedBox(width: 4),
            Text(
              label,
              style: const TextStyle(
                fontSize: 14,
                fontWeight: FontWeight.w500,
              ),
            ),
          ],
        ),
        const SizedBox(height: 4),
        Text(
          '$count',
          style: TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
            color: color,
          ),
        ),
      ],
    );
  }

  Widget _buildEmptyState(BuildContext context, PlantController controller) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.eco,
            size: 80,
            color: Colors.grey.shade300,
          ),
          const SizedBox(height: 16),
          Text(
            '오늘 물 줄 식물이 없어요!',
            style: Theme.of(context).textTheme.titleLarge?.copyWith(
                  color: Colors.grey.shade600,
                ),
          ),
          const SizedBox(height: 8),
          Text(
            '식물을 추가해보세요',
            style: TextStyle(color: Colors.grey.shade500),
          ),
          const SizedBox(height: 24),
          ElevatedButton.icon(
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const PlantFormPage()),
              );
            },
            icon: const Icon(Icons.add),
            label: const Text('첫 식물 추가하기'),
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.green,
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
            ),
          ),
          const SizedBox(height: 16),
          TextButton(
            onPressed: () async {
              await controller.seedDemo();
              if (context.mounted) {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('데모 데이터를 추가했어요!')),
                );
              }
            },
            child: const Text('데모 데이터로 시작하기'),
          ),
        ],
      ),
    );
  }
}
