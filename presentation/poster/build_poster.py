"""Build the A0 poster (designed on the BAM A3 template, printed scaled to A0).

    python presentation/poster/build_poster.py
-> presentation/poster/FB72_Poster_openBIS_AI_Agents.pptx

Template: input/Poster_Vorlage_EN_BAM.pptx (BAM KM). All geometry in cm on the A3 canvas
(29.7 x 42 cm); A0 print = x 2.83, so 14 pt body text becomes ~40 pt, 11 pt captions ~31 pt.
Grid from the template: left margin 2.0 cm, content width 25.7 cm, two columns of 12.7 cm (gap 0.3 cm).
Free content area between the author line (~6.5 cm) and the footer claim (~37.9 cm).
"""

from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Cm, Pt

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "input" / "Poster_Vorlage_EN_BAM.pptx"
OUT = HERE / "FB72_Poster_openBIS_AI_Agents.pptx"
A = HERE / "assets"

# BAM theme colours (from the template theme)
NAVY = RGBColor(0x00, 0x28, 0x32)      # dk2
RED = RGBColor(0xD2, 0x00, 0x1E)       # accent1
CYAN = RGBColor(0x00, 0xAF, 0xF0)      # accent3
PETROL = RGBColor(0x00, 0x55, 0x6E)    # accent4
GREY = RGBColor(0xBE, 0xC3, 0xC8)      # accent5
LIGHT = RGBColor(0xEB, 0xED, 0xEF)     # light tint of accent5
INK = RGBColor(0x0A, 0x19, 0x2F)       # body text colour used in the template
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
MED, LIGHTF = "BAM Klavika Medium", "BAM Klavika Light"

L, W = 2.0, 25.7              # content left / width
C1, C2, CW = 2.0, 15.0, 12.7  # columns

TITLE = "AI agents turn our fatigue tests into a lean openBIS data structure"
AUTHORS = "[Authors]  ·  BAM, 7.2 Buildings and Structures"


# ---------------------------------------------------------------- helpers
def text(slide, x, y, w, h, runs, size=14, font=LIGHTF, color=INK, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, fill=None, margin=0.15, line=None, name=None, space_after=0):
    """runs: str | list of paragraphs; paragraph = str | list of (text, {opts})."""
    shp = slide.shapes.add_textbox(Cm(x), Cm(y), Cm(w), Cm(h))
    if name:
        shp.name = name
    if fill is not None:
        shp.fill.solid(); shp.fill.fore_color.rgb = fill
    tf = shp.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    for side in ("left", "right", "top", "bottom"):
        setattr(tf, f"margin_{side}", Cm(margin))
    paras = runs if isinstance(runs, list) else [runs]
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if line:
            p.line_spacing = Pt(line)
        if space_after:
            p.space_after = Pt(space_after)
        parts = para if isinstance(para, list) else [(para, {})]
        for t, o in parts:
            r = p.add_run(); r.text = t
            r.font.size = Pt(o.get("size", size)); r.font.name = o.get("font", font)
            r.font.color.rgb = o.get("color", color); r.font.bold = False
    return shp


def box(slide, x, y, w, h, fill, shape=MSO_SHAPE.RECTANGLE, name=None):
    shp = slide.shapes.add_shape(shape, Cm(x), Cm(y), Cm(w), Cm(h))
    if name:
        shp.name = name
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    shp.line.fill.background()
    shp.shadow.inherit = False
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        shp.adjustments[0] = 0.12
    return shp


def arrow(slide, x1, y1, x2, y2, color=NAVY, w=2.25):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Cm(x1), Cm(y1), Cm(x2), Cm(y2))
    c.line.color.rgb = color; c.line.width = Pt(w)
    ln = c.line._get_or_add_ln()
    ln.append(ln.makeelement("{http://schemas.openxmlformats.org/drawingml/2006/main}tailEnd",
                             {"type": "triangle", "w": "med", "len": "med"}))
    return c


