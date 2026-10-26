# Module 07 — Bilan matériaux complet et équipements

Ce bilan couvre **tout ce qu'il faut fabriquer** pour la forteresse en plans par zone, adaptée au trou (module 06) :
- la structure des plans 1 et 3 à 11 (plateforme verte comprise), les pics et les carrés de culture ;
- les options à part : colonnade (plan 2) et rehausse de la tour ;
- les 85 tourelles (52 Heavy, 23 Tek, 10 Tesla), plus 15 Plant Species X ;
- les équipements demandés : 1 Réplicateur Tek, 1 forge à vapeur, 1 labo de fortune, 20 stockages dédiés, 20 coffres-forts, 2 générateurs Tek.

Les chiffres sont recalculés par le script : `donnees/synthese.json`, clés `bilan_complet`, `bilan_total` et `options`. Classeur : `donnees/07_bilan_materiaux.xlsx`, régénéré par `python3 outils/bilan_xlsx.py`. Positions des équipements : `donnees/07_equipements.csv`.

## 1. Total à réunir

| Ressource | Sans les tourelles (déjà en inventaire) | **Avec les tourelles** |
|---|---|---|
| Lingots de métal | **147 504** | **182 884** |
| Pâte cimentée | **37 576** | **49 126** |
| Électroniques | 220 | 17 560 |
| Polymère | 5 850 | 13 640 |
| Cristal | 3 350 | 5 350 |
| Élément | 220 | 289 |
| Perles noires | 470 | 470 |
| Huile | 1 400 | 1 400 |
| Poudre étincelante | 100 | 100 |
| Cuir | 1 480 | 1 480 |
| Fibre | 3 136 | 3 136 |
| Chaume (murs de chaume démolis ensuite, carrés de culture) | 1 303 | 1 303 |
| Bois (idem) | 916 | 916 |
| Pierre (carrés de culture) | 1 500 | 1 500 |

Le script place les tourelles (52 Heavy, 23 Tek, 10 Tesla), mais elles sont **déjà dans votre inventaire** : ne fabriquez que la colonne de gauche. Il reste en réserve 28 Heavy, 12 Tek et aucune Tesla. Les 15 graines de Plant Species X se récoltent (marais) et se plantent à la main.

| Option | Pièces | Lingots | Pâte |
|---|---|---|---|
| Colonnade (plan 2) | 226 piliers | +5 650 | +1 582 |
| Rehausse de la tour, par niveau | 52 murs pleins + 24 piliers | +1 900 | +532 |

Si votre étoile (anneaux 1 à 7) est déjà construite, retirez ses 87 fondations et 174 triangles hors du trou : 8 700 lingots et 2 697 pâte.

## 1 bis. Ce qui a changé avec le découpage par zones

Par rapport à la version précédente (138 479 lingots, 34 725 pâte, colonnade comprise) :

