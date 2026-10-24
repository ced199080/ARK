# Forteresse circulaire Ø30 sur Metal Cliff Platform — Notice de montage

Base PvP circulaire de 30 fondations pour **ARK: Survival Ascended**, posée sur une Metal Cliff Platform au sommet d'un piton rocheux en pleine mer.

La forteresse se compose de **6 parts égales de 60°** et d'un **noyau central** : votre Coeur Base et son escalier. Le dossier contient :
- un plan par module ;
- les templates **Template Hammer** (format JSON des exports Wikily.gg), par part et par phase ;
- les coordonnées de chaque pièce (CSV) ;
- le bilan matériaux complet ;
- le générateur Python qui produit tout cela.

| Module | Document | Ce qu'il couvre |
|---|---|---|
| 01 | [01_Sol_Fondations_Decaissement.md](01_Sol_Fondations_Decaissement.md) | Calpinage carrés + triangles en étoile, Ø30, **bord abaissé en 2 paliers** (Ø26 → −150, Ø28 → −300) |
| 02 | [02_Pod_Central_Atelier.md](02_Pod_Central_Atelier.md) | Coeur Base au centre, pod Ø15, hall de 4 murs avec **les machines les plus hautes au centre**, stockage, générateurs |
| 03 | [03_Rampe_Glisse_Overhang.md](03_Rampe_Glisse_Overhang.md) | Mur de rive (socle de la cage), colonnade circulaire de piliers côte à côte (1 rang), **overhang en rampes inclinées**, mur de jupe, ligne de pics |
| 04 | [04_Tourelles_DoubleDoorframes.md](04_Tourelles_DoubleDoorframes.md) | **Cage posée sur la rive** : L1 = 60 tourelles verticales, L2 = 84 double doorframes, casquette ; **plancher de toit Z1200 et toit bas en rampes** |
| 05 | [05_Defense_Cap_Repartition.md](05_Defense_Cap_Repartition.md) | Cap 100 (Tesla comptées), 96 tourelles verticales (16 par part), ordre de pose, couverture, câblage |
| **06** | [06_Plan_6_Parts.md](06_Plan_6_Parts.md) | **Plan complet en 6 parts égales** (sol, structure, tourelles) et noyau central |
| **07** | [07_Bilan_Materiaux.md](07_Bilan_Materiaux.md) | **Bilan matériaux complet**, équipements compris : réplicateur, forge à vapeur, labo de fortune, 20 stockages dédiés, 20 coffres-forts, 2 générateurs Tek |

![Les 6 parts](plans/plan_6_parts.png)

---

## 1. Ce qu'il faut retenir

1. **6 parts identiques.** Chaque part couvre 60° et contient 779 pièces de structure et 16 tourelles. Le script vérifie que les 6 parts coïncident après rotation. Seul le **noyau central** (le Coeur Base, 84 pièces) se pose une fois. Les outils de production et de stockage ne font partie d'aucun template.
2. **96 tourelles** (cap 100, Tesla comptées) : 60 Heavy, 30 Tek et 6 Tesla, soit 16 par part. Le maximum symétrique avec 35 Tek et 10 Tesla est 96. Restent en réserve 20 Heavy, 5 Tek et 4 Tesla ; les 4 Tesla peuvent être ajoutées à la main pour atteindre 100.
3. **L'étoile existante est reproduite à l'identique** : les anneaux 1 à 7 retombent pièce pour pièce sur le template SkunkHD 481.
4. **Les tourelles sont verticales**, comme dans le template *Straight Heavy* (2727) et les tours 1201/1809 :
   - elles sont posées sur un mur de chaume de pose ;
   - **vous démolissez les 96 murs de chaume en jeu**.
5. **Profil bas et discret.** La base culmine à **Z1550 environ (5 murs)** au lieu de Z5150 :
   - la cage à tourelles est posée sur le mur de rive (L1 à Z600, L2 à Z900) ;
   - un seul plancher de toit fermé couvre toute la base à **Z1200 (4 murs)** ;
   - les machines les plus hautes (réplicateur Tek, forge) sont **au centre**, dans le hall du pod, qui a 4 murs de hauteur libre.
