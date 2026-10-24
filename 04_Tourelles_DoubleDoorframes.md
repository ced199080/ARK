# Module 04 — Cage sur la rive, double doorframes, casquette et toit bas

Template : `templates/04_cage_rive_toit.json`, réparti dans les phases :
- **P2** : poteaux D5 et D6 ;
- **P3** : galerie L1 (Z600) ;
- **P5** : murs de coin L1, coursive L2, double doorframes L2, casquette en rampes ;
- **P6** : plancher de toit Z1200 sur toute la base, toit bas en rampes.

Les 60 tourelles de L1 et leurs murs de chaume sont dans `templates/05_tourelles_scenario_B.json` (phase **P7**).
Coordonnées : `donnees/04_cage_rive_toit.csv`, `donnees/05_matrice_tourelles.csv`. Plan des rampes : `plans/plan_rampes.png`.

**Profil bas.** La cage n'est plus au milieu de la base, perchée en haut d'une pente : elle est posée **sur le mur de rive (D7)**. Toute la base tient ainsi sous un plancher de toit à **Z1200** (4 murs), avec des rampes basses jusqu'à Z1550 environ. La version précédente culminait à Z5150.

## 1. Principe : la méthode des tours 1201 / 1809 et du template 2727

Dans les tours fournies, les tourelles ne sont pas posées debout dans les cadres. Elles sont **montées à la verticale** :
1. on remplit un emplacement de mur avec un **mur de chaume** (`Thatch_Wall_Small`), qui sert de gabarit ;
2. on fixe la tourelle sur la **face extérieure** de ce mur de chaume : pivot à 10 UU devant le plan du mur, à mi-hauteur, axe de la tourelle pointé vers l'extérieur ;
3. on **démolit le mur de chaume** en jeu.

La tourelle reste au nu de la façade, dans une ouverture de 300 × 300, avec un champ de tir d'un demi-espace (≈ 180° en azimut, comme une niche de tir). Dans la tour 1809, les étages de double doorframes et les étages de tourelles alternent. La cage reprend cette alternance :

| Étage | Z | Contenu (84 emplacements sur la ligne D7, 7 par côté) |
|---|---|---|
| Rive | 0 → 600 | mur de rive (module 03), socle de la cage |
| **L1** | 600 → 900 | **60 tourelles verticales** sur les 5 emplacements du milieu de chaque côté (30 Tek + 30 Heavy en alternance, 5 + 5 par part), chacune avec son mur de chaume de pose (phase P7). Les 2 emplacements des coins sont murés (24 murs) |
| **L2** | 900 → 1200 | **84 double doorframes** (phase P5) : à fermer par des portes doubles, ou à garder ouverts pour le tir des joueurs |

```
 Z1200 ──┬─────────────╲  casquette en rampes (porte-à-faux 300 UU)
         │ L2 ▯ cadres  ╲  bout Z900
 Z900  ──┤ L1 ▮[T]►      ·   ← tourelle verticale au nu de la façade (chaume démoli)
 Z600  ──┼────────────── ╲  overhang en rampes, jusque dans le vide
         │ rive D7        ╲
 Z0    ──┴──
```

## 2. Galerie et circulation

| Plancher | Z | Anneaux | Rôle |
|---|---|---|---|
| Galerie L1 | 600 (P3) | 12-13 (72 plafonds + 156 triangles) | coursive derrière les tourelles. **6 trappes** (1 par part, à θ ≈ 30° + 60°·k) au-dessus des passages de la colonnade, avec une échelle depuis le hall extérieur |
| Coursive L2 | 900 (P5) | 13 (36 plafonds + 78 triangles) | derrière les double doorframes. **6 trappes** (1 par part, au milieu des côtés E0) avec une échelle depuis la galerie L1 |
| Plancher de toit | 1200 (P6) | 0 à 13 : toute la base (294 plafonds + 588 triangles) | ferme la base ; porte la casquette et le toit bas |

**Appuis du plancher de toit** : le mur de pod et les piliers PA (module 02), les double doorframes L2 sur la rive, et 24 **poteaux** de 4 piliers aux sommets de D5 (rayon 2 898) et de D6 (rayon 3 477), soit 96 piliers.

