#!/usr/bin/env python3
"""
Generate multiple Play Store Feature Graphic variants (1024x500) so the user can choose.
Outputs:
  assets/store_graphics/feature_graphic_variant_a.png (Fresh green gradient + pills)
  assets/store_graphics/feature_graphic_variant_b.png (Minimal light, watermark silhouette)
  assets/store_graphics/feature_graphic_variant_c.png (Dark focus, high contrast)

Shared layout principles:
- Safe margins to prevent cropping
- Square icon container (no clipping)
- Korean fonts with rounded fallback if available
- Responsive wrapping of subtitle and badges
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

WIDTH, HEIGHT = 1024, 500
SAFE = 40
ICON_BOX = 320
BADGE_HEIGHT = 60
BADGE_PAD_X = 28
BADGE_GAP = 16

TITLE = '물주기 알림 Lite'
SUB = '식물 물주기 날짜를 계산하고 정확한 시간에 알려주는 간편한 물주기 도우미'
BADGES = ['맞춤 주기', '정확 알림', 'D-day 표시']
FOOTER = '무료 · 오프라인 · 개인정보 수집 없음'

# Font discovery (rounded preference)
FONT_CANDIDATES = [
    'assets/fonts/rounded_kr.ttf',
    '/Library/Fonts/NanumSquareRoundB.ttf',
    '/Library/Fonts/NanumSquareRoundR.ttf',
    '/Library/Fonts/NanumSquareRoundL.ttf',
    '/System/Library/Fonts/AppleSDGothicNeo.ttc',
]
font_title = font_sub = font_badge = None
for p in FONT_CANDIDATES:
    if os.path.exists(p):
        try:
            font_title = ImageFont.truetype(p, 78)
            font_sub = ImageFont.truetype(p, 34)
            font_badge = ImageFont.truetype(p, 26)
            print('✅ 폰트 사용:', p)
            break
        except Exception:
            pass
if not font_title:
    raise SystemExit('폰트 로드 실패: rounded_kr.ttf 또는 NanumSquareRound 설치 필요')

ROOT = os.path.dirname(os.path.dirname(__file__))
ALT_ROOT = os.path.dirname(ROOT)
def find_icon():
    candidates = [
        ('assets/images', 'app_icon_rounded.png'),  # Prefer rounded version
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
ICON_PATH = find_icon()
app_icon_img = Image.open(ICON_PATH).convert('RGBA') if ICON_PATH else None


def wrap_text(draw, text, font, max_width):
    words = text.split(' ')
    lines, line = [], ''
    for w in words:
        candidate = (line + ' ' + w).strip()
        width = draw.textbbox((0,0), candidate, font=font)[2]
        if width <= max_width:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = w
    if line:
        lines.append(line)
    return lines


def draw_icon_container(base: Image.Image, theme: str):
    icon_x = SAFE
    icon_y = SAFE + 6
    container = Image.new('RGBA', (ICON_BOX, ICON_BOX), (0,0,0,0))
    cd = ImageDraw.Draw(container)
    if theme == 'dark':
        cd.rounded_rectangle([0,0,ICON_BOX,ICON_BOX], radius=54, fill=(34,52,38,255))
    else:
        cd.rounded_rectangle([0,0,ICON_BOX,ICON_BOX], radius=54, fill=(255,255,255,235))
    container = container.filter(ImageFilter.GaussianBlur(0.4))
    base.paste(container, (icon_x, icon_y), container)
    if app_icon_img:
        pad = 38
        target = ICON_BOX - pad*2
        icon = app_icon_img.resize((target, target), Image.Resampling.LANCZOS)
        shadow = Image.new('RGBA', (target, target), (0,0,0,60))
        shadow = shadow.filter(ImageFilter.GaussianBlur(6))
        base.paste(shadow, (icon_x+pad+4, icon_y+pad+6), shadow)
        base.paste(icon, (icon_x+pad, icon_y+pad), icon)
    else:
        d = ImageDraw.Draw(base)
        d.rounded_rectangle([icon_x+20,icon_y+20,icon_x+ICON_BOX-20,icon_y+ICON_BOX-20], radius=40, fill=(80,160,120))
    return icon_x + ICON_BOX + 60, SAFE + 16  # text_x, text_y


def draw_badges(img: Image.Image, draw: ImageDraw.ImageDraw, start_x: int, start_y: int, text_color, bg_color, outline_color):
    x = start_x
    y = start_y
    for label in BADGES:
        badge_text = label
        tw = draw.textbbox((0,0), badge_text, font=font_badge)[2]
        bw = tw + BADGE_PAD_X*2
        if x + bw > WIDTH - SAFE:
            x = start_x
            y += BADGE_HEIGHT + 12
        badge_img = Image.new('RGBA', (bw, BADGE_HEIGHT), (0,0,0,0))
        bd = ImageDraw.Draw(badge_img)
        bd.rounded_rectangle([0,0,bw,BADGE_HEIGHT], radius=30, fill=bg_color)
        bd.rounded_rectangle([2,2,bw,BADGE_HEIGHT], radius=30, outline=outline_color, width=2)
        badge_img = badge_img.filter(ImageFilter.GaussianBlur(0.2))
        img.paste(badge_img, (x,y), badge_img)
        draw.text((x+BADGE_PAD_X, y + (BADGE_HEIGHT-font_badge.size)/2 -2), badge_text, font=font_badge, fill=text_color)
        x += bw + BADGE_GAP
    return y + BADGE_HEIGHT


def variant_a():
    # Fresh green gradient
    base = Image.new('RGB', (WIDTH, HEIGHT), (232,246,238))
    d = ImageDraw.Draw(base)
    # radial accents
    for center, radius, color in [((WIDTH*0.75, HEIGHT*0.35), 420, (198,236,210)), ((WIDTH*0.30, HEIGHT*0.65), 380, (210,240,222))]:
        cx, cy = center
        for r in range(int(radius), 0, -4):
            shade = tuple(int(color[i] + (232-color[i])*(r/radius)) for i in range(3))
            d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=shade)
    ov = Image.new('RGBA', (WIDTH, HEIGHT), (255,255,255,40))
    base.paste(ov, (0,0), ov)
    text_x, text_y = draw_icon_container(base, theme='light')
    d.text((text_x, text_y), TITLE, font=font_title, fill=(35,55,45))
    lines = wrap_text(d, SUB, font_sub, WIDTH - SAFE - text_x)
    yy = text_y + font_title.size + 20
    for ln in lines:
        d.text((text_x, yy), ln, font=font_sub, fill=(70,85,78))
        yy += font_sub.size + 6
    badges_bottom = draw_badges(base, d, text_x, yy + 12, (50,65,58), (255,255,255,250), (0,0,0,30))
    d.text((text_x, badges_bottom + 30), FOOTER, font=font_badge, fill=(85,100,92))
    return base


def variant_b():
    # Minimal light with watermark leaf silhouette
    base = Image.new('RGB', (WIDTH, HEIGHT), (245,248,245))
    d = ImageDraw.Draw(base)
    # Watermark silhouette
    wm = Image.new('RGBA', (WIDTH, HEIGHT), (0,0,0,0))
    wmd = ImageDraw.Draw(wm)
    wmd.polygon([(850,470),(780,180),(990,260)], fill=(180,200,185,60))
    wmd.ellipse([760,120,980,340], outline=(180,200,185,55), width=14)
    wm = wm.filter(ImageFilter.GaussianBlur(12))
    base.paste(wm, (0,0), wm)
    text_x, text_y = draw_icon_container(base, theme='light')
    d.text((text_x, text_y), TITLE, font=font_title, fill=(40,60,50))
    lines = wrap_text(d, SUB, font_sub, WIDTH - SAFE - text_x)
    yy = text_y + font_title.size + 16
    for ln in lines:
        d.text((text_x, yy), ln, font=font_sub, fill=(80,95,88))
        yy += font_sub.size + 6
    badges_bottom = draw_badges(base, d, text_x, yy + 18, (55,70,63), (255,255,255,255), (0,0,0,25))
    d.text((text_x, badges_bottom + 34), FOOTER, font=font_badge, fill=(95,110,103))
    return base


def variant_c():
    # Dark focus
    base = Image.new('RGB', (WIDTH, HEIGHT), (27,38,31))
    d = ImageDraw.Draw(base)
    # subtle vignette
    vignette = Image.new('L', (WIDTH, HEIGHT), 0)
    vg = ImageDraw.Draw(vignette)
    vg.ellipse([ -200, -50, WIDTH+200, HEIGHT+250], fill=255)
    vignette = vignette.filter(ImageFilter.GaussianBlur(180))
    tint = Image.new('RGBA', (WIDTH, HEIGHT), (46,72,56,145))
    base = Image.composite(tint, base.convert('RGBA'), vignette).convert('RGB')
    text_x, text_y = draw_icon_container(base, theme='dark')
    d.text((text_x, text_y), TITLE, font=font_title, fill=(230,244,236))
    lines = wrap_text(d, SUB, font_sub, WIDTH - SAFE - text_x)
    yy = text_y + font_title.size + 20
    for ln in lines:
        d.text((text_x, yy), ln, font=font_sub, fill=(198,215,205))
        yy += font_sub.size + 6
    badges_bottom = draw_badges(base, d, text_x, yy + 16, (230,244,236), (46,72,56,255), (230,244,236,80))
    d.text((text_x, badges_bottom + 34), FOOTER, font=font_badge, fill=(190,205,195))
    return base


def save(img: Image.Image, name: str):
    out_path = f'assets/store_graphics/{name}.png'
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, 'PNG')
    print('✅ 생성:', out_path)

if __name__ == '__main__':
    save(variant_a(), 'feature_graphic_variant_a')
    save(variant_b(), 'feature_graphic_variant_b')
    save(variant_c(), 'feature_graphic_variant_c')
    print('\n완료: 3개 변형 생성. 원하는 방향 알려주세요 (A/B/C 또는 추가 수정 지시).')
