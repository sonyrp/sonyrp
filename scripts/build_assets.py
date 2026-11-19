#!/usr/bin/env python3
"""Build the generated profile art (header, footer, panels and dividers).

Usage: python scripts/build_assets.py   -> writes into assets/
Palette: parchment, ship wood, straw-hat yellow, vest red, turquoise sea.
"""
import os
import random

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
INK, CREAM, RED, STRAW, WOOD = "#3b2a1a", "#fff8e1", "#c0392b", "#f2c14e", "#5a3a1e"
SERIF = "Georgia,'Times New Roman',serif"
HEAVY = "'Arial Black',Impact,'Segoe UI Black','Helvetica Neue',Arial,sans-serif"
MONO = "Consolas,'Courier New',monospace"


def save(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    print("wrote", name)


def frame(w, h):
    """Wooden frame with a parchment sheet inside."""
    return f'''<defs>
<radialGradient id="parch" cx=".5" cy=".5" r=".75"><stop offset="0" stop-color="#f8ebc8"/><stop offset=".75" stop-color="#eed9a4"/><stop offset="1" stop-color="#d2ae6c"/></radialGradient>
<filter id="paper" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".04" numOctaves="4" seed="5"/><feColorMatrix values="0 0 0 0 .45  0 0 0 0 .30  0 0 0 0 .12  0 0 0 .5 -.12"/><feComposite operator="in" in2="SourceGraphic"/></filter>
</defs>
<rect width="{w}" height="{h}" rx="14" fill="{WOOD}"/>
<rect x="2" y="2" width="{w - 4}" height="{h - 4}" rx="12" fill="none" stroke="#8b5a2b" stroke-width="2"/>
<rect x="8" y="8" width="{w - 16}" height="{h - 16}" rx="8" fill="url(#parch)"/>
<rect x="8" y="8" width="{w - 16}" height="{h - 16}" rx="8" filter="url(#paper)"/>
<rect x="15" y="15" width="{w - 30}" height="{h - 30}" rx="5" fill="none" stroke="{INK}" stroke-opacity=".45" stroke-width="1.2"/>
<g fill="{STRAW}" stroke="{INK}" stroke-width="1"><circle cx="8" cy="8" r="3.5"/><circle cx="{w - 8}" cy="8" r="3.5"/><circle cx="8" cy="{h - 8}" r="3.5"/><circle cx="{w - 8}" cy="{h - 8}" r="3.5"/></g>'''


def svg(w, h, style, body, framed=True):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n'
            f'<style>text{{font-family:{SERIF}}}.mono{{font-family:{MONO}}}{style}</style>\n'
            + (frame(w, h) if framed else "") + body + "\n</svg>\n")


def otext(x, y, txt, size, fill=RED, anchor="start", extra=""):
    """Manga-logo text: dark outline, cream outline, bright fill."""
    base = (f'x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" font-weight="900" '
            f'style="font-family:{HEAVY}" stroke-linejoin="round" {extra}')
    return (f'<text {base} fill="{INK}" stroke="{INK}" stroke-width="{size * .26:.1f}">{txt}</text>'
            f'<text {base} fill="{CREAM}" stroke="{CREAM}" stroke-width="{size * .12:.1f}">{txt}</text>'
            f'<text {base} fill="{fill}">{txt}</text>')


def wave(y, amp, fill, cls="", extra="", bottom=400):
    d = f"M0 {y} q50 -{amp} 100 0 " + "t100 0 " * 13 + f"V{bottom} H0 Z"
    return f'<g class="{cls}"><path d="{d}" fill="{fill}" {extra}/></g>'


def chip(x, y, w, txt, fill):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="26" rx="13" fill="{fill}" stroke="{INK}" stroke-width="1.5"/>'
            f'<text class="mono" x="{x + w / 2}" y="{y + 18}" text-anchor="middle" font-size="13" font-weight="700" fill="{INK}">{txt}</text>')


STRAW_HAT = f'''<ellipse cx="0" cy="10" rx="44" ry="11" fill="{STRAW}" stroke="#8a5a12" stroke-width="1.5"/>
<path d="M-26 9 Q-24 -24 0 -24 Q24 -24 26 9 Q0 16 -26 9 Z" fill="#f7d06a" stroke="#8a5a12" stroke-width="1.5"/>
<path d="M-26 2 Q0 10 26 2 L26 9 Q0 16 -26 9 Z" fill="#e63946"/>
<path d="M-18 -12 q18 -6 36 0 M-22 -4 q22 -6 44 0" fill="none" stroke="#c9952c" stroke-width="1"/>'''

SHIP = f'''<rect x="-3" y="-150" width="5" height="126" fill="{INK}"/><rect x="-50" y="-108" width="4" height="84" fill="{INK}"/>
<path d="M70 -34 L104 -52" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>
<g class="flag"><path d="M2 -150 h34 q-5 8 0 18 h-34 Z" fill="#111"/><circle cx="18" cy="-140" r="4.2" fill="#fff"/>
<path d="M11 -143 q7 -7 14 0 Z" fill="{STRAW}"/><path d="M9 -143 h18" stroke="{STRAW}" stroke-width="1.6" stroke-linecap="round"/>
<path d="M11 -135 l14 -4 M11 -139 l14 4" stroke="#fff" stroke-width="1.2" stroke-linecap="round"/></g>
<path d="M-38 -126 Q0 -116 38 -126 L44 -62 Q0 -46 -44 -62 Z" fill="#fffaf0" stroke="{INK}" stroke-width="1.8"/>
<path d="M-30 -110 Q0 -102 30 -110 M-34 -92 Q0 -82 34 -92 M-38 -76 Q0 -64 38 -76" fill="none" stroke="#e63946" stroke-width="3.5"/>
<path d="M-72 -96 Q-48 -90 -26 -96 L-22 -52 Q-48 -42 -76 -52 Z" fill="#fffaf0" stroke="{INK}" stroke-width="1.8"/>
<path d="M70 -36 L4 -112 L4 -40 Z" fill="#fffaf0" stroke="{INK}" stroke-width="1.8"/>
<path d="M-84 -34 L80 -34 Q70 0 46 6 L-52 6 Q-74 0 -84 -34 Z" fill="#8b5a2b" stroke="#2b1a0c" stroke-width="2"/>
<path d="M-80 -24 L76 -24" stroke="{STRAW}" stroke-width="3"/><path d="M-76 -14 L72 -14" stroke="#e63946" stroke-width="2"/>
<g fill="#ffe9a8" stroke="#2b1a0c"><circle cx="-40" cy="-4" r="3"/><circle cx="-12" cy="-4" r="3"/><circle cx="16" cy="-4" r="3"/><circle cx="44" cy="-4" r="3"/></g>'''

SMALL_SHIP = '''<path d="M-22 0 h44 q-4 13 -13 15 h-20 q-8 -2 -11 -15 Z" fill="#8b5a2b" stroke="#2b1a0c" stroke-width="1.2"/>
<path d="M0 0 V-42" stroke="#2b1a0c" stroke-width="2.2"/>
<path d="M2 -38 q20 8 17 32 h-17 Z M-2 -32 q-15 6 -14 26 h14 Z" fill="#fffaf0" stroke="#2b1a0c" stroke-width="1.2"/>
<path d="M0 -42 h13 l-3 4 l3 4 h-13 Z" fill="#111"/>'''

CLOUD = '<g id="cloud" fill="#fff"><circle cx="0" cy="0" r="26"/><circle cx="32" cy="-16" r="34"/><circle cx="72" cy="-4" r="28"/><circle cx="102" cy="8" r="18"/><rect x="-22" y="2" width="142" height="26" rx="13"/></g>'


