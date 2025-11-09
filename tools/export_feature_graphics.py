#!/usr/bin/env python3
"""
Export the active feature graphic (assets/store_graphics/feature_graphic.png)
into additional formats for store uploads and web previews:
- feature_graphic.webp (lossless)
- feature_graphic.jpg (quality=95)
"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(__file__))
ASSETS_PRIMARY = os.path.join(ROOT, 'assets', 'store_graphics')
PNG_PATH = os.path.join(ASSETS_PRIMARY, 'feature_graphic.png')

if not os.path.exists(PNG_PATH):
    raise SystemExit('feature_graphic.png not found. Run generator or chooser first.')

img = Image.open(PNG_PATH).convert('RGB')
webp_path = os.path.join(ASSETS_PRIMARY, 'feature_graphic.webp')
jpg_path = os.path.join(ASSETS_PRIMARY, 'feature_graphic.jpg')

img.save(webp_path, 'WEBP', lossless=True)
img.save(jpg_path, 'JPEG', quality=95, optimize=True, progressive=True)

print('✅ Exported:')
print(' -', os.path.relpath(webp_path, ROOT))
print(' -', os.path.relpath(jpg_path, ROOT))
