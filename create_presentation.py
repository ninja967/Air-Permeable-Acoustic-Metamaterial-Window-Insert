import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

BG_COLOR = RGBColor(248, 250, 252)
PRIMARY_COLOR = RGBColor(15, 23, 42)
SECONDARY_COLOR = RGBColor(30, 41, 59)
ACCENT_BLUE = RGBColor(2, 132, 199)
ACCENT_TEAL = RGBColor(13, 148, 136)
CARD_BG = RGBColor(255, 255, 255)
CARD_BORDER = RGBColor(226, 232, 240)
TEXT_MAIN = RGBColor(30, 41, 59)
TEXT_MUTED = RGBColor(100, 116, 139)

FOLDER = r"c:\Users\sarat\Downloads\New folder"

def add_header(slide, title_text, category_text="AIR-PERMEABLE ACOUSTIC METAMATERIAL WINDOW INSERT"):
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    p_c = tf_c.paragraphs[0]
    p_c.text = category_text.upper()
    p_c.font.size = Pt(11)
    p_c.font.bold = True
    p_c.font.color.rgb = ACCENT_BLUE

    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.8))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.size = Pt(26)
    p_t.font.bold = True
    p_t.font.color.rgb = PRIMARY_COLOR

    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = CARD_BORDER
    line.line.color.rgb = CARD_BORDER

def create_card(slide, left, top, width, height, bg=CARD_BG, border=CARD_BORDER):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg
    shape.line.color.rgb = border
    shape.line.width = Pt(1.2)
    return shape

# ==========================================================
# SLIDE 1: TITLE SLIDE
# ==========================================================
s1 = prs.slides.add_slide(prs.slide_layouts[6])
card1 = create_card(s1, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9), bg=CARD_BG, border=ACCENT_BLUE)

tag_box = s1.shapes.add_textbox(Inches(1.4), Inches(1.2), Inches(10.5), Inches(0.4))
tf_tag = tag_box.text_frame
p_tag = tf_tag.paragraphs[0]
p_tag.text = "COMPUTER-AIDED PRODUCT DEVELOPMENT (CAPD) • COURSE PROJECT"
p_tag.font.size = Pt(12)
p_tag.font.bold = True
p_tag.font.color.rgb = ACCENT_BLUE

title_box1 = s1.shapes.add_textbox(Inches(1.4), Inches(1.6), Inches(10.5), Inches(1.6))
tf_t1 = title_box1.text_frame
tf_t1.word_wrap = True
p1 = tf_t1.paragraphs[0]
p1.text = "Air-Permeable Acoustic Metamaterial\nWindow Insert"
p1.font.size = Pt(36)
p1.font.bold = True
p1.font.color.rgb = PRIMARY_COLOR

sub_box1 = s1.shapes.add_textbox(Inches(1.4), Inches(3.3), Inches(10.5), Inches(0.8))
tf_s1 = sub_box1.text_frame
tf_s1.word_wrap = True
p_sub = tf_s1.paragraphs[0]
p_sub.text = "Continuous Natural Ventilation Coupled with Broadband Destructive Interference Sound Cancellation"
p_sub.font.size = Pt(16)
p_sub.font.color.rgb = ACCENT_TEAL

pres_card = create_card(s1, Inches(1.4), Inches(4.3), Inches(5.2), Inches(1.8), bg=RGBColor(241, 245, 249), border=CARD_BORDER)
pres_box = s1.shapes.add_textbox(Inches(1.6), Inches(4.45), Inches(4.8), Inches(1.5))
tf_p = pres_box.text_frame
p_p1 = tf_p.paragraphs[0]
p_p1.text = "TEAM MEMBERS / PRESENTERS:"
p_p1.font.size = Pt(11)
p_p1.font.bold = True
p_p1.font.color.rgb = TEXT_MUTED

