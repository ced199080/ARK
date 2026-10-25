# Module 05 — Plan de câblage et matrice balistique (cap 100 : Heavy + Tek ; Tesla en plus)

Templates (`templates/plans/`, module 06) :
- `Plan_2_murs_rampes_tourelles_anneaux_12-15.json` : les 36 tourelles extérieures (jupe, rive, bord du trou à Z0 / Z300) ;
- `Plan_7_tourelles_cage_L1.json` : les 60 tourelles de la cage L1 (dont 7 sur les murs de bord du trou).

Chaque tourelle y est précédée de son **mur de chaume de pose**, à démolir en jeu.
Les 100 murs de chaume à démolir sont listés dans `donnees/08_chaume_a_demolir.csv`, avec leur plan, leur n° d'entrée dans le JSON, la tourelle qu'ils portent et ce qui est posé au-dessus (module 08 §4).
Liste maîtresse : `donnees/05_matrice_tourelles.csv`. Elle donne l'ordre, le type, la couche, les coordonnées du chaume et de la tourelle, et le sens de tir.
Plan : `plans/plan_tourelles.png`.

![Plan des tourelles et câblage](plans/plan_tourelles.png)

## 1. Règle du turret cap

| Paramètre serveur | Valeur officielle documentée | Effet |
|---|---|---|
| `bLimitTurretsInRange` | true | active la limite |
| `LimitTurretsRange` | **10 000 UU** (≈ 33,3 fondations) | rayon de la **sphère** de comptage |
| `LimitTurretsNum` | **100** | tourelles au plus dans la sphère |

- Tourelles comptées : auto, Heavy, Tek, Plant Species X. **Les Tesla ne sont pas comptées** (règle moteur retenue au module 09). Jusqu'ici, on les comptait par prudence (scénario B).
- **Les 100 places du cap sont toutes prises** par 65 Heavy et 35 Tek. Les 10 Tesla de l'inventaire s'y ajoutent.
- À la pose, le jeu compte les tourelles déjà posées à moins de 10 000 UU (distance 3D) et refuse la pose si le cap est atteint.

## 2. Le cap est global sur cette base

| Mesure (sur les 110 tourelles) | Valeur |
|---|---|
| Distance 3D maximale entre deux tourelles | **9 101 UU** (< 10 000) |
| Rayon horizontal maximal (jupe) | 4 551 UU |
| Distance minimale d'une tourelle étrangère pour n'entrer dans aucune sphère | **14 551 UU ≈ 48,5 fondations du centre** |

Toutes les tourelles se voient entre elles : la base entière compte pour un seul cap de 100. Gardez une zone d'exclusion d'environ 50 fondations pour toute autre tourelle de votre tribu.

## 3. Répartition : 100 tourelles comptées + 10 Tesla

| Couche | Heavy | Tek | Tesla | Total | Plan |
|---|---|---|---|---|---|
| L1, cage, sur D5 | 26 | 27 | — | 53 | 7 |
| **TROU-L1** : bord du trou, niveau L1 (Z1800) | 4 | 3 | — | 7 | 7 |
| Jupe (16 « int » + 10 « ext ») | 26 | — | — | 26 | 2 |
| Rive : milieu des côtés E0 (5) et des côtés E1 à 30°, 90°, 270°, 330° (4) | — | — | 9 | 9 | 2 |
| **TROU** : bord du trou, Z0 / Z300 | 4 | — | 1 | 5 | 2 |
| **TOIT** : debout sur le plancher de toit Z2400, sous les rampes | 5 | 5 | — | 10 | 6 |
| **Total** | **65** | **35** | **10** | **110** | |
| dont comptées par le cap | 65 | 35 | — | **100** | |
| Inventaire | 80 | 35 | 10 | | |
| Réserve | 15 | 0 | 0 | | |

- Le trou supprime 12 emplacements (7 de L1, 4 de jupe, 1 de rive). Ils sont **reposés sur les murs de bord du trou, face au gouffre** (module 06 §4).
- **Toit** : 10 tourelles debout (5 Tek, 5 Heavy) sur un cercle de 1 000 UU de rayon, sous les rampes du toit. Ce sont les seules qui tirent vers l'intérieur et vers le haut au-dessus du centre :
  - L1 ne voit que l'extérieur de la cage ;
  - le toit et le ciel au-dessus du pod étaient un angle mort ;
  - ces tourelles couvrent aussi le comble, où tombe ce qui passe entre les lames.
