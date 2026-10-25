# Module 03 — Rive, colonnade circulaire, rampes de glisse et overhang dans le vide

Templates (`templates/plans/`, module 06) :
- `Plan_2_murs_rampes_tourelles_anneaux_12-15.json` : rive, colonnade, toute la pente A, overhang et débord, poteaux et poutres d'appui, mur de jupe, murs de bord du trou des anneaux 12-13.

La pente A va de la rive jusqu'à 220 UU du fût : son dernier rang passe au-dessus des anneaux 10-11. Elle est quand même entière dans le plan 2. Chaque ligne de lames est ainsi posée d'un bloc, depuis son appui sur la rive.

Phases à l'intérieur des plans :
- **P2** : mur de rive, colonnade, murs de bord du trou ;
- **P4** : mur de jupe, poteaux et poutres d'appui, puis pente A, overhang et débord en rampes inclinées (les appuis sont dans le template avant les rampes qu'ils portent).

**Aucun toit incliné.** Sur un toit à 45°, on tient debout et rien ne glisse. Toutes les pentes sont donc faites de **rampes inclinées** (Sloped Railing), en lignes de lames au pas de 300 UU comme sur les tours 1201 et 1809 (règle de pose : module 02 §8). **Chaque ligne de lames part d'un appui ; elle monte librement de 6 lames au plus, ou pend d'une seule lame**, comme sur les tours (module 08 §3).

**Le trou** (module 06) coupe la rive, la colonnade, la pente A, l'overhang, la jupe et les pics à l'avant, entre θ ≈ 155° et 205°. Les chiffres ci-dessous sont ceux de la base avec le trou ; la colonne « sans trou » rappelle le tour complet.

Les Tesla de rive et leurs murs de chaume sont posés en **P7** avec les tourelles (module 05).

Coordonnées : `donnees/Plan_2_*.csv`, `donnees/03_colonnade.csv`, `donnees/03_ligne_pics.csv`. Coupe (θ 0°, hors trou) : `plans/coupe_radiale.png`. Rampes : `plans/plan_rampes.png`.

![Coupe radiale](plans/coupe_radiale.png)

## 1. Ordre des couches, du pod vers le vide

Il suit votre schéma (lignes 30 → 32) :

| Couche | Rayon / apothème (UU) | Rôle |
|---|---|---|
| Base du pod (mur D4) | 2 239 | module 02 |
| Couloir, fût de cage D5 | 2 239 → 2 799 | module 04 |
| **Colonnade : piliers larges côte à côte (1 posé, 1 vide de la largeur d'un pilier)** | **3 600 (cercle)** | ce module, §3 |
| Mur de rive D7 | 3 919 | §2 |
| Palier 1 (Z −150) | 3 919 → 4 179 | module 01 §4 |
| **Ligne de Metal Spike Walls** | 4 069, sur le palier 1 | §6 |
| Palier 2 (Z −300) | 4 179 → 4 479 | module 01 §4 |
| Bord de plateforme D8 : mur de jupe | 4 479 | §5 |
| Débord de rampes dans le vide | 4 479 → 5 079 | §5 |

## 2. Mur de rive (D7)

| Niveau | Z | Contenu (84 positions = 12 côtés × 7, dont 10 au-dessus du trou) |
|---|---|---|
| 0 | 0 → 300 | **74 murs**. Pas de sas : l'accès se fait par Tek Teleporter, ou par un sas percé à la main hors template |
| 1 | 300 → 600 | **69 murs** + **5 emplacements laissés libres** (au milieu des côtés E0) pour les Tesla verticales. Chacun reçoit en P7 un mur de chaume de pose et une Tesla fixée sur sa face extérieure |

- Les emplacements Tesla sont à θ = 0° · 60° · 120° · 240° · 300°. Celui de 180° tombe dans le trou : sa Tesla est reposée sur un mur de bord du trou, face au gouffre (module 06 §4).
- Au droit du trou, la rive est remplacée par les **murs de bord du trou** (module 06 §3), qui ferment la base sur le gouffre.
- Hauteur apparente de la rive depuis l'extérieur : 750 UU.
- **Après démolition du chaume**, chaque emplacement Tesla est une ouverture de 300 × 300 entre 450 et 750 UU au-dessus de la bande, la Tesla au nu du mur.
  ⚠ Ce point d'entrée est surveillé par la Tesla elle-même, par les pics en dessous et par la colonnade derrière (§3). Fermez-le par un mur si la Tesla est détruite.

## 3. Colonnade circulaire (piliers larges côte à côte)

C'est une couronne de **piliers métal sur un vrai cercle**, chaque pilier tourné vers le centre (yaw = θ), selon le même principe que les cercles de piliers fournis (704 « 48 pillar circle », 701).

| Paramètre | Valeur |
|---|---|
| Rayon | **3 600 UU** (Ø 24,0 fondations), sous la pente A, entièrement sur les anneaux 12-13, entre D6 (3 359) et la rive (3 919) |
| Pas | **1 pilier / 1 vide de la largeur d'un pilier**. Le template 704 met 48 piliers sur r = 600, soit un pas de 78,5 UU = 2 × 39,3 UU. Ici : 288 positions, pas de 1,25° (78,5 UU d'arc) |
| Passages de service | **6**, 1 par secteur de 60°, de ≈ 360 UU libres, à θ 30° + 60°·k (24 positions retirées), dans l'axe des portes du fût |
| Colonnes | **226** : 288 positions − 24 pour les passages − 36 au-dessus du trou − 2 qui heurtaient un mur de chaume du bord du trou |
| Hauteur | **1 pilier** (Z0 → 300), comme les cercles de piliers fournis (704, 701), qui n'ont qu'un rang |
| Pièces | **226 piliers** |
| Pose | Template Hammer : les positions d'un cercle ne tombent pas sur les coins de fondations. Coordonnées : `donnees/03_colonnade.csv` |