# ───────────────────────── header ─────────────────────────
def header():
    style = """
.w1{animation:wv 7s linear infinite}.w2{animation:wv 11s linear infinite reverse}.w3{animation:wv 16s linear infinite}
@keyframes wv{to{transform:translateX(-200px)}}
.ship{animation:bob 5s ease-in-out infinite;transform-origin:960px 262px}
@keyframes bob{0%,100%{transform:translateY(0) rotate(-2deg)}50%{transform:translateY(-6px) rotate(2deg)}}
.flag{animation:fl 1.6s ease-in-out infinite;transform-origin:0 -150px}
@keyframes fl{0%,100%{transform:skewY(-6deg)}50%{transform:skewY(7deg)}}
.rays{animation:spin 30s linear infinite;transform-origin:1085px 70px}
@keyframes spin{to{transform:rotate(360deg)}}
.c1{animation:dr 60s linear infinite}.c2{animation:dr 90s linear -40s infinite}.c3{animation:dr 75s linear -20s infinite}
@keyframes dr{from{transform:translateX(-260px)}to{transform:translateX(1300px)}}
.gull{animation:gl 26s linear infinite}.gull2{animation:gl 34s linear -12s infinite}
@keyframes gl{from{transform:translateX(-80px)}to{transform:translateX(1300px)}}
.fade{animation:fi 1.4s ease-out both}.fade2{animation:fi 1.4s ease-out .5s both}.fade3{animation:fi 1.4s ease-out 1s both}
@keyframes fi{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
.hat{animation:ht 4s ease-in-out infinite;transform-origin:278px 112px}
@keyframes ht{0%,100%{transform:rotate(-14deg)}50%{transform:rotate(-8deg)}}
.fish{animation:jump 7s ease-in-out infinite;transform-origin:700px 300px}
@keyframes jump{0%,60%{transform:rotate(-70deg)}80%{transform:rotate(20deg)}100%{transform:rotate(70deg)}}
.palm{animation:sway 5s ease-in-out infinite;transform-origin:150px 236px}
.coin{animation:fall 7s ease-in infinite}
@keyframes fall{0%{transform:translateY(-30px)}55%,100%{transform:translateY(330px)}}
.flip{animation:flip .7s linear infinite;transform-box:fill-box;transform-origin:center}
@keyframes flip{0%,100%{transform:scaleX(1)}50%{transform:scaleX(.15)}}
.spk{animation:spk 2.6s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
@keyframes spk{0%,100%{transform:scale(0)}50%{transform:scale(1)}}
@keyframes sway{0%,100%{transform:rotate(-3deg)}50%{transform:rotate(3deg)}}
"""
    rays = "".join(f'<path d="M1085 14 l7 18 h-14 Z" transform="rotate({a} 1085 70)"/>' for a in range(0, 360, 30))
    body = f'''<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1e9fe0"/><stop offset=".55" stop-color="#6fd0f5"/><stop offset=".8" stop-color="#d6f4fb"/></linearGradient>
<clipPath id="frame"><rect width="1200" height="340" rx="14"/></clipPath>{CLOUD}</defs>
<g clip-path="url(#frame)">
<rect width="1200" height="340" fill="url(#sky)"/>
<g class="rays" fill="#ffb703">{rays}</g>
<circle cx="1085" cy="70" r="36" fill="#ffd23f" stroke="#f39c12" stroke-width="3"/>
<g class="c2" opacity=".85"><use href="#cloud" x="0" y="60" transform="scale(.7)"/></g>
<g class="c1"><use href="#cloud" x="0" y="118"/></g>
<g class="c3" opacity=".9"><use href="#cloud" x="0" y="40" transform="scale(1.25)"/></g>
<g fill="#fff" opacity=".95"><circle cx="20" cy="250" r="50"/><circle cx="80" cy="232" r="46"/><circle cx="330" cy="252" r="40"/><circle cx="390" cy="240" r="52"/><circle cx="460" cy="256" r="36"/>
<circle cx="700" cy="254" r="40"/><circle cx="760" cy="238" r="50"/><circle cx="830" cy="254" r="38"/><circle cx="1120" cy="246" r="48"/><circle cx="1180" cy="232" r="50"/></g>
<g class="gull" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"><path d="M0 96 q8 -9 16 0 q8 -9 16 0"/><path d="M40 114 q6 -7 12 0 q6 -7 12 0"/></g>
<g class="gull2" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linecap="round"><path d="M0 150 q6 -7 12 0 q6 -7 12 0"/></g>
<!-- island -->
<path d="M70 250 Q110 214 160 222 Q215 212 245 250 Z" fill="#6ab04c" stroke="{INK}" stroke-width="2"/>
<path d="M60 252 Q150 236 255 252 Z" fill="#f6e2a8" stroke="{INK}" stroke-width="1.5"/>
<g class="palm"><path d="M150 236 q-6 -34 6 -62" fill="none" stroke="#8b5a2b" stroke-width="6" stroke-linecap="round"/>
<path d="M156 174 q-30 -16 -44 6 M156 174 q30 -16 44 6 M156 174 q-12 -30 -38 -24 M156 174 q12 -30 38 -24 M156 174 q-2 -30 2 -36" fill="none" stroke="#2f8f3a" stroke-width="6" stroke-linecap="round"/></g>
{"".join(f'<g class="coin" style="animation-delay:-{d}s"><g class="flip"><circle cx="{x}" cy="0" r="9" fill="#ffd23f" stroke="{INK}" stroke-width="2"/><circle cx="{x}" cy="0" r="4.5" fill="none" stroke="#c9952c" stroke-width="1.5"/></g></g>' for x, d in ((300, 0), (470, 2.4), (640, 4.6), (800, 1.2), (560, 5.8)))}
{"".join(f'<path class="spk" style="animation-delay:{d}s" d="M{x} {y - 9} l3 6 l6 3 l-6 3 l-3 6 l-3 -6 l-6 -3 l6 -3 Z" fill="#fff"/>' for d, (x, y) in enumerate(((228, 150), (868, 96), (430, 96), (700, 190), (1010, 60))))}
{wave(252, 10, "#2ec4c6", "w3", bottom=340)}
<g class="fish"><path d="M700 232 q14 -10 24 0 q-10 10 -24 0 Z M700 232 l-9 -7 v14 Z" fill="#ff7f50" stroke="{INK}" stroke-width="1.2"/></g>
<g class="ship"><g transform="translate(960 262)">{SHIP}</g></g>
{wave(272, 14, "#17a2b8", "w2", bottom=340)}
{wave(298, 16, "#0e7c96", "w1", bottom=340)}
<g class="w1"><path d="M0 300 q50 -16 100 0 {"t100 0 " * 13}" fill="none" stroke="#fff" stroke-width="2" opacity=".6"/></g>
<text class="fade3" x="545" y="62" text-anchor="middle" font-size="17" font-style="italic" font-weight="700" fill="{INK}" letter-spacing="4">— SETTING SAIL ON THE GRAND LINE OF DATA —</text>
<g class="fade">{otext(545, 160, "SONIA RESTREPO", 60, "#e63946", "middle", 'textLength="560" lengthAdjust="spacingAndGlyphs"')}</g>
<g class="fade2"><path d="M246 184 h598 l-14 19 l14 19 h-598 l14 -19 Z" fill="{STRAW}" stroke="{INK}" stroke-width="2.5"/>
<text class="mono" x="545" y="209" text-anchor="middle" font-size="17" font-weight="700" fill="{INK}" letter-spacing="1.5">DATA &amp; AI ENGINEER  ✦  PHYSICS ENGINEER  ✦  R&amp;D&amp;I</text></g>
<g class="fade"><g class="hat"><g transform="translate(278 102)">{STRAW_HAT}</g></g></g>
</g>
<rect x="1.5" y="1.5" width="1197" height="337" rx="13" fill="none" stroke="{INK}" stroke-width="3"/>'''
    save("header-op.svg", svg(1200, 340, style, body, framed=False))


# ───────────────────────── footer ─────────────────────────
def footer():
    style = """
.w1{animation:wv 7s linear infinite}.w2{animation:wv 11s linear infinite reverse}
@keyframes wv{to{transform:translateX(-200px)}}
.sail{animation:go 38s linear -9s infinite}
@keyframes go{from{transform:translateX(-80px)}to{transform:translateX(1290px)}}
.bob{animation:bob 3s ease-in-out infinite}
@keyframes bob{0%,100%{transform:translateY(0) rotate(-3deg)}50%{transform:translateY(-3px) rotate(3deg)}}
.rays{animation:spin 40s linear infinite;transform-origin:600px 124px}
@keyframes spin{to{transform:rotate(360deg)}}
"""
    rays = "".join(f'<path d="M600 -40 l16 164 h-32 Z" transform="rotate({a} 600 124)"/>' for a in range(0, 360, 20))
    body = f'''<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff9a3c"/><stop offset=".7" stop-color="#ffd166"/><stop offset="1" stop-color="#fff1b8"/></linearGradient>
<clipPath id="frame"><rect width="1200" height="170" rx="14"/></clipPath></defs>
<g clip-path="url(#frame)">
<rect width="1200" height="170" fill="url(#sky)"/>
<g class="rays" fill="#fff" opacity=".22">{rays}</g>
<circle cx="600" cy="124" r="58" fill="#e63946" stroke="{INK}" stroke-width="2.5"/>
{otext(600, 62, "THE VOYAGE CONTINUES...", 32, STRAW, "middle")}
<text class="mono" x="600" y="94" text-anchor="middle" font-size="15" font-weight="700" fill="{INK}" letter-spacing="1.5">see you on the next island, nakama  ✦  thanks for coming aboard</text>
{wave(122, 12, "#17a2b8", "w2", bottom=170)}
<g class="sail"><g transform="translate(0 128)"><g class="bob"><g transform="scale(.8)">{SMALL_SHIP}</g></g></g></g>
{wave(142, 14, "#0e7c96", "w1", bottom=170)}
</g>
<rect x="1.5" y="1.5" width="1197" height="167" rx="13" fill="none" stroke="{INK}" stroke-width="3"/>'''
    save("footer-op.svg", svg(1200, 170, style, body, framed=False))


