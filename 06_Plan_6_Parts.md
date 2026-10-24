# Module 06 — Plan complet en 6 parts égales

Ce plan contient sol, structure, colonnade, toitures et tourelles. Les outils de production et de stockage n'en font pas partie : ils figurent au [module 07](07_Bilan_Materiaux.md).

**Principe.** La forteresse est découpée en **6 parts identiques de 60°**. On passe de l'une à la suivante par une rotation de 60° autour du centre. Un seul élément n'entre pas dans ce découpage : le **noyau central** (Coeur Base et son escalier), qui n'a pas de symétrie et se pose une seule fois.

Templates : `templates/parts/`. Coordonnées de la part 1, avec la phase de chaque pièce : `donnees/06_part_1_structure.csv`. La part k s'obtient en tournant la part 1 de 60°·(k − 1).

![Les 6 parts](plans/plan_6_parts.png)

## 1. Découpage

| Part | Secteur θ | Côtés de dodécagone | Coins (piliers PA/PB) |
|---|---|---|---|
| 1 | −14,5° → 45,5° | 0° (E0) et 30° (E1) | 15° et 45° |
| 2 | 45,5° → 105,5° | 60° et 90° | 75° et 105° |
| 3 | 105,5° → 165,5° | 120° et 150° | 135° et 165° |
| 4 | 165,5° → 225,5° | 180° et 210° | 195° et 225° |
| 5 | 225,5° → 285,5° | 240° et 270° | 255° et 285° |
| 6 | 285,5° → 345,5° | 300° et 330° | 315° et 345° |

- Une pièce appartient à la part qui contient son centre.
- Les limites sont décalées de 0,5° par rapport aux arêtes (−15° + 60°·k). Sans ce décalage, les piliers d'angle situés exactement sur une limite seraient attribués au hasard.
- Le script vérifie que **les 6 parts sont identiques à une rotation près** : même classe, même cote, position à moins de 1 UU, pour la structure comme pour les tourelles.

## 2. Contenu d'une part (identique pour les 6)

### Structure : 779 pièces (profil bas, aucun toit incliné)

| Élément | Pièces par part | Détail | Phase |
|---|---|---|---|
| Sol (étoile, anneaux 1-15, dont les 2 paliers de bord) | 192 | 64 fondations + 128 triangles | P1 |
| Mur de pod D4 (4 niveaux) | 32 | 31 murs + 1 cadre double (porte au sol) | P2 |
| Piliers PA (2 colonnes, Z0 → 1200) | 8 | piliers | P2 |
| Poteaux D5 et D6 (4 colonnes, Z0 → 1200) | 16 | piliers | P2 |
| **Colonnade** (40 colonnes de 1 pilier, 1 passage à θ 30°) | 40 | piliers | P2 |
| Rive D7 (2 niveaux, socle de la cage) | 27 | 27 murs. Il reste 1 emplacement libre au niveau 1 pour la Tesla | P2 |
| Galerie L1 Z600 (anneaux 12-13) | 39 | 12 plafonds + 26 triangles + 1 trappe | P3 |
| Overhang (4 rangs, dont 2 dans le vide) | 72 | rampes inclinées | P4 |
| Mur de jupe | 36 | murs | P4 |
| Cage L1 : murs de coin | 4 | murs | P5 |
| Coursive L2 Z900 (anneau 13) | 20 | 6 plafonds + 13 triangles + 1 trappe | P5 |
| Cage L2 | 14 | cadres doubles | P5 |
| Casquette | 18 | rampes inclinées | P5 |
| Plancher de toit Z1200 | 147 | 49 plafonds + 98 triangles | P6 |
| **Toit bas en dents de scie** (2 pans sur 12) | 114 | rampes inclinées | P6 |
| **Total** | **779** | lingots ≈ 18 154 ; pâte ≈ 5 210 | |

Par rapport à la version précédente (827 pièces, 5 555 pâte), une part n'a plus ni fût (60 murs), ni mezzanine (45 plafonds), ni pente A (56 rampes). La galerie de tourelles passe sur la rive, et un seul plancher de toit à Z1200 couvre toute la base.

### Tourelles : 16 par part, chacune avec son mur de chaume

| Couche | Position dans la part | Tourelles |
|---|---|---|
| L1 (cage sur la rive, Z600), côté E0 | 5 emplacements du milieu : T H T H T | 3 Tek + 2 Heavy |
| L1 (cage sur la rive, Z600), côté E1 | 5 emplacements du milieu : H T H T H | 2 Tek + 3 Heavy |
| Jupe, côté E0 | vers la mer (t = −600), vers le piton (t = 0), vers la mer (t = +600) | 3 Heavy |
| Jupe, côté E1 | vers le piton (t = ±600) | 2 Heavy |
| Rive, côté E0 | milieu du côté, niveau 1 (Z300 → 600), sous la cage | 1 Tesla |
| **Total** | | **5 Tek + 10 Heavy + 1 Tesla = 16** (+ 16 murs de chaume) |

