#!/usr/bin/env python3
"""
물주기 알림 앱 아이콘 생성기
귀여운 물방울 캐릭터 디자인
"""

from PIL import Image, ImageDraw
import math

def create_app_icon(size=1024):
    # 부드러운 그라데이션 배경
    img = Image.new('RGB', (size, size), '#FFFFFF')
    
    # 배경 그라데이션 (하늘색에서 청록색으로)
    for y in range(size):
        ratio = y / size
        r = int(135 + (100 - 135) * ratio)
        g = int(206 + (200 - 206) * ratio)
        b = int(250 + (230 - 250) * ratio)
        for x in range(size):
            img.putpixel((x, y), (r, g, b))
    
    draw = ImageDraw.Draw(img)
    center = size // 2
    
    # === 귀여운 물방울 캐릭터 ===
    char_y_offset = -size // 12
    
    # 물방울 몸통 (부드러운 물방울 모양)
    droplet_center_x = center
    droplet_center_y = center + char_y_offset
    droplet_width = size // 2.8
    droplet_height = size // 2.5
    
    # 물방울 외곽선 만들기
    points = []
    for angle in range(140, 400, 1):
        rad = math.radians(angle)
        if angle <= 270:
            # 위쪽 뾰족한 부분
            scale_factor = 0.3 + 0.7 * ((angle - 140) / 130) ** 0.8
        else:
            scale_factor = 1.0
        
        x = droplet_center_x + droplet_width * scale_factor * math.cos(rad)
        y = droplet_center_y + droplet_height * scale_factor * math.sin(rad)
        points.append((x, y))
    
    # 그림자 (여러 레이어로 부드럽게)
    for i in range(5):
        shadow_points = [(p[0] + i*2, p[1] + i*2) for p in points]
        shadow_gray = 200 - i * 15
        draw.polygon(shadow_points, fill=(shadow_gray, shadow_gray, shadow_gray))
    
    # 물방울 본체 (밝은 청록색)
    draw.polygon(points, fill=(100, 200, 255))
    
    # 물방울 하이라이트 (3D 효과)
    highlight1_x = droplet_center_x - droplet_width // 3
    highlight1_y = droplet_center_y - droplet_height // 4
    highlight1_size = droplet_width // 2
    
    # 큰 하이라이트
    draw.ellipse([
        highlight1_x - highlight1_size//2,
        highlight1_y - highlight1_size//2,
        highlight1_x + highlight1_size//2,
        highlight1_y + highlight1_size//2
    ], fill=(180, 230, 255))
    
    # 중간 하이라이트
    draw.ellipse([
        highlight1_x - highlight1_size//3,
        highlight1_y - highlight1_size//3,
        highlight1_x + highlight1_size//3,
        highlight1_y + highlight1_size//3
    ], fill=(220, 245, 255))
    
    # 작은 하이라이트들 (반짝이는 효과)
    small_highlights = [
        (droplet_center_x + droplet_width//3, droplet_center_y - droplet_height//6, droplet_width//8),
        (droplet_center_x - droplet_width//6, droplet_center_y + droplet_height//8, droplet_width//12),
        (droplet_center_x + droplet_width//5, droplet_center_y + droplet_height//5, droplet_width//15)
    ]
    
    for hx, hy, hsize in small_highlights:
        draw.ellipse([hx - hsize, hy - hsize, hx + hsize, hy + hsize], fill=(240, 250, 255))
    
    # 물방울 외곽선 (부드러운 테두리)
    draw.polygon(points, outline=(60, 150, 220), width=size//180)
    
    # === 귀여운 얼굴 ===
    face_y = droplet_center_y
    
    # 눈 (큰 귀여운 눈)
    eye_y = face_y - droplet_height // 8
    eye_spacing = droplet_width // 4
    eye_size = droplet_width // 8
    
    # 왼쪽 눈
    left_eye_x = center - eye_spacing
    # 흰자
    draw.ellipse([
        left_eye_x - eye_size,
        eye_y - eye_size,
        left_eye_x + eye_size,
        eye_y + eye_size
    ], fill=(255, 255, 255))
    # 눈동자
    pupil_size = eye_size // 1.8
    draw.ellipse([
        left_eye_x - pupil_size,
        eye_y - pupil_size,
        left_eye_x + pupil_size,
        eye_y + pupil_size
    ], fill=(40, 40, 60))
    # 하이라이트
    pupil_highlight = pupil_size // 2.5
    draw.ellipse([
        left_eye_x - pupil_size//2 - pupil_highlight//2,
        eye_y - pupil_size//2 - pupil_highlight//2,
        left_eye_x - pupil_size//2 + pupil_highlight//2,
        eye_y - pupil_size//2 + pupil_highlight//2
    ], fill=(255, 255, 255))
    
    # 오른쪽 눈
    right_eye_x = center + eye_spacing
    # 흰자
    draw.ellipse([
        right_eye_x - eye_size,
        eye_y - eye_size,
        right_eye_x + eye_size,
        eye_y + eye_size
    ], fill=(255, 255, 255))
    # 눈동자
    draw.ellipse([
        right_eye_x - pupil_size,
        eye_y - pupil_size,
        right_eye_x + pupil_size,
        eye_y + pupil_size
    ], fill=(40, 40, 60))
    # 하이라이트
    draw.ellipse([
        right_eye_x - pupil_size//2 - pupil_highlight//2,
        eye_y - pupil_size//2 - pupil_highlight//2,
        right_eye_x - pupil_size//2 + pupil_highlight//2,
        eye_y - pupil_size//2 + pupil_highlight//2
    ], fill=(255, 255, 255))
    
    # 미소 (반달 모양)
    smile_y = face_y + droplet_height // 6
    smile_width = droplet_width // 3
    smile_height = droplet_height // 8
    
    # 미소 외곽
    smile_bbox = [
        center - smile_width,
        smile_y - smile_height,
        center + smile_width,
        smile_y + smile_height * 3
    ]
    draw.arc(smile_bbox, 0, 180, fill=(40, 40, 60), width=size//120)
    
    # 볼 홍조
    blush_y = face_y + droplet_height // 12
    blush_size = droplet_width // 10
    # 왼쪽 볼
    draw.ellipse([
        center - eye_spacing * 1.3 - blush_size,
        blush_y - blush_size//2,
        center - eye_spacing * 1.3 + blush_size,
        blush_y + blush_size//2
    ], fill=(255, 180, 200))
    # 오른쪽 볼
    draw.ellipse([
        center + eye_spacing * 1.3 - blush_size,
        blush_y - blush_size//2,
        center + eye_spacing * 1.3 + blush_size,
        blush_y + blush_size//2
    ], fill=(255, 180, 200))
    
    # === 식물 장식 (머리 위 왕관처럼) ===
    plant_y = droplet_center_y - droplet_height * 0.85
    leaf_size = droplet_width // 3.5
    
    # 중앙 줄기
    stem_width = size // 80
    stem_height = droplet_height // 6
    draw.rectangle([
        center - stem_width,
        plant_y - stem_height,
        center + stem_width,
        plant_y
    ], fill=(60, 140, 60))
    
    # 왼쪽 잎 (하트 모양)
    left_leaf_center = center - leaf_size * 0.8
    left_leaf_top = plant_y - stem_height - leaf_size * 0.3
    
    left_leaf_points = []
    for angle in range(0, 360, 5):
        rad = math.radians(angle)
        # 하트 모양 공식
        if angle <= 180:
            r = leaf_size * 0.5 * (1 + 0.3 * math.sin(rad * 3))
        else:
            r = leaf_size * 0.4
        x = left_leaf_center + r * math.cos(rad)
        y = left_leaf_top + r * math.sin(rad) * 1.2
        left_leaf_points.append((x, y))
    
    draw.polygon(left_leaf_points, fill=(80, 200, 100))
    draw.polygon(left_leaf_points, outline=(50, 150, 70), width=size//250)
    
    # 오른쪽 잎
    right_leaf_center = center + leaf_size * 0.8
    right_leaf_points = []
    for angle in range(0, 360, 5):
        rad = math.radians(angle)
        if angle <= 180:
            r = leaf_size * 0.5 * (1 + 0.3 * math.sin(rad * 3))
        else:
            r = leaf_size * 0.4
        x = right_leaf_center + r * math.cos(rad)
        y = left_leaf_top + r * math.sin(rad) * 1.2
        right_leaf_points.append((x, y))
    
    draw.polygon(right_leaf_points, fill=(100, 220, 120))
    draw.polygon(right_leaf_points, outline=(60, 170, 80), width=size//250)
    
    # 잎맥
    draw.line([
        (left_leaf_center, left_leaf_top - leaf_size * 0.3),
        (left_leaf_center, left_leaf_top + leaf_size * 0.3)
    ], fill=(50, 150, 70), width=size//300)
    
    draw.line([
        (right_leaf_center, left_leaf_top - leaf_size * 0.3),
        (right_leaf_center, left_leaf_top + leaf_size * 0.3)
    ], fill=(60, 170, 80), width=size//300)
    
    # 작은 새싹 (가운데)
    sprout_points = [
        (center, plant_y - stem_height - leaf_size * 0.5),
        (center - leaf_size * 0.25, plant_y - stem_height - leaf_size * 0.2),
        (center, plant_y - stem_height),
        (center + leaf_size * 0.25, plant_y - stem_height - leaf_size * 0.2)
    ]
    draw.polygon(sprout_points, fill=(120, 230, 140))
    draw.polygon(sprout_points, outline=(70, 180, 90), width=size//300)
    
    return img

# 1024x1024 아이콘 생성
print("Creating cute character app icon...")
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

print("\n🌱 Done! Cute character icon is ready!")
