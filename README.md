# CoupeFab

Site francophone d’abord (avec version anglaise) pour les ateliers de découpe plasma et de fabrication métallique au Québec : guides CAD/CAM, digest d’occasions, suivi des prix de tôles publiés.

Live (Vercel) : l’URL `*.vercel.app` est indiquée après le premier déploiement.

## Contenu

Les six pages d’angle sont des **brouillons** (`brouillon — à réviser par Michaël`) jusqu’à validation technique :

1. Débuter avec SheetCam en français
2. De BricsCAD à un DXF propre
3. Kerf et qualité de coupe
4. Consommables plasma et achats au Canada
5. Évaluer une table plasma usagée au Québec (liste de vérification + digest n° 1)
6. Prix des tôles au Québec (méthode + première comparaison sourcée)

Aucun paramètre de coupe ni prix n’est inventé. Aucun lien d’affiliation pour le moment.

## Développement

Site statique généré par `build.py`, plus une fonction Vercel `api/subscribe.js`.

```bash
python3 build.py
```

Ouvrir `index.html` ou servir le dossier :

```bash
python3 -m http.server 8080
```

La fonction `/api/subscribe` ne tourne pas dans ce serveur local simple ; utiliser `vercel dev` une fois le projet lié, ou tester après déploiement.

## Infolettre (CASL)

Le formulaire (case de consentement non précochée) envoie un POST JSON à `/api/subscribe`.

Pour une conservation durable, définir dans le projet Vercel (Production + Preview) :

- `NEWSLETTER_INBOX` — une adresse Gmail d’exploitation. Les inscriptions passent par [FormSubmit](https://formsubmit.co). **Confirmez le premier courriel** que FormSubmit envoie à cette boîte.
- et/ou `NEWSLETTER_WEBHOOK_URL` — un script Google Apps Script (ou équivalent) qui ajoute une ligne dans une feuille.

Sans ces variables, l’inscription est acceptée mais n’est consignée que dans le journal éphémère de la fonction (`/tmp` sur Vercel). Configurez au moins `NEWSLETTER_INBOX` avant de pousser l’infolettre.

Les premiers numéros sont prévus pour un envoi manuel depuis Gmail.

## Domaines (plus tard)

`couperfab.ca` et `couperfab.com` sont achetés à part (Porkbun). Ne rien acheter depuis ce dépôt.

Quand les domaines sont actifs, les ajouter dans Vercel : Project → Settings → Domains. Deux approches, au choix :

1. **Enregistrements chez Porkbun** (Vercel affiche les valeurs exactes à coller) :
   - apex (`couperfab.ca` / `couperfab.com`) : enregistrement **A** vers l’IPv4 indiqué par Vercel (souvent `76.76.21.21` — confirmer dans le tableau de bord)
   - `www` : **CNAME** vers `cname.vercel-dns.com` (ou la cible CNAME affichée par Vercel)
2. **Serveurs de noms Vercel** chez Porkbun : `ns1.vercel-dns.com` et `ns2.vercel-dns.com` — Vercel crée alors les enregistrements tout seul.

Faire de `couperfab.ca` le domaine canonique, puis rediriger `www` et `.com` vers celui-ci (ou l’inverse, une fois le choix tranché). Mettre ensuite à jour la constante `SITE` dans `build.py` et régénérer le site pour les URL canoniques, le plan du site et les `hreflang`.

## Licence

Contenu et code : tous droits réservés, CoupeFab / Michaël Brassard, sauf mention contraire des sources citées (Hypertherm, SheetCam, BricsCAD, annonces de tiers, etc.).
