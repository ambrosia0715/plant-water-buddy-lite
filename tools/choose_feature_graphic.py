#!/usr/bin/env python3
"""
Choose one of the generated feature graphics as the default:
Usage:
  python3 tools/choose_feature_graphic.py [a|b|c|v2]
Default picks 'b'. Copies the chosen file to assets/store_graphics/feature_graphic.png
"""
import os, sys, shutil

ROOT = os.path.dirname(os.path.dirname(__file__))  # .../plant_water_buddy_lite
ASSETS_PRIMARY = os.path.join(ROOT, 'assets', 'store_graphics')
# Some runs may have generated assets at repo root due to different CWD
ASSETS_ALT = os.path.join(os.path.dirname(ROOT), 'assets', 'store_graphics')

def candidate_path(name: str):
  p1 = os.path.join(ASSETS_PRIMARY, name)
  if os.path.exists(p1):
    return p1
  p2 = os.path.join(ASSETS_ALT, name)
  if os.path.exists(p2):
    return p2
  return p1  # default to primary for error display

mapping = {
  'a': candidate_path('feature_graphic_variant_a.png'),
  'b': candidate_path('feature_graphic_variant_b.png'),
  'c': candidate_path('feature_graphic_variant_c.png'),
  'v2': candidate_path('feature_graphic_v2.png'),
  'premium': candidate_path('feature_graphic_premium.png'),
}

choice = (sys.argv[1] if len(sys.argv) > 1 else 'b').lower()
src = mapping.get(choice)
if not src or not os.path.exists(src):
    print('❌ 선택한 파일이 없습니다:', src)
    print('사용법: python3 tools/choose_feature_graphic.py [a|b|c|v2]')
    sys.exit(1)

dst = os.path.join(ASSETS_PRIMARY, 'feature_graphic.png')
os.makedirs(ASSETS_PRIMARY, exist_ok=True)
shutil.copyfile(src, dst)
print('✅ 기본 Feature Graphic으로 설정됨:', os.path.relpath(dst, ROOT))
