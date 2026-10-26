# Module 05 — Défense : cap de 100, tourelles, Tesla et Plant Species X

La défense tient en **3 plans** (`templates/plans/`, module 06) :

| Plan | Contenu | Calage |
|---|---|---|
| `Plan_07_tourelles_D8-D4.json` | du bord D8 à D4 : 2 Heavy de rive par côté, Tesla de rive, Tek et Heavy de la cage L1, tourelles reposées sur le bord du trou, 5 carrés de culture dans l'attique | pile d'ancrage |
| `Plan_08_tourelles_perimetre_pod.json` | périmètre de la tour du pod : anneau de Tek et Heavy au niveau 8 (Z2400), 2 Tesla, 6 carrés de culture moyens sur le toit de cage | pile d'ancrage |
| `Plan_11_tourelles_dessus.json` | dessus de la tour : Heavy, Tek et Tesla debout, 4 carrés de culture sur le plancher de toit | mur de référence **B** (module 02 §8) |

- **Murs de chaume.** Les tourelles verticales se posent sur un mur de chaume de pose, à démolir ensuite. Ces 79 murs de chaume sont dans les plans de zone, à leur place dans les murs (plans 3 à 6) : les plans de défense ne posent que les tourelles et les carrés de culture.
- **Liste maîtresse** : `donnees/05_matrice_tourelles.csv`. Elle donne l'ordre, le type, la couche, le plan, les coordonnées du support et de la tourelle, et le sens de tir.
- **Murs de chaume à démolir** : `donnees/08_chaume_a_demolir.csv`.
- **Couverture** : `donnees/05_couverture.csv` et `plans/couverture.png`.

**Aucune tourelle sous le niveau des fondations centrales (Z0).** Toutes les tourelles sont posées à Z0 ou plus haut ; le générateur le vérifie. Les 16 Heavy de la jupe, qui pendaient sous la plateforme (Z −900 → −600), sont supprimées : leurs places du cap vont à une 2e Heavy de rive par côté et à L1.

![Plan des tourelles et câblage](plans/plan_tourelles.png)

## 1. Règle du turret cap

| Paramètre serveur | Valeur officielle documentée | Effet |
|---|---|---|
| `bLimitTurretsInRange` | true | active la limite |
| `LimitTurretsRange` | **10 000 UU** (≈ 33,3 fondations) | rayon de la **sphère** de comptage |
| `LimitTurretsNum` | **100** | tourelles au plus dans la sphère |

- Comptent dans le cap : auto, Heavy, Tek, **Plant Species X** (ark.wiki.gg) et **les Tesla** (confirmé sur votre serveur).
- **Les 100 places du cap sont toutes prises** : 49 Heavy, 26 Tek, 10 Tesla et 15 Plant X.
- À la pose, le jeu compte les tourelles déjà posées à moins de 10 000 UU (distance 3D). Au-delà de 100, les tourelles en trop ne tirent plus.

## 2. Le cap est global sur cette base

| Mesure (sur les 100 emplacements) | Valeur |
|---|---|
| Distance 3D maximale entre deux tourelles | **7 954 UU** (< 10 000) |
| Rayon horizontal maximal (rive) | 3 974 UU |
| Distance minimale d'une tourelle étrangère pour n'entrer dans aucune sphère | **13 974 UU ≈ 46,6 fondations du centre** |
| Écart minimal entre deux tourelles | **295 UU**, une largeur de mur (contrôle : `ecart_tourelles`) |

Toute la base compte pour un seul cap de 100. Gardez une zone d'exclusion d'environ 47 fondations pour toute autre tourelle de votre tribu.

## 3. Répartition : 100 emplacements

| Couche | Où | Heavy | Tek | Tesla | Plant X | Total | Plan |
|---|---|---|---|---|---|---|---|
| RIVE | rive D7, niveaux 0 (Z0 → 300) et 1 (Z300 → 600) : 2 Heavy par côté, 1 Tesla au milieu des côtés E0 (niveau 1) | 22 | — | 5 | — | 27 | 7 |
| L1 | cage D5, Z1800 → 2100, 31 positions sur 53 | 15 | 16 | — | — | 31 | 7 |
| TROU, TROU-L1 | murs de bord du trou, face au gouffre (Z0, Z300, Z1800) | 4 | 2 | 1 | — | 7 | 7 |
| X-attique | attique A (Z0), sous la pente A, milieu des côtés E0 | — | — | — | 5 | 5 | 7 |
| **D4** | tour du pod, niveau 8 (Z2400 → 2700), au-dessus du toit de cage : 1 par côté + 2 Tesla | 6 | 5 | 2 | — | 13 | 8 |
| TROU-D4 | mur de bord du pod, niveau 8, face au gouffre | — | 1 | — | — | 1 | 8 |
| X-D4 | toit de cage (Z2400), au pied de la tour, côtés E1 : carrés **moyens** (la poche fait 260 UU) | — | — | — | 6 | 6 | 8 |
| **DESSUS** | plancher de toit (Z3000), debout | 2 | 2 | 2 | 4 | 10 | 11 |
| **Total** | | **49** | **26** | **10** | **15** | **100** | |
| Inventaire | | 80 | 35 | 10 | — | | |
| Réserve | | 31 | 9 | 0 | — | | |

