"""Generates every page of bluetaperigging.com from one set of partials.

Run `python gen.py` after editing copy here; the HTML files are output, not source.
Hard rule from the client: no individual is named anywhere on this site.
"""
import hashlib
import json
from pathlib import Path

from seo_pages import PAGES as SEO

ROOT = Path(__file__).parent


def ver(rel):
    """Content hash for cache busting: assets are served with a one-year expiry."""
    return hashlib.md5((ROOT / rel).read_bytes()).hexdigest()[:10]

SITE = "https://bluetaperigging.com"

YT = {
    "speedrunners-2": "lSgsnMr-JpQ",
    "nicktoons-dice": "MDsGI19Owe8",
    "pudgy-party": "25WQCnAyyC4",
    "schweppes": "2vb4Z2XoHWw",
}
# Stills we don't host yet fall back to YouTube's own thumbnail.
THUMB = {"schweppes": "https://i.ytimg.com/vi/2vb4Z2XoHWw/hqdefault.jpg"}


def head(title, desc, path, extra=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}{path}">
<meta name="theme-color" content="#0a0f17">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}/assets/img/hero-rig.webp">
<link rel="icon" href="/assets/img/favicon.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/space-grotesk-700-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/fonts.css">
<link rel="stylesheet" href="/assets/css/site.css?v={ver("assets/css/site.css")}">
{extra}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def nav(active):
    items = [("services", "Services"), ("work", "Work"), ("approach", "Approach")]
    links = "".join(
        f'<a href="/{slug}/"{" class=\"is-active\" aria-current=\"page\"" if slug == active else ""}>{label}</a>'
        for slug, label in items
    )
    return f"""<header class="nav">
  <div class="wrap nav__in">
    <a class="nav__mark" href="/" aria-label="Bluetape Rigging Studio — home">
      <img class="nav__logo" src="/assets/img/logo.webp" alt="" width="40" height="43">
      <span class="nav__name">BLUETAPE<small>RIGGING STUDIO</small></span>
    </a>
    <button class="nav__toggle" type="button" aria-label="Menu" aria-expanded="false" aria-controls="nav-links"><span></span><span></span><span></span></button>
    <nav class="nav__links" id="nav-links" aria-label="Main">
      {links}
      <a class="btn btn--solid" href="/contact/">Start a project</a>
    </nav>
  </div>
</header>
<main id="main">
"""


CTA = """<section class="cta">
  <div class="wrap cta__in">
    <div data-reveal>
      <span class="kicker">Next step</span>
      <h2>Send us your asset list.</h2>
    </div>
    <div data-reveal="120">
      <p>How many characters, which engine, when it’s due, and what has already gone wrong. We’ll come back with what we think it takes, and whether we’re the right studio for it.</p>
      <div class="btn-row">
        <a class="btn btn--solid" href="/contact/">Start a project <span class="arr">→</span></a>
        <a class="btn" data-mail href="/contact/">Email us</a>
      </div>
    </div>
  </div>
</section>
"""

FOOT = ("""</main>
<footer class="foot">
  <div class="wrap foot__in">
    <div class="foot__brand">
      <a class="nav__mark" href="/"><img class="nav__logo" src="/assets/img/logo.webp" alt="" width="40" height="43"><span class="nav__name">BLUETAPE<small>RIGGING STUDIO</small></span></a>
      <p>Boutique character rigging for VFX, animation and games. Maya and Unreal Engine pipelines, working remotely with studios worldwide.</p>
    </div>
    <div>
      <h4>Studio</h4>
      <ul><li><a href="/services/">Services</a></li><li><a href="/work/">Work</a></li><li><a href="/approach/">Approach</a></li><li><a href="/contact/">Contact</a></li></ul>
    </div>
    <div>
      <h4>Services</h4>
      <ul>""" + "".join(f'<li><a href="/{p["slug"]}/">{p["nav"]}</a></li>' for p in SEO) + """</ul>
    </div>
    <div>
      <h4>Get in touch</h4>
      <ul><li><a data-mail href="/contact/"></a></li><li><a href="/contact/">Start a project</a></li></ul>
    </div>
  </div>
  <div class="wrap foot__base"><span>© 2026 Bluetape Rigging Studio</span><span>Remote · working worldwide</span></div>
</footer>
<script src="/assets/js/site.js?v=""" + ver("assets/js/site.js") + """" defer></script>
</body>
</html>
""")

