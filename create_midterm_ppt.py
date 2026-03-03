"""
Generate Midterm Project Review PowerPoint for CS 719
Hospital Readmission Prediction — Diabetes 130-US Hospitals
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

# ── Colour palette ──────────────────────────────────────────────
DARK_BG    = RGBColor(0x1B, 0x1F, 0x3B)   # deep navy
ACCENT     = RGBColor(0x00, 0x96, 0xD6)   # bright blue
ACCENT2    = RGBColor(0x00, 0xC8, 0x53)   # green
ACCENT3    = RGBColor(0xFF, 0x57, 0x22)   # orange
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xE0, 0xE0, 0xE0)
MED_GRAY   = RGBColor(0x9E, 0x9E, 0x9E)
DARK_TEXT   = RGBColor(0x33, 0x33, 0x33)
SECTION_BG = RGBColor(0x0D, 0x12, 0x2B)   # darker navy for section dividers
LIGHT_BG   = RGBColor(0xF5, 0xF7, 0xFA)   # off-white for content slides
CARD_BG    = RGBColor(0xFF, 0xFF, 0xFF)
CARD_BORDER = RGBColor(0xDD, 0xDD, 0xDD)

IMG_DIR = "/tmp/nb_images"
SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

prs = Presentation()
prs.slide_width  = SLIDE_W
prs.slide_height = SLIDE_H

# ── Helper functions ─────────────────────────────────────────────

def add_solid_bg(slide, color):
    """Fill slide background with a solid color."""
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_shape_rect(slide, left, top, width, height, fill_color, border_color=None):
    """Add a filled rectangle."""
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1)
    else:
        shape.line.fill.background()
    return shape

def add_text_box(slide, left, top, width, height, text, font_size=18,
                 color=DARK_TEXT, bold=False, alignment=PP_ALIGN.LEFT,
                 font_name="Calibri", line_spacing=1.2):
    """Add a text box with single-run text."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    p.space_after = Pt(0)
    p.space_before = Pt(0)
    if line_spacing != 1.0:
        p.line_spacing = Pt(int(font_size * line_spacing))
    return txBox

def add_rich_text_box(slide, left, top, width, height, paragraphs_data,
                      font_name="Calibri", line_spacing_factor=1.3):
    """
    paragraphs_data: list of dicts with keys:
        text, font_size, color, bold, alignment, bullet (bool), space_after
    """
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True

    for i, pd_item in enumerate(paragraphs_data):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()

        p.text = pd_item.get("text", "")
        fs = pd_item.get("font_size", 18)
        p.font.size = Pt(fs)
        p.font.color.rgb = pd_item.get("color", DARK_TEXT)
        p.font.bold = pd_item.get("bold", False)
        p.font.name = font_name
        p.alignment = pd_item.get("alignment", PP_ALIGN.LEFT)
        p.space_after = Pt(pd_item.get("space_after", 6))
        p.space_before = Pt(pd_item.get("space_before", 0))

        if pd_item.get("bullet"):
            p.level = pd_item.get("level", 0)
    return txBox

def add_accent_line(slide, left, top, width, color=ACCENT, thickness=4):
    """Horizontal accent line."""
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Pt(thickness))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape

def add_image_safe(slide, img_name, left, top, width=None, height=None):
    """Add image if it exists."""
    path = os.path.join(IMG_DIR, img_name)
    if os.path.exists(path):
        kwargs = {"left": left, "top": top}
        if width:
            kwargs["width"] = width
        if height:
            kwargs["height"] = height
        slide.shapes.add_picture(path, **kwargs)
        return True
    return False

def add_slide_number(slide, num, total=21):
    """Add slide number at bottom-right."""
    add_text_box(slide, Inches(11.8), Inches(7.05), Inches(1.3), Inches(0.35),
                 f"{num} / {total}", font_size=10, color=MED_GRAY,
                 alignment=PP_ALIGN.RIGHT)

def add_footer_bar(slide, slide_num, total=21):
    """Thin accent bar at bottom + slide number."""
    add_shape_rect(slide, Inches(0), Inches(7.25), SLIDE_W, Inches(0.25), DARK_BG)
    add_text_box(slide, Inches(11.5), Inches(7.25), Inches(1.6), Inches(0.25),
                 f"{slide_num} / {total}", font_size=9, color=LIGHT_GRAY,
                 alignment=PP_ALIGN.RIGHT)
    add_text_box(slide, Inches(0.3), Inches(7.25), Inches(6), Inches(0.25),
                 "CS 719 — Midterm Project Review", font_size=9, color=MED_GRAY)

def content_slide(title, slide_num, bg_color=LIGHT_BG):
    """Create a standard content slide with title bar."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
    add_solid_bg(slide, bg_color)
    # Top bar
    add_shape_rect(slide, Inches(0), Inches(0), SLIDE_W, Inches(1.05), DARK_BG)
    add_text_box(slide, Inches(0.6), Inches(0.18), Inches(11), Inches(0.7),
                 title, font_size=28, color=WHITE, bold=True)
    add_accent_line(slide, Inches(0.6), Inches(0.92), Inches(2.5), ACCENT, 3)
    add_footer_bar(slide, slide_num)
    return slide

def section_slide(title, subtitle, slide_num):
    """Dark section divider slide."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_solid_bg(slide, SECTION_BG)
    # Big centered title
    add_text_box(slide, Inches(1), Inches(2.3), Inches(11.3), Inches(1.2),
                 title, font_size=44, color=WHITE, bold=True,
                 alignment=PP_ALIGN.CENTER)
    add_accent_line(slide, Inches(5.5), Inches(3.6), Inches(2.3), ACCENT, 4)
    add_text_box(slide, Inches(2), Inches(3.9), Inches(9.3), Inches(0.8),
                 subtitle, font_size=20, color=LIGHT_GRAY,
                 alignment=PP_ALIGN.CENTER)
    add_footer_bar(slide, slide_num)
    return slide

def add_card(slide, left, top, width, height, fill=CARD_BG):
    """White card with subtle shadow effect."""
    # Shadow (slightly offset darker rect)
    shadow = add_shape_rect(slide, left + Inches(0.03), top + Inches(0.03),
                            width, height, RGBColor(0xCC, 0xCC, 0xCC))
    shadow.line.fill.background()
    card = add_shape_rect(slide, left, top, width, height, fill, CARD_BORDER)
    return card

# ══════════════════════════════════════════════════════════════════
# SLIDE 1 — TITLE
# ══════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_solid_bg(slide, DARK_BG)

# Decorative accent shapes
add_shape_rect(slide, Inches(0), Inches(0), Inches(0.15), SLIDE_H, ACCENT)