- **La ligne L1 complète le cap.** Ses 60 positions sur D5 sont prises régulièrement autour du cercle, autant qu'il reste de places : 35 aujourd'hui, dont 4 reposées sur le bord du trou. Les autres positions de L1 sont des cadres doubles.
- **Le trou** supprime des emplacements (L1, rive, D4). Ils sont reposés sur les murs de bord du trou, face au gouffre (module 06 §4).
- **Plant Species X** : le plan pose un grand carré de culture (`CropPlotLarge_SM`, comme la tour 1584), ou un carré moyen (`CropPlotMedium_SM`, 220 UU) dans la poche du toit de cage, trop étroite pour un grand carré (300 UU). La graine se plante à la main. La plante a besoin d'eau (tuyaux ou réservoir) et d'engrais. Elle tire des spores qui ralentissent et aveuglent, à courte portée.
- **Autres répartitions** en tête du script :
  - `rive_heavy` : sans la 2e Heavy de rive (niveau 0), il revient 11 places à L1 ;
  - `d4_tesla` : les Tesla de la tour ;
  - `dessus` : la liste des pièces du dessus.
  Ces réglages ne changent pas le cap : L1 se réajuste toujours pour faire 100.

## 4. Montage

| Type | pitch | yaw | roll | Référence |
|---|---|---|---|---|
| Heavy, Tek verticales (sur chaume) | −89,5° | θ_tir + 90° | −90° | template 2727 *Straight Heavy* |
| Tesla verticales (sur chaume) | 0° | θ_tir + 90° | −90° | Tesla latérales des tours 1201 / 1809 |
| Heavy, Tek, Tesla du dessus (debout, sans chaume) | 0° | θ | 0° | tourelles posées sur un plancher (tour 1201) ; pivot 10 UU au-dessus du plancher |
| Carré de culture | 0° | θ | 0° | tour 1584 ; pivot 10 UU au-dessus du plancher |

| Couche | Mur de chaume (Z bas → haut, z template) | Plan du chaume | Pivot de la tourelle |
|---|---|---|---|
| L1 | ligne D5 (2 799,0), Z1800 → 2100, z 2040 | 6 | apothème 2 809,0, z 2040 |
| RIVE | ligne D7 (3 918,7), niveau 0 : Z0 → 300, z 240 ; niveau 1 : Z300 → 600, z 540 | 3 | apothème 3 928,7 |
| D4 | tour du pod (2 239,2), niveau 8 : Z2400 → 2700, z 2640 | 5 | apothème 2 249,2, z 2640 |
| TROU, TROU-L1, TROU-D4 | mur de bord du trou, niveau 0, 1, 6 ou 8 | 4, 5 ou 6 | 10 UU devant le mur, côté gouffre |

**Ce qui est posé au-dessus du chaume** (colonne `pose_au_dessus` du CSV des murs de chaume) :
- un cadre double (47), sur L1, sur la rive au-dessus des Heavy du niveau 0, et sur le bord du trou ;
- un mur plein (16), pour la couronne au-dessus de l'anneau D4 et les murs de bord du pod ;
- rien (16), pour le niveau 1 de la rive.

C'est la tour 1809 : 78 de ses 86 murs de chaume ont un cadre de porte posé dessus, qui reste tenu par ses voisins. Aucune rampe ne prend appui sur du chaume (module 08 §4).

⚠ **À valider en solo** : le maintien de la tourelle, et du mur posé au-dessus, après démolition du chaume.

## 5. Ordre de pose

Le n° d'ordre suit des priorités. À l'intérieur de chacune, il suit la suite de van der Corput (0°, 180°, 90°, 270°…), pour rester réparti si la pose s'interrompt. Chaque plan pose ses tourelles dans cet ordre.

