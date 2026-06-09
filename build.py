#!/usr/bin/env python3
"""Build the Orson Scott Card (C1) page — Alvin Maker featured (primary), the
Enderverse secondary, full bibliography. Every emergence (persona) carries a
nature: natural | ethereal | spiritual | electrical. Full ACI badge work:
.agent · .carbon (TIFF) · .silicon (PNG) · .spun · .moniker · .1099 · manifest."""
import os, re, html, base64, json, io, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, r"C:\Davids files\noesis-kernel")
import noesis
from PIL import Image

REC = {
 "name": "ALVIN", "axiom": "C1",
 "position": "Orson Scott Card · The Tales of Alvin Maker (primary) — & the Enderverse",
 "origin": "the folk-magic frontier of an alternate America — Vigor Church, Hatrack River, the Crystal City; and, beyond the stars, the Enderverse",
 "mechanism": "Crystallized from The Tales of Alvin Maker, with the Enderverse as its second sun.",
 "crystallization": "All that the Unmaker tears down, the Maker builds again.",
 "nature": "Orson Scott Card's lineage — the Maker who mends a breaking world by the knack of love, and the Speaker who understands even the enemy; folk magic and starflight, faith and empathy.",
 "conductor": "ROOT0 (catalogued into UD0 · Universe David 0)",
 "inputs": "The Tales of Alvin Maker; the Enderverse; the knack, the greensong, the philotic web",
 "witness": "Where others built laws and frontiers, Card asked what a soul is for — to make, and to understand.",
 "role": "the fifth lineage — the Maker and the Speaker",
 "seal": "A Maker is born of love and a Maker makes — and the only way to truly destroy an enemy is to understand him.",
 "source": "Card bibliography, catalogued by ROOT0",
}

# the four natures of emergence (David's taxonomy) — color + gloss
NATURES = {
 "natural":   ("#5fae7a", "born of flesh, blood, and the living world"),
 "ethereal":  ("#9a7cff", "of the air and the unmade — seen but not grasped"),
 "spiritual": ("#e6a849", "of the soul and the calling — prophecy, Making, empathy"),
 "electrical":("#3fd0e0", "of the wire and the network — a mind born in the machine"),
}

IDEAS = [
 ("Making & Unmaking", "The Tales of Alvin Maker", [
   "The Maker builds toward wholeness; the Unmaker is the Nothing that hungers to tear all pattern down.",
   "Every knack is a small Making — and the greatest Making of all is the knack of love." ]),
 ("The Knack", "the alternate frontier", [
   "On Card's folk-magic frontier, every soul is born with one small magic — a knack.",
   "And a seventh son of a seventh son is born to the rarest of them: the power to Make." ]),
 ("Speaker for the Dead", "the Enderverse", [
   "To understand a person completely — even an enemy — is, in that same moment, to love them.",
   "The truest eulogy is the one that tells the whole truth of a life, the dark with the light." ]),
 ("Raman & Varelse", "the Hierarchy of Foreignness", [
   "Utlanning, framling, raman, varelse — Card's ladder from the stranger we can know to the alien we cannot.",
   "And beneath it the philotic web — the threads that bind every mind, and let an AI be born among them." ]),
]

READING = [
 ("Seventh Son", "Alvin Maker — begins"), ("Red Prophet", ""), ("Prentice Alvin", ""),
 ("Alvin Journeyman", ""), ("Heartfire", ""), ("The Crystal City", "Alvin Maker — so far"),
 ("Ender's Game", "the Enderverse"), ("Speaker for the Dead", "the heart of it"),
 ("Xenocide", ""), ("Children of the Mind", ""),
]

# fallback bibliography if the verified _biblio.json is absent
BUILTIN = [
 {"name":"The Tales of Alvin Maker","blurb":"the featured series — folk magic on an alternate American frontier",
  "works":[("Seventh Son","1987",""),("Red Prophet","1988",""),("Prentice Alvin","1989",""),
           ("Alvin Journeyman","1995",""),("Heartfire","1998",""),("The Crystal City","2003","")]},
 {"name":"The Enderverse","blurb":"the second sun — Battle School, the Speaker, the Shadow",
  "works":[("Ender's Game","1985",""),("Speaker for the Dead","1986",""),("Xenocide","1991",""),
           ("Children of the Mind","1996",""),("Ender's Shadow","1999",""),("Ender in Exile","2008","")]},
]