PLAY = '<span class="play__btn"><svg viewBox="0 0 16 16" aria-hidden="true"><path fill="currentColor" d="M4 2.5v11l9-5.5z"/></svg>Play video</span>'


def trailer(slug, title):
    return f"""<figure class="media">
        <img src="{THUMB.get(slug, f"/assets/img/{slug}.webp")}" alt="{title} — video still" width="1280" height="720" loading="lazy">
        <button class="play" type="button" data-yt="{YT[slug]}" data-title="{title}" aria-label="Play the {title} video">{PLAY}</button>
      </figure>"""


SCHWEPPES = """<figure class="media media--logo">
        <img src="/assets/img/partner-bitt.webp" alt="Bitt Animation" width="297" height="81" loading="lazy">
        <span class="nda">Commercial · no public footage</span>
      </figure>"""

WORK = [
    ("speedrunners-2", "SpeedRunners 2: King of Speed", "Games rigging for Fair Play Labs", "Mutant Tools", "Game-ready pipeline"),
    ("nicktoons-dice", "Nicktoons &amp; The Dice of Destiny", "Rigging and production support for Fair Play Labs", "mGear", "Character setup"),
    ("pudgy-party", "Pudgy Party", "Animal and creature rigging", "Mutant Tools", "Specialised movement"),
    ("schweppes", "Schweppes — “Meet Your Match”", "VFX rigging assistance for Bitt Animation", "Mutant Tools", "Commercial VFX"),
]

SERVICES = [
    ("character", "11", "Character &amp; facial rigging",
     "Model in, animation-ready rig out. Skinning, correctives, facial systems, and controls laid out the way your animators actually work.",
     "Model to animation-ready rig. Skinning, correctives, facial systems, and a control layout designed around how your animators work rather than around how the rig was built.",
     ["Bipeds", "Facial systems", "Correctives", "Skinning", "Cloth setups"], "hero-rig.webp"),
    ("creature", "13", "Creature &amp; animal rigging",
     "Quadrupeds, wings, birds, tails, and spines that refuse to behave — the characters where off-the-shelf autorigs give up.",
     "Quadrupeds, wings, birds, tails, and spines that refuse to behave. Hind legs rigged from the animal’s real skeleton, wings built as a driven fan with per-feather offset, chains layered so animators can hit a specific silhouette on a specific frame.",
     ["Quadrupeds", "Wings &amp; birds", "Tails", "Layered chains"], None),
    ("games", "15", "Game-ready rigs &amp; Unreal",
     "Built to a joint budget agreed up front, exported clean, wired into Control Rig and Blueprints.",
     "Joint budget agreed and split by region before a joint is placed. Export treated as a gate with its own validator — count, orientation, bind pose, naming, morph target names. Control Rig and Blueprint integration where the project needs it.",
     ["Joint budgets", "Control Rig", "Blueprints", "Export validation"], "game-rig.webp"),
    ("overflow", "00", "Overflow on a running show",
     "Your team is full and the asset list isn’t getting shorter. We work inside your pipeline and start with whatever is blocking animation.",
     "Your department is at capacity and the asset list isn’t shrinking. We onboard onto your conventions, start with the assets that unblock animation first, and stay invisible in the credits sense — the rigs look like your rigs.",
     ["Your conventions", "Fast onboarding", "Asset triage"], None),
    ("rescue", "08", "Rig rescue",
     "Deformation failed review, the export broke, someone left. We find what’s actually wrong and fix it without restarting the asset.",
     "Deformation failed review, the export broke, or the person who built it has gone. First pass is diagnostic, not cosmetic: find the actual cause, then stabilise without restarting the asset unless restarting is genuinely cheaper. You get a written account of what was wrong.",
     ["Diagnosis", "Deformation repair", "Export repair", "Handover notes"], None),
    ("tools", "09", "Tools &amp; pipeline",
     "Rigging systems and Python tools built for your studio: a new autorig, adapters for yours, pickers, publish checks. Documented, so it’s yours after we leave.",
     "From a single tool to a complete rigging system designed around your shows: autorigs, adapters for the one you already have, pickers, publish validators, component save and load. Written to your standards and documented so your team owns it when the contract ends.",
     ["Custom autorigs", "Python", "PySide / Qt", "Publish validators"], "code.webp"),
]

