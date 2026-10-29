#!/usr/bin/env python3
"""
scripts/build_presentation_deck.py

Builds `Near_Null_Magnetic_Fields_Lunar_Plant_Biology_Presentation.pptx`, a
publication-grade 16:9 widescreen PowerPoint presentation for the research group.

Key Highlights:
- Deconstructs Figure Montages 1-5 into separable, individually repositionable
  subpanel graphic objects overlaid with native, fully editable PowerPoint
  text boxes and callout shapes.
- Includes deep-dive slides for key mechanisms and the Artemis LEAF payload.
- Builds Table 3 (Flight Decision Matrix) as a native, styled PowerPoint table.
- Populates comprehensive presenter notes on every slide for Dr. Barker.

Usage:
    .venv/bin/python scripts/build_presentation_deck.py
"""

import os
import sys
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

REPO_ROOT = Path(__file__).resolve().parent.parent
SUBPANELS_DIR = REPO_ROOT / 'presentation' / 'assets' / 'subpanels'
OUT_PPTX = REPO_ROOT / 'Near_Null_Magnetic_Fields_Lunar_Plant_Biology_Presentation.pptx'

# ---------------------------------------------------------------------------
# Color Palette
# ---------------------------------------------------------------------------
NAVY_DARK     = RGBColor(11, 30, 54)     # #0B1E36 (Title / Dark Slide Background)
NAVY_CARD     = RGBColor(19, 43, 76)     # #132B4C (Dark card background)
WHITE_CANVAS  = RGBColor(248, 250, 252)  # #F8FAFC (Light Slide Background)
CARD_BG_LIGHT = RGBColor(255, 255, 255)  # #FFFFFF (White card background)
CARD_BORDER   = RGBColor(226, 232, 240)  # #E2E8F0 (Subtle card border)

TEXT_DARK     = RGBColor(15, 23, 42)     # #0F172A (Primary text on light)
TEXT_MUTED    = RGBColor(71, 85, 105)    # #475569 (Secondary text on light)
TEXT_LIGHT    = RGBColor(248, 250, 252)  # Primary text on dark
TEXT_LIGHT_MUT= RGBColor(148, 163, 184)  # Secondary text on dark

BLUE_PRIMARY  = RGBColor(2, 132, 199)    # #0284C7 (Aerospace Blue accent)
BLUE_BG_LIGHT = RGBColor(224, 242, 254)  # #E0F2FE (Light blue card bg)
RED_ALERT     = RGBColor(220, 38, 38)    # #DC2626 (Warning / NNMF red)
RED_BG_LIGHT  = RGBColor(254, 242, 242)  # #FEF2F2 (Light red card bg)
AMBER_WARN    = RGBColor(217, 119, 6)    # #D97706 (Amber notice)
AMBER_BG_LIGHT= RGBColor(254, 243, 199)  # #FEF3C7 (Light amber card bg)
GREEN_SUCC    = RGBColor(22, 163, 74)    # #16A34A (Success / Rescue green)
GREEN_BG_LIGHT= RGBColor(220, 252, 231)  # #DCFCE7 (Light green card bg)
PURPLE_ACCENT = RGBColor(147, 51, 234)   # #9333EA (Quantum purple)

# ---------------------------------------------------------------------------
# Slide Helper Functions
# ---------------------------------------------------------------------------
def set_slide_background(slide, color):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_header(slide, category_text, title_text, subtitle_text, dark=False):
    # Category tracker pill
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.35))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(9.5)
    p_cat.font.bold = True
    p_cat.font.color.rgb = BLUE_PRIMARY if not dark else RGBColor(56, 189, 248)

    # Slide Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.733), Inches(0.55))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.size = Pt(20.0)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_LIGHT if dark else TEXT_DARK

    # Subtitle / Takeaway banner
    sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.22), Inches(11.733), Inches(0.4))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.font.size = Pt(11.0)
    p_sub.font.italic = True
    p_sub.font.color.rgb = TEXT_LIGHT_MUT if dark else TEXT_MUTED

def add_footer(slide, slide_num, total_slides=15, dark=False):
    foot_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.3))
    tf = foot_box.text_frame
    p = tf.paragraphs[0]
    p.text = f"Life Sciences in Space Research (2026) | Artemis III LEAF Perspective              Slide {slide_num} of {total_slides}"
    p.font.size = Pt(8.5)
    p.font.color.rgb = RGBColor(100, 116, 139) if not dark else RGBColor(148, 163, 184)

def add_card(slide, left, top, width, height, bg_color, border_color=None, border_width=1):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(border_width)
    else:
        shape.line.fill.background()
    return shape

def add_notes(slide, notes_text):
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = notes_text

# ---------------------------------------------------------------------------
# Slide Builders
# ---------------------------------------------------------------------------

def build_slide_01_title(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, NAVY_DARK)

    # Accent decorative box
    add_card(slide, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.8), NAVY_CARD, BLUE_PRIMARY, border_width=1.5)

    # Pill badge
    pill = slide.shapes.add_textbox(Inches(1.2), Inches(1.1), Inches(8.0), Inches(0.4))
    p = pill.text_frame.paragraphs[0]
    p.text = "COSPAR / ELSEVIER REVIEW ARTICLE — ARTEMIS III LEAF PERSPECTIVE"
    p.font.size = Pt(10.0)
    p.font.bold = True
    p.font.color.rgb = RGBColor(56, 189, 248)

    # Title
    t_box = slide.shapes.add_textbox(Inches(1.2), Inches(1.5), Inches(10.8), Inches(1.4))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = "Near-Null Magnetic Fields in Lunar Plant Biology"
    p_t.font.size = Pt(28.0)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_LIGHT

    # Subtitle
    sub_box = slide.shapes.add_textbox(Inches(1.2), Inches(2.9), Inches(10.8), Inches(0.8))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = "The First Five Days of Seedling Growth, Multi-Stressor Bioenergetics, and Implications for Artemis Agriculture"
    p_sub.font.size = Pt(14.0)
    p_sub.font.italic = True
    p_sub.font.color.rgb = RGBColor(203, 213, 225)

    # Authors block
    auth_box = slide.shapes.add_textbox(Inches(1.2), Inches(3.8), Inches(10.8), Inches(1.0))
    tf_a = auth_box.text_frame
    tf_a.word_wrap = True
    p_a1 = tf_a.paragraphs[0]
    p_a1.text = "D. Marshall Porterfield*, Richard J. Barker*, Caue Borlina, Aubrey O’Rourke, Adriana Sanchez, Manisha Dagar, Sofia Leiva Aldana,\nRay Wheeler, Gioia Massa, Barbara Demmig-Adams, Marta Peirats-Llobet, Pamela Flores, Anirudha Dixit, Christine Chamberlain"
    p_a1.font.size = Pt(10.5)
    p_a1.font.bold = True
    p_a1.font.color.rgb = TEXT_LIGHT

    p_a2 = tf_a.add_paragraph()
    p_a2.text = "La Trobe University • Space Lab Technologies • NASA Kennedy Space Center • University of Colorado Boulder • Purdue University\n*Corresponding Authors: dr.richard.barker@gmail.com, porterf@purdue.edu"
    p_a2.font.size = Pt(9.5)
    p_a2.font.color.rgb = TEXT_LIGHT_MUT

    # Metadata badges
    badge_box = slide.shapes.add_textbox(Inches(1.2), Inches(5.6), Inches(10.8), Inches(0.6))
    tf_b = badge_box.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.text = "Target Journal: Life Sciences in Space Research (LSSR)  |  Mission Context: Artemis III LEAF Payload  |  FAIR Repository & CoSE Portal Ready"
    p_b.font.size = Pt(9.0)
    p_b.font.bold = True
    p_b.font.color.rgb = RGBColor(148, 163, 184)

    add_footer(slide, 1, 15, dark=True)

    add_notes(slide,
        "TALKING POINTS (SLIDE 1 - TITLE):\n"
        "• Welcome everyone. Today we are presenting our comprehensive review manuscript prepared for Life Sciences in Space Research.\n"
        "• The title is 'Near-Null Magnetic Fields in Lunar Plant Biology: The First Five Days of Seedling Growth, Multi-Stressor Bioenergetics, and Implications for Artemis Agriculture'.\n"
        "• Co-authored with Marshall Porterfield, Caue Borlina, Aubrey O'Rourke, Adriana Sanchez, Manisha Dagar, Sofia Leiva Aldana, Ray Wheeler, Gioia Massa, Barbara Demmig-Adams, Marta Peirats-Llobet, Pamela Flores, Anirudha Dixit, and Christine Chamberlain.\n"
        "• Central theme: While gravitational unloading and ionizing radiation dominate the space biology literature, the local magnetic field environment at the biological volume is virtually never controlled or characterized. On the lunar surface, this field drops to an extreme near-null magnetic field (<0.8 nT at Artemis candidate landing sites), posing significant developmental risks during the critical first 5 days of crop establishment."
    )