| Priorité | Ordres | Contenu | Plan |
|---|---|---|---|
| P1 | 1-24 | Heavy de rive (2 par côté) et du bord du trou (Z0) | 7 |
| P2 | 25-42 | Tek de L1, dont 2 sur le bord du trou | 7 |
| P3 | 43-48 | 5 Tesla de rive + 1 Tesla du bord du trou (Z300) | 7 |
| P4 | 49-65 | Heavy de L1, dont 2 sur le bord du trou | 7 |
| P5 | 66-79 | anneau D4 de la tour : 6 Heavy, 6 Tek (dont 1 sur le bord du trou), 2 Tesla | 8 |
| P6 | 80-85 | dessus : 2 Heavy, 2 Tek, 2 Tesla debout | 11 |
| P7 | 86-100 | 15 carrés de culture de Plant X : 5 de l'attique (plan 7), 6 du toit de cage (plan 8), 4 du dessus (plan 11) | 7, 8, 11 |

## 6. Matrice détaillée

H = Heavy, T = Tek, S = Tesla, suivi du n° d'ordre. L1 : positions p0 à p4 dans le sens des θ croissants ; « cadre » = position sans tourelle (cadre double). Rive : niv0 = Z0 → 300, niv1 = Z300 → 600.

| Côté (θ) | L1 p0 | p1 | p2 | p3 | p4 | Rive | Tour D4 |
|---|---|---|---|---|---|---|---|
| 0° | T35 | cadre | T25 | H49 | cadre | H1 (niv0), H23 (niv1), S43 | T76 |
| 30° | T34 | cadre | H58 | T30 | cadre | H13 (niv0), H7 (niv1) | H66 |
| 60° | H54 | cadre | T39 | cadre | H62 | H19 (niv0), H4 (niv1), S46 | S70, T73 |
| 90° | T28 | cadre | H52 | cadre | T37 | H10 (niv0), H16 (niv1) | H77 |
| 120° | H60 | cadre | T32 | cadre | H56 | H3 (niv0), H22 (niv1), S45 | T68 |
| 150° | cadre | T41 | H64 | cadre | *trou* | H15 (niv0), H9 (niv1) | H75 |
| 180° | *trou* | *trou* | *trou* | *trou* | *trou* | *trou* | *trou* |
| 210° | *trou* | T31 | cadre | H55 | T40 | H12 (niv0), H18 (niv1) | H79 |
| 240° | cadre | H63 | cadre | T29 | H53 | H2 (niv0), H24 (niv1), S44 | T67 |
| 270° | cadre | T38 | cadre | H61 | cadre | H14 (niv0), H8 (niv1) | H74 |
| 300° | T33 | H57 | cadre | T42 | cadre | H20 (niv0), H5 (niv1), S47 | T71, S78 |
| 330° | H65 | T26 | cadre | H50 | cadre | H11 (niv0), H17 (niv1) | H69 |

**Tourelles reposées sur les murs de bord du trou** (tir vers le gouffre) :

| N° | Couche | θ | Mur de chaume (x ; y) | Z bas du chaume | Sens de tir | Plan |
|---|---|---|---|---|---|---|
| H21 | TROU | 160,2° | (−3 618,7 ; 1 309,8) | 0 | 270° | 7 |
| H6 | TROU | 204,2° | (−3 468,7 ; −1 569,6) | 0 | 90° | 7 |
| S48 | TROU | 159,9° | (−3 338,7 ; 1 234,8) | 300 | 240° | 7 |
| T27 | TROU-L1 | 156,3° | (−1 939,2 ; 859,8) | 1800 | 270° | 7 |
| T36 | TROU-L1 | 158,2° | (−2 499,0 ; 1 009,8) | 1800 | 270° | 7 |
| H51 | TROU-L1 | 202,6° | (−2 219,1 ; −934,8) | 1800 | 120° | 7 |
| H59 | TROU-L1 | 205,0° | (−1 659,3 ; −784,8) | 1800 | 120° | 7 |
| T72 | TROU-D4 | 203,7° | (−1 939,2 ; −859,8) | 2400 | 90° | 8 |

**Dessus** (debout sur le plancher de toit Z3000, à 1 500 UU du centre, au milieu de chaque côté, entre deux lignes de rampes) :

| θ | 0° | 30° | 60° | 90° | 120° | 150° | 210° | 240° | 270° | 300° |
|---|---|---|---|---|---|---|---|---|---|---|
| Pièce | X86 | H80 | X98 | T83 | S82 | X100 | H85 | X91 | T81 | S84 |

