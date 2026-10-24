# Module 03 — Rive (socle de la cage), colonnade circulaire, rampes de glisse et overhang dans le vide

Template : `templates/03_rive_colonnade_overhang2.json` (`--debord 1` pour la variante courte), réparti dans les phases :
- **P2** : mur de rive, colonnade ;
- **P4** : overhang en rampes inclinées, mur de jupe.

**Profil bas.** La cage à tourelles est posée directement sur le mur de rive (module 04). Il n'y a donc plus de pente A entre la rive et la cage : c'est elle qui faisait monter la base, puisqu'une pente à 45° monte d'autant qu'elle avance.

**Aucun toit incliné.** Sur un toit à 45°, on tient debout et rien ne glisse. Toutes les pentes sont donc faites de **rampes inclinées** (Sloped Railing), en lames au pas de 300 UU comme sur les tours 1201 et 1809 (règle de pose : module 04 §6).

Les Tesla de rive et leurs murs de chaume sont posés en **P7** avec les tourelles (module 05).

Coordonnées : `donnees/03_rive_colonnade_overhang2.csv`, `donnees/03_colonnade.csv`, `donnees/03_ligne_pics.csv`. Coupe : `plans/coupe_radiale.png`.

![Coupe radiale](plans/coupe_radiale.png)

## 1. Ordre des couches, du pod vers le vide

Il suit votre schéma (lignes 30 → 32) :

| Couche | Rayon / apothème (UU) | Rôle |
|---|---|---|
| Base du pod (mur D4) | 2 239 | module 02 |
| Hall extérieur (stockage), poteaux D5 et D6 | 2 239 → 3 919 | modules 02 et 04 |
| **Colonnade : piliers larges côte à côte (1 posé, 1 vide de la largeur d'un pilier)** | **3 360 (cercle)** | ce module, §3 |
| Mur de rive D7, cage à tourelles au-dessus | 3 919 | §2, module 04 |
| Palier 1 (Z −150) | 3 919 → 4 179 | module 01 §4 |
| **Ligne de Metal Spike Walls** | 4 069, sur le palier 1 | §6 |
| Palier 2 (Z −300) | 4 179 → 4 479 | module 01 §4 |
| Bord de plateforme D8, overhang, vide | 4 479 → 5 119 | §5 |

## 2. Mur de rive (D7)

| Niveau | Z | Contenu (84 positions = 12 côtés × 7) |
|---|---|---|
| 0 | 0 → 300 | 84 murs. Pas de sas : 6 parts égales imposeraient 6 brèches. L'accès se fait par Tek Teleporter, ou par un sas percé à la main hors template |
| 1 | 300 → 600 | 78 murs + **6 emplacements laissés libres** (1 par part, au milieu des côtés E0) pour les Tesla verticales. Chacun reçoit en P7 un mur de chaume de pose et une Tesla fixée sur sa face extérieure |
| 2 et 3 | 600 → 1200 | **la cage** : L1 tourelles, L2 double doorframes (module 04) |

- Les emplacements Tesla sont à θ = 0° · 60° · 120° · 180° · 240° · 300°.
- Hauteur apparente depuis le palier 1 : 750 UU pour la rive, 1 350 UU avec la cage posée dessus.
- **Après démolition du chaume**, chaque emplacement Tesla est une ouverture de 300 × 300 entre 450 et 750 UU au-dessus de la bande, la Tesla au nu du mur.
  ⚠ Ce point d'entrée est surveillé par la Tesla elle-même, par les pics en dessous et par la colonnade derrière (§3). Fermez-le par un mur si la Tesla est détruite.

## 3. Colonnade circulaire (piliers larges côte à côte)

C'est une couronne de **piliers métal sur un vrai cercle**, chaque pilier tourné vers le centre (yaw = θ), selon le même principe que les cercles de piliers fournis (704 « 48 pillar circle », 701).

| Paramètre | Valeur |
|---|---|
| Rayon | **3 360 UU** (Ø 22,4 fondations), dans le hall extérieur, sous le bord intérieur de la galerie L1 |
| Pas | **1 pilier / 1 vide de la largeur d'un pilier**. Le template 704 met 48 piliers sur r = 600, soit un pas de 78,5 UU = 2 × 39,3 UU. Ici : 264 positions, pas de 1,364° (79,97 UU d'arc) |
| Passages de service | **6**, 1 par part, de ≈ 360 UU libres, à θ 30° + 60°·k (24 positions retirées), sous les trappes de la galerie L1 |
| Colonnes | **240** (40 par part) |
| Hauteur | **1 pilier** (Z0 → 300), comme les cercles de piliers fournis (704, 701), qui n'ont qu'un rang |
| Pièces | **240 piliers** (contre 768 piliers + 192 demi-piliers dans la version précédente) |
| Pose | Template Hammer : les positions d'un cercle ne tombent pas sur les coins de fondations. Coordonnées : `donnees/03_colonnade.csv` |

**Rôle**
1. Elle forme une **grille intérieure** derrière la rive. Un assaillant qui force la rive ou un emplacement Tesla trouve des vides de 40 UU, trop étroits pour un corps. Un joueur ne saute pas 300 UU : il doit détruire des piliers.
2. Elle partage le hall extérieur en deux anneaux :
   - l'intérieur, entre le pod et la colonnade : stockage et circulation ;
   - l'extérieur, sous la galerie L1 : accès aux Tesla et échelles vers la galerie, par les 6 passages.