**Rôle**
1. Elle forme une **grille intérieure** derrière la rive. Un assaillant qui force la rive ou un emplacement Tesla trouve des vides de 40 UU, trop étroits pour un corps. Un joueur ne saute pas 300 UU : il doit détruire des piliers.
2. Elle ne porte pas la pente A : les rampes s'appuient sur la rive et sur leurs poteaux (§4). Un rang de piliers suffit donc.
3. Elle partage l'attique A en deux anneaux :
   - l'intérieur, entre le fût et la colonnade, reste libre (câbles) ;
   - l'extérieur, entre la colonnade et la rive, donne l'accès aux Tesla.

**Variantes.**
- `colonnade_hauteur` en tête du script : 600 pour 2 piliers (hauteur de la rive), au prix de 226 piliers de plus (1 582 pâte).
- `--colonnade 2560` place la colonnade dans le couloir, entre le mur de pod et le fût, sous la galerie.

⚠ **À valider en solo.** La largeur réelle du pilier métal est déduite du template 704. Si les piliers se touchent ou laissent un vide différent, ajustez `largeur_pilier` en tête du script et régénérez.

## 4. Pente A : de la rive vers la cage, en rampes inclinées

Les lignes de lames sont sur les **joints des murs de rive** (t = ±150, ±450, ±750, ±1 050), comme les lignes de rampes des tours, qui partent des joints de leurs murs. Le milieu de chaque mur reste libre : les Tesla de rive (milieu des côtés E0) sont entre deux lignes, et aucune lame ne prend appui sur leur mur de chaume.

| Rang | Apothème du bas | Z bas → haut | Lignes par côté | Rampes sans trou | **Rampes posées** | Plan |
|---|---|---|---|---|---|---|
| r0 | 3 918,7 (sur la rive) | 600 → 900 | 8 | 96 | 83 | 2 |
| r1 | 3 618,7 | 900 → 1200 | 6 | 72 | 63 | 2 |
| r2 | 3 318,7 | 1200 → 1500 | 6 | 72 | 62 | 2 |
| **Total** | | | | 240 | **208** | |

