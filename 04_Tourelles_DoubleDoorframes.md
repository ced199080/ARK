# Module 04 — Cage à tourelles verticales, double doorframes et casquette anti-accroche

Template : `templates/04_cage_casquette.json`, réparti dans les phases :
- **P2** : fût ;
- **P3** : plancher Z1800 ;
- **P5** : planchers 2100/2400, double doorframes L2, casquette.

Au-dessus de la cage, le toit en rampes inclinées couvre le pod et la cage d'un seul tenant (module 02 §8). Il remplace l'ancienne reprise.

Les 60 tourelles de L1 et leurs murs de chaume sont dans `templates/05_tourelles_scenario_B.json` (phase **P7**).
Coordonnées : `donnees/04_cage_casquette.csv`, `donnees/05_matrice_tourelles.csv`.

## 1. Principe : la méthode des tours 1201 / 1809 et du template 2727

Dans les tours fournies, les tourelles ne sont pas posées debout dans les cadres. Elles sont **montées à la verticale** :
1. on remplit un emplacement de mur avec un **mur de chaume** (`Thatch_Wall_Small`), qui sert de gabarit ;
2. on fixe la tourelle sur la **face extérieure** de ce mur de chaume : pivot à 10 UU devant le plan du mur, à mi-hauteur, axe de la tourelle pointé vers l'extérieur ;
3. on **démolit le mur de chaume** en jeu.

La tourelle reste au nu de la façade, dans une ouverture de 300 × 300, avec un champ de tir d'un demi-espace (≈ 180° en azimut, comme une niche de tir). Dans la tour 1809, les étages de double doorframes et les étages de tourelles alternent. La cage reprend cette alternance :

| Étage | Z | Contenu (60 emplacements sur la ligne D5) |
|---|---|---|
| **L1** | 1800 → 2100 | **60 tourelles verticales** (30 Tek + 30 Heavy en alternance, 5 + 5 par part), chacune avec son mur de chaume de pose (phase P7) |
| **L2** | 2100 → 2400 | **60 double doorframes** (phase P5) : à fermer par des portes doubles, ou à garder ouverts pour le tir des joueurs |

```
 Z2400 ──┬─────────────╲  casquette (porte-à-faux 300 UU)
         │ L2 ▯ cadres  ╲  bout Z2100
 Z2100 ──┤ L1 ▮[T]►      ·   ← tourelle verticale au nu de la façade (chaume démoli)
 Z1800 ──┴───────────── ╲
  galerie (anneaux 8-9) │fût ╲ pente A
```

## 2. Fût (support de la cage)

- Murs sur D5 de Z0 à Z1800 : 6 niveaux × 60 = 360 positions, dont 354 murs et 6 cadres doubles au sol (1 par part, θ 30° + 60°·k) vers l'attique A, dans l'axe des passages de la colonnade.
- Le fût porte le plancher Z1800 côté extérieur. Le mur de pod le porte côté intérieur.

## 3. Galerie : planchers et circulation

Les planchers reprennent les anneaux 8 et 9 du pavage, en plafonds : 54 plafonds + 108 plafonds triangles par plancher.

| Plancher | Z | Rôle |
|---|---|---|
| Galerie L1 | 1800 (P3) | coursive de service derrière les tourelles ; accès depuis la mezzanine par les 12 cadres du niveau 6 du pod |
| Galerie L2 | 2100 (P5) | coursive derrière les double doorframes ; 6 plafonds à trappe (1 par part, côtés E1) + échelles |
| Toit de cage | 2400 (P5) | ferme la cage ; prolonge le plancher de toit du pod ; porte la casquette et le premier rang du toit en rampes |

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
1. Posez les murs de chaume des 60 emplacements L1 (vanilla : un mur s'accroche sur l'arête du plancher Z1800).
2. Fixez chaque tourelle sur la face extérieure de son mur de chaume, dans l'ordre du CSV. En Template Hammer, le template P7 pose les deux.
3. Rechargez et réglez les tourelles depuis la coursive.
4. **Démolissez les 60 murs de chaume.** ⚠ Faites-le d'abord sur un emplacement en solo pour vérifier que la tourelle reste en place : c'est le comportement des tours 1201/1809, mais il dépend du jeu.

Après démolition, L1 devient une bande d'ouvertures où chaque tourelle occupe le centre de la sienne. On ne l'atteint que par la fente de tir, dont le fond est un toit à 45° où l'on ne tient pas debout.

## 5. Casquette anti-accroche

| Rang | Apothème du bord bas | Z bas → haut | Toits par côté | Total |
|---|---|---|---|---|
| Casquette r−1 (défaut) | 3 099,0 | 2100 → 2400 | 6 | 72 |
| Casquette r−2 (option `--casquette 2`) | 3 399,0 | 1800 → 2100 | 7 | 84 |
| Toit en rampes (au-dessus) | pivots à partir de 2 949,0 | 2400 → 5150 | lames au pas de 300 | 360 rampes (module 02 §8) |

**Pourquoi rien ne s'accroche aux tourelles**
1. Les tourelles sont sous le toit de cage (Z2400) et sous la casquette. Rien ne tombe sur elles par le haut.
2. La casquette dépasse le nu de la façade de 300 UU. La tête d'une tourelle verticale fait saillie d'environ 110 UU (hypothèse : 100 UU au-delà du pivot). Ce qui quitte le bout de la casquette tombe donc **≈ 190 UU devant les têtes** (≈ 490 UU avec la casquette 2), dans la fente, sur la pente A environ 680 UU plus bas.
3. La fente entre la casquette et la pente A est parallèle (deux toits à 45°, 600 UU d'écart vertical). On n'y tient pas debout.

**Secteurs de tir verticaux de L1** (coupe au milieu d'un côté ; tête supposée à 110 UU devant la façade, à mi-hauteur de L1) :

| Variante | Site min → max | Dégagement devant les têtes |
|---|---|---|
| **Casquette 1** (défaut) | **−49,0° → +38,2°** | ≈ 190 UU |
| Casquette 2 | −49,0° → −17,1° | ≈ 490 UU |

- La limite basse vient de la pente A et de l'overhang. La limite haute vient du bout de la casquette.
- **Recommandation** : casquette 1, pour garder le tir anti-aérien de L1 (+38°). Passez à la casquette 2 seulement si, en test, de très gros dinos largués frôlent les têtes de tourelles.

## 6. Contrôles de fin de module

- [ ] Fût : 6 niveaux sur D5, 2 portes au sol.
- [ ] 3 planchers de galerie (Z1800, 2100, 2400), 6 trappes à Z2100.
- [ ] L2 : 60 double doorframes ; L1 : 60 emplacements libres jusqu'à la phase P7.
- [ ] P7 : 60 murs de chaume + 60 tourelles à 10 UU devant ; murs de chaume démolis à la fin.
- [ ] Casquette : bout à 300 UU devant la façade, partout.
