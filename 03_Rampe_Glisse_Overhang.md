# Module 03 — Rive, rampes de glisse, overhang dans le vide (et colonnade en option)

Templates (`templates/plans/`, module 06) :

| Plan | Contenu |
|---|---|
| `Plan_03_bord_D8-D7.json` | mur de rive D7 et mur de jupe D8 en **cadres doubles**, **piliers fins de départ** dans leurs joints, overhang et débord en rampes, poteaux sur les paliers, murs de chaume des tourelles de la rive |
| `Plan_04_D7-D5_pente_A.json` | pente A en rampes, de la rive vers la cage, avec ses **poteaux de stabilité** ; murs de bord du trou entre D5 et D7, en cadres doubles |
| `Plan_02_colonnade_option.json` | **option** : colonnade circulaire sous la pente A. Les poteaux de stabilité la remplacent |

**Murs : cadres de porte doubles** (`BP_DoubleDoorframe_Metal`, la pièce des tours 1201 et 1809), partout sauf la tour du pod.

**Chaque ligne de rampes part de la tête d'un pilier fin posé dans le joint de deux cadres.** En jeu, une lame perpendiculaire à un mur ne se pose pas sur son haut : c'est pour cela qu'aucune rampe ne se posait dans le secteur d'essai. Sur la tour 1809, les 52 départs de ligne sur un mur ont tous ce pilier fin (module 08 §3.1).

**Aucun toit incliné.** Sur un toit à 45°, on tient debout et rien ne glisse. Toutes les pentes sont donc faites de **rampes inclinées** (Sloped Railing), en lignes de lames au pas de 300 UU comme sur les tours 1201 et 1809 (module 02 §8). **Chaque ligne de lames part d'un appui. Elle monte librement de 6 lames au plus, ou pend d'une seule lame**, comme sur les tours (module 08 §3). Les lignes qui montent reçoivent en plus des **poteaux de stabilité** : elles tiennent encore si un appui est détruit.

**Le trou** (module 06) coupe la rive, la colonnade, la pente A, l'overhang, la jupe et les pics à l'avant, entre θ ≈ 155° et 205°. Les chiffres ci-dessous sont ceux de la base avec le trou.

Les tourelles de la rive se posent avec le plan 7 (module 05). Leurs murs de chaume sont dans le plan 3, à leur place dans la colonne de murs.

**Aucune tourelle sous le niveau des fondations centrales (Z0).** Les 16 Heavy de la jupe, qui pendaient sous la plateforme, sont supprimées. Leurs places du cap vont à une 2e Heavy de rive par côté, au niveau 0 (Z0 → 300), et à L1.

Coordonnées : `donnees/Plan_03_*.csv`, `donnees/Plan_04_*.csv`, `donnees/03_colonnade.csv`, `donnees/03_ligne_pics.csv`. Coupe (θ 0°, hors trou) : `plans/coupe_radiale.png`. Rampes : `plans/plan_rampes.png`.

![Coupe radiale](plans/coupe_radiale.png)

## 1. Ordre des couches, du pod vers le vide

| Couche | Rayon / apothème (UU) | Rôle |
|---|---|---|
| Tour du pod (mur D4) | 2 239 | module 02 |
| Couloir, fût de cage D5 | 2 239 → 2 799 | module 04 |
| Attique A, sous la pente A, poteaux de stabilité | 2 799 → 3 919 | §3 et §4 |
| Colonnade (option) | 3 600 (cercle) | §3 |
| Mur de rive D7 | 3 919 | §2 |
| Palier 1 (Z −150) | 3 919 → 4 179 | module 01 §4 |
| **Ligne de Metal Spike Walls** | 4 069, sur le palier 1 | §6 |
| Palier 2 (Z −300) | 4 179 → 4 479 | module 01 §4 |
| Bord de plateforme D8 : mur de jupe | 4 479 | §5 |
| Débord de rampes dans le vide | 4 479 → 4 779 | §5 |

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
- **75 piliers fins de départ** au niveau 1 (Z300 → 600), un dans chaque joint de cadres d'où partent les lignes de la pente A et de l'overhang (t = ±150, ±450, ±750, ±1 050). Chacun se pose sur le joint des cadres du niveau 0, **avant** les cadres du niveau 1 qui l'encadrent (comme sur la tour 1809). Sa tête, à Z600, porte la 1re lame de la pente A et la lame r−1 de l'overhang.

## 3. Attique A : poteaux de stabilité, colonnade en option

Les **poteaux de stabilité** de la pente A (§4) forment deux rangées de poteaux en piliers fins dans l'attique :
- à 3 618,7 sous la 1re jonction (83 poteaux de 3 piliers fins) ;
- à 3 018,7 sous le bout haut (63 poteaux, 4 à 5 piliers fins).