add_text_box(slide, Inches(1.2), Inches(1.2), Inches(11), Inches(0.6),
             "CS 719 — MIDTERM PROJECT REVIEW", font_size=18,
             color=ACCENT, bold=True)

add_text_box(slide, Inches(1.2), Inches(2.0), Inches(11), Inches(1.5),
             "Hospital Readmission Prediction", font_size=46,
             color=WHITE, bold=True)

add_text_box(slide, Inches(1.2), Inches(3.3), Inches(11), Inches(0.8),
             "Diabetes 130-US Hospitals Dataset", font_size=28,
             color=LIGHT_GRAY)

add_accent_line(slide, Inches(1.2), Inches(4.3), Inches(3), ACCENT, 4)

add_text_box(slide, Inches(1.2), Inches(4.8), Inches(6), Inches(0.5),
             "Predicting 30-day hospital readmission using explainable machine learning",
             font_size=16, color=MED_GRAY)

add_text_box(slide, Inches(1.2), Inches(5.8), Inches(6), Inches(0.4),
             "Raj Panchal", font_size=22, color=WHITE, bold=True)
add_text_box(slide, Inches(1.2), Inches(6.25), Inches(6), Inches(0.4),
             "March 3, 2026", font_size=16, color=MED_GRAY)

add_footer_bar(slide, 1)

# ══════════════════════════════════════════════════════════════════
# SLIDE 2 — AGENDA
# ══════════════════════════════════════════════════════════════════
slide = content_slide("Agenda", 2)

agenda_items = [
    ("01", "Project Objective & Motivation"),
    ("02", "Dataset Overview"),
    ("03", "Data Cleaning & Feature Engineering"),
    ("04", "Exploratory Data Analysis"),
    ("05", "Statistical Tests"),
    ("06", "Preprocessing Pipeline"),
    ("07", "Model Training & Evaluation"),
    ("08", "Model Comparison & Selection"),
    ("09", "Key Findings"),
    ("10", "Timeline & Next Steps"),
]

for i, (num, item) in enumerate(agenda_items):
    row = i // 2
    col = i % 2
    x = Inches(0.8) + col * Inches(6)
    y = Inches(1.4) + row * Inches(1.05)

    add_text_box(slide, x, y, Inches(0.6), Inches(0.5),
                 num, font_size=24, color=ACCENT, bold=True)
    add_text_box(slide, x + Inches(0.65), y + Inches(0.05), Inches(5), Inches(0.5),
                 item, font_size=18, color=DARK_TEXT)
    add_accent_line(slide, x, y + Inches(0.52), Inches(5.3),
                    RGBColor(0xE0, 0xE0, 0xE0), 1)

# ══════════════════════════════════════════════════════════════════
# SLIDE 3 — PROJECT OBJECTIVE & MOTIVATION
# ══════════════════════════════════════════════════════════════════
slide = content_slide("Project Objective & Motivation", 3)

# Objective card
add_card(slide, Inches(0.5), Inches(1.3), Inches(12.3), Inches(1.4))
add_text_box(slide, Inches(0.8), Inches(1.4), Inches(0.8), Inches(0.4),
             "OBJECTIVE", font_size=11, color=ACCENT, bold=True)
add_text_box(slide, Inches(0.8), Inches(1.8), Inches(11.5), Inches(0.8),
             "Predict whether a diabetic patient will be readmitted to the hospital within 30 days "
             "of discharge, using explainable machine learning models that provide clinical interpretability.",
             font_size=18, color=DARK_TEXT)

# Why it matters
add_text_box(slide, Inches(0.8), Inches(3.1), Inches(5), Inches(0.4),
             "Why Does This Matter?", font_size=22, color=DARK_TEXT, bold=True)

motivations = [
    ("$26 Billion+", "Annual cost of unplanned hospital\nreadmissions in the U.S."),
    ("11.4%", "Diabetic patients readmitted\nwithin 30 days in our dataset"),
    ("Preventable", "Early identification enables\ntargeted interventions"),
]

for i, (stat, desc) in enumerate(motivations):
    x = Inches(0.8) + i * Inches(4.1)
    y = Inches(3.7)
    add_card(slide, x, y, Inches(3.7), Inches(2.2))
    add_text_box(slide, x + Inches(0.3), y + Inches(0.3), Inches(3.1), Inches(0.7),
                 stat, font_size=36, color=ACCENT, bold=True, alignment=PP_ALIGN.CENTER)
    add_text_box(slide, x + Inches(0.3), y + Inches(1.2), Inches(3.1), Inches(0.8),
                 desc, font_size=14, color=MED_GRAY, alignment=PP_ALIGN.CENTER)

# Approach line
add_text_box(slide, Inches(0.8), Inches(6.2), Inches(11.5), Inches(0.5),
             "Approach:  Train LR, RF & XGBoost  \u2192  Compare  \u2192  Select best  \u2192  Explain with PFI & PDP",
             font_size=15, color=MED_GRAY)

# ══════════════════════════════════════════════════════════════════
# SLIDE 4 — DATASET OVERVIEW
# ══════════════════════════════════════════════════════════════════
slide = content_slide("Dataset Overview", 4)

# Key stats
stats = [
    ("101,766", "Patient Encounters"),
    ("50", "Original Features"),
    ("130", "US Hospitals"),
    ("10 Years", "of Clinical Data\n(1999–2008)"),
]
for i, (val, label) in enumerate(stats):
    x = Inches(0.6) + i * Inches(3.15)
    add_card(slide, x, Inches(1.3), Inches(2.85), Inches(1.5))
    add_text_box(slide, x + Inches(0.2), Inches(1.45), Inches(2.45), Inches(0.7),
                 val, font_size=34, color=ACCENT, bold=True, alignment=PP_ALIGN.CENTER)
    add_text_box(slide, x + Inches(0.2), Inches(2.15), Inches(2.45), Inches(0.5),
                 label, font_size=13, color=MED_GRAY, alignment=PP_ALIGN.CENTER)

# Feature categories
add_text_box(slide, Inches(0.8), Inches(3.2), Inches(5), Inches(0.4),
             "Feature Categories", font_size=20, color=DARK_TEXT, bold=True)

cats = [
    ("Demographics", "Race, Gender, Age"),
    ("Admission Info", "Admission type, Discharge disposition, Source"),
    ("Clinical", "Time in hospital, Lab procedures, Medications, Diagnoses"),
    ("Medication Details", "21 individual drug columns (e.g., insulin, metformin)"),
    ("Target Variable", "readmitted  —  NO (53.9%)  |  >30 days (34.9%)  |  <30 days (11.2%)"),
]