STEPS = [
    ("Scope", "You send the asset list, target engine, deadline and conventions. We come back with what we’d do first, the risks, and whether the date is real."),
    ("Definition of done", "What a delivered rig includes, which conventions it follows, how many revision rounds. Agreed in writing before anyone opens Maya."),
    ("Blocking first", "Rough rigs early so animation can start, then deformation passes, then polish. Problems surface while they’re cheap."),
    ("Validated delivery", "Every asset goes through the same publish checks before it reaches you. Failures are loud and specific."),
    ("Handover", "Rig documentation and a walkthrough call. Our work is meant to outlive the contract."),
]


def steps(alt=False):
    items = "".join(
        f'<div class="step" data-reveal="{i*80}"><span class="step__n">{i+1:02d}</span><h3>{t}</h3><p>{p}</p></div>'
        for i, (t, p) in enumerate(STEPS)
    )
    return f'<div class="steps">{items}</div>'


PARTNERS = """<section class="partners" aria-label="Studios we work with">
  <div class="wrap partners__in">
    <span class="partners__label">Studios we’ve rigged for</span>
    <div class="partners__row">
      <img src="/assets/img/partner-fpl.webp" alt="Fair Play Labs" width="166" height="93" loading="lazy">
      <img src="/assets/img/partner-bitt.webp" alt="Bitt Animation" width="297" height="81" loading="lazy">
      <img src="/assets/img/partner-lsp.webp" alt="La Sala Post" width="229" height="120" loading="lazy">
      <img src="/assets/img/partner-futuredeluxe.webp" alt="Future Deluxe" width="89" height="120" loading="lazy">
    </div>
  </div>
</section>
"""

AXIS = """<svg class="vp__axis" viewBox="0 0 34 34" aria-hidden="true"><path d="M6 28h20" stroke="#ff5f5f" stroke-width="1.6"/><path d="M6 28V8" stroke="#4ade80" stroke-width="1.6"/><path d="M6 28l10-8" stroke="#5aa9f0" stroke-width="1.6"/><text x="27" y="31" fill="#ff5f5f" font-size="7" font-family="monospace">X</text><text x="3" y="7" fill="#4ade80" font-size="7" font-family="monospace">Y</text><text x="17" y="19" fill="#5aa9f0" font-size="7" font-family="monospace">Z</text></svg>"""


ROUTE_LIST = [
    ("block-09", "Your system", "Already on mGear, an in-house autorig or another framework? We work inside it, follow its conventions, and the rigs look like your rigs."),
    ("block-03", "Built by hand", "Some characters are better rigged from scratch. Hero faces, odd anatomy, one-off props: bespoke setups when a template would cost more than it saves."),
    ("block-14", "A new system", "Need an autorig or rigging framework of your own? We design and build one around your shows, engine and naming, and hand it over documented."),
    ("block-00", "Our framework", "When the choice is ours, we often reach for Mutant Tools, our own modular framework for Maya. Fast for creatures and game rigs — and optional."),
]
ROUTES = '<div class="cards cards--4">' + "".join(
    f'<div class="card" data-reveal="{i*80}"><div class="card__top"><img class="card__icon" src="/assets/img/{icon}.webp" alt="" width="56" height="56" loading="lazy"><span class="card__num">{i+1:02d}</span></div><h3>{t}</h3><p>{d}</p></div>'
    for i, (icon, t, d) in enumerate(ROUTE_LIST)) + "</div>"