Ils **remplacent la colonnade** : ils tiennent la pente A, et forment une grille de piliers dans l'attique.

**Colonnade (plan 2, option).** Couronne de **piliers métal sur un vrai cercle** de rayon **3 600 UU**, chaque pilier tourné vers le centre, selon le principe des cercles de piliers fournis (704, 701) :

| Paramètre | Valeur |
|---|---|
| Pas | 1 pilier / 1 vide de la largeur d'un pilier : 288 positions, pas de 1,25° (78,5 UU d'arc) |
| Passages | 6, à θ 30° + 60°·k, dans l'axe des portes du fût |
| Colonnes | **226 piliers**, 1 de haut : 288 positions − 24 pour les passages − 36 au-dessus du trou − 2 qui heurtaient un mur de chaume du bord du trou |
| Coût | 5 650 lingots, 1 582 pâte |
| Compatibilité | elle ne touche aucun poteau de stabilité : vous pouvez la poser ou non |

Si vous l'excluez, ne posez pas le plan 2. Rien ne s'y appuie.

## 4. Pente A : de la rive vers la cage, en rampes inclinées

Les lignes de lames sont sur les **joints des murs de rive** (t = ±150, ±450, ±750, ±1 050), comme les lignes de rampes des tours, qui partent des joints de leurs murs. Le milieu de chaque mur reste libre pour les tourelles de rive.

| Rang | Apothème du bas | Z bas → haut | Lignes par côté | **Rampes posées** |
|---|---|---|---|---|
| r0 | 3 918,7 (sur la rive) | 600 → 900 | 8 | 83 |
| r1 | 3 618,7 | 900 → 1200 | 6 | 63 |
| r2 | 3 318,7 | 1200 → 1500 | 6 | 62 |
| **Total** | | | | **208** |

- **3 rangs.** Un 4e rang entrerait de 80 UU dans le fût, à Z1800. La pente s'arrête à 3 018,7 (Z1500), 220 UU devant le fût.
- **Appuis** : chaque ligne part de la tête du pilier fin de départ (Z600), dans le joint de deux cadres de la rive (§2).
- **Poteaux de stabilité** (mode `stable`, défaut) : un poteau sous la 1re jonction (3 piliers fins, Z0 → 900) et un sous le bout haut (5 piliers fins, Z0 → 1500). C'est **146 poteaux et 563 piliers fins**. Si la rive ou l'un des poteaux est détruit, chaque ligne reste dans les règles des tours : au plus 1 lame pendue et 7 lames entre deux appuis. Le contrôle le vérifie lame par lame (module 08 §3) : 208 lames sur 208.
- Option `--appuis tours` : pas de poteau, comme sur les tours (3 lames libres au plus).
- Les mêmes lignes continuent dans l'overhang (§5).
- Ce qui passe entre deux lames tombe dans l'attique A (Z0) : 5 carrés de culture de Plant Species X et le tir de L1 l'y attendent (module 05).
- Au droit du trou, les lignes s'arrêtent au bord du gouffre.

## 5. Overhang, mur de jupe et débord dans le vide

### 5.1 Overhang : au-dessus des paliers

| Rang | Apothème du bas | Z bas → haut | **Rampes posées** | Position |
|---|---|---|---|---|
| r−1 | 4 218,7 | 300 → 600 | 85 | au-dessus du palier 1 et des pics |
| r−2 | 4 518,7 | 0 → 300 | 83 | au-dessus du palier 2 ; finit 40 UU après le bord D8 |

- Mêmes lignes que la pente A, pendues à la tête du même pilier fin de départ.
- **Appui** : un poteau sous la jonction r−1 / r−2 (apothème 4 218,7, Z300), debout sur le palier. Il y en a **83** : 123 piliers fins et 43 demi-piliers fins. Le rang r−2 pend d'une lame au-delà du poteau, comme la lame de rive de la tour 1201.

### 5.2 Mur de jupe : sur le bord de la plateforme

- **Sur l'arête extérieure de l'anneau 15** (bord D8, apothème 4 478,5), 8 cadres doubles par côté.
- **1 niveau**, de Z −300 à 0, posé sur le palier 2. **83 cadres doubles.** Rien n'est posé sous les fondations : l'ancien niveau suspendu (Z −600 → −300), que le jeu n'accepte pas forcément, est supprimé.
- **Aucune tourelle** : les Heavy de la jupe sont remplacées par la 2e Heavy de rive (§2).
- **Pas de plafonds de jupe.** Sous des rampes, ils formeraient un palier où l'on pourrait se poser.

