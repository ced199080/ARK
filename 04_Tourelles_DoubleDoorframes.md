# Module 04 — Cage à tourelles verticales, double doorframes et casquette anti-accroche

Template : `templates/plans/Plan_5_cage_et_pente_interieure.json` (module 06), réparti dans les phases :
- **P2** : fût ;
- **P3** : plancher Z1800 ;
- **P5** : planchers 2100/2400, double doorframes L2, casquette en rampes.

Au-dessus de la cage, le toit en rampes inclinées couvre le pod et la cage d'un seul tenant (module 02 §8). Il remplace l'ancienne reprise. La casquette est le premier rang de ce toit.

Les tourelles de L1 et leurs murs de chaume sont dans `templates/plans/Plan_7_tourelles_cage_L1.json` (phase **P7**).
Coordonnées : `donnees/Plan_5_cage_et_pente_interieure.csv`, `donnees/Plan_7_tourelles_cage_L1.csv`, `donnees/05_matrice_tourelles.csv`.

**Le trou** (module 06) coupe la cage à l'avant : 7 des 60 emplacements de la ligne D5 (côté 150° p4, côté 180° en entier, côté 210° p0) sont au-dessus du gouffre. La cage y est fermée par les murs de bord du trou, et les 7 tourelles sont reposées sur ces murs, **au même niveau L1**, face au gouffre (couche TROU-L1).

## 1. Principe : la méthode des tours 1201 / 1809 et du template 2727

Dans les tours fournies, les tourelles ne sont pas posées debout dans les cadres. Elles sont **montées à la verticale** :
1. on remplit un emplacement de mur avec un **mur de chaume** (`Thatch_Wall_Small`), qui sert de gabarit ;
2. on fixe la tourelle sur la **face extérieure** de ce mur de chaume : pivot à 10 UU devant le plan du mur, à mi-hauteur, axe de la tourelle pointé vers l'extérieur ;
3. on **démolit le mur de chaume** en jeu.

La tourelle reste au nu de la façade, dans une ouverture de 300 × 300, avec un champ de tir d'un demi-espace (≈ 180° en azimut, comme une niche de tir). Dans la tour 1809, les étages de double doorframes et les étages de tourelles alternent. La cage reprend cette alternance :

| Étage | Z | Contenu (60 emplacements sur la ligne D5) |
|---|---|---|
| **L1** | 1800 → 2100 | **53 tourelles verticales** sur D5 (27 Tek + 26 Heavy en alternance) + **7 sur les murs de bord du trou** (3 Tek + 4 Heavy), chacune avec son mur de chaume de pose (phase P7) |
| **L2** | 2100 → 2400 | **53 double doorframes** (phase P5) : à fermer par des portes doubles, ou à garder ouverts pour le tir des joueurs |

```
 Z2400 ──┬─────────────╲  casquette en rampes (porte-à-faux 300 UU)
         │ L2 ▯ cadres  ╲  bout Z2100
 Z2100 ──┤ L1 ▮[T]►      ·   ← tourelle verticale au nu de la façade (chaume démoli)
 Z1800 ──┴───────────── ╲
  galerie (anneaux 8-9) │fût ╲ pente A
```

## 2. Fût (support de la cage)