- **3 rangs au lieu de 4.** Le 4e rang finissait 80 UU derrière la ligne du fût, à Z1800 : il entrait dans les murs du fût, dans les murs de chaume de L1 et dans le plancher de galerie. Le jeu aurait refusé ces 73 rampes. La pente s'arrête donc à 3 018,7 (Z1500), 220 UU devant le fût.
- Les lignes des angles (t = ±1 050) partent du sommet de la rive ; dès le rang r1, elles croiseraient la ligne du côté voisin et s'arrêtent après une lame.
- **Appui** : chaque ligne part du haut de la rive (Z600), sur le joint de deux murs métal. Elle monte ensuite librement de 3 lames au plus, comme les lignes des tours (jusqu'à 6). Aucun poteau n'est nécessaire.
  - Avec `--appuis prudent` : un **poteau de 5 piliers fins** (Z0 → 1500) sous le bout haut de chaque ligne, à 220 UU devant le fût ; 63 poteaux, 314 piliers fins.
- Les mêmes lignes continuent dans l'overhang (§5) : de Z1500 jusqu'à Z0, une lame tous les 300 UU.
- Ce qui passe entre deux lames tombe dans l'attique A (Z0), entre la rive et le fût. Il y trouve la colonnade et le tir de L1, qui voit l'attique entre les lames.
- Au droit du trou, les lignes s'arrêtent au bord du gouffre : aucune rampe n'est posée au-dessus du vide. Les murs de bord montent jusque sous la pente A (module 06 §3).

## 5. Overhang, mur de jupe et débord dans le vide

### 5.1 Overhang : au-dessus des paliers

| Rang | Apothème du bas | Z bas → haut | Lignes par côté | Rampes sans trou | **Rampes posées** | Position |
|---|---|---|---|---|---|---|
| r−1 | 4 218,7 | 300 → 600 | 8 | 96 | 85 | au-dessus du palier 1 et des pics |
| r−2 | 4 518,7 | 0 → 300 | 8 | 96 | 83 | au-dessus du palier 2 ; finit 40 UU après le bord D8 |

- Mêmes lignes que la pente A, accrochées au haut de la rive.
- **Appui** : un **poteau sous la jonction r−1 / r−2** (apothème 4 218,7, Z300), debout sur le palier : **83 poteaux**. Sur le palier 2 (Z −300) : 2 piliers fins ; sur la marche de l'anneau 14 (Z −150) : 1 pilier fin + 1 demi-pilier fin. En tout 123 piliers fins et 43 demi-piliers fins. Le rang r−2 est en porte-à-faux d'une lame au-delà du poteau, comme la lame de rive de la tour 1201.

### 5.2 Mur de jupe : sur le bord de la plateforme

- **Sur l'arête extérieure de l'anneau 15** (bord D8, apothème 4 478,5), 8 murs par côté, exactement sur les arêtes des fondations. Il avait jusqu'ici 9 murs par côté à 4 518,7, soit 40 UU dans le vide sans rien pour le tenir. Ces murs se croisaient aux 12 angles.
- **2 niveaux** :
  - niveau 1, de Z −300 à 0, **posé sur le palier 2** ;
  - niveau 0, de Z −600 à −300, suspendu dessous, contre la tranche des fondations.
- Au total, **166 murs** (192 sans trou).
- Il porte **26 Heavy verticales** du dessous de la plateforme. Leurs murs de chaume pendent sous le niveau 0, au milieu d'un mur de jupe, face côté mer ou face côté piton (module 05). Les 4 Heavy de jupe qui tombaient dans le trou sont reposées sur les murs de bord du trou (module 06 §4).
- **Pas de plafonds de jupe.** Sous des rampes, ils formeraient un palier où l'on pourrait se poser, juste au-dessus des tourelles de jupe.
- ⚠ À valider en solo : le niveau 0 suspendu sous le bord de l'anneau 15. Le contrôle de collisions l'admet : il touche la tranche des fondations sur 10 UU.

### 5.3 Débord : les rampes dans le vide

| Rang | Apothème du bas | Z bas → haut | Lignes par côté | Rampes sans trou | **Rampes posées** | Position |
|---|---|---|---|---|---|---|
| **r−3** | 4 778,5 | −300 → 0 | 9 | 108 | 94 | **1re structure dans le vide**, accrochée au haut de la jupe |
| **r−4** | 5 078,5 | −600 → −300 | 9 | 108 | 94 | **2e structure dans le vide** (`--debord 2`, défaut) |
| **Total overhang + débord** | | | | 408 | **356** | |

- Les lignes du débord partent du haut de la jupe (Z0), sur les **joints de ses murs** (t = 0, ±300 … ±1 200). Elles sont à 150 UU des lignes de l'overhang : r−2 passe 40 UU au-dessus du haut de la jupe, sans la toucher.
- **Appui** : une **poutre fine** (Flat Thin Pillar couché) part du niveau 0 de la jupe, à Z −300, et sort de 300 UU dans le vide sous chaque ligne. Elle porte la jonction r−3 / r−4, comme les poutres fines qui portent la première rampe des lignes de la tour 1809 : **94 poutres**. Le rang r−4 pend d'une lame au bout de la poutre.
- Bout du débord : apothème 5 078,5 à Z −600, soit **600 UU au-delà du bord de la plateforme** (300 UU avec `--debord 1`).
- **Pose en Template Hammer uniquement** sous le bord de la plateforme.

## 6. Ligne de pics protégée (bordure basse)

- **74 Metal Spike Walls**, 7 par côté sauf au droit du trou (84 sans trou), à l'apothème **4 068,7** et à **Z −150** sur le palier 1, pointes vers l'extérieur.
- Coordonnées : `donnees/03_ligne_pics.csv`.
- Le rang r−1 passe 600 UU au-dessus d'eux. Ce qui glisse sur ses lames tombe au-delà ; ce qui passe entre deux lames tombe sur les pics, sous le tir de la Tesla. Les poteaux de l'overhang sont 150 UU plus loin, sur les joints des murs de rive : ils ne gênent pas les pics.
- Avec les 5 Tesla de rive, qui voient tout le palier 1 et le palier 2 à partir de 4 230 UU, ils couvrent l'angle mort de la cage.
- ⚠ La pose d'un mur de pics métal sur fondation est à valider en solo. Repli : bord de plateforme à l'apothème 4 520, sous le rang r−2.

## 7. Glissement : du faîtage jusqu'au vide

Sur une lame inclinée à 45°, ni un joueur ni un dino ne tient debout. Ce qui touche les rampes glisse le long des lames, vers l'extérieur :

| # | Rampes | De → à | À la sortie |
|---|---|---|---|
| 1 | Toit (module 02 §8) | faîtage Z5100 → bord D5 (Z2400) | continue sur la casquette |
| 2 | Casquette | 2 799 → 3 099 (Z2400 → 2100) | chute de ≈ 680 UU sur la pente A, à ≈ 190 UU devant la tête des tourelles L1 (module 04 §5) |
| 3 | Pente A | 3 099 → 3 919 (Z1420 → 600) | continue sur l'overhang |
| 4 | Overhang | 3 919 → 4 519 (Z600 → 0) | tombe de 40 UU sur le débord |
| 5 | Débord | 4 519 → 5 079 (Z −40 → −600) | **dans le vide**, 600 UU au-delà de la plateforme |
| — | Au droit du trou : toit, casquette du trou, pente A | jusqu'au bord du gouffre | **dans le trou** : la casquette du trou (module 02 §8.3) dépasse de 300 UU au-dessus du gouffre |

**Entre les lames** (vide de 300 UU, assez large pour un joueur, trop étroit pour un gros dino) :

| Où | On tombe sur | Défense |
|---|---|---|
| Toit | le plancher fermé Z2400 | aucun accès vers l'intérieur |
| Casquette | une tête de tourelle L1, ou la pente A | à bout portant de L1 (module 04 §5) |
| Pente A | l'attique A (Z0) | colonnade, tir de L1 entre les lames |
| Overhang r−1, r−2 | les paliers de bord | pics, Tesla de rive |
| Débord r−3, r−4 | le vide, le long de la jupe | — |

## 8. Contrôles de fin de module

- [ ] Rive : 2 niveaux (143 murs), 5 emplacements Tesla libres au niveau 1 (θ 0°, 60°, 120°, 240°, 300°) ; remplacée par les murs de bord au droit du trou.
- [ ] Colonnade : 226 piliers sur un rang, 6 passages à θ 30° + 60°·k, interrompue au-dessus du trou.
- [ ] Pente A : 208 rampes sur 3 rangs, chaque ligne sur le haut de la rive. Overhang : 168 rampes et 83 poteaux sur les paliers. Débord : 188 rampes et 94 poutres fines. Mur de jupe : 166 murs sur le bord D8. Aucun toit incliné, aucune rampe au-dessus du trou.
- [ ] Aucune lame ne touche une Tesla de rive ni ne prend appui sur un mur de chaume.
- [ ] 74 pics posés sous r−1.