### 5.3 Débord : les rampes dans le vide

| Rang | Apothème du bas | Z bas → haut | **Rampes posées** | Position |
|---|---|---|---|---|
| **r−3** | 4 778,5 | −300 → 0 | 94 | 1 seule lame dans le vide, pendue au pilier fin de départ de la jupe (`--debord 1`, défaut) |
| **Total overhang + débord** | | | **262** | |

- Les lignes du débord partent du haut de la jupe (Z0), sur les **joints de ses cadres** (t = 0, ±300 … ±1 200), à 150 UU des lignes de l'overhang.
- **Appui** : un **pilier fin de départ** dans chaque joint de la jupe (Z −300 → 0), debout sur l'arête du palier 2 et posé avant les cadres qui l'encadrent : **84 piliers fins** (les coins servent à deux lignes). Une seule lame pend de sa tête, comme la lame de rive de la tour 1201.
- Bout du débord : 300 UU au-delà du bord de la plateforme. `--debord 2` n'a plus d'effet : sans niveau de jupe sous les fondations, un 2e rang n'aurait pas d'appui.

## 6. Ligne de pics protégée (bordure basse)

- **74 Metal Spike Walls**, à l'apothème **4 068,7** et à **Z −150** sur le palier 1, pointes vers l'extérieur (`donnees/03_ligne_pics.csv`).
- Le rang r−1 passe 600 UU au-dessus d'eux. Ce qui passe entre deux lames tombe sur les pics, sous le tir de la Heavy et de la Tesla de rive de son côté.
- ⚠ La pose d'un mur de pics métal sur fondation est à valider en solo. Repli : bord de plateforme à l'apothème 4 520, sous le rang r−2.

## 7. Glissement : du faîtage jusqu'au vide

Sur une lame inclinée à 45°, ni un joueur ni un dino ne tient debout. Ce qui touche les rampes glisse le long des lames, vers l'extérieur :

| # | Rampes | De → à | À la sortie |
|---|---|---|---|
| 1 | Toit du pod (module 02 §8) | faîtage Z5100 → couronne D4 (Z3000) | tombe de 600 UU dans la poche du toit de cage (Z2400), au pied de la tour : anneau de tourelles D4, Plant X |
| 2 | Appentis, puis casquette (module 04) | Z2700 → D5 (Z2400) → 3 099 (Z2100) | chute sur la pente A, devant la tête des tourelles L1 |
| 3 | Pente A | 3 099 → 3 919 (Z1420 → 600) | continue sur l'overhang |
| 4 | Overhang | 3 919 → 4 519 (Z600 → 0) | tombe de 40 UU sur le débord |
| 5 | Débord | 4 519 → 4 779 (Z −40 → −300) | **dans le vide**, 300 UU au-delà de la plateforme |
| — | Au droit du trou : toit, casquettes du trou, pente A | jusqu'au bord du gouffre | **dans le trou** |

**Entre les lames** (vide de 300 UU) :

| Où | On tombe sur | Défense |
|---|---|---|
| Toit du pod | le plancher de toit Z3000 | tourelles et Plant X du dessus |
| Appentis | la poche du toit de cage Z2400 | anneau D4 de la tour, Plant X, Tesla |
| Casquette | une tête de tourelle L1, ou la pente A | L1 à bout portant |
| Pente A | l'attique A (Z0) | Plant X, tir de L1 entre les lames |
| Overhang r−1, r−2 | les paliers de bord | pics, Heavy et Tesla de rive |
| Débord r−3 | le vide, le long de la jupe | 2 Heavy de rive et L1 tirent vers la mer ; sous la plateforme, aucune tourelle (§5.2) |

## 8. Contrôles de fin de module

- [ ] Rive : 2 niveaux de cadres doubles (121), 27 murs de chaume (niveau 0 : 11 Heavy ; niveau 1 : 5 Tesla, 11 Heavy) ; remplacée par les murs de bord au droit du trou.
- [ ] 75 piliers fins de départ dans les joints de la rive (niveau 1), 84 dans ceux de la jupe, posés avant les cadres voisins. Pente A : 208 rampes, 146 poteaux de stabilité (563 piliers fins). Overhang : 168 rampes et 83 poteaux sur les paliers. Débord : 94 rampes. Jupe : 83 cadres doubles sur le palier 2, rien sous Z0. Aucune rampe au-dessus du trou.
- [ ] Colonnade : posée ou non (option) ; elle ne gêne aucun poteau.
- [ ] Aucune lame ne prend appui sur un mur de chaume.
- [ ] 74 pics posés sous r−1.