def build_slide_02_narrative_overview(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, WHITE_CANVAS)
    add_header(slide, "Executive Narrative", "The Missing Variable in Space Agriculture",
               "Geomagnetic field removal is a neglected primary stressor with major consequences for lunar crop production")

    # 3 Core Pillars
    pillars = [
        ("1. The Physical Reality: Lunar Void (<0.8 nT)",
         "• Earth dipolar field: 25,000–65,000 nT.\n• Lunar South Pole candidate sites: <0.8 nT (>30,000× lower).\n• Spacecraft DC bus interference (50–500 µT) can mask this hypomagnetic vacuum unless sample-level 3-axis fluxgate sensing is deployed.",
         BLUE_BG_LIGHT, BLUE_PRIMARY),
        ("2. The First 5 Days: The Developmental Bottleneck",
         "• 0–120 hours post-imbibition dictates crop establishment.\n• Suppresses germination capacity (-10% to -30% count).\n• Retards emergence speed (t50 lag of 12–36 hours).\n• Represses chlorophyll & anthocyanin biosynthesis via CRY1/HY5, resulting in severe seedling chlorosis.",
         RED_BG_LIGHT, RED_ALERT),
        ("3. Multi-Stressor Convergence on Mitochondria",
         "• Exploration atmosphere (56.5 kPa, 34% O2, high CO2) suppresses photorespiratory peroxisomal H2O2.\n• Electron burden shifts to mitochondria, causing ubiquinone (UQ) over-reduction.\n• Alternative Oxidase (AOX1D) induced to vent excess electrons; directly parallels human astronaut mitochondrial stress.",
         GREEN_BG_LIGHT, GREEN_SUCC)
    ]

    for idx, (title, body, bg_col, edge_col) in enumerate(pillars):
        left = Inches(0.8 + idx * 4.0)
        add_card(slide, left, Inches(1.75), Inches(3.733), Inches(3.6), bg_col, edge_col, border_width=1.2)
        tb = slide.shapes.add_textbox(left + Inches(0.2), Inches(1.9), Inches(3.333), Inches(3.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(11.5)
        p_t.font.bold = True
        p_t.font.color.rgb = edge_col

        p_b = tf.add_paragraph()
        p_b.text = body
        p_b.font.size = Pt(9.5)
        p_b.font.color.rgb = TEXT_DARK

    # Bottom summary callout card
    add_card(slide, Inches(0.8), Inches(5.55), Inches(11.733), Inches(1.3), CARD_BG_LIGHT, CARD_BORDER, border_width=1.0)
    tb_bot = slide.shapes.add_textbox(Inches(1.0), Inches(5.65), Inches(11.333), Inches(1.1))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True
    p_bot1 = tf_bot.paragraphs[0]
    p_bot1.text = "THE 5 CORE CONCEPTS INTEGRATED INTO THIS REVIEW:"
    p_bot1.font.size = Pt(9.5)
    p_bot1.font.bold = True
    p_bot1.font.color.rgb = BLUE_PRIMARY

    p_bot2 = tf_bot.add_paragraph()
    p_bot2.text = "1. Lunar Near-Null Reality (<0.8 nT)  |  2. Altered Germination Capacity (# Seedlings)  |  3. Delayed Emergence Velocity & Biomass Yield\n4. Cryptochrome/HY5 Pigment Repression  |  5. Multi-Stressor CO2 ↔ O2 ↔ ROS Convergence with Radiation & Astronaut Parallels"
    p_bot2.font.size = Pt(8.8)
    p_bot2.font.color.rgb = TEXT_DARK

    add_footer(slide, 2, 15)

    add_notes(slide,
        "TALKING POINTS (SLIDE 2 - NARRATIVE OVERVIEW):\n"
        "• This slide sets the narrative stage for the entire presentation.\n"
        "• For 60 years, plant spaceflight experiments have focused almost exclusively on gravity and ionizing radiation.\n"
        "• In contrast, the magnetic field is typically treated as a neutral background constant. On Earth and the ISS in LEO, plants develop inside the Earth's geomagnetic field (25–65 µT).\n"
        "• But on the Moon and in deep space, that protective field disappears. At candidate Artemis South Pole landing sites, the field is less than 0.8 nT.\n"
        "• We focus specifically on the first 5 days of growth (0–120 hours). This is the mission-critical window when seeds must imbibe water, mobilize reserves, germinate, break testa, and turn green to become photosynthetic.\n"
        "• We tie this to quantum biology via cryptochromes, and show how exploration atmospheres and radiation converge on mitochondrial bioenergetics."
    )

def build_slide_03_figure1_montage(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, WHITE_CANVAS)
    add_header(slide, "Figure 1 Montage | Editable Layout",
               "The Lunar Surface Magnetic Environment & Exploration Sites",
               "Global distribution, South Polar Artemis void (<0.8 nT), and vector superposition at the biological volume")

    # Grid coordinates for 4 separable subpanels:
    # Row 1: Left (a) 5.7" x 2.45", Right (b) 5.7" x 2.45"
    # Row 2: Left (c) 5.7" x 2.45", Right (d) 5.7" x 2.45"
    x_left  = Inches(0.8)
    x_right = Inches(6.833)
    y_top   = Inches(1.75)
    y_bot   = Inches(4.45)
    w_p     = Inches(5.7)
    h_p     = Inches(2.45)

    # Subpanel a
    add_card(slide, x_left, y_top, w_p, h_p, CARD_BG_LIGHT, CARD_BORDER)
    slide.shapes.add_picture(str(SUBPANELS_DIR / 'Fig1a_global_map.png'), x_left + Inches(0.1), y_top + Inches(0.35), w_p - Inches(0.2), h_p - Inches(0.42))
    tb_a = slide.shapes.add_textbox(x_left + Inches(0.15), y_top + Inches(0.05), w_p, Inches(0.3))
    tb_a.text_frame.paragraphs[0].text = "(a) Global Lunar Crustal Magnetic Field Distribution (|B| at 30 km)"
    tb_a.text_frame.paragraphs[0].font.size = Pt(9.0)
    tb_a.text_frame.paragraphs[0].font.bold = True
    tb_a.text_frame.paragraphs[0].font.color.rgb = BLUE_PRIMARY

    # Subpanel b
    add_card(slide, x_right, y_top, w_p, h_p, CARD_BG_LIGHT, CARD_BORDER)
    slide.shapes.add_picture(str(SUBPANELS_DIR / 'Fig1b_south_pole_artemis.png'), x_right + Inches(0.1), y_top + Inches(0.35), w_p - Inches(0.2), h_p - Inches(0.42))
    tb_b = slide.shapes.add_textbox(x_right + Inches(0.15), y_top + Inches(0.05), w_p, Inches(0.3))
    tb_b.text_frame.paragraphs[0].text = "(b) Artemis South Polar Exploration Footprint (<0.8 nT Void)"
    tb_b.text_frame.paragraphs[0].font.size = Pt(9.0)
    tb_b.text_frame.paragraphs[0].font.bold = True
    tb_b.text_frame.paragraphs[0].font.color.rgb = BLUE_PRIMARY

    # Subpanel c
    add_card(slide, x_left, y_bot, w_p, h_p, CARD_BG_LIGHT, CARD_BORDER)
    slide.shapes.add_picture(str(SUBPANELS_DIR / 'Fig1c_landing_sites_bar.png'), x_left + Inches(0.1), y_bot + Inches(0.35), w_p - Inches(0.2), h_p - Inches(0.42))
    tb_c = slide.shapes.add_textbox(x_left + Inches(0.15), y_bot + Inches(0.05), w_p, Inches(0.3))
    tb_c.text_frame.paragraphs[0].text = "(c) Field Magnitude at Historical & Candidate Sites vs. Earth GMF"
    tb_c.text_frame.paragraphs[0].font.size = Pt(9.0)
    tb_c.text_frame.paragraphs[0].font.bold = True
    tb_c.text_frame.paragraphs[0].font.color.rgb = BLUE_PRIMARY

    # Subpanel d
    add_card(slide, x_right, y_bot, w_p, h_p, CARD_BG_LIGHT, CARD_BORDER)
    slide.shapes.add_picture(str(SUBPANELS_DIR / 'Fig1d_superposition_box.png'), x_right + Inches(0.1), y_bot + Inches(0.35), w_p - Inches(0.2), h_p - Inches(0.42))
    tb_d = slide.shapes.add_textbox(x_right + Inches(0.15), y_bot + Inches(0.05), w_p, Inches(0.3))
    tb_d.text_frame.paragraphs[0].text = "(d) Vector Superposition & Lander DC Interference Hazard"
    tb_d.text_frame.paragraphs[0].font.size = Pt(9.0)
    tb_d.text_frame.paragraphs[0].font.bold = True
    tb_d.text_frame.paragraphs[0].font.color.rgb = BLUE_PRIMARY

    add_footer(slide, 3, 15)

    add_notes(slide,
        "TALKING POINTS (SLIDE 3 - FIGURE 1 MONTAGE):\n"
        "• Here is Figure 1 exactly as it appears in the manuscript, but reconstructed with independent, editable subpanels.\n"
        "• Panel (a) shows the global crustal magnetic field map from Lunar Prospector and Kaguya data at 30 km altitude. Notice that remanent crustal magnetization is concentrated in isolated swirls, while the South Polar region (dashed red box) is an extreme magnetic void.\n"
        "• Panel (b) zooms into the candidate Artemis South Pole landing sites. All sites, including Shackleton, Faustini Rim A, Haworth, and Connecting Ridge, fall strictly below 0.82 nT.\n"
        "• Panel (c) compares these sites across Apollo, Chang'e, and Artemis missions against Earth's field. Earth's dipolar field is 25,000–65,000 nT—over 30,000 times higher!\n"
        "• Panel (d) highlights a crucial operational trap: the net vector superposition. Unshielded lander avionics and DC power buses can emit 50–500 µT, completely swamping the natural lunar hypomagnetic vacuum unless sample-level 3-axis fluxgate magnetometers are deployed."
    )

def build_slide_04_figure1_deepdive(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, WHITE_CANVAS)
    add_header(slide, "Figure 1 Deep Dive", "Planetary Magnetic Fields & The Lander Interference Trap",
               "Why in-situ 3-axis fluxgate magnetometry is essential to decouple lunar biology from spacecraft avionics")

    # Left: Large Subpanel B + D stacked
    add_card(slide, Inches(0.8), Inches(1.75), Inches(5.6), Inches(2.45), CARD_BG_LIGHT, CARD_BORDER)
    slide.shapes.add_picture(str(SUBPANELS_DIR / 'Fig1b_south_pole_artemis.png'), Inches(0.9), Inches(1.85), Inches(5.4), Inches(2.25))

    add_card(slide, Inches(0.8), Inches(4.35), Inches(5.6), Inches(2.55), CARD_BG_LIGHT, CARD_BORDER)
    slide.shapes.add_picture(str(SUBPANELS_DIR / 'Fig1d_superposition_box.png'), Inches(0.9), Inches(4.45), Inches(5.4), Inches(2.35))

    # Right: Analytical breakdown & Table 1 data
    add_card(slide, Inches(6.6), Inches(1.75), Inches(5.933), Inches(5.15), CARD_BG_LIGHT, CARD_BORDER)
    tb_r = slide.shapes.add_textbox(Inches(6.8), Inches(1.9), Inches(5.533), Inches(4.85))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p1 = tf_r.paragraphs[0]
    p1.text = "TABLE 1: CANDIDATE ARTEMIS SITES VS. HISTORICAL SITES"
    p1.font.size = Pt(11.0)
    p1.font.bold = True
    p1.font.color.rgb = BLUE_PRIMARY

    p2 = tf_r.add_paragraph()
    p2.text = (
        "• Faustini Rim A: 0.45 nT (Near-null void)\n"
        "• Haworth Crater: 0.40 nT (Deep near-null void)\n"
        "• Connecting Ridge: 0.60 nT (Near-null void)\n"
        "• Peak Near Shackleton: 0.82 nT (Near-null void)\n"
        "• Apollo 16 (Descartes): 4.94 nT (Crustal swirl paleomagnetism)\n"
        "• Earth Dipolar Surface: 25,000 – 65,000 nT (>30,000× higher)"
    )
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = TEXT_DARK

    p3 = tf_r.add_paragraph()
    p3.text = "\nTHE CRITICAL SUPERPOSITION HAZARD:"
    p3.font.size = Pt(11.0)
    p3.font.bold = True
    p3.font.color.rgb = RED_ALERT

    p4 = tf_r.add_paragraph()
    p4.text = (
        "1. The Vector Equation:\n"
        "   B_total(t, x) = B_crust + B_ext + B_lander + B_payload + B_control\n"
        "2. The Lander Confounder:\n"
        "   Commercial lunar landers carry heavy DC power wiring, batteries, and reaction wheels that produce localized fields of 50–500 µT.\n"
        "3. The Operational Mandate:\n"
        "   Unless biological growth chambers feature sample-level 3-axis fluxgate telemetry, experiments risk measuring stray avionics EMI rather than true lunar near-null biology!"
    )
    p4.font.size = Pt(9.2)
    p4.font.color.rgb = TEXT_DARK

    add_footer(slide, 4, 15)

    add_notes(slide,
        "TALKING POINTS (SLIDE 4 - FIGURE 1 DEEP DIVE):\n"
        "• Let's dive deeper into the physics of the lunar landing sites.\n"
        "• Notice from Table 1 that every single candidate landing site for Artemis III and future Artemis missions has a crustal magnetic field below 1 nanotesla.\n"
        "• Haworth is at 0.40 nT; Faustini Rim A is at 0.45 nT; Peak Near Shackleton is 0.82 nT.\n"
        "• Compare that to Apollo 16 Descartes highlands, where local crustal anomalies reach 4.94 nT, or Earth where the field is 50,000 nT.\n"
        "• But here is the critical engineering challenge: look at the superposition equation at the bottom left.\n"
        "• If a plant growth payload like LEAF is bolted to an unshielded lander deck, the DC currents from battery buses and avionics produce magnetic fields up to 500 µT right at the chamber wall!\n"
        "• That would completely mask the lunar near-null field. That's why our paper makes the strong operational recommendation: you MUST put a 3-axis fluxgate sensor directly inside the specimen volume."
    )

def build_slide_05_figure2_montage(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, WHITE_CANVAS)
    add_header(slide, "Figure 2 Montage | Editable Layout",
               "The First 5 Days: Early Seedling Kinetics & Pigment Formation",
               "0–120 h developmental trajectory, emergence velocity lag (t50), biomass yield penalties, and pigment repression")

    x_left  = Inches(0.8)
    x_right = Inches(6.833)
    y_top   = Inches(1.75)
    y_bot   = Inches(4.45)
    w_p     = Inches(5.7)
    h_p     = Inches(2.45)

    # Subpanel a
    add_card(slide, x_left, y_top, w_p, h_p, CARD_BG_LIGHT, CARD_BORDER)
    slide.shapes.add_picture(str(SUBPANELS_DIR / 'Fig2a_5day_timeline.png'), x_left + Inches(0.1), y_top + Inches(0.35), w_p - Inches(0.2), h_p - Inches(0.42))
    tb_a = slide.shapes.add_textbox(x_left + Inches(0.15), y_top + Inches(0.05), w_p, Inches(0.3))
    tb_a.text_frame.paragraphs[0].text = "(a) 5-Day Developmental Timeline: Imbibition to Autotrophy"
    tb_a.text_frame.paragraphs[0].font.size = Pt(9.0)
    tb_a.text_frame.paragraphs[0].font.bold = True
    tb_a.text_frame.paragraphs[0].font.color.rgb = BLUE_PRIMARY

    # Subpanel b
    add_card(slide, x_right, y_top, w_p, h_p, CARD_BG_LIGHT, CARD_BORDER)
    slide.shapes.add_picture(str(SUBPANELS_DIR / 'Fig2b_germination_kinetics.png'), x_right + Inches(0.1), y_top + Inches(0.35), w_p - Inches(0.2), h_p - Inches(0.42))
    tb_b = slide.shapes.add_textbox(x_right + Inches(0.15), y_top + Inches(0.05), w_p, Inches(0.3))
    tb_b.text_frame.paragraphs[0].text = "(b) Germination Capacity (#) & Kinetics Lag (t50: +12 to +36 h)"
    tb_b.text_frame.paragraphs[0].font.size = Pt(9.0)
    tb_b.text_frame.paragraphs[0].font.bold = True
    tb_b.text_frame.paragraphs[0].font.color.rgb = BLUE_PRIMARY

    # Subpanel c
    add_card(slide, x_left, y_bot, w_p, h_p, CARD_BG_LIGHT, CARD_BORDER)
    slide.shapes.add_picture(str(SUBPANELS_DIR / 'Fig2c_biomass_yield.png'), x_left + Inches(0.1), y_bot + Inches(0.35), w_p - Inches(0.2), h_p - Inches(0.42))
    tb_c = slide.shapes.add_textbox(x_left + Inches(0.15), y_bot + Inches(0.05), w_p, Inches(0.3))
    tb_c.text_frame.paragraphs[0].text = "(c) Seedling Elongation, Vigor & Harvestable Biomass Yield Penalty"
    tb_c.text_frame.paragraphs[0].font.size = Pt(9.0)
    tb_c.text_frame.paragraphs[0].font.bold = True
    tb_c.text_frame.paragraphs[0].font.color.rgb = BLUE_PRIMARY

    # Subpanel d
    add_card(slide, x_right, y_bot, w_p, h_p, CARD_BG_LIGHT, CARD_BORDER)
    slide.shapes.add_picture(str(SUBPANELS_DIR / 'Fig2d_pigment_pathway.png'), x_right + Inches(0.1), y_bot + Inches(0.35), w_p - Inches(0.2), h_p - Inches(0.42))
    tb_d = slide.shapes.add_textbox(x_right + Inches(0.15), y_bot + Inches(0.05), w_p, Inches(0.3))
    tb_d.text_frame.paragraphs[0].text = "(d) Cryptochrome/HY5 Downregulation & Pigment Repression"
    tb_d.text_frame.paragraphs[0].font.size = Pt(9.0)
    tb_d.text_frame.paragraphs[0].font.bold = True
    tb_d.text_frame.paragraphs[0].font.color.rgb = BLUE_PRIMARY

    add_footer(slide, 5, 15)

    add_notes(slide,
        "TALKING POINTS (SLIDE 5 - FIGURE 2 MONTAGE):\n"
        "• Figure 2 focuses on the biological core of the paper: the first 5 days of growth (0–120 hours).\n"
        "• Panel (a) breaks down the developmental timeline into 4 distinct phases: Phase I imbibition (0–12 h), Phase II peroxisomal catabolism (12–48 h), Phase III radicle emergence (48–72 h), and Phase IV de-etiolation and autotrophic greening (72–120 h).\n"
        "• Panel (b) shows empirical germination kinetics. Under near-null magnetic fields, two critical defects occur: first, the total number of germinated seeds drops by 10–30%; second, the emergence speed (t50) is delayed by 12–36 hours.\n"
        "• Panel (c) shows the vegetative yield consequences: radicle elongation is reduced by 33%, hypocotyl height by 31%, and total fresh/dry biomass by 28.5% on Day 5.\n"
        "• Panel (d) maps the molecular pathway: cryptochromes perceive blue light and form radical pairs. Under near-null fields, HY5 transcription factor stabilization is impaired, downregulating rate-limiting chlorophyll genes (HEMA1, POR) and anthocyanin genes (CHS, CHI), creating severe seedling chlorosis."
    )

def build_slide_06_figure2_deepdive(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, WHITE_CANVAS)
    add_header(slide, "Figure 2 Deep Dive", "The Day 0–5 Bottleneck: Emergence Kinetics & Biomass Deficits",
               "Why early germination delay compounds into substantial yield losses in closed-loop life support systems")

    # Left: Large Subpanel B + C stacked
    add_card(slide, Inches(0.8), Inches(1.75), Inches(5.6), Inches(2.5), CARD_BG_LIGHT, CARD_BORDER)
    slide.shapes.add_picture(str(SUBPANELS_DIR / 'Fig2b_germination_kinetics.png'), Inches(0.9), Inches(1.85), Inches(5.4), Inches(2.3))

    add_card(slide, Inches(0.8), Inches(4.4), Inches(5.6), Inches(2.5), CARD_BG_LIGHT, CARD_BORDER)
    slide.shapes.add_picture(str(SUBPANELS_DIR / 'Fig2c_biomass_yield.png'), Inches(0.9), Inches(4.5), Inches(5.4), Inches(2.3))

    # Right: Quantitative Analysis
    add_card(slide, Inches(6.6), Inches(1.75), Inches(5.933), Inches(5.15), CARD_BG_LIGHT, CARD_BORDER)
    tb_r = slide.shapes.add_textbox(Inches(6.8), Inches(1.9), Inches(5.533), Inches(4.85))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p1 = tf_r.paragraphs[0]
    p1.text = "AGRONOMIC & CELLULAR CONSEQUENCES OF NNMF:"
    p1.font.size = Pt(11.0)
    p1.font.bold = True
    p1.font.color.rgb = BLUE_PRIMARY

    p2 = tf_r.add_paragraph()
    p2.text = (
        "1. Emergence Velocity Lag (Δt50 = 12–36 hours):\n"
        "   • Delayed water uptake in Phase I and slowed endosperm reserve mobilization.\n"
        "   • Testa rupture is postponed, shifting the entire autotrophic transition window.\n\n"
        "2. Cellular Division & Auxin Transport Suppression:\n"
        "   • Dampened mitotic index in the root apical meristem (RAM).\n"
        "   • Disrupted polar localization of PIN2 auxin efflux carriers causes stunted, disoriented primary roots.\n\n"
        "3. Crop Biomass & Canopy Interception Loss:\n"
        "   • Radicle length: -33.0% on Day 3\n"
        "   • Hypocotyl height: -31.0% on Day 5\n"
        "   • Total fresh biomass: -29.1% deficit on Day 5\n\n"
        "4. Operational BLSS Impact:\n"
        "   • Uneven seedling emergence creates patchy canopy architecture.\n"
        "   • Sub-optimal light interception dampens net photosynthetic CO2 scrubbing and fresh food yields, threatening tight mission dietary schedules."
    )
    p2.font.size = Pt(9.2)
    p2.font.color.rgb = TEXT_DARK

    add_footer(slide, 6, 15)

    add_notes(slide,
        "TALKING POINTS (SLIDE 6 - FIGURE 2 DEEP DIVE):\n"
        "• Why does a delay of 12 to 36 hours in germination matter on the Moon?\n"
        "• In field agriculture on Earth, seeds have excess time and buffer. In a tightly scheduled spaceflight payload like LEAF on Artemis III, or a lunar greenhouse, mission timelines are strictly constrained.\n"
        "• LEAF is designed for a nominal mission duration of around 7 to 10 days. If seed germination is delayed by 36 hours, you lose 30% to 50% of your autotrophic growth window!\n"
        "• Furthermore, at the cellular level, near-null fields reduce cell division in the root apical meristem and disrupt PIN2 auxin carriers. That means roots grow slower, are more disoriented, and absorb water and nutrients less efficiently.\n"
        "• The resulting 28% drop in biomass is not an academic curiosity—it is a direct hit to the caloric and nutrient yield of space crops."
    )

def build_slide_07_figure3_montage(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, WHITE_CANVAS)
    add_header(slide, "Figure 3 Montage | Editable Layout",
               "Quantum Molecular Biology of the 0–5 Day Window",
               "Peroxisomal reserve mobilization (QBM-06), evidentiary tiers (T1–T4), and organellar electron transport hubs")

    # Layout: Top panel A spans full width (11.733" x 2.45")
    # Bottom Row: Left Panel B (5.7" x 2.45"), Right Panel C (5.7" x 2.45")
    x_full  = Inches(0.8)
    w_full  = Inches(11.733)
    y_top   = Inches(1.75)
    y_bot   = Inches(4.45)
    x_left  = Inches(0.8)
    x_right = Inches(6.833)
    w_half  = Inches(5.7)
    h_p     = Inches(2.45)

    # Subpanel a
    add_card(slide, x_full, y_top, w_full, h_p, CARD_BG_LIGHT, CARD_BORDER)
    slide.shapes.add_picture(str(SUBPANELS_DIR / 'Fig3a_qbm06_pathway.png'), x_full + Inches(0.1), y_top + Inches(0.35), w_full - Inches(0.2), h_p - Inches(0.42))
    tb_a = slide.shapes.add_textbox(x_full + Inches(0.15), y_top + Inches(0.05), w_full, Inches(0.3))
    tb_a.text_frame.paragraphs[0].text = "(a) QBM-06 Pathway: Reserve Mobilization, Peroxisomal β-Oxidation & Mitochondrial Respiration (0–72 h)"
    tb_a.text_frame.paragraphs[0].font.size = Pt(9.0)
    tb_a.text_frame.paragraphs[0].font.bold = True
    tb_a.text_frame.paragraphs[0].font.color.rgb = BLUE_PRIMARY

    # Subpanel b
    add_card(slide, x_left, y_bot, w_half, h_p, CARD_BG_LIGHT, CARD_BORDER)
    slide.shapes.add_picture(str(SUBPANELS_DIR / 'Fig3b_evidentiary_tiers.png'), x_left + Inches(0.1), y_bot + Inches(0.35), w_half - Inches(0.2), h_p - Inches(0.42))
    tb_b = slide.shapes.add_textbox(x_left + Inches(0.15), y_bot + Inches(0.05), w_half, Inches(0.3))
    tb_b.text_frame.paragraphs[0].text = "(b) Evidentiary Tier Hierarchy (T1 Demonstrated to T4 Context)"
    tb_b.text_frame.paragraphs[0].font.size = Pt(9.0)
    tb_b.text_frame.paragraphs[0].font.bold = True
    tb_b.text_frame.paragraphs[0].font.color.rgb = BLUE_PRIMARY

    # Subpanel c
    add_card(slide, x_right, y_bot, w_half, h_p, CARD_BG_LIGHT, CARD_BORDER)
    slide.shapes.add_picture(str(SUBPANELS_DIR / 'Fig3c_organellar_etc.png'), x_right + Inches(0.1), y_bot + Inches(0.35), w_half - Inches(0.2), h_p - Inches(0.42))
    tb_c = slide.shapes.add_textbox(x_right + Inches(0.15), y_bot + Inches(0.05), w_half, Inches(0.3))
    tb_c.text_frame.paragraphs[0].text = "(c) Organellar Electron Transport Hubs (Chloroplast PETC & Mitochondrial AOX)"
    tb_c.text_frame.paragraphs[0].font.size = Pt(9.0)
    tb_c.text_frame.paragraphs[0].font.bold = True
    tb_c.text_frame.paragraphs[0].font.color.rgb = BLUE_PRIMARY

    add_footer(slide, 7, 15)

    add_notes(slide,
        "TALKING POINTS (SLIDE 7 - FIGURE 3 MONTAGE):\n"
        "• In Figure 3, we address the biophysical mechanism: How can an ambient magnetic field of less than 1 nanotesla produce measurable macroscopic changes in plant growth?\n"
        "• Thermal energy at room temperature (k_B * T) is orders of magnitude larger than magnetic Zeeman energy. Traditional thermodynamic arguments claimed magnetic fields couldn't affect biology.\n"
        "• The radical pair mechanism circumvents this thermodynamic equilibrium constraint. When cryptochromes absorb blue light, they form transient radical pairs between flavin adenine dinucleotide (FAD) and a triad of tryptophan residues.\n"
        "• Panel (a) illustrates the metabolic highway: triacylglycerols in peroxisomes undergo beta-oxidation, producing succinate which enters the mitochondrial electron transport chain.\n"
        "• Panel (b) introduces our rigorous 4-tier evidentiary hierarchy: T1 represents demonstrated quantum biology in cryptochromes; T2 represents plausible enzymatic radical pairs; T3 and T4 are speculative or context-based.\n"
        "• Panel (c) shows how chloroplasts and mitochondria act as the dual bioenergetic hubs that absorb these quantum perturbations."
    )

def build_slide_08_figure3_deepdive(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, WHITE_CANVAS)
    add_header(slide, "Figure 3 Deep Dive", "Cryptochrome Spin Dynamics & Evidentiary Rigor",
               "Separating rigorously demonstrated radical pair quantum biology (T1/T2) from speculative claims (T3/T4)")

    # Left: Large Subpanel B + C stacked
    add_card(slide, Inches(0.8), Inches(1.75), Inches(5.6), Inches(2.5), CARD_BG_LIGHT, CARD_BORDER)
    slide.shapes.add_picture(str(SUBPANELS_DIR / 'Fig3b_evidentiary_tiers.png'), Inches(0.9), Inches(1.85), Inches(5.4), Inches(2.3))

    add_card(slide, Inches(0.8), Inches(4.4), Inches(5.6), Inches(2.5), CARD_BG_LIGHT, CARD_BORDER)
    slide.shapes.add_picture(str(SUBPANELS_DIR / 'Fig3c_organellar_etc.png'), Inches(0.9), Inches(4.5), Inches(5.4), Inches(2.3))

    # Right: Analytical breakdown
    add_card(slide, Inches(6.6), Inches(1.75), Inches(5.933), Inches(5.15), CARD_BG_LIGHT, CARD_BORDER)
    tb_r = slide.shapes.add_textbox(Inches(6.8), Inches(1.9), Inches(5.533), Inches(4.85))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p1 = tf_r.paragraphs[0]
    p1.text = "THE RADICAL PAIR SPIN-CHEMICAL MECHANISM:"
    p1.font.size = Pt(11.0)
    p1.font.bold = True
    p1.font.color.rgb = BLUE_PRIMARY

    p2 = tf_r.add_paragraph()
    p2.text = (
        "1. Radical Pair Formation:\n"
        "   • Photon absorption (450 nm blue light) promotes electron transfer:\n"
        "     FAD + TrpH → [FAD•- ... TrpH•+]\n"
        "   • Generates a spin-correlated singlet-triplet pair.\n\n"
        "2. Zeeman & Hyperfine Modulation:\n"
        "   • In Earth's GMF (45 µT), external Zeeman splitting alters singlet-to-triplet interconversion rates.\n"
        "   • In Near-Null Fields (<0.8 nT), Zeeman mixing collapses, altering radical pair lifetimes and yields.\n\n"
        "3. Downstream Signaling Attenuation:\n"
        "   • Reduced cryptochrome active signaling decreases COP1/SPA1 dissociation.\n"
        "   • Less HY5 transcription factor is stabilized in the nucleus.\n"
        "   • Direct repression of HEMA1, POR, CHS, and CHI (chlorophyll and anthocyanin chlorosis).\n\n"
        "4. Critical Evidentiary Tiers:\n"
        "   • T1 (Solid): Cryptochrome FAD•- in vitro magnetic sensitivity.\n"
        "   • T2 (Plausible): Peroxisomal flavin oxidase radical pairs.\n"
        "   • T3/T4 (Speculative): Mitochondrial DNA quantum coherence."
    )
    p2.font.size = Pt(9.0)
    p2.font.color.rgb = TEXT_DARK

    add_footer(slide, 8, 15)

    add_notes(slide,
        "TALKING POINTS (SLIDE 8 - FIGURE 3 DEEP DIVE):\n"
        "• This slide is essential for defending our paper against skeptical reviewers.\n"
        "• Often when people hear 'quantum biology', they immediately think of speculative claims about macroscopic room-temperature coherence.\n"
        "• We make it crystal clear: Cryptochrome magnetoreception is grounded in rigorous spin chemistry, established over 20 years by Ritz, Hore, Ahmad, and others.\n"
        "• The radical pair [FAD•- ... TrpH•+] lives for microseconds. During that brief nanosecond-to-microsecond window, the electron spins are entangled. The presence or absence of an external magnetic field changes whether the pair recombines as a singlet or diffuses as a triplet.\n"
        "• In near-null fields, that interconversion is shifted, which alters the lifetime of the signaling state of cryptochrome.\n"
        "• This directly explains why cryptochrome-regulated genes like HY5, HEMA1, and CHS are downregulated in hypomagnetic chambers!"
    )

def build_slide_09_figure4_montage(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, WHITE_CANVAS)
    add_header(slide, "Figure 4 Montage | Editable Layout",
               "Multi-Stressor Convergence: The CO2 <-> O2 <-> ROS Nexus",
               "Exploration atmospheres, hypomagnetic fields, and ionizing radiation converge on mitochondrial Alternative Oxidase (AOX1D)")

    x_left  = Inches(0.8)
    x_right = Inches(6.833)
    y_top   = Inches(1.75)
    y_bot   = Inches(4.45)
    w_p     = Inches(5.7)
    h_p     = Inches(2.45)

    # Subpanel a
    add_card(slide, x_left, y_top, w_p, h_p, CARD_BG_LIGHT, CARD_BORDER)
    slide.shapes.add_picture(str(SUBPANELS_DIR / 'Fig4a_multistressor_space.png'), x_left + Inches(0.1), y_top + Inches(0.35), w_p - Inches(0.2), h_p - Inches(0.42))
    tb_a = slide.shapes.add_textbox(x_left + Inches(0.15), y_top + Inches(0.05), w_p, Inches(0.3))
    tb_a.text_frame.paragraphs[0].text = "(a) Multi-Stressor Space: Exploration Atmosphere, NNMF & Radiation"
    tb_a.text_frame.paragraphs[0].font.size = Pt(9.0)
    tb_a.text_frame.paragraphs[0].font.bold = True
    tb_a.text_frame.paragraphs[0].font.color.rgb = BLUE_PRIMARY

    # Subpanel b
    add_card(slide, x_right, y_top, w_p, h_p, CARD_BG_LIGHT, CARD_BORDER)
    slide.shapes.add_picture(str(SUBPANELS_DIR / 'Fig4b_bioenergetic_engine.png'), x_right + Inches(0.1), y_top + Inches(0.35), w_p - Inches(0.2), h_p - Inches(0.42))
    tb_b = slide.shapes.add_textbox(x_right + Inches(0.15), y_top + Inches(0.05), w_p, Inches(0.3))
    tb_b.text_frame.paragraphs[0].text = "(b) The Mitochondrial & Peroxisomal CO2 <-> O2 <-> ROS Engine"
    tb_b.text_frame.paragraphs[0].font.size = Pt(9.0)
    tb_b.text_frame.paragraphs[0].font.bold = True
    tb_b.text_frame.paragraphs[0].font.color.rgb = BLUE_PRIMARY

    # Subpanel c
    add_card(slide, x_left, y_bot, w_p, h_p, CARD_BG_LIGHT, CARD_BORDER)
    slide.shapes.add_picture(str(SUBPANELS_DIR / 'Fig4c_multiomics_overlap.png'), x_left + Inches(0.1), y_bot + Inches(0.35), w_p - Inches(0.2), h_p - Inches(0.42))
    tb_c = slide.shapes.add_textbox(x_left + Inches(0.15), y_bot + Inches(0.05), w_p, Inches(0.3))
    tb_c.text_frame.paragraphs[0].text = "(c) Multi-Omics Empirical Overlap: OSD-782 Radiation vs. NNMF Loci"
    tb_c.text_frame.paragraphs[0].font.size = Pt(9.0)
    tb_c.text_frame.paragraphs[0].font.bold = True
    tb_c.text_frame.paragraphs[0].font.color.rgb = BLUE_PRIMARY

    # Subpanel d
    add_card(slide, x_right, y_bot, w_p, h_p, CARD_BG_LIGHT, CARD_BORDER)
    slide.shapes.add_picture(str(SUBPANELS_DIR / 'Fig4d_crosskingdom_astronaut.png'), x_right + Inches(0.1), y_bot + Inches(0.35), w_p - Inches(0.2), h_p - Inches(0.42))
    tb_d = slide.shapes.add_textbox(x_right + Inches(0.15), y_bot + Inches(0.05), w_p, Inches(0.3))
    tb_d.text_frame.paragraphs[0].text = "(d) Cross-Kingdom Convergence: Plant BLSS & Human Astronaut Health"
    tb_d.text_frame.paragraphs[0].font.size = Pt(9.0)
    tb_d.text_frame.paragraphs[0].font.bold = True
    tb_d.text_frame.paragraphs[0].font.color.rgb = BLUE_PRIMARY

    add_footer(slide, 9, 15)

    add_notes(slide,
        "TALKING POINTS (SLIDE 9 - FIGURE 4 MONTAGE):\n"
        "• Figure 4 brings together the environmental multi-stressor nexus.\n"
        "• In real exploration missions, plants will not experience hypomagnetic fields in isolation. They will face them simultaneously with NASA's exploration atmosphere (56.5 kPa / 8.2 psia, 34% O2, and 1200–3000 ppm CO2) and chronic GCR radiation.\n"
        "• Panel (a) contrasts these baseline environmental parameters.\n"
        "• Panel (b) shows how these stressors interact at the biochemical level. Elevated CO2 suppresses RuBisCO oxygenation, shutting down peroxisomal H2O2 production. That shifts the electron burden onto mitochondria. When the ubiquinone pool becomes over-reduced, electrons leak, forming superoxide.\n"
        "• Alternative Oxidase (AOX1D) acts as an uncoupled safety valve, directly dumping electrons to oxygen without ATP synthesis to prevent ROS bursts.\n"
        "• In Panel (c), we validate this empirically: NASA OSDR dataset OSD-782 (ionizing radiation) and Parmagnani 2022 (near-null magnetic field) show concordant upregulation of AOX1D and CAT3.\n"
        "• Panel (d) reveals the profound cross-kingdom parallel: human astronauts in the NASA Twins Study and Cell 2020 multi-omics exhibit the exact same mitochondrial stress phenotype!"
    )

def build_slide_10_figure4_deepdive(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, WHITE_CANVAS)
    add_header(slide, "Figure 4 Deep Dive", "Mitochondrial Bioenergetics & Human Astronaut Parallels",
               "Mitochondrial dysfunction is the universal biological signature linking space crops and astronaut crews")

    # Left: Large Subpanel C + D stacked
    add_card(slide, Inches(0.8), Inches(1.75), Inches(5.6), Inches(2.5), CARD_BG_LIGHT, CARD_BORDER)
    slide.shapes.add_picture(str(SUBPANELS_DIR / 'Fig4c_multiomics_overlap.png'), Inches(0.9), Inches(1.85), Inches(5.4), Inches(2.3))

    add_card(slide, Inches(0.8), Inches(4.4), Inches(5.6), Inches(2.5), CARD_BG_LIGHT, CARD_BORDER)
    slide.shapes.add_picture(str(SUBPANELS_DIR / 'Fig4d_crosskingdom_astronaut.png'), Inches(0.9), Inches(4.5), Inches(5.4), Inches(2.3))

    # Right: Analytical breakdown
    add_card(slide, Inches(6.6), Inches(1.75), Inches(5.933), Inches(5.15), CARD_BG_LIGHT, CARD_BORDER)
    tb_r = slide.shapes.add_textbox(Inches(6.8), Inches(1.9), Inches(5.533), Inches(4.85))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p1 = tf_r.paragraphs[0]
    p1.text = "THE SHARED BIOENERGETIC PHENOTYPE:"
    p1.font.size = Pt(11.0)
    p1.font.bold = True
    p1.font.color.rgb = BLUE_PRIMARY

    p2 = tf_r.add_paragraph()
    p2.text = (
        "1. The Alternative Oxidase (AOX) Safety Valve:\n"
        "   • In plants, Alternative Oxidase (AOX1D, AT1G32350) acts as an uncoupled terminal oxidase.\n"
        "   • Bypasses Complexes III and IV to oxidize ubiquinol directly to H2O without pumping protons.\n"
        "   • Prevents runaway superoxide (O2•-) formation at Complex I and III.\n\n"
        "2. Empirical Concordance (NASA OSDR OSD-782 vs. NNMF):\n"
        "   • AOX1D: +2.45 log2FC (Radiation) | +1.88 log2FC (NNMF)\n"
        "   • CAT3: +1.92 log2FC (Radiation) | +1.45 log2FC (NNMF)\n"
        "   • HEMA1: -1.85 log2FC (Radiation) | -2.10 log2FC (NNMF)\n\n"
        "3. Cross-Kingdom Spaceflight Nexus:\n"
        "   • Afshinnekoo et al. (Cell 2020) and the NASA Twins Study identified mitochondrial dysfunction as the single most conserved hallmark across astronaut tissues.\n"
        "   • High cell-free mitochondrial DNA (cf-mtDNA), elevated ROS, and respiratory chain decoupling occur in both human astronauts and lunar plants!"
    )
    p2.font.size = Pt(9.0)
    p2.font.color.rgb = TEXT_DARK

    add_footer(slide, 10, 15)

    add_notes(slide,
        "TALKING POINTS (SLIDE 10 - FIGURE 4 DEEP DIVE):\n"
        "• This cross-kingdom connection is one of the most exciting takeaways of our review paper.\n"
        "• In 2020, Afshinnekoo and a large international team published a landmark paper in Cell analyzing 29 spaceflight omics datasets.\n"
        "• They found that whether you look at astronaut muscle, liver, immune cells, or mouse models, mitochondrial dysregulation is the central master biomarker of spaceflight stress.\n"
        "• In plants, mitochondria face the exact same problem: hypobaric atmospheres, radiation, and near-null magnetic fields all force electron leakage at Complexes I and III.\n"
        "• Plants survive this using Alternative Oxidase (AOX1D), which vents excess electrons. Humans do not have AOX, and therefore suffer severe mitochondrial oxidative damage.\n"
        "• This elevates plant space biology from an isolated agricultural study to a fundamental pillar of comparative space bioenergetics."
    )

def build_slide_11_figure5_montage(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, WHITE_CANVAS)
    add_header(slide, "Figure 5 Montage | Editable Layout",
               "Ground Simulation Standards & Post-Flight Disambiguation",
               "3-chamber ground controls, in situ causal rescue proof-of-concept, and post-flight phenotypic disambiguation framework")

    x_left  = Inches(0.8)
    x_right = Inches(6.833)
    x_full  = Inches(0.8)
    w_half  = Inches(5.7)
    w_full  = Inches(11.733)
    y_top   = Inches(1.75)
    h_top   = Inches(2.4)
    y_bot   = Inches(4.35)
    h_bot   = Inches(2.55)

    # Subpanel a (Ground Chambers)
    add_card(slide, x_left, y_top, w_half, h_top, CARD_BG_LIGHT, CARD_BORDER)
    slide.shapes.add_picture(str(SUBPANELS_DIR / 'Fig5a_ground_chambers.png'), x_left + Inches(0.1), y_top + Inches(0.35), w_half - Inches(0.2), h_top - Inches(0.42))
    tb_a = slide.shapes.add_textbox(x_left + Inches(0.15), y_top + Inches(0.05), w_half, Inches(0.3))
    tb_a.text_frame.paragraphs[0].text = "(a) Methodological Ground Simulation Standards (3-Chamber Parity)"
    tb_a.text_frame.paragraphs[0].font.size = Pt(9.0)
    tb_a.text_frame.paragraphs[0].font.bold = True
    tb_a.text_frame.paragraphs[0].font.color.rgb = BLUE_PRIMARY

    # Subpanel b (Hardware Self-Magnetic Assessment)
    add_card(slide, x_right, y_top, w_half, h_top, CARD_BG_LIGHT, CARD_BORDER)
    slide.shapes.add_picture(str(SUBPANELS_DIR / 'Fig5b_hardware_assessment.png'), x_right + Inches(0.1), y_top + Inches(0.35), w_half - Inches(0.2), h_top - Inches(0.42))
    tb_b = slide.shapes.add_textbox(x_right + Inches(0.15), y_top + Inches(0.05), w_half, Inches(0.3))
    tb_b.text_frame.paragraphs[0].text = "(b) Hardware Self-Magnetic Assessment Protocol (Power-State Mapping)"
    tb_b.text_frame.paragraphs[0].font.size = Pt(9.0)
    tb_b.text_frame.paragraphs[0].font.bold = True
    tb_b.text_frame.paragraphs[0].font.color.rgb = BLUE_PRIMARY

    # Subpanel c (Phenotypic Disambiguation Framework)
    add_card(slide, x_full, y_bot, w_full, h_bot, CARD_BG_LIGHT, CARD_BORDER)
    slide.shapes.add_picture(str(SUBPANELS_DIR / 'Fig5c_decision_matrix.png'), x_full + Inches(0.1), y_bot + Inches(0.35), w_full - Inches(0.2), h_bot - Inches(0.42))
    tb_c = slide.shapes.add_textbox(x_full + Inches(0.15), y_bot + Inches(0.05), w_full, Inches(0.3))
    tb_c.text_frame.paragraphs[0].text = "(c) Post-Flight Phenotypic Risk Disambiguation Framework (Comparative Matrix)"
    tb_c.text_frame.paragraphs[0].font.size = Pt(9.0)
    tb_c.text_frame.paragraphs[0].font.bold = True
    tb_c.text_frame.paragraphs[0].font.color.rgb = BLUE_PRIMARY

    add_footer(slide, 11, 15)

    add_notes(slide,
        "TALKING POINTS (SLIDE 11 - FIGURE 5 MONTAGE):\n"
        "• Figure 5 establishes our translational roadmap, focusing on rigorous ground simulation methods and post-flight disambiguation.\n"
        "• Panel (a) sets the 3-chamber ground standard: Chamber 1 (GMF terrestrial control), Chamber 2 (Shielded/Cancelled NNMF lunar simulation), and Chamber 3 (Bifilar sham control matching current, heat, and vibration without magnetic fields).\n"
        "• Panel (b) introduces our hardware self-magnetic assessment protocol: Characterizing induced magnetic fields across subsystem operating states (LED PAR lighting, fluidic pumps, thermal heaters, and avionics bus) to establish empirical transfer functions that subtract hardware self-fields without requiring active coils in flight.\n"
        "• Panel (c) provides our post-flight phenotypic disambiguation framework: A full comparative matrix distinguishing hypomagnetic lesions from lunar partial gravity (0.166 g) and deep-space cosmic radiation (GCR) using specific cellular targets and diagnostic rescue strategies."
    )

def build_slide_12_figure5_deepdive_table(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, WHITE_CANVAS)
    add_header(slide, "Table 3 Deep Dive", "Phenotypic Risk Disambiguation Matrix for Lunar Plant Biology",
               "Diagnostic criteria to decouple Near-Null Magnetic Fields from Lunar Partial Gravity and Deep-Space Radiation")

    # Native PowerPoint Table
    rows = 4
    cols = 4
    left = Inches(0.8)
    top = Inches(1.8)
    width = Inches(11.733)
    height = Inches(4.9)

    table_shape = slide.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table

    # Column widths
    table.columns[0].width = Inches(2.2)   # Stressor
    table.columns[1].width = Inches(2.8)   # Target
    table.columns[2].width = Inches(3.6)   # Phenotypic Signature
    table.columns[3].width = Inches(3.133) # Disambiguation Strategy

    headers = ["Environmental Stressor", "Primary Cellular Target", "Phenotypic Diagnostic Signature (Days 0–5)", "Disambiguation Strategy"]
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_DARK
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE

    gate_data = [
        ("Near-Null Magnetic Field\n(NNMF, < 10 nT)",
         "Cryptochrome radical pairs\n[FAD•- ... TrpH•+];\nSDP1 triacylglycerol lipase.",
         "• Emergence lag (Δt50 = +12–36 h)\n• 10%–30% capacity drop; chlorosis\n• Downregulated HEMA1/CHLH/POR\n• Mitochondrial AOX1D & CAT3 leak\n• Minimal nuclear DNA breaks",
         "• Reversible by in situ 45 µT vector re-application (causal rescue).\n• Insensitive to 1g spin centrifugation.\n• Correlates with 3-axis magnetometer canopy telemetry.",
         RED_BG_LIGHT, RED_ALERT),
        ("Lunar Partial Gravity\n(0.166 g) / Microgravity",
         "Amyloplast statolith sedimentation;\nMechanosensitive ion channels (MSL/MCA);\nPIN auxin carrier polarity.",
         "• Normal germination capacity\n• Negligible emergence lag (Δt50 < 4 h)\n• Random root waving & directional skewing\n• Normal plastid greening under PAR\n• Localized apoplastic ROS (RBOHD/F)",
         "• Fully rescued by onboard 1g centrifuge controls.\n• Completely insensitive to static magnetic field manipulation.\n• Quantified via camera morphometry.",
         GREEN_BG_LIGHT, GREEN_SUCC),
        ("Deep-Space Radiation\n(GCR / SPE)",
         "Direct nuclear DNA ionization;\nRadiolysis of H2O producing •OH;\nOxidation of Fe-S clusters.",
         "• Emergence failure only at lethal doses\n• Mitotic apical cell cycle arrest\n• Severe chromosomal aberrations\n• High γ-H2AX phosphorylated foci\n• Marked lipid peroxidation (MDA)",
         "• Mitigated by passive polyethylene or water-wall shielding.\n• Independent of magnetic coils or centrifuges.\n• Directly calibrated against active dosimeter telemetry (Gy).",
         AMBER_BG_LIGHT, AMBER_WARN)
    ]

    for i, (stress, target, pheno, strat, bg_c, bord_c) in enumerate(gate_data):
        row_idx = i + 1
        
        # Stressor
        c0 = table.cell(row_idx, 0)
        c0.text = stress
        c0.fill.solid()
        c0.fill.fore_color.rgb = bg_c
        p0 = c0.text_frame.paragraphs[0]
        p0.font.size = Pt(9.0)
        p0.font.bold = True
        p0.font.color.rgb = bord_c
        c0.vertical_anchor = MSO_ANCHOR.MIDDLE

        # Target
        c1 = table.cell(row_idx, 1)
        c1.text = target
        c1.fill.solid()
        c1.fill.fore_color.rgb = WHITE_CANVAS
        p1 = c1.text_frame.paragraphs[0]
        p1.font.size = Pt(8.5)
        p1.font.color.rgb = TEXT_DARK
        c1.vertical_anchor = MSO_ANCHOR.MIDDLE

        # Phenotype
        c2 = table.cell(row_idx, 2)
        c2.text = pheno
        c2.fill.solid()
        c2.fill.fore_color.rgb = WHITE_CANVAS
        p2 = c2.text_frame.paragraphs[0]
        p2.font.size = Pt(8.0)
        p2.font.color.rgb = TEXT_DARK
        c2.vertical_anchor = MSO_ANCHOR.MIDDLE

        # Strategy
        c3 = table.cell(row_idx, 3)
        c3.text = strat
        c3.fill.solid()
        c3.fill.fore_color.rgb = WHITE_CANVAS
        p3 = c3.text_frame.paragraphs[0]
        p3.font.size = Pt(8.2)
        p3.font.color.rgb = TEXT_DARK
        c3.vertical_anchor = MSO_ANCHOR.MIDDLE

    add_footer(slide, 12, 15)

    add_notes(slide,
        "TALKING POINTS (SLIDE 12 - PHENOTYPIC DISAMBIGUATION MATRIX):\n"
        "• This table represents our key translational science recommendation for Artemis payloads and lunar greenhouses.\n"
        "• When plants show stress on the lunar surface, how do we know if it was hypomagnetic stress, partial gravity (0.166 g), or radiation?\n"
        "• This matrix provides unambiguous diagnostic markers:\n"
        "  1. Hypomagnetic field delays emergence velocity (Δt50 = +12–36 h), represses chlorophyll/anthocyanin synthesis via cryptochromes, and triggers mitochondrial AOX1D without nuclear DNA damage. In ground controls, it is fully rescued by a 45 µT vector.\n"
        "  2. Lunar partial gravity causes directional skewing and cell wall changes, but germination rate and greening are normal. It is rescued by a 1g centrifuge, but unaffected by magnetic fields.\n"
        "  3. Radiation causes double-strand DNA breaks and γ-H2AX foci, which are independent of magnetic fields or gravity.\n"
        "• This framework replaces arbitrary mission abort criteria with a rigorous post-flight diagnostic methodology."
    )

def build_slide_13_graphical_abstract(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, WHITE_CANVAS)
    add_header(slide, "Graphical Abstract | LSSR Submission Summary",
               "The Complete Narrative in a Single Glance",
               "From lunar surface physics to 0–5 day developmental vulnerability and flight risk retirement")

    # 3 Large side-by-side cards: Panels 1, 2, 3
    x_coords = [Inches(0.8), Inches(4.75), Inches(8.7)]
    w_card   = Inches(3.8)
    h_card   = Inches(5.1)
    panels   = [
        ("GA_panel1_problem.png", "(1) The Lunar Reality (<0.8 nT Void)", BLUE_BG_LIGHT, BLUE_PRIMARY),
        ("GA_panel2_mechanism.png", "(2) The 0–5 Day Vulnerability Bottleneck", RED_BG_LIGHT, RED_ALERT),
        ("GA_panel3_solution.png", "(3) Flight Validation & Risk Retirement", GREEN_BG_LIGHT, GREEN_SUCC)
    ]

    for idx, (img_name, label, bg, edge) in enumerate(panels):
        xc = x_coords[idx]
        add_card(slide, xc, Inches(1.8), w_card, h_card, bg, edge, border_width=1.2)
        slide.shapes.add_picture(str(SUBPANELS_DIR / img_name), xc + Inches(0.15), Inches(2.2), w_card - Inches(0.3), h_card - Inches(0.55))
        tb = slide.shapes.add_textbox(xc + Inches(0.1), Inches(1.85), w_card - Inches(0.2), Inches(0.35))
        p = tb.text_frame.paragraphs[0]
        p.text = label
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = edge
        p.alignment = PP_ALIGN.CENTER

    add_footer(slide, 13, 15)

    add_notes(slide,
        "TALKING POINTS (SLIDE 13 - GRAPHICAL ABSTRACT):\n"
        "• If you have only two minutes to pitch this paper to an executive or conference audience, this slide tells the entire story.\n"
        "• Panel 1 (The Lunar Reality): As missions travel beyond low Earth orbit to the Moon, ambient magnetic fields collapse from Earth's 50 µT to less than 0.8 nT at Artemis South Pole sites. This variable is currently unmonitored in flight payloads.\n"
        "• Panel 2 (The 0–5 Day Vulnerability): Removal of the geomagnetic field causes delayed water uptake, a 12–36 hour emergence velocity lag, a 28% biomass yield loss, and cryptochrome-driven chlorosis.\n"
        "• Panel 3 (The Solution): We establish a standard flight risk-retirement protocol: in-situ 3-axis magnetometry, 3-chamber ground controls, active causal rescue coils, and predeclared Green/Amber/Red operational decision gates."
    )

def build_slide_14_discussion_roadmap(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, WHITE_CANVAS)
    add_header(slide, "Research Roadmap & Discussion",
               "Key Questions for the Working Group",
               "Strategic priorities for Artemis III LEAF operations and long-duration lunar bioregenerative life support")

    topics = [
        ("Question 1: Flight Payload Hardware Integration",
         "• How should Artemis LEAF and commercial lunar biological payloads integrate 3-axis fluxgate magnetometers without introducing thermal or EMI artifacts?\n"
         "• Where is the optimal mounting position relative to seedling cassettes and LEDs?\n"
         "• What telemetry sample rates (10 Hz vs. 1 Hz) are necessary to capture AC ripple?",
         BLUE_BG_LIGHT, BLUE_PRIMARY),
        ("Question 2: Crop Plasticity & Cultivar Selection",
         "• Which candidate space crops (Arabidopsis, microgreens, dwarf wheat, tomato) demonstrate natural genetic tolerance to near-null magnetic fields?\n"
         "• Can pre-flight seed conditioning (magnetic priming or epigenetic pre-exposure) mitigate the Day 0–5 germination and emergence lag?\n"
         "• How do mutant lines (e.g. cry1/cry2, hy5, aox1a/d) perform under simulated lunar fields?",
         AMBER_BG_LIGHT, AMBER_WARN),
        ("Question 3: Active Magnetic Sub-Assemblies for BLSS",
         "• Should future lunar surface greenhouses incorporate triaxial Helmholtz coils as standard operational infrastructure?\n"
         "• What are the mass, volume, and power trade-offs of delivering a continuous 45 µT vector over square meters of plant canopy?\n"
         "• Does vector re-application completely restore nutritional quality and secondary metabolite profiles?",
         GREEN_BG_LIGHT, GREEN_SUCC)
    ]

    for idx, (title, body, bg, edge) in enumerate(topics):
        top = Inches(1.8 + idx * 1.7)
        add_card(slide, Inches(0.8), top, Inches(11.733), Inches(1.5), bg, edge, border_width=1.2)
        tb = slide.shapes.add_textbox(Inches(1.0), top + Inches(0.1), Inches(11.333), Inches(1.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(11.5)
        p_t.font.bold = True
        p_t.font.color.rgb = edge

        p_b = tf.add_paragraph()
        p_b.text = body
        p_b.font.size = Pt(9.5)
        p_b.font.color.rgb = TEXT_DARK

    add_footer(slide, 14, 15)

    add_notes(slide,
        "TALKING POINTS (SLIDE 14 - DISCUSSION & ROADMAP):\n"
        "• Now I'd like to open up the floor to the group for discussion around these three strategic questions.\n"
        "• First: Hardware integration. In LEAF, space is tight. Can we place miniature commercial fluxgate sensors inside the cassette volume, or should they be mounted externally with a calibrated transfer function?\n"
        "• Second: Genetic tolerance and seed priming. Are there specific cultivars that don't suffer the 28% biomass deficit? Can we prime seeds on Earth with specific magnetic exposures prior to launch?\n"
        "• Third: Future lunar infrastructure. If long-term lunar greenhouses are built at Shackleton Crater, should active magnetic coils be part of the baseline environmental control system alongside lighting and HVAC?\n"
        "• Let's hear your thoughts."
    )

def build_slide_15_appendix_links(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, WHITE_CANVAS)
    add_header(slide, "Appendix & Open Science",
               "FAIR Data Repositories, NASA OSDR Accessions & Web Portal",
               "All manuscript drafts, figures, datasets, and analysis scripts are fully open and reproducible")

    cards = [
        ("Manuscript & Documents",
         "• Master Markdown: manuscript/Hypomagnetic_Lunar_Plant_Biology_LSSR_Review.md\n"
         "• Compiled Word Doc: Near_Null_Magnetic_Fields_Lunar_Plant_Biology_LSSR_Review.docx (2.96 MB)\n"
         "• BibTeX Library: references_LSSR.bib (79 audited references; CrossRef-verified)\n"
         "• Target Journal: Life Sciences in Space Research (COSPAR / Elsevier)",
         BLUE_BG_LIGHT, BLUE_PRIMARY),
        ("Processed Empirical Data Tables",
         "• data/landing_sites_magnetic.csv (Field magnitudes across 23 exploration sites)\n"
         "• data/lunar_mag_field_grid.csv (1° resolution Lunar Prospector / Kaguya total field)\n"
         "• data/seedling_kinetics_summary.csv (Empirical Day 0–5 germination kinetics)\n"
         "• data/multiomics_overlap_osd782_nnmf.csv (OSDR-782 vs. NNMF gene concordance)",
         CARD_BG_LIGHT, CARD_BORDER),
        ("NASA Open Science Data Accessions",
         "• OSD-782: Arabidopsis thaliana response to 1 Gy ionizing radiation (rad-bio-app)\n"
         "• OSD-8: Spaceflight transcriptional response in Arabidopsis seedlings\n"
         "• OSD-27: Light quality and microgravity interactions in space crops\n"
         "• Rad-Bio-App: https://osdr.nasa.gov/bio/repo/data/studies/OSD-782",
         CARD_BG_LIGHT, CARD_BORDER),
        ("Interactive Web Portal & Zenodo Release",
         "• Live CoSE Showcase: https://dr-richard-barker.github.io/NMF_review/\n"
         "• GitHub Repository: https://github.com/dr-richard-barker/NMF_review\n"
         "• Zenodo Package: .zenodo.json, CITATION.cff, MANIFEST.tsv, CHECKSUMS.sha256\n"
         "• ABAI Quality Control: 5/5 checks passed; official HEAD attestation active",
         GREEN_BG_LIGHT, GREEN_SUCC)
    ]

    for idx, (title, body, bg, edge) in enumerate(cards):
        col_idx = idx % 2
        row_idx = idx // 2
        left = Inches(0.8 + col_idx * 6.0)
        top = Inches(1.8 + row_idx * 2.55)
        add_card(slide, left, top, Inches(5.733), Inches(2.35), bg, edge, border_width=1.0)
        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), Inches(5.333), Inches(2.05))
        tf = tb.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(11.0)
        p_t.font.bold = True
        p_t.font.color.rgb = edge

        p_b = tf.add_paragraph()
        p_b.text = body
        p_b.font.size = Pt(8.8)
        p_b.font.color.rgb = TEXT_DARK

    add_footer(slide, 15, 15)

    add_notes(slide,
        "TALKING POINTS (SLIDE 15 - APPENDIX & OPEN SCIENCE):\n"
        "• Finally, this slide documents all open science assets and repository deliverables.\n"
        "• Everything we've shown today is fully open, reproducible, and tracked in Git.\n"
        "• The compiled Word document is ready for co-authors to edit.\n"
        "• The CoSE web portal is live at dr-richard-barker.github.io/NMF_review.\n"
        "• All datasets trace directly to NASA OSDR accessions and Lunar Prospector/Kaguya orbital magnetometer archives.\n"
        "• Thank you to all co-authors across Purdue, NASA KSC, CU Boulder, and Space Lab Technologies. Looking forward to your feedback!"
    )

def main():
    print(f"Building PowerPoint presentation: {OUT_PPTX}")
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    build_slide_01_title(prs)
    build_slide_02_narrative_overview(prs)
    build_slide_03_figure1_montage(prs)
    build_slide_04_figure1_deepdive(prs)
    build_slide_05_figure2_montage(prs)
    build_slide_06_figure2_deepdive(prs)
    build_slide_07_figure3_montage(prs)
    build_slide_08_figure3_deepdive(prs)
    build_slide_09_figure4_montage(prs)
    build_slide_10_figure4_deepdive(prs)
    build_slide_11_figure5_montage(prs)
    build_slide_12_figure5_deepdive_table(prs)
    build_slide_13_graphical_abstract(prs)
    build_slide_14_discussion_roadmap(prs)
    build_slide_15_appendix_links(prs)

    prs.save(OUT_PPTX)
    size_mb = OUT_PPTX.stat().st_size / (1024 * 1024)
    print(f"Successfully generated: {OUT_PPTX.name} ({size_mb:.2f} MB, {len(prs.slides)} slides)")

if __name__ == '__main__':
    main()
