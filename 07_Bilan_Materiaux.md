# Module 07 — Bilan matériaux complet et équipements

Ce bilan couvre **tout ce qu'il faut fabriquer** pour la forteresse en 8 plans, adaptée au trou (module 06) :
- la structure (plateforme verte comprise) et les pics ;
- les 96 tourelles ;
- les équipements demandés : 1 Réplicateur Tek, 1 forge à vapeur, 1 labo de fortune, 20 stockages dédiés, 20 coffres-forts, 2 générateurs Tek.

Les chiffres sont recalculés par le script : `donnees/synthese.json`, clés `bilan_complet` et `bilan_total`. Positions des équipements : `donnees/07_equipements.csv`.

## 1. Total à réunir

| Ressource | Sans les tourelles (déjà en inventaire) | **Avec les 96 tourelles** |
|---|---|---|
| Lingots de métal | 135 938 | **174 338** |
| Pâte cimentée | 33 848 | **47 348** |
| Électroniques | 220 | **20 020** |
| Polymère | 5 850 | **13 350** |
| Cristal | 3 350 | **4 550** |
| Élément | 220 | **310** |
| Perles noires | 470 | 470 |
| Huile | 1 400 | 1 400 |
| Poudre étincelante | 100 | 100 |
| Cuir | 1 480 | 1 480 |
| Fibre | 2 604 | 2 604 |
| Chaume (gabarits, démolis ensuite) | 672 | 672 |
| Bois (gabarits) | 384 | 384 |

Le script crée les tourelles du plan (60 Heavy, 30 Tek, 6 Tesla), mais elles sont **déjà dans votre inventaire**. Ne fabriquez que la colonne de gauche. La réserve (20 Heavy, 5 Tek, 4 Tesla) n'est comptée nulle part.

Si votre étoile (anneaux 1 à 7) est déjà construite, retirez ses 87 fondations et 174 triangles hors du trou : 8 700 lingots et 2 697 pâte.

## 1 bis. Ce qui a changé : centre repris à zéro et trou à l'avant

Par rapport à la version précédente (toutes les pentes en rampes, avec le Coeur Base : 147 057 lingots, 36 972 pâte) :

| Changement | Pièces | Lingots | Pâte |
|---|---|---|---|
| **Coeur Base retiré** (la colonne de 6 escaliers reste) | −35 murs, −3 portes secrètes, −57 plafonds | −2 129 | −596 |
| **Fondations du trou** non posées | −40 carrés, −84 triangles | −4 100 | −1 272 |
| Structure au-dessus du trou retirée : murs, cadres, plafonds, piliers, rampes | — | −8 119 | −2 224 |
| **Murs de bord du trou** | +136 murs | +3 400 | +952 |
| **Casquette du trou** | +12 rampes | +144 | +36 |
| Pics et ancres | −10 pics, −5 demi-piliers | −315 | −20 |
| **Total** | | **−11 119** | **−3 124** |

- La plateforme verte (10 fondations, 375 lingots, 115 pâte) est comptée dans la structure : elle est posée.
- **Pourquoi des rampes et pas des toits** : sur un toit à 45°, on tient debout ; sur une lame de rampes inclinées, non. Seules les rampes font glisser (module 03 §7). Une rampe coûte en plus environ trois fois moins qu'un toit.

**Allègements possibles en plus** (non appliqués : ils retirent une fonction de défense) :

| Option | Pâte | Ce qu'on perd |
|---|---|---|
| Supprimer le mur de jupe (188 murs) | −1 316 | le support des 26 Heavy sous la plateforme : leurs murs de chaume flotteraient |
| Overhang d'un seul rang dans le vide (`--debord 1`, supprime aussi le mur de jupe) | ≈ −1 600 | les Heavy de jupe (le script ne les place plus), et 300 UU de dégagement des chutes |
| Fût remplacé par des piliers aux coins et milieux de côtés | ≈ −1 300 | le 2e mur entre l'attique A et le couloir |

## 2. Détail par poste

| Poste | Contenu | Lingots | Pâte | Autres |
|---|---|---|---|---|
| **Structure des 8 plans** | 4 585 pièces : 344 fondations, 684 triangles (dont les 10 pièces de la plateforme verte), 1 098 murs, 76 cadres doubles, 348 piliers, 308 plafonds, 629 plafonds triangles, 5 trappes, 6 escaliers, 1 087 rampes inclinées (aucun toit) | 107 971 | 30 912 | — |
| Ancres temporaires | 9 demi-piliers (démolis à la fin) | 117 | 36 | — |
| **Murs de pics** | 74 Metal Spike Walls | 1 850 | — | 1 480 cuir, 2 220 fibre |
| Gabarits de pose | 96 murs de chaume (démolis ensuite) | — | — | ~672 chaume, ~384 fibre, ~384 bois |
| **Équipements** | voir §3 | 26 000 | 2 900 | 220 élément, 3 350 cristal, 470 perles noires, 5 850 polymère, 220 électroniques, 100 poudre étincelante, 1 400 huile |
| *Tourelles (inventaire)* | *60 Heavy, 30 Tek, 6 Tesla* | *38 400* | *13 500* | *19 800 électroniques, 7 500 polymère, 1 200 cristal, 90 élément* |