p_p2 = tf_p.add_paragraph()
p_p2.text = "• N. SARATH PAVAN KUMAR  (24BSM040)"
p_p2.font.size = Pt(13)
p_p2.font.bold = True
p_p2.font.color.rgb = PRIMARY_COLOR

p_p3 = tf_p.add_paragraph()
p_p3.text = "• PALTHI ANJI  (24BSM041)"
p_p3.font.size = Pt(13)
p_p3.font.bold = True
p_p3.font.color.rgb = PRIMARY_COLOR

inst_card = create_card(s1, Inches(6.9), Inches(4.3), Inches(5.0), Inches(1.8), bg=RGBColor(241, 245, 249), border=CARD_BORDER)
inst_box = s1.shapes.add_textbox(Inches(7.1), Inches(4.45), Inches(4.6), Inches(1.5))
tf_i = inst_box.text_frame
p_i1 = tf_i.paragraphs[0]
p_i1.text = "COURSE INSTRUCTOR:"
p_i1.font.size = Pt(11)
p_i1.font.bold = True
p_i1.font.color.rgb = TEXT_MUTED

p_i2 = tf_i.add_paragraph()
p_i2.text = "DR. AVINASH RAVI RAJA"
p_i2.font.size = Pt(14)
p_i2.font.bold = True
p_i2.font.color.rgb = PRIMARY_COLOR

p_i3 = tf_i.add_paragraph()
p_i3.text = "Department of Mechanical Engineering"
p_i3.font.size = Pt(12)
p_i3.font.color.rgb = TEXT_MUTED

# ==========================================================
# SLIDE 2: THE URBAN DILEMMA
# ==========================================================
s2 = prs.slides.add_slide(prs.slide_layouts[6])
add_header(s2, "The Urban Dilemma: Traffic Noise vs. Fresh Air")

create_card(s2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
tb1 = s2.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.0), Inches(4.6))
tf1 = tb1.text_frame
tf1.word_wrap = True
p = tf1.paragraphs[0]
p.text = "The Strict Urban Living Trade-Off"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = PRIMARY_COLOR

bullets_problem = [
    "Open Window Dilemma: Brings cool breeze and fresh air, but exposes occupants to unbearable 75–85 dB city traffic noise.",
    "Sealed Window Trap: Blocks exterior noise, but traps CO2, humidity, and stale indoor pollutants, forcing 100% reliance on energy-heavy AC.",
    "Acoustic Mass Law Limitation: Conventional soundproofing relies strictly on airtight, heavy mass (double-pane glass, dense foam), which inherently stops airflow."
]
for b in bullets_problem:
    p = tf1.add_paragraph()
    p.text = "• " + b
    p.font.size = Pt(14)
    p.font.color.rgb = TEXT_MAIN
    p.space_before = Pt(14)

create_card(s2, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.0), bg=RGBColor(240, 249, 255), border=ACCENT_BLUE)
tb2 = s2.shapes.add_textbox(Inches(7.2), Inches(2.0), Inches(5.0), Inches(4.6))
tf2 = tb2.text_frame
tf2.word_wrap = True
p = tf2.paragraphs[0]
p.text = "The Metamaterial Breakthrough"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = ACCENT_BLUE

bullets_sol = [
    "Silence Without Sealing: Proves that quiet interiors and continuous natural ventilation are no longer mutually exclusive.",
    "Compact Sub-Wavelength Control: Uses internal geometry much smaller than sound wavelengths to manipulate sound without bulky foam.",
    "33.3% Open Airway Core: Maintains an open, breathable central corridor allowing steady airflow with zero power consumption.",
    "Retrofit Cassette: Installs directly into existing window sliding tracks as a modular, plug-and-play architectural insert."
]
for b in bullets_sol:
    p = tf2.add_paragraph()
    p.text = "✔ " + b
    p.font.size = Pt(14)
    p.font.color.rgb = PRIMARY_COLOR
    p.space_before = Pt(12)

