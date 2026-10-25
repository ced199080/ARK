# Module 03 — Rive, colonnade circulaire, rampes de glisse et overhang dans le vide

Templates (`templates/plans/`, module 06) :
- `Plan_2_murs_rampes_tourelles_anneaux_12-15.json` : rive, colonnade, pente A extérieure (rangs r0-r1), overhang, mur de jupe, murs de bord du trou des anneaux 12-13 ;
- `Plan_5_cage_et_pente_interieure.json` : pente A intérieure (rangs r2-r3).

Phases à l'intérieur des plans :
- **P2** : mur de rive, colonnade, murs de bord du trou ;
- **P4** : pente A et overhang en rampes inclinées, mur de jupe.

**Aucun toit incliné.** Sur un toit à 45°, on tient debout et rien ne glisse. Toutes les pentes sont donc faites de **rampes inclinées** (Sloped Railing), en lames au pas de 300 UU comme sur les tours 1201 et 1809 (règle de pose : module 02 §8).

**Le trou** (module 06) coupe la rive, la colonnade, la pente A, l'overhang, la jupe et les pics à l'avant, entre θ ≈ 155° et 205°. Les chiffres ci-dessous sont ceux de la base avec le trou ; la colonne « sans trou » rappelle le tour complet.

Les Tesla de rive et leurs murs de chaume sont posés en **P7** avec les tourelles (module 05).

Coordonnées : `donnees/Plan_2_*.csv`, `donnees/Plan_5_*.csv`, `donnees/03_colonnade.csv`, `donnees/03_ligne_pics.csv`. Coupe (θ 0°, hors trou) : `plans/coupe_radiale.png`. Rampes : `plans/plan_rampes.png`.

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
| Bord de plateforme D8, overhang, vide | 4 479 → 5 119 | §5 |

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
| Colonnes | **228** : 288 positions − 24 pour les passages − 36 au-dessus du trou |
| Hauteur | **1 pilier** (Z0 → 300), comme les cercles de piliers fournis (704, 701), qui n'ont qu'un rang |
| Pièces | **228 piliers** |
| Pose | Template Hammer : les positions d'un cercle ne tombent pas sur les coins de fondations. Coordonnées : `donnees/03_colonnade.csv` |

**Rôle**
1. Elle forme une **grille intérieure** derrière la rive. Un assaillant qui force la rive ou un emplacement Tesla trouve des vides de 40 UU, trop étroits pour un corps. Un joueur ne saute pas 300 UU : il doit détruire des piliers.
2. Elle ne porte plus la pente A : les rampes s'appuient sur la rive et sur le fût. Un rang de piliers suffit donc.
3. Elle partage l'attique A en deux anneaux :
   - l'intérieur, entre le fût et la colonnade, reste libre (câbles) ;
   - l'extérieur, entre la colonnade et la rive, donne l'accès aux Tesla.

**Variantes.**
- `colonnade_hauteur` en tête du script : 600 pour 2 piliers (hauteur de la rive), au prix de 228 piliers de plus (1 596 pâte).
- `--colonnade 2560` place la colonnade dans le couloir, entre le mur de pod et le fût, sous la galerie.

⚠ **À valider en solo.** La largeur réelle du pilier métal est déduite du template 704. Si les piliers se touchent ou laissent un vide différent, ajustez `largeur_pilier` en tête du script et régénérez.

## 4. Pente A : de la rive à la cage, en rampes inclinées

| Rang | Apothème du bas | Z bas → haut | Lames par côté | Rampes sans trou | **Rampes posées** | Plan |
|---|---|---|---|---|---|---|
| r0 | 3 918,7 (sur la rive) | 600 → 900 | 7 | 84 | 74 | 2 |
| r1 | 3 618,7 | 900 → 1200 | 7 | 84 | 74 | 2 |
| r2 | 3 318,7 | 1200 → 1500 | 7 | 84 | 73 | 5 |
| r3 | 3 018,7 | 1500 → 1800 | 7 | 84 | 73 | 5 |
| **Total** | | | | 336 | **294** | |

- Les lames sont aux positions t = 0, ±300, ±600, ±900 de chaque côté. Les mêmes lames continuent dans l'overhang (§5) : chacune descend sans rupture de Z1800 jusqu'à Z −600.
- Le dernier rang passe 80 UU derrière la ligne du fût, sous la cage.
- Ce qui passe entre deux lames tombe dans l'attique A (Z0), entre la rive et le fût. Il y trouve la colonnade et le tir de L1, qui voit l'attique entre les lames.
- Au droit du trou, les lames s'arrêtent au bord du gouffre : aucune rampe n'est posée au-dessus du vide. Les murs de bord montent jusque sous la pente A (module 06 §3).

## 5. Overhang : débordement dans le vide, en rampes inclinées

