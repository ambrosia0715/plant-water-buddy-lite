#!/usr/bin/env python3
"""
Resize and prepare screenshots for different app stores:
- Play Store (Android): 1080x2340 portrait (already generated)
- App Store iPhone: 1284x2778 (iPhone 14 Pro Max) portrait
- App Store iPad 12.9": 2048x2732 (iPad Pro 12.9" 3rd gen) portrait
- App Store iPad 11": 2064x2752 (iPad Pro 11" 3rd gen) portrait

Input: assets/store_graphics/screenshots/screenshot_*.png (1080x2340)
Output:
  - play_store/ (symlink or copy of originals)
  - app_store_iphone/ (1284x2778 resized)
  - app_store_ipad_129/ (2048x2732 resized with padding)
  - app_store_ipad_11/ (2064x2752 resized with padding)
"""
from PIL import Image
import os, shutil

ROOT = os.path.dirname(os.path.dirname(__file__))
SCREENSHOTS_DIR = os.path.join(ROOT, 'assets', 'store_graphics', 'screenshots')

# Store requirements
SPECS = {
    'play_store': (1080, 2340),       # 16:9 portrait, original
    'app_store_iphone': (1284, 2778),  # iPhone 14 Pro Max
    'app_store_ipad_129': (2048, 2732), # iPad Pro 12.9" 3rd gen
    'app_store_ipad_11': (2064, 2752),  # iPad Pro 11" 3rd gen
}

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def resize_with_fit(img: Image.Image, target_w: int, target_h: int, bg_color=(245, 250, 247)):
    """
    Resize image to fit within target dimensions while maintaining aspect ratio,
    then center on a background canvas of target size.
    """
    src_w, src_h = img.size
    src_ratio = src_w / src_h
    target_ratio = target_w / target_h
    
    if src_ratio > target_ratio:
        # Source is wider: fit width
        new_w = target_w
        new_h = int(target_w / src_ratio)
    else:
        # Source is taller: fit height
        new_h = target_h
        new_w = int(target_h * src_ratio)
    
    # Resize with high quality
    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # Create canvas and center
    canvas = Image.new('RGB', (target_w, target_h), bg_color)
    paste_x = (target_w - new_w) // 2
    paste_y = (target_h - new_h) // 2
    canvas.paste(resized, (paste_x, paste_y))
    
    return canvas

def process_screenshots():
    # Find all source screenshots (any PNG file in screenshots dir)
    source_files = sorted([
        f for f in os.listdir(SCREENSHOTS_DIR)
        if f.endswith('.png') and os.path.isfile(os.path.join(SCREENSHOTS_DIR, f))
    ])
    
    if not source_files:
        print('❌ 소스 스크린샷을 찾을 수 없습니다:', SCREENSHOTS_DIR)
        return
    
    print(f'📱 소스 스크린샷 {len(source_files)}개 발견\n')
    
    for store, (w, h) in SPECS.items():
        store_dir = os.path.join(SCREENSHOTS_DIR, store)
        ensure_dir(store_dir)
        print(f'📂 {store} ({w}x{h}):')
        
        for fname in source_files:
            src_path = os.path.join(SCREENSHOTS_DIR, fname)
            dst_path = os.path.join(store_dir, fname)
            
            if store == 'play_store':
                # Play Store: just copy original (already correct size)
                shutil.copy2(src_path, dst_path)
                print(f'  ✅ {fname} (복사)')
            else:
                # Other stores: resize with fit
                img = Image.open(src_path)
                resized = resize_with_fit(img, w, h)
                resized.save(dst_path, 'PNG', optimize=True)
                print(f'  ✅ {fname} (리사이즈 {w}x{h})')
        print()
    
    print('✅ 완료: 4개 스토어별 스크린샷 세트 생성')
    print(f'   - Play Store: {SCREENSHOTS_DIR}/play_store/')
    print(f'   - App Store iPhone: {SCREENSHOTS_DIR}/app_store_iphone/')
    print(f'   - App Store iPad 12.9": {SCREENSHOTS_DIR}/app_store_ipad_129/')
    print(f'   - App Store iPad 11": {SCREENSHOTS_DIR}/app_store_ipad_11/')

if __name__ == '__main__':
    process_screenshots()