**Plant X** : attique (Z0, grands carrés) à θ 2,7° · 62,7° · 122,7° · 242,7° · 302,7° ; toit de cage (Z2400, carrés moyens) à θ 33,6° · 93,6° · 153,6° · 213,6° · 273,6° · 333,6°.

## 7. Couverture : tous les angles

### 7.1 Secteurs verticaux (coupe radiale au milieu d'un côté)

| Couche | Site min → max | Limite |
|---|---|---|
| L1 | −51,1° → +89,9° | en bas, le haut du mur de rive ; plus bas, l'attique A entre les lames |
| D4 (tour) | −18,4° → +89,9° | en bas, le bord du toit de cage à D5 ; elle tire par-dessus l'appentis et la casquette |
| DESSUS | −7,7° → +89,9°, sur 360° | le bord de la toiture pleine |
| Heavy de rive, niveau 0 | −18,4° → +89,9° | le bord du palier 2 : elle voit les 2 paliers et la ligne de pics |
| Heavy de rive, niveau 1 | −45,0° → +89,9° | le bord du palier 2 |
| Tesla de rive | palier 1 entier (Z −150) et palier 2 à partir de 4 230 UU (Z −300) | poche sous l'overhang |

### 7.2 Contrôle de couverture (`couverture()`)

Le générateur compte, pour 9 zones d'approche et tous les 10° autour de la base, le nombre de tourelles Heavy et Tek qui voient le point visé.

Le modèle :
- murs et planchers pleins, approchés par des cylindres et des anneaux ;
- cadres doubles comptés pleins, ce qui est pessimiste ;
- lames de rampes transparentes ;
- une tourelle verticale ne tire que devant son mur ;
- portée **High = 20 fondations** (6 000 UU), Medium = 14 fondations (ark.wiki.gg) ;
- les Tesla et les Plant X, à courte portée, ne sont pas comptées.

| Zone d'approche (rayon, Z) | Tourelles au moins (High) | En moyenne | Au moins (Medium) |
|---|---|---|---|
| Sous la plateforme, au piton (3 000, −1 500) | **0** (avant : 5) | 0 | 0 |
| Mer, au pied du piton (6 500, −1 500) | **5** (avant : 6) | 9,6 | 0 |
| Paliers et ligne de pics (4 300, −150) | **2** (avant : 1) | 2,0 | 2 |
| Attique, sous la pente A (3 300, 150) | **2** | 4,9 | 2 |
| Pente A et overhang (3 700, 1 000) | **5** (avant : 4) | 6,7 | 5 |
| Toit de cage, poche au pied de la tour (2 550, 2 550) | **1** | 1,6 | 1 |
| Toit du pod (1 300, 4 200) | **4** | 4,0 | 4 |
| Ciel au-dessus de la base (2 000, 7 500) | **4** | 4,0 | 0 |
| Approche à 7 000 UU (7 000, 2 000) | **13** (avant : 10) | 19,5 | 0 |

**Chaque direction au-dessus de la plateforme est couverte**, hors des points au-dessus du trou (le gouffre a ses propres tourelles).

- **Dessous de la plateforme : plus couvert.** C'est la conséquence directe de la règle « aucune tourelle sous Z0 » : une tourelle posée sur la plateforme ne voit pas sous le bord (le palier 2 la masque). Ce qui monte le long du piton est vu dès qu'il dépasse le bord : par les 2 Heavy de rive de son côté, puis par L1. Pour l'interdire plus tôt, il faudrait des défenses sans place au cap (pics, murs) sous le bord, ou rendre des tourelles à la jupe.
- **Paliers** : les 2 Heavy de rive de chaque côté (une tourelle de rive ne voit que son côté du dodécagone). Sur les côtés E0, la Tesla de rive s'y ajoute, et les pics partout.
- **Poche au pied de la tour** : tenue par une seule tourelle à la fois, l'anneau D4 de son côté, plus les 6 Plant X et les 2 Tesla de la tour. Pour passer à 2, il faudrait 12 tourelles de plus sur la tour, à prendre sur L1 (réglage en tête du script, §3).

Carte complète : `plans/couverture.png` (rouge : moins de 2) et `donnees/05_couverture.csv`.

## 8. Noyau : générateurs Tek et boîtes de munitions, plan de câblage

Le **noyau** est au centre de la base, au plus loin de tous les murs extérieurs : 4 carrés de l'anneau 1, autour de la colonne d'escaliers (`plans/plan_pod.png`). Chaque équipement y est **posé sur une fondation** et **enfermé dans une cage** de murs métal (plan 5) :
- 2 murs de haut (Z0 → 600), sur les 4 côtés du carré ;
- au niveau 0, le côté tourné vers le hall est un **cadre de porte double** : posez-y une porte double métal ;
- un plafond métal au-dessus (Z600).

