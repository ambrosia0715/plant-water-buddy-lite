#!/usr/bin/env python3
"""
물주기 알림 앱 아이콘 생성기
물방울과 식물 잎을 조합한 심플한 디자인
"""

from PIL import Image, ImageDraw, ImageFont
import math

def create_app_icon(size=1024):
    # 배경색: 밝은 하늘색 그라데이션
    img = Image.new('RGB', (size, size), '#FFFFFF')
    draw = ImageDraw.Draw(img)
    
    # 원형 배경 (부드러운 그라데이션 효과)
    center = size // 2
    
    # 배경 그라데이션 (연한 파란색에서 청록색으로)
    for i in range(size):
        for j in range(size):
            dx = i - center
            dy = j - center
            distance = math.sqrt(dx*dx + dy*dy)
            if distance < center:
                # 중심에서 멀어질수록 색상 변화
                ratio = distance / center
                r = int(135 + (64 - 135) * ratio)
                g = int(206 + (224 - 206) * ratio)
                b = int(250 + (208 - 250) * ratio)
                img.putpixel((i, j), (r, g, b))
    
    draw = ImageDraw.Draw(img)
    
    # 물방울 그리기 (중앙 상단)
    droplet_center_x = center
    droplet_center_y = center - size // 6
    droplet_width = size // 4
    droplet_height = size // 3
    
    # 물방울 모양 (타원 + 꼭지점)
    points = []
    for angle in range(135, 405, 3):  # 135도부터 405도까지
        rad = math.radians(angle)
        if angle <= 270:
            # 상단 뾰족한 부분
            scale = 0.5 + 0.5 * (angle - 135) / 135
        else:
            scale = 1.0
        x = droplet_center_x + droplet_width * scale * math.cos(rad)
        y = droplet_center_y + droplet_height * scale * math.sin(rad)
        points.append((x, y))
    
    # 물방울 그림자
    shadow_offset = size // 50
    draw.polygon([(p[0] + shadow_offset, p[1] + shadow_offset) for p in points], 
                 fill=(100, 150, 180, 128))
    
    # 물방울 본체 (밝은 청록색)
    draw.polygon(points, fill=(64, 224, 208))
    
    # 물방울 하이라이트
    highlight_x = droplet_center_x - droplet_width // 4
    highlight_y = droplet_center_y - droplet_height // 4
    highlight_size = droplet_width // 3
    draw.ellipse([highlight_x - highlight_size//2, highlight_y - highlight_size//2,
                  highlight_x + highlight_size//2, highlight_y + highlight_size//2],
                 fill=(200, 255, 255, 200))
    
    # 작은 하이라이트
    small_highlight_x = droplet_center_x + droplet_width // 5
    small_highlight_y = droplet_center_y - droplet_height // 6
    small_size = droplet_width // 6
    draw.ellipse([small_highlight_x - small_size//2, small_highlight_y - small_size//2,
                  small_highlight_x + small_size//2, small_highlight_y + small_size//2],
                 fill=(220, 255, 255, 180))
    
    # 식물 잎 그리기 (하단)
    leaf_y = center + size // 6
    leaf_width = size // 3
    leaf_height = size // 5
    
    # 왼쪽 잎
    left_leaf = [
        (center - leaf_width // 4, leaf_y),
        (center - leaf_width, leaf_y + leaf_height // 2),
        (center - leaf_width // 2, leaf_y + leaf_height),
        (center - leaf_width // 6, leaf_y + leaf_height // 2)
    ]
    draw.polygon(left_leaf, fill=(46, 204, 113))
    
    # 왼쪽 잎 잎맥
    draw.line([(center - leaf_width // 4, leaf_y), 
               (center - leaf_width // 2, leaf_y + leaf_height)], 
              fill=(34, 153, 84), width=size//200)
    
    # 오른쪽 잎
    right_leaf = [
        (center + leaf_width // 4, leaf_y),
        (center + leaf_width, leaf_y + leaf_height // 2),
        (center + leaf_width // 2, leaf_y + leaf_height),
        (center + leaf_width // 6, leaf_y + leaf_height // 2)
    ]
    draw.polygon(right_leaf, fill=(52, 211, 153))
    
    # 오른쪽 잎 잎맥
    draw.line([(center + leaf_width // 4, leaf_y), 
               (center + leaf_width // 2, leaf_y + leaf_height)], 
              fill=(34, 153, 84), width=size//200)
    
    # 줄기
    stem_width = size // 50
    draw.rectangle([center - stem_width, leaf_y - leaf_height // 2,
                    center + stem_width, leaf_y + leaf_height],
                   fill=(46, 204, 113))
    
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
