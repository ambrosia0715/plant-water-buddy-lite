// lib/app/all_plants_page.dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../state/plant_controller.dart';
import '../data/plant_repo.dart';
import 'widgets/plant_card.dart';
import 'plant_form_page.dart';

class AllPlantsPage extends ConsumerStatefulWidget {
  const AllPlantsPage({super.key});

  @override
  ConsumerState<AllPlantsPage> createState() => _AllPlantsPageState();
}

class _AllPlantsPageState extends ConsumerState<AllPlantsPage> {
  SortOption _sortOption = SortOption.nearestDue;

  @override
  Widget build(BuildContext context) {
    final plantsAsync = ref.watch(plantControllerProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('전체 식물'),
        backgroundColor: Colors.green,
        foregroundColor: Colors.white,
      ),
      body: Column(
        children: [
          // 정렬 옵션
          _buildSortSegment(),
          
          // 식물 리스트
          Expanded(
            child: plantsAsync.when(
              data: (plants) {
                final repo = ref.read(plantRepositoryProvider);
                final sortedPlants = repo.getAll(sort: _sortOption);
                
                if (sortedPlants.isEmpty) {
                  return _buildEmptyState();
                }
                
                return ListView.builder(
                  itemCount: sortedPlants.length,
                  itemBuilder: (context, index) {
                    final plant = sortedPlants[index];
                    return PlantCard(
                      plant: plant,
                      showWaterButton: false,
                      onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (_) => PlantFormPage(plant: plant),
                          ),
                        );
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
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => const PlantFormPage()),
          );
        },
        backgroundColor: Colors.green,
        foregroundColor: Colors.white,
        child: const Icon(Icons.add),
      ),
    );
  }

  Widget _buildSortSegment() {
    return Container(
      padding: const EdgeInsets.all(16),
      child: Row(
        children: [
          const Text(
            '정렬:',
            style: TextStyle(fontWeight: FontWeight.bold),
          ),
          const SizedBox(width: 8),
          Expanded(
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: SegmentedButton<SortOption>(
                segments: const [
                  ButtonSegment(
                    value: SortOption.nearestDue,
                    label: Text('가까운 순'),
                    icon: Icon(Icons.schedule, size: 16),
                  ),
                  ButtonSegment(
                    value: SortOption.mostOverdue,
                    label: Text('밀린 순'),
                    icon: Icon(Icons.warning, size: 16),
                  ),
                  ButtonSegment(
                    value: SortOption.nameAsc,
                    label: Text('이름순'),
                    icon: Icon(Icons.sort_by_alpha, size: 16),
                  ),
                ],
                selected: {_sortOption},
                onSelectionChanged: (Set<SortOption> selected) {
                  setState(() {
                    _sortOption = selected.first;
                  });
                },
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildEmptyState() {
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
            '아직 식물이 없어요',
            style: Theme.of(context).textTheme.titleLarge?.copyWith(
                  color: Colors.grey.shade600,
                ),
          ),
          const SizedBox(height: 8),
          Text(
            '첫 식물을 추가해보세요!',
            style: TextStyle(color: Colors.grey.shade500),
          ),
        ],
      ),
    );
  }
}