- Les 4 Tesla des côtés E1 de la rive sont dans l'axe des passages de la colonnade, entre deux lignes de rampes.

## 4. Montage vertical : mur de chaume puis tourelle

| Type | pitch | yaw | roll | Référence |
|---|---|---|---|---|
| Heavy, Tek | −89,5° | θ_tir + 90° | −90° | template 2727 *Straight Heavy* |
| Tesla | 0° | θ_tir + 90° | −90° | Tesla latérales des tours 1201 / 1809 |
| Heavy, Tek du toit (debout, sans chaume) | 0° | θ | 0° | tourelles posées sur plancher de la tour 1201 (pivot 10 UU au-dessus du plancher) |

| Couche | Mur de chaume (Z bas → haut, z template) | Pivot de la tourelle |
|---|---|---|
| L1 | ligne D5 (2 799,0), Z1800 → 2100, z 2040 | apothème 2 809,0, z 2040 |
| RIVE | ligne D7 (3 918,7), milieu des côtés E0, Z300 → 600, z 540 | apothème 3 928,7, z 540 |
| JUPE-ext | sous le mur de jupe, au bord D8 (4 478,5), au milieu d'un mur de jupe (t = ±750), suspendu Z −900 → −600, z −660 | apothème 4 488,5, vers la mer |
| JUPE-int | sous le mur de jupe (4 478,5), au milieu d'un mur (t = ±450 sur les côtés impairs, ±150 sur les côtés pairs), suspendu Z −900 → −600, z −660, face côté piton | apothème 4 468,5, vers le piton |
| TROU-L1 | mur de bord du trou, niveau 6 : Z1800 → 2100, z 2040 | 10 UU devant le mur, côté gouffre, z 2040 |
| TROU | mur de bord du trou, niveau 0 (Heavy, Z0 → 300, z 240) ou niveau 1 (Tesla, Z300 → 600, z 540), jamais les deux sur le même mur | 10 UU devant le mur, côté gouffre |

**Ce qui est posé au-dessus du chaume** (`donnees/08_chaume_a_demolir.csv`, colonne `pose_au_dessus`) : comme sur la tour 1809, où 78 des 86 murs de chaume ont un cadre de porte posé dessus, chaque mur de chaume L1 porte un cadre double L2. Une colonne de murs de bord du trou n'a jamais qu'un mur de chaume. Rien d'autre ne repose sur du chaume : aucune rampe n'y prend appui (module 08 §4).

⚠ **À valider en solo** :
- l'accroche d'un mur de chaume sous le mur de jupe ;
- le maintien de la tourelle après démolition du chaume.

## 5. Ordre de pose

- Les tourelles sont réparties entre le plan 2 (extérieur), le plan 6 (toit) et le plan 7 (cage). Le cap est atteint exactement : 100 Heavy et Tek ; les Tesla n'y entrent pas.
- Le n° d'ordre suit des priorités. À l'intérieur de chacune, il suit la suite de van der Corput (0°, 180°, 90°, 270°…), pour rester réparti si la pose s'interrompt. Chaque plan pose ses tourelles dans cet ordre.

| Priorité | Ordres | Contenu | Plan |
|---|---|---|---|
| P1 | 1-30 | 26 Heavy de jupe (dessous de la plateforme et mer) + 4 Heavy du bord du trou (Z0) | 2 |
| P2 | 31-60 | 30 Tek de L1, dont 3 sur le bord du trou | 7 |
| P3 | 61-70 | 9 Tesla de rive (pied de mur) + 1 Tesla du bord du trou (Z300) | 2 |
| P4 | 71-100 | 30 Heavy de L1, dont 4 sur le bord du trou | 7 |
| P5 | 101-110 | 5 Tek + 5 Heavy debout sur le plancher de toit | 6 |

## 6. Matrice détaillée

H = Heavy, T = Tek, S = Tesla, suivi du n° d'ordre. L1 : positions p0 à p4 dans le sens des θ croissants. Jupe : dans l'ordre des t croissants (−750 → +750). *trou* : emplacement au-dessus du gouffre, reposé sur un mur de bord (tableau suivant).

