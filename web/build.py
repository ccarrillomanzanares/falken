#!/usr/bin/env python3
"""Genera la web de Falken (ccmai.org/falken/) a partir de los .md del repo.

Uso: python3 build.py [DESTINO]   (por defecto /var/www/ccmai.org/falken)
"""
import html, re, shutil, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "/var/www/ccmai.org/falken")
GITHUB = "https://github.com/ccarrillomanzanares/falken"

HEX = ('<svg viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg">'
       '<polygon points="50,4 92,30 92,86 50,112 8,86 8,30" fill="#001100" stroke="#00ff00" stroke-width="8"/>'
       '<circle cx="50" cy="58" r="16" fill="#00ff00" opacity="0.9"/></svg>')

LANGS = {
    "en": dict(src="MANIFESTO.md", dir="", root="./",
               title="Falken — the agent-native application profile",
               desc="An open standard for applications that AI agents use on the user's behalf. A profile on top of MCP.",
               tagline="the agent-native application profile",
               phrase="Capabilities before screens. Intent first, interface on demand.",
               status="Draft manifesto · October 2026 · spec v0.1 in progress",
               read="Read the manifesto", repo="GitHub", issues="Ideas & objections",
               foot="Manifesto under CC BY 4.0",
               locale="en_US", og_alt="Falken: the agent-native application profile, an open standard on top of MCP"),
    "es": dict(src="MANIFIESTO.md", dir="es/", root="../",
               title="Falken — el perfil de las aplicaciones nativas de agente",
               desc="Un estándar abierto para las aplicaciones que los agentes de IA usan en nombre del usuario. Un perfil sobre MCP.",
               tagline="el perfil de las aplicaciones nativas de agente",
               phrase="Capacidades antes que pantallas. Intención primero, interfaz bajo demanda.",
               status="Borrador del manifiesto · octubre de 2026 · especificación v0.1 en curso",
               read="Leer el manifiesto", repo="GitHub", issues="Ideas y objeciones",
               foot="Manifiesto con licencia CC BY 4.0",
               locale="es_ES", og_alt="Falken: el perfil de las aplicaciones nativas de agente, un estándar abierto sobre MCP"),
}


def render(md_path, lang):
    body = subprocess.run(["pandoc", "-f", "gfm", "-t", "html5", str(md_path)],
                          check=True, capture_output=True, text=True).stdout
    # Bloques mermaid: <pre class="mermaid"><code>…</code></pre> -> <pre class="mermaid">…</pre>
    body = re.sub(r'<pre class="mermaid"><code>(.*?)</code></pre>',
                  r'<pre class="mermaid">\1</pre>', body, flags=re.S)
    # Enlaces entre idiomas y al resto del repo
    body = body.replace('href="MANIFIESTO.md"', 'href="' + LANGS[lang]["root"] + 'es/"')
    body = body.replace('href="MANIFESTO.md"', 'href="' + LANGS[lang]["root"] + '"')
    body = body.replace('href="LICENSE"', f'href="{GITHUB}/blob/main/LICENSE"')
    body = re.sub(r'<a href="(https?://)', r'<a target="_blank" rel="noopener" href="\1', body)
    return body


def page(lang):
    L = LANGS[lang]
    other = "es" if lang == "en" else "en"
    url = f"https://ccmai.org/falken/{L['dir']}"
    body = render(REPO / L["src"], lang)
    nav = "".join(
        f'<a href="{L["root"]}{LANGS[k]["dir"]}" class="{"on" if k == lang else ""}" hreflang="{k}">{k.upper()}</a>'
        for k in LANGS)
    e = html.escape
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(L['title'])}</title>
<meta name="description" content="{e(L['desc'])}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="CCMAI">
<meta property="og:locale" content="{L['locale']}">
<meta property="og:title" content="{e(L['title'])}">
<meta property="og:description" content="{e(L['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://ccmai.org/falken/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(L['og_alt'])}">
<meta name="twitter:card" content="summary_large_image">
<link rel="alternate" hreflang="{other}" href="https://ccmai.org/falken/{LANGS[other]['dir']}">
<link rel="icon" type="image/svg+xml" href="{L['root']}hex.svg">
<link rel="stylesheet" href="{L['root']}style.css">
</head>
<body>
<div class="screen">
<div class="term-bar"><span class="path">falken@ccmai — /falken/{L['dir']}</span><span>{nav}<a href="{GITHUB}" target="_blank" rel="noopener">GitHub</a></span></div>
<header class="hero">
<span class="hex">{HEX}</span>
<h1>FALKEN</h1>
<p class="tagline">{e(L['tagline'])}</p>
<p class="phrase">&gt; {e(L['phrase'])} <span class="cursor"></span></p>
<div class="actions">
<a class="btn" href="#manifesto">{e(L['read'])}</a>
<a class="btn" href="{GITHUB}" target="_blank" rel="noopener">{e(L['repo'])}</a>
<a class="btn" href="{GITHUB}/issues" target="_blank" rel="noopener">{e(L['issues'])}</a>
</div>
<p class="status">{e(L['status'])}</p>
</header>
<main id="manifesto">
{body}
</main>
<div class="term-foot"><span>{e(L['foot'])} · <a href="https://ccmai.org/">CCMAI</a> · <a href="/aios/">aios</a> · <a href="/kai/">kai</a> · <a href="/miuzika/">miuzika</a></span><span>Professor Falken · WarGames (1983)</span></div>
</div>
<script type="module">
if (document.querySelector('pre.mermaid')) {{
  const {{ default: mermaid }} = await import('https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs');
  mermaid.initialize({{ startOnLoad: true, theme: 'base', themeVariables: {{
    background: '#000600', primaryColor: '#001a00', primaryTextColor: '#33ff33',
    primaryBorderColor: '#00ff00', lineColor: '#00aa00', clusterBkg: '#000a00',
    clusterBorder: '#006400', titleColor: '#00ff00', edgeLabelBackground: '#001100',
    fontFamily: 'Consolas, Menlo, DejaVu Sans Mono, monospace' }} }});
}}
</script>
</body>
</html>
"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for lang, L in LANGS.items():
        d = OUT / L["dir"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(page(lang), encoding="utf-8")
    shutil.copy(HERE / "style.css", OUT / "style.css")
    shutil.copy(HERE / "og.png", OUT / "og.png")  # se regenera con make_og.py
    (OUT / "hex.svg").write_text(HEX, encoding="utf-8")
    print(f"OK -> {OUT}")


if __name__ == "__main__":
    main()
