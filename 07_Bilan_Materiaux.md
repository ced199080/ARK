# Module 07 — Bilan matériaux complet et équipements

Ce bilan couvre **tout ce qu'il faut fabriquer** pour la forteresse en 6 parts (module 06) :
- la structure, le noyau central et les pics ;
- les 96 tourelles ;
- les équipements demandés : 1 Réplicateur Tek, 1 forge à vapeur, 1 labo de fortune, 20 stockages dédiés, 20 coffres-forts, 2 générateurs Tek.

Les chiffres sont recalculés par le script : `donnees/synthese.json`, clés `bilan_complet` et `bilan_total`. Positions des équipements : `donnees/07_equipements.csv`.

## 1. Total à réunir

| Ressource | Sans les tourelles (déjà en inventaire) | **Avec les 96 tourelles** |
|---|---|---|
| Lingots de métal | 196 388 | **234 788** |
| Pâte cimentée | 51 570 | **65 070** |
| Électroniques | 220 | **20 020** |
| Polymère | 5 850 | **13 350** |
| Cristal | 3 350 | **4 550** |
| Élément | 220 | **310** |
| Perles noires | 470 | 470 |
| Huile | 1 400 | 1 400 |
| Poudre étincelante | 100 | 100 |
| Cuir | 1 680 | 1 680 |
| Fibre | 2 904 | 2 904 |
| Chaume (gabarits, démolis ensuite) | 672 | 672 |
| Bois (gabarits) | 384 | 384 |

Le script crée les tourelles du plan (60 Heavy, 30 Tek, 6 Tesla), mais elles sont **déjà dans votre inventaire**. Ne fabriquez que la colonne de gauche. La réserve (20 Heavy, 5 Tek, 4 Tesla) n'est comptée nulle part.

## 2. Détail par poste

| Poste | Contenu | Lingots | Pâte | Autres |
|---|---|---|---|---|
| **6 parts : structure** | 5 826 pièces : 384 fondations, 768 triangles, 1 194 murs, 84 cadres doubles, 1 032 piliers, 216 demi-piliers, 474 plafonds, 504 plafonds triangles, 6 trappes, 1 164 toits | 165 570 | 47 898 | — |
| **Noyau central** | 35 murs, 3 portes secrètes, 6 escaliers, 58 plafonds (dont 48 triangles), 4 demi-toits | 2 536 | 716 | — |
| Ancres temporaires | 14 demi-piliers (démolis à la fin) | 182 | 56 | — |
| **Murs de pics** | 84 Metal Spike Walls | 2 100 | — | 1 680 cuir, 2 520 fibre |
| Gabarits de pose | 96 murs de chaume (démolis ensuite) | — | — | ~672 chaume, ~384 fibre, ~384 bois |
| **Équipements** | voir §3 | 26 000 | 2 900 | 220 élément, 3 350 cristal, 470 perles noires, 5 850 polymère, 220 électroniques, 100 poudre étincelante, 1 400 huile |
| *Tourelles (inventaire)* | *60 Heavy, 30 Tek, 6 Tesla* | *38 400* | *13 500* | *19 800 électroniques, 7 500 polymère, 1 200 cristal, 90 élément* |

Par part, la structure représente ≈ 27 600 lingots et ≈ 8 000 pâte. On peut donc construire et financer la base part par part.

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
| Hall Z0 (6 murs libres) | Réplicateur Tek (θ 0°) · Générateur Tek n°1 (θ 60°) · Forge à vapeur (θ 120°) · Labo de fortune (θ 240°) · 3 stockages dédiés (θ 300°) |
| Coeur Base | 1 coffre-fort « Matiere Premiere 1 » (celui de votre template, à sa place d'origine) |
| Mezzanine Z1800 | Générateur Tek n°2 (θ 180°, à 900 UU du centre) · **19 coffres-forts + 17 stockages dédiés**, en alternance contre la face intérieure du mur de pod. Cela fait 36 emplacements : positions 0, 2 et 3 de chaque côté, la position 1 étant l'accès galerie |

### Couverture des 2 générateurs Tek

Distances mesurées sur le plan, pivot à pivot :

| Générateur | Tek de L1 (alimentation Tek obligatoire) | Heavy de jupe | Tesla de rive |
|---|---|---|---|
| n°2, mezzanine (−900 ; 0), Z1800 | **1 915 → 3 760 UU** : couvre les 30 Tek s'il porte à 3 800 UU | 4 475 → 6 252 UU | 3 316 → 5 014 UU |
| n°1, hall (900 ; 1 559), Z0 | 2 196 → 5 040 UU | 2 893 → 6 651 UU | 2 176 → 5 746 UU |

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
| Minerai de métal | **≈ 393 000** | ≈ 510 000 |
| Chitine ou kératine | **≈ 253 000** | ≈ 367 000 |
| Pierre | **≈ 506 000** | ≈ 734 000 |
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
| Fondation, triangle, mur, plafond, pilier, toit | sources concordantes (wikily.gg, dododex, ark-unity) |
| Plafond triangle, demi-pilier, demi-toit, cadre double, trappe, escalier, porte secrète, mur de chaume | **estimations** : pièce absente des sources consultées |
| Heavy, Tek, Tesla, Réplicateur, forge à vapeur, labo, stockage dédié Tek, générateur Tek | sources concordantes ; ark.wiki.gg donne une variante pour le labo et la Tek |
| Coffre-fort | une seule source (Sportskeeda) |

Sources :
- [wikily.gg — Steam Forge](https://wikily.gg/ark-survival-ascended/items/steam-forge/), [Makeshift Megalab](https://wikily.gg/ark-survival-ascended/items/makeshift-megalab/), [Tek Replicator](https://wikily.gg/ark-survival-ascended/items/tek-replicator/), [Tek Dedicated Storage](https://wikily.gg/ark-survival-ascended/items/tek-dedicated-storage/)
- [ark.wiki.gg — Steam Forge](https://ark.wiki.gg/wiki/Steam_Forge), [Makeshift Megalab](https://ark.wiki.gg/wiki/Makeshift_Megalab), [Tek Generator](https://ark.wiki.gg/wiki/Tek_Generator), [Tek Replicator](https://ark.wiki.gg/wiki/Tek_Replicator), [Tek Dedicated Storage](https://ark.wiki.gg/wiki/Tek_Dedicated_Storage)
- [dododex — Steam Forge](https://www.dododex.com/item/2168/steam-forge), [Makeshift Megalab](https://www.dododex.com/item/2137/makeshift-megalab), [Tek Replicator](https://www.dododex.com/item/1840/tek-replicator), [Tek Dedicated Storage](https://www.dododex.com/item/1808/tek-dedicated-storage)
- [Sportskeeda — storage structures (Vault)](https://www.sportskeeda.com/mmo/all-storage-structures-ark-survival-ascended-craft)
- Autres coûts : sources du README §9.