**Variantes.**
- `colonnade_hauteur` en tête du script : 600 pour 2 piliers (hauteur de la rive), au prix de 240 piliers de plus (1 680 pâte).
- `--colonnade 2560` rapproche la colonnade du pod.

⚠ **À valider en solo.** La largeur réelle du pilier métal est déduite du template 704. Si les piliers se touchent ou laissent un vide différent, ajustez `largeur_pilier` en tête du script et régénérez.

## 4. Overhang : débordement dans le vide, en rampes inclinées

| Rang | Apothème du bas | Z bas → haut | Lames par côté | Rampes | Position |
|---|---|---|---|---|---|
| r−1 | 4 218,7 | 300 → 600 | 9 | 108 | au-dessus du palier 1 et des pics |
| r−2 | 4 518,7 | 0 → 300 | 9 | 108 | au-dessus du palier 2 ; finit 40 UU après le bord D8 |
| **r−3** | 4 818,7 | −300 → 0 | 9 | 108 | **1re structure dans le vide** |
| **r−4** | 5 118,7 | −600 → −300 | 9 | 108 | **2e structure dans le vide** (`--debord 2`, défaut) |
| **Total** | | | | **432** | |

- L'overhang part du haut de la rive (Z600), juste sous les tourelles L1 de la cage. Ses lames continuent celles de la casquette et du toit (module 04).
- Bout de l'overhang : apothème 5 118,7 à Z −600, soit 640 UU au-delà du bord de la plateforme (340 UU avec `--debord 1`).
- **Mur de jupe** (`--debord 2` seulement) : mur d'about à l'apothème 4 518,7, de Z −600 à 0 (216 murs). Il porte les 30 Heavy verticales du dessous de la plateforme : leurs murs de chaume pendent sous ce mur, face côté mer ou face côté piton (module 05).
- **Plus de plafonds de jupe.** Sous des rampes, ils formeraient un palier où l'on pourrait se poser, juste au-dessus des tourelles de jupe. Sans eux, ce qui passe entre les lames de r−3/r−4 tombe dans le vide.
- **Pose en Template Hammer uniquement** sous le bord de la plateforme.

## 5. Ligne de pics protégée (bordure basse)

- **84 Metal Spike Walls**, 7 par côté, à l'apothème **4 068,7** et à **Z −150** sur le palier 1, pointes vers l'extérieur.
- Coordonnées : `donnees/03_ligne_pics.csv`.
- Le rang r−1 passe 600 UU au-dessus d'eux. Ce qui glisse sur ses lames tombe au-delà ; ce qui passe entre deux lames tombe sur les pics, sous le tir de la Tesla.
- Avec les 6 Tesla de rive, qui voient tout le palier 1 et le palier 2 à partir de 4 230 UU, ils couvrent l'angle mort de la cage.
- ⚠ La pose d'un mur de pics métal sur fondation est à valider en solo. Repli : bord de plateforme à l'apothème 4 520, sous le rang r−2.

## 6. Glissement : du toit jusqu'au vide

Sur une lame inclinée à 45°, ni un joueur ni un dino ne tient debout.

| # | Rampes | De → à | À la sortie |
|---|---|---|---|
| 1 | Toit bas en dents de scie (module 04 §6) | Z1200 → 1500 | rien ne s'y pose ; on retombe entre les lames, sur le plancher fermé Z1200 |
| 2 | Casquette | 3 919 → 4 219 (Z1200 → 900) | chute de ≈ 600 UU sur l'overhang, à ≈ 190 UU devant la tête des tourelles L1 (module 04 §5) |
| 3 | Overhang | 3 919 → 5 119 (Z600 → −600) | **dans le vide**, 640 UU au-delà de la plateforme |

⚠ **Le toit bas ne fait pas glisser jusqu'au vide.** Une pente de rampes qui irait du centre au bord monterait aussi haut que la distance parcourue, environ 3 900 UU. Le toit bas empêche seulement de se poser : rien ne tient sur les lames, et ce qui passe entre elles reste sur le plancher fermé. Le glissement vers le vide ne commence qu'au bord : casquette puis overhang.

**Entre les lames** (vide de 300 UU, assez large pour un joueur, trop étroit pour un gros dino) :

| Où | On tombe sur | Défense |
|---|---|---|
| Toit | le plancher fermé Z1200 | aucun accès vers l'intérieur |
| Casquette | une tête de tourelle L1, ou l'overhang | à bout portant de L1 (module 04 §5) |
| Overhang r−1, r−2 | les paliers de bord | pics, Tesla de rive |
| Overhang r−3, r−4 | le vide | — |

## 7. Contrôles de fin de module

- [ ] Rive : 2 niveaux, 6 emplacements Tesla libres au niveau 1 (θ 0° + 60°·k).
- [ ] Colonnade : 240 piliers sur un rang, 6 passages à θ 30° + 60°·k.
- [ ] Overhang : 432 rampes ; mur de jupe : 216 murs. Aucun toit incliné, pas de pente A.
- [ ] 84 pics posés sous r−1.