| Changement | Pièces | Lingots | Pâte |
|---|---|---|---|
| **Poteaux de stabilité** sous les jonctions de lames (pente A, appentis, toit du pod) : chaque ligne montante tient encore si un appui est détruit | +861 piliers fins | +11 193 | +3 444 |
| **Colonnade passée en option** (plan 2), hors du bilan | −226 piliers | −5 650 | −1 582 |
| **Tour du pod** : un niveau de plus (anneau de tourelles D4, Z2700) et la couronne du toit ; piliers PA/PB prolongés | +111 murs et cadres, +48 piliers | +3 975 | +1 113 |
| Toit refait de D4 au centre, appentis au-dessus de la cage | −40 rampes | −480 | −120 |
| Murs en **cadres doubles** partout sauf la tour du pod (même coût estimé qu'un mur) | — | — | — |
| Ancre de pile : une de moins (11 plans au lieu de 8, mais 3 calés sur un mur de D4) | −1 demi-pilier | −13 | −4 |
| **Total** | | **+9 025** | **+2 851** |

- 15 carrés de culture pour les Plant X : 600 bois, 750 chaume, 600 fibre, 1 500 pierre (estimation).
- Les coûts des piliers fins, des poutres fines et des cadres doubles sont des estimations, à vérifier en jeu.
- **Option `--appuis tours`** (sans poteaux de stabilité, comme les tours) : 896 piliers fins de moins, soit −11 648 lingots et −3 584 pâte (135 856 lingots et 33 992 pâte à fabriquer). En contrepartie, seules 48 lames du toit sur 170 et aucune de l'appentis tiennent encore si leur appui est détruit.

**Pourquoi des rampes et pas des toits** : sur un toit à 45°, on tient debout ; sur une lame de rampes inclinées, non. Seules les rampes font glisser (module 03 §7). Une rampe coûte en plus environ trois fois moins qu'un toit.

## 2. Détail par poste

| Poste | Contenu | Lingots | Pâte | Autres |
|---|---|---|---|---|
| **Structure des plans** (sans la colonnade) | 5 495 pièces : 344 fondations et 684 triangles (dont les 10 pièces de la plateforme verte), 489 murs pleins, 774 cadres doubles, 240 piliers, 307 plafonds, 629 plafonds triangles, 6 trappes, 6 escaliers, 852 rampes inclinées (aucun toit), 1 027 piliers fins, 43 demi-piliers fins, 94 poutres fines | 119 550 | 34 644 | — |
| Carrés de culture | 15 grands carrés de culture (Plant X) | — | — | 600 bois, 750 chaume, 600 fibre, 1 500 pierre |
| Ancres temporaires | 8 demi-piliers (démolis à la fin) | 104 | 32 | — |
| **Murs de pics** | 74 Metal Spike Walls | 1 850 | — | 1 480 cuir, 2 220 fibre |
| Gabarits de pose | 79 murs de chaume (démolis ensuite) | — | — | ~553 chaume, ~316 fibre, ~316 bois |
| **Équipements** | voir §3 | 26 000 | 2 900 | 220 élément, 3 350 cristal, 470 perles noires, 5 850 polymère, 220 électroniques, 100 poudre étincelante, 1 400 huile |
| *Tourelles (inventaire)* | *52 Heavy, 23 Tek, 10 Tesla* | *35 380* | *11 550* | *17 340 électroniques, 7 790 polymère, 2 000 cristal, 69 élément* |

Le détail plan par plan (pièces, lingots, pâte) est au module 06 §5 et dans l'onglet « Par plan » du classeur : on peut construire et financer la base plan par plan.

## 3. Équipements

| Équipement | Qté | Recette unitaire | Atelier | Total |
|---|---|---|---|---|
| **Réplicateur Tek** | 1 | 5 000 lingots, 800 polymère, 600 cristal, 150 perles noires, 100 élément | (tekgramme) | — |
| **Forge à vapeur** (Steam Forge, Steampunk Ascent) | 1 | 3 250 lingots, 1 000 polymère, 600 pâte, 500 cristal, 200 électroniques | Fabricator ; engram Forge industrielle requis ; forge alimentée à l'élément | — |
| **Labo de fortune** (Makeshift Megalab) | 1 | 450 lingots, 300 pâte, 250 cristal, 150 polymère, 100 poudre étincelante, 20 électroniques | Fabricator | — |
| **Stockage dédié Tek** (Tek Dedicated Storage) | 20 | 125 lingots, 75 cristal, 55 polymère, 4 perles noires, 3 élément | Tek Replicator | 2 500 lingots, 1 500 cristal, 1 100 polymère, 80 perles noires, 60 élément |
| **Coffre-fort** (Vault) | 20 | 500 lingots, 100 pâte, 90 polymère, 70 huile ⚠ une seule source | Fabricator / Replicator | 10 000 lingots, 2 000 pâte, 1 800 polymère, 1 400 huile |
| **Générateur Tek** | 2 | 2 400 lingots, 500 polymère, 250 cristal, 120 perles noires, 30 élément | Tek Replicator | 4 800 lingots, 1 000 polymère, 500 cristal, 240 perles noires, 60 élément |

Ordre de fabrication logique :
1. Réplicateur Tek (Fabricator ou tekgramme).
2. Générateurs Tek et stockages dédiés (au Réplicateur).
3. Forge à vapeur, labo et coffres-forts (au Fabricator).

### Emplacements (hors plan, `donnees/07_equipements.csv`)

| Lieu | Équipements |
|---|---|
| Hall Z0 (6 murs libres) | Réplicateur Tek (θ 0°) · Générateur Tek n°1 (θ 60°) · Forge à vapeur (θ 120°) · Labo de fortune (θ 240°) · **9 stockages dédiés** (θ 300°, 2 rangées de 4 et 5). Le trou occupe la branche θ 180° |
| Mezzanine Z1800 | Générateur Tek n°2 (θ 180°, à 900 UU du centre, 220 UU avant le mur de bord du trou) · **20 coffres-forts + 11 stockages dédiés**, en alternance contre la face intérieure du mur de pod. Cela fait 31 emplacements : positions 0, 2 et 3 de chaque côté, la position 1 étant l'accès galerie, moins les 5 coupés par le trou |

### Couverture des 2 générateurs Tek

Le générateur n°2 (mezzanine, (−900 ; 0), Z1800) alimente les **23 Tek**, à **1 540 → 3 740 UU** : L1, tour D4, bord du trou et dessus. Réglez-le pour qu'il porte à 3 800 UU. Les Heavy et les Tesla sont électriques : distances au générateur le plus proche au module 05 §8.

⚠ Réglez la portée au maximum et vérifiez la sphère affichée.
- Si le n°2 n'atteint pas 3 800 UU, rapprochez-le du centre ou ajoutez un 3ᵉ générateur.
- Les Heavy de jupe et les Tesla sont électriques. S'ils restent hors de portée, il faut des câbles et un générateur électrique : ce matériel n'est pas dans votre liste et n'est pas compté ici.

## 4. Équivalent en ressources brutes

Recettes usuelles, à vérifier sur votre serveur :
- lingot = 2 minerais de métal ;
- électronique = 1 lingot + 3 perles de silice ;
- polymère = 2 obsidiennes + 2 pâtes cimentées ;
- pâte = 4 chitine ou kératine + 8 pierres ;
- poudre étincelante = 2 silex + 1 pierre.

| Ressource brute | Sans les tourelles | Avec les tourelles |
|---|---|---|
| Minerai de métal | **≈ 295 000** | ≈ 401 000 |
| Chitine ou kératine | **≈ 197 000** | ≈ 306 000 |
| Pierre | **≈ 396 000** | ≈ 613 000 |
| Obsidienne | ≈ 11 700 | ≈ 27 300 |
| Perles de silice | ≈ 660 | ≈ 52 700 |
| Silex | 200 | 200 |
| Cristal / élément / perles noires / huile | 3 350 / 220 / 470 / 1 400 | 5 350 / 289 / 470 / 1 400 |

Avec du polymère organique ou de la pâte d'Achatina, la pierre, la chitine et l'obsidienne baissent fortement.

## 5. Consommables (non chiffrés)

- Balles de fusil avancé (Heavy), fragments d'élément (Tek), cristal (Tesla, munition indiquée par wikily.gg), eau et engrais (Plant X).
- Élément pour les 2 générateurs Tek et la forge à vapeur.

## 6. Fiabilité des chiffres

| Donnée | Statut |
|---|---|
| Fondation, triangle, mur, plafond, pilier | sources concordantes (wikily.gg, dododex, ark-unity) |
| Plafond triangle, demi-pilier, cadre double, trappe, escalier, porte secrète, mur de chaume, grand carré de culture | **estimations** : pièce absente des sources consultées |
| Rampe inclinée (Sloped Railing) | **estimation** : coût de la rambarde métal (12 lingots + 3 pâte, dododex) |
| Pilier fin, demi-pilier fin, pilier fin couché (Thin / Half Thin / Flat Thin Pillar) | **estimations** : moitié d'un pilier métal (13 + 4), quart pour le demi-pilier fin (7 + 2) |
| Heavy, Tek, Tesla, Réplicateur, forge à vapeur, labo, stockage dédié Tek, générateur Tek | sources concordantes ; ark.wiki.gg donne une variante pour le labo et la Tek |
| Coffre-fort | une seule source (Sportskeeda) |

Sources :
- [wikily.gg — Steam Forge](https://wikily.gg/ark-survival-ascended/items/steam-forge/), [Makeshift Megalab](https://wikily.gg/ark-survival-ascended/items/makeshift-megalab/), [Tek Replicator](https://wikily.gg/ark-survival-ascended/items/tek-replicator/), [Tek Dedicated Storage](https://wikily.gg/ark-survival-ascended/items/tek-dedicated-storage/)
- [ark.wiki.gg — Steam Forge](https://ark.wiki.gg/wiki/Steam_Forge), [Makeshift Megalab](https://ark.wiki.gg/wiki/Makeshift_Megalab), [Tek Generator](https://ark.wiki.gg/wiki/Tek_Generator), [Tek Replicator](https://ark.wiki.gg/wiki/Tek_Replicator), [Tek Dedicated Storage](https://ark.wiki.gg/wiki/Tek_Dedicated_Storage)
- [dododex — Steam Forge](https://www.dododex.com/item/2168/steam-forge), [Makeshift Megalab](https://www.dododex.com/item/2137/makeshift-megalab), [Tek Replicator](https://www.dododex.com/item/1840/tek-replicator), [Tek Dedicated Storage](https://www.dododex.com/item/1808/tek-dedicated-storage)
- [Sportskeeda — storage structures (Vault)](https://www.sportskeeda.com/mmo/all-storage-structures-ark-survival-ascended-craft)
- [dododex — Metal Railing](https://www.dododex.com/item/1482/metal-railing)
- Autres coûts : sources du README §9.