for i, (cat, desc) in enumerate(cats):
    y = Inches(3.7) + i * Inches(0.62)
    add_text_box(slide, Inches(0.8), y, Inches(2.5), Inches(0.5),
                 f"\u2022  {cat}", font_size=15, color=DARK_TEXT, bold=True)
    add_text_box(slide, Inches(3.3), y, Inches(9), Inches(0.5),
                 desc, font_size=15, color=MED_GRAY)

# Target distribution plot
add_image_safe(slide, "target_distribution_original.png",
               Inches(8.5), Inches(3.6), width=Inches(4.3))

# ══════════════════════════════════════════════════════════════════
# SLIDE 5 — SECTION: DATA PREPARATION
# ══════════════════════════════════════════════════════════════════
section_slide("Data Preparation", "Cleaning, Engineering & Preprocessing", 5)

# ══════════════════════════════════════════════════════════════════
# SLIDE 6 — DATA CLEANING
# ══════════════════════════════════════════════════════════════════
slide = content_slide("Data Cleaning Pipeline", 6)

steps = [
    ("1", "Dropped High-Null Columns",
     "weight (97%), medical_specialty, max_glu_serum (95%), A1Cresult (83%)  —  4 columns removed"),
    ("2", "Removed Zero-Variance Columns",
     "examide and citoglipton had only one unique value  —  2 columns removed"),
    ("3", "Filtered Expired / Hospice Patients",
     "Removed 2,426 rows where patients expired or were transferred to hospice  —  not relevant for readmission"),
    ("4", "Result After Cleaning",
     "99,340 rows  \u00d7  42 columns  (from original 101,766 \u00d7 50)"),
]

for i, (num, title, desc) in enumerate(steps):
    y = Inches(1.35) + i * Inches(1.35)
    # Number circle
    circle = slide.shapes.add_shape(MSO_SHAPE.OVAL,
                                     Inches(0.7), y + Inches(0.05),
                                     Inches(0.5), Inches(0.5))
    circle.fill.solid()
    circle.fill.fore_color.rgb = ACCENT
    circle.line.fill.background()
    # Number text
    ctf = circle.text_frame
    ctf.paragraphs[0].text = num
    ctf.paragraphs[0].font.size = Pt(18)
    ctf.paragraphs[0].font.color.rgb = WHITE
    ctf.paragraphs[0].font.bold = True
    ctf.paragraphs[0].alignment = PP_ALIGN.CENTER
    ctf.vertical_anchor = MSO_ANCHOR.MIDDLE

    add_text_box(slide, Inches(1.45), y, Inches(6), Inches(0.4),
                 title, font_size=18, color=DARK_TEXT, bold=True)
    add_text_box(slide, Inches(1.45), y + Inches(0.4), Inches(6), Inches(0.6),
                 desc, font_size=14, color=MED_GRAY)

# Missing values chart on right
add_image_safe(slide, "missing_values_bar.png",
               Inches(8.2), Inches(1.3), width=Inches(4.8))

add_text_box(slide, Inches(8.5), Inches(5.0), Inches(4.3), Inches(0.4),
             "Remaining nulls handled via encoding", font_size=12,
             color=MED_GRAY, alignment=PP_ALIGN.CENTER)

# ══════════════════════════════════════════════════════════════════
# SLIDE 7 — FEATURE ENGINEERING
# ══════════════════════════════════════════════════════════════════
slide = content_slide("Feature Engineering", 7)

# New features table
add_text_box(slide, Inches(0.8), Inches(1.3), Inches(5), Inches(0.4),
             "4 New Features Created", font_size=20, color=DARK_TEXT, bold=True)

features = [
    ("total_visits", "Sum of outpatient + emergency + inpatient visits",
     "Captures overall hospital utilization"),
    ("num_med_changed", "Count of medications with dosage changes",
     "Reflects treatment instability"),
    ("num_med_active", "Count of actively prescribed medications",
     "Measures medication burden"),
    ("age_numeric", "Midpoint of age bracket (e.g., [60-70) \u2192 65)",
     "Enables numeric analysis of age"),
]

for i, (name, desc, why) in enumerate(features):
    y = Inches(1.9) + i * Inches(1.1)
    add_card(slide, Inches(0.6), y, Inches(12), Inches(0.9))
    add_text_box(slide, Inches(0.9), y + Inches(0.1), Inches(2.5), Inches(0.35),
                 name, font_size=16, color=ACCENT, bold=True)
    add_text_box(slide, Inches(3.5), y + Inches(0.1), Inches(4.5), Inches(0.35),
                 desc, font_size=14, color=DARK_TEXT)
    add_text_box(slide, Inches(8.2), y + Inches(0.1), Inches(4.2), Inches(0.35),
                 why, font_size=13, color=MED_GRAY)

# Binary target conversion
add_text_box(slide, Inches(0.8), Inches(6.0), Inches(5), Inches(0.4),
             "Binary Target Conversion", font_size=20, color=DARK_TEXT, bold=True)

add_card(slide, Inches(0.6), Inches(6.45), Inches(12), Inches(0.55))
add_text_box(slide, Inches(0.9), Inches(6.5), Inches(11.5), Inches(0.4),
             "readmitted:   <30 days \u2192 1 (Positive, 11.4%)    |    NO / >30 days \u2192 0 (Negative, 88.6%)    "
             "\u2014    23 redundant columns dropped \u2192 Final: 99,340 \u00d7 23",
             font_size=14, color=DARK_TEXT)

# ══════════════════════════════════════════════════════════════════
# SLIDE 8 — SECTION: EDA
# ══════════════════════════════════════════════════════════════════
section_slide("Exploratory Data Analysis", "Understanding patterns in the data", 8)

# ══════════════════════════════════════════════════════════════════
# SLIDE 9 — CLASS IMBALANCE & DISTRIBUTIONS
# ══════════════════════════════════════════════════════════════════
slide = content_slide("Class Imbalance & Feature Distributions", 9)

add_image_safe(slide, "binary_target_distribution.png",
               Inches(0.4), Inches(1.2), width=Inches(5.5))

add_image_safe(slide, "numeric_feature_distributions.png",
               Inches(6.2), Inches(1.2), width=Inches(6.8))

# Key observations
add_rich_text_box(slide, Inches(0.5), Inches(5.5), Inches(5.2), Inches(1.5), [
    {"text": "Key Observations:", "font_size": 15, "bold": True, "color": DARK_TEXT},
    {"text": "\u2022  Severe class imbalance: 88.6% vs 11.4%", "font_size": 13, "color": MED_GRAY},
    {"text": "\u2022  Most features are right-skewed", "font_size": 13, "color": MED_GRAY},
    {"text": "\u2022  Requires SMOTE to balance training data", "font_size": 13, "color": MED_GRAY},
])

