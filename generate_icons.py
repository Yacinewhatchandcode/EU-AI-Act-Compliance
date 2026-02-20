"""Generate proper PWA icons (192x192 and 512x512) using Pillow."""
import math
from PIL import Image, ImageDraw, ImageFont

def make_icon(size, path):
    img = Image.new('RGBA', (size, size), (10, 14, 26, 255))
    d = ImageDraw.Draw(img)
    cx, cy = size//2, int(size*0.42)
    r = int(size * 0.26)

    # Outer ring
    d.ellipse([cx-r-2, cy-r-2, cx+r+2, cy+r+2], outline=(59,130,246,80), width=max(1, size//80))

    # 12 EU stars
    star_r = int(size * 0.22)
    star_sz = max(3, int(size * 0.025))
    for i in range(12):
        angle = math.radians(i * 30 - 90)
        sx = cx + int(star_r * math.cos(angle))
        sy = cy + int(star_r * math.sin(angle))
        d.ellipse([sx-star_sz, sy-star_sz, sx+star_sz, sy+star_sz], fill=(245, 158, 11, 255))

    # Checkmark
    lw = max(3, size//30)
    p1 = (int(cx - r*0.35), cy)
    p2 = (int(cx - r*0.05), int(cy + r*0.35))
    p3 = (int(cx + r*0.45), int(cy - r*0.3))
    d.line([p1, p2, p3], fill=(16, 185, 129, 255), width=lw, joint='curve')

    # Text
    txt_y = int(size * 0.72)
    try:
        font = ImageFont.truetype("arial.ttf", max(10, size//14))
    except:
        font = ImageFont.load_default()
    d.text((cx, txt_y), "AI ACT", fill=(148, 163, 184, 255), font=font, anchor="mt")

    # Subtitle
    try:
        sfont = ImageFont.truetype("arial.ttf", max(8, size//22))
    except:
        sfont = ImageFont.load_default()
    d.text((cx, txt_y + max(14, size//10)), "COMPLIANCE", fill=(100, 116, 139, 200), font=sfont, anchor="mt")

    img.save(path, 'PNG')
    print(f"  ✅ {path} ({size}x{size})")

make_icon(192, r"C:\Users\Mr Robot\YBE\web\icon-192.png")
make_icon(512, r"C:\Users\Mr Robot\YBE\web\icon-512.png")
make_icon(180, r"C:\Users\Mr Robot\YBE\web\apple-touch-icon.png")

# Maskable icon (with safe zone padding)
img = Image.new('RGBA', (512,512), (10,14,26,255))
d = ImageDraw.Draw(img)
# Fill with blue gradient circle background
for ri in range(200, 0, -1):
    alpha = int(30 + (200-ri)*0.3)
    d.ellipse([256-ri, 220-ri, 256+ri, 220+ri], fill=(59,130,246,min(alpha,60)))
# Draw stars and check on top
cx, cy, r = 256, 210, 110
star_r, star_sz = 95, 12
for i in range(12):
    angle = math.radians(i*30-90)
    sx = cx + int(star_r * math.cos(angle))
    sy = cy + int(star_r * math.sin(angle))
    d.ellipse([sx-star_sz, sy-star_sz, sx+star_sz, sy+star_sz], fill=(245,158,11,255))
d.line([(218,210),(248,245),(300,180)], fill=(16,185,129,255), width=14, joint='curve')
try:
    f = ImageFont.truetype("arial.ttf", 36)
except:
    f = ImageFont.load_default()
d.text((256, 360), "AI ACT", fill=(148,163,184,255), font=f, anchor="mt")
img.save(r"C:\Users\Mr Robot\YBE\web\icon-maskable-512.png", 'PNG')
print("  ✅ icon-maskable-512.png (512x512)")
print("\n✅ All icons generated!")