# ─────────────────────── current arc ───────────────────────
def current_arc():
    style = """
.w1{animation:wv 6s linear infinite}.w2{animation:wv 9s linear infinite reverse}
@keyframes wv{to{transform:translateX(-200px)}}
.boat{animation:bob 3.5s ease-in-out infinite;transform-origin:270px 215px}
@keyframes bob{0%,100%{transform:translateY(0) rotate(-2.5deg)}50%{transform:translateY(-6px) rotate(2.5deg)}}
.flag{animation:fl 1.4s ease-in-out infinite;transform-origin:262px 50px}
@keyframes fl{0%,100%{transform:skewY(-7deg)}50%{transform:skewY(7deg)}}
.rays{animation:spin 8s linear infinite;transform-origin:414px 184px}
@keyframes spin{to{transform:rotate(360deg)}}
.zap{animation:zap 2.4s steps(1) infinite}
@keyframes zap{0%{opacity:1}8%{opacity:0}14%{opacity:1}22%,100%{opacity:0}}
.cloud{animation:cl 5s ease-in-out infinite}
@keyframes cl{0%,100%{transform:translateX(0)}50%{transform:translateX(10px)}}
.juice{animation:ch 6s ease-in-out infinite}
@keyframes ch{0%{transform:translateX(-126px)}80%,92%{transform:translateX(0)}100%{transform:translateX(-126px)}}
.spark{animation:zap 1.2s steps(1) infinite}
.front{stroke-dasharray:330;stroke-dashoffset:330;animation:draw 6s ease-out infinite}
@keyframes draw{0%,20%{stroke-dashoffset:330}60%,100%{stroke-dashoffset:0}}
.p{transform-box:fill-box;transform-origin:center;animation:pp 6s ease-out infinite}
@keyframes pp{0%{transform:scale(0)}6%{transform:scale(1.5)}10%,100%{transform:scale(1)}}
.q{transform-box:fill-box;transform-origin:center;animation:qq 6s ease-out infinite}
@keyframes qq{0%,55%{transform:scale(0)}62%{transform:scale(1.7)}68%,100%{transform:scale(1)}}
.gull{animation:gl 14s linear infinite}
@keyframes gl{from{transform:translateX(0)}to{transform:translateX(520px)}}
"""
    rays = "".join(f'<path d="M414 158 l5 10 h-10 Z" transform="rotate({a} 414 184)"/>' for a in range(0, 360, 45))
    windows = "".join(f'<rect x="{x}" y="138" width="30" height="26" rx="5" fill="#9be7f5" stroke="{INK}" stroke-width="1.8"/>'
                      f'<path d="M{x + 5} 160 l12 -18" stroke="#fff" stroke-width="3" opacity=".6"/>' for x in (186, 224, 262, 300))
    dots = "".join(f'<circle class="p" cx="{x}" cy="{y}" r="4" style="animation-delay:{i * .2 + .1:.1f}s"/>'
                   for i, (x, y) in enumerate([(1040, 104), (1090, 92), (1120, 130), (1068, 136), (1010, 130),
                                               (1130, 162), (1092, 162), (1140, 102), (1050, 162), (996, 98)]))
    xs = "".join(f'<path class="q" style="animation-delay:{i * .15:.2f}s" d="M{x - 6} {y - 6}l12 12m0 -12l-12 12"/>'
                 for i, (x, y) in enumerate([(968, 96), (982, 136), (1010, 164), (1056, 181), (1110, 189)]))
    body = f'''<defs>
<linearGradient id="dusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4fc3f7"/><stop offset=".7" stop-color="#c8f1fb"/></linearGradient>
<linearGradient id="juice" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#e63946"/><stop offset=".5" stop-color="#ffd23f"/><stop offset="1" stop-color="#6ab04c"/></linearGradient>
<clipPath id="win"><rect x="40" y="32" width="440" height="236" rx="10"/></clipPath>
<clipPath id="cell"><rect x="204" y="206" width="126" height="20" rx="3"/></clipPath></defs>
<!-- manga panel: the bus-ship -->
<g clip-path="url(#win)">
<rect x="40" y="32" width="440" height="236" fill="url(#dusk)"/>
<g fill="#fff"><circle cx="330" cy="196" r="34"/><circle cx="376" cy="186" r="42"/><circle cx="430" cy="198" r="34"/><circle cx="470" cy="190" r="30"/><circle cx="60" cy="200" r="30"/></g>
<g class="gull" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round"><path d="M0 70 q7 -8 14 0 q7 -8 14 0"/></g>
{wave(206, 9, "#2ec4c6", "w2", bottom=280)}
<g class="cloud"><g fill="#5f5a7a" stroke="{INK}" stroke-width="2"><circle cx="92" cy="70" r="22"/><circle cx="124" cy="58" r="28"/><circle cx="160" cy="70" r="22"/><rect x="74" y="66" width="104" height="26" rx="13"/></g>
<path d="M92 70 a22 22 0 0 1 20 -26 M124 58 a28 28 0 0 1 30 -22" fill="none" stroke="#8a86a8" stroke-width="3" stroke-linecap="round"/></g>
<path class="zap" d="M150 92 L196 76 L186 92 L262 56" fill="none" stroke="#ffd23f" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>
<path class="zap" d="M150 92 L196 76 L186 92 L262 56" fill="none" stroke="#fff" stroke-width="1.5" stroke-linejoin="round"/>
<g class="boat">
  <path d="M262 130 V50" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>
  <g class="flag"><path d="M264 50 h30 q-5 7 0 16 h-30 Z" fill="#111"/><circle cx="278" cy="57" r="3.6" fill="#fff"/><path d="M272 54 q6 -6 12 0 Z" fill="{STRAW}"/></g>
  <path d="M222 70 Q262 80 302 70 L308 120 Q262 132 216 120 Z" fill="#fffaf0" stroke="{INK}" stroke-width="2"/>
  <path d="M268 78 l-14 20 h10 l-6 16 l18 -24 h-10 Z" fill="#ffd23f" stroke="{INK}" stroke-width="1.5"/>
  <rect x="175" y="128" width="200" height="64" rx="13" fill="#fff3d1" stroke="{INK}" stroke-width="2.5"/>
  <path d="M176 172 H374 v8 q0 12 -12 12 H188 q-12 0 -12 -12 Z" fill="#e63946"/><path d="M176 172 H374" stroke="{INK}" stroke-width="1.5"/>
  {windows}
  <path d="M340 138 h20 q8 0 8 9 v17 h-28 Z" fill="#9be7f5" stroke="{INK}" stroke-width="1.8"/>
  <text x="272" y="187" text-anchor="middle" font-size="11" font-weight="700" fill="{CREAM}" letter-spacing="4">MEGABÚS</text>
  <path d="M146 190 L404 190 Q396 234 362 240 L186 240 Q156 234 146 190 Z" fill="#8b5a2b" stroke="#2b1a0c" stroke-width="2.5"/>
  <path d="M150 198 L400 198" stroke="{STRAW}" stroke-width="4"/>
  <rect x="200" y="202" width="134" height="28" rx="6" fill="{INK}" stroke="{CREAM}" stroke-width="2"/><rect x="334" y="210" width="6" height="12" rx="2" fill="{CREAM}"/>
  <g clip-path="url(#cell)"><rect class="juice" x="204" y="206" width="126" height="20" fill="url(#juice)"/></g>
  <path d="M236 206 v20 M267 206 v20 M298 206 v20" stroke="{INK}" stroke-width="2"/>
  <path class="spark" d="M356 204 l-6 9 h5 l-3 8 l8 -11 h-5 Z" fill="#ffd23f" stroke="{INK}" stroke-width="1"/>
  <g class="rays" fill="#ff9f1c" stroke="{INK}" stroke-width="1">{rays}</g>
  <circle cx="414" cy="184" r="15" fill="#ffd23f" stroke="{INK}" stroke-width="2"/>
  <path d="M408 181 v3 M420 181 v3 M407 188 q7 6 14 0" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>
</g>
{wave(238, 12, "#17a2b8", "w1", bottom=280)}
<g class="w1"><path d="M0 240 q50 -12 100 0 {"t100 0 " * 13}" fill="none" stroke="#fff" stroke-width="2" opacity=".7"/></g>
</g>
<rect x="40" y="32" width="440" height="236" rx="10" fill="none" stroke="{INK}" stroke-width="4"/>
<!-- title -->
<text x="512" y="74" font-size="14" font-weight="700" fill="#a12a1e" letter-spacing="6">CURRENT ARC</text>
{otext(512, 128, "MEGABÚS ISLAND", 38, "#e63946", "start", 'textLength="370" lengthAdjust="spacingAndGlyphs"')}
<text class="mono" x="512" y="164" font-size="15" font-weight="700" fill="{INK}">optimizing electric-bus charging with AI</text>
<text x="512" y="188" font-size="14" font-style="italic" fill="#6b4a22">lowest cost · healthy batteries · a calm grid</text>
{chip(512, 208, 130, "NSGA-II + PSO", STRAW)}{chip(650, 208, 132, "ML forecasting", "#ff9f1c")}{chip(790, 208, 110, "IoT live", "#ff6b6b")}
<!-- Pareto treasure hunt -->
<text x="1050" y="62" text-anchor="middle" font-size="14" font-style="italic" font-weight="700" fill="{INK}">✕ marks the Pareto front</text>
<path d="M950 72 V208 H1160" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>
<path d="M945 78 l5 -8 l5 8 M1154 203 l8 5 l-8 5" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>
<text x="1056" y="230" text-anchor="middle" font-size="12" font-weight="700" fill="#6b4a22" letter-spacing="2">ENERGY COST</text>
<text x="934" y="140" text-anchor="middle" font-size="12" font-weight="700" fill="#6b4a22" letter-spacing="2" transform="rotate(-90 934 140)">BATTERY WEAR</text>
<g fill="#b08d57" stroke="{INK}" stroke-width="1">{dots}</g>
<path class="front" d="M966 84 C972 142 1010 182 1150 192" fill="none" stroke="{RED}" stroke-width="3" stroke-dasharray="330" stroke-linecap="round"/>
<g stroke="{RED}" stroke-width="4.5" stroke-linecap="round">{xs}</g>'''
    save("current-arc.svg", svg(1200, 300, style, body))


