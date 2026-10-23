# Module 03 — Rive, colonnade circulaire, pente de glisse et overhang dans le vide

Template : `templates/03_rive_colonnade_pente_overhang2.json` (`--debord 1` pour la variante courte), réparti dans les phases :
- **P2** : mur de rive, colonnade ;
- **P4** : pente A, overhang, jupe.

Les Tesla de rive et leurs murs de chaume sont posés en **P7** avec les tourelles (module 05).

Coordonnées : `donnees/03_rive_colonnade_pente_overhang2.csv`, `donnees/03_colonnade.csv`, `donnees/03_ligne_pics.csv`. Coupe : `plans/coupe_radiale.png`.

![Coupe radiale](plans/coupe_radiale.png)

## 1. Ordre des couches, du pod vers le vide

Il suit votre schéma (lignes 30 → 32) :

| Couche | Rayon / apothème (UU) | Rôle |
|---|---|---|
| Base du pod (mur D4) | 2 239 | module 02 |
| Couloir, fût de cage D5 | 2 239 → 2 799 | module 04 |
| **Colonnade : piliers larges côte à côte (1 posé, 1 vide de la largeur d'un pilier)** | **3 360 (cercle)** | ce module, §3 |
| Mur de rive D7 | 3 919 | §2 |
| **Ligne de Metal Spike Walls** | 4 069 | §6 |
| Bord de plateforme D8, overhang, vide | 4 479 → 5 119 | §5 |

## 2. Mur de rive (D7)

| Niveau | Z | Contenu (84 positions = 12 côtés × 7) |
|---|---|---|
| 0 | 0 → 300 | 83 murs + **1 cadre de porte double** : sas, côté θ 270°, position 3, centre (0 ; −3 918,7) |
| 1 | 300 → 600 | 74 murs + **10 emplacements laissés libres** pour les Tesla verticales. Chacun reçoit en P7 un mur de chaume de pose et une Tesla fixée sur sa face extérieure |

- Les emplacements Tesla sont à θ ≈ 0° · 34,4° · 72,9° · 107,1° · 145,6° · 180° · 214,4° · 252,9° · 287,1° · 325,6°.
- Hauteur apparente de la rive depuis l'extérieur : 750 UU.
- **Après démolition du chaume**, chaque emplacement Tesla est une ouverture de 300 × 300 entre 450 et 750 UU au-dessus de la bande, la Tesla au nu du mur.
  ⚠ Ce point d'entrée est surveillé par la Tesla elle-même, par les pics en dessous et par la colonnade derrière (§3). Fermez-le par un mur si la Tesla est détruite.

## 3. Colonnade circulaire (piliers larges côte à côte)

C'est une couronne de **piliers métal sur un vrai cercle**, chaque pilier tourné vers le centre (yaw = θ), selon le même principe que les cercles de piliers fournis (704 « 48 pillar circle », 701).

| Paramètre | Valeur |
|---|---|
| Rayon | **3 360 UU** (Ø 22,4 fondations), sous le milieu de la pente A, entre le fût (coins à 2 898) et la rive (3 919) |
| Pas | **1 pilier / 1 vide de la largeur d'un pilier**. Le template 704 met 48 piliers sur r = 600, soit un pas de 78,5 UU = 2 × 39,3 UU. Ici : 264 positions, pas de 1,364° (79,97 UU d'arc) |
| Passages de service | 2, de ≈ 360 UU libres, à θ 90° et 270° (8 positions retirées), dans l'axe des portes du fût, du sas et des générateurs |
| Colonnes | **256** |
| Hauteur | de Z0 jusqu'à 30 UU sous la pente A : **3 piliers + 1 demi-pilier** (sommet Z1050) vers le milieu des côtés, **4 piliers** (sommet Z1200) vers les arêtes |
| Pièces | 816 piliers + 208 demi-piliers |
| Pose | Template Hammer : les positions d'un cercle ne tombent pas sur les coins de fondations. Coordonnées : `donnees/03_colonnade.csv` |

**Rôle**
1. Elle soutient la pente A à mi-portée (1 200 UU entre la rive et le fût).
2. Elle forme une **grille intérieure** derrière la rive. Un assaillant qui force la rive ou un emplacement Tesla trouve des vides de 40 UU, trop étroits pour un corps : il doit détruire des piliers.
3. Elle partage l'attique A en deux anneaux :
   - l'intérieur, entre le fût et la colonnade, abrite les générateurs de secours ;
   - l'extérieur, entre la colonnade et la rive, donne l'accès aux Tesla.