Le plancher de la galerie L1 repose sur la rive et sur les poteaux de D6. Il ne dépend pas de L1 : la démolition du chaume ne le fragilise pas.

## 3. Emplacements L1 : mur de chaume + tourelle verticale

| Élément | Position | z template | Rotation |
|---|---|---|---|
| Mur de chaume | sur la ligne D7, centré sur l'emplacement | 840 | yaw = θ du côté |
| Heavy ou Tek | 10 UU devant le chaume, vers l'extérieur | 840 | pitch −89,5°, **yaw = θ + 90°**, roll −90° (template 2727) |

| Côté | p1 | p2 | p3 | p4 | p5 |
|---|---|---|---|---|---|
| 0° : chaume | (3 918,7 ; −600) | (3 918,7 ; −300) | (3 918,7 ; 0) | (3 918,7 ; 300) | (3 918,7 ; 600) |
| 0° : tourelle | (3 928,7 ; −600) Tek | (3 928,7 ; −300) Heavy | (3 928,7 ; 0) Tek | (3 928,7 ; 300) Heavy | (3 928,7 ; 600) Tek |
| 30° : chaume | (3 693,7 ; 1 439,7) | (3 543,7 ; 1 699,5) | (3 393,7 ; 1 959,3) | (3 243,7 ; 2 219,1) | (3 093,7 ; 2 478,9) |
| 30° : tourelle | (3 702,3 ; 1 444,7) Heavy | (3 552,3 ; 1 704,5) Tek | (3 402,3 ; 1 964,3) Heavy | (3 252,3 ; 2 224,1) Tek | (3 102,3 ; 2 483,9) Heavy |
| autres côtés | rotation de 60°·m du côté 0° ou du côté 30° | | | | |

Les emplacements p0 et p6, aux coins, sont murés.

**Ordre en jeu**
1. Posez les murs de chaume des 60 emplacements L1 (vanilla : un mur s'accroche sur l'arête du plancher Z600).
2. Fixez chaque tourelle sur la face extérieure de son mur de chaume, dans l'ordre du CSV. En Template Hammer, le template P7 pose les deux.
3. Rechargez et réglez les tourelles depuis la galerie.
4. **Démolissez les 60 murs de chaume.** ⚠ Faites-le d'abord sur un emplacement en solo pour vérifier que la tourelle reste en place : c'est le comportement des tours 1201/1809, mais il dépend du jeu.

Après démolition, L1 devient une bande d'ouvertures où chaque tourelle occupe le centre de la sienne. Au-dessus (casquette) et en dessous (overhang) de la fente de tir, il n'y a que des rampes inclinées, où l'on ne tient pas debout.

## 4. Pourquoi la cage est sur la rive

Une pente de rampes est à 45° : elle monte d'autant qu'elle avance. Dans la version précédente, la pente A partait de la rive (Z600) et remontait de 1 120 UU vers la cage, placée sur D5 : la cage commençait donc à Z1800. Le toit, lui, montait de 2 800 UU jusqu'au centre.

En posant la cage sur la rive :
- l'overhang garde son rôle : il part du haut de la rive et emmène dans le vide ce qui glisse ;
- la pente A disparaît ;
- le reste de la base n'a besoin que de la hauteur des machines (3 murs).

## 5. Casquette anti-accroche (en rampes inclinées)

| Rang | Apothème du bas | Z bas → haut | Lames par côté | Rampes |
|---|---|---|---|---|
| Casquette r−1 (défaut) | 4 218,7 | 900 → 1200 | 9 | 108 |
| Casquette r−2 (option `--casquette 2`) | 4 518,7 | 600 → 900 | 9 | 108 |

**Pourquoi rien ne s'accroche aux tourelles**
1. On ne tient pas debout sur une lame inclinée : ce qui touche la casquette glisse vers l'extérieur.
2. La casquette dépasse le nu de la façade de 300 UU. La tête d'une tourelle verticale fait saillie d'environ 110 UU (hypothèse : 100 UU au-delà du pivot). Ce qui quitte le bout des lames tombe donc **≈ 190 UU devant les têtes** (≈ 490 UU avec la casquette 2), puis sur l'overhang environ 600 UU plus bas, qui l'emmène dans le vide.
3. ⚠ Un joueur qui passe *entre* deux lames de la casquette (vide de 300 UU) peut tomber sur une tête de tourelle. Il est alors à bout portant des tourelles voisines. Si ce cas pose problème en test, passez à `--casquette 2`.

