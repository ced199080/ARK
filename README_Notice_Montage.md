# Forteresse circulaire Ø30 sur Metal Cliff Platform — Notice de montage

Base PvP circulaire de 30 fondations pour **ARK: Survival Ascended**, posée sur une Metal Cliff Platform au sommet d'un piton rocheux en pleine mer. Le dossier contient :

- un plan découpé en 5 modules ;
- les templates **Template Hammer** (même format JSON que les exports Wikily.gg) ;
- les coordonnées de chaque pièce (CSV), pour une pose manuelle ;
- le générateur Python qui produit tout cela à partir d'une seule géométrie.

| Module | Document | Ce qu'il couvre |
|---|---|---|
| 01 | [01_Sol_Fondations_Decaissement.md](01_Sol_Fondations_Decaissement.md) | Calpinage carrés + triangles en étoile, Ø30, décaissement des 2 derniers anneaux |
| 02 | [02_Pod_Central_Atelier.md](02_Pod_Central_Atelier.md) | Pod Ø15, piliers porteurs, hall de 6 murs libres, gabarits machines, cône étanche |
| 03 | [03_Rampe_Glisse_Overhang.md](03_Rampe_Glisse_Overhang.md) | Mur de rive, pente de glisse, overhang dans le vide, jupe basse, ligne de pics |
| 04 | [04_Tourelles_DoubleDoorframes.md](04_Tourelles_DoubleDoorframes.md) | Cage 2 niveaux en double doorframes, sièges de tourelles, casquette anti-accroche |
| 05 | [05_Defense_Cap_Repartition.md](05_Defense_Cap_Repartition.md) | Turret cap, matrice Heavy/Tek/Tesla, ordre de pose, secteurs de tir, câblage |

![Coupe radiale](plans/coupe_radiale.png)

---

## 1. Ce qu'il faut retenir avant de commencer

1. **Le tracé en étoile existant est reproduit à l'identique.** Le pavage des modules est généré par une règle de croissance anneau par anneau. Sur les 7 premiers anneaux, il retombe pièce pour pièce sur le template SkunkHD « Large Cliff Platform » (n° 481) : 282/282 pièces (96 carrés + 186 triangles), contrôle intégré au script. Les anneaux 8 à 15 prolongent la même règle jusqu'au Ø30, avec zéro recouvrement et zéro jour (contrôle géométrique : aire = aire théorique du dodécagone).
2. **Avec les réglages officiels, il est impossible de poser 80 Heavy + 35 Tek.** Le turret cap compte 100 tourelles dans une sphère de 10 000 UU (≈ 33,3 fondations) de rayon. Or la base ne fait que 30 fondations de diamètre : deux tourelles quelconques de la base sont au plus à 9 414 UU l'une de l'autre, donc chacune « voit » toutes les autres. Le cap est **global** pour la forteresse, et étirer les tourelles sur la périphérie ne permet pas d'en loger davantage. Le module 05 fournit donc trois scénarios :
   - **A** : cap 100, Tesla non comptées → 65 Heavy + 35 Tek + 10 Tesla, 15 Heavy en réserve ;
   - **B** : cap 100, Tesla comptées → 55 Heavy + 35 Tek + 10 Tesla, 25 Heavy en réserve ;
   - **C** : serveur à cap ≥ 125 → tout l'inventaire est posé.
3. **Tout ce qui est sol, murs, plafonds, piliers et cadres de porte se pose en vanilla**, avec les points d'accroche normaux carrés/triangles : chaque ligne de murs suit un contour de fondations. **Les toits en dodécagone exigent Template Hammer** : aux 12 arêtes, les pièces se chevauchent, et aucune pièce vanilla ne ferme un angle de 30°. Les templates fournis 563 (Medium Cliff Base) et 717 (Hexagonal Stable) emploient la même technique.

## 2. Conventions (relevées dans les templates fournis)

