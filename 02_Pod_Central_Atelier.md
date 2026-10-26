# Module 02 — Tour du pod (Ø15, hall, toit D4 → centre)

Le pod est maintenant une **tour en murs pleins**. Son toit se pose sur le haut de la tour, calé sur un **mur de D4 de référence**. Vous pouvez donc faire varier la hauteur de la tour, par exemple pour la reproduction, comme sur une tour : le toit suit.

Templates (`templates/plans/`, module 06) :

| Plan | Contenu | Calage |
|---|---|---|
| `Plan_05_tour_du_pod_D4.json` | tour D4 jusqu'à Z2700, murs de bord du trou du pod, piliers PA et PB, colonne d'escaliers, mezzanine Z1800, cages du noyau (générateurs Tek, boîtes de munitions), murs de chaume de l'anneau de tourelles D4 | pile d'ancrage |
| `Option_rehausse_pod_+1_niveau.json` | un niveau de plus pour la tour, à poser autant de fois que voulu | mur de référence **A** |
| `Plan_09_toiture_pleine_D4-centre.json` | couronne de murs pleins, piliers PA/PB, plancher de toit : toit plat fermé | mur de référence **A** |
| `Plan_10_toit_en_rampes_D4-centre.json` | toit en rampes inclinées de D4 au centre, poteaux de piliers fins sous les jonctions, casquette du trou | mur de référence **C** |
| `Plan_11_tourelles_dessus.json` | tourelles, Tesla et carrés de culture sur le plancher de toit (module 05) | mur de référence **B** |

Le Coeur Base n'est plus dans le projet : le centre du hall est libre. Coordonnées : `donnees/Plan_05_*.csv`, `Plan_09_*.csv`, `Plan_10_*.csv`, `Plan_11_*.csv`. Plans : `plans/plan_pod.png`, `plans/plan_rampes.png`, `plans/coupe_radiale.png`.

![Plan du pod](plans/plan_pod.png)

## 1. Volumes

| Élément | Cotes | Remarque |
|---|---|---|
| Emprise du pod | Dodécagone **D4** : apothème 2 239,2 UU, Ø 14,93 fondations entre plats | c'est l'étoile existante (anneaux 1 à 7) |
| **Trou** | à l'avant (θ 180°), dès x ≈ −1 120 | le pod est fermé sur le gouffre par des murs de bord pleins de toute la hauteur (§5) |
| **Colonne d'escaliers** | (129,9 ; −75), de Z0 à Z1800 | 6 escaliers empilés, à 186 UU du pilier de référence |
| **Hall d'atelier** | Z0 → Z1800 : **6 murs pleins de hauteur libre** | aucun plancher intermédiaire |
| Mezzanine / étage technique | Z1800 → Z2400 (2 murs) | même niveau que la galerie de tourelles |
| **Anneau de tourelles D4** | Z2400 → Z2700 (niveau 8) | au-dessus du toit de cage : les tourelles de la tour tirent par-dessus l'appentis (module 05) |
| **Haut de la tour** | **Z2700** par défaut (9 murs) | + 1 niveau par rehausse |
| **Couronne** | Z2700 → Z3000 | 1 niveau de murs pleins, posé avec la toiture pleine |
| **Plancher de toit** | **Z3000**, sur tout le pod | toit plat fermé (toiture pleine) |
| **Toit en rampes** | Z3000 → Z5100, de D4 au centre | comme le toit des tours 1201 / 1809 ; aucun toit incliné |

## 2. Colonne d'escaliers

La colonne d'escaliers garde la place de l'ancien escalier du Coeur Base : une cellule de 300 × 300 centrée en (129,9 ; −75), axes tournés de −30°.

| Marche | Z | z template |
|---|---|---|
| 1 | 0 → 300 | 240 |
| 2 à 6 | 300 → 1800 | 540 · 840 · 1140 · 1440 · 1740 |

