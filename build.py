#!/usr/bin/env python3
"""Generate the CoupeFab static site (FR-first, EN toggle)."""
import json
from pathlib import Path

ROOT = Path(__file__).parent
SITE = "https://couperfab.vercel.app"
DATE_ISO = "2026-11-26"
DATE_FR = "26 novembre 2026"
DATE_EN = "November 26, 2026"
ZONE = "America/Toronto (UTC−5)"

NAV_FR = [
    ("/", "Accueil"),
    ("/guides/", "Guides"),
    ("/occasions/", "Occasions Québec"),
    ("/prix/", "Prix des tôles"),
    ("/infolettre/", "Infolettre"),
    ("/a-propos/", "À propos"),
]
NAV_EN = [
    ("/en/", "Home"),
    ("/en/guides/", "Guides"),
    ("/en/used-equipment/", "Used equipment"),
    ("/en/sheet-prices/", "Sheet prices"),
    ("/en/newsletter/", "Newsletter"),
    ("/en/about/", "About"),
]


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def layout(
    *,
    lang: str,
    title: str,
    description: str,
    path: str,
    alt: str,
    body: str,
    draft: bool = False,
    article: bool = False,
    crumbs: str = "",
) -> str:
    fr = lang == "fr"
    in_lang = "fr-CA" if fr else "en-CA"
    alt_lang = "en-CA" if fr else "fr-CA"
    nav = NAV_FR if fr else NAV_EN
    canonical = SITE + path
    alt_url = SITE + alt
    draft_banner = ""
    if draft:
        draft_banner = (
            '<div class="draft-banner" role="status"><strong>Brouillon — à réviser par Michaël.</strong> '
            "Cette page n’est pas encore une version publiée. Les paramètres de coupe et les prix ne sont cités que lorsqu’une source publique les donne.</div>"
            if fr
            else '<div class="draft-banner" role="status"><strong>Draft — to be reviewed by Michaël.</strong> '
            "This page is not a published version yet. Cut parameters and prices appear only when a public source gives them.</div>"
        )
    nav_html = []
    for href, label in nav:
        current = ' aria-current="page"' if path == href or (href != "/" and href != "/en/" and path.startswith(href)) else ""
        if href in ("/", "/en/") and path != href:
            current = ""
        nav_html.append(f'<a href="{href}"{current}>{label}</a>')
    nav_html.append(
        f'<div class="lang-switch" role="navigation" aria-label="{"Langue" if fr else "Language"}">'
        f'<a href="{path if fr else alt}" hreflang="fr"{" aria-current=\"true\"" if fr else ""}>FR</a>'
        f'<a href="{alt if fr else path}" hreflang="en"{" aria-current=\"true\"" if not fr else ""}>EN</a>'
        f"</div>"
    )
    schema = ""
    if article:
        schema = (
            "\n<script type=\"application/ld+json\">\n"
            + json.dumps(
                {
                    "@context": "https://schema.org",
                    "@type": "Article",
                    "headline": title,
                    "description": description,
                    "inLanguage": in_lang,
                    "dateModified": DATE_ISO,
                    "url": canonical,
                    "author": {"@type": "Organization", "name": "CoupeFab"},
                    "publisher": {"@type": "Organization", "name": "CoupeFab", "url": SITE + "/"},
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n</script>"
        )
    org_schema = ""
    if path in ("/", "/en/"):
        org_schema = (
            "\n<script type=\"application/ld+json\">\n"
            + json.dumps(
                {
                    "@context": "https://schema.org",
                    "@type": "Organization",
                    "name": "CoupeFab",
                    "url": SITE + "/",
                    "inLanguage": ["fr-CA", "en-CA"],
                    "areaServed": "Quebec, Canada",
                    "description": description,
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n</script>"
        )

    skip = "Aller au contenu" if fr else "Skip to content"
    menu = "Menu" if fr else "Menu"
    footer_tag = (
        "Ressource francophone d’abord, pour les ateliers de découpe plasma et de fabrication métallique au Québec."
        if fr
        else "A French-first resource for plasma cutting and metal fabrication shops in Quebec."
    )
    explore = "Explorer" if fr else "Explore"
    legal_h = "Mentions" if fr else "Legal"
    copy = f"© {DATE_ISO[:4]} CoupeFab. {('Tous droits réservés.' if fr else 'All rights reserved.')}"
    footer_note = (
        f"Consultation des sources publiques le {DATE_FR}, fuseau {ZONE}. Aucun lien d’affiliation pour le moment."
        if fr
        else f"Public sources consulted on {DATE_EN}, time zone {ZONE}. No affiliate links for now."
    )
    foot_links_a = (
        ' / '.join(
            [
                '<a href="/guides/">Guides</a>' if fr else '<a href="/en/guides/">Guides</a>',
                '<a href="/occasions/">Occasions Québec</a>' if fr else '<a href="/en/used-equipment/">Used equipment</a>',
                '<a href="/prix/">Prix des tôles</a>' if fr else '<a href="/en/sheet-prices/">Sheet prices</a>',
                '<a href="/infolettre/">Infolettre</a>' if fr else '<a href="/en/newsletter/">Newsletter</a>',
            ]
        )
    )
    foot_links_b = (
        '<a href="/a-propos/">À propos / contact</a><br>'
        '<a href="/divulgation/">Divulgation (affiliations)</a><br>'
        '<a href="/confidentialite/">Confidentialité et consentement (CASL)</a>'
        if fr
        else '<a href="/en/about/">About / contact</a><br>'
        '<a href="/en/affiliate-disclosure/">Affiliate disclosure</a><br>'
        '<a href="/en/privacy/">Privacy and CASL consent</a>'
    )
    return f"""<!DOCTYPE html>
<html lang="{in_lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <meta name="robots" content="index,follow">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="{in_lang}" href="{canonical}">
  <link rel="alternate" hreflang="{alt_lang}" href="{alt_url}">
  <link rel="alternate" hreflang="x-default" href="{SITE}/">
  <meta property="og:type" content="{'article' if article else 'website'}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:locale" content="{'fr_CA' if fr else 'en_CA'}">
  <meta property="og:locale:alternate" content="{'en_CA' if fr else 'fr_CA'}">
  <meta name="twitter:card" content="summary">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/style.css">
  {schema}{org_schema}
</head>
<body>
  <a class="skip" href="#contenu">{skip}</a>
  <header class="site-header">
    <div class="header-inner">
      <a class="brand" href="{'/' if fr else '/en/'}">
        <svg class="brand-mark" viewBox="0 0 32 32" aria-hidden="true">
          <rect width="32" height="32" rx="6" fill="#1B1D1B"/>
          <path d="M5 11h22M5 21h22M5 16h9.2M18.2 16H27" stroke="#F4F1EA" stroke-width="2"/>
          <rect x="14.2" y="14.2" width="4" height="3.6" fill="#B54300"/>
        </svg>
        Coupe<span>Fab</span>
      </a>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="nav-primary">{menu}</button>
      <nav class="primary" id="nav-primary">
        {''.join(nav_html)}
      </nav>
    </div>
  </header>
  {draft_banner}
  <main id="contenu">
  {crumbs}
  {body}
  </main>
  <footer class="site-footer">
    <div class="footer-inner">
      <div>
        <a class="brand" href="{'/' if fr else '/en/'}" style="color:#fffcf6">Coupe<span>Fab</span></a>
        <p>{footer_tag}</p>
      </div>
      <div>
        <h2>{explore}</h2>
        <p>{foot_links_a}</p>
      </div>
      <div>
        <h2>{legal_h}</h2>
        <p>{foot_links_b}</p>
      </div>
    </div>
    <p class="legal">{copy} {footer_note}</p>
  </footer>
  <script src="/js/site.js" defer></script>
</body>
</html>
"""


def form_newsletter(lang: str) -> str:
    if lang == "fr":
        return """
<form class="stack" data-form="newsletter" data-lang="fr" novalidate>
  <div class="hp" aria-hidden="true"><label>Site web<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
  <label>Prénom ou atelier (facultatif)
    <input type="text" name="name" autocomplete="name">
  </label>
  <label>Courriel
    <input type="email" name="email" required autocomplete="email" inputmode="email">
  </label>
  <label class="consent">
    <input type="checkbox" name="consent" value="oui">
    <span>J’accepte de recevoir l’infolettre de CoupeFab (guides, digest d’occasions et suivi des prix des tôles). Je peux me désabonner en tout temps. Voir la <a href="/confidentialite/">politique de confidentialité</a>.</span>
  </label>
  <button type="submit">S’inscrire</button>
  <p class="form-status" role="status" aria-live="polite"></p>
</form>
<p class="meta">Conformité CASL : la case n’est pas précochée. Aucun envoi sans ce consentement exprès.</p>
"""
    return """
<form class="stack" data-form="newsletter" data-lang="en" novalidate>
  <div class="hp" aria-hidden="true"><label>Website<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
  <label>Name or shop (optional)
    <input type="text" name="name" autocomplete="name">
  </label>
  <label>Email
    <input type="email" name="email" required autocomplete="email" inputmode="email">
  </label>
  <label class="consent">
    <input type="checkbox" name="consent" value="yes">
    <span>I agree to receive the CoupeFab newsletter (guides, used-equipment digest, and sheet-price updates). I may unsubscribe at any time. See the <a href="/en/privacy/">privacy policy</a>.</span>
  </label>
  <button type="submit">Subscribe</button>
  <p class="form-status" role="status" aria-live="polite"></p>
</form>
<p class="meta">CASL compliance: the box is not pre-checked. Nothing is sent without this express consent.</p>
"""


def form_contact(lang: str) -> str:
    if lang == "fr":
        return """
<form class="stack" data-form="contact" data-lang="fr" novalidate>
  <div class="hp" aria-hidden="true"><label>Site web<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
  <label>Nom
    <input type="text" name="name" autocomplete="name">
  </label>
  <label>Courriel
    <input type="email" name="email" required autocomplete="email" inputmode="email">
  </label>
  <label>Message
    <textarea name="message" required></textarea>
  </label>
  <button type="submit">Envoyer</button>
  <p class="form-status" role="status" aria-live="polite"></p>
</form>
"""
    return """
<form class="stack" data-form="contact" data-lang="en" novalidate>
  <div class="hp" aria-hidden="true"><label>Website<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
  <label>Name
    <input type="text" name="name" autocomplete="name">
  </label>
  <label>Email
    <input type="email" name="email" required autocomplete="email" inputmode="email">
  </label>
  <label>Message
    <textarea name="message" required></textarea>
  </label>
  <button type="submit">Send</button>
  <p class="form-status" role="status" aria-live="polite"></p>
</form>
"""


# --- Page bodies ---

HOME_FR = f"""
<section class="hero">
  <div class="hero-inner">
    <p class="kicker">Québec · plasma · CAD/CAM</p>
    <h1>CoupeFab, la référence francophone pour la découpe plasma.</h1>
    <p class="lede">Guides SheetCam et BricsCAD, digest d’équipements d’occasion au Québec, et suivi des prix de tôles publiés. Rédigé pour l’atelier, pas pour la brochure.</p>
    <div class="actions">
      <a class="btn" href="/guides/">Lire les guides</a>
      <a class="btn btn-ghost" href="/infolettre/">S’inscrire à l’infolettre</a>
    </div>
  </div>
</section>
<div class="wrap">
  <h2>Trois outils, un même atelier</h2>
  <div class="grid">
    <article class="card">
      <h3><a href="/guides/">Guides</a></h3>
      <p>SheetCam en français, un DXF propre depuis BricsCAD, le kerf, les consommables au Canada. Pages encore en brouillon, à valider en atelier.</p>
      <a class="more" href="/guides/">Voir les guides</a>
    </article>
    <article class="card">
      <h3><a href="/occasions/">Occasions Québec</a></h3>
      <p>Une ronde d’annonces publiques (tables plasma, laser, presses) avec liens vers Kijiji, Machinio, encans et courtiers, plus une liste de vérification.</p>
      <a class="more" href="/occasions/">Voir le digest</a>
    </article>
    <article class="card">
      <h3><a href="/prix/">Prix des tôles</a></h3>
      <p>Comparaison à partir de listes publiques seulement, avec date et source. Beaucoup de fournisseurs restent en « prix sur demande » — on le dit clairement.</p>
      <a class="more" href="/prix/">Voir la méthode</a>
    </article>
  </div>
  <h2>S’inscrire</h2>
  <p>L’infolettre regroupera les nouveaux guides, le digest d’occasions et la mise à jour des prix. Envoi manuel au départ, depuis Gmail. Pas de pub tierce pour le moment.</p>
  {form_newsletter("fr")}
</div>
"""

HOME_EN = f"""
<section class="hero">
  <div class="hero-inner">
    <p class="kicker">Quebec · plasma · CAD/CAM</p>
    <h1>CoupeFab, a French-first plasma shop reference.</h1>
    <p class="lede">SheetCam and BricsCAD guides, a digest of used fab equipment in Quebec, and a tracker of publicly posted sheet prices. Written for the shop floor, not a brochure.</p>
    <div class="actions">
      <a class="btn" href="/en/guides/">Read the guides</a>
      <a class="btn btn-ghost" href="/en/newsletter/">Join the newsletter</a>
    </div>
  </div>
</section>
<div class="wrap">
  <h2>Three tools, one shop</h2>
  <div class="grid">
    <article class="card">
      <h3><a href="/en/guides/">Guides</a></h3>
      <p>SheetCam in French, a clean DXF from BricsCAD, kerf, and consumables in Canada. These pages are still drafts, waiting for shop-floor review.</p>
      <a class="more" href="/en/guides/">See the guides</a>
    </article>
    <article class="card">
      <h3><a href="/en/used-equipment/">Used equipment in Quebec</a></h3>
      <p>A round-up of public listings (plasma tables, lasers, press brakes) with links to Kijiji, Machinio, auctions and dealers, plus a buyer’s checklist.</p>
      <a class="more" href="/en/used-equipment/">See the digest</a>
    </article>
    <article class="card">
      <h3><a href="/en/sheet-prices/">Sheet prices</a></h3>
      <p>A comparison drawn only from public price lists, with dates and sources. Many suppliers still say “call for pricing” — we say so plainly.</p>
      <a class="more" href="/en/sheet-prices/">See the method</a>
    </article>
  </div>
  <h2>Subscribe</h2>
  <p>The newsletter will carry new guides, the used-equipment digest, and price updates. Early issues will be sent by hand from Gmail. No third-party ads for now.</p>
  {form_newsletter("en")}
</div>
"""

GUIDES_FR = """
<div class="wrap">
  <p class="kicker">Guides</p>
  <h1 class="page-title">Guides de découpe et de CAD/CAM</h1>
  <p class="lede">Quatre textes d’angle, en français d’abord. Ils sont tous marqués <strong>brouillon — à réviser par Michaël</strong> jusqu’à validation technique. Aucun paramètre de coupe inventé.</p>
  <div class="grid">
    <article class="card">
      <h2><a href="/guides/debuter-sheetcam/">Débuter avec SheetCam en français</a></h2>
      <p>Installation du job, import DXF, opération plasma, imbricage, et les pièges d’unités documentés par SheetCam.</p>
    </article>
    <article class="card">
      <h2><a href="/guides/bricscad-dxf/">De BricsCAD à un DXF propre</a></h2>
      <p>La commande officielle DXFOUT, la précision décimale, les objets mandataires, et une liste de contrôle avant le CAM.</p>
    </article>
    <article class="card">
      <h2><a href="/guides/kerf-qualite-coupe/">Kerf et qualité de coupe</a></h2>
      <p>Comment lire un tableau du fabricant, pourquoi ne pas mélanger les manuels, et un exemple cité d’une charte Hypertherm.</p>
    </article>
    <article class="card">
      <h2><a href="/guides/consommables-plasma-canada/">Consommables plasma et achats au Canada</a></h2>
      <p>Entretien recommandé par Hypertherm, électrode et buse, et pistes d’achat au Canada — sans liens d’affiliation.</p>
    </article>
  </div>
</div>
"""

GUIDES_EN = """
<div class="wrap">
  <p class="kicker">Guides</p>
  <h1 class="page-title">Cutting and CAD/CAM guides</h1>
  <p class="lede">Four cornerstone pieces, written French-first. Each is marked <strong>draft — to be reviewed by Michaël</strong> until the technical content is signed off. No invented cut parameters.</p>
  <div class="grid">
    <article class="card">
      <h2><a href="/en/guides/getting-started-sheetcam/">Getting started with SheetCam (French companion)</a></h2>
      <p>Job setup, DXF import, plasma operations, nesting, and the unit pitfalls SheetCam itself documents.</p>
    </article>
    <article class="card">
      <h2><a href="/en/guides/bricscad-to-clean-dxf/">From BricsCAD to a clean DXF</a></h2>
      <p>The official DXFOUT command, decimal precision, proxy objects, and a pre-CAM checklist.</p>
    </article>
    <article class="card">
      <h2><a href="/en/guides/kerf-and-cut-quality/">Kerf and cut quality</a></h2>
      <p>How to read a manufacturer chart, why manuals should not be mixed, and one cited Hypertherm example.</p>
    </article>
    <article class="card">
      <h2><a href="/en/guides/plasma-consumables-canada/">Plasma consumables and buying in Canada</a></h2>
      <p>Hypertherm’s own care guidance, electrode and nozzle practice, and Canadian buying paths — no affiliate links.</p>
    </article>
  </div>
</div>
"""

SHEETCAM_FR = """
<div class="wrap prose">
  <p class="crumb"><a href="/guides/">Guides</a> · SheetCam</p>
  <h1>Débuter avec SheetCam en français</h1>
  <p class="meta">Brouillon · mis à jour le 26 novembre 2026 · à réviser par Michaël</p>
  <p class="lede">SheetCam est un logiciel de FAO (CAM) pour la découpe 2D — plasma, oxycoupage, jet d’eau, laser. Ce n’est pas un logiciel de DAO. Les manuels officiels sont en anglais ; cette page est un compagnon francophone, pas un substitut.</p>

  <h2>Où trouver l’officiel</h2>
  <p>Chez <a href="https://sheetcamshop.myshopify.com/pages/support">SheetCam LLC (page Support Manuals)</a> : guide de démarrage rapide 8.0, guide d’imbricage automatique, guide 2D CAD, et le manuel (formats A4 et US Letter, y compris une version « plasma, unités métriques »). Dans le logiciel : menu <strong>Help → Tutorials</strong> pour des démarches pas à pas.</p>
  <p>La version d’essai, d’après une réponse de l’équipe SheetCam sur le <a href="https://forum.sheetcam.com/t/where-to-learn-sheetcam/8102">forum officiel</a>, est le même exécutable que la version licenciée, sans limite de temps, mais elle ne produit qu’environ 180 lignes de G-code. Téléchargement : le site de SheetCam LLC.</p>

  <h2>Deux réglages d’unités, souvent confondus</h2>
  <p>Même source (équipe SheetCam, forum) : il y a <strong>deux</strong> endroits pour les unités linéaires, et ils sont indépendants.</p>
  <ul>
    <li><strong>Options → Application options</strong> : unités du canevas de conception.</li>
    <li><strong>Options → Machine → Post Processor</strong> : unités du G-code envoyé à la machine.</li>
  </ul>
  <p>Ils n’ont pas à être identiques, mais un décalage mal compris donne des pièces trop petites ou trop grandes. Vérifiez les deux avant le premier essai.</p>
  <div class="callout warn"><p>Les tutoriels intégrés, toujours selon cette même note officielle, <strong>modifient les Options / Job options</strong> (matière, zone de travail, taille de table). Prévoyez de les remettre à votre machine après le tutoriel.</p></div>

  <h2>Démarche typique (sans paramètres inventés)</h2>
  <p>La séquence ci-dessous reprend le flux documenté par SheetCam et des guides d’utilisation publics (notamment le démarrage rapide publié par des intégrateurs). Les valeurs de jeu, de longueur d’entrée et de vitesse doivent venir de <em>votre</em> source plasma, de votre post-processeur et de vos essais — pas de cette page.</p>
  <ol>
    <li><strong>Nouveau job.</strong> File → New job. Puis Options → Job options : zone de travail, épaisseur si vous la suivez ici, origine (souvent le coin inférieur gauche, X0,Y0), hauteur de dégagement des rapides. Validez.</li>
    <li><strong>Importer le dessin.</strong> File → Import drawing… (DXF, SVG, etc.). Dans le dialogue, alignez l’échelle et les unités sur le fichier. Si la pièce est minuscule ou énorme, c’est presque toujours un conflit d’unités : réimportez.</li>
    <li><strong>Vérifier la géométrie.</strong> Contours ouverts, traits en double, ou blocs non explosés se règlent idéalement dans le DAO (voir le guide BricsCAD). SheetCam offre aussi des outils de réparation : utilisez-les en sachant ce que vous changez.</li>
    <li><strong>Minimum requis pour un parcours.</strong> D’après l’équipe SheetCam : au moins une <strong>pièce</strong> (Part — un import DXF arrive déjà dans une pièce), une <strong>couche</strong> (Layer), un <strong>outil</strong> (idéalement deux, pour les règles et comparaisons), et une <strong>opération</strong> (pour le plasma : Jet / Plasma Cut).</li>
    <li><strong>Opération plasma.</strong> Operations → New operation → Plasma Cut. Méthode de contour typique : extérieur pour le profil, intérieur pour les trous, sans décalage pour un traçage. Choisissez la couche et l’outil. Les entrées/sorties (lead-in / lead-out) et le sens de coupe dépendent de votre chalumeau et de votre charte — ne copiez pas une longueur « standard » trouvée au hasard.</li>
    <li><strong>Post-processeur.</strong> Options → Machine → Post Processor : choisissez celui qui correspond à votre commande. S’il n’est pas dans la bibliothèque, SheetCam documente une API et peut citer un travail sur mesure (sales@sheetcam.com, d’après le forum officiel). Puis File → Post process pour écrire le fichier NC.</li>
  </ol>

  <h2>Imbricage automatique (version 8)</h2>
  <p>Selon la FAQ et le guide rapide v8 de SheetCam, l’imbricage automatique s’appuie sur les <strong>parcours déjà créés</strong> (décalage de kerf, entrées et sorties), pas seulement sur le contour. Si vous ouvrez le module sans opération, il ne fait rien. Le logiciel calcule plusieurs variantes ; vous en choisissez une, puis Apply. L’imbricage manuel reste disponible.</p>

  <h2>Ce que cette page ne fait pas</h2>
  <p>Elle ne donne pas de tableau de vitesses, de kerf ou d’avance « pour l’acier doux X mm ». Ces chiffres doivent venir de la charte du fabricant de votre source, puis d’essais sur votre table. Voir le guide <a href="/guides/kerf-qualite-coupe/">Kerf et qualité de coupe</a>.</p>

  <h2>À valider en atelier (Michaël)</h2>
  <ul>
    <li>Quels post-processeurs sont réellement utilisés dans les ateliers québécois que vous connaissez (Machitech, FastCAM, contrôleurs courants, etc.) ?</li>
    <li>Un modèle de job typique (taille de table, origine, unités) à proposer en exemple, sans le présenter comme universel.</li>
    <li>Toute imprécision sur les menus de la v8 par rapport à votre copie de travail.</li>
  </ul>

  <h2>Sources</h2>
  <ul class="source-list">
    <li><a href="https://sheetcamshop.myshopify.com/pages/support">SheetCam LLC — Support Manuals</a> (guides 8.0 et manuels officiels, consulté le 26 novembre 2026).</li>
    <li><a href="https://forum.sheetcam.com/t/where-to-learn-sheetcam/8102">Forum SheetCam — « Where to learn Sheetcam »</a>, réponse de l’équipe (sheetcamCS2), 10 septembre 2024.</li>
    <li>FAQ / aperçu SheetCAM v8.0.1 (imbricage automatique : l’opération doit exister avant le module).</li>
  </ul>
</div>
"""

SHEETCAM_EN = """
<div class="wrap prose">
  <p class="crumb"><a href="/en/guides/">Guides</a> · SheetCam</p>
  <h1>Getting started with SheetCam (French companion)</h1>
  <p class="meta">Draft · updated November 26, 2026 · to be reviewed by Michaël</p>
  <p class="lede">SheetCam is CAM software for 2D cutting — plasma, oxy-fuel, waterjet, laser. It is not a CAD program. The official manuals are in English. This page is a French-first companion, not a substitute for those manuals.</p>

  <h2>Official starting points</h2>
  <p>From <a href="https://sheetcamshop.myshopify.com/pages/support">SheetCam LLC Support Manuals</a>: the 8.0 Quick Start Guide, Auto Nesting Quick Start, 2D CAD Quick Start, and the manual (A4 and US Letter, including a plasma / metric edition). In the software: <strong>Help → Tutorials</strong>.</p>
  <p>According to a SheetCam staff reply on the <a href="https://forum.sheetcam.com/t/where-to-learn-sheetcam/8102">official forum</a>, the trial is the same executable as the licensed build, with no time limit, but it only produces about 180 lines of G-code.</p>

  <h2>Two unit settings, often mixed up</h2>
  <p>The same staff note: linear units are set in <strong>two independent places</strong>.</p>
  <ul>
    <li><strong>Options → Application options</strong> — the design canvas.</li>
    <li><strong>Options → Machine → Post Processor</strong> — the units written into the G-code.</li>
  </ul>
  <p>They do not have to match, but a misunderstood mismatch makes parts come out at the wrong scale. Also: the built-in tutorials <strong>change Job options</strong> (material, work area, table size). Plan to set them back for your machine.</p>

  <h2>Typical workflow (no invented parameters)</h2>
  <p>This sequence follows SheetCam’s documented flow and public quick-start write-ups. Lead lengths, kerf, and speeds must come from <em>your</em> plasma source, post-processor, and tests — not from this page.</p>
  <ol>
    <li><strong>New job.</strong> File → New job, then Options → Job options: work area, thickness if you track it here, origin (often lower left, X0,Y0), rapid clearance.</li>
    <li><strong>Import the drawing.</strong> File → Import drawing… (DXF, SVG, and so on). Match scale and units. A microscopic or gigantic part is almost always a unit mismatch.</li>
    <li><strong>Check geometry.</strong> Open contours, duplicates, or unexploded blocks are best fixed in CAD (see the BricsCAD guide).</li>
    <li><strong>Minimum to get a toolpath.</strong> Per SheetCam staff: at least one Part (a DXF import already lands in a Part), one Layer, one Tool (preferably two), and one Operation (for plasma: Jet / Plasma Cut).</li>
    <li><strong>Plasma operation.</strong> Operations → New operation → Plasma Cut. Typical contour methods: outside for the profile, inside for holes, no offset for marking. Leads and cut direction depend on your torch and chart — do not copy a random “standard” lead length.</li>
    <li><strong>Post-processor.</strong> Options → Machine → Post Processor, pick the one for your control. Then File → Post process to write the NC file.</li>
  </ol>

  <h2>Automatic nesting in version 8</h2>
  <p>Per SheetCam’s v8 FAQ and quick start, AutoNesting uses <strong>existing toolpaths</strong> (kerf offset, lead-in and lead-out), not just raw geometry. Open the module with no operation and it does nothing. The software offers several variants; you pick one and Apply. Manual nesting is still there.</p>

  <h2>What this page will not do</h2>
  <p>It will not publish a speed or kerf table “for X mm mild steel.” Those numbers belong to your manufacturer’s chart and to tests on your table. See <a href="/en/guides/kerf-and-cut-quality/">Kerf and cut quality</a>.</p>

  <h2>For Michaël to review</h2>
  <ul>
    <li>Which post-processors are actually common in the Quebec shops you know?</li>
    <li>A typical job template (table size, origin, units) that we can show as an example, not as a universal default.</li>
    <li>Any v8 menu wording that does not match your working copy.</li>
  </ul>

  <h2>Sources</h2>
  <ul class="source-list">
    <li><a href="https://sheetcamshop.myshopify.com/pages/support">SheetCam LLC — Support Manuals</a> (8.0 guides and official manuals, consulted November 26, 2026).</li>
    <li><a href="https://forum.sheetcam.com/t/where-to-learn-sheetcam/8102">SheetCam forum — “Where to learn Sheetcam”</a>, staff reply (sheetcamCS2), September 10, 2024.</li>
    <li>SheetCAM v8.0.1 FAQ / feature overview (AutoNesting requires an operation first).</li>
  </ul>
</div>
"""

BRICSCAD_FR = """
<div class="wrap prose">
  <p class="crumb"><a href="/guides/">Guides</a> · BricsCAD</p>
  <h1>De BricsCAD à un DXF propre</h1>
  <p class="meta">Brouillon · mis à jour le 26 novembre 2026 · à réviser par Michaël</p>
  <p class="lede">Un DXF « propre » pour SheetCam (ou un autre CAM 2D), c’est un fichier dont les unités, la version et la géométrie correspondent à ce que la FAO sait lire : contours fermés, pas d’objets mandataires, une précision adaptée à la machine.</p>

  <h2>La commande officielle : DXFOUT</h2>
  <p>D’après l’aide BricsCAD (Lite et Pro), <a href="https://help.bricsys.com/en-us/document/command-reference/d/dxfout-command?version=V26">DXFOUT</a> ouvre le dialogue pour enregistrer le dessin courant en DXF. Options documentées :</p>
  <ul>
    <li><strong>Nombre de décimales (0 à 16).</strong> L’aide précise que certaines machines CNC exigent 4 décimales dans le DXF.</li>
    <li><strong>Entities.</strong> Permet d’exporter seulement les entités choisies. Si rien n’est précisé, toutes les entités sont exportées.</li>
    <li><strong>Binary.</strong> Format binaire. Par défaut, le fichier est en ASCII (texte), généralement préférable pour le CAM.</li>
    <li><strong>Version.</strong> Numéro de version du DXF. Par défaut : la plus récente. Exporter vers une version plus ancienne peut faire perdre des entités ou des propriétés.</li>
  </ul>
  <p>La commande <a href="https://helpcenter.bricsys.com/en-us/document/command-reference/e/export-command?version=V27">EXPORT</a> existe aussi pour d’autres formats ; pour un flux plasma typique, DXFOUT reste le point de départ officiel.</p>

  <h2>Objets mandataires et nettoyage</h2>
  <p>Si le dessin contient des objets AEC ou des objets personnalisés que le CAM ne reconnaît pas, l’aide BricsCAD documente <a href="https://help.bricsys.com/en-us/document/command-reference/e/exporttoautocad-command?version=V26">EXPORTTOAUTOCAD</a> pour les convertir en blocs natifs. WBLOCK peut aussi servir à extraire de la géométrie utilisable.</p>
  <p>Avant l’export, un nettoyage habituel (PURGE des définitions inutilisées, y compris imbriquées ; consolidation ou suppression de calques avec les commandes de calques de BricsCAD) réduit les surprises à l’import. Vérifiez que les <strong>unités du dessin</strong> correspondent à celles que SheetCam attend (voir le piège des deux réglages d’unités dans le <a href="/guides/debuter-sheetcam/">guide SheetCam</a>).</p>

  <h2>Liste de contrôle avant le CAM</h2>
  <p>Les points suivants sont des pratiques d’atelier, à valider sur votre flux — pas des garanties du logiciel :</p>
  <ul class="checklist">
    <li>Unités du dessin confirmées (mm ou pouces) et notées pour l’import SheetCam.</li>
    <li>Géométrie de coupe en 2D, contours fermés (polylignes ou arcs joints).</li>
    <li>Calques séparés pour coupe, marquage, pliage ou gravure, selon votre convention.</li>
    <li>Cartouche, cotes, hachures et texte de présentation exclus de l’export (option Entities) s’ils polluent le CAM.</li>
    <li>Pas d’objets mandataires restants ; version DXF et nombre de décimales choisis (4 décimales si votre machine le demande).</li>
    <li>Fichier ASCII plutôt que binaire, sauf raison précise.</li>
  </ul>

  <h2>À valider en atelier (Michaël)</h2>
  <ul>
    <li>Votre convention réelle de calques BricsCAD → SheetCam.</li>
    <li>La version DXF et le nombre de décimales qui fonctionnent avec vos tables.</li>
    <li>Les commandes exactes que vous utilisez (DXFOUT, EXPORT, WBLOCK, EXPORTTOAUTOCAD) selon les types de dessins (pièces simples vs. assemblages).</li>
  </ul>

  <h2>Sources</h2>
  <ul class="source-list">
    <li><a href="https://help.bricsys.com/en-us/document/command-reference/d/dxfout-command?version=V26">BricsCAD Help — commande DXFOUT (V26)</a>, consulté le 26 novembre 2026.</li>
    <li><a href="https://help.bricsys.com/en-us/document/command-reference/e/exporttoautocad-command?version=V26">BricsCAD Help — EXPORTTOAUTOCAD (V26)</a>.</li>
    <li><a href="https://helpcenter.bricsys.com/en-us/document/command-reference/e/export-command?version=V27">BricsCAD Help — EXPORT</a>.</li>
  </ul>
</div>
"""

BRICSCAD_EN = """
<div class="wrap prose">
  <p class="crumb"><a href="/en/guides/">Guides</a> · BricsCAD</p>
  <h1>From BricsCAD to a clean DXF</h1>
  <p class="meta">Draft · updated November 26, 2026 · to be reviewed by Michaël</p>
  <p class="lede">A “clean” DXF for SheetCam (or another 2D CAM) is a file whose units, version, and geometry match what the CAM can read: closed contours, no proxy objects, and precision the machine can use.</p>

  <h2>The official command: DXFOUT</h2>
  <p>According to the BricsCAD (Lite and Pro) help, <a href="https://help.bricsys.com/en-us/document/command-reference/d/dxfout-command?version=V26">DXFOUT</a> saves the current drawing to DXF. Documented options:</p>
  <ul>
    <li><strong>Decimal places (0 to 16).</strong> The help notes that some CNC machines require 4 decimal places in DXF files.</li>
    <li><strong>Entities.</strong> Export only the selected entities. If you leave this unspecified, everything is exported.</li>
    <li><strong>Binary.</strong> Binary format. If unspecified, the file is ASCII (text), usually preferable for CAM.</li>
    <li><strong>Version.</strong> DXF version number. The default is the most current. Exporting to an older version can drop entities or properties.</li>
  </ul>
  <p>The <a href="https://helpcenter.bricsys.com/en-us/document/command-reference/e/export-command?version=V27">EXPORT</a> command also exists for other formats. For a typical plasma workflow, DXFOUT is the official starting point.</p>

  <h2>Proxy objects and cleanup</h2>
  <p>If the drawing holds AEC or custom proxy objects the CAM will not recognize, BricsCAD documents <a href="https://help.bricsys.com/en-us/document/command-reference/e/exporttoautocad-command?version=V26">EXPORTTOAUTOCAD</a> to convert them into native blocks. WBLOCK can also extract usable geometry.</p>
  <p>A usual cleanup before export (PURGE unused definitions, including nested ones; merge or delete leftover layers) reduces import surprises. Confirm that <strong>drawing units</strong> match what SheetCam expects (see the two unit settings in the <a href="/en/guides/getting-started-sheetcam/">SheetCam guide</a>).</p>

  <h2>Pre-CAM checklist</h2>
  <p>Shop practice to confirm on your own workflow — not a software guarantee:</p>
  <ul class="checklist">
    <li>Drawing units confirmed (mm or inches) and noted for the SheetCam import.</li>
    <li>2D cutting geometry, closed contours (joined polylines or arcs).</li>
    <li>Separate layers for cut, mark, bend, or etch, following your shop convention.</li>
    <li>Title blocks, dimensions, hatches, and presentation text left out of the export (Entities option) if they clutter the CAM.</li>
    <li>No leftover proxy objects; DXF version and decimal places chosen (4 places if your machine requires it).</li>
    <li>ASCII rather than binary, unless you have a specific reason.</li>
  </ul>

  <h2>For Michaël to review</h2>
  <ul>
    <li>Your actual BricsCAD → SheetCam layer convention.</li>
    <li>The DXF version and decimal setting that work on your tables.</li>
    <li>Which commands you really use (DXFOUT, EXPORT, WBLOCK, EXPORTTOAUTOCAD) for simple parts versus assemblies.</li>
  </ul>

  <h2>Sources</h2>
  <ul class="source-list">
    <li><a href="https://help.bricsys.com/en-us/document/command-reference/d/dxfout-command?version=V26">BricsCAD Help — DXFOUT (V26)</a>, consulted November 26, 2026.</li>
    <li><a href="https://help.bricsys.com/en-us/document/command-reference/e/exporttoautocad-command?version=V26">BricsCAD Help — EXPORTTOAUTOCAD (V26)</a>.</li>
    <li><a href="https://helpcenter.bricsys.com/en-us/document/command-reference/e/export-command?version=V27">BricsCAD Help — EXPORT</a>.</li>
  </ul>
</div>
"""

KERF_FR = """
<div class="wrap prose">
  <p class="crumb"><a href="/guides/">Guides</a> · Kerf</p>
  <h1>Kerf et qualité de coupe</h1>
  <p class="meta">Brouillon · mis à jour le 26 novembre 2026 · à réviser par Michaël</p>
  <p class="lede">Le kerf est la largeur de matière enlevée par le jet plasma. Si le parcours ne le compense pas, les extérieurs sont trop petits et les trous trop grands. La qualité (bavure, angle, état de surface) dépend de la vitesse, de la hauteur, de l’usure des consommables et de l’état de la table.</p>

  <h2>Comment lire une charte du fabricant</h2>
  <p>Hypertherm, dans ses chartes et dans le guide « How to use the cut charts », présente les valeurs comme un <strong>point de départ</strong>. On y trouve typiquement : épaisseur, hauteur de coupe, hauteur et délai de perçage, réglages « meilleure qualité » (vitesse et tension) et réglages « production » (plus rapides, pas nécessairement le meilleur état de surface). La tension d’arc augmente à mesure que les consommables s’usent ; certains CNC ajustent la hauteur automatiquement.</p>
  <p>Hypertherm indique aussi que les largeurs de kerf publiées sont des <strong>références</strong>, obtenues avec les réglages « Best Quality », et que l’installation et la composition du matériau font varier le résultat réel.</p>
  <div class="callout warn">
    <p><strong>Ne mélangez pas les manuels.</strong> Deux documents officiels du même nom de source peuvent donner des kerfs différents, parce que le chalumeau, le jeu de consommables ou la révision du manuel changent. Utilisez la charte qui correspond à <em>votre</em> système, votre chalumeau et vos consommables.</p>
  </div>

  <h2>Exemple cité — une charte, un montage</h2>
  <p>Le tableau ci-dessous reprend uniquement des largeurs de kerf publiées dans la charte officielle <a href="https://xnet.hypertherm.com/docs/en/Powermax125_retrofit_torch_OM/vkl1065237733940.html">Mild steel — 125 A — air</a> du manuel de chalumeau de modernisation Powermax125, acier doux, air, 125 A, consommables « shielded ». Ce n’est <strong>pas</strong> un tableau universel, ni une recommandation pour une Powermax 45/65/85/105, ni pour un autre chalumeau.</p>
  <div class="table-wrap">
    <table>
      <thead>
        <tr><th>Épaisseur</th><th>Kerf (qualité maximale, selon cette charte)</th></tr>
      </thead>
      <tbody>
        <tr><td>6 mm (1/4 po)</td><td>1,0 mm (0,040 po)</td></tr>
        <tr><td>10 mm (≈ 3/8 po)</td><td>1,1 mm (0,042 po à 3/8 po dans la charte en pouces)</td></tr>
        <tr><td>12 mm (1/2 po)</td><td>1,3 mm (0,051 po)</td></tr>
        <tr><td>25 mm (1 po)</td><td>2,6 mm (0,105 po)</td></tr>
        <tr><td>40 mm (≈ 1 1/2 po)</td><td>3,2 mm (0,122 po à 1 1/2 po)</td></tr>
      </tbody>
    </table>
  </div>
  <p>À titre d’illustration du danger de mélanger les documents : le manuel opérateur Powermax125 (808080) publie une autre table d’« estimated kerf-width compensation » pour un montage « 125 A shielded », avec par exemple 2,2 mm à 6 mm d’épaisseur — donc un chiffre différent, pour un contexte documentaire différent. Nous ne reproduisons pas cette seconde table en entier ici ; allez à la source si c’est votre manuel.</p>

  <h2>Mesurer le kerf sur votre table</h2>
  <p>La méthode la plus honnête reste l’essai : couper une pièce étalon (rectangle ou rond de dimension connue), mesurer le trou et le profil au pied à coulisse, et entrer la compensation réelle dans l’outil SheetCam. Les chartes servent à s’approcher ; elles ne remplacent pas la mesure une fois les consommables usés, l’air humide ou la tôle oxydée.</p>

  <h2>Qualité de coupe, sans chiffres inventés</h2>
  <p>Les manuels Hypertherm lient la « meilleure qualité » à un meilleur angle, moins de bavure et un meilleur état de surface, et la « production » à davantage de pièces. Au-delà, les causes courantes de mauvaise qualité (mauvaise hauteur, consommables usés, air de mauvaise qualité, vitesse trop élevée ou trop basse) sont décrites dans les guides d’entretien et de dépannage du fabricant — pas dans un tableau inventé ici. Voir aussi <a href="/guides/consommables-plasma-canada/">Consommables plasma et achats au Canada</a>.</p>

  <h2>À valider en atelier (Michaël)</h2>
  <ul>
    <li>Quelles sources et quels chalumeaux sont les plus courants chez vos lecteurs cibles, pour citer les bonnes chartes ensuite ?</li>
    <li>Votre méthode personnelle de mesure du kerf et de mise à jour dans SheetCam.</li>
    <li>Toute formulation trop générale sur la bavure ou l’angle.</li>
  </ul>

  <h2>Sources</h2>
  <ul class="source-list">
    <li><a href="https://xnet.hypertherm.com/docs/en/Powermax125_retrofit_torch_OM/vkl1065237733940.html">Hypertherm — Mild steel, 125 A, air cut chart</a> (chalumeau de modernisation Powermax125), consulté le 26 novembre 2026.</li>
    <li><a href="https://xnet.hypertherm.com/docs/en/Powermax125_retrofit_torch_OM/bzv0315406918125.html">Hypertherm — How to use the cut charts</a>.</li>
    <li>Manuel opérateur Powermax125, 808080 (table d’estimation du kerf, contexte distinct ; exemplaire public chez des distributeurs, p. ex. documents PDF de weldersupply.com).</li>
  </ul>
</div>
"""

KERF_EN = """
<div class="wrap prose">
  <p class="crumb"><a href="/en/guides/">Guides</a> · Kerf</p>
  <h1>Kerf and cut quality</h1>
  <p class="meta">Draft · updated November 26, 2026 · to be reviewed by Michaël</p>
  <p class="lede">Kerf is the width of material the plasma jet removes. If the toolpath does not compensate for it, outsides come out small and holes come out large. Cut quality (dross, bevel, surface finish) depends on speed, height, consumable wear, and the state of the table.</p>

  <h2>How to read a manufacturer chart</h2>
  <p>Hypertherm, in its charts and in “How to use the cut charts,” presents the values as a <strong>starting point</strong>. You typically get: thickness, cut height, pierce height and delay, “best quality” settings (speed and voltage), and “production” or “highest production” settings (faster, not necessarily the best finish). Arc voltage rises as consumables wear; some CNCs trim torch height automatically.</p>
  <p>Hypertherm also says published kerf widths are <strong>for reference</strong>, taken with Best Quality settings, and that installation and material composition will change the real result.</p>
  <div class="callout warn">
    <p><strong>Do not mix manuals.</strong> Two official documents for the same source family can list different kerf values, because the torch, consumable set, or manual revision is different. Use the chart that matches <em>your</em> system, torch, and consumables.</p>
  </div>

  <h2>A cited example — one chart, one setup</h2>
  <p>The table below copies kerf widths published in the official <a href="https://xnet.hypertherm.com/docs/en/Powermax125_retrofit_torch_OM/vkl1065237733940.html">Mild steel — 125 A — air</a> chart from the Powermax125 retrofit-torch manual, mild steel, air, 125 A, shielded consumables. It is <strong>not</strong> a universal table, and not a recommendation for a Powermax 45/65/85/105 or another torch.</p>
  <div class="table-wrap">
    <table>
      <thead>
        <tr><th>Thickness</th><th>Kerf (best quality, per this chart)</th></tr>
      </thead>
      <tbody>
        <tr><td>6 mm (1/4 in)</td><td>1.0 mm (0.040 in)</td></tr>
        <tr><td>10 mm (≈ 3/8 in)</td><td>1.1 mm (0.042 in at 3/8 in in the inch chart)</td></tr>
        <tr><td>12 mm (1/2 in)</td><td>1.3 mm (0.051 in)</td></tr>
        <tr><td>25 mm (1 in)</td><td>2.6 mm (0.105 in)</td></tr>
        <tr><td>40 mm (≈ 1-1/2 in)</td><td>3.2 mm (0.122 in at 1-1/2 in)</td></tr>
      </tbody>
    </table>
  </div>
  <p>As a warning against mixing documents: Powermax125 Operator Manual 808080 publishes a separate “estimated kerf-width compensation” table for a “125 A shielded” setup, for example 2.2 mm at 6 mm thickness — a different number, in a different documentary context. We do not reproduce that second table in full here; go to the source if that is your manual.</p>

  <h2>Measuring kerf on your table</h2>
  <p>The honest method is still a test cut: a coupon of known size, measured with calipers, then the real compensation entered into the SheetCam tool. Charts get you close. They do not replace a measurement once consumables are worn, air is wet, or the plate is rusty.</p>

  <h2>Cut quality, with no invented numbers</h2>
  <p>Hypertherm manuals tie “best quality” to better angle, less dross, and a better finish, and “production” to more parts. Common causes of a poor cut (wrong height, worn consumables, poor air, speed too high or too low) belong in the manufacturer’s care and troubleshooting guides — not in a table invented here. See also <a href="/en/guides/plasma-consumables-canada/">Plasma consumables and buying in Canada</a>.</p>

  <h2>For Michaël to review</h2>
  <ul>
    <li>Which sources and torches are most common among the shops you want to reach, so later drafts can cite the right charts?</li>
    <li>Your own method for measuring kerf and updating SheetCam.</li>
    <li>Any wording about dross or bevel that is too sweeping.</li>
  </ul>

  <h2>Sources</h2>
  <ul class="source-list">
    <li><a href="https://xnet.hypertherm.com/docs/en/Powermax125_retrofit_torch_OM/vkl1065237733940.html">Hypertherm — Mild steel, 125 A, air cut chart</a> (Powermax125 retrofit torch), consulted November 26, 2026.</li>
    <li><a href="https://xnet.hypertherm.com/docs/en/Powermax125_retrofit_torch_OM/bzv0315406918125.html">Hypertherm — How to use the cut charts</a>.</li>
    <li>Powermax125 Operator Manual 808080 (estimated kerf-width compensation table, a distinct context; public distributor PDFs, e.g. weldersupply.com).</li>
  </ul>
</div>
"""

CONSOM_FR = """
<div class="wrap prose">
  <p class="crumb"><a href="/guides/">Guides</a> · Consommables</p>
  <h1>Consommables plasma et achats au Canada</h1>
  <p class="meta">Brouillon · mis à jour le 26 novembre 2026 · à réviser par Michaël</p>
  <p class="lede">Les consommables (électrode, buse, anneau de turbulence, capuchon, parfois une cartouche complète sur les systèmes SYNC) déterminent autant la qualité de coupe que la source elle-même. Cette page ne publie pas de prix ni de liens d’affiliation.</p>

  <h2>Ce que dit le fabricant sur l’entretien</h2>
  <p>Hypertherm, dans ses ressources d’entretien préventif Powermax et son guide de soin des consommables, recommande notamment :</p>
  <ul>
    <li>Utiliser des consommables genuins et les inspecter régulièrement (souvent présenté comme un contrôle quotidien).</li>
    <li>Remplacer <strong>l’électrode et la buse ensemble</strong> lorsque la fosse de l’électrode atteint 1,6 mm (1/16 po), ou lorsque l’orifice de la buse n’est plus rond, est ébréché ou a les bords arrondis.</li>
    <li>Ne remplacer l’anneau de turbulence que s’il est fêlé, usé, ou si ses trous de gaz sont bouchés ou déformés ; il dure en général plusieurs changements d’électrode et de buse.</li>
  </ul>
  <p>Les durées de vie en heures d’arc varient énormément selon l’épaisseur, la longueur des coupes, le perçage et la qualité de l’air. Un manuel (Powermax30 AIR) donne un ordre de grandeur d’environ 1 à 2 heures d’arc pour cette machine — ce n’est pas une prévision pour une Powermax 65 ou une source haute définition. Nous ne publions pas de « durée typique » inventée pour d’autres sources.</p>
  <p>La qualité de l’air (sécheresse, filtration) revient souvent dans les guides de dépannage du fabricant comme cause d’usure prématurée. Vérifiez le sécheur et les filtres avant d’accuser seulement les pièces.</p>

  <h2>Familles et compatibilité</h2>
  <p>Les numéros de pièces doivent correspondre à la famille de chalumeau (par exemple Duramax, FineCut, ou cartouches SYNC). Un « compatible » bon marché peut convenir à certains ateliers ; Hypertherm positionne ses consommables d’origine autour de la qualité de coupe et de la garantie du système. Nous n’avons pas de banc d’essai CoupeFab à citer pour l’instant : choisissez en connaissance de cause, et gardez les numéros de pièces de votre manuel.</p>
  <p>Les systèmes Powermax SYNC utilisent une cartouche plutôt qu’un empilement traditionnel. Les procédures d’inspection et les chartes à utiliser sont celles de <em>cette</em> famille, pas celles d’un chalumeau plus ancien.</p>

  <h2>Acheter au Canada — pistes, pas de catalogue</h2>
  <p>Il existe des distributeurs et détaillants canadiens qui affichent des consommables Hypertherm ou des équivalents, avec livraison au pays. Exemples publics, à titre d’orientation seulement (pas de recommandation d’achat, pas de lien affilié) :</p>
  <ul>
    <li><a href="https://famsales.ca/">FAM Sales Corporation</a> (Colombie-Britannique) — se présente comme distributeur Hypertherm et Hougen.</li>
    <li><a href="https://mapleweld.ca/collections/hypertherm">MapleWeld</a> (Toronto) — collection Hypertherm affichée publiquement.</li>
    <li><a href="https://gmweldingsupplies.ca/product/plasma-consumables-powermax-45-65-85-duramax">GM Welding Supplies</a> — consommables Powermax 45/65/85 Duramax affichés.</li>
  </ul>
  <p>Au Québec, plusieurs gaziers, soudeurs-détaillants et constructeurs de tables (dont des fabricants québécois de tables plasma) vendent aussi des consommables. Nous n’inventons pas leurs prix ni leurs stocks. Commandez avec le numéro de pièce du manuel, confirmez la compatibilité du chalumeau, et prévoyez les délais et, le cas échéant, les frais si la pièce vient des États-Unis.</p>

  <h2>À valider en atelier (Michaël)</h2>
  <ul>
    <li>Fournisseurs québécois que vous utilisez vraiment (sans en faire une pub si vous n’êtes pas à l’aise).</li>
    <li>Votre pratique de remplacement (quand vous changez réellement électrode et buse, ce que vous voyez sur la coupe).</li>
    <li>Toute mention trop générale sur les pièces « compatibles ».</li>
  </ul>

  <h2>Sources</h2>
  <ul class="source-list">
    <li><a href="https://www.hypertherm.com/resources/more-resources/videos/powermax-preventive-maintenance/">Hypertherm — Powermax preventive maintenance</a>, consulté le 26 novembre 2026.</li>
    <li>Hypertherm — Consumable care guide (document de bibliothèque xNet, fichier HYP116271).</li>
    <li><a href="https://www.hypertherm.com/solutions/consumables-and-torches/for-powermax-and-max-systems/">Hypertherm — Torches and consumables for Powermax and Max systems</a>.</li>
  </ul>
</div>
"""

CONSOM_EN = """
<div class="wrap prose">
  <p class="crumb"><a href="/en/guides/">Guides</a> · Consumables</p>
  <h1>Plasma consumables and buying in Canada</h1>
  <p class="meta">Draft · updated November 26, 2026 · to be reviewed by Michaël</p>
  <p class="lede">Consumables (electrode, nozzle, swirl ring, shield, or a full cartridge on SYNC systems) do as much for cut quality as the power source itself. This page publishes no prices and no affiliate links.</p>

  <h2>What the manufacturer says about care</h2>
  <p>Hypertherm, in its Powermax preventive-maintenance material and consumable care guide, recommends among other things:</p>
  <ul>
    <li>Use genuine consumables and inspect them regularly (often framed as a daily check).</li>
    <li>Replace the <strong>electrode and nozzle together</strong> when the electrode pit reaches 1.6 mm (1/16 in), or when the nozzle orifice is no longer round, is nicked, or has rounded edges.</li>
    <li>Replace the swirl ring only if it is cracked, worn, or its gas holes are blocked or deformed; it usually lasts through several electrode and nozzle changes.</li>
  </ul>
  <p>Arc-on life varies widely with thickness, cut length, piercing, and air quality. One manual (Powermax30 AIR) gives a rough 1–2 hours of arc time for that machine — not a forecast for a Powermax 65 or a high-definition source. We will not invent a “typical life” for other systems.</p>
  <p>Air quality (dryness, filtration) shows up often in the manufacturer’s troubleshooting guides as a cause of early wear. Check the dryer and filters before blaming the parts alone.</p>

  <h2>Families and compatibility</h2>
  <p>Part numbers must match the torch family (for example Duramax, FineCut, or SYNC cartridges). A cheaper “compatible” stack may be fine for some shops; Hypertherm positions genuine consumables around cut quality and system warranty. CoupeFab has no test bench to cite yet: choose with your eyes open, and keep the part numbers from your manual.</p>
  <p>Powermax SYNC systems use a cartridge rather than a traditional stack. Inspection steps and cut charts must come from <em>that</em> family, not from an older torch.</p>

  <h2>Buying in Canada — leads, not a catalogue</h2>
  <p>Canadian distributors and retailers do list Hypertherm consumables or equivalents, with shipping in Canada. Public examples, for orientation only (not an endorsement, no affiliate link):</p>
  <ul>
    <li><a href="https://famsales.ca/">FAM Sales Corporation</a> (British Columbia) — presents itself as a Hypertherm and Hougen distributor.</li>
    <li><a href="https://mapleweld.ca/collections/hypertherm">MapleWeld</a> (Toronto) — a public Hypertherm collection.</li>
    <li><a href="https://gmweldingsupplies.ca/product/plasma-consumables-powermax-45-65-85-duramax">GM Welding Supplies</a> — listed Powermax 45/65/85 Duramax consumables.</li>
  </ul>
  <p>In Quebec, gas suppliers, welding retailers, and table builders (including Quebec plasma-table makers) also sell consumables. We will not invent their prices or stock. Order with the manual’s part number, confirm torch compatibility, and allow for lead time and, if the part ships from the United States, any extra fees.</p>

  <h2>For Michaël to review</h2>
  <ul>
    <li>Quebec suppliers you actually use (we can name them only if you are comfortable doing so).</li>
    <li>Your real replacement practice (when you change electrode and nozzle, what you see on the cut).</li>
    <li>Any wording about “compatible” parts that feels too broad.</li>
  </ul>

  <h2>Sources</h2>
  <ul class="source-list">
    <li><a href="https://www.hypertherm.com/resources/more-resources/videos/powermax-preventive-maintenance/">Hypertherm — Powermax preventive maintenance</a>, consulted November 26, 2026.</li>
    <li>Hypertherm — Consumable care guide (xNet library document, file HYP116271).</li>
    <li><a href="https://www.hypertherm.com/solutions/consumables-and-torches/for-powermax-and-max-systems/">Hypertherm — Torches and consumables for Powermax and Max systems</a>.</li>
  </ul>
</div>
"""

OCCASIONS_FR = """
<div class="wrap prose" style="max-width:72rem">
  <p class="kicker">Occasions Québec · digest n° 1</p>
  <h1 class="page-title">Évaluer une table plasma usagée au Québec</h1>
  <p class="meta">Brouillon · relevé le 26 novembre 2026 (America/Toronto) · à réviser par Michaël</p>
  <p class="lede">Cette page combine une liste de vérification pour l’achat d’une table usagée, et un premier digest d’annonces <strong>publiques</strong> actuellement en ligne. CoupeFab n’est pas un courtier. Les prix changent, les machines partent, et deux sites peuvent décrire la même table. Vérifiez toujours auprès du vendeur.</p>

  <h2>Méthode du digest</h2>
  <p>Nous relions seulement des pages publiques de courtiers, d’encanteurs ou d’annonces (par exemple Machinerie ALX, Industriel Go / Machinio, Tardif Industrie, Ritchie Bros. / IronPlanet). Pas d’aspiration massive, pas de contournement de connexion. Si un prix n’est pas affiché, nous écrivons « prix sur demande ». La date et le fuseau du relevé sont indiqués ci-dessus.</p>

  <h2>Liste de vérification (achat au Québec)</h2>
  <ul class="checklist">
    <li><strong>Enveloppe de l’atelier.</strong> Dimensions utiles contre portes, pont roulant et hauteur ; tension réelle (208 / 460 / 600 V, mono ou triphasé) ; air comprimé et sécheur ; dépoussiéreur ou table à eau déjà en place.</li>
    <li><strong>Source plasma et chalumeau.</strong> Marque et modèle, intensité, famille de consommables, heures si elles existent, THC fonctionnel. Une « capacité de coupe » publicitaire n’est pas une qualité de production — demandez à voir couper votre épaisseur typique.</li>
    <li><strong>Mécanique.</strong> Jeu des crémaillères ou vis, équerrage du portique, état des rails, câbles et goulottes, rouilles sur la table, fuites d’eau le cas échéant.</li>
    <li><strong>Contrôle et licences.</strong> Contrôleur (Edge, Vision T5, etc.), sauvegardes, logiciels CAM et leurs licences (SheetCam, FastCAM, ou autre) : ce qui est inclus, ce qui est à racheter.</li>
    <li><strong>Historique.</strong> Rétrofit (quand, par qui, quelles pièces), disponibilité des pièces au Canada, documentation d’origine.</li>
    <li><strong>Essai.</strong> Voir la machine couper. Mesurer une pièce étalon (kerf, bavure, équerrage). Écouter les fins de course et les défauts d’arc.</li>
    <li><strong>Logistique et contrat.</strong> Vendu tel quel, démantèlement, transport, taxes (TPS/TVQ), délai de disponibilité. Un prix « sorti d’usine » sans déplacement ni grue n’est pas un prix rendu dans votre cour.</li>
  </ul>
  <p>Cette liste est un canevas d’atelier, pas une expertise. Michaël devrait la compléter avec les points qu’il vérifie systématiquement.</p>

  <h2>Digest n° 1 — annonces publiques relevées le 26 novembre 2026</h2>
  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>Machine</th>
          <th>Lieu / vendeur</th>
          <th>Prix affiché</th>
          <th>Notes (telles que publiées)</th>
          <th>Source</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Machitech Automation EC-300 (2015), table 5 × 5 pi, Hypertherm Powermax45</td>
          <td>Farnham (QC), vendeur Industriel Go (Montréal-Nord)</td>
          <td>Sur demande</td>
          <td>45 A ; « excellent working condition », « fully operational » selon l’annonce ; capacité de séparation jusqu’à 1 po « selon les conditions de coupe » (texte du vendeur, à vérifier).</td>
          <td><a href="https://www.machinio.com/listings/119721949-2015-machitech-automation-ec-300-cnc-plasma-cutting-table-5-x-5-hypertherm-powermax45-included-in-farnham-canada">Machinio</a> · <a href="https://www.industrielgo.com/listings/9640734-used-2015-machitech-automation-ec-300-cnc-plasma-cutting-table-5-x-5-hypertherm-powermax45-included">Industriel Go</a></td>
        </tr>
        <tr>
          <td>E.B.F PL1026 (2011), 10 × 26 pi, 2 têtes, 2 × Hypertherm HPR260XD, EdgePro, dépoussiéreur</td>
          <td>Québec (courtier) — voir les deux pages</td>
          <td>45 000 $ sur Tardif Industrie ; « Demander le prix » chez Machinerie ALX</td>
          <td>Les deux pages publiques décrivent les mêmes spécifications et la mention « fonctionnelle / en production, disponible immédiatement ». Il peut s’agir de la même machine listée deux fois — à confirmer avant tout déplacement. Devise non explicitée sur Tardif ; site québécois.</td>
          <td><a href="https://machineriealx.com/machines/table-de-decoupe-plasma-cnc-e-b-f-2011/">Machinerie ALX</a> · <a href="https://www.tardifindustrie.com/equipement/dcoupe-plasma-10x26">Tardif Industrie</a></td>
        </tr>
        <tr>
          <td>ESAB Sabre EXE 2005, rétrofit contrôleur 2018 (T5 Vision), table 10 × 40 pi, 3 têtes</td>
          <td>Québec, Machinerie ALX</td>
          <td>Sur demande</td>
          <td>300 A, 600 V ; coupe annoncée 1 ½ po en plasma et 5 po en oxycoupage (texte du vendeur). Vendu tel quel, sans garantie ; démantèlement/emballage inclus selon l’annonce, transport à la charge de l’acheteur. Payable avant le démantèlement.</td>
          <td><a href="https://machineriealx.com/machines/cnc-laser-esab-sabre-exe-2005-retrofit-2017/">Machinerie ALX</a></td>
        </tr>
        <tr>
          <td>ESAB Avenger X 5000 (2015), table 14 × 28 pi (hors-tout 22 × 42 pi), 1 tête plasma + 2 têtes oxy, source ESAB EPP-450, Vision T5</td>
          <td>Machinerie ALX</td>
          <td>Sur demande</td>
          <td>Annoncée opérationnelle lors de la dernière utilisation à l’automne 2025, inutilisée depuis. Démantèlement et transport par l’acheteur ; pont roulant sur place ; documentation d’origine disponible, d’après l’annonce.</td>
          <td><a href="https://machineriealx.com/machines/cnc-plasma-esab-avenger-x-5000/">Machinerie ALX</a></td>
        </tr>
        <tr>
          <td>HD EBF Hypertherm XPR 300 (2022), 78 × 150 po</td>
          <td>Québec (QC), Ritchie Bros. / IronPlanet, article 14972875</td>
          <td>137 500 $ CA (achat immédiat, tel quel)</td>
          <td>Annoncée avec dépoussiéreur. Vendu tel quel, sans IronClad Assurance. Des frais de transaction et des taxes québécoises peuvent s’appliquer (barème publié sur la fiche). Enlèvement : pas de quai ni de chariot élévateur selon la fiche ; remorque de type RGN ou avec rampes ; préavis 24 h.</td>
          <td><a href="https://www.ironplanet.com/for-sale/Welding-Machines-and-Equipment-2022-HD-EBF-Hypertherm-XPR-300-78%E2%80%9Dx150%E2%80%9D-Plasma-Cutter-Quebec/14972875">IronPlanet</a> · <a href="https://www.rbauction.com/pdp/2022-hd-ebf-hypertherm-xpr-300-78x150-plasma-cutter/14972875">Ritchie Bros.</a></td>
        </tr>
        <tr>
          <td>Powertek CUT-40 (2026), neuf / unused — découpeur, pas une table CNC</td>
          <td>Mont-Saint-Hilaire (QC), catégorie Ritchie Bros.</td>
          <td>Enchère (fermeture affichée : mardi 8 décembre, au moment du relevé)</td>
          <td>Inclus parce qu’il est au Québec et public, mais ce n’est <strong>pas</strong> une table de découpe CNC. Vérifiez l’état du lot et la date de clôture sur la page de l’encanteur avant de vous déplacer — les enchères bougent vite.</td>
          <td><a href="https://www.rbauction.qc.ca/cp/decoupeur-au-plasma">Ritchie Bros. — Découpeurs au plasma</a></td>
        </tr>
        <tr>
          <td>Trumpf TrumaBend V 200 (2002), presse plieuse 200 t × 12 pi, commande DELEM DA 65</td>
          <td>Machinerie ALX</td>
          <td>Sur demande</td>
          <td>Série B 0106 A 0018 ; 5 hp ; 460 V / 45 kVA, 60 A (selon l’annonce) ; poids annoncé 39 680 lb. <strong>Disponible le 15 mars 2026</strong>.</td>
          <td><a href="https://machineriealx.com/machines/presse-plieuse-trumpf-v200-200-tonne-2002/">Machinerie ALX</a></td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="callout">
    <p>Pas d’avis « bonne affaire » dans ce premier digest : ces notes viendront après la relecture de Michaël. Sur Kijiji, au moment du relevé, les annonces « table plasma CNC » complètes au Québec étaient rares ; plusieurs résultats canadiens étaient des tables neuves hors province ou des ensembles mécaniques. Nous n’avons pas forcé l’ajout d’annonces trop minces ou hors sujet.</p>
  </div>

  <h2>À valider (Michaël)</h2>
  <ul>
    <li>La possible double inscription E.B.F PL1026 (ALX et Tardif) et le prix de 45 000 $.</li>
    <li>Une note d’atelier sur chaque machine (ou un refus de commenter sans visite).</li>
    <li>D’autres sources québécoises à suivre chaque semaine (Facebook Marketplace, encans locaux, etc.), toujours via des pages publiques.</li>
  </ul>
</div>
"""

OCCASIONS_EN = """
<div class="wrap prose" style="max-width:72rem">
  <p class="kicker">Used equipment in Quebec · digest no. 1</p>
  <h1 class="page-title">Evaluating a used plasma table in Quebec</h1>
  <p class="meta">Draft · surveyed November 26, 2026 (America/Toronto) · to be reviewed by Michaël</p>
  <p class="lede">This page pairs a buyer’s checklist with a first digest of <strong>public</strong> listings currently online. CoupeFab is not a broker. Prices move, machines sell, and two sites may describe the same table. Always confirm with the seller.</p>

  <h2>How the digest is built</h2>
  <p>We only link public dealer, auction, or classified pages (for example Machinerie ALX, Industriel Go / Machinio, Tardif Industrie, Ritchie Bros. / IronPlanet). No bulk scraping, no login walls. If no price is posted, we write “ask for price.” The survey date and time zone are listed above.</p>

  <h2>Checklist (buying in Quebec)</h2>
  <ul class="checklist">
    <li><strong>Shop envelope.</strong> Useful size versus doors, crane, and height; real voltage (208 / 460 / 600 V, single or three phase); compressed air and dryer; dust collector or water table already in place.</li>
    <li><strong>Plasma source and torch.</strong> Brand and model, amperage, consumable family, hours if they exist, working THC. An advertised “severance capacity” is not production quality — ask to see your typical thickness cut.</li>
    <li><strong>Mechanics.</strong> Backlash in racks or screws, gantry square, rail condition, cables and carriers, rust on the slats, water leaks if it is a water table.</li>
    <li><strong>Control and licences.</strong> Controller (Edge, Vision T5, and so on), backups, CAM software and licences (SheetCam, FastCAM, or other): what is included, what you would have to buy again.</li>
    <li><strong>History.</strong> Retrofits (when, by whom, which parts), parts availability in Canada, original documentation.</li>
    <li><strong>A test cut.</strong> Watch it cut. Measure a coupon (kerf, dross, square). Listen for limit switches and arc faults.</li>
    <li><strong>Logistics and contract.</strong> As-is terms, dismantling, transport, taxes (GST/QST), availability date. An “ex-works” price is not a delivered-in-your-yard price.</li>
  </ul>
  <p>This is a shop-floor canvas, not an inspection report. Michaël should add the points he always checks.</p>

  <h2>Digest no. 1 — public listings surveyed November 26, 2026</h2>
  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>Machine</th>
          <th>Location / seller</th>
          <th>Posted price</th>
          <th>Notes (as published)</th>
          <th>Source</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Machitech Automation EC-300 (2015), 5 × 5 ft table, Hypertherm Powermax45</td>
          <td>Farnham, QC, seller Industriel Go (Montréal-Nord)</td>
          <td>Ask for price</td>
          <td>45 A; “excellent working condition,” “fully operational” per the listing; severance up to 1 in “subject to cutting conditions” (seller’s wording, to be verified).</td>
          <td><a href="https://www.machinio.com/listings/119721949-2015-machitech-automation-ec-300-cnc-plasma-cutting-table-5-x-5-hypertherm-powermax45-included-in-farnham-canada">Machinio</a> · <a href="https://www.industrielgo.com/listings/9640734-used-2015-machitech-automation-ec-300-cnc-plasma-cutting-table-5-x-5-hypertherm-powermax45-included">Industriel Go</a></td>
        </tr>
        <tr>
          <td>E.B.F PL1026 (2011), 10 × 26 ft, 2 heads, 2 × Hypertherm HPR260XD, EdgePro, dust collector</td>
          <td>Quebec (dealer) — see both pages</td>
          <td>$45,000 on Tardif Industrie; “ask for price” on Machinerie ALX</td>
          <td>Both public pages describe the same specifications and “in production / available immediately.” This may be one machine listed twice — confirm before you travel. Currency is not explicit on Tardif; it is a Quebec site.</td>
          <td><a href="https://machineriealx.com/machines/table-de-decoupe-plasma-cnc-e-b-f-2011/">Machinerie ALX</a> · <a href="https://www.tardifindustrie.com/equipement/dcoupe-plasma-10x26">Tardif Industrie</a></td>
        </tr>
        <tr>
          <td>ESAB Sabre EXE 2005, 2018 controller retrofit (T5 Vision), 10 × 40 ft table, 3 heads</td>
          <td>Quebec, Machinerie ALX</td>
          <td>Ask for price</td>
          <td>300 A, 600 V; advertised cut 1-1/2 in plasma and 5 in oxy-fuel (seller’s wording). Sold as-is, no warranty; dismantling/packing included per the listing, transport at the buyer’s cost. Payable before dismantling.</td>
          <td><a href="https://machineriealx.com/machines/cnc-laser-esab-sabre-exe-2005-retrofit-2017/">Machinerie ALX</a></td>
        </tr>
        <tr>
          <td>ESAB Avenger X 5000 (2015), 14 × 28 ft table (22 × 42 ft overall), 1 plasma + 2 oxy torches, ESAB EPP-450, Vision T5</td>
          <td>Machinerie ALX</td>
          <td>Ask for price</td>
          <td>Listed as operational at last use in autumn 2025, unused since. Buyer dismantles and ships; overhead crane on site; original documentation available, per the listing.</td>
          <td><a href="https://machineriealx.com/machines/cnc-plasma-esab-avenger-x-5000/">Machinerie ALX</a></td>
        </tr>
        <tr>
          <td>HD EBF Hypertherm XPR 300 (2022), 78 × 150 in</td>
          <td>Québec, QC, Ritchie Bros. / IronPlanet item 14972875</td>
          <td>CAD $137,500 (buy now, as-is)</td>
          <td>Listed with a dust collector. Sold as-is, no IronClad Assurance. Transaction fees and Quebec tax may apply (schedule on the listing). Pickup: no dock or forklift per the listing; RGN or a trailer with ramps; 24-hour notice.</td>
          <td><a href="https://www.ironplanet.com/for-sale/Welding-Machines-and-Equipment-2022-HD-EBF-Hypertherm-XPR-300-78%E2%80%9Dx150%E2%80%9D-Plasma-Cutter-Quebec/14972875">IronPlanet</a> · <a href="https://www.rbauction.com/pdp/2022-hd-ebf-hypertherm-xpr-300-78x150-plasma-cutter/14972875">Ritchie Bros.</a></td>
        </tr>
        <tr>
          <td>Powertek CUT-40 (2026), unused — handheld/source cutter, not a CNC table</td>
          <td>Mont-Saint-Hilaire, QC, Ritchie Bros. category page</td>
          <td>Auction (closing shown as Tuesday, December 8, at the time of the survey)</td>
          <td>Included because it is in Quebec and public, but it is <strong>not</strong> a CNC cutting table. Confirm lot status and closing date on the auctioneer’s page before you travel — auctions move quickly.</td>
          <td><a href="https://www.rbauction.qc.ca/cp/decoupeur-au-plasma">Ritchie Bros. — Plasma cutters</a></td>
        </tr>
        <tr>
          <td>Trumpf TrumaBend V 200 (2002), 200 ton × 12 ft press brake, DELEM DA 65 control</td>
          <td>Machinerie ALX</td>
          <td>Ask for price</td>
          <td>Serial B 0106 A 0018; 5 hp; 460 V / 45 kVA, 60 A (per the listing); advertised weight 39,680 lb. <strong>Available March 15, 2026</strong>.</td>
          <td><a href="https://machineriealx.com/machines/presse-plieuse-trumpf-v200-200-tonne-2002/">Machinerie ALX</a></td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="callout">
    <p>No “good deal” notes in this first digest: those will come after Michaël’s review. On Kijiji at the time of the survey, complete CNC plasma tables in Quebec were scarce; many Canadian hits were new tables outside the province or mechanical kits. We did not stretch thin or off-topic ads into the list.</p>
  </div>

  <h2>For Michaël to review</h2>
  <ul>
    <li>The possible duplicate E.B.F PL1026 listing (ALX and Tardif) and the $45,000 figure.</li>
    <li>A shop-floor note on each machine (or a refusal to comment without a visit).</li>
    <li>Other Quebec sources to follow weekly (Marketplace, local auctions), still through public pages only.</li>
  </ul>
</div>
"""

PRIX_FR = """
<div class="wrap prose" style="max-width:52rem">
  <p class="kicker">Prix des tôles</p>
  <h1 class="page-title">Prix des tôles au Québec</h1>
  <p class="meta">Brouillon · première comparaison · sources consultées le 26 novembre 2026 (America/Toronto) · à réviser par Michaël</p>
  <p class="lede">Beaucoup d’ateliers paieraient pour un comparatif honnête de l’acier, de l’inox et de l’aluminium en feuille. En pratique, la plupart des fournisseurs québécois restent en « prix sur demande ». CoupeFab n’invente aucun prix : seulement des listes publiques, datées et liées.</p>

  <h2>Méthode</h2>
  <ol>
    <li>Ne retenir que des pages publiques, consultables sans compte.</li>
    <li>Noter la date de mise à jour affichée par la source, et la date de notre consultation.</li>
    <li>Reproduire les unités telles quelles ($/pi² ou $/lb). Ne pas convertir sans le dire, et ne pas mélanger les unités dans une même colonne sans étiquette.</li>
    <li>Indiquer clairement qu’un prix affiché est indicatif, souvent hors transformation, quantité, format et disponibilité.</li>
    <li>Si une seule source publique est trouvée pour un produit, le dire : ce n’est pas un marché complet, c’est un point de repère.</li>
  </ol>
  <p>Cette première édition n’a trouvé <strong>qu’une</strong> liste publique québécoise assez détaillée pour un tableau : <a href="https://unitedstainless.ca/live-prices">unitedstainless.ca/live-prices</a> (United Stainless / Alluminox Spec, Saint-Hubert, Rive-Sud de Montréal). D’autres acteurs (services centres, distributeurs nationaux) n’affichaient pas, au moment du relevé, une grille comparable de tôles en $/pi². Nous n’avons pas comblé les trous avec des rumeurs de cour ou des indices boursiers.</p>

  <h2>United Stainless — liste indicative</h2>
  <p>La page indique : « Last updated: October 22, 2026 ». United Stainless précise qu’il s’agit d’un atelier de fabrication sur mesure, que la liste sert à estimer un projet avant une soumission, et que l’on ne commande pas la matière à partir de cette grille. Les conditions d’utilisation du site le répètent : prix indicatifs seulement ; le prix final dépend de la quantité, de la disponibilité, de la transformation et du marché.</p>

  <h3>Tôle inox 304L — prix au pied carré</h3>
  <p>Lorsque la même description apparaissait plusieurs fois au même prix, une seule ligne est retenue.</p>
  <div class="table-wrap">
    <table>
      <thead><tr><th>Description (telle qu’affichée)</th><th>Prix affiché</th></tr></thead>
      <tbody>
        <tr><td>11 ga / .125 (304L)</td><td>3,32 $/pi²</td></tr>
        <tr><td>12 ga / .109 (304L)</td><td>3,32 $/pi²</td></tr>
        <tr><td>14 ga / .0781 (304L)</td><td>3,32 $/pi²</td></tr>
        <tr><td>10 g / .140 (304L)</td><td>3,90 $/pi²</td></tr>
        <tr><td>16 ga / .0625 (304L)</td><td>4,23 $/pi²</td></tr>
        <tr><td>18 ga / .050 (304L)</td><td>4,29 $/pi²</td></tr>
        <tr><td>3/16 / .1875 (304L)</td><td>4,94 $/pi²</td></tr>
        <tr><td>1/4 / .250 (304L)</td><td>5,72 $/pi²</td></tr>
        <tr><td>20 ga / .0375 (304L)</td><td>6,76 $/pi²</td></tr>
      </tbody>
    </table>
  </div>

  <h3>Tôle inox 316L — attention aux unités</h3>
  <p>Sur la même page, les lignes 316L consultées étaient affichées <strong>au livre</strong>, pas au pied carré. Ce n’est pas comparable d’un coup d’œil avec le 304L ci-dessus.</p>
  <div class="table-wrap">
    <table>
      <thead><tr><th>Description (telle qu’affichée)</th><th>Prix affiché</th></tr></thead>
      <tbody>
        <tr><td>1/8, (316L)</td><td>4,20 $/lb</td></tr>
        <tr><td>3/16, (316L)</td><td>4,23 $/lb</td></tr>
        <tr><td>1/4, (316L)</td><td>4,23 $/lb</td></tr>
      </tbody>
    </table>
  </div>

  <h3>Plaque aluminium 3003</h3>
  <p>Toutes les lignes « Plate … (3003) » consultées (de 0,04 po à 1 po) affichaient le même prix : <strong>4,79 $/lb</strong>. C’est un prix à la livre, pas au pied carré.</p>
  <div class="callout warn">
    <p>La même page listait aussi des lignes « Plate 7.048 / 8.82 / 14.1 po (6061) » à 28,07 à 56,16 $/lb. Ces descriptions et ces niveaux de prix sortent du lot (un 6061 atelier se chiffre d’habitude tout autrement). <strong>Nous ne les inscrivons pas au comparatif</strong> tant que Michaël n’a pas confirmé s’il s’agit d’une erreur d’unité, d’un format particulier, ou d’autre chose. Allez voir la source pour le libellé exact.</p>
  </div>

  <h3>Acier au carbone en feuille</h3>
  <p>Dans les catégories visibles au moment du relevé, nous n’avons pas trouvé de grille publique « plaque acier doux » comparable (en $/pi²) sur cette page. Les rubriques détaillées reprises ici sont l’inox (plaque, cornière, barre, tube) et l’aluminium. Nous n’inventons pas de prix d’acier laminé à chaud ou décapé.</p>

  <h2>Limites de cette première édition</h2>
  <ul>
    <li>Une seule source publique québécoise détaillée. Ce n’est pas un indice de marché, c’est un atelier de Saint-Hubert qui publie des coûts indicatifs pour des projets de fabrication.</li>
    <li>Unités hétérogènes ($/pi² et $/lb) : ne pas les moyenner.</li>
    <li>Pas de quantité minimale, de format de feuille, ni de fini (2B, brossé, etc.) assez clairs pour un devis de nesting.</li>
    <li>Les cornières, barres et tubes de la même page existent ; ils sortiront peut-être dans une édition suivante, toujours sourcés.</li>
  </ul>

  <h2>À valider (Michaël)</h2>
  <ul>
    <li>Les lignes 6061 atypiques : les inclure avec une mise en garde, ou les laisser de côté.</li>
    <li>D’autres listes publiques québécoises que vous connaissez (même partielles).</li>
    <li>Le choix des épaisseurs « typiques atelier » à suivre chaque mois.</li>
  </ul>

  <h2>Sources</h2>
  <ul class="source-list">
    <li><a href="https://unitedstainless.ca/live-prices">United Stainless — Indicative Material Costs</a>, « Last updated: October 22, 2026 », consulté le 26 novembre 2026. Adresse publiée : 3159, rue Harvey, Saint-Hubert (QC).</li>
    <li><a href="https://unitedstainless.ca/terms">United Stainless — Conditions d’utilisation</a> (prix indicatifs seulement), consulté le 26 novembre 2026.</li>
  </ul>
</div>
"""

PRIX_EN = """
<div class="wrap prose" style="max-width:52rem">
  <p class="kicker">Sheet prices</p>
  <h1 class="page-title">Sheet-metal prices in Quebec</h1>
  <p class="meta">Draft · first comparison · sources consulted November 26, 2026 (America/Toronto) · to be reviewed by Michaël</p>
  <p class="lede">Plenty of shops would pay for an honest comparison of steel, stainless, and aluminum sheet. In practice, most Quebec suppliers still say “call for pricing.” CoupeFab does not invent prices: only public lists, dated and linked.</p>

  <h2>Method</h2>
  <ol>
    <li>Use only public pages that can be read without an account.</li>
    <li>Record the source’s own “last updated” date, and the date we consulted it.</li>
    <li>Keep the units as published ($/sq ft or $/lb). Do not convert quietly, and do not mix units in one column without a label.</li>
    <li>State clearly that a posted price is indicative, often before processing, quantity, sheet size, and availability.</li>
    <li>If only one public source is found for a product, say so: this is a landmark, not a complete market.</li>
  </ol>
  <p>This first edition found <strong>only one</strong> detailed public Quebec list suitable for a table: <a href="https://unitedstainless.ca/live-prices">unitedstainless.ca/live-prices</a> (United Stainless / Alluminox Spec, Saint-Hubert, on Montreal’s South Shore). Other players (service centres, national distributors) did not, at the time of the survey, show a comparable sheet grid in $/sq ft. We did not fill the gaps with shop-floor hearsay or mill index numbers.</p>

  <h2>United Stainless — indicative list</h2>
  <p>The page states: “Last updated: October 22, 2026.” United Stainless says it is a custom fabrication shop, that the list is for estimating a project before a quote, and that you cannot order material from the grid. The site’s terms repeat the point: indicative prices only; the final price depends on quantity, availability, processing, and the market.</p>

  <h3>304L stainless sheet — per square foot</h3>
  <p>Where the same description appeared more than once at the same price, a single row is kept.</p>
  <div class="table-wrap">
    <table>
      <thead><tr><th>Description (as posted)</th><th>Posted price</th></tr></thead>
      <tbody>
        <tr><td>11 ga / .125 (304L)</td><td>$3.32/sq ft</td></tr>
        <tr><td>12 ga / .109 (304L)</td><td>$3.32/sq ft</td></tr>
        <tr><td>14 ga / .0781 (304L)</td><td>$3.32/sq ft</td></tr>
        <tr><td>10 g / .140 (304L)</td><td>$3.90/sq ft</td></tr>
        <tr><td>16 ga / .0625 (304L)</td><td>$4.23/sq ft</td></tr>
        <tr><td>18 ga / .050 (304L)</td><td>$4.29/sq ft</td></tr>
        <tr><td>3/16 / .1875 (304L)</td><td>$4.94/sq ft</td></tr>
        <tr><td>1/4 / .250 (304L)</td><td>$5.72/sq ft</td></tr>
        <tr><td>20 ga / .0375 (304L)</td><td>$6.76/sq ft</td></tr>
      </tbody>
    </table>
  </div>

  <h3>316L stainless — watch the units</h3>
  <p>On the same page, the 316L rows we reviewed were posted <strong>per pound</strong>, not per square foot. They are not a glance-comparable with the 304L table above.</p>
  <div class="table-wrap">
    <table>
      <thead><tr><th>Description (as posted)</th><th>Posted price</th></tr></thead>
      <tbody>
        <tr><td>1/8, (316L)</td><td>$4.20/lb</td></tr>
        <tr><td>3/16, (316L)</td><td>$4.23/lb</td></tr>
        <tr><td>1/4, (316L)</td><td>$4.23/lb</td></tr>
      </tbody>
    </table>
  </div>

  <h3>3003 aluminum plate</h3>
  <p>Every “Plate … (3003)” row we reviewed (from 0.04 in to 1 in) showed the same price: <strong>$4.79/lb</strong>. That is a per-pound price, not per square foot.</p>
  <div class="callout warn">
    <p>The same page also listed “Plate 7.048 / 8.82 / 14.1 in (6061)” rows at $28.07 to $56.16/lb. Those descriptions and price levels stand out (shop-grade 6061 usually sits somewhere else entirely). <strong>They are left out of the comparison</strong> until Michaël confirms whether this is a unit error, a special format, or something else. See the source for the exact wording.</p>
  </div>

  <h3>Carbon steel sheet</h3>
  <p>In the categories visible at the time of the survey, we did not find a comparable public “mild steel plate” grid (in $/sq ft) on that page. The detailed sections reused here are stainless (plate, angle, bar, tube) and aluminum. We will not invent hot-rolled or pickled-and-oiled sheet prices.</p>

  <h2>Limits of this first edition</h2>
  <ul>
    <li>One detailed public Quebec source. This is not a market index; it is a Saint-Hubert fabrication shop posting indicative costs for fabrication projects.</li>
    <li>Mixed units ($/sq ft and $/lb): do not average them.</li>
    <li>No clear minimum quantity, sheet format, or finish (2B, brushed, and so on) for a nesting quote.</li>
    <li>Angles, bar, and tube on the same page may appear in a later edition, still sourced.</li>
  </ul>

  <h2>For Michaël to review</h2>
  <ul>
    <li>The unusual 6061 rows: include them with a warning, or keep them out.</li>
    <li>Other public Quebec lists you know about, even partial ones.</li>
    <li>Which “typical shop” thicknesses to follow each month.</li>
  </ul>

  <h2>Sources</h2>
  <ul class="source-list">
    <li><a href="https://unitedstainless.ca/live-prices">United Stainless — Indicative Material Costs</a>, “Last updated: October 22, 2026,” consulted November 26, 2026. Published address: 3159 Rue Harvey, Saint-Hubert, QC.</li>
    <li><a href="https://unitedstainless.ca/terms">United Stainless — Terms of Use</a> (indicative prices only), consulted November 26, 2026.</li>
  </ul>
</div>
"""

NEWS_FR = f"""
<div class="wrap prose">
  <p class="kicker">Infolettre</p>
  <h1>L’infolettre CoupeFab</h1>
  <p class="lede">Un envoi occasionnel, puis hebdomadaire quand le rythme sera bon : nouveaux guides, digest d’occasions au Québec, mise à jour des prix de tôles. Les premiers numéros partiront à la main, depuis Gmail.</p>
  {form_newsletter("fr")}
  <h2>Ce que vous acceptez</h2>
  <p>En cochant la case, vous donnez un consentement exprès, conformément à la Loi canadienne anti-pourriel (LCAP / CASL), à recevoir des courriels de CoupeFab. Pas de case précochée, pas d’achat lié à l’inscription, et un moyen de se désabonner dans chaque envoi. Détails : <a href="/confidentialite/">confidentialité et consentement</a>.</p>
</div>
"""

NEWS_EN = f"""
<div class="wrap prose">
  <p class="kicker">Newsletter</p>
  <h1>The CoupeFab newsletter</h1>
  <p class="lede">An occasional letter, then a weekly one once the pace is right: new guides, the Quebec used-equipment digest, and sheet-price updates. Early issues will be sent by hand from Gmail.</p>
  {form_newsletter("en")}
  <h2>What you are agreeing to</h2>
  <p>By checking the box, you give express consent, under Canada’s Anti-Spam Legislation (CASL), to receive email from CoupeFab. The box is not pre-checked, a purchase is not required, and every issue will include a way to unsubscribe. Details: <a href="/en/privacy/">privacy and consent</a>.</p>
</div>
"""

ABOUT_FR = f"""
<div class="wrap prose">
  <p class="kicker">À propos</p>
  <h1>À propos de CoupeFab</h1>
  <p class="lede">CoupeFab est une ressource francophone d’abord, bilingue, pour les ateliers de découpe plasma et de fabrication métallique au Québec. Le site rassemble des guides CAD/CAM, un digest d’équipements d’occasion, et un suivi des prix de tôles lorsqu’ils sont publiés.</p>
  <p>Les pages techniques sont relues par Michaël Brassard avant d’être considérées comme publiées. Tant que la bannière « brouillon — à réviser par Michaël » est visible, traitez le texte comme un jet, pas comme une consigne de coupe.</p>
  <p>Nous ne vendons pas de machines et nous ne prenons pas commission sur les annonces pour le moment. Aucun lien d’affiliation n’est en place. Voir la <a href="/divulgation/">page de divulgation</a>.</p>
  <h2>Contact</h2>
  <p>Une question, une correction, une annonce publique à signaler : écrivez-nous. Si vous préférez l’infolettre, c’est par <a href="/infolettre/">ici</a>.</p>
  {form_contact("fr")}
</div>
"""

ABOUT_EN = f"""
<div class="wrap prose">
  <p class="kicker">About</p>
  <h1>About CoupeFab</h1>
  <p class="lede">CoupeFab is a French-first, bilingual resource for plasma cutting and metal fabrication shops in Quebec. The site gathers CAD/CAM guides, a digest of used equipment, and a sheet-price tracker when prices are posted publicly.</p>
  <p>Technical pages are reviewed by Michaël Brassard before they count as published. While the “draft — to be reviewed by Michaël” banner is visible, treat the text as a working draft, not as a cutting instruction.</p>
  <p>We do not sell machines and we do not take a commission on listings for now. There are no affiliate links in place. See the <a href="/en/affiliate-disclosure/">disclosure page</a>.</p>
  <h2>Contact</h2>
  <p>A question, a correction, or a public listing we should see: write to us. If you would rather have the newsletter, it is <a href="/en/newsletter/">here</a>.</p>
  {form_contact("en")}
</div>
"""

DISC_FR = """
<div class="wrap prose">
  <h1>Divulgation — affiliations et publicité</h1>
  <p class="lede">Pour l’instant, CoupeFab <strong>n’a aucun lien d’affiliation</strong>, aucun commanditaire et aucune publicité payante. Aucun compte d’affiliation n’a été ouvert ni approuvé.</p>
  <p>Si cela change, cette page sera mise à jour en premier. Les liens affiliés seront identifiés, et un article restera lisible sans eux. Nous n’accepterons pas qu’un commanditaire dicte un paramètre de coupe ou un prix.</p>
  <p>Les liens vers des manuels, des chartes, des courtiers ou des listes de prix sont des liens ordinaires, sans rémunération.</p>
  <p><a href="/a-propos/">Retour à À propos</a></p>
</div>
"""

DISC_EN = """
<div class="wrap prose">
  <h1>Affiliate and advertising disclosure</h1>
  <p class="lede">For now, CoupeFab has <strong>no affiliate links</strong>, no sponsors, and no paid ads. No affiliate account has been opened or approved.</p>
  <p>If that changes, this page will be updated first. Affiliate links will be labelled, and an article will still be readable without them. A sponsor will not be allowed to dictate a cut parameter or a price.</p>
  <p>Links to manuals, cut charts, dealers, or price lists are ordinary links, with no payment attached.</p>
  <p><a href="/en/about/">Back to About</a></p>
</div>
"""

PRIV_FR = """
<div class="wrap prose">
  <h1>Confidentialité et consentement (LCAP / CASL)</h1>
  <p>CoupeFab recueille le courriel que vous saisissez, le prénom ou le nom d’atelier s’il est fourni, la langue du formulaire, et la date du consentement. Pour un message de contact, nous conservons aussi le texte du message. Nous n’utilisons pas ces données à d’autres fins que d’envoyer l’infolettre, de répondre, et de tenir un registre de consentement.</p>
  <h2>Consentement exprès</h2>
  <p>L’inscription à l’infolettre exige une case à cocher, non précochée. En la cochant, vous acceptez de recevoir des courriels de CoupeFab (guides, digest d’occasions, suivi des prix des tôles). Vous pouvez retirer ce consentement en tout temps, via le lien de désabonnement de chaque envoi ou en nous écrivant.</p>
  <h2>Conservation</h2>
  <p>Les inscriptions transitent par une fonction hébergée sur Vercel. Lorsque c’est configuré, elles sont aussi envoyées vers une boîte courriel d’exploitation ou une feuille de calcul, afin que les premiers numéros puissent partir manuellement depuis Gmail. Nous ne vendons pas la liste et nous ne la partageons pas avec des annonceurs.</p>
  <h2>Vos droits</h2>
  <p>Pour consulter, corriger ou supprimer votre courriel, écrivez-nous depuis la page <a href="/a-propos/">À propos / contact</a>. Cette politique sera mise à jour si un prestataire d’infolettre plus complet est ajouté.</p>
</div>
"""

PRIV_EN = """
<div class="wrap prose">
  <h1>Privacy and CASL consent</h1>
  <p>CoupeFab collects the email you enter, a first name or shop name if you give one, the form language, and the date of consent. For a contact message, we also keep the text of the message. We do not use this data for anything other than sending the newsletter, replying, and keeping a consent record.</p>
  <h2>Express consent</h2>
  <p>Newsletter signup requires a checkbox that is not pre-checked. By ticking it, you agree to receive email from CoupeFab (guides, the used-equipment digest, sheet-price updates). You may withdraw that consent at any time, through the unsubscribe link in each issue or by writing to us.</p>
  <h2>Storage</h2>
  <p>Signups go through a function hosted on Vercel. When it is configured, they are also forwarded to an operations inbox or a spreadsheet, so early issues can be sent by hand from Gmail. We do not sell the list and we do not share it with advertisers.</p>
  <h2>Your rights</h2>
  <p>To review, correct, or delete your email, write to us from the <a href="/en/about/">About / contact</a> page. This policy will be updated if a fuller newsletter provider is added later.</p>
</div>
"""

PAGES = [
    # path, alt, lang, title, description, body, draft, article
    ("/", "/en/", "fr", "CoupeFab — guides plasma, occasions et prix des tôles au Québec",
     "Ressource francophone pour les ateliers de découpe plasma au Québec : guides SheetCam et BricsCAD, digest d’occasions, suivi des prix de tôles.",
     HOME_FR, False, False),
    ("/en/", "/", "en", "CoupeFab — plasma guides, used equipment, and sheet prices in Quebec",
     "A French-first resource for plasma shops in Quebec: SheetCam and BricsCAD guides, a used-equipment digest, and a sheet-price tracker.",
     HOME_EN, False, False),
    ("/guides/", "/en/guides/", "fr", "Guides de découpe et de CAD/CAM — CoupeFab",
     "Guides SheetCam, BricsCAD, kerf et consommables plasma, en français d’abord.",
     GUIDES_FR, False, False),
    ("/en/guides/", "/guides/", "en", "Cutting and CAD/CAM guides — CoupeFab",
     "SheetCam, BricsCAD, kerf, and plasma consumable guides, written French-first.",
     GUIDES_EN, False, False),
    ("/guides/debuter-sheetcam/", "/en/guides/getting-started-sheetcam/", "fr",
     "Débuter avec SheetCam en français — CoupeFab",
     "Compagnon francophone pour démarrer dans SheetCam : unités, job, import DXF, opération plasma et imbricage. Brouillon à réviser.",
     SHEETCAM_FR, True, True),
    ("/en/guides/getting-started-sheetcam/", "/guides/debuter-sheetcam/", "en",
     "Getting started with SheetCam — CoupeFab",
     "A French-first companion to starting in SheetCam: units, jobs, DXF import, plasma operations, and nesting. Draft pending review.",
     SHEETCAM_EN, True, True),
    ("/guides/bricscad-dxf/", "/en/guides/bricscad-to-clean-dxf/", "fr",
     "De BricsCAD à un DXF propre — CoupeFab",
     "Exporter un DXF propre depuis BricsCAD avec DXFOUT, la précision décimale et le nettoyage des objets mandataires. Brouillon à réviser.",
     BRICSCAD_FR, True, True),
    ("/en/guides/bricscad-to-clean-dxf/", "/guides/bricscad-dxf/", "en",
     "From BricsCAD to a clean DXF — CoupeFab",
     "Export a clean DXF from BricsCAD with DXFOUT, decimal precision, and proxy-object cleanup. Draft pending review.",
     BRICSCAD_EN, True, True),
    ("/guides/kerf-qualite-coupe/", "/en/guides/kerf-and-cut-quality/", "fr",
     "Kerf et qualité de coupe — CoupeFab",
     "Lire une charte de kerf du fabricant sans mélanger les manuels, avec un exemple cité d’une charte Hypertherm. Brouillon à réviser.",
     KERF_FR, True, True),
    ("/en/guides/kerf-and-cut-quality/", "/guides/kerf-qualite-coupe/", "en",
     "Kerf and cut quality — CoupeFab",
     "How to read a manufacturer kerf chart without mixing manuals, with a cited Hypertherm example. Draft pending review.",
     KERF_EN, True, True),
    ("/guides/consommables-plasma-canada/", "/en/guides/plasma-consumables-canada/", "fr",
     "Consommables plasma et achats au Canada — CoupeFab",
     "Entretien des consommables selon Hypertherm et pistes d’achat au Canada, sans liens d’affiliation. Brouillon à réviser.",
     CONSOM_FR, True, True),
    ("/en/guides/plasma-consumables-canada/", "/guides/consommables-plasma-canada/", "en",
     "Plasma consumables and buying in Canada — CoupeFab",
     "Hypertherm’s consumable-care guidance and Canadian buying paths, with no affiliate links. Draft pending review.",
     CONSOM_EN, True, True),
    ("/occasions/", "/en/used-equipment/", "fr",
     "Occasions Québec — évaluer une table plasma usagée — CoupeFab",
     "Liste de vérification pour l’achat d’une table plasma usagée au Québec, et premier digest d’annonces publiques daté.",
     OCCASIONS_FR, True, True),
    ("/en/used-equipment/", "/occasions/", "en",
     "Used equipment in Quebec — evaluating a used plasma table — CoupeFab",
     "A checklist for buying a used plasma table in Quebec, and a first dated digest of public listings.",
     OCCASIONS_EN, True, True),
    ("/prix/", "/en/sheet-prices/", "fr",
     "Prix des tôles au Québec — CoupeFab",
     "Méthode et première comparaison de prix de tôles à partir de listes publiques québécoises, avec dates et sources.",
     PRIX_FR, True, True),
    ("/en/sheet-prices/", "/prix/", "en",
     "Sheet-metal prices in Quebec — CoupeFab",
     "Method and first sheet-price comparison from public Quebec lists, with dates and sources.",
     PRIX_EN, True, True),
    ("/infolettre/", "/en/newsletter/", "fr",
     "Infolettre CoupeFab",
     "Inscrivez-vous à l’infolettre CoupeFab : guides, occasions Québec et prix des tôles. Consentement LCAP / CASL.",
     NEWS_FR, False, False),
    ("/en/newsletter/", "/infolettre/", "en",
     "CoupeFab newsletter",
     "Subscribe to the CoupeFab newsletter: guides, used equipment in Quebec, and sheet prices. CASL consent.",
     NEWS_EN, False, False),
    ("/a-propos/", "/en/about/", "fr",
     "À propos et contact — CoupeFab",
     "Qui est derrière CoupeFab et comment nous écrire.",
     ABOUT_FR, False, False),
    ("/en/about/", "/a-propos/", "en",
     "About and contact — CoupeFab",
     "Who is behind CoupeFab and how to reach us.",
     ABOUT_EN, False, False),
    ("/divulgation/", "/en/affiliate-disclosure/", "fr",
     "Divulgation — affiliations et publicité — CoupeFab",
     "CoupeFab n’a pour le moment aucun lien d’affiliation ni commanditaire.",
     DISC_FR, False, False),
    ("/en/affiliate-disclosure/", "/divulgation/", "en",
     "Affiliate and advertising disclosure — CoupeFab",
     "CoupeFab currently has no affiliate links and no sponsors.",
     DISC_EN, False, False),
    ("/confidentialite/", "/en/privacy/", "fr",
     "Confidentialité et consentement (LCAP / CASL) — CoupeFab",
     "Comment CoupeFab recueille les courriels et obtient un consentement exprès conforme à la LCAP.",
     PRIV_FR, False, False),
    ("/en/privacy/", "/confidentialite/", "en",
     "Privacy and CASL consent — CoupeFab",
     "How CoupeFab collects emails and obtains express consent under CASL.",
     PRIV_EN, False, False),
]


def path_to_file(path: str) -> Path:
    rel = path.strip("/")
    if not rel:
        return ROOT / "index.html"
    return ROOT / rel / "index.html"


def write_sitemap():
    urls = []
    for path, alt, lang, *_rest in PAGES:
        urls.append(
            f"""  <url>
    <loc>{SITE}{path}</loc>
    <lastmod>{DATE_ISO}</lastmod>
    <xhtml:link rel="alternate" hreflang="{'fr-CA' if lang == 'fr' else 'en-CA'}" href="{SITE}{path}"/>
    <xhtml:link rel="alternate" hreflang="{'en-CA' if lang == 'fr' else 'fr-CA'}" href="{SITE}{alt}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}/"/>
  </url>"""
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")


def main():
    for path, alt, lang, title, description, body, draft, article in PAGES:
        dest = path_to_file(path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(
            layout(
                lang=lang,
                title=title,
                description=description,
                path=path,
                alt=alt,
                body=body,
                draft=draft,
                article=article,
            ),
            encoding="utf-8",
        )
        print("wrote", dest.relative_to(ROOT))
    write_sitemap()
    print("wrote sitemap.xml")


if __name__ == "__main__":
    main()
