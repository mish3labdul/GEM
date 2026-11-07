"""Assemble M34 Five-Product Contact Sheet with explicit provisional study banners.
"""
from PIL import Image, ImageDraw, ImageFont
import os

HERE = os.path.dirname(os.path.abspath(__file__))
M34_DIR = os.path.dirname(HERE)
RENDERS_DIR = os.path.join(M34_DIR, "renders")
CONTACT_DIR = os.path.join(M34_DIR, "contact_sheets")
OUT_SHEET = os.path.join(CONTACT_DIR, "M34_FIVE_PRODUCT_CONTACT_SHEET.png")

os.makedirs(CONTACT_DIR, exist_ok=True)

# Load fonts
try:
    font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 44)
    font_sub = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
    font_badge = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 20)
    font_caption = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 22)
    font_ar = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 26)
    font_meta = ImageFont.truetype("/System/Library/Fonts/SFNSMono.ttf", 16)
except Exception:
    font_title = font_sub = font_badge = font_caption = font_ar = font_meta = ImageFont.load_default()

SHEET_W = 2400
SHEET_H = 2650

sheet = Image.new("RGBA", (SHEET_W, SHEET_H), (18, 23, 29, 255)) # #12171D Ink
draw = ImageDraw.Draw(sheet)

# Header banner
draw.rectangle([(0, 0), (SHEET_W, 160)], fill=(12, 16, 21, 255))
draw.text((40, 24), "GEM™ — FIVE-PRODUCT HOSPITALITY PACKAGING & 3D VISUAL STUDY", fill=(255, 255, 255, 255), font=font_title)
draw.text((40, 80), "PROVISIONAL_EXPLORATORY_GEOMETRY — INTERNAL CGI STUDY — NOT OWNER-APPROVED PHYSICAL PACKAGING", fill=(235, 175, 75, 255), font=font_sub)
draw.text((40, 118), "Authorization: GEM-PKG-OWNER-20261107-005 | Bilingual Layout A (Jost + Noto Sans Arabic) | M15 Artwork Textures", fill=(188, 172, 167, 255), font=font_caption)

# 1. Main Lineup
lineup_path = os.path.join(RENDERS_DIR, "family_five_lineup.png")
if os.path.isfile(lineup_path):
    im_lineup = Image.open(lineup_path)
    # Scale lineup to width 2320 (height ~1305)
    target_w = 2320
    target_h = int(im_lineup.height * (target_w / im_lineup.width))
    im_lineup_resized = im_lineup.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Paste at (40, 180)
    sheet.paste(im_lineup_resized, (40, 180))
    draw.rectangle([(39, 179), (40 + target_w, 180 + target_h)], outline=(60, 70, 80, 255), width=2)
    
    caption_y = 180 + target_h + 12
    draw.text((40, caption_y), "Figure 1: Five-Product Hospitality Lineup on Studio Sweep (Hand Wash, Shampoo, Conditioner, Body Wash, Body Lotion) — 2000x1125 @ 96 spp Metal GPU", fill=(220, 220, 225, 255), font=font_caption)
else:
    caption_y = 600

# 2. Individual Heroes Row
hero_y = caption_y + 60
draw.text((40, hero_y), "INDIVIDUAL STUDIO HERO PREVIEWS (960x1200 @ 64 spp)", fill=(255, 255, 255, 255), font=font_sub)

prods = [
    ("hand_wash", "HAND WASH", "\uFEE6\uFEF3\uFEAA\uFEF4\uFEDF\uFE8D \uFEDD\uFEEE\uFEB4\uFECF", "studio_hand_wash.png", "PROVISIONAL (M34)"),
    ("shampoo", "SHAMPOO", "\uFEEE\uFE92\uFEE3\uFE8E\uFEB7", "studio_shampoo.png", "CANONICAL M27a/M28"),
    ("conditioner", "CONDITIONER", "\uFEE2\uFEB4\uFEE0\uFE91", "studio_conditioner.png", "CANONICAL M27a/M28"),
    ("body_wash", "BODY WASH", "\uFEE2\uFEB4\uFE9E\uFEDF\uFE8D \uFEDD\uFEEE\uFEB4\uFECF", "studio_body_wash.png", "PROVISIONAL (M34)"),
    ("body_lotion", "BODY LOTION", "\uFEE2\uFEB4\uFE9E\uFEDF\uFE8D \uFEE6\uFEB7\uFEEE\uFEDF", "studio_body_lotion.png", "PROVISIONAL (M34)")
]

col_w = 448
gap = 20
start_x = 40
card_top = hero_y + 40
card_h = 780

for i, (prod_key, name_en, name_ar, img_name, status_tag) in enumerate(prods):
    x = start_x + i * (col_w + gap)
    draw.rectangle([(x, card_top), (x + col_w, card_top + card_h)], fill=(20, 26, 33, 255), outline=(45, 55, 65, 255), width=1)
    
    img_path = os.path.join(RENDERS_DIR, img_name)
    if os.path.isfile(img_path):
        im_hero = Image.open(img_path)
        # Resize to fit inside 432 x 540
        thumb_w = 432
        thumb_h = int(im_hero.height * (thumb_w / im_hero.width))
        im_thumb = im_hero.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(im_thumb, (x + 8, card_top + 8))
        draw.rectangle([(x + 7, card_top + 7), (x + 8 + thumb_w, card_top + 8 + thumb_h)], outline=(35, 45, 55, 255), width=1)
        
    # Text block below thumb
    txt_y = card_top + 560
    draw.text((x + 16, txt_y), f"{name_en}", fill=(255, 255, 255, 255), font=font_badge)
    draw.text((x + 16, txt_y + 28), f"{name_ar}", fill=(200, 190, 185, 255), font=font_ar)
    
    # Status pill
    is_prov = "PROVISIONAL" in status_tag
    pill_col = (180, 120, 20, 255) if is_prov else (30, 140, 60, 255)
    draw.rounded_rectangle([(x + 16, txt_y + 72), (x + col_w - 16, txt_y + 104)], radius=4, fill=pill_col)
    badge_label = "EXPLORATORY CGI" if is_prov else "BASELINE GEOMETRY"
    draw.text((x + 28, txt_y + 77), badge_label, fill=(255, 255, 255, 255), font=font_badge)
    
    draw.text((x + 16, txt_y + 115), "Amber Glass • Satin Pump", fill=(160, 170, 180, 255), font=font_meta)
    draw.text((x + 16, txt_y + 138), "Bilingual Layout A (M15)", fill=(160, 170, 180, 255), font=font_meta)

# Footer banner
footer_y = SHEET_H - 90
draw.rectangle([(0, footer_y), (SHEET_W, SHEET_H)], fill=(10, 13, 17, 255))
draw.text((40, footer_y + 18), "INTERNAL CGI VISUAL STUDY ONLY — STRICTLY NOT PRODUCTION OR COMMERCIAL PHOTOGRAPHY — ALL DIMENSIONS PROVISIONAL (~204 mL NOMINAL)", fill=(240, 180, 80, 255), font=font_caption)
draw.text((40, footer_y + 48), "Packaging Track A Milestone M34 • Authorizations: GEM-PKG-OWNER-20261107-001 through -005 • All Rights Reserved", fill=(140, 145, 150, 255), font=font_meta)

sheet.save(OUT_SHEET, format="PNG", optimize=True)
print(f"Saved contact sheet: {OUT_SHEET} ({os.path.getsize(OUT_SHEET)} bytes)")
