#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os

# Feature Graphic 크기
width, height = 1024, 500

# 배경 생성 (단색 - 밝은 베이지/크림)
img = Image.new('RGB', (width, height), color=(245, 243, 238))
draw = ImageDraw.Draw(img)

# 한글 폰트 찾기
korean_fonts = [
    '/System/Library/Fonts/AppleSDGothicNeo.ttc',  # macOS 기본 한글 폰트
    '/System/Library/Fonts/Supplemental/AppleGothic.ttf',
]

title_font = None
feature_font = None

for font_path in korean_fonts:
    if os.path.exists(font_path):
        try:
            title_font = ImageFont.truetype(font_path, 60)
            feature_font = ImageFont.truetype(font_path, 28)
            print(f'✅ 폰트 로드 성공: {font_path}')
            break
        except Exception as e:
            continue

if not title_font:
    print('❌ 한글 폰트를 찾을 수 없습니다.')
    exit(1)

# 왼쪽: 앱 아이콘 + 이름
icon_path = 'assets/images/app_icon.png'
left_section_x = 120

if os.path.exists(icon_path):
    try:
        # 큰 원형 배경
        circle_x = left_section_x
        circle_y = height // 2 - 100
        circle_size = 200
        draw.ellipse([circle_x, circle_y, circle_x + circle_size, circle_y + circle_size], 
                     fill=(220, 215, 205))
        
        # 아이콘
        icon = Image.open(icon_path).convert('RGBA')
        icon_size = 140
        icon = icon.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
        icon_x = circle_x + (circle_size - icon_size) // 2
        icon_y = circle_y + (circle_size - icon_size) // 2
        img.paste(icon, (icon_x, icon_y), icon)
        
        print('✅ 앱 아이콘 추가 완료')
    except Exception as e:
        print(f'⚠️ 아이콘 로드 실패: {e}')

# 앱 이름 (아이콘 아래)
app_name = '물주기 알림_lite'
name_bbox = draw.textbbox((0, 0), app_name, font=title_font)
name_width = name_bbox[2] - name_bbox[0]
name_x = left_section_x + (200 - name_width) // 2
name_y = height // 2 + 120
draw.text((name_x, name_y), app_name, font=title_font, fill=(80, 80, 80))

# 오른쪽: 주요 기능 설명
right_section_x = 500
start_y = 120

features = [
    ('🌱', '식물마다 주기 설정'),
    ('⏰', '정확한 시간 알림'),
    ('📅', 'D-day 카운터'),
]

for i, (emoji, text) in enumerate(features):
    y_pos = start_y + (i * 100)
    
    # 둥근 배경
    bg_width = 450
    bg_height = 70
    bg_x = right_section_x
    bg_y = y_pos
    
    draw.rounded_rectangle(
        [bg_x, bg_y, bg_x + bg_width, bg_y + bg_height],
        radius=35,
        fill=(255, 255, 255)
    )
    
    # 이모지 (왼쪽)
    emoji_x = bg_x + 25
    emoji_y = bg_y + 10
    try:
        emoji_font = ImageFont.truetype('/System/Library/Fonts/Apple Color Emoji.ttc', 40)
        draw.text((emoji_x, emoji_y), emoji, font=emoji_font, embedded_color=True)
    except:
        draw.text((emoji_x, emoji_y), emoji, font=feature_font)
    
    # 텍스트 (오른쪽)
    text_x = emoji_x + 70
    text_y = bg_y + 18
    draw.text((text_x, text_y), text, font=feature_font, fill=(60, 60, 60))

# 저장
output_path = 'assets/store_graphics/feature_graphic.png'
img.save(output_path, 'PNG')
print(f'✅ Feature Graphic 생성 완료: {output_path}')
print(f'   크기: {width} x {height}')
print(f'   제목: 물주기 알림_lite')
print(f'   주요 기능: 식물마다 주기 설정, 정확한 시간 알림, D-day 카운터')