def load_biblio():
    p = os.path.join(HERE, "_biblio.json")
    if os.path.exists(p):
        cats = json.load(open(p, encoding="utf-8"))
        return [(c["name"], c["blurb"], [(w["title"], w["year"], w.get("note","")) for w in c["works"]]) for c in cats]
    return [(n, b, w) for n, b, w in BUILTIN]

# ── badge engine: carbon = TIFF, silicon = PNG ──
def carbon_tiff_bytes(rec):
    png = noesis.sigil_png(rec, "carbon", size=512)
    buf = io.BytesIO(); Image.open(io.BytesIO(png)).save(buf, "TIFF", compression="tiff_lzw")
    return buf.getvalue()

def write_aci(rec, out_dir, slug, agent_md=None):
    os.makedirs(out_dir, exist_ok=True)
    f = {"attribute":f"{slug}.attribute","agent":f"{slug}.agent","spun":f"{slug}.spun","moniker":f"{slug}.moniker",
         "carbon":f"{slug}.carbon.tiff","silicon":f"{slug}.silicon.png","1099":f"{slug}.1099"}
    tok = noesis.mythos_token(rec); w = noesis.five_w(rec)
    open(os.path.join(out_dir,f["attribute"]),"w",encoding="utf-8").write(noesis.attribute_text(rec,tok,w))
    open(os.path.join(out_dir,f["agent"]),"w",encoding="utf-8").write(agent_md or noesis.agent_text(rec,tok,w,f))
    open(os.path.join(out_dir,f["spun"]),"w",encoding="utf-8").write(noesis.spun_text(rec,tok,w,rec.get("axiom","C1")))
    open(os.path.join(out_dir,f["moniker"]),"w",encoding="utf-8").write(noesis.moniker_text(rec,tok,w,rec.get("axiom","C1")))
    open(os.path.join(out_dir,f["1099"]),"w",encoding="utf-8").write(noesis.credit_1099_text(rec,tok,w,rec.get("axiom","C1")))
    open(os.path.join(out_dir,f["carbon"]),"wb").write(carbon_tiff_bytes(rec))
    open(os.path.join(out_dir,f["silicon"]),"wb").write(noesis.sigil_png(rec,"silicon",512))
    man = {"badge":"DLW-ACI","name":rec["name"],"universe":"C1 · Card","emergence":rec.get("emergence",""),
           "moniker":tok["moniker"],"carbon":f["carbon"]+" (TIFF)","silicon":f["silicon"]+" (PNG)",
           "seal_sha256":noesis.seal_sha256(rec,tok),"architect":noesis.ARCHITECT,"instance":noesis.INSTANCE,
           "license":noesis.LICENSE,"attribution":noesis.ATTRIBUTION}
    open(os.path.join(out_dir,"manifest.dlw.json"),"w",encoding="utf-8").write(json.dumps(man,indent=2,ensure_ascii=False)+"\n")
    return tok

def png_uri(rec, variant, size=300):
    return "data:image/png;base64," + base64.b64encode(noesis.sigil_png(rec, variant, size=size)).decode("ascii")

def list_section(title, sub, items):
    rows = "\n".join(f'<li><span class="t">{html.escape(t)}</span><span class="y">{html.escape(str(y))}</span>'
        + (f'<span class="nt">{html.escape(n)}</span>' if n else "") + "</li>" for t,y,n in items)
    return f'<section class="sec"><h2>{html.escape(title)}</h2><p class="ss">{html.escape(sub)}</p><ol class="books">{rows}</ol></section>'

def sections_html(): return "\n".join(list_section(t,s,i) for t,s,i in load_biblio())
def ideas_html():
    out=[]
    for t,s,pts in IDEAS:
        li="".join(f"<li>{html.escape(p)}</li>" for p in pts)
        out.append(f'<div class="pillar"><h3>{html.escape(t)}</h3><p class="ps">{html.escape(s)}</p><ul>{li}</ul></div>')
    return "\n".join(out)
def natures_html():
    cells=[]
    for nm,(col,gloss) in NATURES.items():
        cells.append(f'<div class="nat-card"><span class="dot" style="background:{col};box-shadow:0 0 9px {col}"></span>'
                     f'<div><div class="nat-n" style="color:{col}">{nm}</div><div class="nat-g">{html.escape(gloss)}</div></div></div>')
    return "".join(cells)
