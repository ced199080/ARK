# Module 04 — Cage D5 → D4 : cadres doubles, tourelles verticales, casquette et appentis

Template : `templates/plans/Plan_06_D5-D4_cage_et_appentis.json` (module 06). Les tourelles de L1 se posent avec `Plan_07_tourelles_D8-D4.json` (module 05). Leurs murs de chaume sont dans le plan 6, à leur place dans la ligne D5.

Coordonnées : `donnees/Plan_06_*.csv`, `donnees/Plan_07_*.csv`, `donnees/05_matrice_tourelles.csv`.

La cage est l'anneau entre le fût **D5** et la tour du pod **D4**. Au-dessus de la cage, un **appentis** en rampes monte du haut de D5 vers la tour, et la **casquette** pend vers l'extérieur. La tour du pod dépasse de la cage, et son toit se pose sur la tour (module 02 §8).

**Le trou** (module 06) coupe la cage à l'avant : 7 des 60 emplacements de la ligne D5 sont au-dessus du gouffre. La cage y est fermée par les murs de bord du couloir, et les tourelles L1 qui y tombaient sont reposées sur des murs de bord, au même niveau L1, face au gouffre (couche TROU-L1).

## 1. Principe : la méthode des tours 1201 / 1809 et du template 2727

**Murs : cadres de porte doubles** (`BP_DoubleDoorframe_Metal`), comme les 873 cadres de la tour 1201 et les 802 de la tour 1809. Toute la ligne D5, du sol au toit de cage, est en cadres doubles.

Les tourelles sont **montées à la verticale**, comme dans le template 2727 et la tour 1809 :
1. un emplacement de mur reçoit un **mur de chaume** (`Thatch_Wall_Small`), qui sert de gabarit ;
2. la tourelle est fixée sur la **face extérieure** de ce mur de chaume : pivot à 10 UU devant le plan du mur, à mi-hauteur, axe pointé vers l'extérieur ;
3. on **démolit le mur de chaume** en jeu.

La tourelle reste au nu de la façade, dans une ouverture de 300 × 300, avec un champ de tir d'un demi-espace :

| Étage | Z | Contenu (60 positions sur la ligne D5, 53 hors du trou) |
|---|---|---|
| Fût | 0 → 1800 | **318 cadres doubles** (6 niveaux) |
| **L1** | 1800 → 2100 | **31 murs de chaume + tourelles** (16 Tek, 15 Heavy, alternées), répartis régulièrement autour du cercle ; **22 cadres doubles** aux autres positions |
| **L2** | 2100 → 2400 | **53 cadres doubles** |

Les 4 tourelles L1 coupées par le trou (2 Tek, 2 Heavy) sont sur des murs de bord du couloir et du pod, au niveau 6.

```
            appentis ╱╲ casquette
 Z2400 ──┬──────────╱──╲   (rampes : monte vers la tour, pend vers l'extérieur)
         │ L2 ▯ cadres  ╲  bout Z2100
 Z2100 ──┤ L1 ▮[T]► ou ▯  ·   ← tourelle verticale au nu de la façade (chaume démoli)
 Z1800 ──┴───────────── ╲
  galerie (anneaux 8-9) │fût (cadres doubles) ╲ pente A
```

## 2. Fût (support de la cage)

