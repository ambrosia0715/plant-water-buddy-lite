#!/usr/bin/env python3
"""
Generate a premium Play Store Feature Graphic (1024x500) with refined visuals:
- Soft layered gradient background + subtle leaf watermark
- Left square icon container using app_icon_rounded.png if available
- Title with "Lite" accent pill
- Short, crisp subtitle
- Clean chips (✓ 맞춤 주기 / ✓ 정확 알림 / ✓ D‑day)
Output: assets/store_graphics/feature_graphic_premium.png
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

WIDTH, HEIGHT = 1024, 500
SAFE = 36
BG_BASE = (239, 247, 243)  # fresh light greenish neutral
ROOT = os.path.dirname(os.path.dirname(__file__))
ALT_ROOT = os.path.dirname(ROOT)

# Canvas
img = Image.new('RGB', (WIDTH, HEIGHT), BG_BASE)
draw = ImageDraw.Draw(img)

# Background: radial layers
radials = [
    ((int(WIDTH*0.20), int(HEIGHT*0.80)), 480, (204, 233, 215)),
    ((int(WIDTH*0.85), int(HEIGHT*0.25)), 420, (200, 228, 210)),
]
for (cx, cy), radius, color in radials:
    for r in range(radius, 0, -3):
        t = r / radius
        shade = (
            int(color[0] + (BG_BASE[0] - color[0]) * t),
            int(color[1] + (BG_BASE[1] - color[1]) * t),
            int(color[2] + (BG_BASE[2] - color[2]) * t),
        )
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=shade)

# Subtle diagonal sheen overlay
sheen = Image.new('RGBA', (WIDTH, HEIGHT), (255,255,255,0))
sd = ImageDraw.Draw(sheen)
for y in range(0, HEIGHT, 4):
    alpha = int(26 * max(0, 1 - y/HEIGHT))
    sd.line([(0, y), (WIDTH, y)], fill=(255,255,255,alpha), width=1)
img.paste(sheen, (0,0), sheen)

# Watermark leaf silhouette
wm = Image.new('RGBA', (WIDTH, HEIGHT), (0,0,0,0))
wmd = ImageDraw.Draw(wm)
# Simple abstract leaf using polygons and arcs
wmd.polygon([(870, 450), (820, 260), (980, 320)], fill=(170, 195, 180, 50))
wmd.ellipse([770, 150, 980, 360], outline=(170, 195, 180, 55), width=10)
wm = wm.filter(ImageFilter.GaussianBlur(10))
img.paste(wm, (0,0), wm)

# Fonts (rounded-preferred)
FONT_CANDIDATES = [
    os.path.join(ROOT, 'assets', 'fonts', 'rounded_kr.ttf'),
    '/Library/Fonts/NanumSquareRoundB.ttf',
    '/Library/Fonts/NanumSquareRoundR.ttf',
    '/System/Library/Fonts/AppleSDGothicNeo.ttc',
]
font_title = font_sub = font_badge = None
for p in FONT_CANDIDATES:
    if os.path.exists(p):
        try:
            font_title = ImageFont.truetype(p, 76)
            font_sub = ImageFont.truetype(p, 34)
            font_badge = ImageFont.truetype(p, 26)
            print('✅ 폰트 사용:', p)
            break
        except Exception:
            pass
if not font_title:
    raise SystemExit('한글 폰트 로드 실패')

# Icon finder
def find_icon():
    candidates = [
        ('assets/images', 'app_icon_rounded.png'),
        ('assets/images', 'app_icon.png'),
        ('assets/images', 'app_icon_512.png'),
        ('assets/store_graphics', 'app_icon_512.png'),
        ('web/icons', 'icon-512.png'),
    ]
    for base, name in candidates:
        p1 = os.path.join(ROOT, base, name)
        p2 = os.path.join(ALT_ROOT, base, name)
        if os.path.exists(p1): return p1
        if os.path.exists(p2): return p2
    return None

# Left icon container
icon_box = 320
icon_x = SAFE
icon_y = SAFE + 12
container = Image.new('RGBA', (icon_box, icon_box), (0,0,0,0))
cd = ImageDraw.Draw(container)
cd.rounded_rectangle([0,0,icon_box,icon_box], radius=48, fill=(255,255,255,240))
container = container.filter(ImageFilter.GaussianBlur(0.4))
img.paste(container, (icon_x, icon_y), container)

icon_path = find_icon()
if icon_path:
    icon = Image.open(icon_path).convert('RGBA')
    pad = 34
    target = icon_box - pad*2
    icon = icon.resize((target, target), Image.Resampling.LANCZOS)
    shadow = Image.new('RGBA', (target, target), (0,0,0,55))
    shadow = shadow.filter(ImageFilter.GaussianBlur(6))
    img.paste(shadow, (icon_x+pad+4, icon_y+pad+6), shadow)
    img.paste(icon, (icon_x+pad, icon_y+pad), icon)
else:
    draw.rounded_rectangle([icon_x+20,icon_y+20,icon_x+icon_box-20,icon_y+icon_box-20], radius=36, fill=(86,170,125))

# Title with Lite pill
title_main = '물주기 알림 '
Lite = 'Lite'
text_x = icon_x + icon_box + 56
text_y = SAFE + 24
# Main title
draw.text((text_x, text_y), title_main, font=font_title, fill=(36, 56, 46))
# Measure to place pill
main_w = draw.textbbox((0,0), title_main, font=font_title)[2]
# Pill background
pill_pad_x, pill_h = 18, font_title.size + 6
pill_w = draw.textbbox((0,0), Lite, font=font_title)[2] + pill_pad_x*2
pill_img = Image.new('RGBA', (pill_w, pill_h), (0,0,0,0))
pd = ImageDraw.Draw(pill_img)
pd.rounded_rectangle([0,0,pill_w,pill_h], radius=int(pill_h/2), fill=(58, 141, 96, 255))
# Slight highlight
pd.rounded_rectangle([1,1,pill_w-1,pill_h-1], radius=int(pill_h/2), outline=(255,255,255,30), width=2)
img.paste(pill_img, (text_x + main_w + 10, text_y - 6), pill_img)
# Pill text
pill_text_x = text_x + main_w + 10 + pill_pad_x
pill_text_y = text_y - 2
draw.text((pill_text_x, pill_text_y), Lite, font=font_title, fill=(255,255,255))

# Subtitle (short & crisp)
subtitle = '맞춤 주기 · 정확 알림 · D‑day'
sub_y = text_y + 100
draw.text((text_x, sub_y), subtitle, font=font_sub, fill=(70, 85, 78))

# Chips
chips = ['✓ 맞춤 주기', '✓ 정확 알림', '✓ D‑day 표시']
chip_y = sub_y + 60
chip_gap = 14
chip_h = 54
chip_pad_x = 22
cx = text_x
for label in chips:
    tw = draw.textbbox((0,0), label, font=font_badge)[2]
    bw = tw + chip_pad_x*2
    if cx + bw > WIDTH - SAFE:
        cx = text_x
        chip_y += chip_h + 10
    chip = Image.new('RGBA', (bw, chip_h), (0,0,0,0))
    cd2 = ImageDraw.Draw(chip)
    cd2.rounded_rectangle([0,0,bw,chip_h], radius=26, fill=(255,255,255,248))
    cd2.rounded_rectangle([2,2,bw,chip_h], radius=26, outline=(0,0,0,24), width=2)
    chip = chip.filter(ImageFilter.GaussianBlur(0.2))
    img.paste(chip, (cx, chip_y), chip)
    draw.text((cx + chip_pad_x, chip_y + (chip_h-font_badge.size)//2 - 1), label, font=font_badge, fill=(52, 66, 60))
    cx += bw + chip_gap

# Footer
footer = '무료 · 오프라인 · 개인정보 수집 없음'
draw.text((text_x, chip_y + chip_h + 28), footer, font=font_badge, fill=(92, 107, 99))

# Save
out_path = os.path.join(ROOT, 'assets', 'store_graphics', 'feature_graphic_premium.png')
os.makedirs(os.path.dirname(out_path), exist_ok=True)
img.save(out_path, 'PNG')
print('✅ 프리미엄 Feature Graphic 생성:', os.path.relpath(out_path, ROOT))