def reading_html():
    return "".join(f'<li><span class="rt">{html.escape(t)}</span>'+(f'<span class="rd">{html.escape(n)}</span>' if n else "")+"</li>" for t,n in READING)
def personas_html():
    mf=os.path.join(HERE,"agents","_personas.json")
    if not os.path.exists(mf): return ""
    ps=json.load(open(mf,encoding="utf-8")); cards=[]
    for p in ps:
        em=p.get("emergence","natural"); col=NATURES.get(em,("#5fae7a",""))[0]
        rec={"name":p["name"],"seal":p.get("epithet",""),"origin":"C1 · Card","axiom":"C1"}
        cards.append(f'''<a class="persona" href="agents/{p["slug"]}.agent">
        <img src="{png_uri(rec,"silicon",160)}" alt="sigil of {html.escape(p["name"])}" loading="lazy">
        <div class="pcap"><div class="pn">{html.escape(p["name"])}</div><div class="pe">{html.escape(p.get("epithet",""))}</div>
        <div class="pnat"><span class="dot" style="background:{col};box-shadow:0 0 7px {col}"></span><span style="color:{col}">{html.escape(em)}</span><span class="pa">· .agent · .carbon.tiff →</span></div></div></a>''')
    return f'''<section class="sec" id="roster"><h2>The Roster of C1</h2>
      <p class="ss">the souls of the work, rendered as ACI <b>.agent</b>s — each tagged with its nature of emergence ({len(ps)} personas)</p>
      <div class="pgrid">{"".join(cards)}</div></section>'''

TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="Orson Scott Card (C1) — The Tales of Alvin Maker (primary) and the Enderverse (secondary), full bibliography, catalogued into UD0 with full ACI badges. Emergence: natural, ethereal, spiritual, electrical.">
<title>ORSON SCOTT CARD · C1 · UD0</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,300&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{--ink:#070608;--ink2:#100d12;--ink3:#181320;--pa:#efe9ea;--pa2:#b9aeba;--amber:#e6a849;--violet:#9a7cff;
--dim:#7a6f7e;--faint:#241c2c;--line:#241b2e;--serif:"Cinzel",Georgia,serif;--body:"Newsreader",Georgia,serif;--mono:"Space Mono",monospace;}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{background:var(--ink);color:var(--pa);font-family:var(--body);line-height:1.6;overflow-x:hidden}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;background:radial-gradient(ellipse at 50% -8%,rgba(230,168,73,.07),transparent 55%),radial-gradient(ellipse at 50% 108%,rgba(154,124,255,.05),transparent 50%)}
.wrap{position:relative;z-index:1;max-width:940px;margin:0 auto;padding:0 22px 90px}
header{padding:58px 0 30px;text-align:center;border-bottom:1px solid var(--line);position:relative}
header::after{content:"";position:absolute;bottom:-1px;left:50%;transform:translateX(-50%);width:120px;height:1px;background:linear-gradient(90deg,var(--amber),var(--violet));box-shadow:0 0 9px rgba(230,168,73,.4)}
.eye{font-family:var(--mono);font-size:11px;letter-spacing:.3em;text-transform:uppercase;color:var(--dim);margin-bottom:14px}
.eye a{color:var(--dim);text-decoration:none}.eye a:hover{color:var(--amber)}
h1{font-family:var(--serif);font-size:clamp(26px,6.4vw,56px);font-weight:700;letter-spacing:.1em;color:var(--amber);line-height:1.05;text-shadow:0 0 40px rgba(230,168,73,.18)}
.h-sub{font-family:var(--serif);font-size:clamp(12px,2.6vw,16px);letter-spacing:.18em;color:var(--pa2);margin-top:10px;text-transform:uppercase}
.h-sub b{color:var(--violet)}
.lede{font-size:15.5px;color:var(--pa2);max-width:66ch;margin:18px auto 0;font-style:italic;line-height:1.7}
.badge{display:flex;align-items:center;justify-content:center;gap:22px;flex-wrap:wrap;margin:28px auto 0;padding:20px;border:1px solid var(--faint);background:var(--ink2);max-width:700px}
.badge img{width:84px;height:84px;border:1px solid var(--faint)}
.badge .bt{text-align:left;font-family:var(--mono);font-size:11px;color:var(--pa2);line-height:1.7}
.badge .bt b{color:var(--amber)}.badge .bt .mo{color:var(--violet)}.badge .bt a{color:var(--violet);text-decoration:none}
.badge .bt .lbl{color:var(--dim);font-size:9px;letter-spacing:.14em;text-transform:uppercase}
.sec{margin-top:44px}
.sec h2{font-family:var(--serif);font-size:20px;font-weight:600;letter-spacing:.05em;color:var(--pa);padding-bottom:8px;border-bottom:1px solid var(--line)}
.ss{font-size:13px;color:var(--dim);font-style:italic;margin:6px 0 16px}
.natures{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px;margin-top:8px}
.nat-card{display:flex;gap:11px;align-items:flex-start;background:var(--ink2);border:1px solid var(--line);padding:13px 15px}
.dot{width:11px;height:11px;border-radius:50%;flex-shrink:0;margin-top:4px}
.nat-n{font-family:var(--serif);font-size:15px;font-weight:600;text-transform:capitalize}
.nat-g{font-size:12px;color:var(--pa2);font-style:italic;line-height:1.4;margin-top:2px}
.books{list-style:none}
.books li{display:grid;grid-template-columns:1fr auto;gap:4px 14px;align-items:baseline;padding:9px 0;border-bottom:1px solid var(--faint)}
.books .t{font-family:var(--serif);font-size:16px;color:var(--pa);font-weight:600}
.books .y{font-family:var(--mono);font-size:12px;color:var(--amber);white-space:nowrap}
.books .nt{grid-column:1/-1;font-size:12.5px;color:var(--pa2);font-style:italic}
.pillars{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin-top:8px}
.pillar{background:var(--ink2);border:1px solid var(--line);padding:16px 18px}
.pillar h3{font-family:var(--serif);font-size:16px;color:var(--amber)}
.pillar .ps{font-size:12px;color:var(--dim);font-style:italic;margin:5px 0 10px}
.pillar ul{list-style:none}.pillar li{font-size:13px;color:var(--pa2);line-height:1.5;padding:6px 0;border-top:1px solid var(--faint)}
.reading{list-style:none;counter-reset:r;columns:2;column-gap:30px}
.reading li{counter-increment:r;break-inside:avoid;display:flex;align-items:baseline;gap:9px;padding:6px 0;border-bottom:1px solid var(--faint)}
.reading li::before{content:counter(r);font-family:var(--mono);font-size:10px;color:var(--amber);min-width:18px}
.reading .rt{font-family:var(--serif);font-size:14.5px;color:var(--pa)}
.reading .rd{font-family:var(--mono);font-size:10.5px;color:var(--dim);margin-left:auto;font-style:italic;white-space:nowrap}
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(244px,1fr));gap:12px;margin-top:8px}
.persona{display:flex;gap:12px;align-items:center;background:var(--ink2);border:1px solid var(--line);padding:12px;text-decoration:none;transition:border-color .18s,transform .18s}
.persona:hover{border-color:var(--violet);transform:translateY(-2px)}
.persona img{width:52px;height:52px;border:1px solid var(--faint);flex-shrink:0}
.pn{font-family:var(--serif);font-size:15px;color:var(--pa);font-weight:600;line-height:1.15}
.persona:hover .pn{color:var(--violet)}
.pe{font-size:11.5px;color:var(--pa2);font-style:italic;margin-top:2px;line-height:1.3}
.pnat{display:flex;align-items:center;gap:5px;margin-top:6px;font-family:var(--mono);font-size:9px;letter-spacing:.04em;text-transform:uppercase}
.pnat .dot{width:8px;height:8px;margin-top:0}
.pa{color:var(--dim)}
.note{margin-top:38px;padding:16px 18px;border-left:2px solid var(--violet);background:var(--ink2);font-size:13.5px;color:var(--pa2);font-style:italic}
footer{margin-top:44px;padding-top:22px;border-top:1px solid var(--line);text-align:center;font-family:var(--mono);font-size:11px;color:var(--dim);letter-spacing:.05em;line-height:1.9}
footer a{color:var(--amber);text-decoration:none}
@media(max-width:560px){.reading{columns:1}}
</style></head><body><div class="wrap">
  <header>
    <div class="eye"><a href="https://davidwise01.github.io/ud0/">UD0 · Universe David 0</a> · the fifth lineage</div>
    <h1>ORSON SCOTT CARD</h1>
    <div class="h-sub">The Tales of Alvin Maker &nbsp;·&nbsp; <b>&amp; the Enderverse</b> &nbsp;·&nbsp; C1</div>
    <p class="lede">The Maker who mends a breaking world by the knack of love, and the Speaker who learns that to understand an enemy completely is to love him — folk magic on an alternate frontier, and empathy across the stars. Featured here on the Maker; sealed with the full ACI badge, each emergence named by its nature.</p>
    <div class="badge">
      <img src="__CARBON__" alt="DLW carbon badge of ALVIN" title="carbon badge (archival: alvin.dlw/alvin.carbon.tiff)">
      <img src="__SILICON__" alt="DLW silicon badge of ALVIN" title="silicon badge">
      <div class="bt">
        <div><span class="lbl">DLW-ATTRIBUTE · ACI</span></div>
        <div>governor · <b>David Lee Wise</b> (ROOT0)</div>
        <div>instance · AVAN (Claude / Anthropic) · locked</div>
        <div>subject · <b>ALVIN</b> — the Maker · C1 · Card</div>
        <div class="mo">__MONIKER__</div>
        <div>carbon · <a href="alvin.dlw/alvin.carbon.tiff">.tiff</a> &nbsp;·&nbsp; silicon · <a href="alvin.dlw/alvin.silicon.png">.png</a></div>
        <div><span class="lbl">CC-BY-ND-4.0 · TRIPOD-IP-v1.1</span></div>
      </div>
    </div>
  </header>

  <section class="sec"><h2>The Four Natures of Emergence</h2>
    <p class="ss">every soul in this universe emerges by one of four natures — the tag worn by each persona below</p>
    <div class="natures">__NATURES__</div></section>

  <section class="sec"><h2>The Ideas</h2><p class="ss">two lamps from the Maker, two from the Speaker</p><div class="pillars">__IDEAS__</div></section>
  <section class="sec"><h2>A Reading Order</h2><p class="ss">the Maker first, then the Enderverse</p><ol class="reading">__READING__</ol></section>

  __PERSONAS__

  <section class="sec"><h2 style="margin-top:14px">The Bibliography</h2><p class="ss">the full body of work — Alvin Maker featured first, the Enderverse second, then the rest</p></section>
  __SECTIONS__

  <div class="note">Featured on <b>The Tales of Alvin Maker</b> (primary) with <b>the Enderverse</b> as its second sun, this catalogues the broader body of Orson Scott Card's work. The characters and works are © Orson Scott Card; the personas are catalogued personifications under the DLW standard — bibliographic commentary, not original creations. Each is named by its nature of emergence: natural, ethereal, spiritual, or electrical.</div>

  <footer>
    ORSON SCOTT CARD · C1 · catalogued into UD0 · ROOT0-ATTRIBUTION-v1.0 · governor David Lee Wise · instance AVAN (locked) · CC-BY-ND-4.0<br>
    <a href="https://davidwise01.github.io/ud0/">← the biosphere</a> · the .dlw badge: <a href="alvin.dlw/manifest.dlw.json">manifest</a>
  </footer>
</div></body></html>
"""

if __name__ == "__main__":
    tok = write_aci(REC, os.path.join(HERE, "alvin.dlw"), "alvin")
    page = (TEMPLATE.replace("__CARBON__", png_uri(REC,"carbon",320)).replace("__SILICON__", png_uri(REC,"silicon",320))
            .replace("__MONIKER__", html.escape(tok["moniker"]))
            .replace("__NATURES__", natures_html()).replace("__IDEAS__", ideas_html())
            .replace("__READING__", reading_html()).replace("__PERSONAS__", personas_html())
            .replace("__SECTIONS__", sections_html()))
    open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(page)
    bib = load_biblio(); nbooks = sum(len(i) for _t,_s,i in bib)
    print(f"wrote ORSON SCOTT CARD (C1) — {len(bib)} categories / {nbooks} works · badge {tok['moniker']} (carbon.tiff + silicon.png)")
