#!/usr/bin/env python3
"""
Generate Play Store screenshots (1080x2340 portrait) with simulated app UI.
Outputs:
  assets/store_graphics/screenshots/screenshot_1_home.png (식물 목록)
  assets/store_graphics/screenshots/screenshot_2_add.png (식물 추가)
  assets/store_graphics/screenshots/screenshot_3_detail.png (식물 상세)
  assets/store_graphics/screenshots/screenshot_4_notification.png (알림 화면)
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

W, H = 1080, 2340
BG = (245, 250, 247)
PRIMARY = (76, 175, 80)
CARD_BG = (255, 255, 255)
TEXT_DARK = (33, 37, 41)
TEXT_MID = (108, 117, 125)
STATUS_BAR_H = 100
APP_BAR_H = 140
SAFE_X = 40

ROOT = os.path.dirname(os.path.dirname(__file__))

# Font setup
FONT_PATHS = [
    '/System/Library/Fonts/AppleSDGothicNeo.ttc',
    '/System/Library/Fonts/Supplemental/AppleGothic.ttf',
]
font_title = font_body = font_caption = None
for p in FONT_PATHS:
    if os.path.exists(p):
        try:
            font_title = ImageFont.truetype(p, 64)
            font_body = ImageFont.truetype(p, 48)
            font_caption = ImageFont.truetype(p, 38)
            break
        except:
            pass
if not font_title:
    font_title = ImageFont.load_default()
    font_body = font_title
    font_caption = font_title

def draw_status_bar(d: ImageDraw.ImageDraw):
    """상태바 (시간, 배터리 등)"""
    d.rectangle([0, 0, W, STATUS_BAR_H], fill=(255, 255, 255))
    d.text((SAFE_X, STATUS_BAR_H//2 - 20), "오후 3:24", font=font_caption, fill=TEXT_DARK)
    d.text((W - SAFE_X - 140, STATUS_BAR_H//2 - 20), "100% 📶", font=font_caption, fill=TEXT_DARK)

def draw_app_bar(d: ImageDraw.ImageDraw, title: str):
    """앱바 (타이틀)"""
    d.rectangle([0, STATUS_BAR_H, W, STATUS_BAR_H + APP_BAR_H], fill=PRIMARY)
    d.text((SAFE_X, STATUS_BAR_H + APP_BAR_H//2 - 30), title, font=font_title, fill=(255, 255, 255))

def draw_plant_card(img: Image.Image, d: ImageDraw.ImageDraw, y: int, name: str, days: str, water_date: str, emoji: str):
    """식물 카드 UI"""
    card_h = 200
    card_x = SAFE_X
    card_w = W - SAFE_X * 2
    # 카드 배경
    card = Image.new('RGBA', (card_w, card_h), CARD_BG)
    cd = ImageDraw.Draw(card)
    cd.rounded_rectangle([0, 0, card_w, card_h], radius=24, fill=CARD_BG)
    cd.rounded_rectangle([2, 2, card_w, card_h], radius=24, outline=(220, 220, 220), width=3)
    card = card.filter(ImageFilter.GaussianBlur(0.3))
    img.paste(card, (card_x, y), card)
    # 아이콘
    d.ellipse([card_x + 30, y + 50, card_x + 130, y + 150], fill=(PRIMARY[0]+30, PRIMARY[1]+30, PRIMARY[2]+30))
    d.text((card_x + 55, y + 70), emoji, font=font_title, fill=TEXT_DARK)
    # 텍스트
    d.text((card_x + 160, y + 50), name, font=font_body, fill=TEXT_DARK)
    d.text((card_x + 160, y + 110), f"D-{days}  {water_date}", font=font_caption, fill=TEXT_MID)

def screenshot_1_home():
    """홈 화면: 식물 목록"""
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    draw_status_bar(d)
    draw_app_bar(d, "물주기 알림 Lite")
    y = STATUS_BAR_H + APP_BAR_H + 60
    plants = [
        ("몬스테라", "2", "4월 12일", "🌿"),
        ("다육이", "5", "4월 15일", "🌵"),
        ("장미", "1", "4월 11일", "🌹"),
    ]
    for name, days, date, emoji in plants:
        draw_plant_card(img, d, y, name, days, date, emoji)
        y += 230
    # FAB 버튼
    fab_x = W - 100 - SAFE_X
    fab_y = H - 120 - SAFE_X
    d.ellipse([fab_x, fab_y, fab_x + 140, fab_y + 140], fill=PRIMARY)
    d.text((fab_x + 40, fab_y + 30), "+", font=ImageFont.truetype(FONT_PATHS[0], 90) if os.path.exists(FONT_PATHS[0]) else font_title, fill=(255, 255, 255))
    return img

def screenshot_2_add():
    """식물 추가 화면"""
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    draw_status_bar(d)
    draw_app_bar(d, "식물 추가")
    y = STATUS_BAR_H + APP_BAR_H + 80
    # 입력 필드들
    fields = [
        ("이름", "장미"),
        ("물주기 주기", "7일"),
        ("알림 시간", "오전 9시"),
    ]
    for label, placeholder in fields:
        d.text((SAFE_X, y), label, font=font_caption, fill=TEXT_MID)
        y += 60
        d.rounded_rectangle([SAFE_X, y, W - SAFE_X, y + 100], radius=16, fill=CARD_BG, outline=(200, 200, 200), width=2)
        d.text((SAFE_X + 30, y + 30), placeholder, font=font_body, fill=TEXT_DARK)
        y += 140
    # 저장 버튼
    btn_y = H - 250
    d.rounded_rectangle([SAFE_X + 100, btn_y, W - SAFE_X - 100, btn_y + 100], radius=50, fill=PRIMARY)
    d.text((W//2 - 60, btn_y + 28), "저장", font=font_title, fill=(255, 255, 255))
    return img

def screenshot_3_detail():
    """식물 상세 화면"""
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    draw_status_bar(d)
    draw_app_bar(d, "몬스테라")
    y = STATUS_BAR_H + APP_BAR_H + 80
    # 큰 아이콘
    icon_size = 240
    icon_x = W//2 - icon_size//2
    d.ellipse([icon_x, y, icon_x + icon_size, y + icon_size], fill=(PRIMARY[0]+40, PRIMARY[1]+40, PRIMARY[2]+40))
    d.text((icon_x + 60, y + 50), "🌿", font=ImageFont.truetype(FONT_PATHS[0], 120) if os.path.exists(FONT_PATHS[0]) else font_title, fill=TEXT_DARK)
    y += icon_size + 80
    # 정보
    info = [
        ("다음 물주기", "D-2 (4월 12일)"),
        ("물주기 주기", "7일마다"),
        ("알림 시간", "오전 9시"),
        ("메모", "밝은 곳에 두기"),
    ]
    for label, value in info:
        d.text((SAFE_X + 40, y), label, font=font_caption, fill=TEXT_MID)
        y += 55
        d.text((SAFE_X + 40, y), value, font=font_body, fill=TEXT_DARK)
        y += 90
    return img

def screenshot_4_notification():
    """알림 화면 (notification bar expanded)"""
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    draw_status_bar(d)
    # 알림 패널
    panel_h = 600
    d.rectangle([0, STATUS_BAR_H, W, STATUS_BAR_H + panel_h], fill=(250, 250, 250))
    d.text((SAFE_X, STATUS_BAR_H + 40), "알림", font=font_title, fill=TEXT_DARK)
    # 알림 카드
    notif_y = STATUS_BAR_H + 140
    notif_h = 200
    d.rounded_rectangle([SAFE_X, notif_y, W - SAFE_X, notif_y + notif_h], radius=20, fill=CARD_BG, outline=(220, 220, 220), width=2)
    d.text((SAFE_X + 30, notif_y + 30), "🌿 물주기 알림", font=font_body, fill=TEXT_DARK)
    d.text((SAFE_X + 30, notif_y + 90), "몬스테라에게 물을 줄 시간이에요!", font=font_caption, fill=TEXT_MID)
    d.text((SAFE_X + 30, notif_y + 140), "오전 9:00", font=font_caption, fill=(150, 150, 150))
    # 배경 흐림
    bg = Image.new('RGBA', (W, H), (0, 0, 0, 100))
    img.paste(bg, (0, STATUS_BAR_H + panel_h), bg)
    return img

def main():
    out_dir = os.path.join(ROOT, 'assets', 'store_graphics', 'screenshots')
    os.makedirs(out_dir, exist_ok=True)
    screens = [
        (screenshot_1_home, 'screenshot_1_home.png'),
        (screenshot_2_add, 'screenshot_2_add.png'),
        (screenshot_3_detail, 'screenshot_3_detail.png'),
        (screenshot_4_notification, 'screenshot_4_notification.png'),
    ]
    for func, filename in screens:
        img = func()
        path = os.path.join(out_dir, filename)
        img.save(path, 'PNG')
        print(f'✅ 생성: {os.path.relpath(path, ROOT)}')
    print('\n완료: Play Store 스크린샷 4개 생성됨 (1080x2340)')

if __name__ == '__main__':
    main()
