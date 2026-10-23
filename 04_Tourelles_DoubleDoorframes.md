# Module 04 — Cage à tourelles en double doorframes et casquette anti-accroche

Template : `templates/04_cage_casquette.json`. Il est réparti dans les phases **P2** (fût), **P3** (plancher Z1800), **P5** (cadres L1/L2, planchers 2100/2400, casquette) et **P6** (reprise).
Coordonnées : `donnees/04_cage_casquette.csv`. Sièges de tourelles : `donnees/05_matrice_tourelles.csv`.

## 1. Position : à la rupture de pente

La cage est un **anneau vertical de 2 étages** posé sur la ligne **D5** (apothème 2 799,0 UU, Ø 18,66 fondations). C'est là que la pente A, qui monte depuis la rive, s'interrompt :
- la pente A arrive au pied de la cage (Z ≈ 1720) ;
- la cage monte de Z1800 à Z2400 ;
- la toiture repart au sommet de la cage, d'abord par la **casquette** en porte-à-faux vers l'extérieur, puis par la **reprise** qui rejoint le mur de pod.

```
          reprise ↗ (vers le pod, Z3000)
 Z2400 ───┬──────────────╲  casquette (porte-à-faux 300 UU)
          │ L2  [T]  ▯    ╲  bout Z2100, 350 UU devant les tourelles
 Z2100 ───┤ L1  [T]  ▯     ·   ← fente de tir, 600 UU de haut
 Z1800 ───┴──────────── ▯   ╲
   galerie (anneaux 8-9) │fût ╲ pente A (→ rive, overhang)
                         │D5
```

## 2. Fût (support de la cage)

- Murs sur D5 de Z0 à Z1800 : **6 niveaux × 60 = 360 positions**, dont 358 murs et **2 cadres doubles au sol** (θ 90° et 270°, position 2) pour passer du couloir à l'attique A.
- Le fût porte le plancher de galerie, côté extérieur. Le mur de pod le porte côté intérieur.
- Il sépare aussi le couloir annulaire (entre D4 et D5) de l'attique A (sous la pente) : c'est une couche de cloisonnement supplémentaire contre les raids.

## 3. Galerie : planchers et circulation

Les planchers reprennent **les anneaux 8 et 9 du pavage, en plafonds** : 54 plafonds + 108 plafonds triangles par plancher. Ils s'accrochent donc en vanilla sur le haut du fût et du mur de pod.

| Plancher | Z | Rôle | Particularités |
|---|---|---|---|
| Galerie L1 | 1800 (phase P3) | anneau 8 = coursive ; anneau 9 = rangée de sièges | même niveau que la mezzanine du pod : passage par les 12 cadres doubles du niveau 6 du pod |
| Galerie L2 | 2100 (phase P5) | idem | **3 plafonds à trappe** (anneau 8, côtés θ 30°, 150°, 270°, 1er carré) + échelles depuis L1 |
| Toit de cage | 2400 (phase P5) | ferme la cage ; porte la casquette et la reprise | — |

- La coursive (anneau 8) fait 260 à 300 UU de large, entre le mur de pod et la rangée de sièges.
- On recharge une tourelle depuis la coursive, sans passer devant l'embrasure.

## 4. Double doorframes : 2 étages × 60

| Étage | Z | Pièces | Repère |
|---|---|---|---|
| L1 | 1800 → 2100 | 60 cadres de porte doubles métal | 5 par côté, centrés sur la ligne D5, yaw = θ du côté |
| L2 | 2100 → 2400 | 60 cadres de porte doubles métal | à l'aplomb des L1 |

Exemple, côté 0° : x = 2 799,0, y = −600, −300, 0, 300, 600, z template 2040 (L1) et 2340 (L2).

Le cadre double offre la plus grande ouverture parmi les « murs ajourés » d'ASA. C'est elle qui donne l'arc de tir horizontal (§5). Avec la variante Tek (`BP_DoubleDoorframe_Tek`, utilisée dans le template 1087), seule la classe change dans le JSON.

**Niches vides.** En scénario A (module 05), 44 niches de L2 restent vides ; 54 en scénario B. Fermez-les par des **portes doubles métal** : on peut les rouvrir pour poser une tourelle plus tard. Une niche ouverte et vide est une entrée depuis la fente de tir.

## 5. Sièges de tourelles

Derrière chaque cadre, sur l'anneau 9 :

| Type de côté | Pièce porteuse | Recul du pivot derrière la ligne D5 | Apothème du siège |
|---|---|---|---|
| E0 (0°, 60°…) | plafond carré (300 de profondeur sous la tourelle) | **50 UU** | 2 749,0 |
| E1 (30°, 90°…) | plafond triangle, pointe vers l'intérieur, base de 300 sur D5 | **50 UU** | 2 749,0 |

Le pivot d'une tourelle debout est à **Z + 100** : z template 1900 en L1, 2200 en L2. Son yaw vaut le θ du côté, canon vers l'extérieur.