**Variante.** `--colonnade 2560` place la colonnade dans le couloir, entre le mur de pod et le fût, sous la galerie : 196 colonnes de 6 piliers, de Z0 à Z1800.

⚠ **À valider en solo.** La largeur réelle du pilier métal est déduite du template 704. Si les piliers se touchent ou laissent un vide différent, ajustez `largeur_pilier` en tête du script et régénérez.

## 4. Pente A : de la rive à la cage

| Rang | Apothème du bord bas | Z bas → haut | Toits par côté | Total |
|---|---|---|---|---|
| r0 | 3 918,7 (sur la rive) | 600 → 900 | 7 | 84 |
| r1 | 3 618,7 | 900 → 1200 | 7 | 84 |
| r2 | 3 318,7 | 1200 → 1500 | 6 | 72 |
| r3 | 3 018,7 | 1500 → 1800 | 6 | 72 |

Le dernier rang passe 80 UU derrière la ligne du fût. La pente coupe donc le fût à Z 1 719,5, sous la cage : aucun jour à la rupture de pente.

## 5. Overhang : débordement dans le vide

| Rang | Apothème du bord bas | Z bas → haut | Toits par côté | Total | Position |
|---|---|---|---|---|---|
| r−1 | 4 218,7 | 300 → 600 | 8 | 96 | au-dessus du décaissement |
| r−2 | 4 518,7 | 0 → 300 | 9 | 108 | finit 40 UU après le bord D8 |
| **r−3** | 4 818,7 | −300 → 0 | 9 | 108 | **1re structure dans le vide** |
| **r−4** | 5 118,7 | −600 → −300 | 10 | 120 | **2e structure dans le vide** (`--debord 2`, défaut) |

- Bout de l'overhang : apothème 5 118,7 à Z −600, soit 640 UU au-delà du bord de la plateforme (340 UU avec `--debord 1`).
- **Jupe** (`--debord 2` seulement) :
  - mur d'about à l'apothème 4 518,7, de Z −600 à 0 (216 murs) ;
  - plafonds s1 et s2 à Z −600 sous les rangs r−3/r−4 (228 plafonds).
  Elle porte les 30 Heavy verticales du dessous de la plateforme : leurs murs de chaume pendent sous la jupe (module 05).
- **Pose en Template Hammer uniquement** sous le bord de la plateforme.

## 6. Ligne de pics protégée (bordure basse)

- **84 Metal Spike Walls**, 7 par côté, à l'apothème **4 068,7** et à **Z −150** sur la bande décaissée, pointes vers l'extérieur.
- Coordonnées : `donnees/03_ligne_pics.csv`.
- Le rang r−1 passe 600 UU au-dessus d'eux : ils sont à l'abri des largages et invisibles d'en haut.
- Avec les Tesla de rive, qui voient toute la bande de 3 919 à 4 479 UU, ils couvrent l'angle mort de la cage.
- ⚠ La pose d'un mur de pics métal sur fondation est à valider en solo. Repli : bord de plateforme à l'apothème 4 520, sous le rang r−2.

## 7. Chaîne de glisse complète

| # | Surface | Entrée → sortie | Chute à la sortie |
|---|---|---|---|
| 1 | Pointe et cône | Z5250 → bord du cône (2 239, Z3000) | 40 UU sur la reprise |
| 2 | Reprise | 2 199 → 2 799 (Z3000 → 2400) | — |
| 3 | Casquette | 2 799 → 3 099 (Z2400 → 2100) | ≈ 680 UU sur la pente A, à ≈ 190 UU devant la tête des tourelles L1 (module 04 §5) |
| 4 | Pente A | 3 099 → 3 919 (Z1420 → 600) | — |
| 5 | Overhang | 3 919 → 5 119 (Z600 → −600) | **dans le vide**, 640 UU au-delà de la plateforme |

## 8. Contrôles de fin de module

- [ ] Rive : 2 niveaux, 1 sas, 10 emplacements Tesla libres au niveau 1.
- [ ] Colonnade : 256 colonnes, 2 passages à 90° et 270°, sommets sous la pente sans contact.
- [ ] Pente A : 312 toits ; overhang : 432 toits ; jupe : 216 murs + 228 plafonds.
- [ ] 84 pics posés sous r−1.