| Rang | Apothème du bas | Z bas → haut | Lames par côté | Rampes sans trou | **Rampes posées** | Position |
|---|---|---|---|---|---|---|
| r−1 | 4 218,7 | 300 → 600 | 9 | 108 | 94 | au-dessus du palier 1 et des pics |
| r−2 | 4 518,7 | 0 → 300 | 9 | 108 | 94 | au-dessus du palier 2 ; finit 40 UU après le bord D8 |
| **r−3** | 4 818,7 | −300 → 0 | 9 | 108 | 94 | **1re structure dans le vide** |
| **r−4** | 5 118,7 | −600 → −300 | 9 | 108 | 94 | **2e structure dans le vide** (`--debord 2`, défaut) |
| **Total** | | | | 432 | **376** | |

Au droit du trou, il n'y a ni palier ni overhang : le gouffre commence au bord de la pente A.

- Bout de l'overhang : apothème 5 118,7 à Z −600, soit 640 UU au-delà du bord de la plateforme (340 UU avec `--debord 1`).
- **Mur de jupe** (`--debord 2` seulement) : mur d'about à l'apothème 4 518,7, de Z −600 à 0 (2 niveaux), interrompu au droit du trou : **188 murs** (216 sans trou). Il porte 26 Heavy verticales du dessous de la plateforme : leurs murs de chaume pendent sous ce mur, face côté mer ou face côté piton (module 05). Les 4 Heavy de jupe qui tombaient dans le trou sont reposées sur les murs de bord du trou (module 06 §4).
- **Plus de plafonds de jupe.** Sous des rampes, ils formeraient un palier où l'on pourrait se poser, juste au-dessus des tourelles de jupe. Sans eux, ce qui passe entre les lames de r−3/r−4 tombe dans le vide.
- **Pose en Template Hammer uniquement** sous le bord de la plateforme.

## 6. Ligne de pics protégée (bordure basse)

- **74 Metal Spike Walls**, 7 par côté sauf au droit du trou (84 sans trou), à l'apothème **4 068,7** et à **Z −150** sur le palier 1, pointes vers l'extérieur.
- Coordonnées : `donnees/03_ligne_pics.csv`.
- Le rang r−1 passe 600 UU au-dessus d'eux. Ce qui glisse sur ses lames tombe au-delà ; ce qui passe entre deux lames tombe sur les pics, sous le tir de la Tesla.
- Avec les 5 Tesla de rive, qui voient tout le palier 1 et le palier 2 à partir de 4 230 UU, ils couvrent l'angle mort de la cage.
- ⚠ La pose d'un mur de pics métal sur fondation est à valider en solo. Repli : bord de plateforme à l'apothème 4 520, sous le rang r−2.

## 7. Glissement : du faîtage jusqu'au vide

Sur une lame inclinée à 45°, ni un joueur ni un dino ne tient debout. Ce qui touche les rampes glisse le long des lames, vers l'extérieur :

| # | Rampes | De → à | À la sortie |
|---|---|---|---|
| 1 | Toit (module 02 §8) | faîtage Z5150 → bord D5 (Z2400) | continue sur la casquette |
| 2 | Casquette | 2 799 → 3 099 (Z2400 → 2100) | chute de ≈ 680 UU sur la pente A, à ≈ 190 UU devant la tête des tourelles L1 (module 04 §5) |
| 3 | Pente A | 3 099 → 3 919 (Z1420 → 600) | continue sur l'overhang |
| 4 | Overhang | 3 919 → 5 119 (Z600 → −600) | **dans le vide**, 640 UU au-delà de la plateforme |
| — | Au droit du trou : toit, casquette du trou, pente A | jusqu'au bord du gouffre | **dans le trou** : la casquette du trou (module 02 §8.3) dépasse de 300 UU au-dessus du gouffre |

**Entre les lames** (vide de 300 UU, assez large pour un joueur, trop étroit pour un gros dino) :

| Où | On tombe sur | Défense |
|---|---|---|
| Toit | le plancher fermé Z2400 | aucun accès vers l'intérieur |
| Casquette | une tête de tourelle L1, ou la pente A | à bout portant de L1 (module 04 §5) |
| Pente A | l'attique A (Z0) | colonnade, tir de L1 entre les lames |
| Overhang r−1, r−2 | les paliers de bord | pics, Tesla de rive |
| Overhang r−3, r−4 | le vide | — |

## 8. Contrôles de fin de module

- [ ] Rive : 2 niveaux (143 murs), 5 emplacements Tesla libres au niveau 1 (θ 0°, 60°, 120°, 240°, 300°) ; remplacée par les murs de bord au droit du trou.
- [ ] Colonnade : 228 piliers sur un rang, 6 passages à θ 30° + 60°·k, interrompue au-dessus du trou.
- [ ] Pente A : 294 rampes ; overhang : 376 rampes ; mur de jupe : 188 murs. Aucun toit incliné, aucune rampe au-dessus du trou.
- [ ] 74 pics posés sous r−1.
