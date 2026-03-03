"""
CS 719 Midterm — V3: CLEAN, LARGE, READABLE
Design principles:
  - ONE idea per slide
  - Minimum 22pt body text, 36pt titles
  - Charts get 80%+ of slide area
  - Max 4-5 bullet points per text slide
  - BIG page numbers (20pt, bottom-right)
  - Only essential charts (6 out of 20+)
  - Visible from the last bench
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

# ── Colors ──
NAVY      = RGBColor(0x0D, 0x1B, 0x2A)
GOLD      = RGBColor(0xD4, 0xA0, 0x1E)
BLUE      = RGBColor(0x2E, 0x86, 0xC1)
GREEN     = RGBColor(0x27, 0xAE, 0x60)
ORANGE    = RGBColor(0xE6, 0x7E, 0x22)
RED       = RGBColor(0xE7, 0x4C, 0x3C)
PURPLE    = RGBColor(0x8E, 0x44, 0xAD)
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
LGRAY     = RGBColor(0xEC, 0xF0, 0xF1)
MGRAY     = RGBColor(0x7F, 0x8C, 0x8D)
DARK      = RGBColor(0x2C, 0x3E, 0x50)
LIGHT_BG  = RGBColor(0xF4, 0xF6, 0xF9)
TEAL      = RGBColor(0x00, 0x97, 0xA7)

IMG = "/tmp/nb_images"
TOTAL = 16

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)

# ── Helpers ──

def bg(sl, c):
    f = sl.background.fill; f.solid(); f.fore_color.rgb = c

def rect(sl, l, t, w, h, fill, bdr=None):
    s = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    s.fill.solid(); s.fill.fore_color.rgb = fill
    if bdr: s.line.color.rgb = bdr; s.line.width = Pt(1)
    else: s.line.fill.background()
    return s

def rrect(sl, l, t, w, h, fill, bdr=None):
    s = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l, t, w, h)
    s.fill.solid(); s.fill.fore_color.rgb = fill
    if bdr: s.line.color.rgb = bdr; s.line.width = Pt(1)
    else: s.line.fill.background()
    return s

def tb(sl, l, t, w, h, txt, sz=22, c=DARK, b=False, al=PP_ALIGN.LEFT):
    box = sl.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = txt; p.font.size = Pt(sz); p.font.color.rgb = c
    p.font.bold = b; p.font.name = "Calibri"; p.alignment = al
    p.space_after = Pt(0); p.space_before = Pt(0)
    return box

def bullet_slide(sl, l, t, w, items):
    """items: list of (text, size, color, bold, space_after)"""
    box = sl.shapes.add_textbox(l, t, w, Inches(5))
    tf = box.text_frame; tf.word_wrap = True
    for i, (txt, sz, col, bld, sa) in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = txt; p.font.size = Pt(sz); p.font.color.rgb = col
        p.font.bold = bld; p.font.name = "Calibri"
        p.space_after = Pt(sa); p.space_before = Pt(0)
    return box

def footer(sl, num):
    """BIG visible page number + subtle left text"""
    rect(sl, Inches(0), Inches(7.05), prs.slide_width, Inches(0.45), NAVY)
    tb(sl, Inches(0.5), Inches(7.1), Inches(7), Inches(0.35),
       "CS 719  |  Raj Panchal  |  Midterm Review", 16, MGRAY)
    # BIG page number
    tb(sl, Inches(11.5), Inches(7.05), Inches(1.5), Inches(0.4),
       f"{num}/{TOTAL}", 22, WHITE, True, PP_ALIGN.RIGHT)

def title_bar(sl, title):
    rect(sl, Inches(0), Inches(0), prs.slide_width, Inches(1.05), NAVY)
    rect(sl, Inches(0.6), Inches(0.85), Inches(3), Pt(5), GOLD)
    tb(sl, Inches(0.6), Inches(0.15), Inches(12), Inches(0.7),
       title, 36, WHITE, True)

def slide(title, num):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s, LIGHT_BG); title_bar(s, title); footer(s, num)
    return s

def add_img(sl, name, l, t, w=None, h=None):
    p = os.path.join(IMG, name)
    if not os.path.exists(p): return False
    kw = {"left": l, "top": t}
    if w: kw["width"] = w
    if h: kw["height"] = h
    sl.shapes.add_picture(p, **kw); return True

def oval(sl, x, y, sz, txt, fc=GOLD, tc=WHITE, ts=20):
    o = sl.shapes.add_shape(MSO_SHAPE.OVAL, x, y, sz, sz)
    o.fill.solid(); o.fill.fore_color.rgb = fc; o.line.fill.background()
    tf = o.text_frame
    tf.paragraphs[0].text = txt
    tf.paragraphs[0].font.size = Pt(ts)
    tf.paragraphs[0].font.color.rgb = tc
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE

def arrow_r(sl, x, y):
    a = sl.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, x, y, Inches(0.4), Inches(0.35))
    a.fill.solid(); a.fill.fore_color.rgb = GOLD; a.line.fill.background()


# ═══════════════════════════════════════════════════
#  SLIDE 1 — TITLE
# ═══════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
bg(s, NAVY)
rect(s, Inches(0), Inches(0), Inches(0.12), Inches(7.5), GOLD)

rect(s, Inches(1.5), Inches(1.2), Inches(4), Pt(5), GOLD)
tb(s, Inches(1.5), Inches(1.6), Inches(10.5), Inches(1.8),
   "Predictive Analytics and\nExplainable AI for Hospital\nReadmission Risk",
   44, WHITE, True)

tb(s, Inches(1.5), Inches(3.6), Inches(10), Inches(0.6),
   "Midterm Project Review", 30, GOLD, True)

rect(s, Inches(1.5), Inches(4.4), Inches(3), Pt(3), GOLD)

tb(s, Inches(1.5), Inches(4.7), Inches(10), Inches(0.5),
   "CS 719 — Data Science Project  |  Winter 2026", 24, LGRAY)

tb(s, Inches(1.5), Inches(5.4), Inches(6), Inches(0.5),
   "Raj Panchal  (200490453)", 24, WHITE, True)

tb(s, Inches(1.5), Inches(5.9), Inches(6), Inches(0.5),
   "March 3, 2026", 22, LGRAY)

tb(s, Inches(1.5), Inches(6.5), Inches(8), Inches(0.5),
   "Instructor:  Howard J. Hamilton", 22, MGRAY)

rect(s, Inches(0), Inches(7.05), prs.slide_width, Inches(0.45), RGBColor(0x08,0x10,0x1A))
tb(s, Inches(0.5), Inches(7.1), Inches(8), Inches(0.35),
   "University of Regina  |  Department of Computer Science", 16, MGRAY)
tb(s, Inches(11.5), Inches(7.05), Inches(1.5), Inches(0.4),
   f"1/{TOTAL}", 22, WHITE, True, PP_ALIGN.RIGHT)


# ═══════════════════════════════════════════════════
#  SLIDE 2 — GOAL & MOTIVATION
# ═══════════════════════════════════════════════════
s = slide("Goal & Motivation", 2)

# Goal — one big sentence
rrect(s, Inches(0.5), Inches(1.3), Inches(12.3), Inches(1.5), WHITE, RGBColor(0xDD,0xDD,0xDD))
rect(s, Inches(0.5), Inches(1.3), Inches(0.12), Inches(1.5), BLUE)
tb(s, Inches(0.9), Inches(1.4), Inches(11.5), Inches(1.3),
   "Predict whether a diabetic patient will be readmitted within 30 days "
   "and explain which clinical factors drive the prediction — "
   "enabling hospitals to intervene early.",
   26, DARK)

# 3 big stat cards — spaced out
stats = [
    ("$26 B+", "Annual cost of unplanned\nreadmissions in the U.S.", BLUE),
    ("11.4 %", "Patients in our dataset\nreadmitted within 30 days", ORANGE),
    ("Preventable", "Early risk identification\ntriggers interventions", GREEN),
]
for i, (big, desc, col) in enumerate(stats):
    x = Inches(0.5) + i * Inches(4.2)
    rrect(s, x, Inches(3.4), Inches(3.9), Inches(3.0), WHITE, RGBColor(0xDD,0xDD,0xDD))
    rect(s, x, Inches(3.4), Inches(3.9), Inches(0.08), col)
    tb(s, x + Inches(0.3), Inches(3.8), Inches(3.3), Inches(1.0),
       big, 44, col, True, PP_ALIGN.CENTER)
    tb(s, x + Inches(0.3), Inches(4.9), Inches(3.3), Inches(1.0),
       desc, 22, MGRAY, al=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════
#  SLIDE 3 — METHOD PIPELINE
# ═══════════════════════════════════════════════════
s = slide("Method — 6-Step Pipeline", 3)

steps = [
    ("1", "Data\nCleaning", BLUE),
    ("2", "Feature\nEngineering", TEAL),
    ("3", "Train 3\nModels", ORANGE),
    ("4", "Compare &\nSelect Best", RED),
    ("5", "Explain\n(PFI + PDP)", PURPLE),
    ("6", "Interactive\nDashboard", GREEN),
]
for i, (num, label, col) in enumerate(steps):
    x = Inches(0.6) + i * Inches(2.1)
    y = Inches(2.5)
    oval(s, x, y, Inches(0.7), num, col, WHITE, 24)
    tb(s, x + Inches(0.85), y + Inches(0.0), Inches(1.2), Inches(0.8),
       label, 22, DARK, True)
    if i < 5:
        arrow_r(s, x + Inches(1.85), y + Inches(0.2))

# Simple summary below
rrect(s, Inches(0.5), Inches(4.2), Inches(12.3), Inches(2.2), WHITE, RGBColor(0xDD,0xDD,0xDD))
bullet_slide(s, Inches(1.0), Inches(4.4), Inches(11), [
    ("\u2022  Cleaned 101,766 records from 130 US hospitals", 24, DARK, False, 12),
    ("\u2022  Trained Logistic Regression, Random Forest, and XGBoost", 24, DARK, False, 12),
    ("\u2022  XGBoost selected as best model (ROC-AUC = 0.671)", 24, DARK, False, 12),
    ("\u2022  Explainability via Permutation Feature Importance & Partial Dependence", 24, DARK, False, 0),
])


# ═══════════════════════════════════════════════════
#  SLIDE 4 — PROJECT SCHEDULE
# ═══════════════════════════════════════════════════
s = slide("Project Schedule", 4)

weeks = [
    ("Week 1", "Jan 27 - Feb 2", "Dataset exploration & literature review", True),
    ("Week 2", "Feb 3 - Feb 9", "Data cleaning, missing values, encoding", True),
    ("Week 3", "Feb 10 - Feb 16", "Feature engineering & binary target", True),
    ("Week 4", "Feb 17 - Feb 23", "Model training: LR, RF, XGBoost", True),
    ("Week 5", "Feb 24 - Mar 2", "Evaluation, model selection, midterm prep", True),
    ("", "Mar 3", "MILESTONE: Mid-Term Review (TODAY)", None),
    ("Week 6-7", "Mar 4 - Mar 17", "Hyperparameter tuning & explainability", False),
    ("Week 8", "Mar 18 - Mar 24", "Visualization of predictions & results", False),
    ("Wk 9-10", "Mar 25 - Apr 7", "Draft report: all sections", False),
    ("Wk 11-12", "Apr 8 - Apr 23", "Review, proofreading & submission", False),
    ("", "Apr 24", "MILESTONE: Final Report Due", None),
]

y0 = Inches(1.25)
rrect(s, Inches(0.4), y0, Inches(12.5), Inches(0.55), NAVY)
tb(s, Inches(0.7), y0 + Inches(0.08), Inches(1.5), Inches(0.4), "Week", 20, WHITE, True)
tb(s, Inches(2.2), y0 + Inches(0.08), Inches(2.2), Inches(0.4), "Dates", 20, WHITE, True)
tb(s, Inches(4.5), y0 + Inches(0.08), Inches(5.5), Inches(0.4), "Task", 20, WHITE, True)
tb(s, Inches(10.5), y0 + Inches(0.08), Inches(2.2), Inches(0.4), "Status", 20, WHITE, True)

for i, (wk, dates, task, done) in enumerate(weeks):
    y = y0 + Inches(0.58) + i * Inches(0.52)
    if done is None:
        rrect(s, Inches(0.4), y, Inches(12.5), Inches(0.52), RGBColor(0xFF,0xF3,0xE0))
        tb(s, Inches(2.2), y + Inches(0.06), Inches(2.2), Inches(0.4), dates, 20, ORANGE, True)
        tb(s, Inches(4.5), y + Inches(0.06), Inches(5.5), Inches(0.4), task, 20, ORANGE, True)
        tb(s, Inches(10.5), y + Inches(0.06), Inches(2.2), Inches(0.4),
           "\u2605", 22, ORANGE, True, PP_ALIGN.CENTER)
    else:
        bgc = WHITE if i % 2 == 0 else RGBColor(0xF0,0xF4,0xF8)
        rect(s, Inches(0.4), y, Inches(12.5), Inches(0.52), bgc)
        tb(s, Inches(0.7), y + Inches(0.06), Inches(1.5), Inches(0.4), wk, 20, DARK, True)
        tb(s, Inches(2.2), y + Inches(0.06), Inches(2.2), Inches(0.4), dates, 20, MGRAY)
        tb(s, Inches(4.5), y + Inches(0.06), Inches(5.5), Inches(0.4), task, 20, DARK)
        if done:
            tb(s, Inches(10.5), y + Inches(0.06), Inches(2.2), Inches(0.4),
               "\u2713 Done", 20, GREEN, True, PP_ALIGN.CENTER)
        else:
            tb(s, Inches(10.5), y + Inches(0.06), Inches(2.2), Inches(0.4),
               "Upcoming", 20, MGRAY, al=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════
#  SLIDE 5 — DATA PREPARATION (text only)
# ═══════════════════════════════════════════════════
s = slide("Achievement 1 — Data Preparation", 5)

bullet_slide(s, Inches(0.8), Inches(1.4), Inches(11.5), [
    ("\u2022  Cleaned 101,766 records from 130 US hospitals", 26, DARK, False, 16),
    ("\u2022  Dropped 4 high-null + 2 zero-variance columns", 26, DARK, False, 16),
    ("\u2022  Removed 2,426 expired/hospice rows", 26, DARK, False, 16),
    ("\u2022  Engineered 4 new features: total_visits, num_med_changed,\n"
     "   num_med_active, age_numeric", 26, DARK, False, 16),
    ("\u2022  Binary target: readmitted <30 days = 1 (11.4%),  else = 0 (88.6%)", 26, DARK, False, 16),
])

# Before/After boxes at bottom
rrect(s, Inches(0.5), Inches(5.4), Inches(5.8), Inches(1.2), WHITE, RED)
rect(s, Inches(0.5), Inches(5.4), Inches(0.12), Inches(1.2), RED)
tb(s, Inches(0.9), Inches(5.5), Inches(5), Inches(0.4),
   "BEFORE", 22, RED, True)
tb(s, Inches(0.9), Inches(5.95), Inches(5), Inches(0.5),
   "101,766 rows  \u00d7  50 columns", 26, DARK, True)

rrect(s, Inches(7.0), Inches(5.4), Inches(5.8), Inches(1.2), WHITE, GREEN)
rect(s, Inches(7.0), Inches(5.4), Inches(0.12), Inches(1.2), GREEN)
tb(s, Inches(7.4), Inches(5.5), Inches(5), Inches(0.4),
   "AFTER", 22, GREEN, True)
tb(s, Inches(7.4), Inches(5.95), Inches(5), Inches(0.5),
   "99,340 rows  \u00d7  23 columns", 26, DARK, True)


# ═══════════════════════════════════════════════════
#  SLIDE 6 — CHART: Target Distribution (FULL SLIDE)
# ═══════════════════════════════════════════════════
s = slide("Target Variable Distribution", 6)

# Chart takes most of the slide
rrect(s, Inches(0.4), Inches(1.2), Inches(8.5), Inches(5.5), WHITE, RGBColor(0xDD,0xDD,0xDD))
add_img(s, "chart_19_00.png", Inches(0.6), Inches(1.3), w=Inches(8.1), h=Inches(5.3))

# Key takeaway on the right
rrect(s, Inches(9.2), Inches(1.2), Inches(3.8), Inches(5.5), WHITE, RGBColor(0xDD,0xDD,0xDD))
rect(s, Inches(9.2), Inches(1.2), Inches(3.8), Inches(0.08), ORANGE)
tb(s, Inches(9.5), Inches(1.5), Inches(3.2), Inches(0.5),
   "Key Takeaway", 24, GOLD, True)

bullet_slide(s, Inches(9.5), Inches(2.2), Inches(3.2), [
    ("88.6%", 40, GREEN, True, 4),
    ("Not readmitted", 22, MGRAY, False, 24),
    ("11.4%", 40, RED, True, 4),
    ("Readmitted\nwithin 30 days", 22, MGRAY, False, 24),
    ("Severe class\nimbalance!", 24, ORANGE, True, 0),
])


# ═══════════════════════════════════════════════════
#  SLIDE 7 — CHART: Readmission by Inpatient Visits (FULL)
# ═══════════════════════════════════════════════════
s = slide("Key Discovery — Readmission by Prior Visits", 7)

rrect(s, Inches(0.4), Inches(1.2), Inches(8.5), Inches(5.5), WHITE, RGBColor(0xDD,0xDD,0xDD))
add_img(s, "chart_24_00.png", Inches(0.6), Inches(1.3), w=Inches(8.1), h=Inches(5.3))

rrect(s, Inches(9.2), Inches(1.2), Inches(3.8), Inches(5.5), WHITE, RGBColor(0xDD,0xDD,0xDD))
rect(s, Inches(9.2), Inches(1.2), Inches(3.8), Inches(0.08), RED)
tb(s, Inches(9.5), Inches(1.5), Inches(3.2), Inches(0.5),
   "Key Finding", 24, GOLD, True)

bullet_slide(s, Inches(9.5), Inches(2.2), Inches(3.2), [
    ("Prior inpatient\nvisits = strongest\npredictor", 24, DARK, True, 20),
    ("0 visits", 22, GREEN, True, 2),
    ("9% readmission", 22, GREEN, False, 16),
    ("4 visits", 22, ORANGE, True, 2),
    ("25% readmission", 22, ORANGE, False, 16),
    ("8 visits", 22, RED, True, 2),
    ("47% readmission", 22, RED, False, 0),
])


# ═══════════════════════════════════════════════════
#  SLIDE 8 — MODEL TRAINING (3 simple cards)
# ═══════════════════════════════════════════════════
s = slide("Achievement 2 — Model Training & Selection", 8)

models = [
    ("Logistic\nRegression", "Linear Baseline",
     "Accuracy: 64.0%\nROC-AUC: 0.642\nRecall: 55%", BLUE),
    ("Random\nForest", "Ensemble (Bagging)",
     "Accuracy: 88.0%\nROC-AUC: 0.653\nRecall: 6%", PURPLE),
    ("XGBoost", "Ensemble (Boosting)",
     "Accuracy: 88.6%\nROC-AUC: 0.671\nRecall: 2%", GREEN),
]
for i, (name, mtype, metrics, col) in enumerate(models):
    x = Inches(0.5) + i * Inches(4.2)
    rrect(s, x, Inches(1.4), Inches(3.9), Inches(4.2), WHITE, RGBColor(0xDD,0xDD,0xDD))
    rect(s, x, Inches(1.4), Inches(3.9), Inches(0.08), col)
    tb(s, x + Inches(0.3), Inches(1.7), Inches(3.3), Inches(1.0),
       name, 32, col, True, PP_ALIGN.CENTER)
    tb(s, x + Inches(0.3), Inches(2.7), Inches(3.3), Inches(0.4),
       mtype, 20, MGRAY, al=PP_ALIGN.CENTER)
    rect(s, x + Inches(0.5), Inches(3.2), Inches(2.9), Pt(3), col)
    tb(s, x + Inches(0.3), Inches(3.5), Inches(3.3), Inches(1.5),
       metrics, 26, DARK, True, PP_ALIGN.CENTER)

# Winner badge
rrect(s, Inches(8.7), Inches(5.8), Inches(4.1), Inches(0.6), GREEN)
tb(s, Inches(8.7), Inches(5.85), Inches(4.1), Inches(0.5),
   "\u2b50  XGBoost Selected — Best ROC-AUC", 22, WHITE, True, PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════
#  SLIDE 9 — CHART: Confusion Matrices (FULL)
# ═══════════════════════════════════════════════════
s = slide("Model Evaluation — Confusion Matrices", 9)

rrect(s, Inches(0.4), Inches(1.2), Inches(12.5), Inches(5.5), WHITE, RGBColor(0xDD,0xDD,0xDD))
add_img(s, "chart_36_00.png", Inches(0.8), Inches(1.4), w=Inches(11.7), h=Inches(5.1))


# ═══════════════════════════════════════════════════
#  SLIDE 10 — CHART: ROC Curves (FULL)
# ═══════════════════════════════════════════════════
s = slide("Model Evaluation — ROC Curves", 10)

rrect(s, Inches(0.4), Inches(1.2), Inches(8.5), Inches(5.5), WHITE, RGBColor(0xDD,0xDD,0xDD))
add_img(s, "chart_37_00.png", Inches(0.6), Inches(1.3), w=Inches(8.1), h=Inches(5.3))

rrect(s, Inches(9.2), Inches(1.2), Inches(3.8), Inches(5.5), WHITE, RGBColor(0xDD,0xDD,0xDD))
rect(s, Inches(9.2), Inches(1.2), Inches(3.8), Inches(0.08), BLUE)
tb(s, Inches(9.5), Inches(1.5), Inches(3.2), Inches(0.5),
   "ROC-AUC Scores", 24, GOLD, True)

bullet_slide(s, Inches(9.5), Inches(2.3), Inches(3.2), [
    ("XGBoost", 24, GREEN, True, 2),
    ("0.671", 40, GREEN, True, 16),
    ("Random Forest", 24, PURPLE, True, 2),
    ("0.653", 40, PURPLE, True, 16),
    ("Logistic Reg.", 24, BLUE, True, 2),
    ("0.642", 40, BLUE, True, 16),
    ("All above 0.5\nrandom baseline", 20, MGRAY, False, 0),
])


# ═══════════════════════════════════════════════════
#  SLIDE 11 — CHART: PFI Explainability (FULL)
# ═══════════════════════════════════════════════════
s = slide("Achievement 3 — Permutation Feature Importance", 11)

rrect(s, Inches(0.4), Inches(1.2), Inches(8.5), Inches(5.5), WHITE, RGBColor(0xDD,0xDD,0xDD))
add_img(s, "chart_44_01.png", Inches(0.6), Inches(1.3), w=Inches(8.1), h=Inches(5.3))

rrect(s, Inches(9.2), Inches(1.2), Inches(3.8), Inches(5.5), WHITE, RGBColor(0xDD,0xDD,0xDD))
rect(s, Inches(9.2), Inches(1.2), Inches(3.8), Inches(0.08), GOLD)
tb(s, Inches(9.5), Inches(1.5), Inches(3.2), Inches(0.5),
   "Top Features", 24, GOLD, True)

bullet_slide(s, Inches(9.5), Inches(2.3), Inches(3.2), [
    ("#1", 22, RED, True, 2),
    ("number_inpatient", 22, RED, True, 4),
    ("(prior hospital visits)", 18, MGRAY, False, 20),
    ("#2", 22, ORANGE, True, 2),
    ("discharge_\ndisposition_id", 22, ORANGE, True, 4),
    ("(where patient sent)", 18, MGRAY, False, 20),
    ("#3", 22, BLUE, True, 2),
    ("number_diagnoses", 22, BLUE, True, 0),
])


# ═══════════════════════════════════════════════════
#  SLIDE 12 — CHART: Threshold Optimization (FULL)
# ═══════════════════════════════════════════════════
s = slide("Threshold Optimization", 12)

rrect(s, Inches(0.4), Inches(1.2), Inches(8.5), Inches(5.5), WHITE, RGBColor(0xDD,0xDD,0xDD))
add_img(s, "chart_48_01.png", Inches(0.6), Inches(1.3), w=Inches(8.1), h=Inches(5.3))

rrect(s, Inches(9.2), Inches(1.2), Inches(3.8), Inches(2.5), WHITE, RED)
rect(s, Inches(9.2), Inches(1.2), Inches(0.12), Inches(2.5), RED)
tb(s, Inches(9.6), Inches(1.4), Inches(3.2), Inches(0.4),
   "BEFORE (t = 0.50)", 22, RED, True)
bullet_slide(s, Inches(9.6), Inches(1.9), Inches(3.2), [
    ("Recall: 2%", 28, DARK, True, 8),
    ("Only 44 of 2,263\nreadmissions caught", 22, MGRAY, False, 0),
])

rrect(s, Inches(9.2), Inches(4.0), Inches(3.8), Inches(2.7), WHITE, GREEN)
rect(s, Inches(9.2), Inches(4.0), Inches(0.12), Inches(2.7), GREEN)
tb(s, Inches(9.6), Inches(4.2), Inches(3.2), Inches(0.4),
   "AFTER (t = 0.15)", 22, GREEN, True)
bullet_slide(s, Inches(9.6), Inches(4.7), Inches(3.2), [
    ("Recall: 44%", 28, DARK, True, 8),
    ("1,004 of 2,263\nreadmissions caught", 22, DARK, True, 8),
    ("22\u00d7 improvement!", 26, GREEN, True, 0),
])


# ═══════════════════════════════════════════════════
#  SLIDE 13 — BIGGEST PROBLEM & SOLUTIONS
# ═══════════════════════════════════════════════════
s = slide("Biggest Problem & Solutions", 13)

# Problem
rrect(s, Inches(0.5), Inches(1.3), Inches(12.3), Inches(1.4), WHITE, RED)
rect(s, Inches(0.5), Inches(1.3), Inches(0.12), Inches(1.4), RED)
tb(s, Inches(0.9), Inches(1.4), Inches(2), Inches(0.4),
   "THE PROBLEM", 22, RED, True)
tb(s, Inches(0.9), Inches(1.85), Inches(11.5), Inches(0.7),
   "Severe class imbalance (88.6% vs 11.4%) — XGBoost at default threshold\n"
   "achieves 88.6% accuracy but catches only 2% of actual readmissions.",
   24, DARK)

# Solution 1
rrect(s, Inches(0.5), Inches(3.1), Inches(5.9), Inches(3.4), WHITE, GREEN)
rect(s, Inches(0.5), Inches(3.1), Inches(0.12), Inches(3.4), GREEN)
tb(s, Inches(0.9), Inches(3.2), Inches(5.2), Inches(0.5),
   "SOLUTION 1: SMOTE", 24, GREEN, True)
bullet_slide(s, Inches(0.9), Inches(3.8), Inches(5.2), [
    ("\u2022  Oversample minority class on\n   training data only", 24, DARK, False, 12),
    ("\u2022  Balanced: 70,421 per class", 24, DARK, False, 12),
    ("\u2022  Test set untouched (no leakage)", 24, DARK, False, 0),
])

# Solution 2
rrect(s, Inches(6.9), Inches(3.1), Inches(5.9), Inches(3.4), WHITE, GREEN)
rect(s, Inches(6.9), Inches(3.1), Inches(0.12), Inches(3.4), GREEN)
tb(s, Inches(7.3), Inches(3.2), Inches(5.2), Inches(0.5),
   "SOLUTION 2: Threshold Tuning", 24, GREEN, True)
bullet_slide(s, Inches(7.3), Inches(3.8), Inches(5.2), [
    ("\u2022  Default 0.50 too conservative", 24, DARK, False, 12),
    ("\u2022  Optimal threshold: 0.15", 24, DARK, False, 12),
    ("\u2022  Recall: 2% \u2192 44%\n   (catches 22\u00d7 more)", 24, BLUE, True, 0),
])


# ═══════════════════════════════════════════════════
#  SLIDE 14 — REVISED SCHEDULE
# ═══════════════════════════════════════════════════
s = slide("Revised Schedule & Progress", 14)

# On schedule banner
rrect(s, Inches(0.5), Inches(1.3), Inches(12.3), Inches(0.7), WHITE, GREEN)
rect(s, Inches(0.5), Inches(1.3), Inches(0.12), Inches(0.7), GREEN)
tb(s, Inches(0.9), Inches(1.35), Inches(11.5), Inches(0.55),
   "On schedule. No revisions needed. All Week 1-5 milestones completed on time.",
   24, GREEN, True)

# Left: Done + Upcoming
bullet_slide(s, Inches(0.8), Inches(2.3), Inches(7), [
    ("COMPLETED (Weeks 1-5)", 22, GREEN, True, 12),
    ("\u2713  Dataset exploration & literature review", 22, DARK, False, 6),
    ("\u2713  Data cleaning, missing values, encoding", 22, DARK, False, 6),
    ("\u2713  Feature engineering & binary target", 22, DARK, False, 6),
    ("\u2713  Model training: LR, RF, XGBoost", 22, DARK, False, 6),
    ("\u2713  Evaluation, selection & midterm prep", 22, DARK, False, 16),
    ("UPCOMING (Weeks 6-12)", 22, BLUE, True, 12),
    ("\u25CB  Hyperparameter tuning & explainability", 22, MGRAY, False, 6),
    ("\u25CB  Visualization & Streamlit dashboard", 22, MGRAY, False, 6),
    ("\u25CB  Final report (all sections)", 22, MGRAY, False, 0),
])

# Right: big progress indicator
rrect(s, Inches(8.5), Inches(2.3), Inches(4.3), Inches(4.4), WHITE, RGBColor(0xDD,0xDD,0xDD))
rect(s, Inches(8.5), Inches(2.3), Inches(4.3), Inches(0.08), GOLD)
tb(s, Inches(8.8), Inches(2.6), Inches(3.7), Inches(0.5),
   "PROGRESS", 24, GOLD, True, PP_ALIGN.CENTER)
tb(s, Inches(8.8), Inches(3.2), Inches(3.7), Inches(1.2),
   "42%", 72, GOLD, True, PP_ALIGN.CENTER)
tb(s, Inches(8.8), Inches(4.4), Inches(3.7), Inches(0.5),
   "5 of 12 weeks", 24, MGRAY, al=PP_ALIGN.CENTER)

# Progress bar
rrect(s, Inches(9.0), Inches(5.1), Inches(3.3), Inches(0.4), LGRAY)
rrect(s, Inches(9.0), Inches(5.1), Inches(3.3 * 0.42), Inches(0.4), GOLD)

tb(s, Inches(8.8), Inches(5.7), Inches(3.7), Inches(0.5),
   "Risk: LOW", 24, GREEN, True, PP_ALIGN.CENTER)
tb(s, Inches(8.8), Inches(6.15), Inches(3.7), Inches(0.4),
   "No blockers", 20, MGRAY, al=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════
#  SLIDE 15 — WHY CONTINUE
# ═══════════════════════════════════════════════════
s = slide("Why This Project Should Continue", 15)

args = [
    ("\u2776", "Strong Foundation Built",
     "Complete pipeline from 101,766 raw records\nto trained, evaluated XGBoost model.", BLUE),
    ("\u2777", "Clear Path to Completion",
     "Remaining work well-defined:\ntuning, explainability, dashboard, report.", GREEN),
    ("\u2778", "Real-World Clinical Impact",
     "Readmissions cost $26B+. Explainable\npredictions enable targeted interventions.", ORANGE),
    ("\u2779", "On Schedule, No Blockers",
     "All 5 weeks done on time. Class imbalance\nsolved. On track for April 24 deadline.", PURPLE),
]
for i, (num, title, desc, col) in enumerate(args):
    row = i // 2
    colm = i % 2
    x = Inches(0.5) + colm * Inches(6.35)
    y = Inches(1.3) + row * Inches(2.85)

    rrect(s, x, y, Inches(6.05), Inches(2.55), WHITE, RGBColor(0xDD,0xDD,0xDD))
    rect(s, x, y, Inches(0.12), Inches(2.55), col)

    tb(s, x + Inches(0.4), y + Inches(0.2), Inches(0.5), Inches(0.5),
       num, 32, col, True)
    tb(s, x + Inches(1.0), y + Inches(0.25), Inches(4.8), Inches(0.5),
       title, 26, DARK, True)
    tb(s, x + Inches(0.5), y + Inches(0.9), Inches(5.3), Inches(1.4),
       desc, 22, MGRAY)


# ═══════════════════════════════════════════════════
#  SLIDE 16 — THANK YOU
# ═══════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
bg(s, NAVY)
rect(s, Inches(0), Inches(0), Inches(0.12), Inches(7.5), GOLD)

tb(s, Inches(1), Inches(1.8), Inches(11.3), Inches(1.2),
   "Thank You", 60, WHITE, True, PP_ALIGN.CENTER)

rect(s, Inches(5.5), Inches(3.1), Inches(2.3), Pt(5), GOLD)

tb(s, Inches(2), Inches(3.5), Inches(9.3), Inches(0.7),
   "Predictive Analytics and Explainable AI\nfor Hospital Readmission Risk",
   26, LGRAY, al=PP_ALIGN.CENTER)

tb(s, Inches(2), Inches(4.5), Inches(9.3), Inches(0.5),
   "Midterm Project Review  |  CS 719", 24, GOLD, True, PP_ALIGN.CENTER)

tb(s, Inches(2), Inches(5.2), Inches(9.3), Inches(0.5),
   "Raj Panchal (200490453)  |  March 3, 2026", 22, LGRAY, al=PP_ALIGN.CENTER)

tb(s, Inches(2), Inches(5.8), Inches(9.3), Inches(0.5),
   "Instructor: Howard J. Hamilton  |  University of Regina", 22, MGRAY, al=PP_ALIGN.CENTER)

tb(s, Inches(2), Inches(6.5), Inches(9.3), Inches(0.6),
   "Questions?", 40, GOLD, True, PP_ALIGN.CENTER)

rect(s, Inches(0), Inches(7.05), prs.slide_width, Inches(0.45), RGBColor(0x08,0x10,0x1A))
tb(s, Inches(11.5), Inches(7.05), Inches(1.5), Inches(0.4),
   f"16/{TOTAL}", 22, WHITE, True, PP_ALIGN.RIGHT)


# ═══════════════════════════════════════════════════
out = "/home/user/CS-719/CS719_Midterm_Final_v3.pptx"
prs.save(out)
print(f"Saved: {out}")
print(f"Slides: {len(prs.slides)}")
