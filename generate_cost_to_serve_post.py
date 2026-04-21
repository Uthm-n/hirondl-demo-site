from PIL import Image, ImageDraw, ImageFont

BASE = "/Users/uthman/Hirondl Website"
W, H = 1200, 628
PAD_X = 52

NAVY     = (16,  21,  53)
SMALT    = (26,  48, 153)
SKY      = (138, 197, 255)
WHITE    = (255, 255, 255)
DIV      = (69,  73,  97)
LEAK_CLR = (190,  55,  55)
LEAK_LBL = (220, 110, 110)
AMBER    = (255, 186,   8)
MID_BAR  = (45,  65, 130)

img  = Image.new("RGB", (W, H), NAVY)
draw = ImageDraw.Draw(img)

# ── HELPERS ───────────────────────────────────────────────────────────────────
def tw(text, font):
    return draw.textbbox((0, 0), text, font=font)[2]

def th_f(font):
    bb = draw.textbbox((0, 0), "Ag", font=font)
    return bb[3] - bb[1]

def hdiv(y, x1=PAD_X, x2=W - PAD_X):
    draw.line([(x1, y), (x2, y)], fill=DIV, width=1)

def vdiv(x, y1, y2):
    draw.line([(x, y1), (x, y2)], fill=DIV, width=1)

def draw_segs(segs, x, y):
    for text, color in segs:
        font = f_stat_hi if color == SKY else f_stat
        draw.text((x, y), text, font=font, fill=color)
        x += tw(text, font)

# ── FONTS ─────────────────────────────────────────────────────────────────────
TITLE = "DO YOU RECOVER YOUR REAL CUSTOMER COST?"
for sz in range(40, 14, -1):
    f_try = ImageFont.truetype(f"{BASE}/Montserrat-ExtraBold.ttf", sz)
    if tw(TITLE, f_try) <= W - 2 * PAD_X:
        f_hed = f_try
        break

f_tags   = ImageFont.truetype(f"{BASE}/Montserrat-Bold.ttf",      11)
f_sub    = ImageFont.truetype(f"{BASE}/Montserrat-Bold.ttf",       14)
f_stat   = ImageFont.truetype(f"{BASE}/Montserrat-Bold.ttf",       15)
f_stat_hi= ImageFont.truetype(f"{BASE}/Montserrat-ExtraBold.ttf",  15)
f_val    = ImageFont.truetype(f"{BASE}/Montserrat-ExtraBold.ttf",  12)
f_blbl   = ImageFont.truetype(f"{BASE}/Montserrat-Bold.ttf",        8)
f_leak   = ImageFont.truetype(f"{BASE}/Montserrat-Bold.ttf",        8)
f_leakamt= ImageFont.truetype(f"{BASE}/Montserrat-ExtraBold.ttf",  12)
f_quote  = ImageFont.truetype(f"{BASE}/Montserrat-Bold.ttf",       15)
f_brand  = ImageFont.truetype(f"{BASE}/Montserrat-Bold.ttf",       11)

# ── TOP SECTION ───────────────────────────────────────────────────────────────
y = 28
draw.text((PAD_X, y), "PRICING  ·  COST-TO-SERVE  ·  COMMERCIAL STRATEGY", font=f_tags, fill=WHITE)
y += th_f(f_tags) + 10
hdiv(y); y += 14

draw.text((PAD_X, y), TITLE, font=f_hed, fill=WHITE)
y += th_f(f_hed) + 8
draw.text((PAD_X, y),
          "The price waterfall most B2B businesses have never mapped.",
          font=f_sub, fill=WHITE)
y += th_f(f_sub) + 16
hdiv(y); y += 20

col_top = y

# ── LEFT COLUMN — key messages ────────────────────────────────────────────────
SPLIT    = 660
COL_GAP  = 32
RIGHT_X  = SPLIT + COL_GAP        # 692
RIGHT_W  = W - PAD_X - RIGHT_X    # 1200 - 52 - 692 = 456
BULLET_X = 38                     # arrows start further left

stats = [
    [("→ In most B2B companies, unrecovered cost-to-serve is worth ", WHITE), ("2–5%", SKY), (" of revenue.", WHITE)],
    [("→ ", WHITE), ("20–30%", SKY), (" of customers are unprofitable once full servicing costs are allocated.", WHITE)],
    [("→ Leaks: small orders, urgent shipments, ", WHITE), ("DSO creep", SKY), (", unpriced complexity.", WHITE)],
    [("→ DSO extending 30→60 days alone costs ", WHITE), ("1–2pp", SKY), (" of margin.", WHITE)],
    [("→ Total recoverable opportunity across all levers: typically ", WHITE), ("5pp+", SKY), (".", WHITE)],
]

ROW_H  = th_f(f_stat) + 52
stat_y = col_top
for segs in stats:
    draw_segs(segs, BULLET_X, stat_y)
    stat_y += ROW_H

left_bottom = stat_y - 4

# ── RIGHT COLUMN — price waterfall ────────────────────────────────────────────
# Chart label + key on the same row
draw.text((RIGHT_X, col_top), "PRICE WATERFALL · % OF LIST PRICE", font=f_blbl, fill=SKY)
key_text = "* pp = percentage points"
key_w = tw(key_text, f_blbl)
draw.text((RIGHT_X + RIGHT_W - key_w, col_top), key_text, font=f_blbl, fill=DIV)
chart_label_bottom = col_top + th_f(f_blbl) + 6

