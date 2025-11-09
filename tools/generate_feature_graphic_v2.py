#!/usr/bin/env python3
"""
Generate a refined Play Store Feature Graphic (1024x500) with:
- Soft radial background
- Left focus app icon in SQUARE container (no crop)
- Bold Korean title hierarchy (rounded-font friendly)
- Three pill badges for key benefits
- Subtle depth (very light shadows only)
Output: assets/store_graphics/feature_graphic_v2.png
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, math

WIDTH, HEIGHT = 1024, 500
SAFE = 36  # safe margin to avoid visual cropping in previews
BG_COLOR = (240, 246, 241)  # very light green-tinted neutral
ROOT = os.path.dirname(os.path.dirname(__file__))  # .../plant_water_buddy_lite
ALT_ROOT = os.path.dirname(ROOT)  # repo root fallback

img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

# Layered radial gradients
radial_layers = [
    ((WIDTH*0.28, HEIGHT*0.55), 420, (219, 238, 223)),
    ((WIDTH*0.75, HEIGHT*0.35), 380, (209, 232, 214)),
]
for center, radius, color in radial_layers:
    cx, cy = center
    for r in range(int(radius), 0, -1):
        alpha = 255 * (1 - r / radius)
        shade = tuple(int(color[i] + (BG_COLOR[i]-color[i]) * (r / radius)) for i in range(3))
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=shade)

# Soft overlay
overlay = Image.new('RGBA', (WIDTH, HEIGHT), (255,255,255,40))
img.paste(overlay, (0,0), overlay)

# Load fonts
# If you have a rounded Korean font (e.g., Pretendard, NanumSquareRound),
# drop it at assets/fonts/rounded_kr.ttf and it will be used.
CUSTOM_FONT = 'assets/fonts/rounded_kr.ttf'
FONT_PATHS = [
    CUSTOM_FONT,
    '/Library/Fonts/NanumSquareRoundB.ttf',
    '/Library/Fonts/NanumSquareRoundR.ttf',
    '/Library/Fonts/NanumSquareRoundL.ttf',
    '/System/Library/Fonts/AppleSDGothicNeo.ttc',
    '/System/Library/Fonts/Supplemental/AppleGothic.ttf',
]
font_title = font_sub = font_badge = None
for p in FONT_PATHS:
    if os.path.exists(p):
        try:
            font_title = ImageFont.truetype(p, 76)
            font_sub = ImageFont.truetype(p, 34)
            font_badge = ImageFont.truetype(p, 26)
            print(f'✅ 폰트 로드: {p}')
            break
        except Exception as e:
            print(f'⚠️ 폰트 로드 실패: {p} ({e})')
if not font_title:
    raise SystemExit('한글 폰트 로드 실패: AppleSDGothicNeo 혹은 rounded_kr.ttf 준비 필요')

TITLE = '물주기 알림 Lite'
SUB = '식물 물주기 날짜를 자동으로 계산하고 정확한 시간에 알려줘요'
# Use check marks instead of emojis for robust rendering across PIL/font combos
BADGES = [
    ('✓', '맞춤 주기 설정'),
    ('✓', '정확한 알림'),
    ('✓', 'D-day 표시'),
]

# Left icon SQUARE container (rounded-rect)
icon_box_size = 320
icon_x = SAFE
icon_y = SAFE + 20
container = Image.new('RGBA', (icon_box_size, icon_box_size), (0,0,0,0))
cd = ImageDraw.Draw(container)
cd.rounded_rectangle([0,0,icon_box_size,icon_box_size], radius=48, fill=(255,255,255,235))
container = container.filter(ImageFilter.GaussianBlur(0.5))
img.paste(container, (icon_x, icon_y), container)

# App icon (square, no crop)
def find_icon():
    candidates_rel = [
        ('assets/images', 'app_icon_rounded.png'),  # Prefer rounded version
        ('assets/images', 'app_icon.png'),
        ('assets/images', 'app_icon_512.png'),
        ('assets/store_graphics', 'app_icon_512.png'),
        ('web/icons', 'icon-512.png'),
    ]
    for base, name in candidates_rel:
        p1 = os.path.join(ROOT, base, name)
        p2 = os.path.join(ALT_ROOT, base, name)
        if os.path.exists(p1):
            return p1
        if os.path.exists(p2):
            return p2
    return None

ICON_PATH = find_icon()
if ICON_PATH:
    app_icon = Image.open(ICON_PATH).convert('RGBA')
    # Fit icon inside container with padding
    pad = 34
    target = icon_box_size - pad*2
    app_icon = app_icon.resize((target, target), Image.Resampling.LANCZOS)
    # Very soft shadow to avoid “깨짐” look
    shadow = Image.new('RGBA', (target, target), (0,0,0,60))
    shadow = shadow.filter(ImageFilter.GaussianBlur(6))
    img.paste(shadow, (icon_x+pad+4, icon_y+pad+6), shadow)
    img.paste(app_icon, (icon_x+pad, icon_y+pad), app_icon)
else:
    # Placeholder
    draw.rounded_rectangle([icon_x+20,icon_y+20,icon_x+icon_box_size-20,icon_y+icon_box_size-20], radius=32, fill=(80,160,120))

# Title & subtitle
text_x = icon_x + icon_box_size + 56
text_y = SAFE + 26
# Title without heavy shadow (cleaner edges)
draw.text((text_x, text_y), TITLE, font=font_title, fill=(38,60,44))

sub_y = text_y + 100
# Wrap subtitle if needed
def draw_wrapped(text, x, y, font, fill, max_width):
    words = text.split(' ')
    lines = []
    line = ''
    for w in words:
        test = (line + ' ' + w).strip()
        tw = draw.textbbox((0,0), test, font=font)[2]
        if tw <= max_width:
            line = test
        else:
            lines.append(line)
            line = w
    if line:
        lines.append(line)
    yy = y
    for ln in lines:
        draw.text((x, yy), ln, font=font, fill=fill)
        yy += font.size + 6
    return yy

right_max = WIDTH - SAFE - text_x
sub_end_y = draw_wrapped(SUB, text_x, sub_y, font_sub, (75,90,80), right_max)

# Badges
badge_y = sub_end_y + 28
badge_gap = 14
badge_height = 58
badge_padding_x = 26
current_x = text_x
# Place badges; wrap to next line if exceeding right bound
for emoji, label in BADGES:
    badge_text = f'{emoji}  {label}'
    tw, th = draw.textbbox((0,0), badge_text, font=font_badge)[2:]
    bw = tw + badge_padding_x*2
    if current_x + bw > WIDTH - SAFE:
        # move to next line
        current_x = text_x
        badge_y += badge_height + 10
    # Badge background with subtle shadow
    badge_img = Image.new('RGBA', (bw, badge_height), (0,0,0,0))
    bd = ImageDraw.Draw(badge_img)
    bd.rounded_rectangle([0,0,bw,badge_height], radius=28, fill=(255,255,255,245))
    bd.rounded_rectangle([3,3,bw, badge_height], radius=28, outline=(0,0,0,25), width=2)
    badge_img = badge_img.filter(ImageFilter.GaussianBlur(0.2))
    img.paste(badge_img, (current_x, badge_y), badge_img)
    draw.text((current_x+badge_padding_x, badge_y + (badge_height-th)/2 -2), badge_text, font=font_badge, fill=(55,70,60))
    current_x += bw + badge_gap

# Footer tagline
footer = '무료 · 오프라인 · 개인정보 수집 없음'
fx = text_x
fy = badge_y + badge_height + 28
draw.text((fx, fy), footer, font=font_badge, fill=(90,105,95))

out_path = 'assets/store_graphics/feature_graphic_v2.png'
os.makedirs(os.path.dirname(out_path), exist_ok=True)
img.save(out_path, 'PNG')
print('✅ 새 Feature Graphic 생성 완료:', out_path)
