"""Generate 10 candidate images for make.fun news-image-20261119.

All facts come from the verified 2026-11-19 story list in the task brief.
No invented facts or figures. All text is drawn programmatically (PIL).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from newsart import C, font, flag, icon

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "candidates")
os.makedirs(OUT, exist_ok=True)

DATE = "THURSDAY, NOVEMBER 19, 2026"

S1H = "TRUMP, XI & PUTIN HOLD FIRST-EVER TRILATERAL SUMMIT"
S1B = ("The US, Chinese and Russian leaders meet in Shenzhen, on the sidelines of APEC. "
       "They issue a four-point 'Declaration toward Peace' on UN reform, oil, the ICC and "
       "nuclear risk, but no deal on Ukraine or Iran. Xi greeted Trump at the airport; "
       "Xi's meeting with Putin was their 50th.")
S2H = "IRAN WIDENS ATTACKS ON GULF NEIGHBOURS"
S2B = ("Iran fires drones at a US base in Kuwait and Bahrain; both say they were stopped. "
       "Three tankers afire near Hormuz.")
S3H = "ISRAEL LAUNCHES GROUND OPERATION IN CENTRAL GAZA"
S3B = "A one-day operation in central Gaza ends Thursday; residents flee the fighting."
S4H = "DEMOCRATS NOMINATE JEFFRIES FOR HOUSE SPEAKER"
S4B = ("Hakeem Jeffries is set to become the first African-American Speaker after "
       "Democrats sweep the midterms, taking the Senate 56-44.")
S5H = "ANTHROPIC'S IPO BREAKS ALL RECORDS"
S5B = ("The AI company raises $81 billion, the largest IPO ever, topping SpaceX's "
       "$75 billion. Shares jump 17% on debut.")
S6H = "GTA VI LAUNCHES WORLDWIDE"
S6B = "'Grand Theft Auto VI' goes on sale around the world to near-perfect reviews."
S7H = "WORLD COURT: MYANMAR COMMITTED GENOCIDE"
S7B = ("In a historic first, the court finds Myanmar guilty of genocide and orders "
       "reparations for the Rohingya.")
S8H = "ETHIOPIA-ERITREA CLASHES RAISE WAR FEARS"
S8B = "Fighting between Ethiopia and Eritrea raises fears of a return to full-scale war."

M1 = "M5.7 earthquake strikes Kumamoto, Japan - no tsunami warning"
M2 = "Voyager 1 becomes the first spacecraft to reach one light-day from Earth"
M3 = "Van Gogh painting sells for a record $190.4 million"
M4 = "South Korea holds its national college entrance exam under strict anti-cheating curbs"

INK = (20, 18, 14)
PAPER = (247, 242, 231)
RED = (179, 35, 42)
GREY = (92, 88, 80)


def save(c, name):
    p = os.path.join(OUT, name)
    c.finish(p)
    print("wrote", name)


# ================================================================ cand 01
def cand01():
    """Classic broadsheet front page."""
    c = C(PAPER)
    c.rect(28, 22, 968, 3, fill=INK)
    c.rect(28, 31, 968, 1, fill=INK)
    c.text(512, 42, "THE WORLD TODAY", "serif_blk", 82, INK, anchor="ma")
    c.text(512, 138, "THE DAY'S NEWS IN ONE PICTURE", "sans_b", 23, GREY, anchor="ma")
    c.rect(28, 176, 968, 48, fill=INK)
    c.text(512, 186, DATE, "sans_b", 32, (255, 255, 255), anchor="ma")
    # hero
    c.text(48, 240, "SHENZHEN, CHINA - ON THE SIDELINES OF APEC", "sans_b", 22, RED)
    y = c.para(48, 266, S1H, "serif_xb", 42, 928, INK, leading=1.12)
    fx = 48
    for nm in ("us", "cn", "ru"):
        flag(c, nm, fx, y + 6, 152, 100)
        fx += 172
    c.text(fx + 4, y + 14, "USA", "sans_b", 21, GREY)
    c.text(fx + 4, y + 42, "CHINA", "sans_b", 21, GREY)
    c.text(fx + 4, y + 70, "RUSSIA", "sans_b", 21, GREY)
    y = c.para(48, y + 120, "The US, Chinese and Russian leaders meet in Shenzhen, on the sidelines "
                            "of APEC. On the agenda: nuclear arms control, the Ukraine war and Iran. "
                            "Xi greeted Trump at the airport; Xi's meeting with Putin was their 50th.",
               "serif", 23, 928, INK, leading=1.28)
    c.rect(28, y + 6, 968, 2, fill=INK)
    # two columns
    top = y + 22
    colw = 452
    S2S = ("Strikes hit a US air base in Kuwait and targets in Bahrain, home of the US Fifth "
           "Fleet. Gulf states repel Iranian drone attacks; three tankers catch fire after "
           "hitting mines east of Hormuz.")
    S4S = ("Hakeem Jeffries is set to become the first African-American Speaker after Democrats "
           "sweep the midterms, taking the Senate 56-44.")
    S5S = ("The AI company raises a reported $107 billion, topping SpaceX's record debut. "
           "Shares begin trading on Nasdaq as ANT.")
    ly = top
    c.text(48, ly, "THE GULF", "sans_b", 19, RED)
    ly = c.para(48, ly + 24, S2H, "sans_xb", 26, colw, INK, leading=1.14)
    ly = c.para(48, ly + 3, S2S, "serif", 20, colw, INK, leading=1.26)
    ly += 12
    c.text(48, ly, "MIDDLE EAST", "sans_b", 19, RED)
    ly = c.para(48, ly + 24, S3H, "sans_xb", 26, colw, INK, leading=1.14)
    ly = c.para(48, ly + 3, S3B, "serif", 20, colw, INK, leading=1.26)
    ry = top
    rx = 524
    c.text(rx, ry, "WASHINGTON", "sans_b", 19, RED)
    ry = c.para(rx, ry + 24, S4H, "sans_xb", 26, colw, INK, leading=1.14)
    ry = c.para(rx, ry + 3, S4S, "serif", 20, colw, INK, leading=1.26)
    ry += 12
    c.text(rx, ry, "BUSINESS", "sans_b", 19, RED)
    ry = c.para(rx, ry + 24, S5H, "sans_xb", 26, colw, INK, leading=1.14)
    ry = c.para(rx, ry + 3, S5S, "serif", 20, colw, INK, leading=1.26)
    c.line([(512, top), (512, max(ly, ry))], GREY, 1)
    # bottom strip
    by = max(ly, ry) + 14
    c.rect(28, by, 968, 2, fill=INK)
    c.text(48, by + 10, "ALSO TODAY:", "sans_b", 21, RED)
    c.para(206, by + 10, "M5.7 quake strikes Kumamoto, Japan - no tsunami warning  ·  Voyager 1 "
                         "reaches one light-day from Earth  ·  Van Gogh sells for a record $190.4M",
           "sans", 20, 774, INK, leading=1.28)
    save(c, "cand01.png")


# ================================================================ cand 02
def cand02():
    """Dark magazine cover."""
    BG = (13, 21, 38)
    CYAN = (55, 200, 232)
    YEL = (255, 210, 63)
    WHITE = (245, 247, 250)
    MUT = (168, 182, 200)
    c = C(BG)
    c.text(48, 36, "ONE DAY", "disp_blk", 74, WHITE)
    c.text(48, 122, "THE WORLD IN ONE PICTURE", "sans_b", 26, CYAN)
    c.rrect(48, 168, 620, 56, 8, fill=YEL)
    c.text(68, 180, DATE, "sans_b", 33, (13, 21, 38))
    # hero
    c.rrect(48, 248, 928, 300, 14, fill=(22, 34, 58), outline=(55, 200, 232), ow=2)
    fx = 76
    for nm in ("us", "cn", "ru"):
        flag(c, nm, fx, 276, 180, 120)
        fx += 200
    c.text(692, 292, "FIRST", "disp_blk", 44, YEL)
    c.text(692, 340, "EVER", "disp_blk", 44, YEL)
    c.para(76, 408, S1H, "disp_xb", 32, 872, WHITE, leading=1.12)
    c.para(76, 488, "US, Chinese and Russian leaders meet in Shenzhen (APEC sidelines). "
                    "Agenda: nuclear arms control, Ukraine, Iran. Xi's meeting with Putin was their 50th.",
           "sans", 22, 872, MUT, leading=1.3)
    # 2x2 chips
    chips = [
        ("missile", (255, 77, 94), S2H, "Kuwait base & Bahrain hit; 3 tankers burn near Hormuz"),
        ("dome", CYAN, "DEMOCRATS PICK JEFFRIES FOR SPEAKER", "First African-American Speaker; Senate flips 56-44"),
        ("chart", (80, 220, 140), S5H, "Reported $107B raised - biggest IPO ever; Nasdaq: ANT"),
        ("controller", (200, 120, 255), S6H, "On sale worldwide to near-perfect reviews"),
    ]
    pos = [(48, 572), (512, 572), (48, 756), (512, 756)]
    for (ic, colr, h, b), (px, py) in zip(chips, pos):
        c.rrect(px, py, 464, 168, 12, fill=(22, 34, 58))
        c.rect(px, py + 10, 8, 148, fill=colr)
        icon(c, ic, px + 26, py + 44, 76, colr)
        hend = c.para(px + 122, py + 16, h, "sans_b", 23, 326, WHITE, leading=1.14)
        c.para(px + 122, max(py + 84, hend + 4), b, "sans", 20, 326, MUT, leading=1.25)
    c.para(48, 946, "ALSO: " + S7H + "  ·  " + S8H + "  ·  " + M1,
           "sans_b", 20, 928, CYAN, leading=1.25)
    save(c, "cand02.png")


# ================================================================ cand 03
def cand03():
    """Panel grid with hero."""
    BG = (238, 241, 245)
    SLATE = (30, 41, 59)
    c = C(BG)
    c.rect(0, 0, 1024, 118, fill=SLATE)
    c.text(40, 22, "THE WORLD ON", "disp_b", 30, (148, 184, 220))
    c.text(40, 52, DATE, "disp_xb", 42, (255, 255, 255))
    c.text(984, 40, "ONE DAY\nONE PICTURE", "sans_b", 22, (148, 184, 220), anchor="ra")
    # hero panel
    c.rrect(32, 138, 960, 252, 12, fill=(255, 255, 255))
    c.rect(32, 138, 960, 10, fill=(197, 48, 49))
    fx = 60
    for nm in ("us", "cn", "ru"):
        flag(c, nm, fx, 168, 132, 88)
        fx += 148
    c.text(524, 178, "SHENZHEN · APEC SIDELINES", "sans_b", 21, (197, 48, 49))
    c.para(524, 204, "FIRST-EVER US-CHINA-RUSSIA SUMMIT", "disp_xb", 31, 440, SLATE, leading=1.12)
    c.para(60, 278, "Trump, Xi and Putin meet in Shenzhen. They issue a four-point 'Declaration "
                    "toward Peace' on UN reform, oil, the ICC and nuclear risk, but no deal on "
                    "Ukraine or Iran. Xi greeted Trump at the airport; the Xi-Putin meeting was their 50th.",
           "sans", 22, 904, (51, 65, 85), leading=1.3)
    panels = [
        ("missile", (197, 48, 49), S2H, "Iran fires drones at a US base in Kuwait and Bahrain; both say they were stopped. Three tankers afire near Hormuz."),
        ("burst", (217, 119, 6), S3H, "A one-day operation in central Gaza ends Thursday; residents flee the fighting."),
        ("dome", (37, 99, 235), S4H, "Hakeem Jeffries, set to be the first African-American Speaker; Democrats also take the Senate 56-44."),
        ("chart", (5, 150, 105), S5H, "$81 billion raised, the largest IPO ever, topping SpaceX's $75 billion. Shares jump 17% on debut."),
        ("controller", (124, 58, 237), S6H, "'Grand Theft Auto VI' goes on sale worldwide to near-perfect reviews."),
        ("scales", (13, 148, 136), S7H, "In a historic first, the court finds Myanmar guilty of genocide and orders reparations for the Rohingya."),
    ]
    pw, ph = 468, 168
    for i, (ic, colr, h, b) in enumerate(panels):
        px = 32 + (i % 2) * (pw + 24)
        py = 410 + (i // 2) * (ph + 16)
        c.rrect(px, py, pw, ph, 10, fill=(255, 255, 255))
        c.rect(px, py, pw, 8, fill=colr)
        icon(c, ic, px + 20, py + 52, 62, colr)
        c.para(px + 100, py + 18, h, "sans_b", 22, 348, SLATE, leading=1.14)
        c.para(px + 100, py + 82, b, "sans", 18, 348, (71, 85, 105), leading=1.24)
    fy = 410 + 3 * (ph + 16) + 2
    c.para(32, fy, "ALSO TODAY:  " + S8H + "  ·  " + M2, "sans_b", 20, 960, SLATE, leading=1.25)
    save(c, "cand03.png")


# ================================================================ cand 04
def cand04():
    """Ranked timeline."""
    BG = (250, 246, 238)
    c = C(BG)
    c.text(56, 34, "19 NOVEMBER 2026", "disp_blk", 76, (26, 26, 26))
    c.text(58, 124, "THURSDAY - THE DAY'S BIGGEST STORIES, RANKED", "sans_b", 26, RED)
    c.rect(56, 168, 912, 3, fill=(26, 26, 26))
    items = [
        ("SHENZHEN", S1H, "US, China and Russia's leaders meet at APEC sidelines: arms control, Ukraine, Iran. Xi-Putin talks: their 50th."),
        ("THE GULF", S2H, "US base in Kuwait and Bahrain targets hit; drones repelled; three tankers burn after mines near Hormuz."),
        ("GAZA", S3H, "Israeli forces move into central Gaza as residents flee."),
        ("WASHINGTON", S4H, "Hakeem Jeffries to be first African-American Speaker; Democrats take the Senate 56-44."),
        ("NEW YORK", S5H, "Reported $107B raise tops SpaceX's record debut; Nasdaq ticker ANT."),
        ("WORLDWIDE", S6H, "'Grand Theft Auto VI' on sale to near-perfect reviews."),
        ("THE HAGUE", S7H, "ICJ delivers its ruling in Myanmar's Rohingya genocide case."),
        ("HORN OF AFRICA", S8H, "Clashes raise fears of a return to full-scale war."),
    ]
    y = 190
    x0 = 108
    ys = []
    for i, (tag, h, b) in enumerate(items):
        ys.append(y)
        c.text(168, y - 2, tag, "sans_b", 18, RED)
        c.para(168, y + 19, h, "sans_xb", 24, 800, (26, 26, 26), leading=1.1)
        y = c.para(168, y + 50, b, "sans", 19, 800, (80, 74, 66), leading=1.2) + 13
    c.line([(x0, ys[0] + 12), (x0, ys[-1] + 12)], (200, 190, 170), 3)
    for i, yy in enumerate(ys):
        c.ellipse(x0 - 21, yy + 2, 42, 42, fill=RED if i == 0 else (26, 26, 26))
        c.text(x0, yy + 9, str(i + 1), "sans_b", 24, (255, 255, 255), anchor="ma")
    c.rect(56, y + 2, 912, 2, fill=(26, 26, 26))
    c.para(56, y + 12, "ALSO: " + M1 + "  ·  " + M3, "sans_b", 18, 912, (80, 74, 66), leading=1.25)
    save(c, "cand04.png")


# ================================================================ cand 05
def _in_poly(lon, lat, poly):
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > lat) != (yj > lat)) and (lon < (xj - xi) * (lat - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside


def _in_ellipse(lon, lat, clon, clat, rx, ry):
    return ((lon - clon) / rx) ** 2 + ((lat - clat) / ry) ** 2 <= 1.0


NA = [(-168, 66), (-140, 70), (-125, 72), (-108, 73), (-95, 79), (-86, 70), (-80, 73),
      (-77, 68), (-85, 66), (-93, 66), (-95, 60), (-90, 58), (-82, 55), (-79, 51),
      (-65, 50), (-60, 46), (-70, 44), (-74, 40), (-76, 35), (-81, 31), (-80, 26),
      (-84, 30), (-90, 29), (-97, 26), (-97, 22), (-94, 18), (-90, 15), (-83, 9),
      (-79, 9), (-86, 13), (-92, 15), (-97, 16), (-102, 18), (-105, 20), (-110, 23),
      (-114, 29), (-120, 34), (-124, 40), (-124, 47), (-130, 54), (-140, 60),
      (-155, 60), (-166, 60)]
SA = [(-79, 9), (-72, 12), (-64, 10), (-55, 6), (-50, 0), (-44, -3), (-35, -8),
      (-39, -13), (-40, -20), (-48, -26), (-56, -35), (-62, -39), (-65, -41),
      (-67, -46), (-69, -50), (-68, -54), (-71, -54), (-73, -46), (-73, -37),
      (-71, -30), (-70, -20), (-75, -15), (-79, -8), (-81, -4), (-80, 1), (-77, 4)]
AF = [(-6, 35), (0, 36), (10, 37), (20, 32), (30, 31), (33, 27), (35, 24), (38, 22),
      (40, 15), (43, 12), (48, 11), (51, 12), (48, 5), (42, -2), (40, -10), (39, -18),
      (36, -22), (33, -26), (28, 33 - 66), (20, -35), (17, -32), (15, -27), (13, -18),
      (12, -10), (13, -5), (9, -1), (9, 4), (4, 6), (-3, 5), (-8, 5), (-13, 8),
      (-17, 12), (-17, 15), (-16, 20), (-15, 25), (-13, 28), (-10, 31)]
EU = [(-9, 37), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 55), (8, 57), (5, 59),
      (5, 61), (11, 65), (16, 68), (25, 71), (35, 69), (45, 68), (60, 69), (75, 72),
      (90, 75), (105, 77), (120, 73), (135, 72), (150, 70), (165, 70), (178, 66),
      (178, 63), (168, 60), (160, 56), (156, 51), (150, 45), (142, 42), (140, 38),
      (135, 34), (129, 33), (126, 35), (122, 30), (120, 24), (114, 22), (108, 17),
      (106, 9), (104, 6), (100, 7), (98, 13), (94, 17), (91, 22), (88, 21), (85, 19),
      (80, 14), (77, 8), (74, 13), (72, 19), (67, 24), (61, 25), (57, 26), (54, 26),
      (51, 28), (49, 30), (50, 26), (55, 24), (59, 22), (55, 17), (52, 15), (45, 12),
      (43, 12), (40, 15), (39, 20), (36, 24), (34, 28), (35, 31), (36, 36), (30, 36),
      (27, 37), (23, 36), (19, 40), (16, 40), (12, 44), (8, 44), (3, 43), (0, 39), (-2, 37)]
AU = [(113, -22), (114, -28), (115, -34), (118, -35), (124, -33), (129, -32), (132, -32),
      (135, -35), (138, -35), (140, -38), (145, -38), (147, -39), (150, -37), (153, -32),
      (153, -27), (151, -24), (149, -20), (146, -19), (145, -15), (143, -11), (142, -11),
      (141, -13), (140, -18), (139, -20), (136, -15), (135, -12), (132, -11), (129, -14),
      (126, -14), (122, -17), (118, -20), (114, -22)]
ISLANDS = [(138, 37, 7, 5), (-2, 54, 3.5, 4), (113, -1, 15, 3), (122, 13, 3.5, 4.5),
           (172, -42, 3.5, 5), (47, -19, 3, 6), (102, 0, 4, 3), (95, 5, 3, 3),
           (129, 33, 3, 2.5), (23, 65, 4, 3)]
HOLES = [(51, 43, 5.5, 4), (35, 43.5, 6, 2.8), (-86, 60, 7, 5), (48, 29, 4, 2.5)]


def _land(lon, lat):
    for clon, clat, rx, ry in HOLES:
        if _in_ellipse(lon, lat, clon, clat, rx, ry):
            return False
    for poly in (NA, SA, AF, EU, AU):
        if _in_poly(lon, lat, poly):
            return True
    for clon, clat, rx, ry in ISLANDS:
        if _in_ellipse(lon, lat, clon, clat, rx, ry):
            return True
    return False


def cand05():
    """World map with numbered pins + legend."""
    c = C((234, 243, 251))
    c.rect(0, 0, 1024, 116, fill=(23, 58, 94))
    c.text(40, 18, DATE, "disp_xb", 40, (255, 255, 255))
    c.text(40, 68, "THE DAY ON THE MAP - THE WORLD'S NEWS, WHERE IT HAPPENED", "sans_b", 22, (150, 197, 240))
    # map area
    mx0, my0, mw, mh = 24, 132, 976, 470
    step = 15.5
    cols = int(mw / step)
    rows = int(mh / step)
    for r in range(rows):
        for col in range(cols):
            lon = -180 + (col + 0.5) * (360 / cols)
            lat = 80 - (r + 0.5) * (140 / rows)
            if _land(lon, lat):
                cx = mx0 + (col + 0.5) * step
                cy = my0 + (r + 0.5) * step
                c.ellipse(cx - 4.4, cy - 4.4, 8.8, 8.8, fill=(47, 107, 178))

    def pin(num, lon, lat):
        x = mx0 + (lon + 180) / 360 * mw
        y = my0 + (80 - lat) / 140 * mh
        c.ellipse(x - 17, y - 17, 34, 34, fill=(197, 48, 49), outline=(255, 255, 255), ow=3)
        c.text(x, y - 13, str(num), "sans_b", 22, (255, 255, 255), anchor="ma")

    pin(1, 114, 22.5)
    pin(2, 49, 28)
    pin(3, 34.3, 31.4)
    pin(4, -86, 36.5)
    pin(5, -70.5, 42.5)
    pin(7, 4.3, 52)
    pin(8, 41, 11)
    pin(9, 130.7, 32.8)
    # legend
    leg = [
        ("1", "SHENZHEN - Trump, Xi & Putin hold the first-ever US-China-Russia summit (at APEC)"),
        ("2", "THE GULF - Iran strikes a US base in Kuwait & targets in Bahrain; 3 tankers burn near Hormuz"),
        ("3", "GAZA - Israel launches a ground operation in central Gaza; residents flee"),
        ("4", "WASHINGTON - Democrats nominate Jeffries for Speaker after sweeping the midterms"),
        ("5", "NEW YORK - Anthropic's record IPO: a reported $107B raised; Nasdaq debut as ANT"),
        ("7", "THE HAGUE - World Court delivers its ruling in the Rohingya genocide case"),
        ("8", "HORN OF AFRICA - Ethiopia-Eritrea clashes raise fears of full-scale war"),
        ("9", "KUMAMOTO, JAPAN - M5.7 earthquake strikes; no tsunami warning issued"),
    ]
    y = 622
    for num, txt in leg:
        c.ellipse(40, y, 30, 30, fill=(197, 48, 49))
        c.text(55, y + 3, num, "sans_b", 19, (255, 255, 255), anchor="ma")
        y = c.para(84, y + 2, txt, "sans_b", 21, 900, (23, 43, 66), leading=1.18) + 7
    c.rrect(32, y + 2, 960, 52, 8, fill=(23, 58, 94))
    c.text(512, y + 13, "AND WORLDWIDE: 'GRAND THEFT AUTO VI' LAUNCHES TO NEAR-PERFECT REVIEWS",
           "sans_b", 22, (255, 255, 255), anchor="ma")
    save(c, "cand05.png")


# ================================================================ cand 06
def cand06():
    """Tabloid."""
    c = C((255, 255, 255))
    c.rect(0, 0, 1024, 14, fill=(208, 2, 27))
    c.text(40, 26, "WORLD DAILY", "disp_blk", 88, (208, 2, 27))
    c.rrect(770, 40, 214, 52, 6, fill=(208, 2, 27))
    c.text(877, 52, "EXTRA! EXTRA!", "sans_b", 26, (255, 255, 255), anchor="ma")
    c.rect(0, 132, 1024, 58, fill=(255, 221, 0))
    c.text(512, 143, DATE, "sans_b", 36, (10, 10, 10), anchor="ma")
    c.text(40, 204, "SHENZHEN, CHINA", "sans_b", 24, (208, 2, 27))
    hs = c.fit_size("THREE SUPERPOWERS. ONE TABLE.", "disp_blk", 64, 944)
    c.text(40, 234, "THREE SUPERPOWERS. ONE TABLE.", "disp_blk", hs, (10, 10, 10))
    fx = 40
    for nm in ("us", "cn", "ru"):
        flag(c, nm, fx, 316, 170, 112)
        fx += 192
    c.para(630, 322, "Trump, Xi and Putin hold the first-ever US-China-Russia summit, on the "
                     "sidelines of APEC. Arms control, Ukraine and Iran top the agenda.",
           "sans", 22, 354, (40, 40, 40), leading=1.3)
    # stat chips
    chips = [("$107B", "ANTHROPIC IPO - BIGGEST EVER, TOPS SPACEX"),
             ("56-44", "SENATE TO DEMOCRATS IN MIDTERM SWEEP"),
             ("M5.7", "EARTHQUAKE HITS KUMAMOTO, JAPAN")]
    cx = 40
    for big, cap in chips:
        c.rrect(cx, 476, 296, 126, 10, fill=(16, 16, 16))
        c.text(cx + 148, 488, big, "disp_blk", 50, (255, 221, 0), anchor="ma")
        c.para(cx + 14, 546, cap, "sans_b", 16, 268, (255, 255, 255), leading=1.2, align="center")
        cx += 324
    # two story blocks
    c.rect(40, 622, 452, 6, fill=(208, 2, 27))
    c.para(40, 640, S2H, "disp_xb", 28, 452, (10, 10, 10), leading=1.12)
    c.para(40, 716, "US base in Kuwait hit; Bahrain targets struck; Gulf states repel drones; "
                    "three tankers afire after mines east of Hormuz.", "sans", 21, 452, (50, 50, 50), leading=1.28)
    c.rect(532, 622, 452, 6, fill=(208, 2, 27))
    c.para(532, 640, S4H, "disp_xb", 28, 452, (10, 10, 10), leading=1.12)
    c.para(532, 716, "Hakeem Jeffries nominated - set to be the first African-American Speaker "
                     "of the House.", "sans", 21, 452, (50, 50, 50), leading=1.28)
    c.rect(40, 856, 944, 108, fill=(240, 240, 240))
    c.para(56, 872, "ALSO TODAY: " + S3H + "  ·  " + S6H + "  ·  " + S7H + "  ·  " + S8H,
           "sans_b", 21, 912, (10, 10, 10), leading=1.3)
    save(c, "cand06.png")


# ================================================================ cand 07
def cand07():
    """Swiss minimal."""
    c = C((255, 255, 255))
    INK2 = (17, 17, 17)
    ACC = (226, 0, 26)
    c.text(44, 8, "19", "disp_blk", 300, INK2)
    c.text(470, 66, "NOVEMBER", "disp_blk", 74, INK2)
    c.text(470, 148, "2026", "disp_blk", 74, INK2)
    c.text(472, 236, "THURSDAY", "disp_xb", 44, ACC)
    c.text(44, 330, DATE, "sans_b", 30, INK2)
    c.rect(44, 378, 936, 6, fill=ACC)
    rows = [
        (S1H, "Trump, Xi & Putin meet in Shenzhen (APEC sidelines): arms control, Ukraine, Iran. Their 50th Xi-Putin meeting."),
        (S2H, "US base in Kuwait and Bahrain targets hit; drones repelled; three tankers burn after mines near Hormuz."),
        (S3H, "Israeli forces move into central Gaza as residents flee."),
        (S4H, "Hakeem Jeffries, set to be first African-American Speaker; Senate taken 56-44."),
        (S5H, "Reported $107 billion raised - biggest IPO ever, topping SpaceX. Nasdaq: ANT."),
        (S7H, "ICJ delivers its ruling in Myanmar's Rohingya genocide case."),
        (S8H, "Clashes raise fears of a return to full-scale war."),
    ]
    y = 404
    for h, b in rows:
        c.rect(44, y + 6, 16, 16, fill=ACC)
        c.para(80, y, h, "sans_b", 25, 900, INK2, leading=1.1)
        y = c.para(80, y + 32, b, "sans", 21, 900, (90, 90, 90), leading=1.22) + 13
    c.rect(44, y + 2, 936, 2, fill=INK2)
    c.para(44, y + 12, M2 + "  ·  " + M3, "sans", 20, 936, (90, 90, 90), leading=1.3)
    save(c, "cand07.png")


# ================================================================ cand 08
def cand08():
    """TV news broadcast."""
    c = C((8, 26, 56))
    for i in range(1024):  # vertical gradient
        t = i / 1024
        col = (int(10 + 6 * t), int(34 + 10 * t), int(74 + 26 * t))
        c.line([(0, i), (1024, i)], col, 1)
    c.rect(0, 0, 330, 92, fill=(200, 16, 46))
    c.text(24, 16, "WORLD NEWS", "disp_blk", 44, (255, 255, 255))
    c.text(24, 64, "ONE DAY IN ONE PICTURE", "sans_b", 17, (255, 190, 200))
    c.text_fit(984, 18, DATE, "sans_b", 30, 620, (255, 255, 255), anchor="ra")
    c.rrect(880, 56, 104, 30, 4, fill=(255, 255, 255))
    c.text(932, 61, "LIVE", "sans_b", 20, (200, 16, 46), anchor="ma")
    # main panel
    c.rrect(32, 116, 640, 560, 10, fill=(255, 255, 255, 22), outline=(120, 170, 230), ow=2)
    c.rect(32, 116, 640, 54, fill=(200, 16, 46))
    c.text(52, 128, "BREAKING NEWS", "disp_xb", 32, (255, 255, 255))
    fx = 56
    for nm in ("us", "cn", "ru"):
        flag(c, nm, fx, 192, 150, 100)
        fx += 170
    c.para(56, 312, "FIRST-EVER SUMMIT OF THE US, CHINESE AND RUSSIAN LEADERS", "disp_xb", 36,
           592, (255, 255, 255), leading=1.14)
    c.para(56, 428, "Trump, Xi and Putin meet in Shenzhen, on the sidelines of APEC. Agenda: "
                    "nuclear arms control, the Ukraine war and Iran. Xi greeted Trump at the "
                    "airport; the Xi-Putin meeting was their 50th.",
           "sans", 23, 592, (205, 222, 245), leading=1.32)
    c.text(56, 622, "SHENZHEN, CHINA", "sans_b", 21, (255, 210, 63))
    # right rail
    rail = [
        ((255, 77, 94), S2H, "Kuwait base & Bahrain hit; drones repelled; 3 tankers burn near Hormuz."),
        ((255, 170, 60), S3H, "Residents flee as Israeli forces move in."),
        ((90, 200, 250), S4H, "Jeffries to be first African-American Speaker; Senate 56-44."),
    ]
    ry = 116
    for colr, h, b in rail:
        c.rrect(696, ry, 296, 176, 10, fill=(255, 255, 255, 22))
        c.rect(696, ry, 296, 8, fill=colr)
        c.para(714, ry + 20, h, "sans_b", 21, 262, (255, 255, 255), leading=1.15)
        c.para(714, ry + 92, b, "sans", 19, 262, (190, 208, 235), leading=1.25)
        ry += 192
    # ticker
    c.rect(0, 692, 1024, 196, fill=(5, 5, 8))
    c.rect(0, 692, 170, 196, fill=(255, 210, 63))
    c.text(85, 742, "THE", "disp_blk", 30, (5, 5, 8), anchor="ma")
    c.text(85, 778, "LATEST", "disp_blk", 30, (5, 5, 8), anchor="ma")
    tick = ("ANTHROPIC IPO RAISES A REPORTED $107B - BIGGEST EVER  +++  GTA VI LAUNCHES WORLDWIDE "
            "TO NEAR-PERFECT REVIEWS  +++  WORLD COURT RULES IN ROHINGYA CASE  +++  M5.7 QUAKE "
            "HITS KUMAMOTO - NO TSUNAMI WARNING  +++  VOYAGER 1 REACHES ONE LIGHT-DAY FROM EARTH  "
            "+++  ETHIOPIA-ERITREA CLASHES RAISE WAR FEARS")
    c.para(192, 710, tick, "sans_b", 22, 800, (255, 255, 255), leading=1.3)
    c.para(32, 906, "PLUS: A VAN GOGH SELLS FOR A RECORD $190.4M - AND SOUTH KOREA HOLDS ITS "
                    "COLLEGE ENTRANCE EXAM UNDER STRICT ANTI-CHEATING CURBS",
           "sans", 20, 960, (160, 190, 225), leading=1.3)
    save(c, "cand08.png")


# ================================================================ cand 09
def cand09():
    """Poster: hero summit + ALSO ON THURSDAY list."""
    c = C((16, 28, 48))
    c.rect(0, 0, 1024, 84, fill=(8, 8, 10))
    c.text(512, 20, DATE, "disp_xb", 40, (255, 255, 255), anchor="ma")
    fx = 232
    for nm in ("us", "cn", "ru"):
        flag(c, nm, fx, 104, 170, 108)
        fx += 200
    c.text(512, 232, "THREE SUPERPOWERS,", "disp_blk", 58, (255, 255, 255), anchor="ma")
    c.text(512, 298, "ONE TABLE", "disp_blk", 58, (255, 210, 63), anchor="ma")
    c.para(112, 368, "Trump, Xi and Putin hold the first-ever US-China-Russia trilateral summit in "
                     "Shenzhen, on the sidelines of APEC - to discuss nuclear arms control, the "
                     "Ukraine war and Iran. Xi greeted Trump at the airport; Xi's meeting with "
                     "Putin was their 50th.", "sans", 21, 800, (200, 214, 235), leading=1.32, align="center")
    # bottom cream zone
    c.rect(0, 492, 1024, 532, fill=(247, 242, 231))
    c.text(48, 510, "ALSO ON THURSDAY", "disp_xb", 30, (179, 35, 42))
    items = [
        (S2H, "Kuwait base & Bahrain targets hit; drones repelled; three tankers burn near Hormuz."),
        (S3H, "Residents flee as Israeli forces move into central Gaza."),
        (S4H, "Jeffries set to be first African-American Speaker; Senate 56-44."),
        (S5H, "Reported $107B raise tops SpaceX's record; Nasdaq debut as ANT."),
        (S6H, "On sale worldwide to near-perfect reviews."),
        (S7H, "ICJ delivers its ruling in Myanmar's Rohingya genocide case."),
        (S8H, "Clashes raise fears of a return to full-scale war."),
    ]
    y = 556
    for i, (h, b) in enumerate(items):
        c.text(48, y, str(i + 2), "disp_blk", 27, (179, 35, 42))
        c.para(92, y + 1, h, "sans_b", 22, 884, (20, 18, 14), leading=1.1)
        c.para(92, y + 28, b, "sans", 19, 884, (92, 88, 80), leading=1.2)
        y += 57
    c.rect(48, y + 4, 928, 2, fill=(179, 35, 42))
    c.para(48, y + 14, "PLUS: " + M1 + "  ·  " + M3, "sans_b", 18, 928, (92, 88, 80), leading=1.25)
    save(c, "cand09.png")


# ================================================================ cand 10
def cand10():
    """Mondrian mosaic of colour tiles."""
    c = C((24, 24, 24))
    W_ = (255, 255, 255)
    # date tile
    c.rect(0, 0, 1024, 118, fill=(10, 10, 10))
    c.text(36, 22, DATE, "disp_xb", 42, W_)
    c.text(36, 74, "THE DAY'S WORLD NEWS IN ONE PICTURE", "sans_b", 21, (255, 210, 63))
    # summit tile
    c.rect(0, 118, 648, 296, fill=(23, 58, 94))
    fx = 30
    for nm in ("us", "cn", "ru"):
        flag(c, nm, fx, 142, 108, 72)
        fx += 124
    c.text(426, 152, "SUMMIT", "disp_blk", 34, (255, 210, 63))
    c.text(426, 190, "SHENZHEN", "sans_b", 19, W_)
    c.para(30, 232, "TRUMP, XI & PUTIN: FIRST-EVER TRILATERAL SUMMIT", "disp_xb", 30, 590, W_, leading=1.12)
    c.para(30, 306, "At APEC's sidelines: arms control, Ukraine, Iran. Xi-Putin talks were their 50th.",
           "sans", 20, 590, (190, 214, 240), leading=1.25)
    # anthropic tile
    c.rect(648, 118, 376, 296, fill=(6, 120, 74))
    c.text(836, 140, "$107B", "disp_blk", 84, W_, anchor="ma")
    c.para(678, 240, "ANTHROPIC'S RECORD IPO", "sans_b", 25, 316, W_, leading=1.15, align="center")
    c.para(678, 306, "Reported raise tops SpaceX's record debut. Now trading on Nasdaq: ANT",
           "sans", 20, 316, (190, 240, 215), leading=1.25, align="center")
    # iran tile
    c.rect(0, 414, 512, 216, fill=(178, 30, 40))
    icon(c, "missile", 28, 470, 92, W_, (255, 190, 80))
    hend = c.para(140, 436, S2H, "sans_b", 25, 348, W_, leading=1.14)
    c.para(140, hend + 8, "US base in Kuwait & Bahrain targets hit; drones repelled; 3 tankers burn near Hormuz.",
           "sans", 20, 348, (255, 215, 218), leading=1.25)
    # gaza tile
    c.rect(512, 414, 512, 216, fill=(194, 102, 10))
    icon(c, "burst", 540, 470, 92, W_, (255, 230, 120))
    hend = c.para(652, 436, S3H, "sans_b", 25, 348, W_, leading=1.14)
    c.para(652, hend + 8, "Israeli forces move into central Gaza as residents flee the fighting.",
           "sans", 20, 348, (255, 232, 205), leading=1.25)
    # jeffries tile
    c.rect(0, 630, 341, 216, fill=(88, 50, 160))
    icon(c, "dome", 24, 664, 74, W_)
    hend = c.para(112, 650, "JEFFRIES NOMINATED FOR SPEAKER", "sans_b", 21, 216, W_, leading=1.15)
    c.para(112, hend + 5, "Democrats' pick - first African-American Speaker-to-be; Senate 56-44.", "sans", 18, 216, (220, 205, 250), leading=1.25)
    # gta tile
    c.rect(341, 630, 342, 216, fill=(40, 40, 46))
    icon(c, "controller", 365, 664, 74, (255, 210, 63))
    hend = c.para(453, 650, S6H, "sans_b", 21, 216, W_, leading=1.15)
    c.para(453, hend + 5, "On sale worldwide to near-perfect reviews.", "sans", 18, 216, (210, 210, 215), leading=1.25)
    # icj tile
    c.rect(683, 630, 341, 216, fill=(10, 116, 116))
    icon(c, "scales", 707, 664, 74, W_)
    hend = c.para(795, 650, "WORLD COURT RULES ON ROHINGYA CASE", "sans_b", 21, 216, W_, leading=1.15)
    c.para(795, hend + 5, "ICJ delivers its ruling in Myanmar's Rohingya genocide case.", "sans", 18, 216, (200, 240, 240), leading=1.25)
    # bottom strip
    c.rect(0, 846, 1024, 178, fill=(52, 52, 56))
    c.para(30, 862, S8H, "sans_b", 23, 964, W_, leading=1.12)
    c.para(30, 900, "ALSO: " + M1 + "  ·  " + M2 + "  ·  " + M3 + "  ·  " + M4,
           "sans", 20, 964, (205, 205, 210), leading=1.3)
    save(c, "cand10.png")


if __name__ == "__main__":
    cand01(); cand02(); cand03(); cand04(); cand05()
    cand06(); cand07(); cand08(); cand09(); cand10()
    print("done")