# --------------------------------------------------------------------------- home
def home():
    cards = "".join(
        f"""<a class="card" href="/services/#{sid}" data-reveal="{(i%3)*80}">
        <div class="card__top"><img class="card__icon" src="/assets/img/block-{icon}.webp" alt="" width="56" height="56" loading="lazy"><span class="card__num">{i+1:02d}</span></div>
        <h3>{name}</h3><p>{short}</p><span class="card__more">Details →</span>
      </a>"""
        for i, (sid, icon, name, short, _l, _t, _img) in enumerate(SERVICES)
    )
    shots = ""
    for i, (slug, title, client, rig, kind) in enumerate(WORK):
        media = trailer(slug, title) if slug else SCHWEPPES
        shots += f"""<article class="shot" data-reveal="{(i%2)*100}">
      {media}
      <div class="shot__meta"><div><h3>{title}</h3><p class="shot__client">{client}</p></div><span class="tag">{rig} · {kind}</span></div>
    </article>"""

    ld = """<script type="application/ld+json">{"@context":"https://schema.org","@type":"ProfessionalService","name":"Bluetape Rigging Studio","alternateName":"Bluetape","url":"https://www.bluetaperigging.com/","logo":"https://www.bluetaperigging.com/assets/img/logo.png","description":"Boutique character rigging studio for VFX, animation and games. Maya and Unreal Engine pipelines.","areaServed":"Worldwide","knowsAbout":["Character rigging","Facial rigging","Creature rigging","Quadruped rigging","Wing and bird rigging","Game-ready rigs","Unreal Engine","Autodesk Maya"]}</script>
"""
    return head("Bluetape — Character Rigging Studio for VFX, Animation &amp; Games",
                "Boutique rigging studio. Character, facial, creature and game-ready rigs for Maya and Unreal Engine pipelines, built to your studio’s conventions.",
                "/", ld) + nav("") + f"""
<section class="hero">
  <div class="wrap hero__in">
    <div>
      <span class="kicker">Rigging studio · VFX · Animation · Games</span>
      <h1 class="hero__h1">We do rigging.<br><em>That’s all<br>we do.</em></h1>
      <p class="hero__lead">Characters, faces and creatures for VFX, animation and games — built in Maya and Unreal, using your naming conventions and your file structure. Animals, wings and game-ready bipeds are what we’re best at.</p>
      <div class="btn-row">
        <a class="btn btn--solid" href="/contact/">Start a project <span class="arr">→</span></a>
        <a class="btn" href="/work/">See the work</a>
      </div>
      <p class="hero__status"><span class="dot-live"></span>Remote · working with studios worldwide</p>
    </div>
    <figure class="vp">
      <div class="vp__bar"><span class="vp__dots"><i></i><i></i><i></i></span><span>persp · character_rig</span><span>animation controls</span></div>
      <img class="vp__img" src="/assets/img/hero-rig.webp" alt="A cartoon strongman character in the Maya viewport with its full animation control rig visible" width="1600" height="900" fetchpriority="high">
      <figcaption class="vp__hud"><b>●</b> Body &amp; face controls · animation-ready</figcaption>
      {AXIS}
    </figure>
  </div>
</section>
{PARTNERS}
<section class="section">
  <div class="wrap">
    <div class="section__head">
      <div data-reveal><span class="kicker">What we take on</span><h2 class="section__title">The work we get asked for</h2></div>
      <p class="section__lead" data-reveal="100">Usually one of these. Sometimes all six at once, which is fine. Every job lands inside your pipeline, not beside it.</p>
    </div>
    <div class="cards">{cards}</div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section__head">
      <div data-reveal><span class="kicker">Shipped</span><h2 class="section__title">Selected work</h2></div>
      <p class="section__lead" data-reveal="100">What we rigged, and who it was for. Most of our work sits behind another studio’s name, and some is under NDA and isn’t listed.</p>
    </div>
    <div class="work">{shots}</div>
    <div class="more-row"><a class="link" href="/work/">Full work index →</a></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section__head">
      <div data-reveal><span class="kicker">Your pipeline, your call</span><h2 class="section__title">Any rig system. Or a new one.</h2></div>
      <p class="section__lead" data-reveal="100">We don’t ask studios to adopt our tools. We rig in whatever your show already runs on, build by hand when that’s the better call, or design a system around your needs.</p>
    </div>
    {ROUTES}
    <ul class="stack" data-reveal><li>Your in-house autorig</li><li>mGear</li><li>Mutant Tools</li><li>Hand-built</li><li>Custom frameworks</li></ul>
    <div class="more-row"><a class="link" href="/approach/">How we work with your pipeline →</a></div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section__head">
      <div data-reveal><span class="kicker">Process</span><h2 class="section__title">How a job runs</h2></div>
      <p class="section__lead" data-reveal="100">No surprises at delivery. Scope and acceptance are agreed before a joint is placed.</p>
    </div>
    {steps()}
    <ul class="stack" data-reveal>
      <li>Autodesk Maya</li><li>Unreal Engine</li><li>Control Rig</li><li>mGear</li><li>Python</li><li>PySide / Qt</li><li>Git</li>
    </ul>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="soon" data-reveal>
      <div class="soon__icons"><img src="/assets/img/block-13.webp" alt="" width="64" height="64" loading="lazy"><img src="/assets/img/block-12.webp" alt="" width="64" height="64" loading="lazy"><img src="/assets/img/block-15.webp" alt="" width="64" height="64" loading="lazy"></div>
      <div><h3>Free rigs, still being checked</h3><p>Production rigs and Unreal templates for animals, birds and game-ready bipeds, free to use. No date yet — we’d rather get them right than get them out.</p></div>
      <span class="pill">In audit</span>
    </div>
  </div>
</section>
""" + CTA + FOOT