# ==========================================================
# SLIDE 3: WORKING PRINCIPLE
# ==========================================================
s3 = prs.slides.add_slide(prs.slide_layouts[6])
add_header(s3, "How the Product Works: Geometry as the Machine")

create_card(s3, Inches(0.8), Inches(1.8), Inches(5.2), Inches(5.0))
tb3 = s3.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(4.8), Inches(4.6))
tf3 = tb3.text_frame
tf3.word_wrap = True
p = tf3.paragraphs[0]
p.text = "Purely Passive Operational Logic"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = PRIMARY_COLOR

bullets_work = [
    "No Active Electronics: Functions completely without microphones, speakers, motors, sensors, or electrical power.",
    "Acoustic Wave Splitting: Incoming sound waves are divided into a straight central path and two folded perimeter labyrinth side branches.",
    "Decoupled Airflow: While sound waves bounce into the side chambers, continuous air breeze glides straight through the central corridor.",
    "Self-Canceling Exit: When the delayed sound waves rejoin the central stream, they eliminate each other automatically."
]
for b in bullets_work:
    p = tf3.add_paragraph()
    p.text = "• " + b
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MAIN
    p.space_before = Pt(12)

concept_img = os.path.join(FOLDER, "concept_how_it_works.png")
if os.path.exists(concept_img):
    create_card(s3, Inches(6.3), Inches(1.8), Inches(6.2), Inches(5.0))
    s3.shapes.add_picture(concept_img, Inches(6.45), Inches(2.0), Inches(5.9), Inches(4.6))

# ==========================================================
# SLIDE 4: THE SCIENCE: DESTRUCTIVE INTERFERENCE
# ==========================================================
s4 = prs.slides.add_slide(prs.slide_layouts[6])
add_header(s4, "The Science Behind It: Destructive Wave Interference")

cards_data = [
    ("1. Sound as a Traveling Wave", 
     ["Sound energy travels through air as oscillating compression waves (crests and troughs).",
      "Human ears detect sound when these oscillating pressure peaks strike the eardrum.",
      "If pressure peaks are canceled by matching troughs, the net acoustic pressure becomes zero (silence)."],
     Inches(0.8)),
    ("2. Path Difference & Half-Wavelength Delay", 
     ["The central ventilation duct offers a short, direct path for sound and air.",
      "The side labyrinth channels force sound to take an extended, multi-pass detour.",
      "The folded path is engineered to delay sound by exactly one half-wavelength for target urban traffic rumble."],
     Inches(4.8)),
    ("3. Crest-Meets-Trough Cancellation", 
     ["At the exit, the delayed sound wave collides with the direct wave in the airway.",
      "Because of the half-wavelength delay, wave crests perfectly align with wave troughs.",
      "The sound waves cancel destructively, while the physical air stream passes unaffected."],
     Inches(8.8))
]

for title, points, left_pos in cards_data:
    create_card(s4, left_pos, Inches(1.8), Inches(3.733), Inches(5.0))
    tb = s4.shapes.add_textbox(left_pos + Inches(0.2), Inches(2.0), Inches(3.333), Inches(4.6))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE
    for pt in points:
        p = tf.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(12)

# ==========================================================
# SLIDE 5: COMPONENT 1: CENTRAL VENTILATION CORE
# ==========================================================
s5 = prs.slides.add_slide(prs.slide_layouts[6])
add_header(s5, "Component 1: Central Ventilation Airway Duct")

create_card(s5, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
tb5 = s5.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.0), Inches(4.4))
tf5 = tb5.text_frame
tf5.word_wrap = True
p = tf5.paragraphs[0]
p.text = "Direct Airflow Transmission Corridor"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = PRIMARY_COLOR