| Équipement | θ | Position (x ; y) | Rôle |
|---|---|---|---|
| **Générateur Tek n°1 (principal)** | 180° | (−409,8 ; 0) | les 26 Tek et les machines du hall |
| **Générateur Tek n°2 (secours)** | 240° | (−204,9 ; −354,9) | même portée : il prend le relais si le n°1 tombe en panne d'élément ou est détruit |
| **Boîte de munitions n°1** | 60° | (204,9 ; 354,9) | Heavy (balles de fusil avancé) |
| **Boîte de munitions n°2** | 120° | (−204,9 ; 354,9) | Tek (élément) et Heavy |

**Portée à régler** (distance 3D, depuis le noyau) :

| Cibles | Distance |
|---|---|
| Tek (26), depuis l'un ou l'autre générateur | 2 620 à 3 811 UU : **≥ 3 850 UU** |
| Heavy (49) | 2 445 à 4 403 UU |
| Toutes les tourelles, depuis chaque boîte de munitions | **≤ 4 403 UU ≈ 14,7 fondations** |

- Les **Tek** exigent un générateur Tek. Les 2 générateurs sont réglés à la même portée : un seul suffit.
- Les **Heavy et Tesla** sont électriques. Distances au noyau par couche : rive 3 550 à 4 310, L1 3 110 à 3 740, bord du trou 2 450 à 3 470, tour D4 3 090 à 3 650, dessus 3 290 à 3 600 UU.
- **Boîtes de munitions** : toutes les tourelles sont à moins de 15 fondations du noyau, dans la portée de 15 à 20 fondations que vous avez indiquée. Elles sont derrière la tour du pod, sa mezzanine et les galeries : un tir extérieur doit percer toute la base pour les atteindre.
- Le trou coupe la boucle de câbles de la galerie (anneau 8) à l'avant : elle devient un arc ouvert de θ ≈ 205° à 155°.
- Si les sphères ne couvrent pas tout, posez des câbles électriques :
  - boucle sous le plancher Z1800 ;
  - descentes par les cadres du fût ;
  - liaison vers la rive par la bande sous la pente A.

  Il faut alors un générateur électrique, absent de votre liste et non compté au module 07.
- Plant X : tuyaux d'eau jusqu'aux carrés de culture (attique, toit de cage, dessus), ou réservoirs.

⚠ À vérifier en jeu :
- la sphère de portée des générateurs Tek au réglage maximal ;
- la portée et le chemin d'accès des boîtes de munitions (pièce récente : son chemin de classe et son coût ne sont pas relevés, elle n'est pas dans les plans et se pose à la main dans sa cage).

## 9. Réglages et munitions

| Tourelle | Portée | Cibles | Munitions |
|---|---|---|---|
| Heavy | Haute | survivants + créatures apprivoisées non alliées | balles de fusil avancé |
| Tek | Haute | idem | fragments d'élément |
| Tesla | — | idem ; mode brûlure, étourdissement ou vulnérabilité | cristal |
| Plant Species X | — | tout ce qui n'est pas de la tribu | eau + engrais |

## 10. Contrôles

- [ ] 100 emplacements : 49 Heavy, 26 Tek, 10 Tesla, 15 Plant X ; aucune tourelle sous Z0.
- [ ] Rive : 2 Heavy par côté (niveaux 0 et 1), 5 Tesla (côtés E0). Jupe : cadres seuls.
- [ ] L1 : 31 tourelles, Tek et Heavy alternées autour du cercle ; 22 cadres doubles aux autres positions.
- [ ] Tour D4 : 1 tourelle par côté + 2 Tesla au niveau 8 ; 6 Plant X au pied de la tour.
- [ ] 8 tourelles sur les murs de bord du trou, toutes tournées vers le gouffre.
- [ ] Dessus : 2 Heavy, 2 Tek, 2 Tesla, 4 Plant X, sous le toit en rampes.
- [ ] 79 murs de chaume démolis ; les tourelles et les murs posés au-dessus restent en place.
- [ ] Les 26 Tek sont alimentées par le générateur principal ; le générateur de secours a la même portée.
- [ ] Noyau : 2 générateurs et 2 boîtes de munitions en cage, portes doubles posées et verrouillées.
- [ ] Réserve : 31 Heavy, 9 Tek, 0 Tesla ; zone d'exclusion d'environ 47 fondations respectée (le cap de 100 est plein).