# --------------------------------------------------------------------------- services
def services():
    rows = ""
    for i, (sid, icon, name, _s, long, chips, img) in enumerate(SERVICES):
        media = (f'<div class="srow__media"><img src="/assets/img/{img}" alt="" loading="lazy"></div>' if img
                 else f'<div class="srow__media srow__media--icon"><img src="/assets/img/block-{icon}.webp" alt="" width="160" height="160" loading="lazy"></div>')
        chip = "".join(f"<li>{c}</li>" for c in chips)
        more = f'<p style="margin-top:26px"><a class="link" href="/{SERVICE_SEO[sid][0]}/">{SERVICE_SEO[sid][1]} →</a></p>' if sid in SERVICE_SEO else ""
        rows += f"""<article class="srow{' srow--flip' if i % 2 else ''}" id="{sid}">
      {media}
      <div data-reveal><span class="srow__num">{i+1:02d} / 06</span><h2>{name}</h2><p>{long}</p><ul class="stack">{chip}</ul>{more}</div>
    </article>"""

    faq = [
        ("Can you work in our pipeline and naming conventions?", "Yes. Adapting to a studio’s own naming conventions, asset structure and versioning is standard for us. Rigs arrive inside your pipeline rather than beside it."),
        ("Do you rig for Unreal Engine?", "Yes. Game-ready rigs built to an agreed joint budget, exported clean and integrated with Control Rig and Blueprints."),
        ("Can you take over a rig somebody else started?", "Yes. Rig rescue is a normal contract for us: diagnose what is actually breaking the deformation or the export, then stabilise the asset without restarting it unless restarting is cheaper."),
        ("Do you do creature and animal rigging?", "It’s our strongest specialism: quadrupeds, wings, bird systems, tails and anything that has to hold up at extreme range."),
        ("Do we have to use your rigging system?", "No. We work in whatever the show already uses — your in-house autorig, mGear, or another framework — build by hand where that’s the better call, or design a new system for you. Our own framework, Mutant Tools, is one option, never a requirement."),
        ("Do you sign NDAs?", "Yes, as standard. Most of our work sits behind another studio’s name and we’re happy to keep it that way."),
    ]
    faq_html = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faq)
    ld = '<script type="application/ld+json">' + (
        '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":['
        + ",".join('{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}' % (q, a.replace("’", "'")) for q, a in faq)
        + "]}") + "</script>\n"

    return head("Rigging Services — Character, Creature &amp; Game-Ready | Bluetape",
                "Character and facial rigging, creature and animal rigging, game-ready Unreal rigs, overflow capacity, rig rescue and pipeline tools.",
                "/services/", ld) + nav("services") + f"""
<section class="phero">
  <div class="wrap phero__in">
    <div>
      <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><span>Services</span></nav>
      <span class="kicker">Services</span>
      <h1>What we do, and how it lands.</h1>
    </div>
    <div>
      <p class="phero__lead">We’re a rigging studio, not a generalist vendor. The work arrives finished to a production standard, documented, and shaped to the pipeline it has to live in.</p>
      <div class="btn-row"><a class="btn btn--solid" href="/contact/">Start a project <span class="arr">→</span></a></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">{rows}</div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section__head section__head--solo" data-reveal><span class="kicker">Process</span><h2 class="section__title">How a job runs</h2></div>
    {steps()}
  </div>
</section>

<section class="section">
  <div class="wrap split" style="align-items:start">
    <div data-reveal>
      <span class="kicker">Before we start</span>
      <h2 class="section__title">What we need from you</h2>
      <ul class="check" style="margin-top:36px">
        <li>The asset list, and which assets block animation first.</li>
        <li>The target engine or renderer, and the DCC everything is authored in.</li>
        <li>Your naming conventions, folder structure and publish process — a document or an example rig is perfect.</li>
        <li>The real deadline and what happens on it.</li>
        <li>One named approver, and the number of revision rounds you expect.</li>
        <li>If this is a rescue: what broke, and when it started.</li>
      </ul>
    </div>
    <div data-reveal="120">
      <span class="kicker">FAQ</span>
      <h2 class="section__title">Common questions</h2>
      <div class="faq" style="margin-top:36px">{faq_html}</div>
    </div>
  </div>
</section>
""" + CTA + FOOT


