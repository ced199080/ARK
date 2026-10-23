# Forteresse circulaire Ø30 sur Metal Cliff Platform — Notice de montage

Base PvP circulaire de 30 fondations pour **ARK: Survival Ascended**, posée sur une Metal Cliff Platform au sommet d'un piton rocheux en pleine mer. Le dossier contient :

- un plan découpé en 5 modules ;
- les templates **Template Hammer** (même format JSON que les exports Wikily.gg) ;
- les coordonnées de chaque pièce (CSV), pour une pose manuelle ;
- le générateur Python qui produit tout cela à partir d'une seule géométrie.

| Module | Document | Ce qu'il couvre |
|---|---|---|
| 01 | [01_Sol_Fondations_Decaissement.md](01_Sol_Fondations_Decaissement.md) | Calpinage carrés + triangles en étoile, Ø30, décaissement des 2 derniers anneaux |
| 02 | [02_Pod_Central_Atelier.md](02_Pod_Central_Atelier.md) | **Coeur Base au centre** et son escalier prolongé, pod Ø15, piliers porteurs, hall de 6 murs libres, gabarits machines, cône étanche |
| 03 | [03_Rampe_Glisse_Overhang.md](03_Rampe_Glisse_Overhang.md) | Mur de rive, **colonnade circulaire de piliers côte à côte**, pente de glisse, overhang dans le vide, jupe, ligne de pics |
| 04 | [04_Tourelles_DoubleDoorframes.md](04_Tourelles_DoubleDoorframes.md) | Cage : **L1 = 60 tourelles verticales**, L2 = 60 double doorframes, casquette anti-accroche |
| 05 | [05_Defense_Cap_Repartition.md](05_Defense_Cap_Repartition.md) | **Scénario B** (cap 100, Tesla comptées), montage vertical sur murs de chaume, ordre de pose, couverture, câblage |

![Coupe radiale](plans/coupe_radiale.png)

---

## 1. Ce qu'il faut retenir avant de commencer