**Secteur de tir vertical de L1** (coupe au milieu d'un côté ; tête supposée à 110 UU devant la façade, à mi-hauteur de L1) : **−56,8° → +89,9°**, avec la casquette 1 comme avec la casquette 2. Les rampes ne masquent ni le ciel ni le sol. Vers le bas, la limite vient du haut du mur de jupe ; plus bas encore, le tir voit les paliers entre les lames de l'overhang.

## 6. Toit bas en rampes inclinées (dents de scie)

**Aucun toit incliné dans toute la base** : sur un toit à 45°, on tient debout. Le dessus de la base est donc :
1. un **plancher de toit fermé à Z1200** sur toute la base (882 pièces) ;
2. au-dessus, un **toit bas en rampes inclinées** (`StructureBP_Railing_Sloped_Metal`, la pièce des tours 1201 et 1809), en **dents de scie** de 300 UU de haut.

**Règle de pose des rampes, relevée sur la tour 1201** (la même pour la casquette et l'overhang) :
- Les rampes forment des **lames** parallèles à la pente, espacées de 300 UU (t = 0, ±300, ±600… le long de chaque côté). Les lames du toit continuent celles de la casquette et de l'overhang.
- Chaque rampe couvre 300 UU et monte de 300 UU.
- Pivot : au milieu de la rampe, 150 UU en retrait de son bas, à z template = Z du bas + 290.
- Rotation : **yaw = θ du côté − 90°** pour une rampe qui monte vers le centre (tour 1201 : yaw −90° sur le côté θ = 0°), et **θ + 90°** pour une rampe qui redescend.
- Une lame peut dépasser l'arête de son côté de 150 UU au plus. Aux 12 arêtes, l'écart entre lames reste donc ≤ 300 UU.

**Dents de scie.** Sur le toit, une rampe sur deux redescend. Chaque lame est une suite de petits faîtages de 300 UU, comme le faîtage des tours 1201 / 1809 en miniature. Elle commence en haut de la casquette et va jusqu'au centre : 13 rangs, 684 rampes, sommet à Z1500 (≈ Z1550 en haut des rampes).

- **Rien ne peut se poser** : un dino largué ne trouve aucune surface. Ce qui passe entre deux lames retombe sur le plancher fermé Z1200, sans accès vers l'intérieur.
- ⚠ **Le toit bas ne fait pas glisser jusqu'au vide.** Une pente de rampes du centre jusqu'au bord monterait d'environ 3 900 UU. C'est justement la hauteur qu'on supprime. Le glissement vers le vide commence au bord : casquette puis overhang.
- Coût : une rampe vaut environ **12 lingots + 3 pâte**, contre 35 + 10 pour un toit. ⚠ C'est une estimation : le coût de la rambarde métal (Metal Railing).
- ⚠ À valider en solo : le décalage de la rampe (+290 en z template) vient de la tour 1201, où les rampes reposent sur des cadres de porte. Si les rampes apparaissent trop haut ou trop bas, corrigez `+ 200` dans `rang_rampes()` et `toit_dents()`, puis régénérez.

## 7. Contrôles de fin de module

- [ ] 24 poteaux (D5 et D6), de Z0 à Z1200.
- [ ] Galerie L1 à Z600 avec 6 trappes ; coursive L2 à Z900 avec 6 trappes ; échelles posées à la main.
- [ ] L1 : 60 emplacements libres jusqu'à la phase P7, 24 murs de coin ; L2 : 84 double doorframes.
- [ ] P7 : 60 murs de chaume + 60 tourelles à 10 UU devant ; murs de chaume démolis à la fin.
- [ ] Casquette : 108 rampes, bout à 300 UU devant la façade, partout.
- [ ] Plancher de toit Z1200 fermé, sans jour ; 684 rampes en dents de scie au-dessus. Aucun toit incliné.