# ─────────────────── jolly roger + haki ───────────────────
def crew_flag():
    style = """
.flag{animation:fl 2.2s ease-in-out infinite;transform-origin:100px 140px}
@keyframes fl{0%,100%{transform:skewY(-4deg) scaleX(1)}50%{transform:skewY(4deg) scaleX(.97)}}
.bar{transform-box:fill-box;transform-origin:left center;animation:grow 7s ease-out infinite}
@keyframes grow{0%{transform:scaleX(0)}22%,92%{transform:scaleX(1)}100%{transform:scaleX(0)}}
.aura{animation:au 2.4s ease-in-out infinite}
@keyframes au{0%,100%{opacity:.25}50%{opacity:.9}}
"""
    rows = [("Observation Haki", "data analysis · machine learning", .92, "#e63946"),
            ("Armament Haki", "software · data engineering", .86, "#ff9f1c"),
            ("Conqueror's Haki", "leading automation projects", .78, STRAW),
            ("Future Sight", "forecasting · optimization", .88, "#2ec4c6")]
    bars = ""
    for i, (name, sub, val, col) in enumerate(rows):
        y = 118 + i * 42
        bars += (f'<text x="470" y="{y}" font-size="17" font-weight="700" fill="{INK}">{name}</text>'
                 f'<text x="470" y="{y + 15}" font-size="12" font-style="italic" fill="#6b4a22">{sub}</text>'
                 f'<rect x="700" y="{y - 14}" width="450" height="20" rx="10" fill="#d9c08a" stroke="{INK}" stroke-width="1.5"/>'
                 f'<rect class="bar" style="animation-delay:{i * .25:.2f}s" x="702" y="{y - 12}" width="{446 * val:.0f}" height="16" rx="8" fill="{col}"/>'
                 f'<path class="aura" style="animation-delay:{i * .4:.1f}s" d="M{702 + 446 * val + 8:.0f} {y - 14} l4 7 l8 3 l-8 3 l-4 7 l-4 -7 l-8 -3 l8 -3 Z" fill="{col}" stroke="{INK}" stroke-width="1"/>')
    body = f'''<path d="M92 26 V282" stroke="#8b5a2b" stroke-width="9" stroke-linecap="round"/><path d="M92 26 V282" stroke="{INK}" stroke-width="1" opacity=".4"/>
<circle cx="92" cy="24" r="8" fill="{STRAW}" stroke="{INK}" stroke-width="2"/>
<g class="flag">
<path d="M98 42 H410 q-14 48 0 98 q14 48 0 98 H98 Z" fill="#151515" stroke="{INK}" stroke-width="2"/>
<g stroke="#f5f0e0" stroke-width="15" stroke-linecap="round"><path d="M170 80 L338 204 M338 80 L170 204"/></g>
<g fill="#f5f0e0"><circle cx="166" cy="72" r="10"/><circle cx="160" cy="86" r="10"/><circle cx="342" cy="72" r="10"/><circle cx="348" cy="86" r="10"/>
<circle cx="166" cy="212" r="10"/><circle cx="160" cy="198" r="10"/><circle cx="342" cy="212" r="10"/><circle cx="348" cy="198" r="10"/></g>
<circle cx="254" cy="136" r="50" fill="#f5f0e0"/><rect x="226" y="166" width="56" height="34" rx="9" fill="#f5f0e0"/>
<path d="M240 184 v14 M254 184 v16 M268 184 v14" stroke="#151515" stroke-width="3"/>
<circle cx="234" cy="140" r="13" fill="#151515"/><circle cx="274" cy="140" r="13" fill="#151515"/>
<path d="M254 154 l-6 12 h12 Z" fill="#151515"/>
<g fill="none" stroke="{STRAW}" stroke-width="3.5"><circle cx="234" cy="140" r="18"/><circle cx="274" cy="140" r="18"/><path d="M252 140 h4 M216 138 l-12 -6 M292 138 l12 -6"/></g>
<g transform="translate(254 92) scale(1.45)">{STRAW_HAT}</g>
</g>
{otext(470, 62, "THE R&amp;D&amp;I PIRATES", 30, "#e63946")}
<text x="470" y="86" font-size="14" font-style="italic" fill="#6b4a22">our flag flies over every process we automate · haki report below</text>
{bars}'''
    save("crew-flag.svg", svg(1200, 300, style, body))


# ───────────────────────── news coo ─────────────────────────
def news():
    style = """
.paper{animation:pp 6s ease-in-out infinite;transform-origin:440px 160px}
@keyframes pp{0%,100%{transform:rotate(-1.6deg)}50%{transform:rotate(-.6deg)}}
.bird{animation:fly 3s ease-in-out infinite}
@keyframes fly{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}
.wing{animation:flap .5s ease-in-out infinite;transform-box:fill-box;transform-origin:50% 100%}
@keyframes flap{0%,100%{transform:scaleY(1)}50%{transform:scaleY(-.5)}}
.extra{animation:ex 1.6s steps(1) infinite}
@keyframes ex{0%{opacity:1}60%{opacity:.25}}
.stamp{animation:st 6s ease-out infinite;transform-box:fill-box;transform-origin:center}
@keyframes st{0%,12%{transform:scale(3) rotate(-14deg);opacity:0}18%,100%{transform:scale(1) rotate(-14deg);opacity:.85}}
"""
    cols = [("PHISHING FLEET SUNK", ["A whole armada of fake emails", "went down after running into", "an NLP + ML detector."]),
            ("BUSES CHARGE SMARTER", ["The Megabús electric fleet now", "refuels under evolutionary", "algorithms. Grid relieved."]),
            ("BOUNTY ON THE RISE", ["Sources say she keeps", "automating the boring.", "Marines can't keep up."])]
    colsvg = ""
    for i, (h, lines) in enumerate(cols):
        x = 84 + i * 245
        colsvg += f'<text x="{x}" y="192" font-size="14" font-weight="700" fill="{INK}">{h}</text>'
        colsvg += "".join(f'<text x="{x}" y="{212 + j * 17}" font-size="13" fill="{INK}">{ln}</text>' for j, ln in enumerate(lines))
        if i:
            colsvg += f'<path d="M{x - 14} 178 V262" stroke="{INK}" stroke-width="1"/>'
    body = f'''<g class="paper">
<rect x="66" y="40" width="760" height="248" fill="#3b2a1a" opacity=".25" transform="translate(6 6)"/>
<rect x="60" y="34" width="760" height="248" fill="#fdf8ea" stroke="{INK}" stroke-width="2"/>
<text x="440" y="78" text-anchor="middle" font-size="36" font-weight="700" fill="{INK}" letter-spacing="2">THE GRAND LINE GAZETTE</text>
<path d="M76 88 H804 M76 92 H804 M76 110 H804" stroke="{INK}" stroke-width="1.5"/>
<text x="440" y="105" text-anchor="middle" font-size="10.5" fill="{INK}" letter-spacing="2.5">MORNING EDITION · DELIVERED BY NEWS COO · PRICE: 100 BERRIES</text>
<text x="440" y="150" text-anchor="middle" font-size="29" font-weight="900" fill="{INK}" style="font-family:{HEAVY}" textLength="700" lengthAdjust="spacingAndGlyphs">“DATA NAVIGATOR” STRIKES AGAIN!</text>
<path d="M76 164 H804" stroke="{INK}" stroke-width="1"/>
{colsvg}
<g class="stamp"><rect x="668" y="226" width="130" height="38" rx="4" fill="none" stroke="{RED}" stroke-width="3.5"/>
<text x="733" y="252" text-anchor="middle" font-size="19" font-weight="900" fill="{RED}" style="font-family:{HEAVY}">EXTRA!</text></g>
</g>
<!-- News Coo -->
<g class="bird"><g transform="translate(1000 150)">
<path class="wing" d="M-20 -6 Q-70 -70 -120 -40 Q-80 -30 -60 -4 Z" fill="#fff" stroke="{INK}" stroke-width="2.5"/>
<path class="wing" d="M24 -6 Q74 -70 124 -40 Q84 -30 64 -4 Z" fill="#fff" stroke="{INK}" stroke-width="2.5"/>
<ellipse cx="0" cy="14" rx="44" ry="34" fill="#fff" stroke="{INK}" stroke-width="2.5"/>
<path d="M-30 42 l-10 22 l16 -8 l6 12 l6 -22 Z" fill="#fff" stroke="{INK}" stroke-width="2"/>
<circle cx="34" cy="-26" r="24" fill="#fff" stroke="{INK}" stroke-width="2.5"/>
<path d="M12 -38 Q34 -62 58 -38 Z" fill="#e63946" stroke="{INK}" stroke-width="2"/><path d="M52 -40 h22 q4 4 -2 6 h-18 Z" fill="#e63946" stroke="{INK}" stroke-width="2"/>
<circle cx="42" cy="-26" r="3.6" fill="{INK}"/>
<path d="M56 -24 l30 6 l-30 8 Z" fill="#ff9f1c" stroke="{INK}" stroke-width="2"/>
<path d="M-34 -8 L26 40" stroke="#8b5a2b" stroke-width="5"/>
<rect x="6" y="26" width="46" height="36" rx="5" fill="#8b5a2b" stroke="{INK}" stroke-width="2"/><rect x="14" y="20" width="30" height="14" fill="#fdf8ea" stroke="{INK}" stroke-width="1.5"/>
<path d="M18 26 h22 M18 30 h16" stroke="{INK}" stroke-width="1"/><circle cx="29" cy="46" r="4" fill="{STRAW}" stroke="{INK}" stroke-width="1.5"/>
</g></g>
<text class="extra" x="1000" y="268" text-anchor="middle" font-size="20" font-weight="900" fill="{RED}" style="font-family:{HEAVY}" letter-spacing="2">COO! COO! FRESH NEWS!</text>'''
    save("news-coo.svg", svg(1200, 320, style, body))