Le détail plan par plan (pièces, lingots, pâte) est au module 06 §5. On peut construire et financer la base plan par plan.

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

Distances mesurées sur le plan, pivot à pivot :

| Générateur | Tek de L1, bord du trou compris (alimentation Tek obligatoire) | Heavy de jupe | Tesla de rive |
|---|---|---|---|
| n°2, mezzanine (−900 ; 0), Z1800 | **1 351 → 3 760 UU** : couvre les 30 Tek s'il porte à 3 800 UU | 4 520 → 6 028 UU | 3 812 → 5 014 UU |
| n°1, hall (900 ; 1 559), Z0 | 2 196 → 5 040 UU | 2 811 → 6 401 UU | 2 176 → 5 746 UU |

Les 12 tourelles du bord du trou sont à 1 100 → 3 436 UU du générateur n°2.

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
| Minerai de métal | **≈ 272 000** | ≈ 389 000 |
| Chitine ou kératine | **≈ 182 000** | ≈ 296 000 |
| Pierre | **≈ 364 000** | ≈ 592 000 |
| Obsidienne | ≈ 11 700 | ≈ 26 700 |
| Perles de silice | ≈ 660 | ≈ 60 000 |
| Silex | 200 | 200 |
| Cristal / élément / perles noires / huile | 3 350 / 220 / 470 / 1 400 | 4 550 / 310 / 470 / 1 400 |

Avec du polymère organique ou de la pâte d'Achatina, la pierre, la chitine et l'obsidienne baissent fortement.

## 5. Consommables (non chiffrés)

- Balles de fusil avancé (Heavy), fragments d'élément (Tek), cristal (Tesla, munition indiquée par wikily.gg).
- Élément pour les 2 générateurs Tek et la forge à vapeur.

## 6. Fiabilité des chiffres

| Donnée | Statut |
|---|---|
| Fondation, triangle, mur, plafond, pilier | sources concordantes (wikily.gg, dododex, ark-unity) |
| Plafond triangle, demi-pilier, cadre double, trappe, escalier, porte secrète, mur de chaume | **estimations** : pièce absente des sources consultées |
| Rampe inclinée (Sloped Railing) | **estimation** : coût de la rambarde métal (12 lingots + 3 pâte, dododex) |
| Heavy, Tek, Tesla, Réplicateur, forge à vapeur, labo, stockage dédié Tek, générateur Tek | sources concordantes ; ark.wiki.gg donne une variante pour le labo et la Tek |
| Coffre-fort | une seule source (Sportskeeda) |

Sources :
- [wikily.gg — Steam Forge](https://wikily.gg/ark-survival-ascended/items/steam-forge/), [Makeshift Megalab](https://wikily.gg/ark-survival-ascended/items/makeshift-megalab/), [Tek Replicator](https://wikily.gg/ark-survival-ascended/items/tek-replicator/), [Tek Dedicated Storage](https://wikily.gg/ark-survival-ascended/items/tek-dedicated-storage/)
- [ark.wiki.gg — Steam Forge](https://ark.wiki.gg/wiki/Steam_Forge), [Makeshift Megalab](https://ark.wiki.gg/wiki/Makeshift_Megalab), [Tek Generator](https://ark.wiki.gg/wiki/Tek_Generator), [Tek Replicator](https://ark.wiki.gg/wiki/Tek_Replicator), [Tek Dedicated Storage](https://ark.wiki.gg/wiki/Tek_Dedicated_Storage)
- [dododex — Steam Forge](https://www.dododex.com/item/2168/steam-forge), [Makeshift Megalab](https://www.dododex.com/item/2137/makeshift-megalab), [Tek Replicator](https://www.dododex.com/item/1840/tek-replicator), [Tek Dedicated Storage](https://www.dododex.com/item/1808/tek-dedicated-storage)
- [Sportskeeda — storage structures (Vault)](https://www.sportskeeda.com/mmo/all-storage-structures-ark-survival-ascended-craft)
- [dododex — Metal Railing](https://www.dododex.com/item/1482/metal-railing)
- Autres coûts : sources du README §9.
