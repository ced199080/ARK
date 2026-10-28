# Module 03 — Rive, rampes de glisse, overhang dans le vide (et colonnade en option)

Templates (`templates/plans/`, module 06) :

| Plan | Contenu |
|---|---|
| `Plan_03_bord_D8-D7.json` | mur de rive D7 et mur de jupe D8 en **cadres doubles**, murs de chaume des tourelles de la rive |
| `Plan_04_D7-D5_pente_A.json` | **rampes extérieures** : pente A, overhang et débord en rampes inclinées, sur les mêmes lignes, et leurs **poteaux de piliers fins** ; murs de bord du trou entre D5 et D7, en cadres doubles |
| `Plan_02_colonnade_option.json` | **option** : colonnade circulaire sous la pente A |

**Murs : cadres de porte doubles** (`BP_DoubleDoorframe_Metal`, la pièce des tours 1201 et 1809), partout sauf la tour du pod.

**Aucun toit incliné.** Sur un toit à 45°, on tient debout et rien ne glisse. Toutes les pentes sont donc faites de **rampes inclinées** (Sloped Railing), en lignes de lames au pas de 300 UU comme sur les tours 1201 et 1809.

**Comment une ligne de rampes tient en jeu** (essais en solo, module 08 §3.1) :
- une lame ne tient qu'à la **tête d'un poteau de piliers fins entiers**, debout sur un **coin de fondation** (carrée ou triangle), au **centre d'une fondation carrée** ou sur un **coin de plafond** ; les lames voisines de la ligne s'y enchaînent ;
- jusqu'à **3 lames pendues** à la suite sous un poteau, jusqu'à 6 lames qui montent au-dessus ;
- **ne tiennent pas une lame** : le haut d'un mur, un pilier fin dans le joint d'un mur, une colonne de piliers fins dans un mur, un demi-pilier fin, le bord d'un plafond ; le pilier fin ne se pose pas au milieu d'une arête.

Le générateur place donc chaque ligne pour que ses jonctions tombent au-dessus de ces points : il la décale de 0 à 300 UU vers l'extérieur, ce qui la remonte d'autant. Les lignes ne s'appuient plus sur la rive : elles passent **au-dessus**.

**Le trou** (module 06) coupe la rive, la colonnade, les rampes extérieures, la jupe et les pics à l'avant, entre θ ≈ 155° et 205°. Les chiffres ci-dessous sont ceux de la base avec le trou.

Les tourelles de la rive se posent avec le plan 7 (module 05). Leurs murs de chaume sont dans le plan 3, à leur place dans la colonne de murs.

**Aucune tourelle sous le niveau des fondations centrales (Z0).** Les 16 Heavy de la jupe, qui pendaient sous la plateforme, sont supprimées. Leurs places du cap vont à une 2e Heavy de rive par côté, au niveau 0 (Z0 → 300), et à L1.

Coordonnées : `donnees/Plan_03_*.csv`, `donnees/Plan_04_*.csv`, `donnees/03_colonnade.csv`, `donnees/03_ligne_pics.csv`. Coupe (θ 0°, hors trou, tracé sans le décalage des lignes) : `plans/coupe_radiale.png`. Rampes : `plans/plan_rampes.png`.

![Coupe radiale](plans/coupe_radiale.png)

## 1. Ordre des couches, du pod vers le vide

| Couche | Rayon / apothème (UU) | Rôle |
|---|---|---|
| Tour du pod (mur D4) | 2 239 | module 02 |
| Couloir, fût de cage D5 | 2 239 → 2 799 | module 04 |
| Attique A, sous la pente A, poteaux | 2 799 → 3 919 | §3 et §4 |
| Colonnade (option) | 3 600 (cercle) | §3 |
| Mur de rive D7 | 3 919 | §2 |
| Palier 1 (Z −150) | 3 919 → 4 179 | module 01 §4 |
| **Ligne de Metal Spike Walls** | 4 069, sur le palier 1 | §6 |
| Palier 2 (Z −300) | 4 179 → 4 479 | module 01 §4 |
| Bord de plateforme D8 : mur de jupe | 4 479 | §5 |
| Débord de rampes dans le vide | 4 479 → 4 929 | §5 |

## 2. Mur de rive (D7), en cadres doubles