add_rich_text_box(slide, Inches(6.4), Inches(5.5), Inches(6.5), Inches(1.5), [
    {"text": "Distribution Highlights:", "font_size": 15, "bold": True, "color": DARK_TEXT},
    {"text": "\u2022  Most stays: 1-6 days  |  Lab procedures centered ~40-50", "font_size": 13, "color": MED_GRAY},
    {"text": "\u2022  Elderly population dominant (age 55-85)", "font_size": 13, "color": MED_GRAY},
    {"text": "\u2022  total_visits extremely right-skewed (most = 0)", "font_size": 13, "color": MED_GRAY},
])

# ══════════════════════════════════════════════════════════════════
# SLIDE 10 — CORRELATION & CATEGORICALS
# ══════════════════════════════════════════════════════════════════
slide = content_slide("Correlation Matrix & Categorical Features", 10)

add_image_safe(slide, "correlation_matrix.png",
               Inches(0.3), Inches(1.15), width=Inches(5.8))

add_image_safe(slide, "categorical_distributions.png",
               Inches(6.3), Inches(1.15), width=Inches(6.7))

add_rich_text_box(slide, Inches(0.5), Inches(5.7), Inches(5.5), Inches(1.3), [
    {"text": "Correlation Insights:", "font_size": 15, "bold": True, "color": DARK_TEXT},
    {"text": "\u2022  Strongest: num_medications \u2194 time_in_hospital (~0.4)", "font_size": 13, "color": MED_GRAY},
    {"text": "\u2022  Target 'readmitted' has weak correlations with", "font_size": 13, "color": MED_GRAY},
    {"text": "    all features \u2014 confirms this is a hard problem", "font_size": 13, "color": MED_GRAY},
])

add_rich_text_box(slide, Inches(6.5), Inches(5.7), Inches(6.3), Inches(1.3), [
    {"text": "Categorical Insights:", "font_size": 15, "bold": True, "color": DARK_TEXT},
    {"text": "\u2022  Race: Caucasian dominant (~75%)  |  Gender: nearly balanced", "font_size": 13, "color": MED_GRAY},
    {"text": "\u2022  Primary diagnosis: Circulatory diseases #1, then Other", "font_size": 13, "color": MED_GRAY},
    {"text": "\u2022  Diabetes appears more as secondary/tertiary diagnosis", "font_size": 13, "color": MED_GRAY},
])

# ══════════════════════════════════════════════════════════════════
# SLIDE 11 — KEY EDA: READMISSION PATTERNS
# ══════════════════════════════════════════════════════════════════
slide = content_slide("Key Discovery: Readmission Patterns", 11)

add_image_safe(slide, "readmission_by_age_inpatient.png",
               Inches(0.3), Inches(1.15), width=Inches(12.7))

add_card(slide, Inches(0.5), Inches(4.6), Inches(5.8), Inches(2.3))
add_text_box(slide, Inches(0.8), Inches(4.7), Inches(5.3), Inches(0.35),
             "Readmission Rate by Age", font_size=17, color=DARK_TEXT, bold=True)
add_rich_text_box(slide, Inches(0.8), Inches(5.15), Inches(5.3), Inches(1.5), [
    {"text": "\u2022  Peaks at age 25 (~14.3%) — surprisingly high", "font_size": 14, "color": MED_GRAY},
    {"text": "\u2022  Plateaus at ~10-12% for ages 35-95", "font_size": 14, "color": MED_GRAY},
    {"text": "\u2022  Very young patients (5-15) have lowest rates", "font_size": 14, "color": MED_GRAY},
    {"text": "\u2022  Age alone is not a strong discriminator", "font_size": 14, "color": MED_GRAY},
])

add_card(slide, Inches(6.8), Inches(4.6), Inches(6), Inches(2.3))
add_text_box(slide, Inches(7.1), Inches(4.7), Inches(5.5), Inches(0.35),
             "Readmission Rate by Prior Inpatient Visits", font_size=17, color=DARK_TEXT, bold=True)
add_rich_text_box(slide, Inches(7.1), Inches(5.15), Inches(5.5), Inches(1.5), [
    {"text": "\u2022  STRONGEST signal: 0 visits = 9% \u2192 8 visits = 47%", "font_size": 14, "color": ACCENT, "bold": True},
    {"text": "\u2022  Near-linear monotonic increase", "font_size": 14, "color": MED_GRAY},
    {"text": "\u2022  Prior hospitalization is the #1 predictor", "font_size": 14, "color": MED_GRAY},
    {"text": "\u2022  Confirmed later by PFI analysis", "font_size": 14, "color": MED_GRAY},
])

# ══════════════════════════════════════════════════════════════════
# SLIDE 12 — STATISTICAL TESTS
# ══════════════════════════════════════════════════════════════════
slide = content_slide("Statistical Tests", 12)

# Normality tests
add_text_box(slide, Inches(0.8), Inches(1.3), Inches(5), Inches(0.4),
             "Normality Tests (Shapiro-Wilk)", font_size=20, color=DARK_TEXT, bold=True)

norm_tests = [
    ("time_in_hospital", "W = 0.886", "p \u2248 0.000", "Not Normal"),
    ("num_lab_procedures", "W = 0.984", "p \u2248 0.000", "Not Normal"),
    ("num_medications", "W = 0.926", "p \u2248 0.000", "Not Normal"),
]

# Table header
y_start = Inches(1.85)
headers = ["Feature", "Statistic", "p-value", "Result"]
x_positions = [Inches(0.8), Inches(3.8), Inches(5.6), Inches(7.2)]
widths = [Inches(3), Inches(1.8), Inches(1.6), Inches(2)]

add_shape_rect(slide, Inches(0.6), y_start, Inches(8.5), Inches(0.4), DARK_BG)
for j, (hdr, xp, w) in enumerate(zip(headers, x_positions, widths)):
    add_text_box(slide, xp, y_start + Inches(0.03), w, Inches(0.35),
                 hdr, font_size=13, color=WHITE, bold=True)

for i, (feat, stat, pval, result) in enumerate(norm_tests):
    y = y_start + Inches(0.45) + i * Inches(0.4)
    bg = CARD_BG if i % 2 == 0 else RGBColor(0xF0, 0xF4, 0xF8)
    add_shape_rect(slide, Inches(0.6), y, Inches(8.5), Inches(0.4), bg)
    add_text_box(slide, x_positions[0], y + Inches(0.03), widths[0], Inches(0.35),
                 feat, font_size=13, color=DARK_TEXT)
    add_text_box(slide, x_positions[1], y + Inches(0.03), widths[1], Inches(0.35),
                 stat, font_size=13, color=DARK_TEXT)
    add_text_box(slide, x_positions[2], y + Inches(0.03), widths[2], Inches(0.35),
                 pval, font_size=13, color=DARK_TEXT)
    add_text_box(slide, x_positions[3], y + Inches(0.03), widths[3], Inches(0.35),
                 result, font_size=13, color=ACCENT3, bold=True)