- Même x, y et yaw (−120°) pour les 6 escaliers.
- **Trémie de la mezzanine** : le script retire les 6 pièces du plancher Z1800 traversées par la cellule d'escalier. Ce sont 4 triangles du centre et 2 carrés de l'anneau 1 (θ 0° et θ 300°), tracés en violet sur le plan. On sort de l'escalier directement sur la mezzanine, puis on gagne la galerie de tourelles par les 11 cadres du niveau 6 du mur de pod.
- **Accès au toit** : une trappe dans le plancher de toit, sur le carré de l'anneau 1 à θ 0°, en (409,8 ; 0). Posez une échelle de 4 niveaux depuis la mezzanine, plus 1 par rehausse.
- **Pilier de référence.** La pile d'ancrage est en (0 ; 300), à 186 UU de la cellule d'escalier. Démolissez-la à la fin.

## 3. Mur de pod (D4) : une tour en murs pleins

- **48 positions par niveau** (12 côtés × 4). Le trou en coupe 6 (côtés 150°, 180° et 210°) : il en reste **42 par niveau**.
- Le mur de pod est la seule enceinte en **murs pleins** de la base. Partout ailleurs, les murs sont des cadres de porte doubles (modules 03 et 04). Seules ses ouvertures sont des cadres doubles :

| Niveau | Z | Contenu |
|---|---|---|
| 0 | 0 → 300 | **6 cadres doubles** (côtés E1, position 1 : θ ≈ 26°, 86°, 146°, 206°, 266°, 326°) : hall ↔ couloir annulaire |
| 1 à 5 | 300 → 1800 | murs pleins |
| **6** | 1800 → 2100 | **11 cadres doubles** (position 1 de chaque côté, sauf celui du côté 180°, dans le trou) : mezzanine ↔ galerie de tourelles |
| 7 | 2100 → 2400 | murs pleins ; le toit de cage Z2400 s'y accroche |
| **8** | 2400 → 2700 | **anneau de tourelles D4** : 13 murs de chaume (11 tourelles + 2 Tesla), 29 murs pleins |
| 9 (couronne) | 2700 → 3000 | plan 9 ; murs B et C : plans 11 et 10 |

Dans le plan 5 : **348 murs + 17 cadres doubles** et 13 murs de chaume.

## 4. Système porteur à piliers intérieurs

| Couronne | Position | Hauteur | Pièces | Rôle |
|---|---|---|---|---|
| **PA** | 12 coins de D2 : rayon 1 159,1, θ = 15° + 30°·k | Z0 → 2700 (9 piliers), + 1 avec la couronne, + 1 par rehausse | 108 + 12 | portent la mezzanine et le plancher de toit |
| **PB** | 12 coins de D1 : rayon 579,6, θ = 15° + 30°·k | idem | 108 + 12 | portent le centre de la mezzanine et du plancher de toit ; ils passent à 260 UU de la cellule d'escalier |

- Aucun plafond n'est à plus de 2 cases d'un appui relié au sol (module 09) : les colonnes PA et PB descendent jusqu'au sol et montent jusqu'au plancher de toit.
- Les 2 piliers PA à θ 165° et 195° sont aux sommets du bord du trou, en (−1 119,6 ; ±300) : ils restent en place et portent les murs de bord.

## 5. Bord du trou dans le pod