**À la pose** :
- Ligne des murs de pics : 14 Metal Spike Walls par part (7 par côté). Ils se posent à la main ; coordonnées dans `donnees/03_ligne_pics.csv`. Leur classe Unreal ne figure dans aucun des templates fournis, c'est pourquoi le template ne les contient pas.
- Démolition des 16 murs de chaume après la pose des tourelles.

## 3. Noyau central (posé une seule fois)

`templates/parts/Noyau_central.json`, 84 pièces :

| Élément | Pièces |
|---|---|
| Coeur Base sans ses fondations ni son coffre (le coffre est compté dans les 20 coffres-forts, module 07) | 35 murs, 3 portes secrètes, 1 escalier, 40 plafonds triangles, 5 plafonds |
Le plancher de toit et le toit bas n'ont pas de pièce centrale propre : le centre du plancher est fait de 6 triangles, et les lames du toit s'arrêtent à 19 UU du centre. Ils sont donc entièrement répartis dans les 6 parts.

## 4. Ce que la symétrie a changé

Six parts égales imposent que tout élément unique soit présent dans chaque part ou dans aucune.

| Élément | Version précédente | Version en 6 parts |
|---|---|---|
| Portes au sol du pod | 4 (θ 90° / 270°) | **6**, 1 par part (côté E1, position 1). Celle de la part 1 est à θ ≈ 26°, face à la porte du Coeur Base |
| Accès à la galerie de tourelles | 2 portes au sol du fût | **6 trappes** dans la galerie L1 (θ ≈ 30° + 60°·k), au-dessus des passages de la colonnade |
| Trappes de la coursive L2 | 3 | **6** (milieu des côtés E0) |
| Passages de la colonnade | 2 (256 colonnes) | **6** (240 colonnes), sous les trappes de la galerie L1 |
| Sas dans la rive | 1 (θ 270°) | **supprimé** : 6 sas feraient 6 brèches. Accès par Tek Teleporter, ou sas percé à la main hors template |
| Bobines Tesla | 10 | **6** (1 par part, au milieu des côtés E0) |
| Tourelles | 55 H + 35 T + 10 S = 100 | **60 H + 30 T + 6 S = 96** |
| Réserve | 25 H | **20 H + 5 T + 4 S** |

**Pourquoi 96 et pas 100.** Avec 35 Tek et 10 Tesla, il est impossible de faire 6 parts identiques qui totalisent 100 : 100 n'est pas divisible par 6, et 6 Tek par part en demanderaient 36. 16 par part donnent 96 ≤ 100.

**Option hors symétrie.** Le cap laisse 4 places. Vous pouvez poser à la main les 4 Tesla restantes, par exemple au milieu des côtés E1 de la rive (θ 90°, 150°, 270°, 330°), avec le même montage sur mur de chaume. Elles ne sont pas dans les templates de part.

## 5. Ordre de pose par parts

| Étape | Template | Remarque |
|---|---|---|
| 1 | `parts/Part_1_structure.json` | contient la pile d'ancrage de 2 demi-piliers en (0 ; 300) (`snapOverrides [0,1]`) |
| 2 à 6 | `parts/Part_2_structure.json` … `Part_6_structure.json` | chacun a 1 demi-pilier qui se pose sur la pile (`snapOverrides [0]`) ; ils sont déjà tournés, aucune rotation à faire |
| 7 | `parts/Noyau_central.json` | Coeur Base et son escalier |
| 8 à 13 | `parts/Part_1_tourelles.json` … `Part_6_tourelles.json` | 16 paires mur de chaume + tourelle par part. 96 tourelles au total, sous le cap |
| 14 | à la main | démolition des 96 murs de chaume, 84 pics, portes doubles, échelles, équipements (module 07), démolition de la pile d'ancrage |

- Dans chaque template de part, les pièces sont **triées par phase** (sol → piliers et murs → galerie → overhang → cage → plancher de toit et toit bas). L'ordre des accroches est donc respecté à l'intérieur de la part.
- ⚠ Une part posée d'un bloc contient des pièces dont l'appui est en partie dans la part voisine : plafonds en limite, rampes près des arêtes et du centre. Si Template Hammer refuse des pièces faute d'appui, utilisez les templates par phase (`templates/phases/P1` à `P7`). Ils contiennent exactement les mêmes pièces, posées couche par couche sur tout le tour.

## 6. Contrôles

- [ ] Après les 6 structures et le noyau : contour D8 complet, 6 portes au sol du pod, 6 passages dans la colonnade sous 6 trappes, plancher de toit Z1200 fermé.
- [ ] Après les 6 templates de tourelles : 60 Heavy, 30 Tek, 6 Tesla. Le compteur du cap ne bloque pas.
- [ ] 96 murs de chaume démolis ; les tourelles restent en place.
