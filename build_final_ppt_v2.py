"""
CS 719 — Midterm Project Review Presentation  (V2 — Redesigned Layout)
Same content as V1, but with:
  - Better graph/plot placement (no clutter, generous whitespace)
  - Modern design: layered title bar, accent bars, rounded cards
  - Charts inside labeled card containers — no floating/overlapping
  - Minimum font 16pt.  University of Regina / CS 719 branding.
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

# ── Colour palette ──────────────────────────────────────────────
NAVY       = RGBColor(0x0D, 0x1B, 0x2A)
MID_NAVY   = RGBColor(0x14, 0x25, 0x3D)
GOLD       = RGBColor(0xD4, 0xA0, 0x1E)
SOFT_GOLD  = RGBColor(0xF0, 0xC8, 0x50)
BLUE       = RGBColor(0x2E, 0x86, 0xC1)
GREEN      = RGBColor(0x27, 0xAE, 0x60)
ORANGE     = RGBColor(0xE6, 0x7E, 0x22)
RED        = RGBColor(0xE7, 0x4C, 0x3C)
PURPLE     = RGBColor(0x8E, 0x44, 0xAD)
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
LGRAY      = RGBColor(0xEC, 0xF0, 0xF1)
MGRAY      = RGBColor(0x7F, 0x8C, 0x8D)
DARK       = RGBColor(0x2C, 0x3E, 0x50)
LIGHT_BG   = RGBColor(0xF4, 0xF6, 0xF9)
CARD_BG    = RGBColor(0xFF, 0xFF, 0xFF)
CARD_BDR   = RGBColor(0xE0, 0xE4, 0xE8)
SHADOW_C   = RGBColor(0xD5, 0xD8, 0xDC)
TEAL       = RGBColor(0x00, 0x97, 0xA7)

IMG = "/tmp/nb_images"
TOTAL = 14

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)

# ── Helpers ─────────────────────────────────────────────────────

def bg(slide, color):
    f = slide.background.fill; f.solid(); f.fore_color.rgb = color

def rect(slide, l, t, w, h, fill, border=None):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    s.fill.solid(); s.fill.fore_color.rgb = fill
    if border:
        s.line.color.rgb = border; s.line.width = Pt(1)
    else:
        s.line.fill.background()
    return s

def rrect(slide, l, t, w, h, fill, border=None):
    s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l, t, w, h)
    s.fill.solid(); s.fill.fore_color.rgb = fill
    if border:
        s.line.color.rgb = border; s.line.width = Pt(1)
    else:
        s.line.fill.background()
    return s

def tb(slide, l, t, w, h, txt, sz=18, c=DARK, b=False, align=PP_ALIGN.LEFT,
       font="Calibri"):
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = txt; p.font.size = Pt(sz); p.font.color.rgb = c
    p.font.bold = b; p.font.name = font; p.alignment = align
    p.space_after = Pt(0); p.space_before = Pt(0)
    return box

def rtb(slide, l, t, w, h, items, font="Calibri"):
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame; tf.word_wrap = True
    for i, (txt, sz, col, bld, sa) in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = txt; p.font.size = Pt(sz); p.font.color.rgb = col
        p.font.bold = bld; p.font.name = font
        p.space_after = Pt(sa); p.space_before = Pt(0)
    return box

def accent_line(slide, l, t, w, color=GOLD, thick=4):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, Pt(thick))
    s.fill.solid(); s.fill.fore_color.rgb = color; s.line.fill.background()

def footer(slide, num):
    rect(slide, Inches(0), Inches(7.1), prs.slide_width, Inches(0.4), NAVY)
    tb(slide, Inches(0.6), Inches(7.15), Inches(8), Inches(0.3),
       "CS 719 — Data Science Project  |  Midterm Project Review  |  Raj Panchal",
       14, MGRAY)
    tb(slide, Inches(11.0), Inches(7.15), Inches(2), Inches(0.3),
       f"{num} / {TOTAL}", 14, LGRAY, align=PP_ALIGN.RIGHT)

def card(slide, l, t, w, h, fill=CARD_BG, border=CARD_BDR, accent=None):
    rrect(slide, l + Inches(0.04), t + Inches(0.04), w, h, SHADOW_C)
    c = rrect(slide, l, t, w, h, fill, border)
    if accent:
        rect(slide, l, t + Inches(0.08), Inches(0.1), h - Inches(0.16), accent)
    return c

def title_section(slide, title_text):
    rect(slide, Inches(0), Inches(0), prs.slide_width, Inches(1.15), NAVY)
    rect(slide, Inches(0), Inches(0.9), prs.slide_width, Inches(0.25), MID_NAVY)
    accent_line(slide, Inches(0.7), Inches(0.92), Inches(3.0), GOLD, 5)
    tb(slide, Inches(0.7), Inches(0.2), Inches(11), Inches(0.65),
       title_text, 28, WHITE, True)

def cslide(title, num):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s, LIGHT_BG)
    rect(s, Inches(11.5), Inches(0), Inches(1.833), Inches(0.08), GOLD)
    title_section(s, title)
    footer(s, num)
    return s

def img(slide, name, l, t, w=None, h=None):
    p = os.path.join(IMG, name)
    if not os.path.exists(p): return False
    kw = {"left": l, "top": t}
    if w: kw["width"] = w
    if h: kw["height"] = h
    slide.shapes.add_picture(p, **kw); return True

def oval(slide, x, y, sz, text, fill_c=GOLD, txt_c=WHITE, txt_sz=18):
    o = slide.shapes.add_shape(MSO_SHAPE.OVAL, x, y, sz, sz)
    o.fill.solid(); o.fill.fore_color.rgb = fill_c; o.line.fill.background()
    tf = o.text_frame
    tf.paragraphs[0].text = text
    tf.paragraphs[0].font.size = Pt(txt_sz)
    tf.paragraphs[0].font.color.rgb = txt_c
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    return o

def arrow_r(slide, x, y, w=Inches(0.35), h=Inches(0.3)):
    a = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, x, y, w, h)
    a.fill.solid(); a.fill.fore_color.rgb = GOLD; a.line.fill.background()

def arrow_d(slide, x, y, w=Inches(0.25), h=Inches(0.3)):
    a = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, x, y, w, h)
    a.fill.solid(); a.fill.fore_color.rgb = GOLD; a.line.fill.background()

def section_label(slide, l, t, text, color=GOLD):
    tb(slide, l, t, Inches(5), Inches(0.3), text, 16, color, True)
    accent_line(slide, l, t + Inches(0.28), Inches(1.5), color, 3)


# ══════════════════════════════════════════════════════════════════
#  SLIDE 1 — TITLE
# ══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
bg(s, NAVY)

rect(s, Inches(0), Inches(0), Inches(0.12), Inches(7.5), GOLD)
rect(s, Inches(0.12), Inches(0), Inches(0.04), Inches(7.5), MID_NAVY)
rect(s, Inches(0.16), Inches(3.5), prs.slide_width, Inches(0.06), MID_NAVY)

accent_line(s, Inches(1.5), Inches(1.0), Inches(4.0), GOLD, 5)

tb(s, Inches(1.5), Inches(1.4), Inches(10.5), Inches(1.6),
   "Predictive Analytics and Explainable AI\nfor Hospital Readmission Risk",
   42, WHITE, True)

tb(s, Inches(1.5), Inches(3.1), Inches(10), Inches(0.5),
   "Midterm Project Review", 28, GOLD, True)

accent_line(s, Inches(1.5), Inches(3.85), Inches(3.0), GOLD, 3)
tb(s, Inches(1.5), Inches(4.15), Inches(10), Inches(0.5),
   "CS 719 — Data Science Project (Winter 2026)", 22, LGRAY)

tb(s, Inches(1.5), Inches(4.9), Inches(6), Inches(0.4),
   "Prepared By:  Raj Panchal (200490453)", 20, WHITE, True)

tb(s, Inches(1.5), Inches(5.4), Inches(6), Inches(0.4),
   "Date:  March 3, 2026", 20, WHITE)

tb(s, Inches(1.5), Inches(6.0), Inches(8), Inches(0.5),
   "Under Esteemed Guidance of Instructor:", 18, MGRAY)
tb(s, Inches(1.5), Inches(6.4), Inches(8), Inches(0.4),
   "Howard J. Hamilton", 22, WHITE, True)

rect(s, Inches(0), Inches(7.1), prs.slide_width, Inches(0.4), RGBColor(0x08, 0x10, 0x1A))
tb(s, Inches(0.6), Inches(7.15), Inches(8), Inches(0.3),
   "University of Regina  |  Faculty of Science  |  Department of Computer Science",
   14, MGRAY)
tb(s, Inches(11.0), Inches(7.15), Inches(2), Inches(0.3),
   f"1 / {TOTAL}", 14, LGRAY, align=PP_ALIGN.RIGHT)


# ══════════════════════════════════════════════════════════════════
#  SLIDE 2 — GOAL, MOTIVATION & METHOD
# ══════════════════════════════════════════════════════════════════
s = cslide("Goal, Motivation & Method", 2)

section_label(s, Inches(0.7), Inches(1.3), "GOAL")
card(s, Inches(0.5), Inches(1.65), Inches(12.3), Inches(1.15), accent=BLUE)
tb(s, Inches(0.85), Inches(1.75), Inches(11.7), Inches(0.9),
   "Build a machine learning system that predicts whether a diabetic patient will be "
   "readmitted to the hospital within 30 days of discharge, and explain which clinical "
   "factors drive the prediction — enabling hospitals to intervene early and reduce "
   "costly readmissions.", 18, DARK)

section_label(s, Inches(0.7), Inches(3.05), "WHY IT MATTERS")

motiv = [
    ("$26 B+", "Annual cost of unplanned\nreadmissions in the U.S.", BLUE),
    ("11.4%", "Diabetic patients in our\ndataset readmitted within 30 days", ORANGE),
    ("Preventable", "Early risk identification can\ntrigger targeted interventions", GREEN),
]
for i, (stat, desc, col) in enumerate(motiv):
    x = Inches(0.5) + i * Inches(4.15)
    card(s, x, Inches(3.45), Inches(3.85), Inches(1.45), accent=col)
    tb(s, x + Inches(0.35), Inches(3.55), Inches(3.3), Inches(0.5),
       stat, 30, col, True, PP_ALIGN.CENTER)
    tb(s, x + Inches(0.35), Inches(4.05), Inches(3.3), Inches(0.7),
       desc, 16, MGRAY, align=PP_ALIGN.CENTER)

section_label(s, Inches(0.7), Inches(5.15), "METHOD — 6-Step Pipeline")

card(s, Inches(0.5), Inches(5.5), Inches(12.3), Inches(1.3))
method_steps = [
    ("1", "Data\nCleaning"), ("2", "Feature\nEngineering"),
    ("3", "Train 3\nModels"), ("4", "Compare &\nSelect Best"),
    ("5", "Explain\n(PFI + PDP)"), ("6", "Interactive\nDashboard"),
]
for i, (num, label) in enumerate(method_steps):
    x = Inches(0.8) + i * Inches(2.0)
    y = Inches(5.68)
    oval(s, x, y, Inches(0.45), num, GOLD, WHITE, 16)
    tb(s, x + Inches(0.55), y - Inches(0.02), Inches(1.3), Inches(0.55),
       label, 16, DARK)
    if i < 5:
        arrow_r(s, x + Inches(1.7), y + Inches(0.1), Inches(0.25), Inches(0.25))


# ══════════════════════════════════════════════════════════════════
#  SLIDE 3 — PICTORIAL OVERVIEW
# ══════════════════════════════════════════════════════════════════
s = cslide("Pictorial Overview — Project Design", 3)

row1_y = Inches(1.35)
row1_boxes = [
    ("Raw Dataset", "101,766 records\n50 features\n130 US hospitals", BLUE),
    ("Data Cleaning", "Drop high-null cols\nRemove expired rows\n99,340 × 42", TEAL),
    ("Feature\nEngineering", "4 new features\nBinary target\n99,340 × 23", RGBColor(0x42,0xA5,0xF5)),
    ("Exploratory\nData Analysis", "Distributions\nCorrelations\nStatistical tests", PURPLE),
]
for i, (title, desc, col) in enumerate(row1_boxes):
    x = Inches(0.4) + i * Inches(3.25)
    rrect(s, x, row1_y, Inches(2.85), Inches(1.6), WHITE, CARD_BDR)
    rect(s, x, row1_y, Inches(2.85), Inches(0.06), col)
    tb(s, x + Inches(0.15), row1_y + Inches(0.15), Inches(2.55), Inches(0.4),
       title, 17, col, True, PP_ALIGN.CENTER)
    tb(s, x + Inches(0.15), row1_y + Inches(0.6), Inches(2.55), Inches(0.85),
       desc, 16, MGRAY, align=PP_ALIGN.CENTER)
    if i < 3:
        arrow_r(s, x + Inches(2.9), row1_y + Inches(0.6))

arrow_d(s, Inches(6.55), Inches(3.05))

row2_y = Inches(3.55)
row2_boxes = [
    ("Preprocessing", "One-Hot Encode\n80/20 split\nSMOTE + Scale", RGBColor(0xFF,0xB3,0x00)),
    ("Model Training", "Logistic Regression\nRandom Forest\nXGBoost", ORANGE),
    ("Evaluation &\nSelection", "ROC-AUC, F1, CV\nConfusion matrices\nBest: XGBoost", RED),
]
for i, (title, desc, col) in enumerate(row2_boxes):
    x = Inches(0.4) + i * Inches(3.25)
    rrect(s, x, row2_y, Inches(2.85), Inches(1.6), WHITE, CARD_BDR)
    rect(s, x, row2_y, Inches(2.85), Inches(0.06), col)
    tb(s, x + Inches(0.15), row2_y + Inches(0.15), Inches(2.55), Inches(0.4),
       title, 17, col, True, PP_ALIGN.CENTER)
    tb(s, x + Inches(0.15), row2_y + Inches(0.6), Inches(2.55), Inches(0.85),
       desc, 16, MGRAY, align=PP_ALIGN.CENTER)
    if i < 2:
        arrow_r(s, x + Inches(2.9), row2_y + Inches(0.6))

arrow_d(s, Inches(6.55), Inches(5.25))

row3_y = Inches(5.75)
row3_boxes = [
    ("Explainability", "PFI + PDP\non best model", GREEN),
    ("Dashboard", "Streamlit app\nwhat-if analysis", TEAL),
    ("Final Report", "Complete\nwrite-up", MID_NAVY),
]
for i, (title, desc, col) in enumerate(row3_boxes):
    x = Inches(0.4) + i * Inches(3.25)
    rrect(s, x, row3_y, Inches(2.85), Inches(1.0), WHITE, CARD_BDR)
    rect(s, x, row3_y, Inches(2.85), Inches(0.06), col)
    tb(s, x + Inches(0.15), row3_y + Inches(0.1), Inches(2.55), Inches(0.3),
       title, 16, col, True, PP_ALIGN.CENTER)
    tb(s, x + Inches(0.15), row3_y + Inches(0.42), Inches(2.55), Inches(0.5),
       desc, 16, MGRAY, align=PP_ALIGN.CENTER)
    if i < 2:
        arrow_r(s, x + Inches(2.9), row3_y + Inches(0.3))

card(s, Inches(10.2), Inches(3.55), Inches(2.9), Inches(3.2), accent=GOLD)
tb(s, Inches(10.5), Inches(3.65), Inches(2.4), Inches(0.3),
   "STATUS", 16, DARK, True, PP_ALIGN.CENTER)
rect(s, Inches(10.5), Inches(4.05), Inches(2.4), Inches(0.05), GREEN)
tb(s, Inches(10.5), Inches(4.15), Inches(2.4), Inches(0.35),
   "Rows 1 & 2: DONE", 16, GREEN, True, PP_ALIGN.CENTER)
tb(s, Inches(10.5), Inches(4.5), Inches(2.4), Inches(0.55),
   "Data pipeline fully\ncomplete. Models\ntrained & evaluated.", 16, MGRAY, align=PP_ALIGN.CENTER)
rect(s, Inches(10.5), Inches(5.2), Inches(2.4), Inches(0.05), ORANGE)
tb(s, Inches(10.5), Inches(5.3), Inches(2.4), Inches(0.35),
   "Row 3: UPCOMING", 16, ORANGE, True, PP_ALIGN.CENTER)
tb(s, Inches(10.5), Inches(5.65), Inches(2.4), Inches(0.55),
   "Explainability, dashboard\n& final report in\nWeeks 6-12.", 16, MGRAY, align=PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════════════════
#  SLIDE 4 — ORIGINAL PROJECT SCHEDULE
# ══════════════════════════════════════════════════════════════════
s = cslide("Original Project Schedule", 4)

weeks = [
    ("Week 1", "Jan 27 - Feb 2", "Dataset exploration & literature review", True),
    ("Week 2", "Feb 3 - Feb 9", "Data cleaning, missing values, encoding", True),
    ("Week 3", "Feb 10 - Feb 16", "Feature engineering & binary target", True),
    ("Week 4", "Feb 17 - Feb 23", "Model training: LR, RF, XGBoost", True),
    ("Week 5", "Feb 24 - Mar 2", "Evaluation, model selection, midterm prep", True),
    ("", "Mar 3, 2026", "MILESTONE: Mid-Term Project Review (TODAY)", None),
    ("Week 6", "Mar 4 - Mar 10", "Hyperparameter tuning & cross-validation", False),
    ("Week 7", "Mar 11 - Mar 17", "Explainability: PFI & PDP on final model", False),
    ("Week 8", "Mar 18 - Mar 24", "Visualization of predictions & results", False),
    ("Week 9", "Mar 25 - Mar 31", "Draft report: Intro, Background, Results", False),
    ("Wk 10", "Apr 1 - Apr 7", "Discussion, Conclusion; figures & tables", False),
    ("Wk 11-12", "Apr 8 - Apr 23", "Review, proofreading & final formatting", False),
    ("", "Apr 24, 2026", "MILESTONE: Final Project Report Due", None),
]

y_start = Inches(1.3)
rrect(s, Inches(0.5), y_start, Inches(12.3), Inches(0.44), NAVY)
tb(s, Inches(0.7), y_start + Inches(0.06), Inches(1.3), Inches(0.32),
   "Week", 16, WHITE, True)
tb(s, Inches(2.0), y_start + Inches(0.06), Inches(2.0), Inches(0.32),
   "Dates", 16, WHITE, True)
tb(s, Inches(4.1), y_start + Inches(0.06), Inches(6.5), Inches(0.32),
   "Task", 16, WHITE, True)
tb(s, Inches(10.9), y_start + Inches(0.06), Inches(1.8), Inches(0.32),
   "Status", 16, WHITE, True)

for i, (wk, dates, task, done) in enumerate(weeks):
    y = y_start + Inches(0.46) + i * Inches(0.43)
    if done is None:
        rrect(s, Inches(0.5), y, Inches(12.3), Inches(0.43), RGBColor(0xFF,0xF3,0xE0))
        tb(s, Inches(2.0), y + Inches(0.05), Inches(2.0), Inches(0.32),
           dates, 16, ORANGE, True)
        tb(s, Inches(4.1), y + Inches(0.05), Inches(6.5), Inches(0.32),
           task, 16, ORANGE, True)
        tb(s, Inches(10.9), y + Inches(0.05), Inches(1.8), Inches(0.32),
           "\u2605", 18, ORANGE, True, PP_ALIGN.CENTER)
    else:
        bg_c = WHITE if i % 2 == 0 else RGBColor(0xF0,0xF4,0xF8)
        rect(s, Inches(0.5), y, Inches(12.3), Inches(0.43), bg_c)
        tb(s, Inches(0.7), y + Inches(0.05), Inches(1.3), Inches(0.32),
           wk, 16, DARK, True)
        tb(s, Inches(2.0), y + Inches(0.05), Inches(2.0), Inches(0.32),
           dates, 16, MGRAY)
        tb(s, Inches(4.1), y + Inches(0.05), Inches(6.5), Inches(0.32),
           task, 16, DARK)
        if done:
            tb(s, Inches(10.9), y + Inches(0.05), Inches(1.8), Inches(0.32),
               "\u2713 Done", 16, GREEN, True, PP_ALIGN.CENTER)
        else:
            tb(s, Inches(10.9), y + Inches(0.05), Inches(1.8), Inches(0.32),
               "Upcoming", 16, MGRAY, False, PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════════════════
#  SLIDE 5 — ACHIEVEMENT 1: DATA PREPARATION & FEATURE ENGINEERING
# ══════════════════════════════════════════════════════════════════
s = cslide("Achievement 1 — Data Preparation & Feature Engineering", 5)

# Left: key accomplishments
section_label(s, Inches(0.7), Inches(1.3), "WHAT WAS DONE")
card(s, Inches(0.5), Inches(1.65), Inches(6.4), Inches(2.65), accent=BLUE)
rtb(s, Inches(0.85), Inches(1.75), Inches(5.8), Inches(2.4), [
    ("\u2022  Cleaned 101,766 records from 130 US hospitals", 17, DARK, False, 4),
    ("\u2022  Dropped 4 high-null + 2 zero-variance columns", 17, DARK, False, 4),
    ("\u2022  Removed 2,426 expired/hospice rows -> 99,340 x 42", 17, DARK, False, 6),
    ("\u2022  Engineered 4 new features:", 17, DARK, False, 3),
    ("   total_visits, num_med_changed,", 17, BLUE, True, 2),
    ("   num_med_active, age_numeric", 17, BLUE, True, 6),
    ("\u2022  Binary target: <30d = 1 (11.4%), else = 0 (88.6%)", 17, DARK, False, 4),
    ("\u2022  Dropped 21 medication cols -> final: 99,340 x 23", 17, DARK, False, 0),
])

# Right: Missing values chart in card
section_label(s, Inches(7.2), Inches(1.3), "MISSING VALUES")
card(s, Inches(7.0), Inches(1.65), Inches(5.8), Inches(2.65))
img(s, "chart_13_01.png", Inches(7.2), Inches(1.85), w=Inches(5.4))

# Bottom left: Target distribution in card
section_label(s, Inches(0.7), Inches(4.5), "TARGET DISTRIBUTION")
card(s, Inches(0.5), Inches(4.85), Inches(5.8), Inches(2.05))
img(s, "chart_19_00.png", Inches(0.7), Inches(4.95), w=Inches(5.3), h=Inches(1.85))

# Bottom right: summary
section_label(s, Inches(7.2), Inches(4.5), "DATA TRANSFORMATION SUMMARY")
card(s, Inches(7.0), Inches(4.85), Inches(5.8), Inches(2.05), accent=GOLD)
rtb(s, Inches(7.35), Inches(5.0), Inches(5.2), Inches(1.7), [
    ("Before:  101,766 rows x 50 columns (202 MB)", 17, RED, True, 6),
    ("After:    99,340 rows x 23 columns (clean)", 17, GREEN, True, 10),
    ("Positive class rate: 11.39% (11,314 readmissions)", 17, DARK, False, 4),
    ("Negative class rate: 88.61% (88,026 not readmitted)", 17, MGRAY, False, 0),
])


# ══════════════════════════════════════════════════════════════════
#  SLIDE 6 — ACHIEVEMENT 1b: EDA & STATISTICAL TESTS
# ══════════════════════════════════════════════════════════════════
s = cslide("Achievement 1 — Exploratory Analysis & Statistical Tests", 6)

# Top left: chart in card
section_label(s, Inches(0.7), Inches(1.3), "READMISSION BY AGE & INPATIENT VISITS")
card(s, Inches(0.5), Inches(1.65), Inches(7.8), Inches(2.75))
img(s, "chart_24_00.png", Inches(0.7), Inches(1.75), w=Inches(7.3), h=Inches(2.55))

# Top right: Key discovery
section_label(s, Inches(8.8), Inches(1.3), "KEY DISCOVERY")
card(s, Inches(8.6), Inches(1.65), Inches(4.3), Inches(2.75), accent=GOLD)
rtb(s, Inches(8.95), Inches(1.8), Inches(3.8), Inches(2.4), [
    ("Prior inpatient visits is the", 18, DARK, True, 2),
    ("strongest predictor of", 18, DARK, True, 2),
    ("30-day readmission", 18, DARK, True, 12),
    ("0 visits -> 9% readmission", 17, GREEN, False, 4),
    ("4 visits -> 25% readmission", 17, ORANGE, False, 4),
    ("8 visits -> 47% readmission", 17, RED, True, 8),
    ("Near-linear monotonic increase", 16, MGRAY, False, 0),
])

# Bottom left: Correlation matrix in card
section_label(s, Inches(0.7), Inches(4.6), "CORRELATION MATRIX")
card(s, Inches(0.5), Inches(4.95), Inches(5.3), Inches(1.95))
img(s, "chart_21_00.png", Inches(0.65), Inches(5.0), w=Inches(4.8), h=Inches(1.85))

# Bottom right: Stats
section_label(s, Inches(6.3), Inches(4.6), "STATISTICAL TEST RESULTS")
card(s, Inches(6.1), Inches(4.95), Inches(6.8), Inches(1.95), accent=PURPLE)
rtb(s, Inches(6.45), Inches(5.05), Inches(6.3), Inches(1.7), [
    ("Shapiro-Wilk: All features non-normal (p = 0.00)", 16, DARK, False, 3),
    ("   -> Justifies tree-based models over parametric", 16, MGRAY, False, 6),
    ("Chi2 (diag_1 vs readmitted): p = 0.00 -- SIGNIFICANT", 16, GREEN, True, 3),
    ("   Diagnosis category predicts readmission", 16, MGRAY, False, 5),
    ("Chi2 (gender vs readmitted): p = 0.43 -- NOT significant", 16, RED, True, 3),
    ("   Gender does NOT predict readmission", 16, MGRAY, False, 5),
    ("Pearson: num_meds vs lab_procs r = 0.27 (weak)", 16, DARK, False, 0),
])


# ══════════════════════════════════════════════════════════════════
#  SLIDE 7 — ACHIEVEMENT 2: MODEL TRAINING
# ══════════════════════════════════════════════════════════════════
s = cslide("Achievement 2 — Model Training, Evaluation & Selection", 7)

section_label(s, Inches(0.7), Inches(1.3), "THREE MODELS TRAINED")
models = [
    ("Logistic Regression", "Linear Baseline", "max_iter=1000\nsolver=lbfgs",
     "Acc: 64.0%\nROC-AUC: 0.642\nRecall: 55%", BLUE),
    ("Random Forest", "Ensemble (Bagging)", "200 trees\nmax_depth=15",
     "Acc: 88.0%\nROC-AUC: 0.653\nRecall: 6%", PURPLE),
    ("XGBoost", "Ensemble (Boosting)", "200 estimators\nmax_depth=6, lr=0.1",
     "Acc: 88.6%\nROC-AUC: 0.671\nRecall: 2%", GREEN),
]
for i, (name, mtype, params, metrics, col) in enumerate(models):
    x = Inches(0.5) + i * Inches(4.2)
    card(s, x, Inches(1.65), Inches(3.85), Inches(2.2), accent=col)
    tb(s, x + Inches(0.35), Inches(1.75), Inches(3.3), Inches(0.35),
       name, 20, col, True, PP_ALIGN.CENTER)
    tb(s, x + Inches(0.35), Inches(2.1), Inches(3.3), Inches(0.25),
       mtype, 16, MGRAY, align=PP_ALIGN.CENTER)
    accent_line(s, x + Inches(0.7), Inches(2.4), Inches(2.5), col, 2)
    tb(s, x + Inches(0.35), Inches(2.55), Inches(1.6), Inches(1.0),
       params, 16, MGRAY)
    tb(s, x + Inches(2.0), Inches(2.55), Inches(1.6), Inches(1.0),
       metrics, 16, DARK, True)

rrect(s, Inches(9.2), Inches(1.6), Inches(3.6), Inches(0.32), GREEN)
tb(s, Inches(9.2), Inches(1.6), Inches(3.6), Inches(0.32),
   "\u2b50 SELECTED -- Best ROC-AUC", 14, WHITE, True, PP_ALIGN.CENTER)

# Charts in cards with labels
section_label(s, Inches(0.7), Inches(4.05), "CONFUSION MATRICES")
card(s, Inches(0.5), Inches(4.4), Inches(7.8), Inches(2.5))
img(s, "chart_36_00.png", Inches(0.7), Inches(4.5), w=Inches(7.4), h=Inches(2.3))

section_label(s, Inches(8.8), Inches(4.05), "MODEL COMPARISON")
card(s, Inches(8.6), Inches(4.4), Inches(4.3), Inches(2.5))
img(s, "chart_39_00.png", Inches(8.7), Inches(4.5), w=Inches(4.1), h=Inches(2.3))


# ══════════════════════════════════════════════════════════════════
#  SLIDE 8 — ACHIEVEMENT 3: DEEPER INSIGHTS (ROC, PR, CV)
# ══════════════════════════════════════════════════════════════════
s = cslide("Achievement 3 — Deeper Insights from Evaluation", 8)

chart_data = [
    ("ROC CURVES", "chart_37_00.png", BLUE),
    ("PRECISION-RECALL CURVES", "chart_38_00.png", GREEN),
    ("CROSS-VALIDATION STABILITY", "chart_40_01.png", PURPLE),
]
for i, (label, fname, col) in enumerate(chart_data):
    x = Inches(0.3) + i * Inches(4.3)
    section_label(s, x + Inches(0.2), Inches(1.3), label, col)
    card(s, x, Inches(1.65), Inches(4.1), Inches(2.6))
    img(s, fname, x + Inches(0.1), Inches(1.75), w=Inches(3.9), h=Inches(2.4))

interp = [
    ("ROC Curves", BLUE, [
        ("XGBoost: 0.671", 18, BLUE, True, 4),
        ("RF: 0.653  |  LR: 0.642", 17, DARK, False, 6),
        ("All models above random", 16, MGRAY, False, 2),
        ("baseline (0.5). XGBoost", 16, MGRAY, False, 2),
        ("consistently leads.", 16, MGRAY, False, 0),
    ]),
    ("Precision-Recall Curves", GREEN, [
        ("XGBoost AP: 0.228", 18, GREEN, True, 4),
        ("LR: 0.202  |  RF: 0.199", 17, DARK, False, 6),
        ("All above baseline prevalence", 16, MGRAY, False, 2),
        ("(0.114). Steep drop-off", 16, MGRAY, False, 2),
        ("confirms hard task.", 16, MGRAY, False, 0),
    ]),
    ("Cross-Validation Stability", PURPLE, [
        ("RF: 0.960  |  XGB: 0.958", 18, PURPLE, True, 4),
        ("LR: 0.654", 17, DARK, False, 6),
        ("RF and XGBoost both highly", 16, MGRAY, False, 2),
        ("stable (s = 0.0015). Tree-based", 16, MGRAY, False, 2),
        ("models vastly outperform LR.", 16, MGRAY, False, 0),
    ]),
]
for i, (title, col, items) in enumerate(interp):
    x = Inches(0.3) + i * Inches(4.3)
    card(s, x, Inches(4.45), Inches(4.1), Inches(2.35), accent=col)
    tb(s, x + Inches(0.3), Inches(4.55), Inches(3.5), Inches(0.3),
       title, 18, col, True)
    rtb(s, x + Inches(0.3), Inches(4.9), Inches(3.5), Inches(1.6), items)


# ══════════════════════════════════════════════════════════════════
#  SLIDE 9 — EXPLAINABILITY (PFI + PDP)
# ══════════════════════════════════════════════════════════════════
s = cslide("Achievement 3 — Explainability: PFI & PDP Analysis", 9)

section_label(s, Inches(0.7), Inches(1.3), "PERMUTATION FEATURE IMPORTANCE (PFI)")
card(s, Inches(0.5), Inches(1.65), Inches(6.1), Inches(2.6))
img(s, "chart_44_01.png", Inches(0.6), Inches(1.75), w=Inches(5.9), h=Inches(2.4))

section_label(s, Inches(7.1), Inches(1.3), "PARTIAL DEPENDENCE PLOTS (PDP)")
card(s, Inches(6.9), Inches(1.65), Inches(6.1), Inches(2.6))
img(s, "chart_46_01.png", Inches(7.0), Inches(1.75), w=Inches(5.9), h=Inches(2.4))

card(s, Inches(0.5), Inches(4.5), Inches(6.1), Inches(2.3), accent=RED)
tb(s, Inches(0.85), Inches(4.6), Inches(5.5), Inches(0.3),
   "Permutation Feature Importance (PFI)", 18, GOLD, True)
rtb(s, Inches(0.85), Inches(5.0), Inches(5.5), Inches(1.5), [
    ("Top features by ROC-AUC drop:", 17, DARK, True, 6),
    ("#1  number_inpatient (prior hospital visits)", 17, RED, True, 4),
    ("#2  discharge_disposition_id (where sent)", 17, ORANGE, True, 4),
    ("#3  number_diagnoses", 17, BLUE, False, 4),
    ("Prior hospital utilization dominates", 16, MGRAY, False, 0),
])

card(s, Inches(6.9), Inches(4.5), Inches(6.1), Inches(2.3), accent=ORANGE)
tb(s, Inches(7.25), Inches(4.6), Inches(5.5), Inches(0.3),
   "Partial Dependence Plots (PDP)", 18, GOLD, True)
rtb(s, Inches(7.25), Inches(5.0), Inches(5.5), Inches(1.5), [
    ("Marginal effect on predicted probability:", 17, DARK, True, 6),
    ("number_inpatient: Strong monotonic rise", 17, RED, True, 4),
    ("  0 visits -> ~10%  |  8+ visits -> ~47%", 17, DARK, False, 4),
    ("discharge_disposition: Non-home = higher", 17, ORANGE, True, 4),
    ("Clinically actionable and interpretable", 16, MGRAY, False, 0),
])


# ══════════════════════════════════════════════════════════════════
#  SLIDE 10 — THRESHOLD OPTIMIZATION & SAMPLE PREDICTIONS
# ══════════════════════════════════════════════════════════════════
s = cslide("Threshold Optimization & Sample Predictions", 10)

section_label(s, Inches(0.7), Inches(1.3), "THRESHOLD ANALYSIS")
card(s, Inches(0.5), Inches(1.65), Inches(6.1), Inches(2.6))
img(s, "chart_48_01.png", Inches(0.6), Inches(1.75), w=Inches(5.9), h=Inches(2.4))

section_label(s, Inches(7.1), Inches(1.3), "SAMPLE PREDICTIONS")
card(s, Inches(6.9), Inches(1.65), Inches(6.1), Inches(2.6))
img(s, "chart_52_00.png", Inches(7.0), Inches(1.75), w=Inches(5.9), h=Inches(2.4))

card(s, Inches(0.5), Inches(4.5), Inches(6.1), Inches(1.0), accent=RED)
tb(s, Inches(0.85), Inches(4.55), Inches(5.3), Inches(0.3),
   "BEFORE  (threshold = 0.50)", 17, RED, True)
tb(s, Inches(0.85), Inches(4.9), Inches(5.3), Inches(0.4),
   "Accuracy: 88.6%  |  Recall: 2%  |  TP: 44 / 2,263", 17, DARK)

card(s, Inches(6.9), Inches(4.5), Inches(6.1), Inches(1.0), accent=GREEN)
tb(s, Inches(7.25), Inches(4.55), Inches(5.3), Inches(0.3),
   "AFTER  (threshold = 0.15)", 17, GREEN, True)
tb(s, Inches(7.25), Inches(4.9), Inches(5.3), Inches(0.4),
   "Accuracy: 74.0%  |  Recall: 44%  |  TP: 1,004 / 2,263", 17, DARK, True)

section_label(s, Inches(0.7), Inches(5.7), "LIVE PATIENT RISK ASSESSMENT DEMO")
card(s, Inches(0.5), Inches(6.05), Inches(12.4), Inches(0.85), accent=GOLD)
rtb(s, Inches(0.85), Inches(6.15), Inches(11.8), Inches(0.6), [
    ("High-Risk: Age 65, 2 prior visits, 15 meds -> Prob: 0.19, MEDIUM RISK  |  "
     "Low-Risk: Age 35, 0 visits, 8 meds -> Prob: 0.10, LOW RISK  |  "
     "Frequent: Age 75, 5 visits, 22 meds -> Prob: 0.35, HIGH RISK", 16, DARK, False, 0),
])


# ══════════════════════════════════════════════════════════════════
#  SLIDE 11 — BIGGEST PROBLEM & SOLUTIONS
# ══════════════════════════════════════════════════════════════════
s = cslide("Biggest Problem Encountered & How I Am Dealing With It", 11)

section_label(s, Inches(0.7), Inches(1.3), "THE PROBLEM", RED)
card(s, Inches(0.5), Inches(1.65), Inches(12.3), Inches(1.0), accent=RED)
tb(s, Inches(0.85), Inches(1.75), Inches(11.7), Inches(0.8),
   "Severe class imbalance (88.6% negative vs 11.4% positive) causes high-accuracy models "
   "that are clinically useless. XGBoost at threshold 0.50 achieves 88.6% accuracy but catches "
   "only 2% of actual readmissions (44 out of 2,263).",
   17, DARK)

section_label(s, Inches(0.7), Inches(2.85), "SOLUTION 1: SMOTE Oversampling", GREEN)
card(s, Inches(0.5), Inches(3.2), Inches(6.1), Inches(2.0), accent=GREEN)
rtb(s, Inches(0.85), Inches(3.35), Inches(5.5), Inches(1.7), [
    ("\u2022  Applied on training data only (no leakage)", 17, DARK, False, 4),
    ("\u2022  Balanced: 70,421 per class", 17, DARK, False, 4),
    ("   (from 9,051 vs 70,421)", 16, MGRAY, False, 4),
    ("\u2022  Test set remains untouched", 17, DARK, False, 6),
    ("Result: Models learn from both classes", 17, BLUE, True, 0),
])

section_label(s, Inches(7.1), Inches(2.85), "SOLUTION 2: Threshold Tuning", GREEN)
card(s, Inches(6.9), Inches(3.2), Inches(6.1), Inches(2.0), accent=GREEN)
rtb(s, Inches(7.25), Inches(3.35), Inches(5.5), Inches(1.7), [
    ("\u2022  Default 0.50 is too conservative", 17, DARK, False, 4),
    ("\u2022  Swept thresholds 0.05 to 0.95", 17, DARK, False, 4),
    ("\u2022  Optimal: 0.15 (maximizes F1)", 17, DARK, False, 6),
    ("Result: Recall jumps 2% -> 44%", 17, BLUE, True, 2),
    ("(catches 22x more readmissions)", 17, BLUE, True, 0),
])

section_label(s, Inches(0.7), Inches(5.4), "CLASS IMBALANCE")
card(s, Inches(0.5), Inches(5.75), Inches(6.1), Inches(1.15))
img(s, "chart_10_01.png", Inches(0.7), Inches(5.8), w=Inches(5.7), h=Inches(1.05))

section_label(s, Inches(7.1), Inches(5.4), "SMOTE EFFECT")
card(s, Inches(6.9), Inches(5.75), Inches(6.1), Inches(1.15))
img(s, "chart_56_01.png", Inches(7.1), Inches(5.8), w=Inches(5.7), h=Inches(1.05))


# ══════════════════════════════════════════════════════════════════
#  SLIDE 12 — REVISED SCHEDULE
# ══════════════════════════════════════════════════════════════════
s = cslide("Revised Schedule", 12)

card(s, Inches(0.5), Inches(1.25), Inches(12.3), Inches(0.55), accent=GREEN)
tb(s, Inches(0.85), Inches(1.3), Inches(12), Inches(0.4),
   "The project is on schedule. No revisions needed. All Week 1-5 milestones completed on time.",
   20, GREEN, True)

section_label(s, Inches(0.7), Inches(2.05), "COMPLETED (Weeks 1-5)", GREEN)
done_items = [
    ("Week 1", "Dataset exploration & literature review"),
    ("Week 2", "Data cleaning, missing values, encoding"),
    ("Week 3", "Feature engineering & binary target"),
    ("Week 4", "Model training: LR, RF, XGBoost"),
    ("Week 5", "Evaluation, selection & midterm prep"),
]
for i, (wk, task) in enumerate(done_items):
    y = Inches(2.45) + i * Inches(0.4)
    tb(s, Inches(0.7), y, Inches(0.35), Inches(0.32), "\u2713", 18, GREEN, True)
    tb(s, Inches(1.1), y, Inches(1.1), Inches(0.32), wk, 16, DARK, True)
    tb(s, Inches(2.3), y, Inches(4.5), Inches(0.32), task, 16, DARK)

card(s, Inches(0.5), Inches(4.5), Inches(6.5), Inches(0.45), accent=ORANGE)
tb(s, Inches(0.85), Inches(4.53), Inches(6), Inches(0.35),
   "\u2605  Mid-Term Project Review -- March 3, 2026 (TODAY)", 17, ORANGE, True)

section_label(s, Inches(0.7), Inches(5.2), "UPCOMING (Weeks 6-12)", BLUE)
upcoming_items = [
    ("Week 6", "Hyperparameter tuning & cross-validation"),
    ("Week 7", "Explainability: PFI & PDP on XGBoost"),
    ("Week 8", "Visualization of predictions & results"),
    ("Wk 9-10", "Draft & write final report sections"),
    ("Wk 11-12", "Review, proofreading & submission"),
]
for i, (wk, task) in enumerate(upcoming_items):
    y = Inches(5.55) + i * Inches(0.35)
    tb(s, Inches(0.7), y, Inches(0.35), Inches(0.3), "\u25CB", 16, BLUE)
    tb(s, Inches(1.1), y, Inches(1.1), Inches(0.3), wk, 16, DARK, True)
    tb(s, Inches(2.3), y, Inches(4.5), Inches(0.3), task, 16, MGRAY)

card(s, Inches(7.5), Inches(2.0), Inches(5.2), Inches(4.8), accent=GOLD)
tb(s, Inches(7.85), Inches(2.2), Inches(4.5), Inches(0.35),
   "PROGRESS OVERVIEW", 17, GOLD, True, PP_ALIGN.CENTER)
tb(s, Inches(7.85), Inches(2.7), Inches(4.5), Inches(0.9),
   "42%", 60, GOLD, True, PP_ALIGN.CENTER)
tb(s, Inches(7.85), Inches(3.55), Inches(4.5), Inches(0.35),
   "5 of 12 weeks complete", 17, MGRAY, align=PP_ALIGN.CENTER)

bar_y = Inches(4.05)
rrect(s, Inches(8.2), bar_y, Inches(3.9), Inches(0.3), LGRAY)
rrect(s, Inches(8.2), bar_y, Inches(3.9 * 0.42), Inches(0.3), GOLD)

rtb(s, Inches(7.85), Inches(4.55), Inches(4.5), Inches(2.1), [
    ("What Remains:", 18, DARK, True, 8),
    ("\u2022  Hyperparameter tuning of XGBoost", 16, DARK, False, 3),
    ("\u2022  Full PFI + PDP explainability analysis", 16, DARK, False, 3),
    ("\u2022  Streamlit interactive dashboard", 16, DARK, False, 3),
    ("\u2022  Prediction visualization & tables", 16, DARK, False, 3),
    ("\u2022  Complete final report (all sections)", 16, DARK, False, 8),
    ("Risk assessment: LOW", 17, GREEN, True, 3),
    ("No blockers. Clear path forward.", 16, MGRAY, False, 0),
])


# ══════════════════════════════════════════════════════════════════
#  SLIDE 13 — WHY THIS PROJECT SHOULD CONTINUE
# ══════════════════════════════════════════════════════════════════
s = cslide("Why This Project Should Continue", 13)

arguments = [
    ("\u2776", "Strong Foundation Built",
     "Complete data pipeline -- from raw data (101,766 records) through cleaning, "
     "feature engineering, EDA, statistical validation, and preprocessing. "
     "Three models trained, evaluated, and XGBoost selected (ROC-AUC = 0.671).",
     BLUE),
    ("\u2777", "Clear Path to Completion",
     "Remaining work is well-defined: hyperparameter tuning (Wk 6), "
     "explainability with PFI and PDP (Wk 7), visualization (Wk 8), "
     "and report writing (Wk 9-12). Streamlit dashboard framework already built.",
     GREEN),
    ("\u2778", "Real-World Clinical Impact",
     "Hospital readmissions cost $26B+ annually. This project delivers an "
     "explainable prediction tool -- not a black box. Clinicians understand "
     "why a patient is high-risk, enabling targeted interventions.",
     ORANGE),
    ("\u2779", "On Schedule, No Blockers",
     "All 5 weeks completed on time. Biggest challenge (class imbalance) "
     "identified and addressed with SMOTE + threshold optimization. "
     "No risks or dependencies. Fully on track for April 24 deadline.",
     PURPLE),
]

for i, (num, title, desc, col) in enumerate(arguments):
    row = i // 2
    colm = i % 2
    x = Inches(0.5) + colm * Inches(6.35)
    y = Inches(1.3) + row * Inches(2.85)

    card(s, x, y, Inches(6.05), Inches(2.55), accent=col)
    tb(s, x + Inches(0.35), y + Inches(0.15), Inches(0.5), Inches(0.4),
       num, 26, col, True)
    tb(s, x + Inches(0.9), y + Inches(0.18), Inches(4.9), Inches(0.35),
       title, 20, DARK, True)
    tb(s, x + Inches(0.35), y + Inches(0.65), Inches(5.5), Inches(1.7),
       desc, 17, MGRAY)


# ══════════════════════════════════════════════════════════════════
#  SLIDE 14 — THANK YOU
# ══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
bg(s, NAVY)

rect(s, Inches(0), Inches(0), Inches(0.12), Inches(7.5), GOLD)
rect(s, Inches(0.12), Inches(0), Inches(0.04), Inches(7.5), MID_NAVY)
rect(s, Inches(11.5), Inches(0), Inches(1.833), Inches(0.08), GOLD)

tb(s, Inches(1), Inches(1.8), Inches(11.3), Inches(1.0),
   "Thank You", 52, WHITE, True, PP_ALIGN.CENTER)

accent_line(s, Inches(5.5), Inches(2.9), Inches(2.3), GOLD, 5)

tb(s, Inches(2), Inches(3.3), Inches(9.3), Inches(0.6),
   "Predictive Analytics and Explainable AI\nfor Hospital Readmission Risk",
   22, LGRAY, align=PP_ALIGN.CENTER)

tb(s, Inches(2), Inches(4.3), Inches(9.3), Inches(0.4),
   "Midterm Project Review", 20, GOLD, True, PP_ALIGN.CENTER)

tb(s, Inches(2), Inches(5.0), Inches(9.3), Inches(0.4),
   "Raj Panchal (200490453)  |  CS 719  |  March 3, 2026", 20, MGRAY, align=PP_ALIGN.CENTER)

tb(s, Inches(2), Inches(5.6), Inches(9.3), Inches(0.4),
   "Instructor: Howard J. Hamilton  |  University of Regina", 18, MGRAY, align=PP_ALIGN.CENTER)

tb(s, Inches(2), Inches(6.3), Inches(9.3), Inches(0.5),
   "Questions?", 32, GOLD, True, PP_ALIGN.CENTER)

footer(s, 14)


# ══════════════════════════════════════════════════════════════════
#  SAVE
# ══════════════════════════════════════════════════════════════════
out = "/home/user/CS-719/CS719_Midterm_Final_v2.pptx"
prs.save(out)
print(f"Saved: {out}")
print(f"Slides: {len(prs.slides)}")