Le trou entame le pod sur les anneaux 4 à 7 (27 pièces de l'étoile). Le pod est fermé sur le gouffre par des **murs de bord pleins** posés sur les arêtes entre les fondations gardées et le trou :

| Élément | Valeur |
|---|---|
| Arêtes de bord dans le pod | 10, de x = −1 119,6 jusqu'à D4 |
| Hauteur | **9 murs** (Z0 → 2700, plan 5), + 1 dans la couronne (plan 9), + 1 par rehausse |
| Murs | **87** dans le plan 5, plus 3 murs de chaume de tourelles (2 TROU-L1 au niveau 6, 1 TROU-D4 au niveau 8) ; 10 dans la couronne |
| Mezzanine et plancher de toit | s'arrêtent sur les murs de bord |
| Toit | la **casquette du trou** prolonge le toit au-dessus du gouffre (§8.3) |

## 6. Gabarits de placement des machines (hall Z0 → 1800)

Ce sont des zones de réservation, pas les cotes exactes des maillages. Elles commencent à 1 200 UU du centre, au-delà des piliers PA.

| Machine | Branche θ | Centre (x ; y) | Gabarit | Hauteur réservée | Énergie / carburant |
|---|---|---|---|---|---|
| **Réplicateur Tek** | 0° | (1 650 ; 0) | 3 × 2 fondations | 3 murs | à vérifier |
| **Forge à vapeur** (Steam Forge) | 120° | (−825 ; 1 428,9) | 3 × 3 | 3 murs | élément (forge alimentée à l'élément) |
| *le trou* | 180° | — | — | — | — |
| **Labo de fortune** (Makeshift Megalab) | 240° | (−825 ; −1 428,9) | 2 × 2 | 2 murs | à vérifier |
| **9 stockages dédiés Tek** | 300° | (800 ; −1 385,6) | 5 × 2, en 2 rangées (4 + 5) | 2 murs | — |
| *noyau* | 60° à 240° | anneau 1 | 4 cages de 1 × 1 | 2 murs + plafond | §6.1 |

Sur la mezzanine (Z1800) se trouvent **20 coffres-forts et 11 stockages dédiés** en alternance contre la face intérieure du mur de pod. Le trou supprime 5 des 36 emplacements ; les 9 stockages qui n'y trouvent plus de place sont dans le hall. Positions exactes : `donnees/07_equipements.csv` et module 07.

**Allées** : coffres-forts (2 murs de haut) et stockages dédiés ont tous une face libre pour l'accès. Dans le hall, la rangée extérieure des stockages est tournée vers le mur de pod, avec une **allée de 329 UU (plus d'une fondation)** entre les deux ; la rangée intérieure est tournée vers le hall. Le générateur refuse une allée de moins d'une fondation.

### 6.1 Noyau : générateurs et boîtes de munitions en cage

Au centre de la base, sur 4 carrés de l'anneau 1 autour de la colonne d'escaliers (plan 5) :

| θ | Centre (x ; y) | Contenu |
|---|---|---|
| 180° | (−409,8 ; 0) | **Générateur Tek n°1 (principal)** |
| 240° | (−204,9 ; −354,9) | **Générateur Tek n°2 (secours)** |
| 60° | (204,9 ; 354,9) | **Boîte de munitions n°1** |
| 120° | (−204,9 ; 354,9) | **Boîte de munitions n°2** |

- Chaque équipement est **posé sur une fondation** de l'étoile centrale, la plus éloignée de tous les murs extérieurs.
- **Cage** : 4 côtés en murs métal, 2 murs de haut (Z0 → 600), plafond métal à Z600 ; au niveau 0, le côté tourné vers le hall est un cadre de porte double (porte à poser). Les piliers PB sont aux coins extérieurs des cages. 4 cages : 28 murs, 4 cadres doubles, 4 plafonds.
- Le générateur de secours a la même portée que le principal (module 05 §8) : si l'un tombe, l'autre alimente encore les 26 Tek.
- Les carrés θ 0° et 300° restent libres : la colonne d'escaliers les touche. Ses deux bouts (côtés 60° et 240°) longent une cage sur une moitié de leur largeur (couloir de 110 UU) et donnent sur un triangle libre de l'étoile sur l'autre moitié : l'escalier reste accessible.

Pour la reproduction, rehaussez la tour (§8.2) : le hall garde ses 6 murs libres sous la mezzanine. Pour un hall plus haut encore, retirez la mezzanine. Les colonnes PA et PB portent seules le plancher de toit.

## 7. Mezzanine Z1800

Elle reprend le centre et les anneaux 1 à 7 en plafonds, **moins la trémie de l'escalier et les 27 pièces du trou** : 85 plafonds + 170 plafonds triangles.

## 8. Haut de la tour : calé sur un mur de D4

### 8.1 Murs de référence

Les plans du haut de la tour ne se calent pas sur la pile d'ancrage : leur hauteur dépend de celle de la tour. Chacun a pour pièce de référence (`snapOverrides [0]`) **un mur de D4** que vous snappez sur le haut d'un mur de la tour, comme on pose un mur sur un mur. Les 3 murs de référence sont sur le côté θ 90°, celui qui fait face à la pile d'ancrage :

| Mur | Index | Position (x ; y) | Plans qui l'utilisent | Remarque |
|---|---|---|---|---|
| **A** | 1 | (+150 ; 2 239,2) | toiture pleine (plan 9), rehausse | juste au-dessus de la porte du hall du côté θ 90° |
| **B** | 2 | (−150 ; 2 239,2) | tourelles du dessus (plan 11) | à droite de A, vu de l'extérieur |
| **C** | 3 | (−450 ; 2 239,2) | toit en rampes (plan 10) | à droite de B, vu de l'extérieur |

- Chaque mur de référence fait partie de la couronne : ce n'est pas une pièce provisoire. La toiture pleine laisse vides les places B et C ; les plans 11 et 10 les remplissent avec leur propre mur de référence.
- **Pose** : visez le haut du mur de la tour à la même place (A, B ou C), au dernier niveau posé. Vérifiez dans l'aperçu que le plancher tombe à l'intérieur de la tour, et non à l'extérieur : sinon, tournez de 180°.

### 8.2 Rehausse (option)

`Option_rehausse_pod_+1_niveau.json` ajoute **1 niveau** à la tour : 42 murs de D4 et 10 murs de bord du trou, tous pleins, plus 24 piliers PA/PB. C'est 76 pièces, soit 1 900 lingots et 532 pâte.

1. Posez la tour (plan 5) et ses tourelles (plan 8).
2. Posez la rehausse autant de fois que vous voulez de niveaux. Calez-la sur le mur A du dernier niveau.
3. Posez ensuite la toiture pleine, le toit en rampes et les tourelles du dessus, sur le haut de la dernière rehausse.

L'anneau de tourelles D4 reste au niveau 8, juste au-dessus du toit de cage, là où il couvre l'appentis. Le générateur refait tous ses contrôles sur la tour rehaussée d'un niveau : aucune collision, appuis et ordre de pose bons.

### 8.3 Toiture pleine (plan 9)

| Élément | Pièces |
|---|---|
| Couronne : murs pleins de D4 (dont le mur de référence A, sans B ni C) | 40 |
| Couronne : murs de bord du trou du pod | 10 |
| Piliers PA et PB, 1 niveau | 24 |
| Plancher de toit : centre et anneaux 1 à 7, sans le trou | 86 plafonds + 174 triangles + 1 trappe |
| **Total** | **335 entrées**, 8 027 lingots, 2 258 pâte |

Elle ferme le pod seule : c'est un **toit plat**, sur lequel se posent les tourelles du dessus. Le toit en rampes se pose dessus.

### 8.4 Toit en rampes (plan 10), comme les tours 1201 / 1809

**Aucun toit incliné dans toute la base.** Sur un toit à 45°, on tient debout et rien ne glisse. Le toit du pod est donc un **toit en rampes inclinées** (`StructureBP_Railing_Sloped_Metal`, la pièce des tours 1201 et 1809), posé sur la toiture pleine :
- **lignes de lames** au pas de 300 UU, au milieu de chaque mur de la couronne (t = ±150, ±450 le long de chaque côté) ;
- chaque rampe monte de 300 UU sur 300 UU vers le centre. Pivot au milieu de la rampe, z template = Z du bas + 290, **yaw = θ du côté − 90°** (tour 1201) ;
- chaque ligne part du haut de la couronne, au bord du plancher de toit ;
- **poteaux de piliers fins sous les jonctions de lames**, debout sur le plancher de toit, sous les jonctions 1, 4 et 7 (et sous le bout haut de chaque ligne). Si la couronne ou un poteau est détruit, chaque ligne reste dans les règles des tours : au plus 7 lames entre deux appuis, 6 lames libres, 1 lame pendue (module 08 §3) ;
- **arêtes** : deux lames de côtés voisins qui se croiseraient ne peuvent pas être posées toutes les deux. Le script retire la plus haute, en bout de ligne, et chaque ligne reste continue depuis la couronne ;
- **au-dessus du trou, aucune lame** : une ligne s'arrête à sa première rampe au-dessus du gouffre.

| Rang | Z du bas | Rampes posées |
|---|---|---|
| r0 | 3000 | 42 |
| r1 | 3300 | 32 |
| r2 | 3600 | 32 |
| r3 | 3900 | 22 |
| r4 | 4200 | 22 |
| r5 | 4500 | 12 |
| r6 | 4800 | 8 |
| **Total** | faîtage Z5100 | **170** |

**Poteaux du toit** : **96 poteaux, 288 piliers fins**, tous debout sur le plancher de toit. Il y en a 42 d'un pilier (jonction 1), 42 de 3 à 5 piliers (jonctions 3 à 5) et 12 de 6 à 7 piliers (faîtage).

**On ne tient pas debout sur une lame** : un dino largué n'y trouve aucune surface et glisse vers l'extérieur. Ce qui passe entre deux lames tombe sur le plancher de toit, où le couvrent les tourelles du dessus.

### 8.5 Casquette du trou

| Élément | Valeur |
|---|---|
| Couloir (plan 6) | 4 lames en haut des murs de bord du couloir, de Z2400 à Z2100, au-dessus du gouffre |
| Pod (plan 10) | 8 lames en haut des murs de bord de la couronne, de Z3000 à Z2700 |
| Lame | 1 rampe par mur, pivot 150 UU devant le mur côté gouffre, **yaw = sens du gouffre − 90°** (elle monte vers le mur) ; les lames des angles rentrants, qui croiseraient un mur ou une lame voisine, ne sont pas posées |
| Rôle | comme la casquette de D5 : ce qui glisse quitte le bord devant les tourelles reposées face au gouffre et tombe dans le trou |

- Coût : une rampe vaut environ **12 lingots + 3 pâte** ; un pilier fin environ 13 + 4. ⚠ Ce sont des estimations : rambarde métal (Metal Railing) et demi-pilier métal.
- ⚠ À valider en solo :
  - le décalage de la rampe (+290 en z template) vient des tours 1201 et 1809. Si les rampes apparaissent trop haut ou trop bas, corrigez `+ 200` dans `pente()` et `bouts_lame()` et régénérez ;
  - la pose d'un plan calé sur un mur : le mur de référence doit se snapper sur le haut du mur de la tour (module 08 §6).

## 9. Contrôles de fin de module

- [ ] 6 escaliers empilés de Z0 à Z1800 ; la trémie de la mezzanine est ouverte au-dessus.
- [ ] Tour en murs pleins : 6 cadres doubles au sol, 11 à Z1800, 13 murs de chaume au niveau 8.
- [ ] Murs de bord du trou du pod pleins, du sol à la couronne, sans jour.
- [ ] 24 colonnes de piliers PA/PB, du sol au plancher de toit.
- [ ] Noyau : 4 cages (2 murs + plafond) ; 2 générateurs Tek et 2 boîtes de munitions posés sur leur fondation, portes doubles fermées.
- [ ] Toiture pleine posée sur le mur de référence A : plancher fermé, places B et C vides jusqu'aux plans 11 et 10.
- [ ] Toit : 170 rampes, 96 poteaux (288 piliers fins) ; casquette du trou : 8 lames sur la couronne. Aucun toit incliné.
