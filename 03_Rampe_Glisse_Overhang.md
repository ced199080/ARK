# Module 03 — Pente de glisse, rive extérieure et overhang dans le vide

Template : `templates/03_rive_pente_overhang2.json` (`--debord 1` pour la variante courte). Il est réparti dans les phases **P2** (mur de rive) et **P4** (pente A, overhang, jupe).
Coordonnées : `donnees/03_rive_pente_overhang2.csv`, `donnees/03_ligne_pics.csv`. Coupe : `plans/coupe_radiale.png`.

![Coupe radiale](plans/coupe_radiale.png)

## 1. Principe

Depuis la cage à tourelles (module 04) jusqu'au vide, la toiture est une **surface continue à 45°** faite de toits métal. Elle ne contient aucune rampe : les rampes sont praticables à pied, les toits non. La pente :
1. passe au-dessus du mur de rive, haut de 2 niveaux ;
2. recouvre la bande décaissée, où se trouve la ligne de pics ;
3. **dépasse de 1 ou 2 structures au-delà du bord de la plateforme**.

Tout ce qui glisse quitte le toit **hors de l'emprise de la plateforme** et tombe dans la mer.

## 2. Mur de rive (D7)

| Niveau | Z | Contenu (84 positions = 12 côtés × 7) |
|---|---|---|
| 0 | 0 → 300 | 73 murs + **10 murs-fenêtres** (embrasures Tesla) + **1 cadre de porte double** (sas, côté θ 270°, position 3, centre (0 ; −3 918,7)) |
| 1 | 300 → 600 | 84 murs |

- Les murs s'accrochent sur l'arête D7, entre l'anneau 13 (Z0) et l'anneau 14 (Z −150).
- Hauteur apparente depuis l'extérieur : 600 + 150 = 750 UU.
- **Embrasures Tesla** : murs-fenêtres aux θ ≈ 0° · 34,4° · 72,9° · 107,1° · 145,6° · 180° · 214,4° · 252,9° · 287,1° · 325,6°. Les repères côté/index exacts sont dans `donnees/synthese.json`. La Tesla se pose dans l'attique, 150 UU en retrait du mur-fenêtre (module 05).
- **Sas.** Porte double métal dans le cadre, puis porte du fût au même azimut (module 04), puis porte du hall (θ 270°). Le Tek Teleporter du hall reste l'accès normal ; le sas sert de secours. Pour le fermer définitivement, remplacez le cadre par un mur.

## 3. Pente A : de la rive à la cage

Quatre rangs de toits montent du haut de la rive (Z600) vers le centre.

| Rang | Apothème du bord bas (UU) | Z bas → haut | Toits par côté | Total |
|---|---|---|---|---|
| r0 | 3 918,7 (sur la rive) | 600 → 900 | 7 | 84 |
| r1 | 3 618,7 | 900 → 1200 | 7 | 84 |
| r2 | 3 318,7 | 1200 → 1500 | 6 | 72 |
| r3 | 3 018,7 | 1500 → 1800 | 6 | 72 |

- Le bord haut du rang 3 (apothème 2 718,7, Z1800) passe **80 UU derrière la ligne du fût** (D5 = 2 799,0). La pente coupe donc le fût à Z 1 719,5, juste sous le plancher de galerie : **aucun jour à la rupture de pente**.
- Exemple de pose, côté θ = 0°, rang r0 : 7 toits centrés en x = 3 768,7, y = −900 à +900 par pas de 300, z template = 600 + 90 + 150 = 840, yaw 180°.
- Sous la pente, l'**attique A** (entre le fût et la rive) fait 2 murs de haut à la rive et 5,7 murs au fût. Il accueille les générateurs de secours, les Tesla et les câbles.

## 4. Overhang : débordement dans le vide

Les rangs continuent vers l'extérieur et vers le bas, avec la même pente.

| Rang | Apothème du bord bas (UU) | Z bas → haut | Toits par côté | Total | Position |
|---|---|---|---|---|---|
| r−1 | 4 218,7 | 300 → 600 | 8 | 96 | au-dessus du décaissement |
| r−2 | 4 518,7 | 0 → 300 | 9 | 108 | au-dessus du décaissement ; finit 40 UU après le bord D8 |
| **r−3** | 4 818,7 | −300 → 0 | 9 | 108 | **1re structure dans le vide** |
| **r−4** | 5 118,7 | −600 → −300 | 10 | 120 | **2e structure dans le vide** (option `--debord 2`, par défaut) |

