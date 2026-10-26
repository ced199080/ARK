# Module 07 — Bilan matériaux complet et équipements

Ce bilan couvre **tout ce qu'il faut fabriquer** pour la forteresse en plans par zone, adaptée au trou (module 06) :
- la structure des plans 1 et 3 à 11 (plateforme verte comprise), les pics et les carrés de culture ;
- les options à part : colonnade (plan 2) et rehausse de la tour ;
- les 85 tourelles (49 Heavy, 26 Tek, 10 Tesla), plus 15 Plant Species X ;
- les équipements demandés : 1 Réplicateur Tek, 1 forge à vapeur, 1 labo de fortune, 20 stockages dédiés, 20 coffres-forts, 2 générateurs Tek, 2 boîtes de munitions (coût non relevé).

Les chiffres sont recalculés par le script : `donnees/synthese.json`, clés `bilan_complet`, `bilan_total` et `options`. Classeur : `donnees/07_bilan_materiaux.xlsx`, régénéré par `python3 outils/bilan_xlsx.py`. Positions des équipements : `donnees/07_equipements.csv`.

## 1. Total à réunir

| Ressource | Sans les tourelles (déjà en inventaire) | **Avec les tourelles** |
|---|---|---|
| Lingots de métal | **143 619** | **177 679** |
| Pâte cimentée | **36 489** | **47 589** |
| Électroniques | 220 | 17 050 |
| Polymère | 5 850 | 13 580 |
| Cristal | 3 350 | 5 350 |
| Élément | 220 | 298 |
| Perles noires | 470 | 470 |
| Huile | 1 400 | 1 400 |
| Poudre étincelante | 100 | 100 |
| Cuir | 1 480 | 1 480 |
| Fibre | 3 076 | 3 076 |
| Chaume (murs de chaume démolis ensuite, carrés de culture) | 1 123 | 1 123 |
| Bois (idem) | 676 | 676 |
| Pierre (carrés de culture) | 1 200 | 1 200 |

Le script place les tourelles (49 Heavy, 26 Tek, 10 Tesla), mais elles sont **déjà dans votre inventaire** : ne fabriquez que la colonne de gauche. Il reste en réserve 31 Heavy, 9 Tek et aucune Tesla. Les 15 graines de Plant Species X se récoltent (marais) et se plantent à la main.

| Option | Pièces | Lingots | Pâte |
|---|---|---|---|
| Colonnade (plan 2) | 226 piliers | +5 650 | +1 582 |
| Rehausse de la tour, par niveau | 52 murs pleins + 24 piliers | +1 900 | +532 |

Si votre étoile (anneaux 1 à 7) est déjà construite, retirez ses 87 fondations et 174 triangles hors du trou : 8 700 lingots et 2 697 pâte.

## 1 bis. Ce qui a changé avec l'audit : aucune tourelle sous Z0, noyau en cage

Par rapport à la version précédente (147 504 lingots, 37 576 pâte) :

| Changement | Pièces | Lingots | Pâte |
|---|---|---|---|
| **Jupe sur un seul niveau**, posé sur le palier 2 : le niveau suspendu sous les fondations et les 16 Heavy de jupe sont supprimés | −83 cadres doubles | −2 075 | −581 |
| **Débord d'une seule lame** (`--debord 1`), pendue au haut de la jupe : plus de 2e rang ni de poutres | −94 rampes, −94 poutres fines | −2 350 | −658 |
| **Cages du noyau** : 2 générateurs Tek et 2 boîtes de munitions sur leur fondation, au centre | +28 murs, +4 cadres doubles, +4 plafonds | +940 | +264 |
| 2e Heavy de rive (niveau 0) et tourelles reposées : murs remplacés par du chaume de pose | −14 cadres doubles, −2 murs | −400 | −112 |
| 6 carrés de culture **moyens** dans la poche du toit de cage (au lieu de grands) | — | — | — |
| **Total** | | **−3 885** | **−1 087** |

## 1 ter. Ce qui a changé avec le découpage par zones

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