bullets_core = [
    "Unobstructed 20.00 mm Central Duct: Provides an open cross-sectional airflow corridor straight through the center of the unit cell.",
    "33.3% Open Ventilation Area: Ensures natural indoor room breathing, heat removal, and passive cross-ventilation without draft constriction.",
    "Zero Bulk Airflow Resistance: Because natural breeze moves as bulk fluid drift, it glides straight through without entering the labyrinth traps.",
    "Acoustic Mixing Zone: Serves as the recombining chamber where direct sound waves collide with out-of-phase labyrinth waves."
]
for b in bullets_core:
    p = tf5.add_paragraph()
    p.text = "• " + b
    p.font.size = Pt(13.5)
    p.font.color.rgb = TEXT_MAIN
    p.space_before = Pt(12)

img_front = os.path.join(FOLDER, "render_unit_cell_front.png")
if os.path.exists(img_front):
    create_card(s5, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    s5.shapes.add_picture(img_front, Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))

# ==========================================================
# SLIDE 6: COMPONENT 2: SPACE-COILING LABYRINTH BAFFLES
# ==========================================================
s6 = prs.slides.add_slide(prs.slide_layouts[6])
add_header(s6, "Component 2: Space-Coiling Labyrinth Baffles")

create_card(s6, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
tb6 = s6.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.0), Inches(4.4))
tf6 = tb6.text_frame
tf6.word_wrap = True
p = tf6.paragraphs[0]
p.text = "Internal Acoustic Folding Partitions"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = PRIMARY_COLOR

bullets_baffle = [
    "3 Staggered Partitions Per Chamber: Thin 1.50 mm rigid baffles divide each 20 mm wide side chamber into 4 serpentine vertical passes.",
    "Path Extension in Compact Depth: Compresses an extended ~107 mm acoustic journey into an ultra-thin 30 mm window cassette profile.",
    "Alternating Baffle Topology: Alternating floor and ceiling attachments eliminate short-circuiting and guarantee full 4-pass sound travel.",
    "Open 3D Visualization: Rendered with an open cutaway top so internal serpentine baffle channels are clearly visible in isometric view."
]
for b in bullets_baffle:
    p = tf6.add_paragraph()
    p.text = "• " + b
    p.font.size = Pt(13.5)
    p.font.color.rgb = TEXT_MAIN
    p.space_before = Pt(12)

img_iso = os.path.join(FOLDER, "render_unit_cell_iso.png")
if os.path.exists(img_iso):
    create_card(s6, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    s6.shapes.add_picture(img_iso, Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))

# ==========================================================
# SLIDE 7: COMPONENT 3: ACOUSTIC ENTRY SLITS & RESONATOR
# ==========================================================
s7 = prs.slides.add_slide(prs.slide_layouts[6])
add_header(s7, "Component 3: Acoustic Entry Slits & Resonator Chamber")

create_card(s7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
tb7 = s7.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.0), Inches(4.4))
tf7 = tb7.text_frame
tf7.word_wrap = True
p = tf7.paragraphs[0]
p.text = "Coupling Portals & Dead-End Reflection"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = PRIMARY_COLOR

bullets_slit = [
    "Calibrated 2.00 mm Entrance Portals: Located near the bottom on the 1.50 mm inner airway wall to cleanly capture incoming sound oscillations.",
    "Selective Acoustic Coupling: Diverts fluctuating acoustic pressure waves into the side labyrinths while allowing smooth bulk airflow to bypass.",
    "Dual Symmetric Chambers: Both left and right chambers operate in parallel, canceling sound from both sides of the central ventilation stream.",
    "Dead-End Reflection Boundary: The 4th channel terminates against a solid end-wall, reflecting the inverted acoustic wave back into the airway."
]
for b in bullets_slit:
    p = tf7.add_paragraph()
    p.text = "• " + b
    p.font.size = Pt(13.5)
    p.font.color.rgb = TEXT_MAIN
    p.space_before = Pt(12)

img_air_front = os.path.join(FOLDER, "render_air_domain_front.png")
if os.path.exists(img_air_front):
    create_card(s7, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    s6.shapes.add_picture(img_air_front, Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))