# --------------------------------------------------------------------------- work
def work():
    rows = ""
    for i, (slug, title, client, rig, kind) in enumerate(WORK):
        media = trailer(slug, title) if slug else SCHWEPPES
        rows += f"""<article class="wrow">
      <div data-reveal>{media}</div>
      <div data-reveal="120">
        <span class="wrow__idx">{i+1:02d} / {len(WORK):02d}</span>
        <h2>{title}</h2>
        <p class="wrow__client">{client}</p>
        <dl class="spec"><dt>Rig</dt><dd>{rig}</dd><dt>Focus</dt><dd>{kind}</dd></dl>
      </div>
    </article>"""
    return head("Work — Games, Animation &amp; VFX Rigging | Bluetape",
                "Shipped rigging work: SpeedRunners 2, Nicktoons & The Dice of Destiny, Pudgy Party and Schweppes “Meet Your Match”.",
                "/work/") + nav("work") + f"""
<section class="phero">
  <div class="wrap phero__in">
    <div>
      <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><span>Work</span></nav>
      <span class="kicker">Shipped</span>
      <h1>Work</h1>
    </div>
    <p class="phero__lead">What we rigged, who it was for, and what the rigging job actually was. Some client work is covered by NDA and isn’t listed.</p>
  </div>
</section>
<section class="section"><div class="wrap">{rows}</div></section>
{PARTNERS}
<section class="section">
  <div class="wrap split">
    <div data-reveal><span class="kicker">Partners</span><h2 class="section__title">Who we work with</h2></div>
    <div data-reveal="120" style="color:var(--soft);font-size:17px;display:grid;gap:18px">
      <p>We collaborate with studios on VFX rigging and creature setup across the globe — as an outsourcing partner on a full package, or as extra capacity inside an existing department.</p>
      <p>Most of our work sits behind another studio’s name, which is how outsourcing should be. If you need references for a specific kind of asset — a quadruped, a wing system, a facial setup inside a joint budget — ask and we’ll arrange what the NDA allows.</p>
    </div>
  </div>
</section>
""" + CTA + FOOT


# --------------------------------------------------------------------------- approach
def approach():
    feats = [
        ("Your conventions", "Naming, folder structure, versioning and publishing follow your studio. Send a document or an example rig and the deliveries match it."),
        ("Layered chains", "Tails, necks and spines get an authored FK layer and a smooth spline layer, blendable. Simulation on top where the pipeline supports it — never instead of, because animation has to hit a specific silhouette on a specific frame."),
        ("Engine ready", "Joint budgets are agreed and split by region up front. The export skeleton is treated as a contract with its own acceptance test: count, orientation, bind pose, naming, morph target names."),
        ("Validated delivery", "Every asset goes through the same checks before it reaches you, whichever system built it. Failures are loud and specific, not silent."),
    ]
    fh = "".join(f'<div data-reveal="{(i%2)*100}"><span class="feat__n">{i+1:02d}</span><h3>{t}</h3><p>{p}</p></div>' for i, (t, p) in enumerate(feats))
    return head("Our Approach — Any Rigging System, or a New One | Bluetape",
                "We rig inside your pipeline: your in-house autorig, mGear or another framework, hand-built setups, or a new rigging system designed for your studio.",
                "/approach/") + nav("approach") + f"""
<section class="phero">
  <div class="wrap phero__in">
    <div>
      <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><span>Approach</span></nav>
      <span class="kicker">Approach</span>
      <h1>Your system, ours, or a new one.</h1>
    </div>
    <div>
      <p class="phero__lead">Rigging has to live in your pipeline after we leave. So the system is your call: we work inside what your show already uses, build by hand, or design something new for you.</p>
      <div class="btn-row"><a class="btn btn--solid" href="/contact/">Talk to us about your pipeline <span class="arr">→</span></a></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section__head section__head--solo" data-reveal><span class="kicker">Four ways in</span><h2 class="section__title">Pick what fits the show</h2></div>
    {ROUTES}
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section__head section__head--solo" data-reveal><span class="kicker">Whatever the system</span><h2 class="section__title">What stays the same</h2></div>
    <div class="feat">{fh}</div>
  </div>
</section>

<section class="section">
  <div class="wrap fw fw--small">
    <div class="fw__art" data-reveal><img src="/assets/img/blocks.webp" alt="The Mutant Tools rigging blocks" width="900" height="900" loading="lazy"></div>
    <div class="fw__body" data-reveal="120">
      <span class="kicker">Our own framework</span>
      <h2 class="section__title">Mutant Tools, when it helps</h2>
      <p>When a studio leaves the choice to us, we often build with Mutant Tools, our modular rigging framework for Maya. It is free and open source, so a rig built with it never depends on us or on a licence server.</p>
      <div class="btn-row"><a class="btn" href="https://mutanttools.com/" rel="noopener">mutanttools.com ↗</a></div>
    </div>
  </div>
</section>
""" + CTA + FOOT


