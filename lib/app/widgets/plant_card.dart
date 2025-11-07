// lib/app/widgets/plant_card.dart
import 'dart:io';
import 'package:flutter/material.dart';
import '../../domain/plant.dart';
import '../../core/utils/date_formats.dart';

class PlantCard extends StatelessWidget {
  const PlantCard({
    super.key,
    required this.plant,
    this.onWatered,
    this.onTap,
    this.showWaterButton = true,
  });

  final Plant plant;
  final VoidCallback? onWatered;
  final VoidCallback? onTap;
  final bool showWaterButton;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final daysUntil = plant.daysUntilNextWater;
    final isOverdue = plant.isOverdue;
    final isDueToday = plant.isDueToday;

    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      elevation: 2,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              // 아바타 (이미지 또는 이니셜)
              _buildAvatar(),
              const SizedBox(width: 16),
              
              // 정보
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Expanded(
                          child: Text(
                            plant.name,
                            style: theme.textTheme.titleMedium?.copyWith(
                              fontWeight: FontWeight.bold,
                            ),
                            overflow: TextOverflow.ellipsis,
                          ),
                        ),
                        if (!plant.isActive)
                          Container(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 8,
                              vertical: 2,
                            ),
                            decoration: BoxDecoration(
                              color: Colors.grey.shade300,
                              borderRadius: BorderRadius.circular(12),
                            ),
                            child: const Text(
                              '비활성',
                              style: TextStyle(fontSize: 12),
                            ),
                          ),
                      ],
                    ),
                    const SizedBox(height: 4),
                    Text(
                      '마지막: ${DateFormats.formatSimple(plant.lastWateredAt)}',
                      style: theme.textTheme.bodySmall?.copyWith(
                        color: Colors.grey.shade600,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Row(
                      children: [
                        Icon(
                          Icons.water_drop,
                          size: 16,
                          color: isOverdue
                              ? Colors.red
                              : isDueToday
                                  ? Colors.orange
                                  : Colors.blue,
                        ),
                        const SizedBox(width: 4),
                        Text(
                          '${plant.intervalDays}일마다',
                          style: theme.textTheme.bodySmall,
                        ),
                        const SizedBox(width: 8),
                        _buildDDayBadge(daysUntil, isOverdue, isDueToday),
                      ],
                    ),
                  ],
                ),
              ),
              
              // 물 줬어요 버튼
              if (showWaterButton && plant.isActive && (isDueToday || isOverdue))
                ElevatedButton(
                  onPressed: onWatered,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.green,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(
                      horizontal: 16,
                      vertical: 8,
                    ),
                  ),
                  child: const Text('물 줬어요'),
                ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildAvatar() {
    if (plant.imagePath != null && plant.imagePath!.isNotEmpty) {
      final file = File(plant.imagePath!);
      if (file.existsSync()) {
        return CircleAvatar(
          radius: 30,
          backgroundImage: FileImage(file),
        );
      }
    }

    // 이니셜 표시
    final initial = plant.name.isNotEmpty ? plant.name[0].toUpperCase() : '?';
    return CircleAvatar(
      radius: 30,
      backgroundColor: Colors.green.shade200,
      child: Text(
        initial,
        style: const TextStyle(
          fontSize: 24,
          fontWeight: FontWeight.bold,
          color: Colors.white,
        ),
      ),
    );
  }

  Widget _buildDDayBadge(int daysUntil, bool isOverdue, bool isDueToday) {
    Color bgColor;
    Color textColor;

    if (isOverdue) {
      bgColor = Colors.red.shade100;
      textColor = Colors.red.shade900;
    } else if (isDueToday) {
      bgColor = Colors.orange.shade100;
      textColor = Colors.orange.shade900;
    } else {
      bgColor = Colors.blue.shade100;
      textColor = Colors.blue.shade900;
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
      decoration: BoxDecoration(
        color: bgColor,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Text(
        DateFormats.getDDayText(daysUntil),
        style: TextStyle(
          fontSize: 12,
          fontWeight: FontWeight.bold,
          color: textColor,
        ),
      ),
    );
  }
}
