#!/usr/bin/env python3
"""
물주기 알림 앱 아이콘 생성기
물방울과 식물 잎을 조합한 심플한 디자인
"""

from PIL import Image, ImageDraw, ImageFont
import math

def create_app_icon(size=1024):
    # 배경색: 밝은 하늘색 (전체 사각형)
    img = Image.new('RGB', (size, size), '#E8F4F8')
    draw = ImageDraw.Draw(img)
    
    center = size // 2
    
    center = size // 2
    
    # 물방울 그리기 (더 크게, 중앙 상단)
    droplet_center_x = center
    droplet_center_y = center - size // 8
    droplet_width = size // 2.5
    droplet_height = size // 2.2
    
    # 물방울 모양 (타원 + 뾰족한 꼭지점)
    points = []
    for angle in range(135, 405, 2):  # 더 부드러운 곡선
        rad = math.radians(angle)
        if angle <= 270:
            # 상단 뾰족한 부분
            scale = 0.4 + 0.6 * (angle - 135) / 135
        else:
            scale = 1.0
        x = droplet_center_x + droplet_width * scale * math.cos(rad)
        y = droplet_center_y + droplet_height * scale * math.sin(rad)
        points.append((x, y))
    
    # 물방울 그림자 (더 부드럽게)
    shadow_offset = size // 60
    for i in range(3):
        offset = shadow_offset * (i + 1)
        alpha_val = 50 - i * 15
        shadow_points = [(p[0] + offset, p[1] + offset) for p in points]
        # PIL은 RGB만 지원하므로 어두운 회색 사용
        shadow_color = (180 - i * 20, 200 - i * 20, 210 - i * 20)
        draw.polygon(shadow_points, fill=shadow_color, outline=shadow_color)
    
    # 물방울 본체 (더 진한 청록색 - 파란색 계열)
    draw.polygon(points, fill=(30, 144, 255))  # DodgerBlue
    
    # 물방울 외곽선
    draw.polygon(points, outline=(20, 100, 200), width=size//150)
    
    # 물방울 하이라이트 (더 밝게)
    highlight_x = droplet_center_x - droplet_width // 3
    highlight_y = droplet_center_y - droplet_height // 3
    highlight_size = droplet_width // 2.5
    draw.ellipse([highlight_x - highlight_size//2, highlight_y - highlight_size//2,
                  highlight_x + highlight_size//2, highlight_y + highlight_size//2],
                 fill=(150, 200, 255))
    
    # 작은 하이라이트
    small_highlight_x = droplet_center_x + droplet_width // 4
    small_highlight_y = droplet_center_y - droplet_height // 5
    small_size = droplet_width // 5
    draw.ellipse([small_highlight_x - small_size//2, small_highlight_y - small_size//2,
                  small_highlight_x + small_size//2, small_highlight_y + small_size//2],
                 fill=(180, 220, 255))
    
    # 식물 잎 그리기 (하단, 더 크고 선명한 초록색)
    leaf_y = center + size // 5
    leaf_width = size // 2.2
    leaf_height = size // 3.5
    
    # 식물 잎 그리기 (하단, 더 크고 선명한 초록색)
    leaf_y = center + size // 5
    leaf_width = size // 2.2
    leaf_height = size // 3.5
    
    # 왼쪽 잎 (더 진한 초록색)
    left_leaf = [
        (center - leaf_width // 5, leaf_y),
        (center - leaf_width * 0.85, leaf_y + leaf_height // 2),
        (center - leaf_width * 0.6, leaf_y + leaf_height),
        (center - leaf_width // 8, leaf_y + leaf_height // 2)
    ]
    draw.polygon(left_leaf, fill=(34, 139, 34))  # ForestGreen
    
    # 왼쪽 잎 외곽선
    draw.polygon(left_leaf, outline=(25, 100, 25), width=size//200)
    
    # 왼쪽 잎 잎맥 (더 굵게)
    draw.line([(center - leaf_width // 5, leaf_y), 
               (center - leaf_width * 0.6, leaf_y + leaf_height)], 
              fill=(20, 80, 20), width=size//120)
    
    # 오른쪽 잎 (밝은 초록색으로 대비)
    right_leaf = [
        (center + leaf_width // 5, leaf_y),
        (center + leaf_width * 0.85, leaf_y + leaf_height // 2),
        (center + leaf_width * 0.6, leaf_y + leaf_height),
        (center + leaf_width // 8, leaf_y + leaf_height // 2)
    ]
    draw.polygon(right_leaf, fill=(50, 205, 50))  # LimeGreen
    
    # 오른쪽 잎 외곽선
    draw.polygon(right_leaf, outline=(30, 150, 30), width=size//200)
    
    # 오른쪽 잎 잎맥 (더 굵게)
    draw.line([(center + leaf_width // 5, leaf_y), 
               (center + leaf_width * 0.6, leaf_y + leaf_height)], 
              fill=(25, 120, 25), width=size//120)
    
    # 줄기 (더 굵고 진한 초록색)
    stem_width = size // 40
    draw.rectangle([center - stem_width, leaf_y - leaf_height // 3,
                    center + stem_width, leaf_y + leaf_height],
                   fill=(40, 120, 40))
    
    return img

# 1024x1024 아이콘 생성
print("Creating app icon...")
icon = create_app_icon(1024)
icon.save('/Users/ambrosia0715/Desktop/project/AquaLeaf/plant_water_buddy_lite/assets/images/app_icon.png')
print("✓ App icon created: assets/images/app_icon.png")

# iOS용 둥근 모서리 버전도 생성
print("Creating rounded icon for iOS...")
rounded = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
mask = Image.new('L', (1024, 1024), 0)
mask_draw = ImageDraw.Draw(mask)
mask_draw.rounded_rectangle([0, 0, 1024, 1024], radius=180, fill=255)
rounded.paste(icon, (0, 0))
rounded.putalpha(mask)
rounded.save('/Users/ambrosia0715/Desktop/project/AquaLeaf/plant_water_buddy_lite/assets/images/app_icon_rounded.png')
print("✓ Rounded icon created: assets/images/app_icon_rounded.png")

print("\nDone! Icons are ready to use.")