| Niveau | Z | Contenu (84 positions = 12 côtés × 7, dont 10 au-dessus du trou) |
|---|---|---|
| 0 | 0 → 300 | **63 cadres doubles** + **11 murs de chaume** de Heavy, une par côté (mur 1 ou 5 des côtés E0 et E1, à l'opposé de celle du niveau 1). Pas de sas : l'accès se fait par Tek Teleporter, ou par une porte double dans un cadre |
| 1 | 300 → 600 | **58 cadres doubles** + **16 murs de chaume** de tourelles : 5 Tesla au milieu des côtés E0 (θ 0°, 60°, 120°, 240°, 300°) et 11 Heavy, une par côté (milieu des côtés E1, mur 1 ou 5 des côtés E0) |

- **2 Heavy par côté**, à 2 niveaux et à 600 UU l'une de l'autre au moins : chaque côté du dodécagone et ses paliers sont vus par 2 tourelles. Elles sont toutes au-dessus de Z0, sur la fondation de l'anneau 13.
- Les 3 emplacements qui tombent dans le trou (la Tesla de 180° et les 2 Heavy du côté 180°) sont reposés sur les murs de bord du trou, face au gouffre (module 06 §4).
- Au droit du trou, la rive est remplacée par les **murs de bord du trou** (module 06 §3).
- **Cadres doubles** : chaque cadre laisse une ouverture de porte double. Les tourelles, qui sont derrière, tirent au travers, comme sur les tours 1201 et 1809. Posez des portes doubles dans les cadres que vous voulez fermer.
- **Après démolition du chaume**, chaque emplacement de tourelle est une ouverture de 300 × 300, la tourelle au nu du mur.

## 3. Attique A : poteaux, colonnade en option

Les poteaux des rampes extérieures (§4) sont des colonnes de piliers fins : dans l'attique, sous les lignes des côtés à triangles, et sur le palier 2, sous celles des côtés à carrés.

**Colonnade (plan 2, option).** Couronne de **piliers métal sur un vrai cercle** de rayon **3 600 UU**, chaque pilier tourné vers le centre, selon le principe des cercles de piliers fournis (704, 701) :

| Paramètre | Valeur |
|---|---|
| Pas | 1 pilier / 1 vide de la largeur d'un pilier : 288 positions, pas de 1,25° (78,5 UU d'arc) |
| Passages | 6, à θ 30° + 60°·k, dans l'axe des portes du fût |
| Colonnes | **224 piliers**, 1 de haut : 288 positions − 24 pour les passages − 36 au-dessus du trou − 4 qui heurtaient un mur de chaume du bord du trou ou un poteau |
| Coût | 5 600 lingots, 1 568 pâte |
| Compatibilité | elle s'efface devant les poteaux : vous pouvez la poser ou non |

Si vous l'excluez, ne posez pas le plan 2. Rien ne s'y appuie.

## 4. Rampes extérieures : pente A, overhang, débord

Une seule nappe de lignes radiales, de la cage jusqu'au vide : la **pente A** monte de la rive vers la cage, l'**overhang** descend au-dessus des 2 paliers, le **débord** finit dans le vide. Toutes dans le plan 4, avec leurs poteaux.

| Côtés | Lignes | Décalage | Lames par ligne | Poteau (un par ligne) | Passage sur la rive |
|---|---|---|---|---|---|
| **à carrés** (θ 0°, 60°, 120°, 240°, 300°) | t = ±150, ±450, ±750, ±1 050 | 110 UU | 6 : 3 de pente A, 2 d'overhang, 1 de débord (5 aux coins) | **2 piliers fins au centre d'une fondation du palier 2** (Z −300 → 300) : 2 lames pendues dessous, 4 qui montent | 110 UU au-dessus du haut de la rive |
| **à triangles** (θ 30°, 90°…) | t = 0, ±300, ±600, ±900 | 40 UU | 5 : 3 de pente A, 2 d'overhang | **3 piliers fins sur un coin de fondation** de l'attique (Z0 → 900) : 3 lames pendues dessous, 2 qui montent | 40 UU au-dessus |
| près du trou (θ 150°, 210°) | t = ±150… | — | 4 | 4 piliers fins au centre d'une fondation de l'attique | — |

| Rang | Z bas → haut (sans le décalage) | **Rampes posées** |
|---|---|---|
| pente A r0, r1, r2 | 600 → 1500 | 75 + 75 + 65 = **215** |
| overhang r−1, r−2 | 0 → 600 | 71 + 62 = **133** |
| débord r−3 | −300 → 0 | **40** (côtés à carrés) |
| **Total** | | **388**, sur 75 lignes, avec **79 poteaux** (210 piliers fins) |

- La pente s'arrête 330 UU devant le fût D5 (côtés à carrés) ou 260 UU (côtés à triangles).
- Une ligne de 3 lames, au milieu des côtés à triangles (t = 0), a 2 poteaux : elle tient encore si l'un est détruit. Les autres lignes n'ont qu'un poteau possible : si on le détruit, la ligne tombe.
- Ce qui passe entre deux lames tombe dans l'attique A (Z0) : 5 carrés de culture de Plant Species X et le tir de L1 l'y attendent (module 05).
- Au droit du trou, les lignes s'arrêtent au bord du gouffre.