# ─────────────────────── treasure chest ───────────────────────
def chest():
    style = """
.lid{animation:lid 5s ease-in-out infinite;transform-origin:118px 150px}
@keyframes lid{0%,15%,100%{transform:rotate(0)}35%,80%{transform:rotate(-38deg)}}
.glow{animation:gw 5s ease-in-out infinite}
@keyframes gw{0%,18%,100%{opacity:0}40%,78%{opacity:1}}
.rays{animation:spin 14s linear infinite;transform-origin:200px 150px}
@keyframes spin{to{transform:rotate(360deg)}}
.coin{animation:cn 5s ease-out infinite;opacity:0}
@keyframes cn{0%,30%{opacity:0;transform:translateY(0)}38%{opacity:1}60%{transform:translateY(-78px);opacity:1}80%,100%{transform:translateY(-70px);opacity:0}}
.tw{animation:tw 1.8s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
@keyframes tw{0%,100%{transform:scale(0)}50%{transform:scale(1)}}
"""
    rays = "".join(f'<path d="M200 150 L190 20 L210 20 Z" transform="rotate({a} 200 150)"/>' for a in range(-80, 81, 20))
    coins = "".join(f'<g class="coin" style="animation-delay:{d}s"><circle cx="{x}" cy="150" r="9" fill="#ffd23f" stroke="{INK}" stroke-width="1.5"/>'
                    f'<text x="{x}" y="154" text-anchor="middle" font-size="10" font-weight="700" fill="#8a5a12">฿</text></g>'
                    for x, d in ((160, 0), (200, .25), (240, .5), (180, .7), (222, .9)))
    body = f'''<g class="glow"><g class="rays" fill="#ffd23f" opacity=".45">{rays}</g>
<ellipse cx="200" cy="150" rx="84" ry="26" fill="#fff3b0"/></g>
{coins}
<g class="lid"><path d="M118 150 Q118 96 200 96 Q282 96 282 150 Z" fill="#8b5a2b" stroke="#2b1a0c" stroke-width="2.5"/>
<path d="M150 104 V150 M250 104 V150" stroke="{STRAW}" stroke-width="10"/><path d="M122 132 H278" stroke="#2b1a0c" stroke-width="1.2" opacity=".5"/></g>
<rect x="118" y="150" width="164" height="78" rx="6" fill="#a0672f" stroke="#2b1a0c" stroke-width="2.5"/>
<path d="M150 150 V228 M250 150 V228" stroke="{STRAW}" stroke-width="10"/><path d="M120 176 H280 M120 202 H280" stroke="#2b1a0c" stroke-width="1.2" opacity=".5"/>
<rect x="186" y="150" width="28" height="30" rx="5" fill="{STRAW}" stroke="#2b1a0c" stroke-width="2"/><circle cx="200" cy="162" r="4" fill="#2b1a0c"/><path d="M200 162 v10" stroke="#2b1a0c" stroke-width="3"/>
<ellipse cx="200" cy="236" rx="100" ry="8" fill="#3b2a1a" opacity=".25"/>
<path class="tw" d="M300 100 l3 9 l9 3 l-9 3 l-3 9 l-3 -9 l-9 -3 l9 -3 Z" fill="#ff9f1c"/>
<path class="tw" style="animation-delay:.9s" d="M96 120 l2 6 l6 2 l-6 2 l-2 6 l-2 -6 l-6 -2 l6 -2 Z" fill="#ff9f1c"/>
<text x="350" y="70" font-size="14" font-weight="700" fill="#a12a1e" letter-spacing="6">TREASURE Nº 1</text>
{otext(350, 122, "phishing-detector", 40, "#e63946")}
<text x="350" y="160" font-size="18" fill="{INK}">Hunts phishing emails and messages across the seas</text>
<text x="350" y="184" font-size="18" fill="{INK}">using <tspan font-weight="700">NLP</tspan> and <tspan font-weight="700">Machine Learning</tspan>.</text>
{chip(350, 204, 80, "Python", STRAW)}{chip(438, 204, 100, "NLP + ML", "#ff9f1c")}{chip(546, 204, 130, "Flask web app", "#ff6b6b")}
<text x="1160" y="222" text-anchor="end" font-size="14" font-style="italic" font-weight="700" fill="#6b4a22">click to open the chest ⟶</text>
<text x="1160" y="70" text-anchor="end" font-size="13" font-style="italic" fill="#6b4a22">more treasures on the next islands…</text>'''
    save("treasure-chest.svg", svg(1200, 260, style, body))