def heading(slide, x, y, w, num, label, fill=CYAN):
    """Template 'Ueberschriften-Leiste': filled bar, white Klavika Medium 17 pt."""
    return text(slide, x, y, w, 1.1, [[(f"{num}   {label}", {"font": MED})]], size=17,
                color=WHITE, fill=fill, anchor=MSO_ANCHOR.MIDDLE, margin=0.35, name=f"Heading {num}")


def picture(slide, path, x, y, w, h, name=None):
    """Picture fitted into w x h (keeps aspect ratio, centred) with a thin grey frame."""
    im = Image.open(path); ar = im.width / im.height
    pw, ph = (h * ar, h) if w / h > ar else (w, w / ar)
    pic = slide.shapes.add_picture(str(path), Cm(x + (w - pw) / 2), Cm(y + (h - ph) / 2), Cm(pw), Cm(ph))
    pic.line.color.rgb = GREY; pic.line.width = Pt(0.75)
    if name:
        pic.name = name
    return pic


def picture_fill(slide, path, x, y, w, h, focus=(0.5, 0.5), name=None):
    """Picture cropped to exactly fill the w x h cell (like CSS object-fit: cover)."""
    im = Image.open(path); ar_img, ar_box = im.width / im.height, w / h
    pic = slide.shapes.add_picture(str(path), Cm(x), Cm(y), Cm(w), Cm(h))
    if ar_img > ar_box:      # too wide -> crop left/right
        cut = 1 - ar_box / ar_img
        pic.crop_left = cut * focus[0]; pic.crop_right = cut - pic.crop_left
    else:                    # too tall -> crop top/bottom
        cut = 1 - ar_img / ar_box
        pic.crop_top = cut * focus[1]; pic.crop_bottom = cut - pic.crop_top
    pic.line.color.rgb = GREY; pic.line.width = Pt(0.75)
    if name:
        pic.name = name
    return pic


def use_focus_area(prs, slide, master_index):
    """Point the slide at the layout of another master (= BAM topic-field icon in the footer)."""
    layout = prs.slide_masters[master_index].slide_layouts[0]
    for rel in slide.part.rels.values():
        if rel.reltype.endswith("/slideLayout"):
            rel._target = layout.part


def checkpoint(slide, x, y, w, title, source, cols, rows, footer):
    """Excerpt of a review document as a compact table on a light panel (height 3.2 cm)."""
    box(slide, x, y, w, 3.2, LIGHT, name=title)
    text(slide, x + 0.2, y + 0.1, w - 0.4, 0.65, [[("✔ " + title, {"font": MED, "color": RED, "size": 13}),
                                                  ("   " + source, {"color": PETROL})]], size=11, margin=0.02)
    for r, row in enumerate(rows):
        cx = x + 0.2
        for c, (cell, cw) in enumerate(zip(row, cols)):
            text(slide, cx, y + 0.8 + r * 0.55, cw - 0.1, 0.55, cell, size=11,
                 font=MED if c == 0 else LIGHTF, color=NAVY if c == 0 else INK, margin=0.02)
            cx += cw
    text(slide, x + 0.2, y + 2.5, w - 0.4, 0.6, footer, size=11, color=PETROL, margin=0.02)