| Côté | Siège p0 | p1 | p2 | p3 | p4 |
|---|---|---|---|---|---|
| 0° (E0) | (2 749,0 ; −600) | (2 749,0 ; −300) | (2 749,0 ; 0) | (2 749,0 ; 300) | (2 749,0 ; 600) |
| 30° (E1) | (2 680,7 ; 854,9) | (2 530,7 ; 1 114,7) | (2 380,7 ; 1 374,5) | (2 230,7 ; 1 634,3) | (2 080,7 ; 1 894,1) |
| autres | rotation de 60°·m du côté 0° ou du côté 30° | | | | |

**Arc de tir horizontal.**
- Plus la tourelle est près du nu du cadre, plus son arc est large. On l'estime à 2·atan(demi-ouverture / recul) : avec un recul de 50 UU et une ouverture de cadre double d'environ 220 UU, il vaut ≈ 130°.
- Il approche les 180° quand la tourelle est au nu du cadre, comme dans les tours 1087 et 1201 fournies.
- Le recul est réglable : `--recul 0` place la tourelle au nu, `--recul 150` au centre du plafond, plus abritée mais avec un arc d'environ 70°.
- ⚠ Mesurez l'ouverture réelle du cadre double en solo.

**Variante « Straight » (template 2727 fourni).** On peut aussi monter une tourelle latéralement contre un petit mur de chaume (pitch −89,5°, roll −90°), comme dans les tours 1201 et 1809. Cela libère le plancher de la niche, mais n'ajoute aucune tourelle au-delà du cap. On ne s'en sert que pour doubler une niche en scénario C.

## 6. Casquette anti-accroche

Elle est faite de toits en **porte-à-faux devant la cage**. Leur bord haut est sur la ligne D5 à Z2400 ; ils descendent vers l'extérieur.

| Rang | Apothème du bord bas | Z bas → haut | Toits par côté | Total |
|---|---|---|---|---|
| Casquette r−1 (défaut) | 3 099,0 | 2100 → 2400 | 6 | 72 |
| Casquette r−2 (option `--casquette 2`) | 3 399,0 | 1800 → 2100 | 7 | 84 |
| Reprise r0 | 2 799,0 | 2400 → 2700 | 5 | 60 |
| Reprise r1 | 2 499,0 | 2700 → 3000 (s'encastre de 40 UU dans le mur de pod, à Z ≈ 2960) | 5 | 60 |

### Pourquoi rien ne s'accroche aux tourelles

1. Les tourelles sont **derrière la ligne des cadres** (50 UU) et sous un plafond (Z2400). Rien ne tombe sur elles par le haut.
2. La casquette couvre **l'aplomb des tourelles** et le dépasse de 300 UU. Un joueur ou un dino qui glisse de la reprise quitte le bout de la casquette à **350 UU devant l'axe des tourelles** (650 UU avec la casquette 2). Il tombe dans la fente, sur la pente A, environ 680 UU plus bas, puis repart vers l'overhang.
3. La fente entre la casquette et la pente A est **parallèle** : les deux surfaces sont à 45°, séparées de 600 UU à la verticale. Le fond de la fente est un toit : personne ne peut y tenir debout devant une niche.

### Secteurs de tir verticaux (coupe au milieu d'un côté)

Hypothèses : canon à 120 UU au-dessus du plancher, pivot à 50 UU derrière la ligne des cadres. L'ouverture du cadre n'est pas modélisée. Calcul : `secteur_tir()` dans le script.

| Variante | L1 (site min → max) | L2 (site min → max) | Dégagement de chute devant les tourelles |
|---|---|---|---|
| **Casquette 1** (défaut) | **−46,7° → +27,2°** | **−49,9° → −19,0°** | 350 UU |
| Casquette 2 | −46,7° → −10,5° | −49,9° → −32,9° | 650 UU |

- **Limite basse.** Elle vient de la pente A et de l'overhang : un tir plus plongeant toucherait le toit. Le pied de la rive reste donc un angle mort, couvert par les pics et les Tesla.
- **Limite haute.** Elle vient du bout de la casquette : L1 garde un tir **montant** jusqu'à +27,2°, utile contre les volants en approche ; L2 tire uniquement vers le bas.
- **Recommandation.** Gardez la **casquette 1**. La casquette 2 protège mieux contre les très gros dinos (650 UU de dégagement), mais retire tout tir horizontal à L1, qui ne tire plus au-dessus de −10,5°.

## 7. Contrôles de fin de module

- [ ] Fût : 6 niveaux sur D5, 2 portes au sol.
- [ ] 3 planchers de galerie (Z1800, 2100, 2400), 3 trappes à Z2100.
- [ ] 120 cadres doubles alignés (60 par étage), sans décalage à l'aplomb.
- [ ] Casquette : le bout est à 300 UU devant les cadres, partout.
- [ ] De chaque siège, la vue sort par l'ouverture du cadre sans buter sur le bout de la casquette (L1) ni sur la pente A (L1 et L2).