## 5. Mur de jupe et débord dans le vide

### 5.1 Mur de jupe : sur le bord de la plateforme

- **Sur l'arête extérieure de l'anneau 15** (bord D8, apothème 4 478,5), 8 cadres doubles par côté.
- **1 niveau**, de Z −300 à 0, posé sur le palier 2. **83 cadres doubles.** Rien n'est posé sous les fondations.
- **Aucune tourelle** : les Heavy de la jupe sont remplacées par la 2e Heavy de rive (§2).
- **Pas de plafonds de jupe.** Sous des rampes, ils formeraient un palier où l'on pourrait se poser.
- Les lignes de rampes passent au-dessus de la jupe sans la toucher.

### 5.2 Débord

- Sur les côtés à carrés, chaque ligne finit par une lame dans le vide (r−3), **450 UU au-delà du bord de la plateforme** (Z −300). Elle pend à la suite de l'overhang sous le poteau du palier 2.
- Sur les côtés à triangles, le poteau est dans l'attique : 3 lames pendues au plus, l'overhang s'arrête 80 UU après le bord de la plateforme, sans débord.
- `--debord 2` n'a plus d'effet (4 lames pendues : trop).

## 6. Ligne de pics protégée (bordure basse)

- **74 Metal Spike Walls**, à l'apothème **4 068,7** et à **Z −150** sur le palier 1, pointes vers l'extérieur (`donnees/03_ligne_pics.csv`).
- L'overhang passe 640 à 710 UU au-dessus d'eux. Ce qui passe entre deux lames tombe sur les pics, sous le tir de la Heavy et de la Tesla de rive de son côté.
- ⚠ La pose d'un mur de pics métal sur fondation est à valider en solo. Repli : bord de plateforme à l'apothème 4 520, sous le rang r−2.

## 7. Glissement : du faîtage jusqu'au vide

Sur une lame inclinée à 45°, ni un joueur ni un dino ne tient debout. Ce qui touche les rampes glisse le long des lames, vers l'extérieur :

| # | Rampes | De → à | À la sortie |
|---|---|---|---|
| 1 | Toit du pod (module 02 §8) | faîtage → bord de la couronne D4 (Z3000 à 3300) | tombe dans la poche du toit de cage (Z2400), au pied de la tour : anneau de tourelles D4, Plant X |
| 2 | Appentis, puis casquette (module 04) | Z2700 → D5 (Z2400) → 3 099 (Z2100) | chute sur la pente A, devant la tête des tourelles L1 |
| 3 | Pente A | → rive (40 à 110 UU au-dessus de son haut) | continue sur l'overhang, sur la même ligne |
| 4 | Overhang, puis débord | → 80 à 450 UU au-delà du bord de la plateforme | **dans le vide** |
| — | Au droit du trou : toit, pente A | jusqu'au bord du gouffre | **dans le trou** |

**Entre les lames** (vide de 300 UU) :

| Où | On tombe sur | Défense |
|---|---|---|
| Toit du pod | le plancher de toit Z3000 | tourelles et Plant X du dessus |
| Appentis | la poche du toit de cage Z2400 | anneau D4 de la tour, Plant X, Tesla |
| Casquette | une tête de tourelle L1, ou la pente A | L1 à bout portant |
| Pente A | l'attique A (Z0) | Plant X, tir de L1 entre les lames |
| Overhang r−1, r−2 | les paliers de bord | pics, Heavy et Tesla de rive |
| Débord r−3 | le vide, le long de la jupe | 2 Heavy de rive et L1 tirent vers la mer ; sous la plateforme, aucune tourelle (§5.1) |

## 8. Contrôles de fin de module

- [ ] Rive : 2 niveaux de cadres doubles (121), 27 murs de chaume (niveau 0 : 11 Heavy ; niveau 1 : 5 Tesla, 11 Heavy) ; remplacée par les murs de bord au droit du trou.
- [ ] Rampes extérieures (plan 4) : 388 rampes sur 75 lignes, 79 poteaux (210 piliers fins) ; chaque poteau sur un coin ou un centre de fondation. Jupe : 83 cadres doubles sur le palier 2, rien sous Z0. Aucune rampe au-dessus du trou.
- [ ] Colonnade : posée ou non (option) ; elle s'efface devant les poteaux.
- [ ] Aucune lame ne prend appui sur un mur de chaume.
- [ ] 74 pics posés sous r−1.