# ==========================================================
# SLIDE 8: COMPONENT 4: UNIT CELL STRUCTURAL FRAME
# ==========================================================
s8 = prs.slides.add_slide(prs.slide_layouts[6])
add_header(s8, "Component 4: Unit Cell 60x30x30 mm Blueprint Frame")

create_card(s8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
tb8 = s8.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.0), Inches(4.4))
tf8 = tb8.text_frame
tf8.word_wrap = True
p = tf8.paragraphs[0]
p.text = "Exact Dimensional Stack-Up"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = PRIMARY_COLOR

bullets_cap = [
    "60.00 mm Width x 30.00 mm Height: Perfectly proportioned 2:1 aspect ratio centered on the coordinate Origin (0,0).",
    "1.50 mm Uniform Wall Standard: Outer frame walls, central airway walls, and internal baffles share identical 1.50 mm wall thickness.",
    "1.50 mm Rigid Base Floor: Closes the back of both side resonators while maintaining a clean, open central ventilation passage.",
    "Additive Manufacturing DFAM: Self-supporting vertical walls designed for direct 3D printing in ABS or PETG polymer without infill voids."
]
for b in bullets_cap:
    p = tf8.add_paragraph()
    p.text = "• " + b
    p.font.size = Pt(13.5)
    p.font.color.rgb = TEXT_MAIN
    p.space_before = Pt(12)

if os.path.exists(img_front):
    create_card(s8, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    s8.shapes.add_picture(img_front, Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))

# ==========================================================
# SLIDE 9: COMPONENT 5: 3x3 MODULAR WINDOW PANEL MATRIX
# ==========================================================
s9 = prs.slides.add_slide(prs.slide_layouts[6])
add_header(s9, "Component 5: 3x3 Modular Window Panel Matrix")

create_card(s9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
tb9 = s9.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.0), Inches(4.4))
tf9 = tb9.text_frame
tf9.word_wrap = True
p = tf9.paragraphs[0]
p.text = "Full Window-Scale Cassette Assembly"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = PRIMARY_COLOR

bullets_panel = [
    "180 x 180 x 30 mm Assembly: Patterns 9 identical unit cells into a single monolithic cassette ready for architectural installation.",
    "3 Continuous Ventilation Corridors: Triples the total airflow throughput across the window opening for rapid indoor air refreshment.",
    "18 Coiled Resonator Chambers: Multiplies acoustic cancellation zones across the full surface to trap noise arriving at oblique angles.",
    "Monolithic Printability: Fused into a single manifold solid body without loose mechanical fasteners or assembly vibration rattles."
]
for b in bullets_panel:
    p = tf9.add_paragraph()
    p.text = "• " + b
    p.font.size = Pt(13.5)
    p.font.color.rgb = TEXT_MAIN
    p.space_before = Pt(12)

img_p3x3 = os.path.join(FOLDER, "render_panel_3x3_iso.png")
if os.path.exists(img_p3x3):
    create_card(s9, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    s9.shapes.add_picture(img_p3x3, Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))

# ==========================================================
# SLIDE 10: COMPONENT 6: WINDOW-TRACK MOUNTING FLANGE
# ==========================================================
s10 = prs.slides.add_slide(prs.slide_layouts[6])
add_header(s10, "Component 6: Window-Track Flange & Gasket Interface")

create_card(s10, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
tb10 = s10.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.0), Inches(4.4))
tf10 = tb10.text_frame
tf10.word_wrap = True
p = tf10.paragraphs[0]
p.text = "Toolless Architectural Retrofit Interface"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = PRIMARY_COLOR