- 15 carrés de culture pour les Plant X (9 grands, 6 moyens) : 360 bois, 570 chaume, 540 fibre, 1 200 pierre (estimation).
- Les coûts des piliers fins, des poutres fines et des cadres doubles sont des estimations, à vérifier en jeu.
- **Option `--appuis tours`** (sans poteaux de stabilité, comme les tours) : 896 piliers fins de moins, soit −11 648 lingots et −3 584 pâte (131 971 lingots et 32 905 pâte à fabriquer). En contrepartie, seules 48 lames du toit sur 170 et aucune de l'appentis tiennent encore si leur appui est détruit.

**Pourquoi des rampes et pas des toits** : sur un toit à 45°, on tient debout ; sur une lame de rampes inclinées, non. Seules les rampes font glisser (module 03 §7). Une rampe coûte en plus environ trois fois moins qu'un toit.

## 2. Détail par poste

| Poste | Contenu | Lingots | Pâte | Autres |
|---|---|---|---|---|
| **Structure des plans** (sans la colonnade) | 5 244 pièces : 344 fondations et 684 triangles (dont les 10 pièces de la plateforme verte), 515 murs pleins, 681 cadres doubles, 240 piliers, 311 plafonds, 629 plafonds triangles, 6 trappes, 6 escaliers, 758 rampes inclinées (aucun toit), 1 027 piliers fins, 43 demi-piliers fins | 115 665 | 33 557 | — |
| Carrés de culture | 9 grands et 6 moyens (Plant X) | — | — | 360 bois, 570 chaume, 540 fibre, 1 200 pierre |
| Ancres temporaires | 8 demi-piliers (démolis à la fin) | 104 | 32 | — |
| **Murs de pics** | 74 Metal Spike Walls | 1 850 | — | 1 480 cuir, 2 220 fibre |
| Gabarits de pose | 79 murs de chaume (démolis ensuite) | — | — | ~553 chaume, ~316 fibre, ~316 bois |
| **Équipements** | voir §3 (boîtes de munitions non chiffrées) | 26 000 | 2 900 | 220 élément, 3 350 cristal, 470 perles noires, 5 850 polymère, 220 électroniques, 100 poudre étincelante, 1 400 huile |
| *Tourelles (inventaire)* | *49 Heavy, 26 Tek, 10 Tesla* | *34 060* | *11 100* | *16 830 électroniques, 7 730 polymère, 2 000 cristal, 78 élément* |

Le détail plan par plan (pièces, nombre de structures, coût de chaque pièce, total du plan, puis récapitulatif de tous les plans) est dans l'onglet « Coût par plan » du classeur, et au module 06 §5 : on peut construire et financer la base plan par plan.

## 3. Équipements

| Équipement | Qté | Recette unitaire | Atelier | Total |
|---|---|---|---|---|
| **Réplicateur Tek** | 1 | 5 000 lingots, 800 polymère, 600 cristal, 150 perles noires, 100 élément | (tekgramme) | — |
| **Forge à vapeur** (Steam Forge, Steampunk Ascent) | 1 | 3 250 lingots, 1 000 polymère, 600 pâte, 500 cristal, 200 électroniques | Fabricator ; engram Forge industrielle requis ; forge alimentée à l'élément | — |
| **Labo de fortune** (Makeshift Megalab) | 1 | 450 lingots, 300 pâte, 250 cristal, 150 polymère, 100 poudre étincelante, 20 électroniques | Fabricator | — |
| **Stockage dédié Tek** (Tek Dedicated Storage) | 20 | 125 lingots, 75 cristal, 55 polymère, 4 perles noires, 3 élément | Tek Replicator | 2 500 lingots, 1 500 cristal, 1 100 polymère, 80 perles noires, 60 élément |
| **Coffre-fort** (Vault) | 20 | 500 lingots, 100 pâte, 90 polymère, 70 huile ⚠ une seule source | Fabricator / Replicator | 10 000 lingots, 2 000 pâte, 1 800 polymère, 1 400 huile |
| **Générateur Tek** | 2 | 2 400 lingots, 500 polymère, 250 cristal, 120 perles noires, 30 élément | Tek Replicator | 4 800 lingots, 1 000 polymère, 500 cristal, 240 perles noires, 60 élément |
| **Boîte de munitions** (Ammo Box) | 2 | ⚠ non relevée : à lire à l'établi | — | non compté |