1. **Le tracé en étoile existant est reproduit à l'identique.** Les anneaux 1 à 7 retombent pièce pour pièce sur le template SkunkHD 481 (282/282 pièces, contrôle intégré au script). Les anneaux 8 à 15 prolongent la même règle jusqu'au Ø30, sans recouvrement ni jour.
2. **Le Coeur Base est le centre du cercle.** Votre template est repris tel quel, avec ses portes secrètes, son escalier et son coffre « Matiere Premiere 1 ». Seules ses 10 fondations, sur une grille tournée de −30°, sont remplacées par l'étoile. Son escalier est prolongé jusqu'à la mezzanine (Z1800).
3. **La colonnade suit votre schéma** : base du pod → piliers larges côte à côte (1 posé, 1 vide de la largeur d'un pilier) → Metal Spike Walls. C'est un cercle de 256 colonnes de piliers métal à 3 360 UU du centre, au pas du template 704.
4. **Toutes les tourelles sont verticales**, selon la méthode du template *Straight Heavy* (2727) et des tours 1201/1809 :
   - un **mur de chaume** de pose occupe l'emplacement ;
   - la tourelle est fixée sur sa face extérieure ;
   - **vous démolissez le chaume en jeu**.
   Le template P7 contient les 100 murs de chaume et les 100 tourelles, par paires.
5. **Scénario B** : cap 100, Tesla comptées. Sont posées 55 Heavy + 35 Tek + 10 Tesla = 100 ; 25 Heavy restent en réserve. Les tourelles de la base sont au plus à 9 692 UU les unes des autres, donc le cap de 100 dans 10 000 UU vaut pour toute la forteresse.
6. **Sol, murs, plafonds, piliers PA/PB et cadres se posent en vanilla**, avec les accroches carré/triangle. Le reste exige **Template Hammer** :
   - toitures dodécagonales ;
   - colonnade sur cercle ;
   - Coeur Base posé sur l'étoile ;
   - pièces dans le vide (overhang, jupe).

## 2. Conventions (relevées dans les templates fournis)

| Grandeur | Valeur | Origine |
|---|---|---|
| Fondation | 300 × 300 UU ; triangle de côté 300, hauteur 259,81 | Floor_Metal / BP_TriFoundation_Metal |
| Niveau (mur) | 300 UU | Wall_Metal |
| Repère | origine = centre de l'étoile et du Coeur Base ; θ = atan2(y, x) = yaw Unreal ; axe 0° = première branche de carrés | templates 481 et Coeur Base |
| Cote plan **Z** | 0 = dessus des fondations intérieures | — |
| z template | fondation Z + 40 · mur, cadre Z_bas + 240 · plafond Z + 90 · pilier Z_bas + 240 | templates 1201, 1087, Coeur Base, mho |
| Triangle | pivot à mi-hauteur, yaw = base → pointe (un même triangle s'écrit aussi yaw ± 120°) | contrôle 481 : 282/282 |
| Toit (MetalRoof_SM) | 45° ; centre à 150 UU en retrait du bord bas et 150 UU au-dessus ; yaw = sens de montée | templates 2552, 563 |
| **Tourelle verticale** | mur de chaume dans l'emplacement ; pivot 10 UU devant le plan du mur, à mi-hauteur ; Heavy/Tek : pitch −89,5°, yaw θ_tir + 90°, roll −90° ; Tesla : pitch 0°, yaw θ_tir + 90°, roll −90° | templates 2727, 1809, 1201 |
| Pilier « large » | Pillar_Metal, largeur prise à 39,3 UU (48 piliers sur r = 600 = 1 pilier / 1 vide) | template 704 |

### Contours de référence : dodécagones D(n)

| Contour | Rôle | Apothème (UU) | Rayon des coins (UU) | Ø entre plats (fondations) | Pièces par côté |
|---|---|---|---|---|---|
| D1 / D2 | coins = piliers PB / PA | 559,8 / 1 119,6 | 579,6 / 1 159,1 | 3,73 / 7,46 | 1 / 2 |
| **D4** | mur du pod (= étoile 481) | 2 239,2 | 2 318,2 | 14,93 | 4 → 48 / niveau |
| **D5** | cage (L1 tourelles, L2 cadres) | 2 799,0 | 2 897,8 | 18,66 | 5 → 60 / niveau |
| *cercle* | **colonnade** | rayon 3 360 | — | 22,4 | 264 positions |
| **D7** | mur de rive | 3 918,7 | 4 056,9 | 26,12 | 7 → 84 / niveau |
| **D8** | bord de la plateforme | 4 478,5 | 4 636,4 | 29,86 | 8 |

## 3. Contenu du dépôt

| Chemin | Contenu |
|---|---|
| `templates/phases/P1.json` … `P7.json` | **Templates à importer dans l'ordre de la notice** (§5) |
| `templates/0X_*.json` | Les mêmes pièces regroupées par module, plus l'extension seule du sol (`01b`) |
| `references/Coeur_Base.json` | Votre template Coeur Base, que le générateur lit |
| `donnees/*.csv` | Une ligne par pièce : type, x, y, Z plan, yaw, θ, rayon, repère. Séparateur `;` |
| `donnees/05_matrice_tourelles.csv` | Les 100 tourelles : ordre, couche, mur de chaume, pivot, sens de tir |
| `donnees/03_colonnade.csv`, `03_ligne_pics.csv` | Colonnes de la colonnade (composition, sommet) et 84 pics |
| `donnees/synthese.json` | Toutes les cotes calculées, les comptages, les bilans et les contrôles |
| `plans/*.png` | Calpinage, coupe radiale, plan du pod (Coeur Base), plan des tourelles et du câblage |
| `outils/forteresse.py` | Générateur (Python 3 ; matplotlib et shapely sont optionnels) |

## 4. Pré-requis

- Mod **Template Hammer** sur le serveur. Testez chaque phase d'abord en solo ou sur un serveur de test, avec la même plateforme.
- **Pile d'ancrage.** P1 pose 2 demi-piliers empilés en **(0 ; 300)** (`snapOverrides [0,1]`), au sommet de l'hexagone central situé à θ 90°. Le centre exact est réservé à la porte secrète centrale du Coeur Base. Les phases P2 à P7 portent 1 demi-pilier (`snapOverrides [0]`) qui se pose sur cette pile. Après P2, la pile se trouve dans la pièce du niveau 1 du Coeur Base : on y entre par sa porte d'entrée. Démolissez-la à la fin.
  ⚠ Si votre version de Template Hammer interprète `snapOverrides` autrement, passez en placement libre sur la pile.
- **Orientation.** Le Coeur Base n'a pas de symétrie de rotation : l'axe 0° du template doit correspondre exactement à la branche de carrés orientée vers la droite sur `plans/plan_calpinage.png`.
- **Réglages serveur** : `LimitTurretsNum`, `LimitTurretsRange`, et la limite de structures dans un rayon. La base compte ≈ 6 000 structures, hors 100 tourelles et 100 murs de chaume temporaires.
- **Si l'étoile existe déjà** : remplacez P1 par `templates/01b_sol_extension_D4_D8.json`, ou par la pose manuelle du module 01 §3.

## 5. Séquence ordonnée de pose

| Phase | Template | Contenu | Pièces | Lingots | Pâte |
|---|---|---|---|---|---|
| **P1 Fondations** | `phases/P1.json` | 384 carrés + 768 triangles ; anneaux 14-15 à Z −150 | 1 154 | 38 426 | 11 912 |
| **P2 Piliers et murs porteurs** | `phases/P2.json` | Coeur Base niveau 1 (murs, portes secrètes, escalier, coffre) ; piliers PA de Z0 à 1800 ; **colonnade** (256 colonnes) ; mur de pod niveaux 0-5 ; fût D5 ; rive D7 (sas ; 10 emplacements Tesla laissés libres) | 1 925 | 45 617 | 12 849 |
| **P3 Plafonds intermédiaires** | `phases/P3.json` | Coeur Base : plancher Z300 et murs du niveau 2 ; 5 escaliers jusqu'à Z1800 ; mezzanine (avec trémie) et galerie Z1800 | 513 | 12 116 | 3 415 |
| **P4 Rampes** | `phases/P4.json` | Pente A (4 rangs), overhang (4 rangs), jupe (mur d'about + plafonds) | 1 189 | 39 433 | 11 236 |
| **P5 Cage** | `phases/P5.json` | Planchers Z2100 (3 trappes) et Z2400 ; 60 double doorframes L2 ; casquette. L1 reste libre pour P7 | 457 | 11 701 | 3 304 |
| **P6 Pod haut et dôme** | `phases/P6.json` | Mur de pod niveaux 6-9 (12 accès galerie) ; piliers PA/PB hauts ; reprise ; cône ; capuchon | 762 | 22 212 | 6 298 |
| **P7 Tourelles** | `phases/P7.json` (= `05_tourelles_scenario_B.json`) | 100 paires mur de chaume + tourelle verticale, dans l'ordre de pose | 201 | voir §6 | |
| P8 Manuel | — | Démolition du chaume, pics, portes, échelles, machines, générateurs, câbles, démolition de l'ancre | — | — | — |

### Détail pas à pas

**P0 — Préparation**
1. Plateforme vide ou étoile existante vérifiée (4 pièces par côté sur le contour D4).
2. Aucune autre tourelle de votre tribu à moins d'environ 50 fondations du centre.

**P1 — Sol** (module 01)
3. Importez `P1.json` en accrochant la pile en (0 ; 300). Si l'étoile existe déjà, importez `01b`.
4. Contrôle : 8 pièces par côté sur le contour D8 ; marche de 150 UU entre l'anneau 13 et l'anneau 14.

**P2 — Piliers et murs porteurs** (modules 02, 03, 04)
5. Le template P2 pose le niveau 1 du Coeur Base au centre, les 12 colonnes PA (6 piliers chacune), la colonnade circulaire, puis le mur de pod, le fût et la rive.
   En manuel : d'abord les piliers PA puis les murs, de l'intérieur vers l'extérieur ; la colonnade en Template Hammer.
6. Contrôle :
   - Coeur Base complet au niveau 1 ;
   - 2 passages dans la colonnade, à θ 90° et 270° ;
   - sur la rive niveau 1, 10 trous aux emplacements Tesla.

**P3 — Plafonds intermédiaires**
7. Plancher Z300 et niveau 2 du Coeur Base. Escalier empilé jusqu'à Z1800. Mezzanine et galerie Z1800.
8. Contrôle : le hall offre 6 murs libres autour du Coeur Base ; on sort de l'escalier par la trémie de la mezzanine.

**P4 — Rampes** (module 03)
9. Pente A, overhang et jupe. Les pièces dans le vide se posent en Template Hammer uniquement.

**P5 — Cage** (module 04)
10. Planchers Z2100 et Z2400, double doorframes L2, casquette. L'étage L1 reste ouvert.

**P6 — Pod haut et dôme** (module 02)
11. Mur de pod niveaux 6-9, piliers hauts, reprise, cône, capuchon. Contrôle d'étanchéité depuis l'intérieur.

**P7 — Tourelles** (module 05)
12. Importez `P7.json`, ou posez à la main dans l'ordre du CSV : à chaque fois le mur de chaume, puis la tourelle sur sa face.
13. Contrôle du compteur : 100 posées.
14. Réglez, alimentez et chargez les tourelles.

**P8 — Finitions manuelles**
15. **Démolissez les 100 murs de chaume.** Testez d'abord sur une tourelle que celle-ci reste en place.
16. Posez les 84 Metal Spike Walls (`donnees/03_ligne_pics.csv`).
17. Posez les portes doubles (sas, hall, fût, accès galerie, cadres L2), les échelles sous les trappes, les machines et les générateurs, puis le câblage.
18. Démolissez la pile d'ancrage.

## 6. Bilan matériaux

Les coûts unitaires viennent de wikily.gg, dododex et ark-unity (§9). Les postes marqués ~ sont estimés : plafond triangle, demi-pilier, demi-toit, cadre double, trappe, escalier, porte secrète, mur de chaume.

### Structures (P1 à P6 + pics)

| Pièce | Quantité | Lingots/u | Pâte/u |
|---|---|---|---|
| Fondation métal | 384 | 50 | 15 |
| Fondation triangle métal | 768 | 25 | 8 |
| Mur métal (dont 35 du Coeur Base) | 1 230 | 25 | 7 |
| Cadre de porte double métal | 79 | ~25 | ~7 |
| Plafond métal | 487 | 35 | 10 |
| Plafond triangle métal | 552 | ~18 | ~5 |
| Plafond à trappe métal | 3 | ~35 | ~10 |
| Pilier métal (dont 816 de colonnade) | 1 080 | 25 | 7 |
| Demi-pilier métal (dont 208 de colonnade et 7 ancres) | 239 | ~13 | ~4 |
| Toit incliné métal | 1 164 | 35 | 10 |
| Demi-toit métal | 4 | ~18 | ~5 |
| Escalier métal (1 du Coeur Base + 5) | 6 | ~50 | ~15 |
| Porte secrète métal (Coeur Base) | 3 | ~25 | ~7 |
| Mur de pics métal (manuel) | 84 | 25 (+ 20 cuir, 30 fibre) | — |
| **Total** | **≈ 6 080** (+ le coffre du Coeur Base) | **171 605** | **49 014** |

Équivalent brut indicatif :
- ≈ 343 000 de minerai de métal ;
- ≈ 196 000 de chitine ou kératine et ≈ 392 000 de pierre pour la pâte faite au mortier ;
- 1 680 de cuir et 2 520 de fibre.

**Gabarits temporaires** : 100 murs de chaume, ≈ 700 chaume + 400 fibre + 400 bois (estimation). Ils sont démolis en P8.

### Tourelles posées (scénario B, déjà en inventaire : valeur de remplacement)

| Posées | Lingots | Pâte | Électroniques | Polymère | Cristal | Élément |
|---|---|---|---|---|---|---|
| 55 Heavy + 35 Tek + 10 Tesla | 38 200 | 12 750 | 19 350 | 8 600 | 2 000 | 105 |

Recettes retenues :
- **Heavy** = tourelle auto (140 lingots, 50 pâte, 70 électroniques, 20 polymère) + 400 / 150 / 200 / 50 ;
- **Tek** = 100 électroniques, 100 lingots, 50 pâte, 50 polymère, 3 éléments ;
- **Tesla** = 500 lingots, 200 cristaux, 100 électroniques, 300 polymère.

**Consommables** : balles de fusil avancé, fragments d'élément, élément pour 4 Tek Generators, cristal, essence pour 2 générateurs.

## 7. Points à valider en jeu (solo / serveur de test)

| # | Point | Repli |
|---|---|---|
| 1 | La tourelle reste en place quand on démolit son mur de chaume | Méthode des tours 1201/1809 à vérifier sur une tourelle ; sinon laissez le chaume, ou remplacez-le par un mur métal derrière la tourelle |
| 2 | Un mur de chaume s'accroche sous un plafond ou sous un mur (jupe) | Template Hammer |
| 3 | Largeur réelle du pilier métal (colonnade 1 pilier / 1 vide) | Ajuster `largeur_pilier` et régénérer |
| 4 | Coeur Base posé sur l'étoile (ses murs ne sont pas sur des arêtes) | Template Hammer, centré sur la pile |
| 5 | Diamètre utile de la plateforme : les 12 pointes de D8 vont à 4 636 UU | Laisser vides les triangles de pointe de l'anneau 15 |
| 6 | Décaissement −150 posable | Template Hammer, ou `--decaissement 0` |
| 7 | `snapOverrides` de Template Hammer | Placement libre sur la pile (0 ; 300) |
| 8 | Metal Spike Wall sur fondation | Bord de plateforme, sous l'overhang |
| 9 | Portée des Tek Generators ; alimentation de la Tesla | Câbles et générateurs de secours (module 05 §8) |
| 10 | Sous-face de la plateforme au-dessus de Z −600 | Jupe plus basse |
| 11 | Encombrement réel des machines | Les gabarits laissent de la marge |

## 8. Régénérer ou adapter

```bash
python3 outils/forteresse.py                        # défaut : overhang 2, casquette 1, décaissement 150, colonnade r=3360
python3 outils/forteresse.py --colonnade 2560       # colonnade dans le couloir, sous la galerie (6 piliers de haut)
python3 outils/forteresse.py --coeur-rotation 240   # Coeur Base tourné (multiples de 60°)
python3 outils/forteresse.py --debord 1             # overhang d'une seule structure dans le vide (sans jupe)
python3 outils/forteresse.py --casquette 2          # casquette plus longue (L1 ne tire plus vers le haut)
python3 outils/forteresse.py --decaissement 300     # « −1 niveau » = un mur complet
python3 outils/forteresse.py --verifier-481 chemin/template-481-building-0.json
```

Les autres paramètres (inventaire, cap, jupe, passages de la colonnade, gabarits, générateurs) sont en tête du script : `P`, `GABARITS`, `GENERATEURS`.

## 9. Sources

Templates fournis (zip *Construction ARK*), utilisés ainsi :
- **Coeur Base** (le vôtre) : noyau central et escalier ;
- **481** (SkunkHD, Large Cliff Platform) : étoile de référence ;
- **2901 / 2902 / 2903** (mho) : rayons de contrôle et ancre à demi-piliers ;
- **704 / 701** (WUAN) : cercles de piliers, d'où la colonnade (pas 1 pilier / 1 vide) et les couronnes PA/PB ;
- **563 / 717** : toitures à arêtes chevauchantes ;
- **2727** (*Straight Heavy*), **1809**, **1201** : tourelles verticales sur murs de chaume de pose, Tesla latérales ;
- **1087** : tourelles en double doorframes ;
- **2552** : convention de pivot des toits.

Sources web consultées pour les règles et les coûts :
- [ark.wiki.gg — Heavy Auto Turret](https://ark.wiki.gg/wiki/Heavy_Auto_Turret), [Tek Turret](https://ark.wiki.gg/wiki/Tek_Turret), [Turret](https://ark.wiki.gg/wiki/Turret), [Tesla Coil](https://ark.wiki.gg/wiki/Tesla_Coil)
- [wikily.gg — Heavy Auto Turret](https://wikily.gg/ark-survival-ascended/items/heavy-auto-turret/), [Tek Turret](https://wikily.gg/ark-survival-ascended/items/tek-turret/), [Tesla Coil](https://wikily.gg/ark-survival-ascended/items/tesla-coil/), [Metal Foundation](https://wikily.gg/ark-survival-ascended/items/metal-foundation/), [Metal Pillar](https://wikily.gg/ark-survival-ascended/items/metal-pillar/), [Sloped Metal Roof](https://wikily.gg/ark-survival-ascended/items/sloped-metal-roof/), [Metal Spike Wall](https://wikily.gg/ark-survival-ascended/items/metal-spike-wall/)
- [dododex — Tesla Coil](https://www.dododex.com/item/2165/tesla-coil), [Metal Triangle Foundation](https://www.dododex.com/item/1492/metal-triangle-foundation), [Metal Spike Wall](https://www.dododex.com/item/1486/metal-spike-wall)
- [ark-unity — Metal Ceiling](https://ark-unity.com/ark-survival-ascended/items/metal-ceiling-hatchframe/), [ase.gg — Metal Wall](https://ase.gg/items/metal-wall)
- [mp1st — patch Heavy Turret / turret limit](https://mp1st.com/news/ark-update-now-live-on-pc-adding-heavy-turret-doubled-tek-turret-damage), [GINX — Tesla Coil](https://www.ginx.tv/en/aberration-tesla-coil-turrets), [GINX — Tek Generator](https://www.ginx.tv/en/tek-generator-craft-uses)
