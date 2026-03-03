"""
CS 719 — Midterm Project Review Presentation
~11 slides, ~10 minutes, Board of Directors audience.

Follows the evaluation rubric exactly:
  1. Title
  2. Goal, Motivation & Method
  3. Pictorial Overview of Project Design
  4. Original Project Schedule
  5. Achievement 1 — Data Preparation & Exploratory Analysis
  6. Achievement 2 — Model Training, Evaluation & Selection
  7. Achievement 3 (optional) — Key Clinical Discoveries
  8. Biggest Problem Encountered & How I Am Dealing With It
  9. Revised Schedule
 10. Convincing Argument — Why This Project Should Continue
 11. Thank You / Questions
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

# ── Colour palette ──────────────────────────────────────────────
NAVY       = RGBColor(0x1B, 0x1F, 0x3B)
DEEP_NAVY  = RGBColor(0x0F, 0x13, 0x2A)
BLUE       = RGBColor(0x00, 0x96, 0xD6)
GREEN      = RGBColor(0x00, 0xC8, 0x53)
ORANGE     = RGBColor(0xFF, 0x57, 0x22)
RED        = RGBColor(0xE5, 0x39, 0x35)
PURPLE     = RGBColor(0x7B, 0x1F, 0xA2)
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
LGRAY      = RGBColor(0xE0, 0xE0, 0xE0)
MGRAY      = RGBColor(0x9E, 0x9E, 0x9E)
DARK       = RGBColor(0x33, 0x33, 0x33)
LIGHT_BG   = RGBColor(0xF5, 0xF7, 0xFA)

IMG = "/tmp/nb_images"
TOTAL = 11

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)

# ── Helpers ──────────────────────────────────────────────────────

def bg(slide, color):
    f = slide.background.fill; f.solid(); f.fore_color.rgb = color

def rect(slide, l, t, w, h, fill, border=None):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    s.fill.solid(); s.fill.fore_color.rgb = fill
    if border: s.line.color.rgb = border; s.line.width = Pt(1)
    else: s.line.fill.background()
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
    """items: list of (text, size, color, bold, space_after)"""
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame; tf.word_wrap = True
    for i, (txt, sz, col, bld, sa) in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = txt; p.font.size = Pt(sz); p.font.color.rgb = col
        p.font.bold = bld; p.font.name = font
        p.space_after = Pt(sa); p.space_before = Pt(0)
    return box

def accent_line(slide, l, t, w, color=BLUE, thick=4):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, Pt(thick))
    s.fill.solid(); s.fill.fore_color.rgb = color; s.line.fill.background()

def footer(slide, num):
    rect(slide, Inches(0), Inches(7.25), prs.slide_width, Inches(0.25), NAVY)
    tb(slide, Inches(0.4), Inches(7.25), Inches(5), Inches(0.25),
       "CS 719  |  Midterm Project Review  |  Raj Panchal", 9, MGRAY)
    tb(slide, Inches(11.5), Inches(7.25), Inches(1.6), Inches(0.25),
       f"{num} / {TOTAL}", 9, LGRAY, align=PP_ALIGN.RIGHT)

def card(slide, l, t, w, h, fill=WHITE, border=RGBColor(0xDD, 0xDD, 0xDD)):
    rect(slide, l + Inches(0.03), t + Inches(0.03), w, h, RGBColor(0xCC,0xCC,0xCC))
    return rect(slide, l, t, w, h, fill, border)

def title_bar(slide, title_text):
    rect(slide, Inches(0), Inches(0), prs.slide_width, Inches(1.05), NAVY)
    tb(slide, Inches(0.6), Inches(0.18), Inches(11), Inches(0.7),
       title_text, 28, WHITE, True)
    accent_line(slide, Inches(0.6), Inches(0.92), Inches(2.5), BLUE, 3)

def cslide(title, num):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s, LIGHT_BG); title_bar(s, title); footer(s, num)
    return s

def img(slide, name, l, t, w=None, h=None):
    p = os.path.join(IMG, name)
    if not os.path.exists(p): return False
    kw = {"left": l, "top": t}
    if w: kw["width"] = w
    if h: kw["height"] = h
    slide.shapes.add_picture(p, **kw); return True

def oval(slide, x, y, sz, text, fill_c=BLUE, txt_c=WHITE, txt_sz=18):
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
    a.fill.solid(); a.fill.fore_color.rgb = BLUE; a.line.fill.background()

def arrow_d(slide, x, y, w=Inches(0.25), h=Inches(0.3)):
    a = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, x, y, w, h)
    a.fill.solid(); a.fill.fore_color.rgb = BLUE; a.line.fill.background()

# ══════════════════════════════════════════════════════════════════
#  SLIDE 1 — TITLE
# ══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
bg(s, NAVY)
rect(s, Inches(0), Inches(0), Inches(0.12), Inches(7.5), BLUE)

tb(s, Inches(1.2), Inches(1.0), Inches(11), Inches(0.5),
   "MIDTERM PROJECT REVIEW", 16, BLUE, True)

tb(s, Inches(1.2), Inches(1.8), Inches(11), Inches(1.4),
   "Hospital Readmission Prediction\nfor Diabetic Patients",
   44, WHITE, True)

tb(s, Inches(1.2), Inches(3.5), Inches(11), Inches(0.6),
   "Diabetes 130-US Hospitals  |  Explainable Machine Learning",
   22, LGRAY)

accent_line(s, Inches(1.2), Inches(4.4), Inches(3), BLUE, 4)

tb(s, Inches(1.2), Inches(5.2), Inches(6), Inches(0.4),
   "Raj Panchal", 24, WHITE, True)
tb(s, Inches(1.2), Inches(5.7), Inches(6), Inches(0.4),
   "CS 719  |  March 3, 2026", 18, MGRAY)

footer(s, 1)

# ══════════════════════════════════════════════════════════════════
#  SLIDE 2 — GOAL, MOTIVATION & METHOD
# ══════════════════════════════════════════════════════════════════
s = cslide("Goal, Motivation & Method", 2)

# --- Goal ---
card(s, Inches(0.5), Inches(1.25), Inches(12.3), Inches(1.35))
tb(s, Inches(0.8), Inches(1.3), Inches(1.0), Inches(0.3),
   "GOAL", 12, BLUE, True)
tb(s, Inches(0.8), Inches(1.65), Inches(11.7), Inches(0.8),
   "Build a machine learning system that predicts whether a diabetic patient will be "
   "readmitted to the hospital within 30 days of discharge, and explain which clinical "
   "factors drive the prediction — enabling hospitals to intervene early and reduce "
   "costly readmissions.", 17, DARK)

# --- Motivation (3 cards) ---
tb(s, Inches(0.8), Inches(2.85), Inches(5), Inches(0.35),
   "WHY IT MATTERS", 12, BLUE, True)

motiv = [
    ("$26B+", "Annual cost of unplanned\nhospital readmissions\nin the U.S.", BLUE),
    ("11.4%", "Diabetic patients in our\ndataset readmitted\nwithin 30 days", ORANGE),
    ("Preventable", "Early risk identification\ncan trigger targeted\ninterventions", GREEN),
]
for i, (stat, desc, col) in enumerate(motiv):
    x = Inches(0.5) + i * Inches(4.15)
    card(s, x, Inches(3.2), Inches(3.85), Inches(1.7))
    tb(s, x + Inches(0.25), Inches(3.35), Inches(3.35), Inches(0.6),
       stat, 34, col, True, PP_ALIGN.CENTER)
    tb(s, x + Inches(0.25), Inches(3.95), Inches(3.35), Inches(0.8),
       desc, 14, MGRAY, align=PP_ALIGN.CENTER)

# --- Method ---
tb(s, Inches(0.8), Inches(5.2), Inches(5), Inches(0.35),
   "METHOD", 12, BLUE, True)

card(s, Inches(0.5), Inches(5.55), Inches(12.3), Inches(1.4))

method_steps = [
    ("1", "Data\nCleaning"),
    ("2", "Feature\nEngineering"),
    ("3", "Train 3\nModels"),
    ("4", "Compare &\nSelect Best"),
    ("5", "Explain\n(PFI + PDP)"),
    ("6", "Interactive\nDashboard"),
]
for i, (num, label) in enumerate(method_steps):
    x = Inches(0.8) + i * Inches(2.0)
    y = Inches(5.7)
    oval(s, x, y, Inches(0.45), num, BLUE, WHITE, 14)
    tb(s, x + Inches(0.55), y - Inches(0.02), Inches(1.3), Inches(0.55),
       label, 12, DARK)
    if i < 5:
        arrow_r(s, x + Inches(1.7), y + Inches(0.1), Inches(0.25), Inches(0.25))

# ══════════════════════════════════════════════════════════════════
#  SLIDE 3 — PICTORIAL OVERVIEW (Project Design Flow)
# ══════════════════════════════════════════════════════════════════
s = cslide("Pictorial Overview — Project Design", 3)

# === ROW 1: Data Pipeline ===
row1_y = Inches(1.35)
row1_boxes = [
    ("Raw Dataset", "101,766 records\n50 features\n130 US hospitals", BLUE),
    ("Data Cleaning", "Drop high-null cols\nRemove expired rows\n99,340 \u00d7 42", RGBColor(0x26,0xA6,0x9A)),
    ("Feature\nEngineering", "4 new features\nBinary target\n99,340 \u00d7 23", RGBColor(0x42,0xA5,0xF5)),
    ("Exploratory\nData Analysis", "Distributions\nCorrelations\nStatistical tests", PURPLE),
]
for i, (title, desc, col) in enumerate(row1_boxes):
    x = Inches(0.4) + i * Inches(3.25)
    bx = rect(s, x, row1_y, Inches(2.85), Inches(1.65), WHITE, RGBColor(0xDD,0xDD,0xDD))
    # Color top stripe
    rect(s, x, row1_y, Inches(2.85), Inches(0.06), col)
    tb(s, x + Inches(0.15), row1_y + Inches(0.15), Inches(2.55), Inches(0.4),
       title, 15, col, True, PP_ALIGN.CENTER)
    tb(s, x + Inches(0.15), row1_y + Inches(0.6), Inches(2.55), Inches(0.9),
       desc, 12, MGRAY, align=PP_ALIGN.CENTER)
    if i < 3:
        arrow_r(s, x + Inches(2.9), row1_y + Inches(0.65))

# Down arrow from row 1 to row 2
arrow_d(s, Inches(6.55), Inches(3.1))

# === ROW 2: Modeling Pipeline ===
row2_y = Inches(3.6)
row2_boxes = [
    ("Preprocessing", "One-Hot Encode\n80/20 split\nSMOTE + Scale", RGBColor(0xFF,0xB3,0x00)),
    ("Model Training", "Logistic Regression\nRandom Forest\nXGBoost", ORANGE),
    ("Evaluation &\nSelection", "ROC-AUC, F1, CV\nConfusion matrices\nBest: XGBoost", RED),
]
for i, (title, desc, col) in enumerate(row2_boxes):
    x = Inches(0.4) + i * Inches(3.25)
    rect(s, x, row2_y, Inches(2.85), Inches(1.65), WHITE, RGBColor(0xDD,0xDD,0xDD))
    rect(s, x, row2_y, Inches(2.85), Inches(0.06), col)
    tb(s, x + Inches(0.15), row2_y + Inches(0.15), Inches(2.55), Inches(0.4),
       title, 15, col, True, PP_ALIGN.CENTER)
    tb(s, x + Inches(0.15), row2_y + Inches(0.6), Inches(2.55), Inches(0.9),
       desc, 12, MGRAY, align=PP_ALIGN.CENTER)
    if i < 2:
        arrow_r(s, x + Inches(2.9), row2_y + Inches(0.65))

# Down arrow from row 2 to row 3
arrow_d(s, Inches(6.55), Inches(5.35))

# === ROW 3: Remaining work ===
row3_y = Inches(5.8)
row3_boxes = [
    ("Explainability", "PFI + PDP\non best model", GREEN),
    ("Dashboard", "Streamlit app\nwhat-if analysis", RGBColor(0x00,0x97,0xA7)),
    ("Final Report", "Complete\nwrite-up", NAVY),
]
for i, (title, desc, col) in enumerate(row3_boxes):
    x = Inches(0.4) + i * Inches(3.25)
    rect(s, x, row3_y, Inches(2.85), Inches(1.15), WHITE, RGBColor(0xDD,0xDD,0xDD))
    rect(s, x, row3_y, Inches(2.85), Inches(0.06), col)
    tb(s, x + Inches(0.15), row3_y + Inches(0.12), Inches(2.55), Inches(0.35),
       title, 14, col, True, PP_ALIGN.CENTER)
    tb(s, x + Inches(0.15), row3_y + Inches(0.45), Inches(2.55), Inches(0.6),
       desc, 12, MGRAY, align=PP_ALIGN.CENTER)
    if i < 2:
        arrow_r(s, x + Inches(2.9), row3_y + Inches(0.4))

# Legend on the right
card(s, Inches(10.2), Inches(3.6), Inches(2.9), Inches(3.35))
tb(s, Inches(10.4), Inches(3.7), Inches(2.5), Inches(0.3),
   "STATUS", 13, DARK, True, PP_ALIGN.CENTER)

legend = [
    ("\u2713  Completed", GREEN),
    ("\u25CB  Weeks 6–12", MGRAY),
]
# Completed marker
rect(s, Inches(10.4), Inches(4.15), Inches(2.5), Inches(0.06), GREEN)
tb(s, Inches(10.4), Inches(4.25), Inches(2.5), Inches(0.4),
   "Rows 1 & 2: DONE", 14, GREEN, True, PP_ALIGN.CENTER)
tb(s, Inches(10.4), Inches(4.6), Inches(2.5), Inches(0.7),
   "Data pipeline fully\ncomplete. Models\ntrained & evaluated.", 12, MGRAY, align=PP_ALIGN.CENTER)

rect(s, Inches(10.4), Inches(5.4), Inches(2.5), Inches(0.06), ORANGE)
tb(s, Inches(10.4), Inches(5.5), Inches(2.5), Inches(0.4),
   "Row 3: UPCOMING", 14, ORANGE, True, PP_ALIGN.CENTER)
tb(s, Inches(10.4), Inches(5.85), Inches(2.5), Inches(0.7),
   "Explainability, dashboard\n& final report in\nWeeks 6–12.", 12, MGRAY, align=PP_ALIGN.CENTER)

# ══════════════════════════════════════════════════════════════════
#  SLIDE 4 — ORIGINAL PROJECT SCHEDULE
# ══════════════════════════════════════════════════════════════════
s = cslide("Original Project Schedule", 4)

weeks = [
    ("Week 1", "Jan 27 – Feb 2", "Dataset exploration & literature review", True),
    ("Week 2", "Feb 3 – Feb 9", "Data cleaning, missing values, encoding", True),
    ("Week 3", "Feb 10 – Feb 16", "Feature engineering & binary target", True),
    ("Week 4", "Feb 17 – Feb 23", "Model training: LR, RF, XGBoost", True),
    ("Week 5", "Feb 24 – Mar 2", "Evaluation, model selection, midterm prep", True),
    ("", "Mar 3, 2026", "MILESTONE: Mid-Term Project Review (TODAY)", None),  # milestone
    ("Week 6", "Mar 4 – Mar 10", "Hyperparameter tuning & cross-validation", False),
    ("Week 7", "Mar 11 – Mar 17", "Explainability: PFI & PDP on final model", False),
    ("Week 8", "Mar 18 – Mar 24", "Visualization of predictions & results", False),
    ("Week 9", "Mar 25 – Mar 31", "Draft report: Intro, Background, Approach, Results", False),
    ("Week 10", "Apr 1 – Apr 7", "Write Discussion, Conclusion; add figures & tables", False),
    ("Week 11-12", "Apr 8 – Apr 23", "Review, proofreading & final formatting", False),
    ("", "Apr 24, 2026", "MILESTONE: Final Project Report Due", None),  # milestone
]

# Table headers
y_start = Inches(1.2)
rect(s, Inches(0.4), y_start, Inches(12.5), Inches(0.4), NAVY)
tb(s, Inches(0.6), y_start + Inches(0.04), Inches(1.3), Inches(0.32),
   "Week", 13, WHITE, True)
tb(s, Inches(1.9), y_start + Inches(0.04), Inches(2.0), Inches(0.32),
   "Dates", 13, WHITE, True)
tb(s, Inches(4.0), y_start + Inches(0.04), Inches(6.5), Inches(0.32),
   "Task", 13, WHITE, True)
tb(s, Inches(10.8), y_start + Inches(0.04), Inches(1.8), Inches(0.32),
   "Status", 13, WHITE, True)

for i, (wk, dates, task, done) in enumerate(weeks):
    y = y_start + Inches(0.42) + i * Inches(0.42)

    if done is None:  # milestone row
        rect(s, Inches(0.4), y, Inches(12.5), Inches(0.42), RGBColor(0xFF,0xF3,0xE0))
        tb(s, Inches(1.9), y + Inches(0.05), Inches(2.0), Inches(0.32),
           dates, 12, ORANGE, True)
        tb(s, Inches(4.0), y + Inches(0.05), Inches(6.5), Inches(0.32),
           task, 12, ORANGE, True)
        tb(s, Inches(10.8), y + Inches(0.05), Inches(1.8), Inches(0.32),
           "\u2605", 14, ORANGE, True, PP_ALIGN.CENTER)
    else:
        bg_c = WHITE if i % 2 == 0 else RGBColor(0xF0,0xF4,0xF8)
        rect(s, Inches(0.4), y, Inches(12.5), Inches(0.42), bg_c)
        tb(s, Inches(0.6), y + Inches(0.05), Inches(1.3), Inches(0.32),
           wk, 12, DARK, True)
        tb(s, Inches(1.9), y + Inches(0.05), Inches(2.0), Inches(0.32),
           dates, 12, MGRAY)
        tb(s, Inches(4.0), y + Inches(0.05), Inches(6.5), Inches(0.32),
           task, 12, DARK)
        if done:
            tb(s, Inches(10.8), y + Inches(0.05), Inches(1.8), Inches(0.32),
               "\u2713 Done", 12, GREEN, True, PP_ALIGN.CENTER)
        else:
            tb(s, Inches(10.8), y + Inches(0.05), Inches(1.8), Inches(0.32),
               "Upcoming", 12, MGRAY, False, PP_ALIGN.CENTER)

# ══════════════════════════════════════════════════════════════════
#  SLIDE 5 — ACHIEVEMENT 1: DATA PREPARATION & EDA
# ══════════════════════════════════════════════════════════════════
s = cslide("Achievement 1 — Data Preparation & Exploratory Analysis", 5)

# Left: key accomplishments
rtb(s, Inches(0.6), Inches(1.2), Inches(6.5), Inches(2.8), [
    ("What Was Done", 20, DARK, True, 10),
    ("\u2022  Cleaned 101,766 records: dropped 4 high-null columns, 2 zero-variance", 14, DARK, False, 5),
    ("   columns, and 2,426 expired/hospice rows  \u2192  99,340 \u00d7 42", 14, MGRAY, False, 10),
    ("\u2022  Engineered 4 new features: total_visits, num_med_changed,", 14, DARK, False, 5),
    ("   num_med_active, age_numeric  \u2014  capturing hospital utilization patterns", 14, MGRAY, False, 10),
    ("\u2022  Converted target to binary: <30 days = 1 (11.4%), else = 0 (88.6%)", 14, DARK, False, 5),
    ("   21 redundant medication columns summarized and dropped  \u2192  99,340 \u00d7 23", 14, MGRAY, False, 10),
    ("\u2022  Statistical tests: Shapiro-Wilk (non-normal), Chi-squared (diagnosis", 14, DARK, False, 5),
    ("   matters, gender does not), Pearson/Spearman correlations", 14, MGRAY, False, 10),
])

# Right: readmission by inpatient visits chart (strongest EDA finding)
img(s, "readmission_by_age_inpatient.png", Inches(6.9), Inches(1.15), w=Inches(6.2))

# Bottom highlight box
card(s, Inches(0.5), Inches(4.5), Inches(12.3), Inches(2.5))
tb(s, Inches(0.8), Inches(4.6), Inches(6), Inches(0.35),
   "KEY DISCOVERY FROM EDA", 15, BLUE, True)

rtb(s, Inches(0.8), Inches(5.0), Inches(5.5), Inches(1.8), [
    ("Prior inpatient visits is the strongest", 16, DARK, True, 4),
    ("predictor of 30-day readmission", 16, DARK, True, 10),
    ("\u2022  0 prior visits  \u2192  9% readmission rate", 15, DARK, False, 4),
    ("\u2022  4 prior visits  \u2192  25% readmission rate", 15, DARK, False, 4),
    ("\u2022  8 prior visits  \u2192  47% readmission rate", 15, RED, True, 8),
    ("Near-linear monotonic increase — clinically actionable", 14, MGRAY, False, 0),
])

rtb(s, Inches(6.8), Inches(5.0), Inches(5.5), Inches(1.8), [
    ("Other important EDA findings:", 15, DARK, True, 8),
    ("\u2022  Diagnosis category significantly predicts readmission (p \u2248 0.00)", 14, DARK, False, 5),
    ("\u2022  Gender does NOT predict readmission (p = 0.43)", 14, DARK, False, 5),
    ("\u2022  All numeric features are non-normal \u2192 justifies tree-based models", 14, DARK, False, 5),
    ("\u2022  Weak feature-target correlations \u2192 inherently difficult problem", 14, MGRAY, False, 5),
    ("\u2022  Elderly population (55-85) dominates; most stays 1-6 days", 14, MGRAY, False, 0),
])

# ══════════════════════════════════════════════════════════════════
#  SLIDE 6 — ACHIEVEMENT 2: MODEL TRAINING & SELECTION
# ══════════════════════════════════════════════════════════════════
s = cslide("Achievement 2 — Model Training, Evaluation & Selection", 6)

# 3 model cards at top
models = [
    ("Logistic Regression", "Linear Baseline", "max_iter=1000\nsolver=lbfgs",
     "Acc: 64.0%\nROC-AUC: 0.642\nRecall: 55%", BLUE),
    ("Random Forest", "Ensemble (Bagging)", "200 trees\nmax_depth=15",
     "Acc: 88.0%\nROC-AUC: 0.653\nRecall: 6%", PURPLE),
    ("XGBoost", "Ensemble (Boosting)", "200 estimators\nmax_depth=6, lr=0.1",
     "Acc: 88.6%\nROC-AUC: 0.671\nRecall: 2%", GREEN),
]

for i, (name, mtype, params, metrics, col) in enumerate(models):
    x = Inches(0.4) + i * Inches(4.2)
    card(s, x, Inches(1.2), Inches(3.9), Inches(2.5))
    rect(s, x, Inches(1.2), Inches(3.9), Inches(0.06), col)
    tb(s, x + Inches(0.2), Inches(1.35), Inches(3.5), Inches(0.35),
       name, 18, col, True, PP_ALIGN.CENTER)
    tb(s, x + Inches(0.2), Inches(1.7), Inches(3.5), Inches(0.3),
       mtype, 12, MGRAY, align=PP_ALIGN.CENTER)
    accent_line(s, x + Inches(0.6), Inches(2.05), Inches(2.7), col, 2)
    tb(s, x + Inches(0.2), Inches(2.2), Inches(1.7), Inches(1.2),
       params, 13, MGRAY)
    tb(s, x + Inches(2.0), Inches(2.2), Inches(1.7), Inches(1.2),
       metrics, 13, DARK, True)

# Winner badge on XGBoost
rect(s, Inches(9.3), Inches(1.15), Inches(3.4), Inches(0.35), col)
tb(s, Inches(9.3), Inches(1.15), Inches(3.4), Inches(0.35),
   "\u2b50 SELECTED — Best ROC-AUC", 12, WHITE, True, PP_ALIGN.CENTER)

# Confusion matrices + model comparison
img(s, "confusion_matrices.png", Inches(0.2), Inches(3.8), w=Inches(8.5))
img(s, "model_comparison_bar.png", Inches(8.3), Inches(3.85), w=Inches(4.8))

# Selection rationale
card(s, Inches(0.4), Inches(6.2), Inches(12.5), Inches(0.8))
tb(s, Inches(0.7), Inches(6.3), Inches(12), Inches(0.55),
   "Selection Rationale:  XGBoost has the highest Test ROC-AUC (0.671), highest Average Precision (0.228), "
   "and best cross-validation stability (\u03C3 = 0.0015).  All three models were validated using 5-fold "
   "stratified CV on SMOTE-balanced training data.",
   14, DARK)

# ══════════════════════════════════════════════════════════════════
#  SLIDE 7 — ACHIEVEMENT 3 (OPTIONAL): DEEPER INSIGHTS
# ══════════════════════════════════════════════════════════════════
s = cslide("Achievement 3 — Deeper Insights from Evaluation", 7)

# ROC curves
img(s, "roc_curves.png", Inches(0.2), Inches(1.1), w=Inches(5.5))

# PR curves
img(s, "precision_recall_curves.png", Inches(5.8), Inches(1.1), w=Inches(5.5))

# CV box plot on far right
img(s, "cv_box_plot.png", Inches(8.8), Inches(1.1), w=Inches(4.3))

# Interpretation cards at bottom
card(s, Inches(0.4), Inches(4.7), Inches(4.0), Inches(2.3))
tb(s, Inches(0.6), Inches(4.8), Inches(3.6), Inches(0.3),
   "ROC Curves", 16, BLUE, True)
rtb(s, Inches(0.6), Inches(5.15), Inches(3.6), Inches(1.5), [
    ("XGBoost: 0.671", 15, BLUE, True, 5),
    ("RF: 0.653  |  LR: 0.642", 14, DARK, False, 8),
    ("All models above random", 13, MGRAY, False, 3),
    ("baseline (0.5). XGBoost", 13, MGRAY, False, 3),
    ("consistently leads.", 13, MGRAY, False, 0),
])

card(s, Inches(4.7), Inches(4.7), Inches(4.0), Inches(2.3))
tb(s, Inches(4.9), Inches(4.8), Inches(3.6), Inches(0.3),
   "Precision-Recall Curves", 16, GREEN, True)
rtb(s, Inches(4.9), Inches(5.15), Inches(3.6), Inches(1.5), [
    ("XGBoost AP: 0.228", 15, GREEN, True, 5),
    ("LR: 0.202  |  RF: 0.199", 14, DARK, False, 8),
    ("All above baseline prevalence", 13, MGRAY, False, 3),
    ("(0.114). Steep drop-off confirms", 13, MGRAY, False, 3),
    ("this is a hard task.", 13, MGRAY, False, 0),
])

card(s, Inches(9.0), Inches(4.7), Inches(3.9), Inches(2.3))
tb(s, Inches(9.2), Inches(4.8), Inches(3.5), Inches(0.3),
   "Cross-Validation Stability", 16, PURPLE, True)
rtb(s, Inches(9.2), Inches(5.15), Inches(3.5), Inches(1.5), [
    ("RF: 0.960  |  XGB: 0.958", 15, PURPLE, True, 5),
    ("LR: 0.654", 14, DARK, False, 8),
    ("RF and XGBoost both highly", 13, MGRAY, False, 3),
    ("stable (\u03C3 = 0.0015). Tree-based", 13, MGRAY, False, 3),
    ("models vastly outperform LR.", 13, MGRAY, False, 0),
])

# ══════════════════════════════════════════════════════════════════
#  SLIDE 8 — BIGGEST PROBLEM & HOW I'M DEALING WITH IT
# ══════════════════════════════════════════════════════════════════
s = cslide("Biggest Problem Encountered & How I Am Dealing With It", 8)

# Problem statement
card(s, Inches(0.5), Inches(1.2), Inches(12.3), Inches(1.35))
rect(s, Inches(0.5), Inches(1.2), Inches(0.12), Inches(1.35), RED)
tb(s, Inches(0.85), Inches(1.3), Inches(1.5), Inches(0.3),
   "THE PROBLEM", 13, RED, True)
tb(s, Inches(0.85), Inches(1.65), Inches(11.7), Inches(0.8),
   "Severe class imbalance (88.6% negative vs 11.4% positive) causes high-accuracy models that are "
   "clinically useless. At the default threshold of 0.50, XGBoost achieves 88.6% accuracy — but catches "
   "only 2% of actual readmissions (44 out of 2,263). A naive model that predicts 'not readmitted' for "
   "everyone gets the same accuracy. High accuracy is misleading.",
   16, DARK)

# Two-column solution
# Solution 1: SMOTE
card(s, Inches(0.5), Inches(2.85), Inches(5.9), Inches(2.8))
rect(s, Inches(0.5), Inches(2.85), Inches(0.12), Inches(2.8), GREEN)
tb(s, Inches(0.85), Inches(2.95), Inches(5.3), Inches(0.3),
   "SOLUTION 1:  SMOTE (Synthetic Minority Oversampling)", 14, GREEN, True)
rtb(s, Inches(0.85), Inches(3.35), Inches(5.3), Inches(2.1), [
    ("\u2022  Applied SMOTE on training data only (no data leakage)", 14, DARK, False, 5),
    ("\u2022  Balanced classes: 70,421 per class (from 9,051 vs 70,421)", 14, DARK, False, 5),
    ("\u2022  Test set remains untouched — evaluation is on real data", 14, DARK, False, 10),
    ("Result: Models learn meaningful patterns from both classes", 14, BLUE, True, 5),
    ("instead of defaulting to the majority class.", 14, BLUE, False, 0),
])

# Solution 2: Threshold Optimization
card(s, Inches(6.9), Inches(2.85), Inches(5.9), Inches(2.8))
rect(s, Inches(6.9), Inches(2.85), Inches(0.12), Inches(2.8), GREEN)
tb(s, Inches(7.25), Inches(2.95), Inches(5.3), Inches(0.3),
   "SOLUTION 2:  Classification Threshold Tuning", 14, GREEN, True)
rtb(s, Inches(7.25), Inches(3.35), Inches(5.3), Inches(2.1), [
    ("\u2022  Default threshold 0.50 is far too conservative", 14, DARK, False, 5),
    ("\u2022  Swept thresholds from 0.05 to 0.95", 14, DARK, False, 5),
    ("\u2022  Optimal threshold: 0.15 (maximizes F1 score)", 14, DARK, False, 10),
    ("Result: Recall jumps from 2% to 44%", 14, BLUE, True, 5),
    ("(catches 22\u00d7 more readmissions at cost of some false alarms)", 14, BLUE, False, 0),
])

# Before/After comparison
card(s, Inches(0.5), Inches(5.95), Inches(5.9), Inches(0.95))
tb(s, Inches(0.85), Inches(6.0), Inches(5.3), Inches(0.3),
   "BEFORE  (threshold = 0.50)", 14, RED, True)
tb(s, Inches(0.85), Inches(6.35), Inches(5.3), Inches(0.4),
   "Accuracy: 88.6%   |   Recall: 2%   |   True positives: 44 / 2,263", 15, DARK)

card(s, Inches(6.9), Inches(5.95), Inches(5.9), Inches(0.95))
tb(s, Inches(7.25), Inches(6.0), Inches(5.3), Inches(0.3),
   "AFTER  (threshold = 0.15)", 14, GREEN, True)
tb(s, Inches(7.25), Inches(6.35), Inches(5.3), Inches(0.4),
   "Accuracy: 74.0%   |   Recall: 44%   |   True positives: 1,004 / 2,263", 15, DARK, True)

# ══════════════════════════════════════════════════════════════════
#  SLIDE 9 — REVISED SCHEDULE
# ══════════════════════════════════════════════════════════════════
s = cslide("Revised Schedule", 9)

tb(s, Inches(0.6), Inches(1.2), Inches(12), Inches(0.6),
   "The project is on schedule. No revisions needed. All Week 1–5 milestones completed on time.",
   18, GREEN, True)

# Completed
tb(s, Inches(0.6), Inches(1.85), Inches(3), Inches(0.35),
   "COMPLETED  (Weeks 1–5)", 14, GREEN, True)

done_items = [
    ("Week 1", "Dataset exploration & literature review"),
    ("Week 2", "Data cleaning, missing values, encoding"),
    ("Week 3", "Feature engineering & binary target"),
    ("Week 4", "Model training: LR, RF, XGBoost"),
    ("Week 5", "Evaluation, selection & midterm prep"),
]
for i, (wk, task) in enumerate(done_items):
    y = Inches(2.25) + i * Inches(0.42)
    tb(s, Inches(0.6), y, Inches(0.35), Inches(0.35), "\u2713", 16, GREEN, True)
    tb(s, Inches(1.0), y, Inches(1.1), Inches(0.35), wk, 13, DARK, True)
    tb(s, Inches(2.2), y, Inches(4.5), Inches(0.35), task, 13, DARK)

# Milestone today
card(s, Inches(0.4), Inches(4.4), Inches(6.5), Inches(0.5))
tb(s, Inches(0.7), Inches(4.45), Inches(6), Inches(0.35),
   "\u2605  Mid-Term Project Review  —  March 3, 2026  (TODAY)", 15, ORANGE, True)

# Upcoming
tb(s, Inches(0.6), Inches(5.15), Inches(3), Inches(0.35),
   "UPCOMING  (Weeks 6–12)", 14, BLUE, True)

upcoming_items = [
    ("Week 6", "Hyperparameter tuning & cross-validation"),
    ("Week 7", "Explainability: PFI & PDP on XGBoost"),
    ("Week 8", "Visualization of predictions & results"),
    ("Wk 9–10", "Draft & write final report sections"),
    ("Wk 11–12", "Review, proofreading & submission"),
]
for i, (wk, task) in enumerate(upcoming_items):
    y = Inches(5.55) + i * Inches(0.38)
    tb(s, Inches(0.6), y, Inches(0.35), Inches(0.35), "\u25CB", 14, BLUE)
    tb(s, Inches(1.0), y, Inches(1.1), Inches(0.35), wk, 13, DARK, True)
    tb(s, Inches(2.2), y, Inches(4.5), Inches(0.35), task, 13, MGRAY)

# Final milestone
card(s, Inches(0.4), Inches(7.0), Inches(6.5), Inches(0.0))  # hidden

# Right side: progress visual + what's ahead summary
card(s, Inches(7.5), Inches(1.8), Inches(5.3), Inches(5.3))

# Progress percentage
tb(s, Inches(7.7), Inches(1.95), Inches(4.9), Inches(0.35),
   "PROGRESS OVERVIEW", 14, BLUE, True, PP_ALIGN.CENTER)

tb(s, Inches(7.7), Inches(2.45), Inches(4.9), Inches(0.9),
   "42%", 60, BLUE, True, PP_ALIGN.CENTER)
tb(s, Inches(7.7), Inches(3.35), Inches(4.9), Inches(0.35),
   "5 of 12 weeks complete", 14, MGRAY, align=PP_ALIGN.CENTER)

# Progress bar
bar_y = Inches(3.85)
rect(s, Inches(8.1), bar_y, Inches(4.1), Inches(0.3), LGRAY)
rect(s, Inches(8.1), bar_y, Inches(4.1 * 0.42), Inches(0.3), BLUE)

# What remains
rtb(s, Inches(7.8), Inches(4.4), Inches(4.8), Inches(2.5), [
    ("What Remains:", 15, DARK, True, 10),
    ("\u2022  Hyperparameter tuning of XGBoost", 13, DARK, False, 5),
    ("\u2022  Full PFI + PDP explainability analysis", 13, DARK, False, 5),
    ("\u2022  Streamlit interactive dashboard", 13, DARK, False, 5),
    ("\u2022  Prediction visualization & tables", 13, DARK, False, 5),
    ("\u2022  Complete final report (all sections)", 13, DARK, False, 10),
    ("Risk assessment: LOW", 14, GREEN, True, 5),
    ("No blockers. Clear path forward.", 13, MGRAY, False, 0),
])

# ══════════════════════════════════════════════════════════════════
#  SLIDE 10 — WHY THIS PROJECT SHOULD CONTINUE
# ══════════════════════════════════════════════════════════════════
s = cslide("Why This Project Should Continue", 10)

# 4 argument cards
arguments = [
    ("\u2776", "Strong Foundation Built",
     "The entire data pipeline is complete — from raw data (101,766 records) through cleaning, "
     "feature engineering, EDA, statistical validation, and preprocessing. Three models have been "
     "trained, evaluated with multiple metrics, and the best model (XGBoost, ROC-AUC = 0.671) has "
     "been selected. This represents a solid, reproducible foundation.",
     BLUE),
    ("\u2777", "Clear Path to Completion",
     "The remaining work is well-defined: hyperparameter tuning (Week 6), explainability analysis "
     "with PFI and PDP (Week 7), visualization (Week 8), and report writing (Weeks 9–12). The Streamlit "
     "dashboard framework is already built — it just needs the tuned model artifacts. No unknowns remain.",
     GREEN),
    ("\u2778", "Real-World Clinical Impact",
     "Hospital readmissions cost $26B+ annually. This project delivers an explainable prediction tool — "
     "not just a black-box model. Clinicians will understand why a patient is flagged as high-risk "
     "(e.g., prior inpatient visits, discharge destination), enabling informed, targeted interventions.",
     ORANGE),
    ("\u2779", "On Schedule, No Blockers",
     "All 5 weeks of the original schedule completed on time. The biggest technical challenge (class "
     "imbalance) has been identified and addressed with SMOTE + threshold optimization. There are no "
     "outstanding risks or dependencies. The project is fully on track for the April 24 deadline.",
     PURPLE),
]

for i, (num, title, desc, col) in enumerate(arguments):
    row = i // 2
    colm = i % 2
    x = Inches(0.4) + colm * Inches(6.35)
    y = Inches(1.25) + row * Inches(2.85)

    card(s, x, y, Inches(6.05), Inches(2.55))
    rect(s, x, y, Inches(0.12), Inches(2.55), col)

    tb(s, x + Inches(0.3), y + Inches(0.15), Inches(0.5), Inches(0.4),
       num, 26, col, True)
    tb(s, x + Inches(0.85), y + Inches(0.18), Inches(5.0), Inches(0.35),
       title, 19, DARK, True)
    tb(s, x + Inches(0.35), y + Inches(0.65), Inches(5.5), Inches(1.7),
       desc, 14, MGRAY)

# Bottom conclusion
card(s, Inches(0.4), Inches(6.95), Inches(12.5), Inches(0.0))

# ══════════════════════════════════════════════════════════════════
#  SLIDE 11 — THANK YOU
# ══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
bg(s, NAVY)
rect(s, Inches(0), Inches(0), Inches(0.12), Inches(7.5), BLUE)

tb(s, Inches(1), Inches(2.0), Inches(11.3), Inches(1.0),
   "Thank You", 52, WHITE, True, PP_ALIGN.CENTER)

accent_line(s, Inches(5.5), Inches(3.1), Inches(2.3), BLUE, 4)

tb(s, Inches(2), Inches(3.5), Inches(9.3), Inches(0.6),
   "Hospital Readmission Prediction for Diabetic Patients",
   20, LGRAY, align=PP_ALIGN.CENTER)

tb(s, Inches(2), Inches(4.3), Inches(9.3), Inches(0.4),
   "Raj Panchal  |  CS 719  |  March 3, 2026",
   18, MGRAY, align=PP_ALIGN.CENTER)

tb(s, Inches(2), Inches(5.3), Inches(9.3), Inches(0.5),
   "Questions?", 30, BLUE, True, PP_ALIGN.CENTER)

footer(s, 11)

# ══════════════════════════════════════════════════════════════════
#  SAVE
# ══════════════════════════════════════════════════════════════════
out = "/home/user/CS-719/CS719_Midterm_Project_Review.pptx"
prs.save(out)
print(f"Saved: {out}")
print(f"Slides: {len(prs.slides)}")