bars_data = [
    ("LIST\nPRICE",    100, None,          None),
    ("INVOICE\nPRICE",  86, "Discounts", "−14pp*"),
    ("NET\nREV.",       78, "Rebates",   "−8pp*"),
    ("AFTER\nFREIGHT",  71, "Freight",   "−7pp*"),
    ("AFTER\nCREDIT",   65, "Credit",    "−6pp*"),
    ("POCKET\nMARGIN",  56, "Servicing", "−9pp*"),
]
N = len(bars_data)

# Footer geometry (needed to set bar bottom)
logo_h       = 28
ly_logo      = H - 10 - logo_h           # 590
footer_div_y = ly_logo - 10              # 580

QUOTE_RESERVE = 38                        # space for quote below columns
BLBL_H  = 2 * (th_f(f_blbl) + 2) + 4    # ~26px for bar labels
bar_bottom_y = footer_div_y - 14 - BLBL_H - QUOTE_RESERVE   # ~502

BAR_AREA_H = bar_bottom_y - chart_label_bottom - 4
SCALE      = BAR_AREA_H / 100.0

# Bar geometry: pack 6 bars into RIGHT_W (~526px)
BAR_W = 44
GAP   = int((RIGHT_W - N * BAR_W) / (N - 1))   # auto-space gaps evenly

def bar_left(i):
    return RIGHT_X + i * (BAR_W + GAP)

for i, (lbl, val, leak_lbl, leak_amt) in enumerate(bars_data):
    x   = bar_left(i)
    top = bar_bottom_y - int(val * SCALE)
    col = SMALT if i == 0 else (AMBER if i == N - 1 else MID_BAR)

    # Leak section
    if i > 0:
        prev_val = bars_data[i - 1][1]
        prev_top = bar_bottom_y - int(prev_val * SCALE)
        draw.rectangle([x, prev_top, x + BAR_W, top], fill=LEAK_CLR)

        # Dashed connector
        px_right = bar_left(i - 1) + BAR_W
        dash = px_right
        while dash + 4 < x:
            draw.line([(dash, prev_top), (min(dash + 4, x), prev_top)], fill=DIV, width=1)
            dash += 8

        # Leak label: stacked in horizontal gap, centred on leak zone
        gap_cx       = px_right + GAP // 2
        leak_zone_cy = (prev_top + top) // 2

        if leak_lbl and leak_amt:
            lh = th_f(f_leak)
            ah = th_f(f_leakamt)
            stack   = lh + 2 + ah
            start_y = leak_zone_cy - stack // 2

            lw = tw(leak_lbl, f_leak)
            draw.text((gap_cx - lw // 2, start_y), leak_lbl, font=f_leak, fill=LEAK_LBL)
            aw = tw(leak_amt, f_leakamt)
            draw.text((gap_cx - aw // 2, start_y + lh + 2), leak_amt, font=f_leakamt, fill=LEAK_CLR)

    # Retained bar
    draw.rectangle([x, top, x + BAR_W, bar_bottom_y], fill=col)

    # Value label inside bar
    val_str = f"{val}%"
    if (bar_bottom_y - top) > th_f(f_val) + 10:
        vw = tw(val_str, f_val)
        draw.text((x + (BAR_W - vw) // 2, top + 5), val_str, font=f_val, fill=WHITE)

    # Bar label below baseline
    lbl_y = bar_bottom_y + 4
    for ll in lbl.split('\n'):
        lw = tw(ll, f_blbl)
        draw.text((x + (BAR_W - lw) // 2, lbl_y), ll, font=f_blbl, fill=WHITE)
        lbl_y += th_f(f_blbl) + 2

# Baseline rule
draw.line([(RIGHT_X, bar_bottom_y),
           (bar_left(N - 1) + BAR_W, bar_bottom_y)], fill=DIV, width=1)

right_bottom = bar_bottom_y + BLBL_H + 4

# ── VERTICAL DIVIDER ──────────────────────────────────────────────────────────
col_bottom = max(left_bottom, right_bottom)
vdiv(SPLIT, col_top, col_bottom + 8)

# ── QUOTE — full-width below columns ─────────────────────────────────────────
q_div_y = col_bottom + 12
hdiv(q_div_y)
q_y = q_div_y + 10
draw.text((PAD_X, q_y),
          '"The question to ask of every portfolio company: do you recover your real customer cost?"',
          font=f_quote, fill=WHITE)

# ── FOOTER ────────────────────────────────────────────────────────────────────
hdiv(footer_div_y)
logo_orig = Image.open(f"{BASE}/logo.png").convert("RGBA")
_, _, _, alpha = logo_orig.split()
logo_white = Image.new("RGBA", logo_orig.size, (255, 255, 255, 255))
logo_white.putalpha(alpha)
logo_w = int(logo_orig.width * logo_h / logo_orig.height)
logo_final = logo_white.resize((logo_w, logo_h), Image.LANCZOS)
img.paste(logo_final, (PAD_X, ly_logo), mask=logo_final.split()[3])

brand_text = "Commercial Transformation Partners  ·  Est. 2014"
brand_y    = ly_logo + (logo_h - th_f(f_brand)) // 2
draw.text((PAD_X + logo_w + 12, brand_y), brand_text, font=f_brand, fill=WHITE)

# ── SAVE ──────────────────────────────────────────────────────────────────────
out = f"{BASE}/hirondl-linkedin-post-cost-to-serve.jpg"
img.save(out, "JPEG", quality=95)
print(f"Saved  → {out}")
print(f"Title  → {sz}px  |  BAR_W={BAR_W}  GAP={GAP}")
print(f"col_top={col_top}  bar_bottom_y={bar_bottom_y}  SCALE={SCALE:.2f}")
print(f"q_div_y={q_div_y}  footer_div_y={footer_div_y}  gap={footer_div_y - (q_y + th_f(f_quote))}px")
