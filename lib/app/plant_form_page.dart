// lib/app/plant_form_page.dart
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:image_picker/image_picker.dart';
import '../domain/plant.dart';
import '../state/plant_controller.dart';
import '../core/utils/date_formats.dart';

class PlantFormPage extends ConsumerStatefulWidget {
  const PlantFormPage({super.key, this.plant});

  final Plant? plant;

  @override
  ConsumerState<PlantFormPage> createState() => _PlantFormPageState();
}

class _PlantFormPageState extends ConsumerState<PlantFormPage> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _customIntervalController = TextEditingController();
  
  String? _imagePath;
  int _intervalDays = 7;
  DateTime _lastWateredAt = DateTime.now();
  TimeOfDay _notifyTime = const TimeOfDay(hour: 9, minute: 0);
  bool _isActive = true;
  
  final List<int> _presetIntervals = [3, 7, 10, 14, 30];
  bool _useCustomInterval = false;

  @override
  void initState() {
    super.initState();
    
    if (widget.plant != null) {
      final plant = widget.plant!;
      _nameController.text = plant.name;
      _imagePath = plant.imagePath;
      _intervalDays = plant.intervalDays;
      _lastWateredAt = plant.lastWateredAt;
      _notifyTime = TimeOfDay(hour: plant.notifyHour, minute: plant.notifyMinute);
      _isActive = plant.isActive;
      
      if (!_presetIntervals.contains(_intervalDays)) {
        _useCustomInterval = true;
        _customIntervalController.text = _intervalDays.toString();
      }
    }
  }

  @override
  void dispose() {
    _nameController.dispose();
    _customIntervalController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final isEditing = widget.plant != null;

    return Scaffold(
      appBar: AppBar(
        title: Text(isEditing ? '식물 수정' : '식물 추가'),
        backgroundColor: Colors.green,
        foregroundColor: Colors.white,
      ),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            // 이미지 선택
            _buildImagePicker(),
            const SizedBox(height: 24),
            
            // 이름
            TextFormField(
              controller: _nameController,
              decoration: const InputDecoration(
                labelText: '식물 이름 *',
                border: OutlineInputBorder(),
                prefixIcon: Icon(Icons.eco),
              ),
              validator: (value) {
                if (value == null || value.trim().isEmpty) {
                  return '식물 이름을 입력해주세요';
                }
                return null;
              },
            ),
            const SizedBox(height: 16),
            
            // 물주기 주기
            const Text(
              '물주기 주기',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Wrap(
              spacing: 8,
              children: [
                ..._presetIntervals.map((days) => ChoiceChip(
                      label: Text('$days일'),
                      selected: !_useCustomInterval && _intervalDays == days,
                      onSelected: (selected) {
                        if (selected) {
                          setState(() {
                            _useCustomInterval = false;
                            _intervalDays = days;
                          });
                        }
                      },
                    )),
                ChoiceChip(
                  label: const Text('직접 입력'),
                  selected: _useCustomInterval,
                  onSelected: (selected) {
                    setState(() {
                      _useCustomInterval = selected;
                    });
                  },
                ),
              ],
            ),
            if (_useCustomInterval) ...[
              const SizedBox(height: 8),
              TextFormField(
                controller: _customIntervalController,
                decoration: const InputDecoration(
                  labelText: '주기 (일)',
                  border: OutlineInputBorder(),
                  suffixText: '일',
                ),
                keyboardType: TextInputType.number,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return '주기를 입력해주세요';
                  }
                  final days = int.tryParse(value);
                  if (days == null || days < 1) {
                    return '1일 이상 입력해주세요';
                  }
                  return null;
                },
                onChanged: (value) {
                  final days = int.tryParse(value);
                  if (days != null && days >= 1) {
                    _intervalDays = days;
                  }
                },
              ),
            ],
            const SizedBox(height: 16),
            
            // 마지막 물 준 날짜
            ListTile(
              contentPadding: EdgeInsets.zero,
              title: const Text('마지막 물 준 날짜'),
              subtitle: Text(DateFormats.formatWithWeekday(_lastWateredAt)),
              trailing: const Icon(Icons.calendar_today),
              onTap: () async {
                final date = await showDatePicker(
                  context: context,
                  initialDate: _lastWateredAt,
                  firstDate: DateTime.now().subtract(const Duration(days: 365)),
                  lastDate: DateTime.now(),
                );
                if (date != null) {
                  setState(() {
                    _lastWateredAt = date;
                  });
                }
              },
            ),
            const Divider(),
            
            // 알림 시간
            ListTile(
              contentPadding: EdgeInsets.zero,
              title: const Text('알림 시간'),
              subtitle: Text(DateFormats.formatTime(_notifyTime.hour, _notifyTime.minute)),
              trailing: const Icon(Icons.access_time),
              onTap: () async {
                final time = await showTimePicker(
                  context: context,
                  initialTime: _notifyTime,
                  builder: (context, child) {
                    return MediaQuery(
                      data: MediaQuery.of(context).copyWith(alwaysUse24HourFormat: false),
                      child: child!,
                    );
                  },
                );
                if (time != null) {
                  setState(() {
                    _notifyTime = time;
                  });
                }
              },
            ),
            const Divider(),
            
            // 활성화 스위치
            SwitchListTile(
              contentPadding: EdgeInsets.zero,
              title: const Text('알림 활성화'),
              subtitle: Text(_isActive ? '알림을 받습니다' : '알림을 받지 않습니다'),
              value: _isActive,
              onChanged: (value) {
                setState(() {
                  _isActive = value;
                });
              },
            ),
            const SizedBox(height: 24),
            
            // 저장 버튼
            ElevatedButton(
              onPressed: _savePlant,
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.green,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(vertical: 16),
                textStyle: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              ),
              child: Text(isEditing ? '수정하기' : '저장하기'),
            ),
            
            // 삭제 버튼 (수정 모드일 때만)
            if (isEditing) ...[
              const SizedBox(height: 8),
              OutlinedButton(
                onPressed: _deletePlant,
                style: OutlinedButton.styleFrom(
                  foregroundColor: Colors.red,
                  padding: const EdgeInsets.symmetric(vertical: 16),
                ),
                child: const Text('삭제하기'),
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildImagePicker() {
    return Center(
      child: GestureDetector(
        onTap: _pickImage,
        child: Stack(
          children: [
            CircleAvatar(
              radius: 60,
              backgroundColor: Colors.green.shade100,
              backgroundImage: _imagePath != null && _imagePath!.isNotEmpty
                  ? FileImage(File(_imagePath!))
                  : null,
              child: _imagePath == null || _imagePath!.isEmpty
                  ? Icon(Icons.camera_alt, size: 40, color: Colors.green.shade700)
                  : null,
            ),
            Positioned(
              bottom: 0,
              right: 0,
              child: Container(
                padding: const EdgeInsets.all(4),
                decoration: const BoxDecoration(
                  color: Colors.green,
                  shape: BoxShape.circle,
                ),
                child: const Icon(Icons.edit, size: 20, color: Colors.white),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Future<void> _pickImage() async {
    final picker = ImagePicker();
    final image = await picker.pickImage(source: ImageSource.gallery);
    
    if (image != null) {
      setState(() {
        _imagePath = image.path;
      });
    }
  }

  void _savePlant() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    final controller = ref.read(plantControllerProvider.notifier);
    
    final plant = Plant(
      id: widget.plant?.id ?? '',
      name: _nameController.text.trim(),
      imagePath: _imagePath,
      intervalDays: _intervalDays,
      lastWateredAt: _lastWateredAt,
      notifyHour: _notifyTime.hour,
      notifyMinute: _notifyTime.minute,
      isActive: _isActive,
    );

    if (widget.plant == null) {
      await controller.add(plant);
    } else {
      await controller.update(plant);
    }

    if (mounted) {
      Navigator.pop(context);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(widget.plant == null ? '식물을 추가했어요!' : '식물 정보를 수정했어요!'),
          backgroundColor: Colors.green,
        ),
      );
    }
  }

  void _deletePlant() async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('식물 삭제'),
        content: const Text('정말 삭제하시겠어요?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('취소'),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, true),
            style: TextButton.styleFrom(foregroundColor: Colors.red),
            child: const Text('삭제'),
          ),
        ],
      ),
    );

    if (confirmed == true && widget.plant != null) {
      final controller = ref.read(plantControllerProvider.notifier);
      await controller.delete(widget.plant!.id);
      
      if (mounted) {
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('식물을 삭제했어요'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }
}
