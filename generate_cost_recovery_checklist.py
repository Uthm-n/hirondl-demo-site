from PIL import Image, ImageDraw, ImageFont

BASE = "/Users/uthman/Hirondl Website"
W, H = 1200, 628
PAD_X = 52

NAVY  = (16,  21,  53)
SKY   = (138, 197, 255)
WHITE = (255, 255, 255)
DIV   = (69,  73,  97)

img  = Image.new("RGB", (W, H), NAVY)
draw = ImageDraw.Draw(img)

def divider(y):
    draw.line([(PAD_X, y), (W - PAD_X, y)], fill=DIV, width=1)

def tw(text, font):
    return draw.textbbox((0, 0), text, font=font)[2]

def th(font):
    bb = draw.textbbox((0, 0), "Ag", font=font)
    return bb[3] - bb[1]

# ── FONTS ─────────────────────────────────────────────────────────────────────
f_tags     = ImageFont.truetype(f"{BASE}/Montserrat-Bold.ttf",      11)
f_hed1     = ImageFont.truetype(f"{BASE}/Montserrat-ExtraBold.ttf", 38)
f_item_reg = ImageFont.truetype(f"{BASE}/Montserrat-Bold.ttf",      17)
f_item_hi  = ImageFont.truetype(f"{BASE}/Montserrat-ExtraBold.ttf", 17)
f_sub      = ImageFont.truetype(f"{BASE}/Montserrat-Bold.ttf",      17)
f_brand    = ImageFont.truetype(f"{BASE}/Montserrat-Bold.ttf",      11)

# Auto-size second headline line to fit one line
SUB_TITLE = "DO YOU RECOVER YOUR REAL CUSTOMER COST?"
for sz in range(32, 14, -1):
    f_hed2 = ImageFont.truetype(f"{BASE}/Montserrat-ExtraBold.ttf", sz)
    if tw(SUB_TITLE, f_hed2) <= W - 2 * PAD_X:
        break

# ── TAGS ──────────────────────────────────────────────────────────────────────
y = 32
draw.text((PAD_X, y), "TRANSACTIONAL PRICING  ·  MARGIN RECOVERY  ·  COMMERCIAL STRATEGY",
          font=f_tags, fill=WHITE)
y += th(f_tags) + 12
divider(y); y += 1 + 20

# ── HEADLINE ──────────────────────────────────────────────────────────────────
draw.text((PAD_X, y), "CEO CHECKLIST:", font=f_hed1, fill=WHITE)
y += th(f_hed1) + 8
draw.text((PAD_X, y), SUB_TITLE, font=f_hed2, fill=SKY)
y += th(f_hed2) + 10
divider(y); y += 1   # divider immediately after headline — no extra gap
div_y = y            # save divider bottom for spacing calc

# ── CHECKLIST ITEMS ───────────────────────────────────────────────────────────
CB  = 20    # checkbox size
GAP = 15    # gap between checkbox and text

logo_h       = 30
ly           = H - 12 - logo_h
footer_div_y = ly - 12
ITEM_H       = max(CB, th(f_item_reg) + 4)
N_ITEMS      = 5
SUB_H    = th(f_sub)
SUB_TEXT = "Five questions that reveal where margin is leaking undetected."

# Top section = 2×ITEM_GAP; items fill the rest with equal ITEM_GAP between/after
# (N_ITEMS + 2) × ITEM_GAP + N_ITEMS × ITEM_H = available
ITEM_GAP = (footer_div_y - 12 - div_y - N_ITEMS * ITEM_H) // (N_ITEMS + 2)

# First item starts exactly 2×ITEM_GAP below the divider
first_item_y = div_y + 2 * ITEM_GAP

# Centre the "subtitle + separator" block in the top section
BLOCK_H  = SUB_H + 5 + 1          # subtitle height + gap + 1px line
block_y  = div_y + (2 * ITEM_GAP - BLOCK_H) // 2   # vertically centred

# Draw subtitle left-aligned
draw.text((PAD_X, block_y), SUB_TEXT, font=f_sub, fill=WHITE)

# Separator line just below subtitle
sep_y = block_y + SUB_H + 5
draw.line([(PAD_X, sep_y), (W - PAD_X, sep_y)], fill=DIV, width=1)

y = first_item_y

items = [
    [("Can you identify which customers are profitable after ", WHITE), ("all servicing costs", SKY), (", not just COGS?", WHITE)],
    [("Are small orders, urgent shipments and freight costs ", WHITE), ("systematically recovered", SKY), (" in your contracts?", WHITE)],
    [("Do your credit terms reflect ", WHITE), ("actual DSO exposure", SKY), (", or are they set by relationship?", WHITE)],
    [("Are any customers receiving customisation or support ", WHITE), ("at no incremental charge", SKY), ("?", WHITE)],
    [("Have you set ", WHITE), ("repricing triggers", SKY), (" for when service complexity changes, not just input costs?", WHITE)],
]

for segments in items:
    # Checkbox
    draw.rectangle([PAD_X, y, PAD_X + CB, y + CB], outline=SKY, width=2)
    tx = PAD_X + CB + GAP
    ty = y + 1
    for text, color in segments:
        font = f_item_hi if color == SKY else f_item_reg
        draw.text((tx, ty), text, font=font, fill=color)
        tx += tw(text, font)
    y += max(CB, th(f_item_reg) + 4) + ITEM_GAP

# ── FOOTER ────────────────────────────────────────────────────────────────────
divider(footer_div_y)

logo_orig = Image.open(f"{BASE}/logo.png").convert("RGBA")
_, _, _, alpha = logo_orig.split()
logo_white = Image.new("RGBA", logo_orig.size, (255, 255, 255, 255))
logo_white.putalpha(alpha)
logo_w = int(logo_orig.width * logo_h / logo_orig.height)
logo_final = logo_white.resize((logo_w, logo_h), Image.LANCZOS)
img.paste(logo_final, (PAD_X, ly), mask=logo_final.split()[3])

brand_text = "Commercial Transformation Partners  ·  Est. 2014"
brand_y    = ly + (logo_h - th(f_brand)) // 2
draw.text((PAD_X + logo_w + 12, brand_y), brand_text, font=f_brand, fill=WHITE)

# ── SAVE ──────────────────────────────────────────────────────────────────────
out = f"{BASE}/hirondl-linkedin-post-cost-recovery-checklist.jpg"
img.save(out, "JPEG", quality=95)
print(f"Saved  → {out}")
print(f"Sub-title size: {sz}px  |  Checklist ends at y≈{y}")