| Côté (θ) | L1 p0 | p1 | p2 | p3 | p4 | Jupe | Rive |
|---|---|---|---|---|---|---|---|
| 0° | T42 | H89 | T31 | H71 | T46 | ext 8, int 23, ext 1 | S61 |
| 30° | H86 | T39 | H79 | T54 | H94 | int 16, int 9 | S66 |
| 60° | T35 | H75 | T50 | H90 | T43 | ext 24, int 5, ext 20 | S64 |
| 90° | H83 | T58 | H98 | T33 | H73 | int 13, int 28 | S69 |
| 120° | T48 | H88 | T41 | H81 | T56 | ext 3, int 18, ext 11 | S63 |
| 150° | H96 | T37 | H77 | T52 | *trou* | int 26, int 7 | — |
| 180° | *trou* | *trou* | *trou* | *trou* | *trou* | *trou* (3) | *trou* |
| 210° | *trou* | T45 | H92 | T60 | H85 | int 17, *trou* (1) | — |
| 240° | T32 | H100 | T47 | H72 | T40 | ext 10, int 25, ext 6 | S65 |
| 270° | H87 | T55 | H80 | T36 | H95 | int 21, int 14 | S70 |
| 300° | T51 | H76 | T44 | H91 | T59 | ext 29, int 4, ext 19 | S62 |
| 330° | H84 | T34 | H99 | T49 | H74 | int 12, int 27 | S67 |

Sur L1, Tek et Heavy alternent sans interruption hors du trou.

**Tourelles reposées sur les murs de bord du trou** (tir vers le gouffre) :

| N° | Couche | θ | Mur de chaume (x ; y) | Z bas du chaume | Sens de tir | Plan |
|---|---|---|---|---|---|---|
| H2 | TROU | 204,9° | (−3 188,7 ; −1 494,6) | 0 | 120° | 2 |
| H15 | TROU | 160,2° | (−3 618,7 ; 1 309,8) | 0 | 270° | 2 |
| H22 | TROU | 159,9° | (−3 338,7 ; 1 234,8) | 0 | 240° | 2 |
| H30 | TROU | 204,2° | (−3 468,7 ; −1 569,6) | 0 | 90° | 2 |
| T38 | TROU-L1 | 201,8° | (−2 499,0 ; −1 009,8) | 1800 | 90° | 7 |
| T53 | TROU-L1 | 202,6° | (−2 219,1 ; −934,8) | 1800 | 120° | 7 |
| T57 | TROU-L1 | 156,3° | (−1 939,2 ; 859,8) | 1800 | 270° | 7 |
| S68 | TROU | 159,4° | (−3 058,8 ; 1 159,8) | 300 | 270° | 2 |
| H78 | TROU-L1 | 203,7° | (−1 939,2 ; −859,8) | 1800 | 90° | 7 |
| H82 | TROU-L1 | 157,4° | (−2 219,1 ; 934,8) | 1800 | 240° | 7 |
| H93 | TROU-L1 | 205,0° | (−1 659,3 ; −784,8) | 1800 | 120° | 7 |
| H97 | TROU-L1 | 158,2° | (−2 499,0 ; 1 009,8) | 1800 | 270° | 7 |