| Variante | Bout de l'overhang | Dépassement du bord de plateforme (D8 = 4 478,5) |
|---|---|---|
| `--debord 1` | apothème 4 818,7, Z −300 | 340 UU |
| `--debord 2` (défaut) | apothème 5 118,7, Z −600 | 640 UU |

- Aux angles, le point le plus éloigné du bout est à 5 299 UU du centre (rayon de coin).
- Les rangs r−3 et r−4 sont entièrement dans le vide. **Pose en Template Hammer uniquement** : aucune accroche vanilla n'existe sous le bord d'une plateforme.
- Les toits de l'overhang comptent plus de pièces par côté que les côtés eux-mêmes ne mesurent. Le chevauchement aux 12 arêtes (de 60 à 140 UU par extrémité de rang) empêche tout jour.

## 5. Ligne de pics protégée (bordure basse)

- **84 Metal Spike Walls**, 7 par côté, sur la bande décaissée.
- Ils sont posés à l'apothème **4 068,7** (150 UU devant la rive), à **Z −150**, pointes vers l'extérieur (yaw = θ du côté), et suivent les murs de rive.
- Coordonnées : `donnees/03_ligne_pics.csv`. Exemple, côté 0° : x = 4 068,7, y = −900 à +900.
- **Protection.** Le rang r−1 passe à 600 UU au-dessus des pics. Ils sont hors de portée d'un dino largué, ne se voient pas d'en haut, et leur toit les met à l'abri des tirs plongeants.
- **Rôle.**
  - Le pied de la rive est un angle mort pour la cage (module 05 §5). Les pics interdisent d'y stationner : ils blessent au contact et repoussent.
  - Avec les Tesla des embrasures, ils couvrent toute la bande.
- ⚠ **À valider en solo** : la pose d'un mur de pics métal sur fondation. Les murs de pics en bois exigent le sol. Si la pose est refusée, placez la ligne à l'apothème 4 520 sur le bord de la plateforme : elle reste couverte par le rang r−2.

## 6. Jupe basse (sous l'overhang)

C'est le support des tourelles qui couvrent le **dessous de la plateforme** (module 05). Seulement avec `--debord 2`.

| Élément | Cotes | Pièces |
|---|---|---|
| Mur d'about | apothème 4 518,7, de Z −600 à Z0 (2 niveaux), 9 murs par côté | 216 |
| Plafonds s1 | de 4 518,7 à 4 818,7, Z −600, 9 par côté | 108 |
| Plafonds s2 | de 4 818,7 à 5 118,7, Z −600, 10 par côté | 120 |

- Le mur d'about rejoint le bord haut du rang r−3 à Z0.
- Le caisson (mur d'about + plafonds + toits r−3/r−4) est fermé.
- Les tourelles pendent **sous** les plafonds s1. Elles sont à 450 UU en retrait du bord de chute : un dino qui glisse du bout de l'overhang (5 118,7) tombe devant elles sans les toucher.
- **Service.** Remplacez 1 plafond s1 sur 3 par un plafond à trappe pour recharger depuis le caisson. On entre dans le caisson par une porte dans le mur d'about, depuis la bande décaissée, au droit du sas. ⚠ Accroche d'une tourelle sous une trappe à valider ; le template 1087 suspend ses tourelles sous des trappes Tek.

## 7. Chaîne de glisse complète (anti-drop / anti-launch)

| # | Surface | Entrée → sortie | Chute à la sortie |
|---|---|---|---|
| 1 | Pointe et cône | Z5250 → bord du cône (2 239, Z3000) | 40 UU sur la reprise |
| 2 | Reprise (module 04) | 2 199 → 2 799 (Z3000 → 2400) | — |
| 3 | Casquette | 2 799 → 3 099 (Z2400 → 2100) | **≈ 680 UU** sur la pente A, à 350 UU devant l'axe des tourelles |
| 4 | Pente A | 3 099 → 3 919 (Z1420 → 600) | — |
| 5 | Overhang | 3 919 → 5 119 (Z600 → −600) | **dans le vide**, 640 UU au-delà de la plateforme |

Aucune surface n'est plane ni en contre-pente. Le seul ressaut, la fente devant la cage, est le lieu de tir des tourelles (module 04).

## 8. Contrôles de fin de module

- [ ] Rive : 2 niveaux, 10 murs-fenêtres, 1 sas.
- [ ] Pente A : 312 toits ; overhang : 432 toits (`--debord 2`) ; jupe : 216 murs + 228 plafonds.
- [ ] Aucun jour visible depuis l'attique A, ni à la jonction pente/fût.
- [ ] 84 pics posés et à l'abri sous r−1.