# Correlation test
add_text_box(slide, Inches(0.8), Inches(3.7), Inches(8), Inches(0.4),
             "Correlation Test (num_medications vs num_lab_procedures)",
             font_size=20, color=DARK_TEXT, bold=True)
add_rich_text_box(slide, Inches(0.8), Inches(4.2), Inches(8), Inches(1.0), [
    {"text": "Pearson r = 0.265,  p \u2248 0.000   |   Spearman r = 0.248,  p \u2248 0.000",
     "font_size": 15, "color": DARK_TEXT},
    {"text": "Weak but statistically significant positive correlation", "font_size": 14, "color": MED_GRAY},
])

# Chi-squared tests
add_text_box(slide, Inches(0.8), Inches(5.2), Inches(5), Inches(0.4),
             "Chi-Squared Independence Tests", font_size=20, color=DARK_TEXT, bold=True)

chi2_data = [
    ("diag_1 vs readmitted", "\u03C7\u00B2 = 81.96, p \u2248 0.000", "Dependent", ACCENT2),
    ("gender vs readmitted", "\u03C7\u00B2 = 0.63,  p = 0.428", "Independent", ACCENT3),
]

for i, (test, stat, result, color) in enumerate(chi2_data):
    y = Inches(5.7) + i * Inches(0.6)
    add_card(slide, Inches(0.6), y, Inches(8.5), Inches(0.5))
    add_text_box(slide, Inches(0.9), y + Inches(0.07), Inches(3.2), Inches(0.35),
                 test, font_size=14, color=DARK_TEXT, bold=True)
    add_text_box(slide, Inches(4.1), y + Inches(0.07), Inches(3), Inches(0.35),
                 stat, font_size=13, color=MED_GRAY)
    add_text_box(slide, Inches(7.3), y + Inches(0.07), Inches(1.6), Inches(0.35),
                 result, font_size=14, color=color, bold=True)

# Takeaway box on right
add_card(slide, Inches(9.5), Inches(1.3), Inches(3.4), Inches(5.5))
add_text_box(slide, Inches(9.7), Inches(1.5), Inches(3), Inches(0.35),
             "KEY TAKEAWAYS", font_size=14, color=ACCENT, bold=True)
add_rich_text_box(slide, Inches(9.7), Inches(2.0), Inches(3), Inches(4.5), [
    {"text": "1. All numeric features are non-normal", "font_size": 13, "color": DARK_TEXT, "bold": True, "space_after": 4},
    {"text": "\u2192 Justifies using tree-based models over parametric methods", "font_size": 12, "color": MED_GRAY, "space_after": 14},
    {"text": "2. Diagnosis category predicts readmission", "font_size": 13, "color": DARK_TEXT, "bold": True, "space_after": 4},
    {"text": "\u2192 diag_1 is statistically dependent on the target", "font_size": 12, "color": MED_GRAY, "space_after": 14},
    {"text": "3. Gender does NOT predict readmission", "font_size": 13, "color": DARK_TEXT, "bold": True, "space_after": 4},
    {"text": "\u2192 p = 0.43, no significant relationship", "font_size": 12, "color": MED_GRAY, "space_after": 14},
    {"text": "4. Weak feature-target correlations overall", "font_size": 13, "color": DARK_TEXT, "bold": True, "space_after": 4},
    {"text": "\u2192 This is an inherently difficult prediction task", "font_size": 12, "color": MED_GRAY},
])

# ══════════════════════════════════════════════════════════════════
# SLIDE 13 — PREPROCESSING PIPELINE
# ══════════════════════════════════════════════════════════════════
slide = content_slide("Preprocessing Pipeline", 13)

pipeline_steps = [
    ("One-Hot Encoding", "Categorical \u2192 binary dummies\n46 final features"),
    ("Stratified Split", "80% Train / 20% Test\nPreserves 11.4% positive rate"),
    ("SMOTE", "Training set only\n70,421 per class"),
    ("StandardScaler", "Zero mean, unit variance\nFitted on train only"),
]

for i, (title, desc) in enumerate(pipeline_steps):
    x = Inches(0.5) + i * Inches(3.2)
    y = Inches(1.5)

    # Step box
    add_card(slide, x, y, Inches(2.8), Inches(2.5))

    # Step number
    circle = slide.shapes.add_shape(MSO_SHAPE.OVAL,
                                     x + Inches(1.05), y - Inches(0.2),
                                     Inches(0.5), Inches(0.5))
    circle.fill.solid()
    circle.fill.fore_color.rgb = ACCENT
    circle.line.fill.background()
    ctf = circle.text_frame
    ctf.paragraphs[0].text = str(i + 1)
    ctf.paragraphs[0].font.size = Pt(18)
    ctf.paragraphs[0].font.color.rgb = WHITE
    ctf.paragraphs[0].font.bold = True
    ctf.paragraphs[0].alignment = PP_ALIGN.CENTER
    ctf.vertical_anchor = MSO_ANCHOR.MIDDLE

    add_text_box(slide, x + Inches(0.2), y + Inches(0.5), Inches(2.4), Inches(0.45),
                 title, font_size=17, color=DARK_TEXT, bold=True, alignment=PP_ALIGN.CENTER)
    add_text_box(slide, x + Inches(0.2), y + Inches(1.1), Inches(2.4), Inches(1.0),
                 desc, font_size=14, color=MED_GRAY, alignment=PP_ALIGN.CENTER)

    # Arrow between steps
    if i < 3:
        arrow_x = x + Inches(2.85)
        arrow = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW,
                                        arrow_x, y + Inches(1.0),
                                        Inches(0.3), Inches(0.35))
        arrow.fill.solid()
        arrow.fill.fore_color.rgb = ACCENT
        arrow.line.fill.background()

# Data split summary
add_card(slide, Inches(0.5), Inches(4.5), Inches(12.3), Inches(2.3))
add_text_box(slide, Inches(0.8), Inches(4.6), Inches(5), Inches(0.35),
             "Data Split Summary", font_size=18, color=DARK_TEXT, bold=True)

# Before SMOTE
add_text_box(slide, Inches(0.8), Inches(5.1), Inches(5.5), Inches(0.35),
             "Before SMOTE:", font_size=15, color=DARK_TEXT, bold=True)
add_text_box(slide, Inches(0.8), Inches(5.45), Inches(5.5), Inches(0.7),
             "Train: 79,472 (70,421 neg / 9,051 pos)  |  Test: 19,868 (17,605 neg / 2,263 pos)",
             font_size=14, color=MED_GRAY)

