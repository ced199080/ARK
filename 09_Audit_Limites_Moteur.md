# Module 09 — Audit des limites moteur

Ce module audite la forteresse Ø30 telle que la produit `outils/forteresse.py`, au regard des règles que vous avez fixées :

| Règle | Seuil |
|---|---|
| Structures dans la zone d'influence (≈ 33 fondations de rayon) | 10 500 au plus pour le moteur ; **8 400 au plus pour le bâti**, ce qui garde 2 100 structures (20 %) pour le mobilier, les coffres, les câbles, les tuyaux et les ajouts |
| Tourelles dans la bulle de 33,3 fondations | **100** Heavy, Tek et Plantes X, **toutes utilisées** |
| Portée des plafonds et planchers | **2 cases au plus** jusqu'à un appui qui touche le sol (fondation ou pilier) |
| Hauteur | **70 murs au plus** au-dessus du sol |

Ces quatre règles sont maintenant des contrôles du générateur (`verifier_limites`). Le script refuse d'écrire des plans qui ne les respectent pas.

## 1. Bilan avant / après

| Mesure | Avant (version b286b33) | Après | Règle |
|---|---|---|---|
| Structures du bâti : 8 plans, tourelles, pics, équipements | 4 884 | **4 966** | ≤ 8 400 ✔ |
| Structures au plus fort du chantier (murs de chaume et pile d'ancrage pas encore démolis) | 4 989 | **5 075** | ≤ 8 400 ✔ |
| Marge sous les 8 400, en plus des 2 100 de réserve | 3 516 | **3 434** | — |
| Tourelles comptées par le cap (Heavy + Tek) | 90 (60 H + 30 T) | **100** (65 H + 35 T) | = 100 ✔ |
| Tesla, hors cap | 6 | **10** (tout l'inventaire) | — |
| Plafonds à plus de 2 cases d'un appui au sol | **30** (jusqu'à 4 cases) | **0** | ✔ |
| Hauteur maximale | 17 murs (Z5100) | 17 murs | ≤ 70 ✔ |
| Phases de pose (2 000 entrées au plus) | 1 613 / 1 612 / 1 640 | 1 613 / 1 688 / 1 650 | ✔ |

Les **10 tourelles qui manquaient** au cap correspondaient à :
- 4 Tesla gardées en réserve. Dans la version précédente, on les comptait dans le cap par prudence (scénario B). Votre règle ne compte que les Heavy, les Tek et les Plantes X.
- 10 places du cap de 100 restées libres, parce que les 6 Tesla y occupaient une place.

## 2. Audit du plan existant

### 2.1 Structures

| Poste | Avant | Après |
|---|---|---|
| Fondations et triangles, plateforme verte comprise | 1 028 | 1 028 |
| Murs, cadres doubles | 1 152 | 1 148 (4 murs de rive deviennent des emplacements de Tesla) |
| Piliers | 346 | **418** (+72 : piliers PB jusqu'au sol) |
| Plafonds, trappes | 942 | 942 |
| Rampes inclinées | 892 | 892 |
| Poteaux et poutres fines des rampes | 303 | 303 |
| Escaliers | 6 | 6 |
| **Structure des 8 plans** | **4 669** | **4 737** |
| Tourelles | 96 | 110 |
| Murs de pics, équipements (hors plans) | 74 + 45 | 74 + 45 |
| **Bâti** | **4 884** | **4 966** |
| Murs de chaume et pile d'ancrage (provisoires) | 96 + 9 | 100 + 9 |

### 2.2 Pièces superflues et compartimentage

- **Pas de honeycomb.** La base n'a qu'une épaisseur de mur partout. La seule double ligne est volontaire : le mur de pod (D4) et le fût de cage (D5), séparés par le couloir de 560 UU.
- Comme la base est à 4 966 structures, **rien n'a besoin d'être retiré** pour tenir sous 8 400.
- Si vous voulez de la place en plus, voici les postes les moins utiles à la défense (non retirés) :

| Poste | Structures | Ce qu'on perd |
|---|---|---|
| Colonnade (1 rang de piliers derrière la rive) | 226 | la grille anti-intrusion derrière la rive (module 03 §3) |
| Débord réduit à 1 rang (`--debord 1`) | 188 | 300 UU de dégagement des chutes devant les Heavy de jupe |
| Plateforme verte | 10 | votre projet futur |

### 2.3 Ruptures de support au sol

Le contrôle remonte chaque plafond jusqu'au sol. Il compte comme **appui au sol** :
- une fondation ;
- une colonne continue de murs, de cadres ou de piliers qui descend jusqu'à une fondation.

Ne comptent pas :
- le chaume, puisqu'il est démoli ;
- la plateforme verte, où rien n'est accroché.

| Défaut trouvé | Où | Cause |
|---|---|---|
| **30 plafonds à 3 ou 4 cases d'un appui au sol** | centre de la mezzanine Z1800 (12) et du plancher de toit Z2400 (18), anneaux 0 et 1 | les 12 piliers PB, au centre, partaient de la mezzanine : ils ne touchaient pas le sol |
| Murs posés au-dessus d'un mur de chaume | cadres L2 au-dessus de L1, murs de bord au-dessus des tourelles du trou | après démolition du chaume, ils tiennent par leurs voisins et par le plancher, comme sur la tour 1809. Les plafonds voisins restent à 2 cases au plus d'un appui au sol |

## 3. Modifications

| Modification | Pièces | Pourquoi |
|---|---|---|
| **Piliers PB descendus jusqu'au sol** (Z0 → 2400, au lieu de Z1800 → 2400) | +72 piliers | chaîne de soutien verticale au centre. La mezzanine et le plancher de toit ont maintenant tous leurs plafonds à 2 cases au plus d'un appui au sol (452 à 0 case, 290 à 1, 200 à 2). Les PB passent à 260 UU de la cellule d'escalier |
| **4 Tesla de plus** au milieu des côtés E1 de la rive (θ 30°, 90°, 270°, 330°) | 4 murs → 4 murs de chaume + 4 Tesla | les 10 Tesla de l'inventaire sont posées : 9 au pied de la rive, 1 sur le bord du trou. Elles sont dans l'axe des passages de la colonnade, entre deux lignes de rampes |
| **10 tourelles debout sous le toit** (5 Tek, 5 Heavy), sur le plancher Z2400, en cercle de 1 000 UU de rayon | +10 tourelles | le dessus du centre était un angle mort : L1 ne tire que vers l'extérieur de la cage. Ces tourelles couvrent le toit, le ciel au-dessus du pod et le comble. Les 5 Tek sont à 810 → 2 020 UU du générateur Tek n°2 |
| Règle du cap | — | `tesla_comptee = False` : 100 Heavy et Tek, les Tesla en plus. Les 35 Tek de l'inventaire sont toutes posées ; il reste 15 Heavy en réserve |
| Contrôles ajoutés au générateur | — | structures ≤ 8 400 (y compris au plus fort du chantier) ; exactement 100 tourelles comptées ; hauteur ≤ 70 murs ; plafonds à 2 cases au plus d'un appui au sol |

**Coût** : +1 700 lingots et +476 pâte (module 07 §1 bis). Les tourelles ajoutées viennent de votre inventaire.

## 4. Plan adapté

### 4.1 Découpage par niveau (phases de pose, `templates/phases/`)

| Phase | Hauteur | Contenu | Entrées |
|---|---|---|---|
| 1 | sous Z0 | toutes les fondations, pile d'ancrage ; sous le bord : pieds des poteaux de l'overhang, mur de jupe, poutres et rampes du débord, 26 Heavy de jupe sur leurs murs de chaume | 1 613 |
| 2 | Z0 → 1800 | murs du pod, fût, murs de bord du trou, rive, colonnade, **piliers PA et PB depuis le sol**, escaliers, pente A et overhang, 10 Tesla et 4 Heavy (rive et bord du trou) | 1 688 |
| 3 | Z1800 → 5100 | mezzanine, galeries, 60 tourelles L1, cadres L2, haut des murs et des piliers, plancher de toit, **10 tourelles debout**, toit en rampes et casquettes | 1 650 |

### 4.2 Chaîne de soutien

- **Au sol** : 1 028 fondations, sur 2 paliers au bord.
- **Colonnes maîtresses**, toutes du sol jusqu'au plancher de toit Z2400 :
  - mur de pod D4, 8 niveaux ;
  - 12 colonnes PA (coins de D2) et 12 colonnes PB (coins de D1), 8 piliers chacune ;
  - murs de bord du trou, 8 niveaux dans le pod et le couloir.
- **Fût D5** : du sol à Z1800. Au-dessus, les galeries Z2100 et Z2400 s'appuient sur le mur de pod, 1 à 2 cases plus loin.
- **Rampes** : appuis comme sur les tours (module 08 §3).

### 4.3 Maillage défensif : 100 tourelles comptées + 10 Tesla

| Axe d'approche | Couche | Tourelles | Couverture |
|---|---|---|---|
| Tout autour, de la mer au ciel | L1 sur D5 (Z1950) | 26 H + 27 T | 360° vers l'extérieur, site −51° → +90° ; voit aussi l'attique et les paliers entre les lames |
| Gouffre (trou à l'avant) | TROU-L1 (Z1950) et TROU (Z0 / Z300) | 8 H + 3 T + 1 S | vers le trou, des deux bords |
| Dessous de la plateforme | jupe intérieure | 16 H | vers le piton, sous la plateforme |
| Mer, pied du piton | jupe extérieure | 10 H | −90° → +90° vers la mer |
| Pied de rive, paliers, pics | Tesla de rive | 9 S | palier 1 entier, palier 2 à partir de 4 230 UU |
| **Toit, dessus du centre, comble** | **toit (Z2410)** | **5 H + 5 T** | vers le haut, au-dessus du pod, à travers les lames du toit |
| **Total** | | **65 H + 35 T = 100**, + 10 S | |

- Les tourelles voisines sont à 300 UU les unes des autres sur L1, et à 620 UU sur le toit. Chacune tire depuis une face libre : aucune n'est dans le champ d'une autre.
- Matrice complète : module 05 §6, et `donnees/05_matrice_tourelles.csv`.

## 5. Ce qui reste à confirmer en jeu

| Hypothèse | Si elle est fausse |
|---|---|
| Les Tesla ne comptent pas dans le cap de 100 (votre règle) | avec `tesla_comptee=True` en tête du script, le générateur signale 10 tourelles de trop. Il faut alors en retirer 10, de préférence des Heavy de L1 plutôt que les tourelles du toit |
| Un mur ou un cadre posé en colonne sur une fondation compte comme un appui au sol, au même titre qu'un pilier | si seuls les piliers comptent, il faut des colonnes de piliers sous les galeries de la cage (anneaux 8-9). Je peux les ajouter |
| Les tourelles du toit tirent à travers les lames de rampes (10 UU d'épaisseur, 300 UU d'écart) | les poser plus haut, sur des plafonds au-dessus du faîtage |
| Comptage des structures : une tourelle, un mur de pics et un équipement comptent pour une structure chacun ; les câbles et le mobilier sont dans la réserve de 2 100 | — |
