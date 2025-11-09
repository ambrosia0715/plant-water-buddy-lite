from PIL import Image, ImageDraw, ImageFont
import os

def create_screenshot(title, content_lines, filename):
    # 전화 화면 크기 (9:16 비율)
    width, height = 1080, 1920
    
    # 배경
    img = Image.new('RGB', (width, height), '#FFFFFF')
    draw = ImageDraw.Draw(img)
    
    # 폰트 설정
    try:
        title_font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 60)
        content_font = ImageFont.truetype('/System/Library/Fonts/AppleSDGothicNeo.ttc', 45)
        small_font = ImageFont.truetype('/System/Library/Fonts/AppleSDGothicNeo.ttc', 35)
    except:
        title_font = ImageFont.load_default()
        content_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # 상단 바 (초록색)
    draw.rectangle([(0, 0), (width, 150)], fill='#4CAF50')
    
    # 앱 제목
    draw.text((40, 50), title, font=title_font, fill='white')
    
    # 콘텐츠 영역
    y_offset = 200
    for line in content_lines:
        if isinstance(line, tuple):
            text, color, font_type = line
            font = content_font if font_type == 'content' else small_font
            draw.text((40, y_offset), text, font=font, fill=color)
            y_offset += 80 if font_type == 'content' else 60
        else:
            draw.text((40, y_offset), line, font=content_font, fill='#333333')
            y_offset += 80
    
    # 저장
    output_path = f'assets/store_graphics/screenshots/{filename}'
    img.save(output_path)
    print(f'✅ {filename} 생성 완료')

# 스크린샷 1: 홈 화면
screenshot1 = [
    ('오늘 할 일', '#4CAF50', 'content'),
    '',
    ('🌱 몬스테라', '#333333', 'content'),
    ('D-2 (2일 후 물주기)', '#666666', 'small'),
    '',
    ('🌿 스킨답서스', '#333333', 'content'),
    ('D-0 (오늘 물주기!)', '#F44336', 'small'),
    '',
    ('전체 식물', '#4CAF50', 'content'),
    '',
    ('🌱 몬스테라', '#333333', 'content'),
    ('마지막 물주기: 2025-11-07', '#666666', 'small'),
    '',
    ('🌿 스킨답서스', '#333333', 'content'),
    ('마지막 물주기: 2025-11-02', '#666666', 'small'),
    '',
    ('🌵 선인장', '#333333', 'content'),
    ('마지막 물주기: 2025-10-20', '#666666', 'small'),
]
create_screenshot('물주기 알림_lite', screenshot1, '01_home_screen.png')

# 스크린샷 2: 식물 추가 화면
screenshot2 = [
    ('새 식물 추가', '#4CAF50', 'content'),
    '',
    ('식물 이름', '#666666', 'small'),
    ('몬스테라', '#333333', 'content'),
    '',
    ('물주기 주기 (일)', '#666666', 'small'),
    ('7일', '#333333', 'content'),
    '',
    ('알림 시간', '#666666', 'small'),
    ('오전 9:00', '#333333', 'content'),
    '',
    ('마지막 물 준 날짜', '#666666', 'small'),
    ('2025-11-09', '#333333', 'content'),
    '',
    '',
    ('             [저장 버튼]', '#4CAF50', 'content'),
]
create_screenshot('식물 추가', screenshot2, '02_add_plant.png')

# 스크린샷 3: 식물 상세 화면
screenshot3 = [
    ('🌱 몬스테라', '#4CAF50', 'content'),
    '',
    ('물주기 주기', '#666666', 'small'),
    ('7일마다', '#333333', 'content'),
    '',
    ('마지막 물 준 날짜', '#666666', 'small'),
    ('2025-11-07', '#333333', 'content'),
    '',
    ('다음 물주기', '#666666', 'small'),
    ('2025-11-14 (D-5)', '#333333', 'content'),
    '',
    ('알림 시간', '#666666', 'small'),
    ('오전 9:00', '#333333', 'content'),
    '',
    '',
    ('         [물 줬어요 버튼]', '#4CAF50', 'content'),
    '',
    ('메모', '#666666', 'small'),
    ('햇빛을 좋아하는 식물', '#333333', 'content'),
]
create_screenshot('식물 상세', screenshot3, '03_plant_detail.png')

# 스크린샷 4: 설정 화면
screenshot4 = [
    ('설정', '#4CAF50', 'content'),
    '',
    ('알림 관리', '#666666', 'small'),
    ('  테스트 알림 보내기', '#333333', 'content'),
    ('  예약된 알림 확인', '#333333', 'content'),
    ('  알림 재설정', '#333333', 'content'),
    '',
    ('데이터 관리', '#666666', 'small'),
    ('  데이터 내보내기', '#333333', 'content'),
    ('  데이터 가져오기', '#333333', 'content'),
    '',
    ('앱 정보', '#666666', 'small'),
    ('  버전: 1.0.0', '#333333', 'content'),
    ('  개인정보 처리방침', '#333333', 'content'),
    '',
    ('배터리 최적화 안내', '#666666', 'small'),
    ('알림이 제대로 울리지 않는다면', '#999999', 'small'),
    ('배터리 최적화를 해제해주세요', '#999999', 'small'),
]
create_screenshot('설정', screenshot4, '04_settings.png')

print('\n✅ 모든 스크린샷 생성 완료!')
print('📁 위치: assets/store_graphics/screenshots/')