SERVICE_SEO = {
    "character": ("facial-rigging", "Facial rigging"),
    "creature": ("creature-rigging", "Creature rigging"),
    "games": ("game-character-rigging", "Game character rigging"),
    "overflow": ("rigging-outsourcing", "Rigging outsourcing"),
    "rescue": ("rig-troubleshooting", "Rig rescue"),
    "tools": ("custom-autorig-development", "Custom autorigs"),
}
WORK_BY_SLUG = {w[0]: w for w in WORK}


# --------------------------------------------------------------------------- search landing pages
def seo_page(p):
    url = f"{SITE}/{p['slug']}/"
    plain = lambda t: t.replace("&amp;", "&")
    ld = [
        {"@context": "https://schema.org", "@type": "Service", "name": plain(p["kicker"]), "serviceType": plain(p["kicker"]),
         "description": plain(p["desc"]), "url": url, "areaServed": "Worldwide",
         "provider": {"@type": "Organization", "name": "Bluetape Rigging Studio", "url": SITE + "/"}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in p["faq"]]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Services", "item": SITE + "/services/"},
            {"@type": "ListItem", "position": 3, "name": plain(p["kicker"]), "item": url}]},
    ]
    extra = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld)

    if p.get("img"):
        media = f'<div class="srow__media"><img src="/assets/img/{p["img"]}" alt="" loading="lazy"></div>'
    else:
        media = f'<div class="srow__media srow__media--icon"><img src="/assets/img/{p["icon"]}.webp" alt="" width="160" height="160" loading="lazy"></div>'
    deliver = "".join(f"<li>{d}</li>" for d in p["deliver"])
    body = "".join(f"<h3>{h}</h3><p>{t}</p>" for h, t in p["body"])
    fit = "".join(f"<li>{f}</li>" for f in p["fit"])
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in p["faq"])

    work = ""
    if p["work"]:
        shots = ""
        for i, key in enumerate(p["work"]):
            slug, title, client, rig, kind = WORK_BY_SLUG[key]
            media_w = trailer(slug, title) if slug else SCHWEPPES
            shots += f"""<article class="shot" data-reveal="{(i%2)*100}">{media_w}
      <div class="shot__meta"><div><h3>{title}</h3><p class="shot__client">{client}</p></div><span class="tag">{rig} · {kind}</span></div></article>"""
        work = f"""<section class="section">
  <div class="wrap">
    <div class="section__head section__head--solo" data-reveal><span class="kicker">Shipped</span><h2 class="section__title">Related work</h2></div>
    <div class="work">{shots}</div>
  </div>
</section>"""

    others = "".join(f'<li><a href="/{o["slug"]}/">{o["nav"]}</a></li>' for o in SEO if o is not p)
    return head(p["title"], p["desc"], f"/{p['slug']}/", extra) + nav("") + f"""
<section class="phero">
  <div class="wrap phero__in">
    <div>
      <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><a href="/services/">Services</a><span>/</span><span>{p['kicker']}</span></nav>
      <span class="kicker">{p['kicker']}</span>
      <h1>{p['h1']}</h1>
    </div>
    <div>
      <p class="phero__lead">{p['lead']}</p>
      <div class="btn-row"><a class="btn btn--solid" href="/contact/">Start a project <span class="arr">→</span></a><a class="btn" href="/work/">See the work</a></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap srow" style="padding-block:0;border:0">
    {media}
    <div data-reveal><span class="kicker">What you get</span><h2 class="section__title">What we deliver</h2><ul class="check" style="margin-top:32px">{deliver}</ul></div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap split" style="align-items:start">
    <div class="prose" data-reveal><span class="kicker">How we approach it</span>{body}</div>
    <aside data-reveal="120"><span class="kicker">A good fit when</span><ul class="check" style="margin-top:28px">{fit}</ul></aside>
  </div>
</section>
{work}
<section class="section{' section--alt' if p['work'] else ''}">
  <div class="wrap split" style="align-items:start">
    <div data-reveal><span class="kicker">FAQ</span><h2 class="section__title">Questions studios ask</h2></div>
    <div class="faq" data-reveal="120">{faq}</div>
  </div>
</section>

<section class="section{'' if p['work'] else ' section--alt'}">
  <div class="wrap">
    <span class="kicker">More services</span>
    <ul class="stack stack--links">{others}</ul>
  </div>
</section>
""" + CTA + FOOT