# ───────────────────────── poneglyph ─────────────────────────
def poneglyph():
    rnd = random.Random(1522)
    bx, by, cols, rows, c = 60, 42, 12, 5, 33

    def glyph(x, y):
        p = [(x + 6 + i * 10, y + 6 + j * 10) for j in range(3) for i in range(3)]
        out = []
        for _ in range(rnd.randint(3, 4)):
            k = rnd.random()
            a, b = rnd.sample(p, 2)
            if k < .55:
                out.append(f"M{a[0]} {a[1]}L{b[0]} {b[1]}")
            elif k < .8:
                out.append(f"M{a[0]} {a[1]}Q{x + 16} {y + 16} {b[0]} {b[1]}")
            else:
                out.append(f"M{a[0] - 3} {a[1]}a3 3 0 1 0 6 0a3 3 0 1 0 -6 0")
        return " ".join(out)

    style = f"""
.g{{fill:none;stroke:#f6c9a0;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round;animation:scan 6s ease-in-out infinite}}
@keyframes scan{{0%,100%{{stroke:#d99a7c;opacity:.6}}8%{{stroke:#fff3c4;opacity:1}}20%{{stroke:#d99a7c;opacity:.6}}}}
.beam{{animation:beam 6s linear infinite}}
@keyframes beam{{0%{{transform:translateX(0);opacity:0}}5%{{opacity:.5}}62%{{opacity:.5}}68%,100%{{transform:translateX({cols * c}px);opacity:0}}}}
.r{{animation:rv 1.4s ease-out backwards}}.r2{{animation-delay:1.2s}}.r3{{animation-delay:2.6s}}.r4{{animation-delay:3.6s}}
@keyframes rv{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
.q{{animation:qp 6s ease-in-out infinite}}
@keyframes qp{{0%,100%{{fill:#3b2a1a}}50%{{fill:#a12a1e}}}}
"""
    w, h = cols * c, rows * c
    glyphs = "".join(f'<path class="g" style="animation-delay:{i * .32 + j * .05:.2f}s" d="{glyph(bx + i * c, by + j * c)}"/>'
                     for i in range(cols) for j in range(rows))
    tx = bx + w + 56
    body = f'''<defs><linearGradient id="stone" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#b8402f"/><stop offset="1" stop-color="#7a2318"/></linearGradient></defs>
<ellipse cx="{bx + w / 2}" cy="{by + h + 18}" rx="{w / 2 + 30}" ry="9" fill="{INK}" opacity=".25"/>
<path d="M{bx - 16} {by - 12} h{w + 32} v{h + 24} h-{w + 32} Z" fill="url(#stone)" stroke="#3d0f0a" stroke-width="3"/>
<path d="M{bx - 16} {by - 12} h{w + 32} l-8 8 h-{w + 16} Z" fill="#fff" opacity=".14"/>
<path d="M{bx - 16} {by + h + 12} h{w + 32} l-8 -8 h-{w + 16} Z" fill="#000" opacity=".25"/>
{glyphs}
<rect class="beam" x="{bx - 6}" y="{by - 8}" width="10" height="{h + 16}" fill="#fff3c4"/>
<text class="r" x="{tx}" y="64" font-size="13" font-weight="700" fill="#a12a1e" letter-spacing="5">TRANSLATED FROM THE PONEGLYPH OF R&amp;D&amp;I</text>
<text class="r r2" x="{tx}" y="114" font-size="33" font-style="italic" font-weight="700" fill="{INK}">“When do you think people die?</text>
<text class="r r3" x="{tx}" y="156" font-size="33" font-style="italic" font-weight="700" fill="{INK}">…When they are forgotten.”</text>
<text class="r r4" x="{tx}" y="198" font-size="17" font-weight="700" fill="{INK}">— Dr. Hiriluk  <tspan fill="#6b4a22" font-style="italic" font-weight="400">(so I document my code)</tspan></text>'''
    save("poneglyph.svg", svg(1200, 250, style, body))


# ───────────────────────── dividers ─────────────────────────
def dividers():
    mini_hat = f'<g transform="scale(.8)">{STRAW_HAT}</g>'
    spokes = "".join(f'<path d="M0 -7 V-29" transform="rotate({a})"/>' for a in range(0, 360, 45))
    sword = ('<path d="M0 -30 V12" stroke="#3b2a1a" stroke-width="6" stroke-linecap="round"/><path d="M0 -30 V12" stroke="#e8eef0" stroke-width="3.2" stroke-linecap="round"/>'
             '<path d="M-7 12 H7" stroke="#f2c14e" stroke-width="4" stroke-linecap="round"/><path d="M0 14 V28" stroke="{c}" stroke-width="5.5" stroke-linecap="round"/>')
    icons = {
        "hat": ("a{animation:k 3s ease-in-out infinite}@keyframes k{0%,100%{transform:rotate(-8deg)}50%{transform:rotate(8deg)}}",
                f'<g class="a">{mini_hat}</g>'),
        "skull": ("a{animation:k 2.4s ease-in-out infinite}@keyframes k{0%,100%{transform:rotate(-6deg)}50%{transform:rotate(6deg)}}",
                  f'<g class="a"><g stroke-linecap="round"><path d="M-28 -16 L28 22 M28 -16 L-28 22" stroke="{INK}" stroke-width="11"/><path d="M-28 -16 L28 22 M28 -16 L-28 22" stroke="#f5f0e0" stroke-width="7"/></g>'
                  f'<circle cy="-2" r="17" fill="#f5f0e0" stroke="{INK}" stroke-width="2"/><rect x="-10" y="10" width="20" height="12" rx="4" fill="#f5f0e0" stroke="{INK}" stroke-width="2"/>'
                  f'<circle cx="-6.5" cy="-1" r="5" fill="{INK}"/><circle cx="6.5" cy="-1" r="5" fill="{INK}"/><path d="M-4 15 v6 M0 15 v7 M4 15 v6" stroke="{INK}" stroke-width="1.5"/>'
                  f'<g transform="translate(0 -20) scale(.55)">{STRAW_HAT}</g></g>'),
        "helm": ("a{animation:k 12s linear infinite}@keyframes k{to{transform:rotate(360deg)}}",
                 f'<g class="a"><g stroke="{INK}" stroke-width="7" stroke-linecap="round">{spokes}</g><g stroke="#a0672f" stroke-width="4" stroke-linecap="round">{spokes}</g>'
                 f'<circle r="19" fill="none" stroke="{INK}" stroke-width="8"/><circle r="19" fill="none" stroke="#a0672f" stroke-width="5"/><circle r="7" fill="{STRAW}" stroke="{INK}" stroke-width="2"/></g>'),
        "anchor": ("a{animation:k 3s ease-in-out infinite;transform-origin:0 -24px}@keyframes k{0%,100%{transform:rotate(-12deg)}50%{transform:rotate(12deg)}}",
                   ''.join(f'<g class="a" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"><circle cy="-21" r="5"/><path d="M0 -16 V22 M-11 -6 H11 M-20 6 Q-18 22 0 22 Q18 22 20 6 M-24 10 l4 -6 l5 6 M24 10 l-4 -6 l-5 6"/></g>'
                           for c, w in ((INK, 8), ("#8fa3ad", 4.5)))),
        "swords": ("a{animation:k 2.5s ease-in-out infinite}@keyframes k{0%,100%{transform:scale(1)}50%{transform:scale(1.12)}}",
                   f'<g class="a"><g transform="rotate(-48)">{sword.replace("{c}", "#f5f0e0")}</g><g transform="rotate(48)">{sword.replace("{c}", "#c0392b")}</g><g>{sword.replace("{c}", "#222")}</g></g>'),
        "meat": ("a{animation:k 1.6s ease-in-out infinite}@keyframes k{0%,100%{transform:translateY(0) rotate(-10deg)}50%{transform:translateY(-4px) rotate(-4deg)}}",
                 f'<g class="a"><path d="M-36 0 H36" stroke="{INK}" stroke-width="10" stroke-linecap="round"/><path d="M-36 0 H36" stroke="#f5f0e0" stroke-width="6" stroke-linecap="round"/>'
                 f'<g fill="#f5f0e0" stroke="{INK}" stroke-width="2"><circle cx="-38" cy="-5" r="5.5"/><circle cx="-38" cy="5" r="5.5"/><circle cx="38" cy="-5" r="5.5"/><circle cx="38" cy="5" r="5.5"/></g>'
                 f'<ellipse rx="22" ry="16" fill="#b5651d" stroke="{INK}" stroke-width="2.5"/><path d="M-12 -7 q10 -8 22 -2" fill="none" stroke="#e8a15a" stroke-width="3.5" stroke-linecap="round"/></g>'),
        "logpose": ("a{animation:k 2.2s ease-in-out infinite;transform-origin:0 -4px}@keyframes k{0%,100%{transform:rotate(-30deg)}50%{transform:rotate(40deg)}}",
                    f'<rect x="-30" y="10" width="60" height="11" rx="4" fill="#8b5a2b" stroke="{INK}" stroke-width="2"/><circle cy="-4" r="19" fill="#dff6fa" fill-opacity=".85" stroke="{INK}" stroke-width="2.5"/>'
                    f'<path d="M-11 -13 q8 -8 18 -3" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/><g class="a"><path d="M0 -4 L0 -18" stroke="#e63946" stroke-width="3.5" stroke-linecap="round"/><path d="M0 -4 L0 6" stroke="{INK}" stroke-width="3" stroke-linecap="round"/></g><circle cy="-4" r="2.5" fill="{INK}"/>'),
        "chest": ("a{animation:k 1.8s ease-in-out infinite;transform-box:fill-box;transform-origin:center}@keyframes k{0%,100%{transform:scale(0)}50%{transform:scale(1)}}",
                  f'<path d="M-22 0 Q-22 -20 0 -20 Q22 -20 22 0 Z" fill="#8b5a2b" stroke="{INK}" stroke-width="2.5"/><rect x="-22" y="0" width="44" height="22" rx="3" fill="#a0672f" stroke="{INK}" stroke-width="2.5"/>'
                  f'<path d="M-11 -17 V22 M11 -17 V22" stroke="{STRAW}" stroke-width="5"/><rect x="-5" y="-3" width="10" height="11" rx="2" fill="{STRAW}" stroke="{INK}" stroke-width="1.5"/>'
                  f'<path class="a" d="M30 -22 l2.500 7 l7 2.500 l-7 2.500 l-2.500 7 l-2.500 -7 l-7 -2.500 l7 -2.500 Z" fill="#ff9f1c" stroke="{INK}" stroke-width=".8"/>'
                  f'<path class="a" style="animation-delay:.9s" d="M-32 -14 l2 5 l5 2 l-5 2 l-2 5 l-2 -5 l-5 -2 l5 -2 Z" fill="#ff9f1c" stroke="{INK}" stroke-width=".8"/>'),
    }
    for name, (css, icon) in icons.items():
        rope = ""
        for a, b, sag in ((24, 536, 1), (664, 1176, -1)):
            mid = (a + b) / 2
            d = f"M{a} 36 Q{mid} {36 + 9 * sag} {b} 36"
            rope += (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
                     f'<path d="{d}" fill="none" stroke="#d2ae6c" stroke-width="6" stroke-linecap="round"/>'
                     f'<path class="twist" d="{d}" fill="none" stroke="#8a5a12" stroke-width="6" stroke-dasharray="2 8"/>')
        knots = "".join(f'<circle cx="{x}" cy="36" r="7" fill="#d2ae6c" stroke="{INK}" stroke-width="2.5"/>' for x in (24, 536, 664, 1176))
        lag = list(icons).index(name) * 5
        style = (".twist{animation:tw 1.2s linear infinite}@keyframes tw{to{stroke-dashoffset:-10}}"
                 f".boat{{animation:bt 40s linear -{lag}s infinite}}@keyframes bt{{from{{transform:translateX(30px)}}to{{transform:translateX(1170px)}}}}"
                 ".rock{animation:rk 1.4s ease-in-out infinite}@keyframes rk{0%,100%{transform:rotate(-7deg)}50%{transform:rotate(7deg)}}." + css)
        boat = f'<g class="boat"><g transform="translate(0 30)"><g class="rock"><g transform="scale(.42)">{SMALL_SHIP}</g></g></g></g>'
        body = f'{rope}{knots}{boat}<g transform="translate(600 36)">{icon}</g>'
        save(f"divider-{name}.svg", svg(1200, 72, style, body, framed=False))
        glow = ('<defs><filter id="glow" x="-5%" y="-60%" width="110%" height="220%">'
                '<feDropShadow dx="0" dy="0" stdDeviation="2.4" flood-color="#ffe9a8" flood-opacity=".8"/></filter></defs>')
        save(f"divider-{name}-dark.svg", svg(1200, 72, style, f'{glow}<g filter="url(#glow)">{body}</g>', framed=False))