bullets_flange = [
    "5.0 mm Perimeter Mounting Lip: Extends continuously around the panel mid-plane to slot directly into standard sliding window frames.",
    "1.5 mm Lead-in Chamfers: Beveled insertion edges guide the cassette smoothly into standard rubber window gaskets without pinching or tearing.",
    "Acoustic Perimeter Seal: Compresses against window frame weatherstripping to eliminate flanking sound leakage around the panel edges.",
    "Modular Scalability: Multiple 180x180 mm panels can be snap-interlocked horizontally and vertically to fill any window opening size."
]
for b in bullets_flange:
    p = tf10.add_paragraph()
    p.text = "• " + b
    p.font.size = Pt(13.5)
    p.font.color.rgb = TEXT_MAIN
    p.space_before = Pt(12)

img_p3x3_front = os.path.join(FOLDER, "render_panel_3x3_front.png")
if os.path.exists(img_p3x3_front):
    create_card(s10, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    s10.shapes.add_picture(img_p3x3_front, Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))

# ==========================================================
# SLIDE 11: INVERSE AIR DOMAIN: VISUALIZING THE SOUND PATH
# ==========================================================
s11 = prs.slides.add_slide(prs.slide_layouts[6])
add_header(s11, "Acoustic Air Domain: Visualizing Sound & Air Paths")

create_card(s11, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
tb11 = s11.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.0), Inches(4.4))
tf11 = tb11.text_frame
tf11.word_wrap = True
p = tf11.paragraphs[0]
p.text = "The Physical Geometry of the Air Space"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = PRIMARY_COLOR

bullets_air = [
    "Inverse Geometry Extraction: Represents the exact positive shape of the fluid and sound traveling inside the metamaterial cassette.",
    "Visual Proof of Coexistence: Clearly reveals the continuous central ventilation core flanked by the dual folded serpentine labyrinth loops.",
    "Watertight Manifold Fluid Body: Generated through precision Boolean subtraction to model the complete acoustic wave propagation volume.",
    "100 mm Waveguide Ports: Modeled with standardized upstream and downstream ducts to verify acoustic port coupling."
]
for b in bullets_air:
    p = tf11.add_paragraph()
    p.text = "• " + b
    p.font.size = Pt(13.5)
    p.font.color.rgb = TEXT_MAIN
    p.space_before = Pt(12)

img_air_iso = os.path.join(FOLDER, "render_air_domain_iso.png")
if os.path.exists(img_air_iso):
    create_card(s11, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    s11.shapes.add_picture(img_air_iso, Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))

# ==========================================================
# SLIDE 12: SUMMARY & ENGINEERING TAKEAWAYS
# ==========================================================
s12 = prs.slides.add_slide(prs.slide_layouts[6])
add_header(s12, "Summary & Key Engineering Takeaways")

summaries = [
    ("Urban Dilemma Solved", 
     "Successfully broke the historical trade-off between natural breeze and acoustic silence in urban architecture.",
     Inches(0.8), Inches(1.8)),
    ("Geometry as the Machine", 
     "Replaced heavy double-glazing and active electronic speakers with a purely passive, 3D-printable polymer metamaterial.",
     Inches(6.8), Inches(1.8)),
    ("Destructive Phase Cancellation", 
     "Path difference delays sound waves by 180°, canceling noise crest-to-trough while maintaining a 33.3% open ventilation core.",
     Inches(0.8), Inches(4.4)),
    ("Modular Architectural Retrofit", 
     "Engineered 180x180 mm 3x3 cassette with integrated mounting flange and chamfers for instant, toolless window installation.",
     Inches(6.8), Inches(4.4))
]

for title, desc, l, t in summaries:
    create_card(s12, l, t, Inches(5.7), Inches(2.4), bg=CARD_BG, border=ACCENT_BLUE)
    tb = s12.shapes.add_textbox(l + Inches(0.3), t + Inches(0.25), Inches(5.1), Inches(1.9))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.size = Pt(14)
    p2.font.color.rgb = TEXT_MAIN
    p2.space_before = Pt(10)

out_pptx = os.path.join(FOLDER, "Acoustic_Metamaterial_Presentation.pptx")
prs.save(out_pptx)
print(f"Presentation successfully updated and saved to: {out_pptx}")
