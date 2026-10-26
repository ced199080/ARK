# Module 09 — Audit des limites moteur

Ce module audite la forteresse Ø30 telle que la produit `outils/forteresse.py` (11 plans par zone), au regard des règles que vous avez fixées :

| Règle | Seuil |
|---|---|
| Structures dans la zone d'influence (≈ 33 fondations de rayon) | 10 500 au plus pour le moteur ; **8 400 au plus pour le bâti**, ce qui garde 2 100 structures (20 %) pour le mobilier, les coffres, les câbles, les tuyaux et les ajouts |
| Tourelles dans la bulle de 33,3 fondations | **100**, **Tesla et Plant Species X comprises**, toutes utilisées |
| Portée des plafonds et planchers | **2 cases au plus** jusqu'à un appui qui touche le sol (fondation ou pilier) |
| Hauteur | **70 murs au plus** au-dessus du sol |

Ces quatre règles sont des contrôles du générateur (`verifier_limites`). Le script refuse d'écrire des plans qui ne les respectent pas.

## 1. Bilan

| Mesure | Version précédente | **Maintenant** | Règle |
|---|---|---|---|
| Structures du bâti : plans (colonnade comprise), tourelles, carrés de culture, pics, équipements | 5 940 | **5 691** | ≤ 8 400 ✔ |
| Structures au plus fort du chantier (murs de chaume et pile d'ancrage pas encore démolis) | 6 028 | **5 779** | ≤ 8 400 ✔ |
| Marge sous les 8 400, en plus des 2 100 de réserve | 2 460 | **2 709** | — |
| Places du cap (Tesla et Plant X comprises) | 100 (52 H + 23 T + 10 S + 15 X) | **100** (49 H + 26 T + 10 S + 15 X) | = 100 ✔ |
| Tourelles sous le niveau des fondations centrales (Z0) | 16 | **0** | 0 ✔ |
| Écart minimal entre deux tourelles | — | **295 UU** | ≥ 1 mur ✔ |
| Plafonds à plus de 2 cases d'un appui au sol | 0 | **0** | ✔ |
| Hauteur maximale | 17 murs (Z5100) | **17 murs** (Z5100) ; + 1 par rehausse de la tour | ≤ 70 ✔ |
| Plans (2 000 entrées au plus) | 11 plans | **11 plans** de 11 à 1 046 entrées | ✔ |

## 2. Audit du plan

### 2.1 Structures

| Poste | Structures |
|---|---|
| Fondations et triangles, plateforme verte comprise | 1 028 |
| Murs pleins (tour du pod, cages du noyau) | 515 |
| Cadres de porte doubles | 681 |
| Piliers PA/PB (option colonnade : +226) | 240 |
| Plafonds, trappes | 946 |
| Rampes inclinées | 758 |
| Piliers fins, demi-piliers fins (appuis des rampes) | 1 070 |
| Escaliers | 6 |
| **Structure des plans, sans la colonnade** | **5 244** |
| Colonnade (option) | 226 |
| Tourelles (49 H, 26 T, 10 S) | 85 |
| Carrés de culture (Plant X) | 15 |
| Murs de pics, équipements (hors plans, boîtes de munitions comprises) | 74 + 47 |
| **Bâti** | **5 691** |
| Murs de chaume et pile d'ancrage (provisoires) | 79 + 9 |

### 2.2 Ce qui pèse

- Les **poteaux de stabilité** (pente A, appentis, toit) font à eux seuls 896 piliers fins. Avec `--appuis tours`, sans eux, le bâti tombe à 4 795 structures.
- La **colonnade** (226) est en option : sans elle, le bâti est à 5 465.
- Chaque **rehausse** de la tour ajoute 76 structures. La marge de 2 709 en permet environ 35, bien avant la limite de 70 murs de haut.

### 2.3 Appuis au sol

Le contrôle remonte chaque plafond jusqu'au sol, sur la base finie. Il compte comme **appui au sol** :
- une fondation ;
- une colonne continue de murs, de cadres ou de piliers qui descend jusqu'à une fondation.

Ne comptent pas : le chaume, puisqu'il est démoli, et la plateforme verte, où rien n'est accroché.

| Plafonds | À 0 case d'un appui au sol | À 1 case | À 2 cases |
|---|---|---|---|
| 946 | 489 | 331 | 126 |

- Mezzanine et plancher de toit : les colonnes PA et PB et la tour du pod les portent du sol au toit, à toute hauteur.
- Galeries : la tour du pod d'un côté, le fût D5 de l'autre.
- Plafonds des cages du noyau : sur leurs murs, qui sont sur les fondations de l'anneau 1.

## 3. Plan adapté

### 3.1 Découpage par zone (`templates/plans/`)

| Plan | Zone | Entrées |
|---|---|---|
| 1 | sol complet | 1 030 |
| 2 | colonnade (option) | 227 |
| 3 | bord D8 → D7 | 660 |
| 4 | D7 → D5 | 808 |
| 5 | tour du pod | 982 |
| 6 | D5 → D4 | 1 046 |
| 7 | défense D8 → D4 | 71 |
| 8 | défense du périmètre du pod | 21 |
| 9 | toiture pleine D4 → centre (mur A) | 335 |
| 10 | toit en rampes D4 → centre (mur C) | 467 |
| 11 | défense du dessus (mur B) | 11 |
| option | rehausse de la tour, +1 niveau (mur A) | 76 |

### 3.2 Chaîne de soutien

- **Au sol** : 1 028 fondations, sur 2 paliers au bord. Rien n'est posé sous les fondations : la jupe est sur le palier 2.
- **Colonnes maîtresses**, toutes du sol au plancher de toit :
  - tour du pod D4, 9 niveaux + couronne ;
  - 12 colonnes PA (coins de D2) et 12 colonnes PB (coins de D1) ;
  - murs de bord du trou du pod.
- **Fût D5** : du sol à Z2400, en cadres doubles.
- **Rampes** : appuis comme sur les tours, plus les poteaux de stabilité (module 08 §3).

### 3.3 Maillage défensif : 100 places

| Axe d'approche | Couche | Places |
|---|---|---|
| Pied de rive, paliers, pics, mer | rive (2 Heavy par côté aux niveaux 0 et 1, Tesla sur les côtés E0) | 22 H + 5 S |
| Tout autour, de la mer au ciel | L1 sur D5 (Z1950) | 15 H + 16 T |
| Gouffre (trou à l'avant) | murs de bord (Z0 à Z2400) | 4 H + 3 T + 1 S |
| Attique, sous la pente A | Plant X | 5 X |
| Toit de cage, poche au pied de la tour, ciel | anneau D4 de la tour (Z2550) | 6 H + 5 T + 2 S |
| Poche au pied de la tour | Plant X | 6 X |
| Toit du pod, ciel au-dessus du centre | dessus (Z3000, debout) | 2 H + 2 T + 2 S + 4 X |
| **Total** | | **49 H + 26 T + 10 S + 15 X = 100** |

Couverture par zone d'approche : module 05 §7. Chaque direction au-dessus de la plateforme est vue par au moins une Heavy ou une Tek, les paliers par 2 ; la poche au pied de la tour a en plus des Tesla et des Plant X. **Le dessous de la plateforme n'est plus couvert** : c'est le prix de la règle « aucune tourelle sous Z0 ».

## 4. Ce qui reste à confirmer en jeu

| Hypothèse | Si elle est fausse |
|---|---|
| Un mur ou un cadre posé en colonne sur une fondation compte comme un appui au sol, au même titre qu'un pilier | il faudrait des colonnes de piliers sous les galeries (anneaux 8-9) |
| Les tourelles du dessus et de la tour tirent à travers les lames de rampes (10 UU d'épaisseur, 300 UU d'écart) | poser les tourelles du dessus plus haut, sur des plafonds au-dessus du faîtage |
| Plant Species X compte dans le cap (wiki) | 15 places à rendre à L1 : passer `plante_x_comptee` à False et régénérer |
| La boîte de munitions compte pour une structure, pas pour une tourelle | — |
| Comptage des structures : une tourelle, un carré de culture, un mur de pics et un équipement comptent pour une structure chacun ; les câbles, tuyaux et le mobilier sont dans la réserve de 2 100 | — |