# After SMOTE
add_text_box(slide, Inches(0.8), Inches(5.95), Inches(5.5), Inches(0.35),
             "After SMOTE (training set only):", font_size=15, color=DARK_TEXT, bold=True)
add_text_box(slide, Inches(0.8), Inches(6.3), Inches(11), Inches(0.4),
             "Train: 140,842 (70,421 per class — perfectly balanced)  |  Test: 19,868 (unchanged — no data leakage)",
             font_size=14, color=MED_GRAY)

# ══════════════════════════════════════════════════════════════════
# SLIDE 14 — SECTION: MODELING
# ══════════════════════════════════════════════════════════════════
section_slide("Model Training & Evaluation", "Logistic Regression  |  Random Forest  |  XGBoost", 14)

# ══════════════════════════════════════════════════════════════════
# SLIDE 15 — MODEL CONFIGURATIONS
# ══════════════════════════════════════════════════════════════════
slide = content_slide("Model Training — Three Classifiers", 15)

models = [
    ("Logistic Regression", "Linear Baseline",
     ["max_iter = 1,000", "solver = lbfgs", "random_state = 42"],
     "Simple, interpretable, fast. Serves as the baseline to beat."),
    ("Random Forest", "Ensemble — Bagging",
     ["n_estimators = 200", "max_depth = 15", "min_samples_split = 10"],
     "Reduces variance through bootstrapped decision trees."),
    ("XGBoost", "Ensemble — Boosting",
     ["n_estimators = 200", "max_depth = 6", "learning_rate = 0.1"],
     "Sequential correction of errors; typically best for tabular data."),
]

for i, (name, mtype, params, desc) in enumerate(models):
    x = Inches(0.5) + i * Inches(4.2)
    add_card(slide, x, Inches(1.4), Inches(3.9), Inches(5.0))

    # Model name
    add_text_box(slide, x + Inches(0.3), Inches(1.6), Inches(3.3), Inches(0.5),
                 name, font_size=22, color=ACCENT, bold=True, alignment=PP_ALIGN.CENTER)
    add_text_box(slide, x + Inches(0.3), Inches(2.1), Inches(3.3), Inches(0.35),
                 mtype, font_size=14, color=MED_GRAY, alignment=PP_ALIGN.CENTER)

    add_accent_line(slide, x + Inches(0.8), Inches(2.55), Inches(2.3), ACCENT, 2)

    # Parameters
    add_text_box(slide, x + Inches(0.3), Inches(2.8), Inches(3.3), Inches(0.3),
                 "Hyperparameters:", font_size=13, color=DARK_TEXT, bold=True)
    for j, param in enumerate(params):
        add_text_box(slide, x + Inches(0.5), Inches(3.15) + j * Inches(0.35),
                     Inches(3), Inches(0.3),
                     f"\u2022  {param}", font_size=13, color=MED_GRAY)

    # Description
    add_text_box(slide, x + Inches(0.3), Inches(4.4), Inches(3.3), Inches(0.3),
                 "Role:", font_size=13, color=DARK_TEXT, bold=True)
    add_text_box(slide, x + Inches(0.3), Inches(4.75), Inches(3.3), Inches(1.2),
                 desc, font_size=13, color=MED_GRAY)

add_text_box(slide, Inches(0.8), Inches(6.65), Inches(11), Inches(0.4),
             "All models trained on the same SMOTE-balanced training data (140,842 samples) and evaluated on the original test set (19,868 samples).",
             font_size=13, color=MED_GRAY)

# ══════════════════════════════════════════════════════════════════
# SLIDE 16 — CONFUSION MATRICES
# ══════════════════════════════════════════════════════════════════
slide = content_slide("Model Evaluation — Confusion Matrices", 16)

add_image_safe(slide, "confusion_matrices.png",
               Inches(0.3), Inches(1.15), width=Inches(12.7))

add_card(slide, Inches(0.4), Inches(4.2), Inches(4.0), Inches(2.8))
add_text_box(slide, Inches(0.6), Inches(4.3), Inches(3.6), Inches(0.35),
             "Logistic Regression", font_size=16, color=ACCENT, bold=True)
add_rich_text_box(slide, Inches(0.6), Inches(4.7), Inches(3.6), Inches(2.0), [
    {"text": "\u2022  Most balanced predictions", "font_size": 13, "color": DARK_TEXT},
    {"text": "\u2022  1,238 true positives (best recall)", "font_size": 13, "color": DARK_TEXT},
    {"text": "\u2022  6,122 false positives (many false alarms)", "font_size": 13, "color": MED_GRAY},
    {"text": "\u2022  Recall: 55% — catches most readmissions", "font_size": 13, "color": ACCENT2, "bold": True},
])

add_card(slide, Inches(4.7), Inches(4.2), Inches(4.0), Inches(2.8))
add_text_box(slide, Inches(4.9), Inches(4.3), Inches(3.6), Inches(0.35),
             "Random Forest", font_size=16, color=ACCENT, bold=True)
add_rich_text_box(slide, Inches(4.9), Inches(4.7), Inches(3.6), Inches(2.0), [
    {"text": "\u2022  Very conservative predictions", "font_size": 13, "color": DARK_TEXT},
    {"text": "\u2022  Only 127 true positives out of 2,263", "font_size": 13, "color": DARK_TEXT},
    {"text": "\u2022  High accuracy (88%) but misleading", "font_size": 13, "color": MED_GRAY},
    {"text": "\u2022  Recall: 6% — misses most readmissions", "font_size": 13, "color": ACCENT3, "bold": True},
])

add_card(slide, Inches(9.0), Inches(4.2), Inches(4.0), Inches(2.8))
add_text_box(slide, Inches(9.2), Inches(4.3), Inches(3.6), Inches(0.35),
             "XGBoost", font_size=16, color=ACCENT, bold=True)
add_rich_text_box(slide, Inches(9.2), Inches(4.7), Inches(3.6), Inches(2.0), [
    {"text": "\u2022  Most conservative at default threshold", "font_size": 13, "color": DARK_TEXT},
    {"text": "\u2022  Only 44 true positives out of 2,263", "font_size": 13, "color": DARK_TEXT},
    {"text": "\u2022  Highest accuracy (88.6%)", "font_size": 13, "color": MED_GRAY},
    {"text": "\u2022  Recall: 2% — needs threshold tuning", "font_size": 13, "color": ACCENT3, "bold": True},
])

# ══════════════════════════════════════════════════════════════════
# SLIDE 17 — ROC & PR CURVES
# ══════════════════════════════════════════════════════════════════
slide = content_slide("Model Evaluation — ROC & Precision-Recall Curves", 17)