Ordre de fabrication logique :
1. Réplicateur Tek (Fabricator ou tekgramme).
2. Générateurs Tek et stockages dédiés (au Réplicateur).
3. Forge à vapeur, labo et coffres-forts (au Fabricator).

### Emplacements (hors plan, `donnees/07_equipements.csv`)

| Lieu | Équipements |
|---|---|
| Noyau Z0 (anneau 1, en cage) | Générateur Tek n°1, principal (θ 180°) · Générateur Tek n°2, secours (θ 240°) · 2 boîtes de munitions (θ 60° et 120°). Module 02 §6.1 |
| Hall Z0 (6 murs libres) | Réplicateur Tek (θ 0°) · Forge à vapeur (θ 120°) · Labo de fortune (θ 240°) · **9 stockages dédiés** (θ 300°, 2 rangées de 4 et 5 dos à dos, allée de 329 UU entre la rangée extérieure et le mur de pod). Le trou occupe la branche θ 180° |
| Mezzanine Z1800 | **20 coffres-forts + 11 stockages dédiés**, en alternance contre la face intérieure du mur de pod. Cela fait 31 emplacements : positions 0, 2 et 3 de chaque côté, la position 1 étant l'accès galerie, moins les 5 coupés par le trou |

### Couverture des 2 générateurs Tek

Les 2 générateurs sont au noyau, à 410 UU du centre. Chacun atteint les **26 Tek** à **2 620 → 3 811 UU** : L1, tour D4, bord du trou et dessus. Réglez-les tous deux à **3 850 UU** au moins : le n°2 est le secours du n°1. Les Heavy et les Tesla sont électriques : distances au noyau au module 05 §8.

⚠ Réglez la portée au maximum et vérifiez la sphère affichée.
- Si un générateur n'atteint pas 3 850 UU, il faut un 3ᵉ générateur près de la galerie.
- Les Heavy et les Tesla sont électriques. Si elles restent hors de portée, il faut des câbles et un générateur électrique : ce matériel n'est pas dans votre liste et n'est pas compté ici.

## 4. Équivalent en ressources brutes

Recettes usuelles, à vérifier sur votre serveur :
- lingot = 2 minerais de métal ;
- électronique = 1 lingot + 3 perles de silice ;
- polymère = 2 obsidiennes + 2 pâtes cimentées ;
- pâte = 4 chitine ou kératine + 8 pierres ;
- poudre étincelante = 2 silex + 1 pierre.

| Ressource brute | Sans les tourelles | Avec les tourelles |
|---|---|---|
| Minerai de métal | **≈ 288 000** | ≈ 389 000 |
| Chitine ou kératine | **≈ 193 000** | ≈ 299 000 |
| Pierre | **≈ 387 000** | ≈ 599 000 |
| Obsidienne | ≈ 11 700 | ≈ 27 200 |
| Perles de silice | ≈ 660 | ≈ 51 200 |
| Silex | 200 | 200 |
| Cristal / élément / perles noires / huile | 3 350 / 220 / 470 / 1 400 | 5 350 / 298 / 470 / 1 400 |

Avec du polymère organique ou de la pâte d'Achatina, la pierre, la chitine et l'obsidienne baissent fortement.

## 5. Consommables (non chiffrés)

- Balles de fusil avancé (Heavy), fragments d'élément (Tek), à charger dans les 2 boîtes de munitions du noyau, cristal (Tesla, munition indiquée par wikily.gg), eau et engrais (Plant X).
- Élément pour les 2 générateurs Tek et la forge à vapeur.

## 6. Fiabilité des chiffres

| Donnée | Statut |
|---|---|
| Fondation, triangle, mur, plafond, pilier | sources concordantes (wikily.gg, dododex, ark-unity) |
| Plafond triangle, demi-pilier, cadre double, trappe, escalier, porte secrète, mur de chaume, grand et moyen carrés de culture | **estimations** : pièce absente des sources consultées |
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