**Tourelles du toit** (debout sur le plancher Z2400, pivot z 2500, tournées vers l'extérieur ; plan 6) :

| N° | θ | Position (x ; y) |
|---|---|---|
| T101 | 18° | (951,1 ; 309,0) |
| H106 | 54° | (587,8 ; 809,0) |
| T104 | 90° | (0 ; 1 000,0) |
| H109 | 126° | (−587,8 ; 809,0) |
| T103 | 162° | (−951,1 ; 309,0) |
| H108 | 198° | (−951,1 ; −309,0) |
| T105 | 234° | (−587,8 ; −809,0) |
| H110 | 270° | (0 ; −1 000,0) |
| T102 | 306° | (587,8 ; −809,0) |
| H107 | 342° | (951,1 ; −309,0) |

La Tesla S66 est sur un autre mur de bord que les 4 Heavy : un mur ne porte jamais deux murs de chaume superposés.

## 7. Couverture et zones d'ombre

| Couche | Couverture verticale | Limite |
|---|---|---|
| L1 | −51,1° → +89,9°, ≈ 180° en azimut par tourelle | en bas, le haut du mur de jupe ; plus bas, le tir voit l'attique A et les paliers entre les rampes. En haut, rien : les rampes de la casquette ne masquent pas le ciel |
| JUPE-ext | −89,9° → +89,9° vers la mer | aucune : les rampes de l'overhang et du débord ne masquent rien |
| JUPE-int | −89,9° → +9,7° vers le piton et le dessous de la plateforme | dessous de la base ; sous-face de plateforme non modélisée |
| Tesla | palier 1 entier (3 919 → 4 179 UU, Z −150) et palier 2 de 4 230 à 4 479 UU (Z −300) | poche fermée sous l'overhang ; 51 UU du palier 2 masqués derrière la marche de Ø 28 |

**Zones d'ombre traitées**
- Pied de rive : 5 Tesla et 74 pics. Les 51 UU masqués au pied de la marche de Ø 28 sont trop étroits pour un dino, mais un joueur collé à la marche y échappe à la Tesla. Pour fermer ce recoin, posez une rangée de pics au pied de la marche (à la main, hors template).
- Dessous de la plateforme : 16 Heavy tournées vers le piton.
- Mer au pied du piton : 10 Heavy tournées vers l'extérieur, plus L1 jusqu'à −49°.
- **Gouffre** : 12 tourelles face au trou, sur ses deux bords. 5 au ras de la plateforme (4 Heavy à Z0, 1 Tesla à Z300) près du bord extérieur, 7 au niveau L1 (Z1800) dans le pod et le couloir. Leurs secteurs de tir se recouvrent au-dessus du trou.

**Ciel** : couvert jusqu'à la verticale par L1 et par la jupe extérieure. Les rampes inclinées ne bloquent ni la vue ni le tir (lames espacées de 300 UU), et rien ne peut se poser dessus.

## 8. Plan de câblage : 2 générateurs Tek

| Source | Position | Rôle | Portée à régler |
|---|---|---|---|
| **Générateur Tek n°2** (mezzanine) | (−900 ; 0), Z1800 | **35 Tek** : les 30 de L1 entre 1 350 et 3 760 UU, et les 5 du toit entre 810 et 2 020 UU | **≥ 3 800 UU** |
| **Générateur Tek n°1** (hall) | (900 ; 1 559), Z0 | réplicateur, forge à vapeur, labo, puis secours de L1 jusqu'à 5 040 UU | maximum |

- Les **Tek** exigent un générateur Tek.
- Les **Heavy et Tesla** sont électriques. Celles de la jupe sont à 2 780–5 600 UU du générateur le plus proche, les Tesla de rive à 2 180–4 650 UU, les tourelles du bord du trou à 1 100–3 440 UU.
- Le trou coupe la boucle de câbles de la galerie (anneau 8) à l'avant : elle devient un arc ouvert de θ ≈ 205° à 155°.
- Si les sphères ne les couvrent pas, posez des câbles électriques :
  - boucle sous le plancher Z1800 ;
  - descentes par les 6 passages de la colonnade ;
  - liaison vers la jupe par la bande sous l'overhang.
  Il faut alors un générateur électrique, absent de votre liste et non compté au module 07.

⚠ Vérifiez en jeu la sphère de portée des générateurs Tek au réglage maximal.

## 9. Réglages et munitions

| Tourelle | Portée | Cibles | Munitions |
|---|---|---|---|
| Heavy | Haute | survivants + créatures apprivoisées non alliées | balles de fusil avancé |
| Tek | Haute | idem | fragments d'élément |
| Tesla | — | idem ; mode brûlure, étourdissement ou vulnérabilité | cristal |

## 10. Contrôles

- [ ] 110 tourelles : 65 Heavy, 35 Tek (100 comptées par le cap), 10 Tesla. Sur L1, motif T H T H T / H T H T H hors du trou. 10 tourelles debout sous le toit.
- [ ] Les 16 de jupe « int » tirent vers le piton, les 10 « ext » vers la mer.
- [ ] 12 tourelles sur les murs de bord du trou, toutes tournées vers le gouffre.
- [ ] 100 murs de chaume démolis ; les tourelles restent en place.
- [ ] Les 35 Tek (30 de L1, 5 du toit) sont alimentées par le générateur n°2.
- [ ] Réserve : 15 Heavy ; zone d'exclusion d'environ 50 fondations respectée (le cap de 100 est plein).