add_image_safe(slide, "roc_curves.png",
               Inches(0.2), Inches(1.1), width=Inches(6.2))

add_image_safe(slide, "precision_recall_curves.png",
               Inches(6.5), Inches(1.1), width=Inches(6.5))

add_card(slide, Inches(0.4), Inches(5.6), Inches(6.0), Inches(1.4))
add_text_box(slide, Inches(0.6), Inches(5.65), Inches(5.6), Inches(0.3),
             "ROC Curves — Area Under Curve", font_size=15, color=DARK_TEXT, bold=True)
add_rich_text_box(slide, Inches(0.6), Inches(5.95), Inches(5.6), Inches(0.9), [
    {"text": "XGBoost: 0.671  >  RF: 0.653  >  LR: 0.642", "font_size": 14, "color": ACCENT, "bold": True},
    {"text": "All above random baseline (0.5), XGBoost leads", "font_size": 13, "color": MED_GRAY},
])

add_card(slide, Inches(6.7), Inches(5.6), Inches(6.2), Inches(1.4))
add_text_box(slide, Inches(6.9), Inches(5.65), Inches(5.8), Inches(0.3),
             "Precision-Recall — Average Precision", font_size=15, color=DARK_TEXT, bold=True)
add_rich_text_box(slide, Inches(6.9), Inches(5.95), Inches(5.8), Inches(0.9), [
    {"text": "XGBoost: 0.228  >  LR: 0.202  >  RF: 0.199", "font_size": 14, "color": ACCENT, "bold": True},
    {"text": "All above baseline prevalence (0.114), steep drop-off reflects difficulty", "font_size": 13, "color": MED_GRAY},
])

# ══════════════════════════════════════════════════════════════════
# SLIDE 18 — MODEL COMPARISON & SELECTION
# ══════════════════════════════════════════════════════════════════
slide = content_slide("Model Comparison & Best Model Selection", 18)

add_image_safe(slide, "model_comparison_bar.png",
               Inches(0.2), Inches(1.1), width=Inches(6.5))

add_image_safe(slide, "cv_box_plot.png",
               Inches(6.5), Inches(1.1), width=Inches(6.5))

# Selection summary table
add_text_box(slide, Inches(0.8), Inches(4.7), Inches(12), Inches(0.4),
             "Model Selection Summary", font_size=20, color=DARK_TEXT, bold=True)

# Table
table_data = [
    ["Model", "Test ROC-AUC", "Test F1", "CV ROC-AUC", "CV Std", "Stability"],
    ["Logistic Regression", "0.6417", "0.7051", "0.6543", "0.0019", "0.9981"],
    ["Random Forest", "0.6525", "0.8403", "0.9600", "0.0015", "0.9985"],
    ["XGBoost", "0.6711", "0.8368", "0.9576", "0.0015", "0.9985"],
]

col_widths = [Inches(2.5), Inches(1.8), Inches(1.5), Inches(1.8), Inches(1.3), Inches(1.5)]
x_start = Inches(0.7)
y_table = Inches(5.15)

for row_i, row in enumerate(table_data):
    x = x_start
    y = y_table + row_i * Inches(0.38)

    if row_i == 0:
        bg_c = DARK_BG
        txt_c = WHITE
        is_bold = True
    elif row_i == 3:
        bg_c = RGBColor(0xE3, 0xF2, 0xFD)
        txt_c = DARK_TEXT
        is_bold = True
    else:
        bg_c = CARD_BG if row_i % 2 == 1 else RGBColor(0xF5, 0xF5, 0xF5)
        txt_c = DARK_TEXT
        is_bold = False

    add_shape_rect(slide, x_start, y, Inches(10.4), Inches(0.38), bg_c)

    for col_i, (cell, w) in enumerate(zip(row, col_widths)):
        add_text_box(slide, x, y + Inches(0.03), w, Inches(0.32),
                     cell, font_size=13, color=txt_c if row_i == 0 else (ACCENT if (row_i == 3 and col_i == 1) else txt_c),
                     bold=is_bold if col_i == 0 or row_i == 0 else (True if row_i == 3 and col_i == 1 else False),
                     alignment=PP_ALIGN.CENTER if col_i > 0 else PP_ALIGN.LEFT)
        x += w

# Winner badge
add_text_box(slide, Inches(11.3), Inches(5.52), Inches(1.8), Inches(0.5),
             "\u2b50 SELECTED", font_size=15, color=ACCENT, bold=True)

add_text_box(slide, Inches(0.8), Inches(6.75), Inches(12), Inches(0.35),
             "XGBoost selected as best model: Highest Test ROC-AUC (0.6711) with best cross-validation stability (\u03C3 = 0.0015)",
             font_size=15, color=DARK_TEXT, bold=True)

# ══════════════════════════════════════════════════════════════════
# SLIDE 19 — KEY FINDINGS
# ══════════════════════════════════════════════════════════════════
slide = content_slide("Key Findings So Far", 19)

findings = [
    ("\u2776", "Class Imbalance is Critical",
     "Only 11.4% positive rate. SMOTE was essential — without it, models predict 'not readmitted' for nearly everyone.",
     ACCENT),
    ("\u2777", "Prior Inpatient Visits = #1 Predictor",
     "Readmission rate jumps from 9% (0 visits) to 47% (8+ visits). Strongest monotonic signal in the dataset.",
     ACCENT2),
    ("\u2778", "High Accuracy is Misleading",
     "XGBoost achieves 88.6% accuracy but only 2% recall at default threshold. A naive 'predict all 0' gets 88.6% too.",
     ACCENT3),
    ("\u2779", "XGBoost is the Best Model",
     "Highest ROC-AUC (0.671), highest Average Precision (0.228), and stable cross-validation (std = 0.0015).",
     ACCENT),
    ("\u277A", "This is an Inherently Hard Problem",
     "Weak feature-target correlations, non-normal distributions. ROC-AUC of 0.67 is typical for this dataset in literature.",
     RGBColor(0x9C, 0x27, 0xB0)),
]

for i, (num, title, desc, color) in enumerate(findings):
    y = Inches(1.3) + i * Inches(1.15)
    add_card(slide, Inches(0.5), y, Inches(12.3), Inches(1.0))

    # Number
    add_text_box(slide, Inches(0.7), y + Inches(0.1), Inches(0.5), Inches(0.4),
                 num, font_size=24, color=color, bold=True)
    add_text_box(slide, Inches(1.3), y + Inches(0.08), Inches(3.5), Inches(0.35),
                 title, font_size=17, color=DARK_TEXT, bold=True)
    add_text_box(slide, Inches(1.3), y + Inches(0.47), Inches(11.2), Inches(0.45),
                 desc, font_size=14, color=MED_GRAY)

