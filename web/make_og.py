#!/usr/bin/env python3
"""Falken — genera web/og.png (1200x630), la imagen que muestran las redes al compartir
un enlace de ccmai.org/falken. Las redes no muestran SVG, por eso es PNG.

Uso: python3 web/make_og.py   (después, build.py la copia a la web)
Mismo estilo que scripts/make-og.py de aios-base (DejaVu Sans Mono, verde terminal).
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 1200, 630
BG, PANEL, BRIGHT, INK, DIM, LINE = "#000000", "#001100", "#00ff00", "#33ff33", "#008800", "#006400"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)


def hexagon(draw, cx, cy, s):
    # el mismo hexágono que hex.svg (viewBox 100x116), escalado a s
    pts = [(50, 4), (92, 30), (92, 86), (50, 112), (8, 86), (8, 30)]
    pts = [(cx + (x - 50) * s, cy + (y - 58) * s) for x, y in pts]
    draw.polygon(pts, fill=PANEL, outline=BRIGHT, width=int(8 * s))
    r = 16 * s
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BRIGHT)


def main():
    img = Image.new("RGB", (W, H), BG)

    # resplandor verde detrás del hexágono, como el drop-shadow de la web
    glow = Image.new("RGB", (W, H), BG)
    hexagon(ImageDraw.Draw(glow), 130, 175, 0.95)
    img = Image.blend(img, glow.filter(ImageFilter.GaussianBlur(14)), 0.6)
    d = ImageDraw.Draw(img)
    hexagon(d, 130, 175, 0.95)

    # identidad a la izquierda
    d.text((205, 122), "FALKEN", font=font(92, True), fill=BRIGHT)
    d.text((84, 265), "the agent-native", font=font(28), fill=DIM)
    d.text((84, 300), "application profile", font=font(28), fill=DIM)
    for i, line in enumerate(["> an open standard", "> a profile on top of MCP",
                              "> apps agents use for you"]):
        d.text((84, 365 + i * 34), line, font=font(23), fill=INK)
    d.text((84, 488), "ccmai.org/falken", font=font(24, True), fill=BRIGHT)

    # terminal a la derecha con los principios del manifiesto
    x, y, sw, sh = 630, 165, 520, 330
    d.rectangle([x - 2, y - 30, x + sw + 1, y + sh + 1], fill=PANEL, outline=LINE, width=2)
    for i, c in enumerate(("#ff5f56", "#ffbd2e", BRIGHT)):
        d.ellipse([x + 12 + i * 20, y - 21, x + 24 + i * 20, y - 9], fill=c)
    d.text((x + 80, y - 24), "falken — manifesto", font=font(15), fill=DIM)
    d.rectangle([x, y, x + sw - 1, y + sh - 1], fill="#000600")
    lines = [
        ("GREETINGS, PROFESSOR FALKEN.", BRIGHT),
        ("SHALL WE PLAY A GAME?", BRIGHT),
        ("", INK),
        ("> capabilities before screens", INK),
        ("> every action declares its risk", INK),
        ("> irreversible = user confirms", INK),
        ("> every action can be verified", INK),
        ("> everything is logged", INK),
        ("> interface on demand", INK),
        ("> local first", INK),
    ]
    for i, (line, col) in enumerate(lines):
        d.text((x + 16, y + 16 + i * 28), line, font=font(19), fill=col)
    cy = y + 16 + len(lines) * 28
    d.rectangle([x + 16, cy + 2, x + 27, cy + 22], fill=BRIGHT)  # cursor

    out = HERE / "og.png"
    img.save(out, optimize=True)
    print(out, img.size, out.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