# ---------------------------------------------------------------- build
def build():
    prs = Presentation(str(TEMPLATE))
    sldIdLst = prs.slides._sldIdLst
    for sldId in list(sldIdLst)[:-1]:           # keep only the empty poster page (slide 6)
        prs.part.drop_rel(sldId.rId); sldIdLst.remove(sldId)
    s = prs.slides[0]
    use_focus_area(prs, s, 1)                    # master 1 = FOCUS AREA INFRASTRUCTURE
    # unused framed picture/text placeholders of that layout would print as empty frames -> remove them
    lay = prs.slide_masters[1].slide_layouts[0]
    for ph in list(lay.placeholders):
        if ph.placeholder_format.idx not in (0, 13):
            ph._element.getparent().remove(ph._element)
    for ph in list(s.placeholders):
        if ph.name == "Titel 2":
            ph.text_frame.text = TITLE
        elif ph.name == "Textplatzhalter 1":
            ph.text_frame.text = AUTHORS
        else:
            ph._element.getparent().remove(ph._element)

    # ---------------- idea box
    text(s, L, 7.3, W, 2.0, [
        [("Idea   ", {"font": MED}),
         ("Describe the experiment once, in domain language. AI agents check it against the BAM data standard "
          "and the live BAM Data Store, design a flat structure and create only what is really missing. "
          "Humans approve every decision.", {})]],
        size=14, line=17, color=WHITE, fill=PETROL, margin=0.4, anchor=MSO_ANCHOR.MIDDLE, name="Idea box")

    # ================= row 1 left: 1 the tests (graphic 1: photo strip + phases)
    y0 = 9.75
    heading(s, C1, y0, CW, "1", "The tests: S-N curves of welded joints", fill=CYAN)
    text(s, C1, y0 + 1.3, CW, 1.35,
         "Butt and cruciform joints, randomised load levels – scatter starts before the test, so every specimen must be traceable.", size=14, line=17, margin=0.05)
    py = y0 + 2.75; cell = (CW - 3 * 0.2) / 4; ph = 3.15
    shots = [("s02_01.png", (0.55, 0.5), "3D scan"), ("s05_07.png", (0.5, 0.4), "test rig"),
             ("s06_09.png", (0.45, 0.62), "crack monitoring"), ("s07_11.jpg", (0.6, 0.5), "fracture surface")]
    for i, (f, foc, lab) in enumerate(shots):
        x = C1 + i * (cell + 0.2)
        picture_fill(s, A / f, x, py, cell, ph, focus=foc, name=f"Photo {lab}")
        text(s, x, py + ph + 0.05, cell, 0.55, lab, size=11, color=PETROL, align=PP_ALIGN.CENTER, margin=0.02)
    phases = [("01–02", "Preparation", "quality check,", "grinding"),
              ("03–06", "Characterisation", "3D scan, weld", "rating, geometry"),
              ("07–11", "Test rig", "gauges, cyclic", "test, evaluation"),
              ("12", "Post-test", "fracture", "surface")]
    fy = py + ph + 0.75; pw = (CW - 3 * 0.25) / 4
    for i, (n, t, d1, d2) in enumerate(phases):
        x = C1 + i * (pw + 0.25)
        box(s, x, fy, pw, 2.85, LIGHT, name=f"Phase {n}")
        text(s, x, fy + 0.05, pw, 0.95, n, size=22, font=MED, color=CYAN, align=PP_ALIGN.CENTER, margin=0.02)
        text(s, x, fy + 0.95, pw, 0.65, t, size=12, font=MED, color=NAVY, align=PP_ALIGN.CENTER, margin=0.02)
        text(s, x, fy + 1.6, pw, 1.2, [d1, d2], size=11, align=PP_ALIGN.CENTER, margin=0.02)
        if i < 3:
            arrow(s, x + pw + 0.01, fy + 0.55, x + pw + 0.24, fy + 0.55, color=CYAN, w=2)
    text(s, C1, fy + 3.0, CW, 0.7, [[("Per specimen:  ", {"font": MED, "color": NAVY}),
                                     ("34 data items · 10 instruments · 17 file kinds", {})]], size=14, margin=0.05)

    # ================= row 1 right: 2 the agent approach (graphic 2)
    heading(s, C2, y0, CW, "2", "The agent approach: check first", fill=RED)
    cy = y0 + 1.4; bw = (CW - 2 * 0.3) / 3
    srcs = [("Workflow", ["12 steps,", "domain language"]), ("BAM standard", ["bam-masterdata,", "141 object types"]),
            ("BAM Data Store", ["what exists?", "read-only"])]
    for i, (t, d) in enumerate(srcs):
        x = C2 + i * (bw + 0.3)
        text(s, x, cy, bw, 2.1, [[(t, {"font": MED, "color": NAVY, "size": 13})]] + d, size=11,
             fill=LIGHT, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, margin=0.1, name=f"Source {t}")
        arrow(s, x + bw / 2, cy + 2.12, x + bw / 2, cy + 2.7, color=NAVY)
    text(s, C2, cy + 2.75, CW, 1.3, [[("AI agents + scripts", {"font": MED, "size": 14})],
                                     "understand · design · compare – every element gets one verdict"],
         size=11, color=WHITE, fill=NAVY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, margin=0.1, name="Agents")
    # counts = every single element of the gap analysis (types, vocabularies, property fields, dataset types)
    verdicts = [("REUSE", "20", ["types, fields, file", "types used as is"], PETROL),
                ("EXTEND", "2", ["existing lists get", "new terms"], CYAN),
                ("CREATE", "41", ["2 object types,", "6 lists, 33 fields"], RED)]
    vy = cy + 4.3; vw = (CW - 2 * 0.25) / 3
    for i, (k, n, d, col) in enumerate(verdicts):
        x = C2 + i * (vw + 0.25)
        box(s, x, vy, vw, 3.1, col, name=f"Verdict {k}")
        text(s, x, vy + 0.05, vw, 1.15, [[(n + "  ", {"size": 30}), (k, {"size": 13})]], font=MED, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, margin=0.02)
        text(s, x, vy + 1.3, vw, 1.7, d, size=11, color=WHITE, align=PP_ALIGN.CENTER, margin=0.08)
    text(s, C2, vy + 3.25, CW, 1.3, [[("Humans approve twice ", {"font": MED, "color": RED}),
                                      ("(see 4). Only missing elements are created; new types go to the "
                                       "BAM standard as a pull request.", {})]], size=12, line=15, margin=0.05)

    # ================= row 2: 3 pipeline (graphic 3)
    py3 = 21.05
    heading(s, L, py3, W, "3", "Seven steps: scripts count, agents decide, humans approve", fill=PETROL)
    steps = [("1", "Catalog the", "standard", "S"), ("2", "Inventory the", "instance", "S"), ("3", "Read the", "workflow", "A"),
             ("4", "Design a flat", "structure", "A"), ("5", "Gap analysis,", "3 verdicts", "A"),
             ("6", "Python classes,", "import-tested", "A"), ("7", "Apply to openBIS,", "dry run first", "S")]
    sw = (W - 6 * 0.3) / 7; sy = py3 + 1.35
    for i, (n, t1, t2, kind) in enumerate(steps):
        x = L + i * (sw + 0.3)
        col, tc = (NAVY, WHITE) if kind == "A" else (LIGHT, NAVY)
        box(s, x, sy, sw, 2.4, col, shape=MSO_SHAPE.ROUNDED_RECTANGLE, name=f"Step {n}")
        text(s, x, sy + 0.05, sw, 0.85, n, size=20, font=MED, color=CYAN, align=PP_ALIGN.CENTER, margin=0.02)
        text(s, x, sy + 0.85, sw, 1.5, [t1, t2], size=11, color=tc, align=PP_ALIGN.CENTER, margin=0.05)
        if i < 6:
            arrow(s, x + sw + 0.02, sy + 1.2, x + sw + 0.28, sy + 1.2, color=NAVY, w=1.75)
        if n in ("4", "5"):
            text(s, x, sy + 2.45, sw, 0.6, "✔ human approval", size=11, font=MED, color=RED, align=PP_ALIGN.CENTER, margin=0.02)
    text(s, L, sy + 2.45, 9.0, 0.6, [[("■ ", {"color": NAVY}), ("AI agent    ", {}), ("■ ", {"color": GREY}),
                                      ("deterministic script", {})]], size=11, margin=0.05)

    # ================= row 3 left: 4 what the human checks (graphic 4: excerpts of the two review documents)
    y4 = 25.85
    heading(s, C1, y4, CW, "4", "What the human checks", fill=RED)
    checkpoint(s, C1, y4 + 1.4, CW, "Checkpoint 1 · Design", "design.md – every step gets one place",
               [2.9, 4.1, 5.3],
               [("01 Quality check", "specimen, section 01", "6 fields"),
                ("03 3D scan", "own SCAN object", "GOM scanner, raw data"),
                ("10 Fatigue test", "TEST, section 10", "machine, load programme")],
               "34 data items + 17 file kinds placed · 0 unplaced · 8 questions answered")
    checkpoint(s, C1, y4 + 4.85, CW, "Checkpoint 2 · Gap report", "gap-report.md – one verdict per element",
               [2.1, 4.0, 6.2],
               [("REUSE", "testing machine", "standard, object_types.py:1604"),
                ("EXTEND", "weld type list", "+2 terms, vocabularies.py:38"),
                ("CREATE", "cyclic fatigue test", "nearest: FCG test – no S-N data")],
               "file:line in the standard or a reason – nothing is created unchecked")

    # ================= row 3 right: 5 result in openBIS (graphic 5)
    heading(s, C2, y4, CW, "5", "Result: one specimen, three steps, one level", fill=CYAN)
    ty = y4 + 1.4
    text(s, C2, ty, CW, 1.15, [[("Specimen   ", {"font": MED}), ("“Next step” on top · sections 01 · 02 · 04 · 05 · 06", {})]],
         size=12, color=WHITE, fill=NAVY, anchor=MSO_ANCHOR.MIDDLE, margin=0.3, name="Specimen node")
    kids = [("SCAN", "steps 03–04"), ("TEST", "steps 07–11"), ("FRACTURE", "step 12")]
    kw = (CW - 2 * 0.3) / 3
    for i, (k, d) in enumerate(kids):
        x = C2 + i * (kw + 0.3)
        arrow(s, x + kw / 2, ty + 1.15, x + kw / 2, ty + 1.7, color=NAVY)
        text(s, x, ty + 1.75, kw, 1.2, [[(k, {"font": MED, "color": NAVY})], d], size=11, fill=LIGHT,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, margin=0.05, name=f"Child {k}")
    text(s, C2, ty + 3.0, CW, 0.6, "Instruments & consumables: created once in the inventory, linked as parents",
         size=11, color=PETROL, margin=0.05)
    ky = ty + 3.75
    kpis = [("2", "new object", "types"), ("6+2", "vocabularies", "new + extended"), ("0", "new dataset", "types"), ("1", "link", "depth")]
    kw2 = (CW - 3 * 0.2) / 4
    for i, (n, d1, d2) in enumerate(kpis):
        x = C2 + i * (kw2 + 0.2)
        text(s, x, ky, kw2, 1.2, n, size=30, font=MED, color=RED, align=PP_ALIGN.CENTER, margin=0.02)
        text(s, x, ky + 1.15, kw2, 1.1, [d1, d2], size=11, align=PP_ALIGN.CENTER, margin=0.02)

    # ================= take-home (results box at the end, template recommendation)
    ry = 34.85
    box(s, L, ry, W, 2.45, RED, name="Take-home box")
    text(s, L, ry, 4.2, 2.45, [[("Take-home", {"font": MED, "size": 17})]], color=WHITE,
         anchor=MSO_ANCHOR.MIDDLE, margin=0.4)
    msgs = [("Check, don’t just generate", "deterministic catalog, real import test, dry run"),
            ("Humans decide", "design & gap report approved; domain calls stay with experts"),
            ("Reusable pattern", "any department: describe → agents check → approve")]
    mw = (W - 4.2 - 0.3) / 3
    for i, (h1, d) in enumerate(msgs):
        x = L + 4.2 + i * mw
        text(s, x, ry + 0.15, mw - 0.2, 2.15, [[(h1, {"font": MED, "size": 14})], d], size=12, line=15,
             color=WHITE, anchor=MSO_ANCHOR.MIDDLE, margin=0.1)
    return prs


if __name__ == "__main__":
    prs = build()
    prs.save(str(OUT))
    print("saved", OUT)