# ══════════════════════════════════════════════════════════════════
# SLIDE 20 — PROJECT TIMELINE
# ══════════════════════════════════════════════════════════════════
slide = content_slide("Project Timeline & Progress", 20)

# Completed weeks
add_text_box(slide, Inches(0.8), Inches(1.3), Inches(5), Inches(0.4),
             "COMPLETED (Weeks 1–5)", font_size=18, color=ACCENT2, bold=True)

completed = [
    ("Week 1", "Jan 27 – Feb 2", "Dataset exploration & literature review"),
    ("Week 2", "Feb 3 – Feb 9", "Data cleaning, missing values, encoding"),
    ("Week 3", "Feb 10 – Feb 16", "Feature engineering & binary target creation"),
    ("Week 4", "Feb 17 – Feb 23", "Model training: LR, RF, XGBoost"),
    ("Week 5", "Feb 24 – Mar 2", "Evaluation, model selection, midterm prep"),
]

for i, (week, dates, desc) in enumerate(completed):
    y = Inches(1.8) + i * Inches(0.58)
    # Green check
    add_text_box(slide, Inches(0.7), y, Inches(0.4), Inches(0.35),
                 "\u2713", font_size=18, color=ACCENT2, bold=True)
    add_text_box(slide, Inches(1.1), y, Inches(1.1), Inches(0.35),
                 week, font_size=14, color=DARK_TEXT, bold=True)
    add_text_box(slide, Inches(2.2), y, Inches(1.8), Inches(0.35),
                 dates, font_size=12, color=MED_GRAY)
    add_text_box(slide, Inches(4.1), y, Inches(5.5), Inches(0.35),
                 desc, font_size=14, color=DARK_TEXT)

# Milestone
add_card(slide, Inches(0.5), Inches(4.8), Inches(9.0), Inches(0.5))
add_text_box(slide, Inches(0.8), Inches(4.85), Inches(8.5), Inches(0.35),
             "\u2605  MILESTONE:  Mid-Term Project Review — March 3, 2026  (TODAY)",
             font_size=15, color=ACCENT, bold=True)

# Upcoming weeks
add_text_box(slide, Inches(0.8), Inches(5.6), Inches(5), Inches(0.4),
             "UPCOMING (Weeks 6–12)", font_size=18, color=ACCENT3, bold=True)

upcoming = [
    ("Week 6–7", "Hyperparameter tuning, Explainability (PFI + PDP)"),
    ("Week 8", "Visualization of predictions & explainability results"),
    ("Week 9–10", "Final report drafting (Intro, Background, Results, Discussion)"),
    ("Week 11–12", "Review, proofreading & final submission (Apr 24)"),
]

for i, (week, desc) in enumerate(upcoming):
    y = Inches(6.0) + i * Inches(0.4)
    add_text_box(slide, Inches(1.1), y, Inches(1.4), Inches(0.35),
                 week, font_size=13, color=DARK_TEXT, bold=True)
    add_text_box(slide, Inches(2.5), y, Inches(7), Inches(0.35),
                 desc, font_size=13, color=MED_GRAY)

# Progress bar on right
add_card(slide, Inches(10.0), Inches(1.3), Inches(2.8), Inches(5.6))
add_text_box(slide, Inches(10.2), Inches(1.5), Inches(2.4), Inches(0.35),
             "PROGRESS", font_size=14, color=ACCENT, bold=True, alignment=PP_ALIGN.CENTER)

# Progress indicator
pct = 42  # 5/12 weeks
add_text_box(slide, Inches(10.2), Inches(2.0), Inches(2.4), Inches(1.0),
             f"{pct}%", font_size=56, color=ACCENT, bold=True, alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(10.2), Inches(3.0), Inches(2.4), Inches(0.35),
             "5 of 12 weeks complete", font_size=13, color=MED_GRAY, alignment=PP_ALIGN.CENTER)

# Mini progress bar
bar_y = Inches(3.6)
bar_x = Inches(10.4)
bar_w = Inches(2.0)
bar_h = Inches(0.25)
add_shape_rect(slide, bar_x, bar_y, bar_w, bar_h, RGBColor(0xE0, 0xE0, 0xE0))
add_shape_rect(slide, bar_x, bar_y, Inches(2.0 * pct / 100), bar_h, ACCENT)

# Remaining milestones
add_text_box(slide, Inches(10.2), Inches(4.2), Inches(2.4), Inches(0.3),
             "Remaining Milestones:", font_size=12, color=DARK_TEXT, bold=True, alignment=PP_ALIGN.CENTER)
mini_milestones = [
    "Explainability analysis",
    "Streamlit dashboard",
    "Final report writing",
    "Final submission: Apr 24",
]
for i, m in enumerate(mini_milestones):
    add_text_box(slide, Inches(10.3), Inches(4.6) + i * Inches(0.35),
                 Inches(2.3), Inches(0.3),
                 f"\u25CB  {m}", font_size=11, color=MED_GRAY)

# ══════════════════════════════════════════════════════════════════
# SLIDE 21 — THANK YOU
# ══════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_solid_bg(slide, DARK_BG)
add_shape_rect(slide, Inches(0), Inches(0), Inches(0.15), SLIDE_H, ACCENT)

add_text_box(slide, Inches(1), Inches(2.2), Inches(11.3), Inches(1.2),
             "Thank You", font_size=52, color=WHITE, bold=True,
             alignment=PP_ALIGN.CENTER)

add_accent_line(slide, Inches(5.5), Inches(3.5), Inches(2.3), ACCENT, 4)

add_text_box(slide, Inches(2), Inches(3.9), Inches(9.3), Inches(0.6),
             "Hospital Readmission Prediction — Diabetes 130-US Hospitals",
             font_size=20, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)

add_text_box(slide, Inches(2), Inches(4.7), Inches(9.3), Inches(0.5),
             "Raj Panchal  |  CS 719  |  March 3, 2026",
             font_size=18, color=MED_GRAY, alignment=PP_ALIGN.CENTER)

add_text_box(slide, Inches(2), Inches(5.6), Inches(9.3), Inches(0.5),
             "Questions?",
             font_size=28, color=ACCENT, bold=True, alignment=PP_ALIGN.CENTER)

add_footer_bar(slide, 21)

# ══════════════════════════════════════════════════════════════════
# SAVE
# ══════════════════════════════════════════════════════════════════
output_path = "/home/user/CS-719/CS719_Midterm_Project_Review.pptx"
prs.save(output_path)
print(f"Presentation saved to: {output_path}")
print(f"Total slides: {len(prs.slides)}")