# ─────────────── crew as a devil fruit encyclopedia ───────────────
def _shade(hex_color):
    """Swirl colour: darker for bright fruits, lighter for very dark ones."""
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    if .3 * r + .59 * g + .11 * b < 70:
        r, g, b = (min(255, int(v + (255 - v) * .45)) for v in (r, g, b))
    else:
        r, g, b = (int(v * .62) for v in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


def crew_fruits():
    groups = [
        ("ZOAN", "languages &amp; data science", [
            ("Python", "Py-Py no Mi", "bends any data to its will", "#3776ab"),
            ("PyTorch", "Torch-Torch no Mi", "sets tensors on fire", "#ee4c2c"),
            ("TensorFlow", "Flow-Flow no Mi", "gradients flow like water", "#ff6f00"),
            ("scikit-learn", "Kit-Kit no Mi", "a model for every occasion", "#f7931e"),
            ("MATLAB", "Mat-Mat no Mi", "total matrix mastery", "#e16737"),
            ("LaTeX", "Tex-Tex no Mi", "papers that typeset themselves", "#008080"),
        ]),
        ("PARAMECIA", "development &amp; tools", [
            ("FastAPI", "Fast-Fast no Mi", "APIs at lightning speed", "#009688"),
            ("Flask", "Flask-Flask no Mi", "web apps in a bottle", "#3b2a1a"),
            ("Docker", "Dock-Dock no Mi", "ships anything in a container", "#2496ed"),
            ("Linux", "Nix-Nix no Mi", "commands the whole ship", "#f2c14e"),
            ("Git", "Git-Git no Mi", "rewinds time itself", "#f05032"),
            ("GitHub Actions", "Act-Act no Mi", "chores that do themselves", "#6e5494"),
        ]),
        ("LOGIA", "AI &amp; automation", [
            ("Claude", "Clau-Clau no Mi", "a navigator that thinks along", "#d97757"),
            ("Claude Code", "Code-Code no Mi", "writes code at full sail", "#191919"),
            ("ChatGPT", "Chat-Chat no Mi", "answers on demand", "#74aa9c"),
            ("Hugging Face", "Hug-Hug no Mi", "a whole library of models", "#ffd21e"),
            ("LangChain", "Chain-Chain no Mi", "links models into a crew", "#1c3c3c"),
            ("n8n", "Node-Node no Mi", "automates the entire deck", "#ea4b71"),
        ]),
    ]
    shapes = [
        "M0 -48 C34 -48 54 -24 54 4 C54 34 30 50 0 50 C-30 50 -54 34 -54 4 C-54 -24 -34 -48 0 -48 Z",
        "M0 -50 C20 -50 26 -30 30 -12 C36 8 48 16 46 34 C42 52 16 54 0 54 C-16 54 -42 52 -46 34 C-48 16 -36 8 -30 -12 C-26 -30 -20 -50 0 -50 Z",
        "M0 -40 C40 -44 62 -22 62 6 C62 34 36 48 0 48 C-36 48 -62 34 -62 6 C-62 -22 -40 -44 0 -40 Z",
        "M0 -30 C10 -54 54 -50 54 -14 C54 18 20 38 0 54 C-20 38 -54 18 -54 -14 C-54 -50 -10 -54 0 -30 Z",
        "M0 -52 C26 -40 50 -14 44 18 C40 44 18 54 0 54 C-18 54 -40 44 -44 18 C-50 -14 -26 -40 0 -52 Z",
        "M-30 -40 C-6 -52 6 -52 30 -40 C56 -26 58 22 34 42 C16 54 -16 54 -34 42 C-58 22 -56 -26 -30 -40 Z",
    ]
    stem_y = [-46, -48, -40, -32, -48, -44]
    swirl = "".join(f'<path d="M{x} {y} a4 4 0 1 1 8 0 a8 8 0 1 1 -16 0"/>' for x, y in
                    ((-28, -20), (8, -30), (30, -4), (-8, 2), (-36, 14), (14, 26), (-14, 34), (44, 22), (-48, -8)))
    defs = ('<defs><radialGradient id="shade" cx=".32" cy=".28" r=".85"><stop offset="0" stop-color="#fff" stop-opacity=".5"/>'
            '<stop offset=".45" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".32"/></radialGradient>'
            f'<g id="sw" fill="none" stroke-width="3" stroke-linecap="round">{swirl}</g>'
            '<g id="stem"><path d="M0 0 q-2 -16 8 -22 q12 -6 14 4 q0 8 -8 6 q-5 -2 -2 -6" fill="none" stroke="#3f7d3a" stroke-width="6" stroke-linecap="round"/>'
            '<path d="M-2 -6 q-20 -12 -30 2 q16 10 30 -2 Z" fill="#57a64a" stroke="#2f5f2c" stroke-width="2"/></g>'
            + "".join(f'<path id="f{i}" d="{d}"/><clipPath id="k{i}"><use href="#f{i}"/></clipPath>' for i, d in enumerate(shapes))
            + "</defs>")
    style = """
.fl{animation:fl 4s ease-in-out infinite}
@keyframes fl{0%,100%{transform:translateY(0) rotate(-5deg)}50%{transform:translateY(-5px) rotate(5deg)}}
.sp{animation:sp 2.6s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
@keyframes sp{0%,100%{transform:scale(0)}50%{transform:scale(1)}}
"""
    rnd = random.Random(11)
    body = defs + otext(40, 56, "DEVIL FRUIT ENCYCLOPEDIA", 30, "#e63946")
    body += f'<text x="1160" y="52" text-anchor="end" font-size="14" font-style="italic" font-weight="700" fill="#6b4a22">every fruit my crew has eaten, and the power it grants</text>'
    n = 0
    for c, (kind, sub, fruits) in enumerate(groups):
        x0 = 40 + c * 380
        body += (f'<path d="M{x0} 76 h350 l-10 17 l10 17 h-350 l10 -17 Z" fill="{STRAW}" stroke="{INK}" stroke-width="2.5"/>'
                 f'<text x="{x0 + 22}" y="100" font-size="19" font-weight="900" fill="{INK}" style="font-family:{HEAVY}" letter-spacing="2">{kind}</text>'
                 f'<text x="{x0 + 330}" y="99" text-anchor="end" font-size="13" font-style="italic" font-weight="700" fill="{INK}">{sub}</text>')
        if c:
            body += f'<path d="M{x0 - 15} 84 V528" stroke="{INK}" stroke-width="1.2" stroke-dasharray="3 6" opacity=".6"/>'
        for r, (tool, fruit, power, col) in enumerate(fruits):
            y = 152 + r * 66
            k = (n * 5 + c) % len(shapes)
            body += f'''<ellipse cx="{x0 + 36}" cy="{y + 27}" rx="20" ry="3.5" fill="{INK}" opacity=".22"/>
<g transform="translate({x0 + 36} {y})"><g class="fl" style="animation-delay:-{rnd.uniform(0, 4):.1f}s"><g transform="scale(.44)">
<use href="#f{k}" fill="{col}"/><use href="#sw" stroke="{_shade(col)}" clip-path="url(#k{k})"/><use href="#f{k}" fill="url(#shade)"/>
<use href="#f{k}" fill="none" stroke="{INK}" stroke-width="4"/><use href="#stem" y="{stem_y[k]}"/></g></g></g>
<path class="sp" style="animation-delay:{rnd.uniform(0, 2.6):.1f}s" d="M{x0 + 64} {y - 26} l2 5 l5 2 l-5 2 l-2 5 l-2 -5 l-5 -2 l5 -2 Z" fill="#ff9f1c" stroke="{INK}" stroke-width=".7"/>
<text x="{x0 + 80}" y="{y - 6}" font-size="18" font-weight="700" fill="{INK}">{tool}</text>
<text x="{x0 + 345}" y="{y - 6}" text-anchor="end" font-size="13" font-style="italic" font-weight="700" fill="#a12a1e">{fruit}</text>
<text x="{x0 + 80}" y="{y + 13}" font-size="13.5" font-style="italic" fill="#6b4a22">{power}</text>'''
            if r < 5:
                body += f'<path d="M{x0 + 80} {y + 30} H{x0 + 345}" stroke="{INK}" stroke-width="1" stroke-dasharray="2 5" opacity=".4"/>'
            n += 1
    body += f'<text x="600" y="556" text-anchor="middle" font-size="14" font-style="italic" font-weight="700" fill="#6b4a22">also aboard: Anaconda · Jupyter · VS Code · Power Automate</text>'
    save("crew-fruits.svg", svg(1200, 580, style, body))


# ───────────────────────── sagas ─────────────────────────
def sagas():
    style = """
.pn{animation:pn 10s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
@keyframes pn{0%,20%,100%{transform:scale(1)}8%{transform:scale(1.045) rotate(-.6deg)}}
.air{animation:air 1.2s steps(1) infinite}
@keyframes air{0%{opacity:1}55%{opacity:.25}}
.march{stroke-dasharray:10 9;animation:mr 1.2s linear infinite}
@keyframes mr{to{stroke-dashoffset:-19}}
.sail{animation:sl 10s ease-in-out infinite}
@keyframes sl{0%{transform:translateX(172px)}22%,25%{transform:translateX(172px)}47%,50%{transform:translateX(457px)}72%,75%{transform:translateX(742px)}97%,100%{transform:translateX(1027px)}}
.bob{animation:bob 1.6s ease-in-out infinite}
@keyframes bob{0%,100%{transform:rotate(-5deg)}50%{transform:rotate(5deg)}}
"""
    icons = [
        f'<g fill="none" stroke="{INK}" stroke-width="2.5"><ellipse rx="30" ry="11"/><ellipse rx="30" ry="11" transform="rotate(60)"/><ellipse rx="30" ry="11" transform="rotate(-60)"/></g><circle r="6" fill="#e63946" stroke="{INK}" stroke-width="2"/>',
        f'<path d="M-9 -30 h18 M-6 -30 v18 l-18 34 q-4 10 8 10 h32 q12 0 8 -10 l-18 -34 v-18" fill="#fffaf0" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/><path d="M-17 8 h34 l7 14 q3 8 -6 8 h-36 q-9 0 -6 -8 Z" fill="#ff9f1c" stroke="{INK}" stroke-width="2"/><circle cx="-3" cy="18" r="3" fill="#fff"/><circle cx="8" cy="12" r="2" fill="#fff"/>',
        f'<rect x="-34" y="-12" width="68" height="34" rx="8" fill="#fff3d1" stroke="{INK}" stroke-width="2.5"/><path d="M-34 10 h68 v4 q0 8 -8 8 h-52 q-8 0 -8 -8 Z" fill="#e63946" stroke="{INK}" stroke-width="2"/><g fill="#9be7f5" stroke="{INK}" stroke-width="1.5"><rect x="-28" y="-6" width="13" height="12" rx="2"/><rect x="-11" y="-6" width="13" height="12" rx="2"/><rect x="6" y="-6" width="13" height="12" rx="2"/></g><circle cx="-18" cy="24" r="6" fill="#222"/><circle cx="18" cy="24" r="6" fill="#222"/><path d="M4 -40 l-10 14 h8 l-4 12 l14 -18 h-8 Z" fill="#ffd23f" stroke="{INK}" stroke-width="1.8"/>',
        f'<path d="M-26 0 Q-26 -24 0 -24 Q26 -24 26 0 Z" fill="#8b5a2b" stroke="{INK}" stroke-width="2.5"/><rect x="-26" y="0" width="52" height="26" rx="3" fill="#a0672f" stroke="{INK}" stroke-width="2.5"/><path d="M-13 -21 V26 M13 -21 V26" stroke="{STRAW}" stroke-width="6"/><text x="0" y="-32" text-anchor="middle" font-size="26" font-weight="900" fill="#e63946" style="font-family:{HEAVY}">?</text>',
    ]
    data = [("EAST BLUE SAGA", "Physics Engineering", "Universidad Tecnológica de Pereira", STRAW, "COMPLETED", "#6b4a22"),
            ("GRAND LINE SAGA", "Data &amp; AI Engineer", "R&amp;D&amp;I · Integra S.A.", "#ff9f1c", "ON AIR", "#a12a1e"),
            ("NEW WORLD SAGA", "M.Sc. + Megabús research", "Minciencias scholarship · UTP", "#ff6b6b", "ON AIR", "#a12a1e"),
            ("FINAL SAGA", "Open-source release", "to be continued…", "#3b2a1a", "COMING SOON", "#6b4a22")]
    panels = ""
    for i, (saga, t1, t2, col, tag, tagc) in enumerate(data):
        x = 40 + i * 285
        tc = CREAM if col == "#3b2a1a" else INK
        blink = ' class="air"' if tag == "ON AIR" else ""
        panels += f'''<g class="pn" style="animation-delay:{i * 2.5}s">
<rect x="{x + 5}" y="77" width="265" height="186" fill="{INK}" opacity=".3"/>
<rect x="{x}" y="72" width="265" height="186" fill="#fdf8ea" stroke="{INK}" stroke-width="3"/>
<rect x="{x}" y="72" width="265" height="34" fill="{col}" stroke="{INK}" stroke-width="3"/>
<text x="{x + 132}" y="96" text-anchor="middle" font-size="17" font-weight="900" fill="{tc}" style="font-family:{HEAVY}" letter-spacing="1">{saga}</text>
<g transform="translate({x + 132} 152)">{icons[i]}</g>
<text x="{x + 132}" y="212" text-anchor="middle" font-size="17" font-weight="700" fill="{INK}">{t1}</text>
<text x="{x + 132}" y="230" text-anchor="middle" font-size="12.5" font-style="italic" fill="#6b4a22">{t2}</text>
<g{blink}><rect x="{x + 259 - len(tag) * 8.4 - 12:.0f}" y="112" width="{len(tag) * 8.4 + 12:.0f}" height="18" rx="3" fill="#fdf8ea" stroke="{tagc}" stroke-width="2"/>
<text x="{x + 259 - (len(tag) * 8.4 + 12) / 2:.0f}" y="125" text-anchor="middle" font-size="10.5" font-weight="700" fill="{tagc}" letter-spacing="1">{tag}</text></g></g>'''
    stops = "".join(f'<circle cx="{172 + i * 285}" cy="292" r="7" fill="{STRAW}" stroke="{INK}" stroke-width="2.5"/>' for i in range(4))
    body = f'''{otext(40, 52, "THE SAGAS SO FAR", 30, "#e63946")}
<text x="1160" y="50" text-anchor="end" font-size="14" font-style="italic" font-weight="700" fill="#6b4a22">one arc at a time, like any good 1,100-chapter story</text>
{panels}
<path class="march" d="M60 292 H1140" fill="none" stroke="{RED}" stroke-width="3.5" stroke-linecap="round"/>{stops}
<g class="sail"><g transform="translate(0 286)"><g class="bob"><g transform="scale(.55)">{SMALL_SHIP}</g></g></g></g>'''
    save("sagas.svg", svg(1200, 322, style, body))


if __name__ == "__main__":
    header(); footer(); current_arc(); crew_flag(); news(); chest(); poneglyph(); dividers()
    crew_fruits(); sagas()