- Murs sur D5 de Z0 à Z1800 : 6 niveaux × 60 = 360 positions, dont 42 au-dessus du trou. Restent **312 murs et 6 cadres doubles au sol** (θ 30° + 60°·k) vers l'attique A, dans l'axe des passages de la colonnade.
- Au droit du trou, la cage est fermée par les murs de bord du couloir (50 murs, 8 niveaux jusqu'à Z2400 entre D4 et D5, module 06 §3).
- Le fût porte le plancher Z1800 côté extérieur. Le mur de pod le porte côté intérieur.

## 3. Galerie : planchers et circulation

Les planchers reprennent les anneaux 8 et 9 du pavage, en plafonds : 54 plafonds + 108 plafonds triangles par plancher sans le trou. Le trou en retire 20 par plancher (18 fondations blanches + 2 de la plateforme verte, au-dessus de laquelle rien n'est posé) : **142 pièces par plancher, 426 en tout**.

| Plancher | Z | Rôle |
|---|---|---|
| Galerie L1 | 1800 (P3) | coursive de service derrière les tourelles ; accès depuis la mezzanine par les 11 cadres du niveau 6 du pod |
| Galerie L2 | 2100 (P5) | coursive derrière les double doorframes ; 5 plafonds à trappe (côtés E1 ; celle du côté 210° tombe dans le trou) + échelles |
| Toit de cage | 2400 (P5) | ferme la cage ; prolonge le plancher de toit du pod ; porte la casquette et le toit en rampes |

Le plancher Z2100 est porté par le mur de pod et par les pièces des anneaux 8-9 qui s'y accrochent. Il ne dépend pas de L1 : la démolition du chaume ne le fragilise pas.

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
| 30° : tourelle | (2 732,7 ; 884,9) | (2 582,7 ; 1 144,7) | (2 432,7 ; 1 404,5) | (2 282,7 ; 1 664,3) | (2 132,7 ; 1 924,1) |
| autres côtés | rotation de 60°·m du côté 0° ou du côté 30° | | | | |

**Ordre en jeu**
1. Posez les murs de chaume des 60 emplacements L1 : 53 sur D5 et 7 sur les murs de bord du trou, au niveau 6 (vanilla : un mur s'accroche sur l'arête du plancher Z1800).
2. Fixez chaque tourelle sur la face extérieure de son mur de chaume, dans l'ordre du CSV. En Template Hammer, le plan 7 pose les deux.
3. Rechargez et réglez les tourelles depuis la coursive.
4. **Démolissez les 60 murs de chaume.** ⚠ Faites-le d'abord sur un emplacement en solo pour vérifier que la tourelle reste en place : c'est le comportement des tours 1201/1809, mais il dépend du jeu.

Après démolition, L1 devient une bande d'ouvertures où chaque tourelle occupe le centre de la sienne. Au-dessus et en dessous de la fente de tir, il n'y a que des rampes inclinées, où l'on ne tient pas debout.

## 5. Casquette anti-accroche (en rampes inclinées)

Comme toutes les pentes de la base, la casquette n'est plus faite de toits mais de **rampes inclinées** (Sloped Railing), en lames au pas de 300 UU (module 02 §8). C'est aussi le premier rang du toit : ses lames continuent celles du toit jusqu'au faîtage.

| Rang | Apothème du bas | Z bas → haut | Lames par côté | Rampes |
|---|---|---|---|---|
| Casquette r−1 (défaut) | 3 099,0 | 2100 → 2400 | 7 | 73 (84 sans trou) |
| Casquette r−2 (option `--casquette 2`) | 3 399,0 | 1800 → 2100 | 7 | 84 sans trou |
| Toit (au-dessus, module 02 §8) | 2 799,0 | 2400 → 5150 | 5 à 1 | 332 (372 sans trou) |
| **Casquette du trou** (module 02 §8.3) | bord du trou | 2100 → 2400 | 1 par mur de bord | 12 |

Au droit du trou, la casquette de D5 n'est pas posée : c'est la **casquette du trou** qui protège les 7 tourelles TROU-L1, avec la même saillie de 300 UU au-dessus du gouffre.

**Pourquoi rien ne s'accroche aux tourelles**
1. On ne tient pas debout sur une lame inclinée : ce qui touche le toit ou la casquette glisse le long des lames vers l'extérieur.
2. La casquette dépasse le nu de la façade de 300 UU. La tête d'une tourelle verticale fait saillie d'environ 110 UU (hypothèse : 100 UU au-delà du pivot). Ce qui quitte le bout des lames tombe donc **≈ 190 UU devant les têtes** (≈ 490 UU avec la casquette 2), puis sur les lames de la pente A environ 680 UU plus bas, qui le font glisser jusqu'à l'overhang.
3. ⚠ Un joueur qui passe *entre* deux lames de la casquette (vide de 300 UU) peut tomber sur une tête de tourelle. Il est alors à bout portant des tourelles voisines. Si ce cas pose problème en test, posez une seconde casquette (`--casquette 2`) : ce qui tombe entre ses lames passe 490 UU devant les têtes.

**Secteurs de tir verticaux de L1** (coupe au milieu d'un côté ; tête supposée à 110 UU devant la façade, à mi-hauteur de L1) :

| Variante | Site min → max | Dégagement devant les têtes |
|---|---|---|
| **Casquette 1** (défaut) | **−50,4° → +89,9°** | ≈ 190 UU |
| Casquette 2 | −50,4° → +89,9° | ≈ 490 UU |

- Les rampes ne masquent ni le ciel ni le sol : le tir de L1 n'est plus limité vers le haut. Vers le bas, la limite vient du haut du mur de jupe. Plus bas encore, le tir voit l'attique A et les paliers entre les lames.
- **Recommandation** : casquette 1. Passez à la casquette 2 si, en test, des joueurs tombent entre les lames sur les têtes de tourelles.

## 6. Contrôles de fin de module

- [ ] Fût : 6 niveaux sur D5, 6 portes au sol ; fermé par les murs de bord au droit du trou.
- [ ] 3 planchers de galerie (Z1800, 2100, 2400), 5 trappes à Z2100.
- [ ] L2 : 53 double doorframes ; L1 : 53 emplacements libres sur D5 et 7 au niveau 6 des murs de bord, jusqu'à la phase P7.
- [ ] P7 (plan 7) : 60 murs de chaume + 60 tourelles à 10 UU devant ; murs de chaume démolis à la fin.
- [ ] Casquette : 73 rampes, bout à 300 UU devant la façade, partout hors du trou ; casquette du trou : 12 rampes.
