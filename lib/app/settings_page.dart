// lib/app/settings_page.dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../state/plant_controller.dart';

class SettingsPage extends ConsumerStatefulWidget {
  const SettingsPage({super.key});

  @override
  ConsumerState<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends ConsumerState<SettingsPage> {
  @override
  Widget build(BuildContext context) {
    final controller = ref.read(plantControllerProvider.notifier);
    final notificationService = ref.read(notificationServiceProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('설정'),
        backgroundColor: Colors.green,
        foregroundColor: Colors.white,
      ),
      body: ListView(
        children: [
          // 알림 설정
          _buildSection(
            title: '알림',
            children: [
              ListTile(
                leading: const Icon(Icons.notifications),
                title: const Text('알림 권한 요청'),
                subtitle: const Text('알림을 받으려면 권한이 필요합니다'),
                trailing: const Icon(Icons.chevron_right),
                onTap: () async {
                  await notificationService.requestPermission();
                  if (mounted) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('알림 권한을 확인했습니다')),
                    );
                  }
                },
              ),
              ListTile(
                leading: const Icon(Icons.refresh),
                title: const Text('알림 재설정'),
                subtitle: const Text('모든 알림을 다시 예약합니다'),
                trailing: const Icon(Icons.chevron_right),
                onTap: () async {
                  await controller.reconcileNotifications();
                  if (mounted) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(
                        content: Text('알림을 재설정했습니다'),
                        backgroundColor: Colors.green,
                      ),
                    );
                  }
                },
              ),
            ],
          ),
          
          const Divider(height: 32),
          
          // 데이터 관리
          _buildSection(
            title: '데이터 관리',
            children: [
              ListTile(
                leading: const Icon(Icons.upload_file),
                title: const Text('데이터 내보내기'),
                subtitle: const Text('식물 정보를 JSON 파일로 저장'),
                trailing: const Icon(Icons.chevron_right),
                onTap: () async {
                  try {
                    await controller.exportJson();
                    if (mounted) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(
                          content: Text('데이터를 내보냈습니다'),
                          backgroundColor: Colors.green,
                        ),
                      );
                    }
                  } catch (e) {
                    if (mounted) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text('오류 발생: $e'),
                          backgroundColor: Colors.red,
                        ),
                      );
                    }
                  }
                },
              ),
              ListTile(
                leading: const Icon(Icons.download),
                title: const Text('데이터 가져오기'),
                subtitle: const Text('JSON 파일에서 식물 정보 복원'),
                trailing: const Icon(Icons.chevron_right),
                onTap: () async {
                  await _importData(controller);
                },
              ),
            ],
          ),
          
          const Divider(height: 32),
          
          // 앱 정보
          _buildSection(
            title: '앱 정보',
            children: [
              const ListTile(
                leading: Icon(Icons.info),
                title: Text('버전'),
                subtitle: Text('1.0.0'),
              ),
              ListTile(
                leading: const Icon(Icons.description),
                title: const Text('개인정보 처리방침'),
                trailing: const Icon(Icons.chevron_right),
                onTap: () {
                  _showPrivacyPolicy(context);
                },
              ),
              ListTile(
                leading: const Icon(Icons.article),
                title: const Text('오픈소스 라이선스'),
                trailing: const Icon(Icons.chevron_right),
                onTap: () {
                  showLicensePage(
                    context: context,
                    applicationName: 'Plant Water Buddy - Lite',
                    applicationVersion: '1.0.0',
                  );
                },
              ),
            ],
          ),
          
          const Divider(height: 32),
          
          // 개발자 옵션
          _buildSection(
            title: '개발자',
            children: [
              ListTile(
                leading: const Icon(Icons.bug_report),
                title: const Text('데모 데이터 추가'),
                trailing: const Icon(Icons.chevron_right),
                onTap: () async {
                  await controller.seedDemo();
                  if (mounted) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(
                        content: Text('데모 데이터를 추가했습니다'),
                        backgroundColor: Colors.green,
                      ),
                    );
                  }
                },
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildSection({
    required String title,
    required List<Widget> children,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          child: Text(
            title,
            style: const TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.bold,
              color: Colors.grey,
            ),
          ),
        ),
        ...children,
      ],
    );
  }

  Future<void> _importData(PlantController controller) async {
    try {
      // 파일 선택 대신 간단한 텍스트 입력으로 구현
      final jsonString = await showDialog<String>(
        context: context,
        builder: (context) => _ImportDialog(),
      );

      if (jsonString != null && jsonString.isNotEmpty) {
        final count = await controller.importJson(jsonString);
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('$count개의 식물 정보를 가져왔습니다'),
              backgroundColor: Colors.green,
            ),
          );
        }
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('오류 발생: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  void _showPrivacyPolicy(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('개인정보 처리방침'),
        content: const SingleChildScrollView(
          child: Text(
            'Plant Water Buddy - Lite는 다음과 같이 개인정보를 처리합니다:\n\n'
            '1. 수집하는 정보\n'
            '- 식물 이름, 물주기 주기, 사진 등 사용자가 직접 입력한 정보만 수집합니다.\n'
            '- 모든 데이터는 기기 내부에만 저장됩니다.\n\n'
            '2. 정보의 이용\n'
            '- 물주기 알림 전송\n'
            '- 식물 관리 기록 유지\n\n'
            '3. 정보의 보관\n'
            '- 모든 정보는 사용자 기기에만 저장되며, 외부 서버로 전송되지 않습니다.\n'
            '- 앱 삭제 시 모든 정보가 함께 삭제됩니다.\n\n'
            '4. 광고\n'
            '- Google AdMob을 통한 광고가 표시됩니다.\n'
            '- AdMob의 개인정보 처리방침은 Google 정책을 따릅니다.\n\n'
            '5. 문의\n'
            '- 문의사항은 앱 스토어 리뷰를 통해 전달해주세요.',
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('확인'),
          ),
        ],
      ),
    );
  }
}

class _ImportDialog extends StatefulWidget {
  @override
  State<_ImportDialog> createState() => _ImportDialogState();
}

class _ImportDialogState extends State<_ImportDialog> {
  final _controller = TextEditingController();

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('JSON 데이터 가져오기'),
      content: TextField(
        controller: _controller,
        decoration: const InputDecoration(
          hintText: 'JSON 텍스트를 붙여넣으세요',
          border: OutlineInputBorder(),
        ),
        maxLines: 10,
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context),
          child: const Text('취소'),
        ),
        TextButton(
          onPressed: () => Navigator.pop(context, _controller.text),
          child: const Text('가져오기'),
        ),
      ],
    );
  }
}