# --------------------------------------------------------------------------- contact
def contact():
    opts = "".join(f"<option>{o}</option>" for o in [
        "Character &amp; facial rigging", "Creature or animal rigging", "Game-ready rigs / Unreal",
        "Overflow on a running show", "Rig rescue", "Tools &amp; pipeline", "Something else"])
    return head("Start a Project — Contact | Bluetape",
                "Send Bluetape your asset list, engine and deadline. We’ll come back with what we think it takes.",
                "/contact/") + nav("contact") + f"""
<section class="phero">
  <div class="wrap phero__in">
    <div>
      <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><span>Contact</span></nav>
      <span class="kicker">Contact</span>
      <h1>Start a project</h1>
    </div>
    <p class="phero__lead">The more specific the message, the more useful the answer. Asset list, engine, deadline and what has already gone wrong is enough for a real reply.</p>
  </div>
</section>
<section class="section">
  <div class="wrap contact">
    <form class="form" id="brief" data-reveal>
      <div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" autocomplete="name" required></div>
      <div class="field"><label for="f-studio">Studio</label><input id="f-studio" name="studio" autocomplete="organization"></div>
      <div class="field"><label for="f-need">What you need</label><select id="f-need" name="need">{opts}</select></div>
      <div class="field"><label for="f-deadline">Deadline or window</label><input id="f-deadline" name="deadline" placeholder="e.g. first rigs by March"></div>
      <div class="field field--full"><label for="f-scope">Scope</label><textarea id="f-scope" name="scope" required placeholder="How many characters, which engine or renderer, your conventions, and anything that has already gone wrong."></textarea></div>
      <div class="form__foot"><p class="form__note">Opens your email app with the brief filled in. Nothing is stored on this site.</p><button class="btn btn--solid" type="submit">Write the email <span class="arr">→</span></button></div>
    </form>
    <aside class="info" data-reveal="120">
      <div><h3>Email</h3><p><a data-mail href="/contact/"></a></p></div>
      <div><h3>Where</h3><p>Remote, working with studios worldwide across VFX, animation and games.</p></div>
      <div><h3>Framework</h3><p><a href="https://mutanttools.com/" rel="noopener">mutanttools.com ↗</a></p></div>
      <div><h3>NDA</h3><p>Standard for us. Most of our work sits behind another studio’s name and we’re happy to keep it that way.</p></div>
    </aside>
  </div>
</section>
""" + FOOT


PAGES = {
    "index.html": home,
    "services/index.html": services,
    "work/index.html": work,
    "approach/index.html": approach,
    "contact/index.html": contact,
}

for _p in SEO:
    PAGES[f"{_p['slug']}/index.html"] = (lambda p=_p: seo_page(p))

def not_found():
    return head("Page not found | Bluetape", "This page doesn’t exist.", "/404.html").replace(
        '<link rel="canonical"', '<meta name="robots" content="noindex">\n<link rel="canonical"') + nav("") + """
<section class="phero">
  <div class="wrap phero__in">
    <div><span class="kicker">404</span><h1>Nothing rigged here.</h1></div>
    <div><p class="phero__lead">The page you’re looking for doesn’t exist, or moved when the site was rebuilt.</p>
      <div class="btn-row"><a class="btn btn--solid" href="/">Home <span class="arr">→</span></a><a class="btn" href="/services/">Services</a></div></div>
  </div>
</section>
""" + FOOT


PAGES["404.html"] = not_found
SITEMAP_EXCLUDE = {"contact/index.html", "404.html"}


def sitemap():
    urls = "".join(
        f"  <url><loc>{SITE}/{rel[:-len('index.html')]}</loc></url>\n" for rel in PAGES if rel not in SITEMAP_EXCLUDE)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n'


if __name__ == "__main__":
    (ROOT / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    for rel, fn in PAGES.items():
        out = ROOT / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(fn(), encoding="utf-8")
        print("wrote", rel)