6. **Aucun toit incliné : des rampes partout.** Sur un toit à 45°, on tient debout ; sur des rampes inclinées (Sloped Railing), rien ne tient. La casquette et l'overhang font glisser jusqu'au vide. Le toit bas est en dents de scie de 300 UU : rien ne peut s'y poser. Au total, **1 224 rampes inclinées** en lames, comme sur les tours 1201 et 1809.
   Il reste à fabriquer (hors tourelles, déjà en inventaire) ≈ **139 100 lingots de métal** et **34 700 pâte cimentée**, contre 196 400 et 51 600 dans la première version. S'y ajoutent cristal, élément, perles noires, polymère et huile pour les équipements (module 07).
7. **Bord abaissé deux fois** : l'anneau 14 (Ø26 → Ø28) est à −150, l'anneau 15 (Ø28 → Ø30) à −300.
8. Sol, murs, plafonds, piliers et cadres se posent en vanilla. Les rampes inclinées, la colonnade, le Coeur Base sur l'étoile et les pièces dans le vide exigent **Template Hammer**.

## 2. Conventions (relevées dans les templates fournis)

| Grandeur | Valeur | Origine |
|---|---|---|
| Fondation | 300 × 300 UU ; triangle de côté 300, hauteur 259,81 | Floor_Metal / BP_TriFoundation_Metal |
| Niveau (mur) | 300 UU | Wall_Metal |
| Repère | origine = centre de l'étoile et du Coeur Base ; θ = atan2(y, x) = yaw Unreal ; axe 0° = première branche de carrés | templates 481 et Coeur Base |
| Cote plan **Z** | 0 = dessus des fondations intérieures | — |
| z template | fondation Z + 40 · mur, cadre Z_bas + 240 · plafond Z + 90 · pilier Z_bas + 240 | templates 1201, 1087, Coeur Base, mho |
| Triangle | pivot à mi-hauteur, yaw = base → pointe (aussi valable à ± 120°) | contrôle 481 : 282/282 |
| Rampe inclinée (StructureBP_Railing_Sloped_Metal) | lames au pas de 300 ; +300 UU en hauteur par pas de 300 UU ; pivot au milieu de la rampe, z template = Z du bas + 290 ; yaw = θ du côté − 90° ; seule pièce de pente de la base | tours 1201, 1809 |
| Tourelle verticale | mur de chaume dans l'emplacement ; pivot 10 UU devant, à mi-hauteur ; Heavy/Tek : pitch −89,5°, yaw θ_tir + 90°, roll −90° ; Tesla : pitch 0°, yaw θ_tir + 90°, roll −90° | templates 2727, 1809, 1201 |
| Pilier « large » | Pillar_Metal, largeur prise à 39,3 UU (1 pilier / 1 vide) | template 704 |
| Part k | secteur θ ∈ [−14,5° + 60°·(k−1) ; 45,5° + 60°·(k−1)[ | module 06 |

### Contours de référence : dodécagones D(n)

| Contour | Rôle | Apothème (UU) | Rayon des coins | Ø entre plats (fondations) | Pièces par côté |
|---|---|---|---|---|---|
| D1 / D2 | coins = piliers PB / PA | 559,8 / 1 119,6 | 579,6 / 1 159,1 | 3,73 / 7,46 | 1 / 2 |
| **D4** | mur du pod (= étoile 481) | 2 239,2 | 2 318,2 | 14,93 | 4 |
| **D5** / **D6** | poteaux du plancher de toit (sommets) | 2 799,0 / 3 358,8 | 2 897,8 / 3 477,4 | 18,66 / 22,39 | 5 / 6 |
| *cercle* | colonnade | rayon 3 360 | — | 22,4 | 264 positions |
| **D7** | mur de rive et cage | 3 918,7 | 4 056,9 | 26,12 | 7 |
| **D8** | bord de la plateforme | 4 478,5 | 4 636,4 | 29,86 | 8 |

## 3. Contenu du dépôt

| Chemin | Contenu |
|---|---|
| `templates/parts/Part_1_structure.json` … `Part_6_structure.json` | **Structure de chaque part**, déjà tournée, triée par phase |
| `templates/parts/Part_1_tourelles.json` … `Part_6_tourelles.json` | 16 paires mur de chaume + tourelle par part |
| `templates/parts/Noyau_central.json` | Coeur Base et son escalier |
| `templates/phases/P1.json` … `P7.json` | Les mêmes pièces, découpées par phase sur tout le tour (méthode alternative) |
| `templates/0X_*.json` | Les mêmes pièces regroupées par module, plus l'extension seule du sol (`01b`) |
| `references/Coeur_Base.json` | Votre template Coeur Base, que le générateur lit |
| `donnees/06_part_1_structure.csv` | Toutes les pièces de la part 1 avec leur phase. Pour la part k, tourner de 60°·(k−1) |
| `donnees/07_equipements.csv` | Positions des équipements, hors plan |
| `donnees/*.csv`, `donnees/synthese.json` | Coordonnées par module, matrice des tourelles, colonnade, pics, toutes les cotes et tous les bilans |
| `plans/*.png` | Les 6 parts, calpinage, coupe radiale, pod, plan des rampes, tourelles et câblage |
| `outils/forteresse.py` | Générateur (Python 3) |

## 4. Pré-requis

- Mod **Template Hammer**. Testez d'abord en solo, avec la même plateforme.
- **Pile d'ancrage en (0 ; 300)**, au sommet de l'hexagone central situé à θ 90° : le centre exact est réservé à la porte secrète du Coeur Base.
  - `Part_1_structure` (ou `P1`) pose 2 demi-piliers empilés (`snapOverrides [0,1]`).
  - Tous les autres templates portent 1 demi-pilier qui se pose sur cette pile (`snapOverrides [0]`).
  - Démolissez la pile à la fin.
- **Orientation** : l'axe 0° du template correspond à la branche de carrés orientée vers la droite sur `plans/plan_calpinage.png`. Les templates de part sont déjà tournés : aucune rotation à faire à l'import.
- **Réglages serveur** : `LimitTurretsNum`, `LimitTurretsRange`, limite de structures. La base compte ≈ 4 850 structures, plus 96 tourelles et 96 murs de chaume temporaires.
- **Étoile déjà construite** : utilisez `templates/01b_sol_extension_D4_D8.json` à la place du sol des parts, ou retirez le sol (phase P1) des templates de part.

## 5. Séquence de pose

### Méthode A : par parts (module 06)

| Étape | Template | Contenu |
|---|---|---|
| 1 | `parts/Part_1_structure.json` | sol, piliers, murs, colonnade, galerie, overhang, cage, plancher de toit et toit bas du secteur 1, triés par phase ; contient la pile d'ancrage |
| 2-6 | `parts/Part_2_structure.json` … `Part_6_structure.json` | idem pour les secteurs 2 à 6 |
| 7 | `parts/Noyau_central.json` | Coeur Base et son escalier |
| 8-13 | `parts/Part_k_tourelles.json` | 16 paires mur de chaume + tourelle par part |
| 14 | à la main | voir « Finitions » ci-dessous |

### Méthode B : par phases, couche par couche sur tout le tour

C'est la méthode à utiliser si Template Hammer refuse des pièces faute d'appui dans la part voisine.

| Phase | Template | Contenu | Pièces | Lingots | Pâte |
|---|---|---|---|---|---|
| P1 Fondations | `phases/P1.json` | 384 carrés + 768 triangles ; anneau 14 à Z −150, anneau 15 à Z −300 | 1 154 | 38 426 | 11 912 |
| P2 Piliers et murs porteurs | `phases/P2.json` | Coeur Base niveau 1, mur de pod (4 niveaux), piliers PA, poteaux D5/D6, colonnade, rive | 760 | 19 013 | 5 325 |
| P3 Plafonds intermédiaires | `phases/P3.json` | Coeur Base Z300 et niveau 2, galerie L1 Z600 | 298 | 6 896 | 1 940 |
| P4 Rampes de glisse | `phases/P4.json` | overhang en rampes inclinées, mur de jupe | 649 | 10 597 | 2 812 |
| P5 Cage sur la rive | `phases/P5.json` | murs de coin L1, coursive L2 Z900, 84 double doorframes L2, casquette en rampes | 337 | 6 883 | 1 894 |
| P6 Toit | `phases/P6.json` | plancher de toit Z1200 sur toute la base, 684 rampes en dents de scie | 1 567 | 29 095 | 7 936 |
| P7 Tourelles | `phases/P7.json` | 96 paires mur de chaume + tourelle | 193 | — | — |

### Finitions (dans les deux méthodes)

1. **Démolissez les 96 murs de chaume.** Testez d'abord sur une tourelle qu'elle reste en place.
2. Posez les 84 Metal Spike Walls (`donnees/03_ligne_pics.csv`), soit 14 par part.
3. Posez les portes doubles : 6 au sol du pod, cadres de L2. Ajoutez les échelles sous les 12 trappes (6 de la galerie L1, 6 de la coursive L2).
4. Posez les équipements aux emplacements prévus (module 07 §3) et le câblage (module 05 §8).
5. Démolissez la pile d'ancrage.

## 6. Bilan matériaux (détail : module 07)

| Poste | Lingots | Pâte | Autres |
|---|---|---|---|
| 6 parts (structure, 4 674 pièces) | 108 924 | 31 260 | — |
| Noyau central (84 pièces) | 1 895 | 531 | — |
| Ancres (14 demi-piliers, temporaires) | 182 | 56 | — |
| 84 murs de pics | 2 100 | — | 1 680 cuir, 2 520 fibre |
| 96 murs de chaume (gabarits) | — | — | ~672 chaume, ~384 fibre, ~384 bois |
| Équipements : 1 réplicateur, 1 forge à vapeur, 1 labo de fortune, 20 stockages dédiés, 20 coffres-forts, 2 générateurs Tek | 26 000 | 2 900 | 220 élément, 3 350 cristal, 470 perles noires, 5 850 polymère, 220 électroniques, 100 poudre étincelante, 1 400 huile |
| **Total à fabriquer** | **139 101** | **34 747** | — |
| *Tourelles (60 H, 30 T, 6 S), en inventaire* | *38 400* | *13 500* | *19 800 électroniques, 7 500 polymère, 1 200 cristal, 90 élément* |

Équivalent brut (hors tourelles) : ≈ 279 000 minerai de métal, ≈ 186 000 chitine ou kératine, ≈ 372 000 pierre.

Si votre étoile (anneaux 1 à 7) est déjà construite, retirez encore 96 fondations et 192 triangles : 9 600 lingots et 2 976 pâte.

## 7. Points à valider en jeu (solo / serveur de test)

| # | Point | Repli |
|---|---|---|
| 1 | La tourelle reste en place quand on démolit son mur de chaume | Laisser le chaume, ou un mur métal derrière la tourelle |
| 2 | Une part posée d'un bloc ne se fait pas refuser de pièces faute d'appui | Méthode B (phases) |
| 3 | Un mur de chaume s'accroche sous le mur de jupe | Template Hammer |
| 4 | Largeur réelle du pilier métal (colonnade 1 pilier / 1 vide) | Ajuster `largeur_pilier` et régénérer |
| 5 | Coeur Base posé sur l'étoile | Template Hammer, centré sur la pile |
| 6 | Diamètre utile de la plateforme (les 12 pointes de D8 vont à 4 636 UU) | Laisser vides les triangles de pointe de l'anneau 15 |
| 7 | Paliers −150 et −300 posables | `--decaissement 0` |
| 8 | `snapOverrides` de Template Hammer | Placement libre sur la pile (0 ; 300) |
| 9 | Metal Spike Wall sur fondation | Bord de plateforme, sous l'overhang |
| 10 | Portée des 2 générateurs Tek ≥ 4 300 UU (les 30 Tek de la cage) ; alimentation de la jupe et des Tesla | 3ᵉ générateur dans la galerie L1, câbles et générateur électrique |
| 11 | Sous-face de la plateforme au-dessus de Z −600 | Jupe plus basse |
| 12 | Coût du coffre-fort (une seule source) et des pièces marquées ~ | Vérifier à l'établi |
| 13 | Hauteur des rampes inclinées par rapport à leurs appuis (décalage relevé sur la tour 1201) | Corriger `+ 200` dans `rang_rampes()` et `toit_dents()` |
| 14 | Un joueur ne tient pas debout sur une lame de rampes, et glisse | Lames plus serrées (pas de 150) |
| 15 | Le réplicateur Tek et la forge tiennent sous 4 murs (3 murs réservés) | Un niveau de plus partout (`rive_niveaux` ou `cage_niveaux`, et `pod_niveaux`) |

## 8. Régénérer ou adapter

```bash
python3 outils/forteresse.py                        # défaut : 6 parts, overhang 2, casquette 1, paliers de 150, colonnade r=3360
python3 outils/forteresse.py --colonnade 2560       # colonnade plus près du pod
python3 outils/forteresse.py --coeur-rotation 60    # Coeur Base tourné (multiples de 60°)
python3 outils/forteresse.py --debord 1             # overhang d'une seule structure dans le vide (sans jupe)
python3 outils/forteresse.py --casquette 2          # casquette plus longue
python3 outils/forteresse.py --decaissement 300     # paliers d'un mur complet (−300 puis −600)
python3 outils/forteresse.py --verifier-481 chemin/template-481-building-0.json
```

Les autres paramètres (inventaire, cap, nombre de parts, colonnade, emplacements des équipements, générateurs) sont en tête du script : `P`, `GABARITS`, `GENERATEURS`.

## 9. Sources

Templates fournis (zip *Construction ARK*), utilisés ainsi :
- **Coeur Base** (le vôtre) : noyau central ;
- **481** (SkunkHD) : étoile de référence ;
- **2901 / 2902 / 2903** (mho) : rayons et ancre ;
- **704 / 701** (WUAN) : cercles de piliers et colonnade ;
- **2727**, **1809**, **1201** : tourelles verticales sur chaume, Tesla latérales ; **toit en rampes inclinées** (1201, 1809) ;
- **1087** : double doorframes ;
- **2552** : repère des pièces de toit (plus utilisées : aucun toit incliné).

Sources web :
- [ark.wiki.gg — Heavy Auto Turret](https://ark.wiki.gg/wiki/Heavy_Auto_Turret), [Tek Turret](https://ark.wiki.gg/wiki/Tek_Turret), [Turret](https://ark.wiki.gg/wiki/Turret), [Tesla Coil](https://ark.wiki.gg/wiki/Tesla_Coil), [Steam Forge](https://ark.wiki.gg/wiki/Steam_Forge), [Makeshift Megalab](https://ark.wiki.gg/wiki/Makeshift_Megalab), [Tek Generator](https://ark.wiki.gg/wiki/Tek_Generator), [Tek Replicator](https://ark.wiki.gg/wiki/Tek_Replicator), [Tek Dedicated Storage](https://ark.wiki.gg/wiki/Tek_Dedicated_Storage)
- [wikily.gg — Heavy Auto Turret](https://wikily.gg/ark-survival-ascended/items/heavy-auto-turret/), [Tek Turret](https://wikily.gg/ark-survival-ascended/items/tek-turret/), [Tesla Coil](https://wikily.gg/ark-survival-ascended/items/tesla-coil/), [Metal Foundation](https://wikily.gg/ark-survival-ascended/items/metal-foundation/), [Metal Pillar](https://wikily.gg/ark-survival-ascended/items/metal-pillar/), [Sloped Metal Roof](https://wikily.gg/ark-survival-ascended/items/sloped-metal-roof/), [Metal Spike Wall](https://wikily.gg/ark-survival-ascended/items/metal-spike-wall/), [Steam Forge](https://wikily.gg/ark-survival-ascended/items/steam-forge/), [Makeshift Megalab](https://wikily.gg/ark-survival-ascended/items/makeshift-megalab/), [Tek Replicator](https://wikily.gg/ark-survival-ascended/items/tek-replicator/), [Tek Dedicated Storage](https://wikily.gg/ark-survival-ascended/items/tek-dedicated-storage/)
- [dododex — Tesla Coil](https://www.dododex.com/item/2165/tesla-coil), [Metal Triangle Foundation](https://www.dododex.com/item/1492/metal-triangle-foundation), [Metal Spike Wall](https://www.dododex.com/item/1486/metal-spike-wall), [Steam Forge](https://www.dododex.com/item/2168/steam-forge), [Makeshift Megalab](https://www.dododex.com/item/2137/makeshift-megalab), [Tek Replicator](https://www.dododex.com/item/1840/tek-replicator), [Tek Dedicated Storage](https://www.dododex.com/item/1808/tek-dedicated-storage)
- [dododex — Metal Railing](https://www.dododex.com/item/1482/metal-railing), [ark.wiki.gg — Metal Railing](https://ark.wiki.gg/wiki/Metal_Railing) (coût repris pour la rampe inclinée)
- [ark-unity — Metal Ceiling](https://ark-unity.com/ark-survival-ascended/items/metal-ceiling-hatchframe/), [ase.gg — Metal Wall](https://ase.gg/items/metal-wall), [Sportskeeda — Vault](https://www.sportskeeda.com/mmo/all-storage-structures-ark-survival-ascended-craft)
- [mp1st — turret limit](https://mp1st.com/news/ark-update-now-live-on-pc-adding-heavy-turret-doubled-tek-turret-damage), [GINX — Tesla Coil](https://www.ginx.tv/en/aberration-tesla-coil-turrets), [GINX — Tek Generator](https://www.ginx.tv/en/tek-generator-craft-uses)