| Grandeur | Valeur | Origine |
|---|---|---|
| Fondation | 300 × 300 UU ; triangle de côté 300, hauteur H = 259,81 UU | Floor_Metal / BP_TriFoundation_Metal |
| Hauteur d'un niveau (mur) | 300 UU | Wall_Metal |
| Repère | origine = centre de l'étoile ; θ = atan2(y, x) = yaw Unreal ; axe 0° = première branche de carrés (E0) | template 481 |
| Cote plan **Z** | 0 = dessus des fondations intérieures | — |
| z template | fondation : Z + 40 · mur, cadre de porte : Z_bas + 240 · plafond : Z + 90 · pilier : Z_bas + 240 · tourelle debout : Z + 100 · tourelle suspendue : Z + 90 (roll 180) | templates 1201, 1087, Coeur Base, mho |
| Triangle | pivot à mi-hauteur, yaw = direction base → pointe (un même triangle peut aussi s'écrire yaw ± 120°) | contrôle 481 : 282/282 |
| Toit incliné (MetalRoof_SM) | pente 45° (300 de course pour 300 de montée) ; centre à 150 UU en retrait du bord bas et à 150 UU au-dessus ; yaw = sens de la montée | template 2552 (Pixeleen), 563 |
| Demi-toit | 300 de large, 150 de course, 150 de montée | templates 2552, 563 |

Les toits ARK sont à 45°. C'est la pente au-delà de laquelle personnage et créatures glissent : c'est pour cela que la glisse se fait en **toits** et non en rampes (les rampes sont praticables à pied).

### Géométrie de référence : dodécagones D(n)

Chaque contour fermé du pavage est un dodécagone régulier D(n), de côté n fondations.

| Contour | Rôle | Apothème (UU) | Rayon des coins (UU) | Ø entre plats (fondations) | Pièces par côté |
|---|---|---|---|---|---|
| D1 | coins = piliers PB | 559,8 | 579,6 | 3,73 | 1 |
| D2 | coins = piliers PA | 1 119,6 | 1 159,1 | 7,46 | 2 |
| **D4** | **mur du pod** (= étoile 481) | 2 239,2 | 2 318,2 | **14,93** | 4 → 48 murs/niveau |
| **D5** | **ligne des double doorframes** | 2 799,0 | 2 897,8 | 18,66 | 5 → 60 cadres/niveau |
| **D7** | **mur de rive** | 3 918,7 | 4 056,9 | 26,12 | 7 → 84 murs/niveau |
| **D8** | **bord de la plateforme** | 4 478,5 | 4 636,4 | **29,86** | 8 |

D4 et D8 ont exactement les rayons des cercles 48 et 96 côtés de mho, fournis dans le dossier : 2 240,5 et 4 478,5 UU.

## 3. Contenu du dépôt

| Chemin | Contenu |
|---|---|
| `templates/phases/P1.json` … `P6.json` | **Templates à importer dans l'ordre de la notice** (§5) |
| `templates/0X_*.json` | Les mêmes pièces regroupées par module, avec l'extension seule du sol (`01b`) et les 3 scénarios de tourelles (`05_*_A/B/C`) |
| `donnees/*.csv` | Une ligne par pièce : type, x, y, Z plan, yaw, θ, rayon, repère (anneau, côté, index). Séparateur `;` |
| `donnees/05_matrice_tourelles.csv` | Les 125 emplacements de tourelles, l'ordre de pose et la colonne oui/réserve de chaque scénario |
| `donnees/03_ligne_pics.csv` | Les 84 emplacements de Metal Spike Walls |
| `donnees/synthese.json` | Toutes les cotes calculées : apothèmes, anneaux, secteurs de tir, comptages, bilans |
| `plans/*.png` | Plan de calpinage, coupe radiale, plan du pod, plan des tourelles et du câblage |
| `outils/forteresse.py` | Générateur (Python 3, sans dépendance pour les JSON/CSV ; matplotlib et shapely optionnels pour les plans et les contrôles) |

## 4. Pré-requis

- **Mod Template Hammer** (import Wikily.gg) sur le serveur. Testez chaque phase d'abord sur une partie solo ou un serveur de test, avec la même carte et la même plateforme.
- **Ancre centrale.** P1 pose deux demi-piliers empilés au centre de l'étoile (`snapOverrides [0,1]`, même principe que les cercles de mho). P2 à P7 portent un seul demi-pilier (`snapOverrides [0]`) à poser **sur** cette pile : c'est lui qui garantit l'alignement de toutes les phases. Laissez la pile en place jusqu'à la fin, puis démolissez-la. Elle se trouve dans la trémie centrale du hall et ne gêne rien.
  ⚠ Si votre version de Template Hammer interprète `snapOverrides` autrement, passez en placement libre et alignez visuellement le demi-pilier du template sur la pile.
- **Orientation.** L'axe 0° du template correspond à la branche de carrés de l'anneau 1 orientée vers la droite sur `plans/plan_calpinage.png`. Le motif a une symétrie de 60° : une erreur de 60°, 120° ou 180° reste invisible, une erreur de 30° ou 90° décale tout.
- **Réglages serveur à relever** : `LimitTurretsNum`, `LimitTurretsRange`, `bLimitTurretsInRange`, puis la limite de structures dans un rayon. La base totalise ≈ 4 950 structures, hors tourelles et mobilier.
- **Si l'étoile existe déjà** (template 481 ou équivalent) : sautez P1 et importez `templates/01b_sol_extension_D4_D8.json` (anneaux 8 à 15 seulement), ou posez ces anneaux à la main selon la règle du module 01 (§3).

## 5. Séquence ordonnée de pose

L'ordre suit la logique des points d'accroche d'ASA : chaque pièce s'accroche à une pièce déjà posée, et rien ne doit traverser une pièce posée plus tôt, sans quoi la prévisualisation passe au rouge (« obstructed »).

| Phase | Template | Contenu | Pièces | Lingots | Pâte |
|---|---|---|---|---|---|
| **P1 Fondations** | `phases/P1.json` | 384 fondations carrées + 768 triangles (anneaux 1-15) ; anneaux 14-15 à Z −150 | 1 154 | 38 426 | 11 912 |
| **P2 Piliers et murs porteurs** | `phases/P2.json` | 12 piliers PA de Z0 à 1800 ; mur de pod niveaux 0-5 ; fût D5 niveaux 0-5 ; rive D7 niveaux 0-1 (10 embrasures + 1 sas) | 889 | 22 213 | 6 220 |
| **P3 Plafonds intermédiaires** | `phases/P3.json` | Plancher Z1800 : mezzanine du pod (anneaux 1-7) et galerie L1 (anneaux 8-9) | 445 | 10 555 | 2 974 |
| **P4 Rampes** | `phases/P4.json` | Pente A (4 rangs), overhang (4 rangs), jupe basse (mur d'about + 2 rangs de plafonds) | 1 189 | 39 433 | 11 236 |
| **P5 Cages** | `phases/P5.json` | Double doorframes L1 et L2 (120), planchers Z2100 (avec 3 trappes) et Z2400, casquette | 517 | 13 201 | 3 724 |
| **P6 Pod haut et dôme** | `phases/P6.json` | Mur de pod niveaux 6-9 (12 accès galerie), piliers PA/PB hauts, reprise de toiture, cône 7 rangs, capuchon | 762 | 22 212 | 6 298 |
| **P7 Tourelles** | `05_tourelles_scenario_A/B/C.json` | Tourelles seules, dans l'ordre de pose (module 05) | 100 à 125 | — | — |
| P8 Manuel | — | Pics, portes, échelles, ascenseur, machines, générateurs, câbles | — | voir §6 | |

### Détail pas à pas

**P0 — Préparation**
1. Plateforme vide ou étoile existante vérifiée. Comptez 4 carrés sur chaque côté du contour extérieur de l'étoile : c'est D4.
2. Videz un rayon de 50 fondations autour du centre de toute autre tourelle de votre tribu, y compris d'un avant-poste. Explication au module 05 §2.

**P1 — Sol** (module 01)
3. Importez `P1.json` en accrochant la pile de demi-piliers au centre ; sinon importez `01b` sur l'étoile existante.
4. Contrôle : contour extérieur à 8 pièces par côté ; marche de 150 UU entre l'anneau 13 et l'anneau 14, sur tout le pourtour.

**P2 — Piliers et murs porteurs** (modules 02, 03, 04)
5. Les murs du pod (D4), du fût (D5) et de la rive (D7) suivent tous un contour de fondations : en manuel, ils s'accrochent en vanilla sur les arêtes. Montez d'abord **les piliers PA** (aux coins de D2, 6 piliers chacun), puis le mur de pod, puis le fût, puis la rive. L'ordre va de l'intérieur vers l'extérieur pour garder un accès au centre.
6. Contrôle : 4 cadres doubles au sol du pod (θ 90° et 270°), 2 au sol du fût, 1 sur la rive (sas, θ 270°), 10 murs-fenêtres sur la rive.

**P3 — Plafonds intermédiaires**
7. Posez le plancher Z1800 : il prend appui sur le haut des piliers PA, du mur de pod et du fût. Dans le pod, la trémie hexagonale centrale (6 triangles absents) reste ouverte pour l'ascenseur.
8. Contrôle : le hall mesure 6 murs libres entre Z0 et Z1800.

**P4 — Rampes** (module 03)
9. Pente A : 4 rangs de toits, du haut de la rive (Z600) jusqu'au fût. Le dernier rang passe 80 UU sous la galerie, ce qui supprime tout jour.
10. Overhang : 2 rangs au-dessus du décaissement, puis 2 rangs dans le vide (1 seul avec `--debord 1`).
11. Jupe : mur d'about à 4 518,7 UU d'apothème (Z −600 → 0), puis plafonds à Z −600 sous les rangs dans le vide.
    ⚠ Ces pièces sont dans le vide : pose en Template Hammer uniquement.

**P5 — Cages** (module 04)
12. Double doorframes L1 sur la ligne D5 (Z1800 → 2100), plancher Z2100 (anneaux 8-9, avec 3 trappes), double doorframes L2, plancher Z2400.
13. Casquette : 1 rang de toits en porte-à-faux devant la cage (2 avec `--casquette 2`).

**P6 — Pod haut et dôme** (module 02)
14. Mur de pod niveaux 6 à 9. Le niveau 6 (Z1800) porte 12 cadres doubles qui ouvrent sur la galerie. Ensuite viennent les piliers PA de Z1800 à 4050 et les piliers PB de Z1800 à 4650.
15. Reprise : 2 rangs de toits du haut de la cage jusqu'au mur de pod, où ils s'encastrent de 40 UU. Puis le cône (7 rangs), le plafond capuchon à Z5100 et 4 demi-toits en pointe.
16. Contrôle d'étanchéité : de l'intérieur, aucune lumière ne doit passer aux 12 arêtes du cône.

**P7 — Tourelles** (module 05)
17. Choisissez le scénario selon vos réglages serveur. Posez dans l'ordre du CSV (colonne `ordre`) : si le cap bloque plus tôt que prévu, la couverture reste répartie sur 360°.
18. Réglez chaque tourelle (module 05 §6) et chargez-la.

**P8 — Finitions manuelles**
19. 84 Metal Spike Walls sur le décaissement (`donnees/03_ligne_pics.csv`).
20. Portes doubles métal dans les cadres de porte (sas, hall, fût, accès galerie) ; échelles sous les 3 trappes ; ascenseur dans la trémie centrale.
21. Machines et générateurs aux gabarits (module 02 §4, module 05 §7), câblage.
22. Démolissez la pile d'ancrage centrale.

## 6. Bilan matériaux

Coûts unitaires repris de wikily.gg, dododex et ark-unity (sources §9). Les postes marqués ~ sont des estimations, faute de source pour la pièce : plafond triangle, demi-pilier, demi-toit, cadre double, mur-fenêtre, trappe. Vérifiez-les à l'établi.

### Structures (P1 à P6 + pics)

| Pièce | Quantité | Lingots/u | Pâte/u |
|---|---|---|---|
| Fondation métal | 384 | 50 | 15 |
| Fondation triangle métal | 768 | 25 | 8 |
| Mur métal | 1 195 | 25 | 7 |
| Mur-fenêtre métal (embrasures Tesla) | 10 | ~25 | ~7 |
| Cadre de porte double métal | 139 | ~25 | ~7 |
| Plafond métal | 484 | 35 | 10 |
| Plafond triangle métal | 510 | ~18 | ~5 |
| Plafond à trappe métal | 3 | ~35 | ~10 |
| Pilier métal | 264 | 25 | 7 |
| Demi-pilier métal (dont 7 ancres) | 31 | ~13 | ~4 |
| Toit incliné métal | 1 164 | 35 | 10 |
| Demi-toit métal | 4 | ~18 | ~5 |
| Mur de pics métal (manuel) | 84 | 25 (+ 20 cuir, 30 fibre) | — |
| **Total** | **≈ 5 040** | **148 140** | **42 364** |

Équivalent brut indicatif : ≈ 296 000 de minerai de métal (2 minerais par lingot) ; ≈ 169 000 de chitine ou kératine et ≈ 339 000 de pierre si la pâte est fabriquée au mortier (4 + 8 par pâte) ; 1 680 de cuir ; 2 520 de fibre.

### Tourelles (déjà en inventaire : valeur de remplacement)

| Scénario | Posées | Lingots | Pâte | Électroniques | Polymère | Cristal | Élément |
|---|---|---|---|---|---|---|---|
| A | 65 H + 35 T + 10 S | 43 600 | 14 750 | 22 050 | 9 300 | 2 000 | 105 |
| B | 55 H + 35 T + 10 S | 38 200 | 12 750 | 19 350 | 8 600 | 2 000 | 105 |
| C | 80 H + 35 T + 10 S | 51 700 | 17 750 | 26 100 | 10 350 | 2 000 | 105 |

Recettes retenues :
- **Heavy** = 1 tourelle auto (140 lingots, 50 pâte, 70 électroniques, 20 polymère) + 400 lingots, 150 pâte, 200 électroniques, 50 polymère.
- **Tek** = 100 électroniques, 100 lingots, 50 pâte, 50 polymère, 3 éléments. ark.wiki.gg y ajoute des perles de silice : à vérifier.
- **Tesla** = 500 lingots, 200 cristaux, 100 électroniques, 300 polymère.

### Consommables à stocker (non chiffrés : dépend du réglage serveur)

- Balles de fusil avancé pour les Heavy.
- Fragments d'élément pour les Tek ; élément pour les Tek Generators (4 prévus).
- Cristal pour les Tesla (munition indiquée par wikily.gg).
- Essence pour les 2 générateurs électriques de secours.

## 7. Points à valider en jeu (solo / serveur de test)

| # | Point | Pourquoi | Repli |
|---|---|---|---|
| 1 | Diamètre utile réel de votre plateforme | Le brief indique 30 fondations. Les 12 pointes de D8 vont jusqu'à 4 636 UU, contre 4 500 pour un cercle de Ø30 | Laisser vides les 12 triangles de pointe de l'anneau 15 |
| 2 | Décaissement −150 posable | Si l'étoile repose à même la plateforme, l'anneau abaissé entre dans la tôle de la plateforme | Template Hammer, ou `--decaissement 0` puis demi-murs de bordure |
| 3 | `snapOverrides` de Template Hammer | Leur interprétation dépend de la version du mod | Placement libre sur la pile d'ancrage |
| 4 | Metal Spike Wall posable sur fondation | Les murs de pics en bois exigent le sol ; pour le métal, l'avis communautaire est partagé | Les poser sur le bord de plateforme, sous l'overhang |
| 5 | Tesla comptée ou non dans le cap | Non documenté pour ASA | Scénario A ou B |
| 6 | Encombrement réel des machines | Gabarits de réservation, pas les cotes des maillages | Les gabarits laissent 300 UU de marge |
| 7 | Portée des Tek Generators | Elle doit englober la galerie (rayon ≤ 2 900 UU depuis le centre) | Câbles et générateurs électriques (module 05 §7) |
| 8 | Sous-face de la plateforme au-dessus de Z −600 | Sinon les tourelles de jupe ne voient pas sous la plateforme | Régénérer avec une jupe plus basse |

## 8. Régénérer ou adapter

```bash
python3 outils/forteresse.py                     # par défaut : overhang 2 au-delà de la plateforme, casquette 1, décaissement 150
python3 outils/forteresse.py --debord 1          # overhang d'une seule structure dans le vide
python3 outils/forteresse.py --casquette 2       # casquette plus longue (650 UU de dégagement, mais L1 ne tire plus vers le haut)
python3 outils/forteresse.py --decaissement 300  # « −1 niveau » = un mur complet au lieu d'un demi-mur
python3 outils/forteresse.py --recul 150          # tourelles au centre du plafond de niche (arc réduit, plus abritées)
python3 outils/forteresse.py --verifier-481 chemin/template-481-building-0.json   # contrôle d'alignement avec l'étoile SkunkHD
```

Les autres paramètres (hauteurs, nombre de rangs, gabarits, générateurs) sont en tête du script : dictionnaires `P`, `GABARITS` et `GENERATEURS`.

## 9. Sources

Templates fournis (zip *Construction ARK*), utilisés ainsi :
- **481** (SkunkHD, Large Cliff Platform) : étoile de référence.
- **2901 / 2902 / 2903** (mho, cercles 96/48/24) : rayons de contrôle et principe de l'ancre à demi-piliers.
- **704 / 701** (WUAN) : cercles à piliers, d'où les couronnes PA/PB.
- **563 / 717** : toitures à arêtes chevauchantes.
- **1087 / 1201 / 1809** : tours à tourelles (double doorframes, tourelles suspendues `roll 180`, Tesla latérales).
- **2727** : aide « Straight Heavy ».
- **2552** : convention de pivot des toits.
- **Coeur Base** : noyau optionnel (module 02 §7).

Sources web consultées pour les règles et les coûts :
- [ark.wiki.gg — Heavy Auto Turret](https://ark.wiki.gg/wiki/Heavy_Auto_Turret), [Tek Turret](https://ark.wiki.gg/wiki/Tek_Turret), [Turret](https://ark.wiki.gg/wiki/Turret), [Tesla Coil](https://ark.wiki.gg/wiki/Tesla_Coil)
- [wikily.gg — Heavy Auto Turret](https://wikily.gg/ark-survival-ascended/items/heavy-auto-turret/), [Tek Turret](https://wikily.gg/ark-survival-ascended/items/tek-turret/), [Tesla Coil](https://wikily.gg/ark-survival-ascended/items/tesla-coil/), [Metal Foundation](https://wikily.gg/ark-survival-ascended/items/metal-foundation/), [Metal Pillar](https://wikily.gg/ark-survival-ascended/items/metal-pillar/), [Sloped Metal Roof](https://wikily.gg/ark-survival-ascended/items/sloped-metal-roof/), [Metal Spike Wall](https://wikily.gg/ark-survival-ascended/items/metal-spike-wall/)
- [dododex — Tesla Coil](https://www.dododex.com/item/2165/tesla-coil), [Metal Triangle Foundation](https://www.dododex.com/item/1492/metal-triangle-foundation), [Metal Spike Wall](https://www.dododex.com/item/1486/metal-spike-wall)
- [ark-unity — Metal Ceiling](https://ark-unity.com/ark-survival-ascended/items/metal-ceiling-hatchframe/), [ase.gg — Metal Wall](https://ase.gg/items/metal-wall)
- [mp1st — patch Heavy Turret / turret limit](https://mp1st.com/news/ark-update-now-live-on-pc-adding-heavy-turret-doubled-tek-turret-damage), [GINX — Tesla Coil](https://www.ginx.tv/en/aberration-tesla-coil-turrets), [GINX — Tek Generator](https://www.ginx.tv/en/tek-generator-craft-uses)