- Cadres doubles sur D5 de Z0 à Z1800 : 6 niveaux × 53 positions hors du trou = **318 cadres doubles**. Chaque cadre est une ouverture vers l'attique A : posez des portes doubles là où vous voulez fermer.
- Au droit du trou, la cage est fermée par les murs de bord du couloir (4 arêtes, 8 niveaux jusqu'à Z2400, en cadres doubles, module 06 §3).
- Le fût porte le plancher Z1800 côté extérieur, et la tour du pod le porte côté intérieur.

## 3. Galerie : planchers et circulation

Les planchers reprennent les anneaux 8 et 9 du pavage, en plafonds. Le trou retire 20 pièces par plancher : **142 pièces par plancher, 426 en tout** (136 plafonds, 285 triangles, 5 trappes).

| Plancher | Z | Rôle |
|---|---|---|
| Galerie L1 | 1800 | coursive de service derrière les tourelles ; accès depuis la mezzanine par les 11 cadres du niveau 6 de la tour |
| Galerie L2 | 2100 | coursive derrière les cadres L2 ; 5 plafonds à trappe (côtés E1) + échelles |
| **Toit de cage** | 2400 | ferme la cage ; porte l'appentis, ses poteaux et les 6 carrés de culture du périmètre de la tour |

Le plancher Z2100 est porté par la tour du pod et par les pièces des anneaux 8-9 qui s'y accrochent. Il ne dépend pas de L1 : la démolition du chaume ne le fragilise pas.

## 4. Emplacements L1 : mur de chaume + tourelle verticale

| Élément | Position | z template | Rotation |
|---|---|---|---|
| Mur de chaume | sur la ligne D5, centré sur l'emplacement | 2040 | yaw = θ du côté |
| Heavy ou Tek | 10 UU devant le chaume, vers l'extérieur | 2040 | pitch −89,5°, **yaw = θ + 90°**, roll −90° (template 2727) |

| Côté | p0 | p1 | p2 | p3 | p4 |
|---|---|---|---|---|---|
| 0° : chaume | (2 799,0 ; −600) | (2 799,0 ; −300) | (2 799,0 ; 0) | (2 799,0 ; 300) | (2 799,0 ; 600) |
| 0° : tourelle | (2 809,0 ; −600) | (2 809,0 ; −300) | (2 809,0 ; 0) | (2 809,0 ; 300) | (2 809,0 ; 600) |
| 30° : chaume | (2 724,0 ; 879,9) | (2 574,0 ; 1 139,7) | (2 424,0 ; 1 399,5) | (2 274,0 ; 1 659,3) | (2 124,0 ; 1 919,1) |
| autres côtés | rotation de 60°·m du côté 0° ou du côté 30° | | | | |

Les 31 positions occupées sont prises régulièrement autour du cercle, à peu près une sur deux (`donnees/05_matrice_tourelles.csv`, couche L1). C'est la ligne L1 qui complète le cap de 100 (module 05).

**Ordre en jeu**
1. Le plan 6 pose les murs de chaume dans la ligne D5, au niveau L1, avec les cadres L2 au-dessus.
2. Le plan 7 pose les tourelles sur la face extérieure de leur mur de chaume.
3. Rechargez et réglez les tourelles depuis la coursive.
4. **Démolissez les murs de chaume** (liste : `donnees/08_chaume_a_demolir.csv`). Chacun porte un cadre double L2 au-dessus, comme sur la tour 1809 (78 de ses 86 murs de chaume ont un cadre de porte posé dessus). Le cadre reste tenu par ses voisins et par le plancher de galerie Z2100. ⚠ Testez d'abord sur un emplacement en solo : la tourelle et le cadre du dessus doivent rester en place.

## 5. Casquette et appentis (en rampes inclinées)

Les deux partent du haut de D5 (Z2400), sur les mêmes lignes de lames, aux **joints des cadres de D5** (t = ±150, ±450, et les coins). Chaque ligne part de la **tête d'un pilier fin posé dans le joint**, au niveau L2 (Z2100 → 2400) : en jeu, une lame perpendiculaire à un mur ne se pose pas sur son haut (module 08 §3.1). **54 piliers fins de départ**, dans le plan 6, posés avant les cadres L2 voisins.

| Système | Apothème | Z | Rampes | Appuis |
|---|---|---|---|---|
| **Casquette** (porte-à-faux vers l'extérieur) | 2 799 → 3 099 | 2400 → 2100 | **64** | pend d'une lame du pilier fin de départ, comme la lame de rive de la tour 1201 |
| **Appentis** (vers la tour du pod) | 2 799 → 2 499 | 2400 → 2700 | **62** | monte du pilier fin de départ ; **1 poteau de stabilité** (1 pilier fin) sous son bout haut, sur le toit de cage : 60 poteaux (2 lignes n'en ont pas : la Tesla de la tour est juste devant) |
| Casquette r−2 (option `--casquette 2`) | 3 099 → 3 399 | 2100 → 1800 | 0 | plus posable : ses poteaux tomberaient sur les lignes de la pente A, qui partent des mêmes joints |
| **Casquette du trou** (couloir) | bord du trou | 2400 → 2100 | 4 | pend d'une lame du pilier fin de départ, au bout d'un mur de bord |

- Le haut de D5 est un faîtage : ce qui tombe sur l'appentis glisse vers D5, puis sur la casquette et hors de la base.
- Entre le bout haut de l'appentis (2 499) et la tour (2 239), il reste une **poche** de 260 UU sur le toit de cage. Un appentis plus long toucherait la tour. Ce qui tombe du toit du pod ou entre les lames atterrit dans la poche. Elle est couverte à bout portant par l'anneau de tourelles de la tour (Z2400 → 2700, module 05) et par les carrés de culture de Plant X, posés au milieu des côtés E1 (t = 0), entre deux lignes de l'appentis.
- La casquette dépasse le nu de la façade de 300 UU. Ce qui quitte le bout des lames tombe **≈ 190 UU devant les têtes de L1**, puis sur la pente A.
- ⚠ Un joueur qui passe *entre* deux lames de la casquette peut tomber sur une tête de tourelle L1. Il est alors à bout portant des tourelles voisines. Repli : `--casquette 2`.

**Secteurs de tir verticaux** (coupe au milieu d'un côté ; tête supposée à 110 UU devant la façade) :

| Couche | Site min → max |
|---|---|
| L1 (Z1950) | **−51,1° → +89,9°** |
| Anneau D4 de la tour (Z2550) | **−18,4° → +89,9°** : elle tire par-dessus l'appentis et la casquette |

## 6. Contrôles de fin de module

- [ ] Fût : 318 cadres doubles ; fermé par les murs de bord au droit du trou.
- [ ] 3 planchers de galerie (Z1800, 2100, 2400), 5 trappes à Z2100.
- [ ] L1 : 31 murs de chaume et 22 cadres doubles sur D5 ; L2 : 53 cadres doubles.
- [ ] 54 piliers fins de départ dans les joints de L2 ; casquette : 64 rampes ; appentis : 62 rampes et 60 poteaux ; casquette du trou du couloir : 4 rampes.
- [ ] Après le plan 7 : 31 tourelles L1 (+ 4 au bord du trou) ; murs de chaume démolis à la fin, cadres L2 restés en place.
