# Module 05 — Défense : cap de 100, tourelles, Tesla et Plant Species X

La défense tient en **3 plans** (`templates/plans/`, module 06) :

| Plan | Contenu | Calage |
|---|---|---|
| `Plan_07_tourelles_D8-D4.json` | du bord D8 à D4 : Heavy de jupe et de rive, Tesla de rive, Tek et Heavy de la cage L1, tourelles reposées sur le bord du trou, 5 carrés de culture dans l'attique | pile d'ancrage |
| `Plan_08_tourelles_perimetre_pod.json` | périmètre de la tour du pod : anneau de Tek et Heavy au niveau 8 (Z2400), 2 Tesla, 6 carrés de culture sur le toit de cage | pile d'ancrage |
| `Plan_11_tourelles_dessus.json` | dessus de la tour : Heavy, Tek et Tesla debout, 4 carrés de culture sur le plancher de toit | mur de référence **B** (module 02 §8) |

- **Murs de chaume.** Les tourelles verticales se posent sur un mur de chaume de pose, à démolir ensuite. Ces 79 murs de chaume sont dans les plans de zone, à leur place dans les murs (plans 3 à 6) : les plans de défense ne posent que les tourelles et les carrés de culture.
- **Liste maîtresse** : `donnees/05_matrice_tourelles.csv`. Elle donne l'ordre, le type, la couche, le plan, les coordonnées du support et de la tourelle, et le sens de tir.
- **Murs de chaume à démolir** : `donnees/08_chaume_a_demolir.csv`.
- **Couverture** : `donnees/05_couverture.csv` et `plans/couverture.png`.

![Plan des tourelles et câblage](plans/plan_tourelles.png)

## 1. Règle du turret cap

| Paramètre serveur | Valeur officielle documentée | Effet |
|---|---|---|
| `bLimitTurretsInRange` | true | active la limite |
| `LimitTurretsRange` | **10 000 UU** (≈ 33,3 fondations) | rayon de la **sphère** de comptage |
| `LimitTurretsNum` | **100** | tourelles au plus dans la sphère |

- Comptent dans le cap : auto, Heavy, Tek, **Plant Species X** (ark.wiki.gg) et **les Tesla** (confirmé sur votre serveur).
- **Les 100 places du cap sont toutes prises** : 52 Heavy, 23 Tek, 10 Tesla et 15 Plant X.
- À la pose, le jeu compte les tourelles déjà posées à moins de 10 000 UU (distance 3D). Au-delà de 100, les tourelles en trop ne tirent plus.

## 2. Le cap est global sur cette base

| Mesure (sur les 100 emplacements) | Valeur |
|---|---|
| Distance 3D maximale entre deux tourelles | **9 002 UU** (< 10 000) |
| Rayon horizontal maximal (jupe) | 4 551 UU |
| Distance minimale d'une tourelle étrangère pour n'entrer dans aucune sphère | **14 551 UU ≈ 48,5 fondations du centre** |

Toute la base compte pour un seul cap de 100. Gardez une zone d'exclusion d'environ 50 fondations pour toute autre tourelle de votre tribu.

## 3. Répartition : 100 emplacements

| Couche | Où | Heavy | Tek | Tesla | Plant X | Total | Plan |
|---|---|---|---|---|---|---|---|
| JUPE-int | sous la jupe (Z −900 → −600), face au piton : dessous de la plateforme | 11 | — | — | — | 11 | 7 |
| JUPE-ext | sous la jupe, face à la mer | 5 | — | — | — | 5 | 7 |
| RIVE | rive D7, niveau 1 (Z300 → 600) : 1 Heavy par côté, 1 Tesla au milieu des côtés E0 | 11 | — | 5 | — | 16 | 7 |
| L1 | cage D5, Z1800 → 2100, une position sur deux environ | 13 | 13 | — | — | 26 | 7 |
| TROU, TROU-L1 | murs de bord du trou, face au gouffre (Z0, Z300, Z1800) | 4 | 2 | 1 | — | 7 | 7 |
| X-attique | attique A (Z0), sous la pente A, milieu des côtés E0 | — | — | — | 5 | 5 | 7 |
| **D4** | tour du pod, niveau 8 (Z2400 → 2700), au-dessus du toit de cage : 1 par côté + 2 Tesla | 6 | 5 | 2 | — | 13 | 8 |
| TROU-D4 | mur de bord du pod, niveau 8, face au gouffre | — | 1 | — | — | 1 | 8 |
| X-D4 | toit de cage (Z2400), au pied de la tour, côtés E1 | — | — | — | 6 | 6 | 8 |
| **DESSUS** | plancher de toit (Z3000), debout | 2 | 2 | 2 | 4 | 10 | 11 |
| **Total** | | **52** | **23** | **10** | **15** | **100** | |
| Inventaire | | 80 | 35 | 10 | — | | |
| Réserve | | 28 | 12 | 0 | — | | |

- **La ligne L1 complète le cap.** Ses 60 positions sur D5 sont prises régulièrement autour du cercle, autant qu'il reste de places : 29 aujourd'hui, dont 3 reposées sur le bord du trou. Les autres positions de L1 sont des cadres doubles.
- **Le trou** supprime des emplacements (L1, jupe, rive, D4). Ils sont reposés sur les murs de bord du trou, face au gouffre (module 06 §4).
- **Plant Species X** : le plan pose un grand carré de culture (`CropPlotLarge_SM`, comme la tour 1584). La graine se plante à la main. La plante a besoin d'eau (tuyaux ou réservoir) et d'engrais. Elle tire des spores qui ralentissent et aveuglent, à courte portée.
- **Autres répartitions** en tête du script :
  - `rive_heavy` : sans les Heavy de rive, il revient 11 places à L1 ;
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
| RIVE | ligne D7 (3 918,7), Z300 → 600, z 540 | 3 | apothème 3 928,7, z 540 |
| JUPE-ext / int | sous la jupe au bord D8 (4 478,5), au milieu d'un cadre, suspendu Z −900 → −600, z −660 | 3 | 10 UU devant, vers la mer ou vers le piton |
| D4 | tour du pod (2 239,2), niveau 8 : Z2400 → 2700, z 2640 | 5 | apothème 2 249,2, z 2640 |
| TROU, TROU-L1, TROU-D4 | mur de bord du trou, niveau 0, 1, 6 ou 8 | 4, 5 ou 6 | 10 UU devant le mur, côté gouffre |

**Ce qui est posé au-dessus du chaume** (colonne `pose_au_dessus` du CSV des murs de chaume) :
- un cadre double (49), sur L1 et le bord du trou ;
- un mur plein (14), pour la couronne au-dessus de l'anneau D4 et les murs de bord du pod ;
- rien (16), pour la rive et la jupe.

C'est la tour 1809 : 78 de ses 86 murs de chaume ont un cadre de porte posé dessus, qui reste tenu par ses voisins. Aucune rampe ne prend appui sur du chaume (module 08 §4).

⚠ **À valider en solo** :
- l'accroche d'un mur de chaume sous le mur de jupe ;
- le maintien de la tourelle, et du mur posé au-dessus, après démolition du chaume.

## 5. Ordre de pose

Le n° d'ordre suit des priorités. À l'intérieur de chacune, il suit la suite de van der Corput (0°, 180°, 90°, 270°…), pour rester réparti si la pose s'interrompt. Chaque plan pose ses tourelles dans cet ordre.

| Priorité | Ordres | Contenu | Plan |
|---|---|---|---|
| P1 | 1-30 | Heavy de jupe, de rive et du bord du trou (Z0) | 7 |
| P2 | 31-45 | Tek de L1, dont 2 sur le bord du trou | 7 |
| P3 | 46-51 | 5 Tesla de rive + 1 Tesla du bord du trou (Z300) | 7 |
| P4 | 52-65 | Heavy de L1, dont 1 sur le bord du trou | 7 |
| P5 | 66-79 | anneau D4 de la tour : 6 Heavy, 6 Tek (dont 1 sur le bord du trou), 2 Tesla | 8 |
| P6 | 80-85 | dessus : 2 Heavy, 2 Tek, 2 Tesla debout | 11 |
| P7 | 86-100 | 15 carrés de culture de Plant X : 5 de l'attique (plan 7), 6 du toit de cage (plan 8), 4 du dessus (plan 11) | 7, 8, 11 |

## 6. Matrice détaillée

H = Heavy, T = Tek, S = Tesla, suivi du n° d'ordre. L1 : positions p0 à p4 dans le sens des θ croissants ; « cadre » = position sans tourelle (cadre double). Jupe : i = face au piton, e = face à la mer.

| Côté (θ) | L1 p0 | p1 | p2 | p3 | p4 | Jupe | Rive | Tour D4 |
|---|---|---|---|---|---|---|---|---|
| 0° | cadre | cadre | T31 | cadre | H52 | H1e, H23i | H8, S46 | T76 |
| 30° | cadre | T39 | cadre | H59 | cadre | H16i | H9 | H66 |
| 60° | T35 | cadre | H56 | cadre | T43 | H5i, H24e | H20, S49 | S70, T73 |
| 90° | cadre | H63 | cadre | T33 | cadre | H28i | H13 | H77 |
| 120° | H54 | cadre | T41 | cadre | H61 | H11e, H18i | H3, S48 | T68 |
| 150° | cadre | T37 | cadre | H58 | *trou* | H26i | H7 | H75 |
| 180° | *trou* | *trou* | *trou* | *trou* | *trou* | *trou* | *trou* | *trou* |
| 210° | *trou* | cadre | H53 | cadre | T40 | H17i | H2 | H79 |
| 240° | cadre | H60 | cadre | T36 | cadre | H6e, H25i | H10, S47 | T67 |
| 270° | H57 | cadre | T44 | cadre | H64 | H21i | H14 | H74 |
| 300° | cadre | T34 | cadre | H55 | cadre | H4i, H29e | H19, S50 | T71, S78 |
| 330° | T42 | cadre | H62 | cadre | T38 | H27i | H12 | H69 |

**Tourelles reposées sur les murs de bord du trou** (tir vers le gouffre) :

| N° | Couche | θ | Mur de chaume (x ; y) | Z bas du chaume | Sens de tir | Plan |
|---|---|---|---|---|---|---|
| H15 | TROU | 160,2° | (−3 618,7 ; 1 309,8) | 0 | 270° | 7 |
| H22 | TROU | 159,9° | (−3 338,7 ; 1 234,8) | 0 | 240° | 7 |
| H30 | TROU | 204,2° | (−3 468,7 ; −1 569,6) | 0 | 90° | 7 |
| S51 | TROU | 205,0° | (−3 188,7 ; −1 494,6) | 300 | 120° | 7 |
| T32 | TROU-L1 | 201,8° | (−2 499,0 ; −1 009,8) | 1800 | 90° | 7 |
| T45 | TROU-L1 | 158,2° | (−2 499,0 ; 1 009,8) | 1800 | 270° | 7 |
| H65 | TROU-L1 | 157,4° | (−2 219,1 ; 934,8) | 1800 | 240° | 7 |
| T72 | TROU-D4 | 203,7° | (−1 939,2 ; −859,8) | 2400 | 90° | 8 |

**Dessus** (debout sur le plancher de toit Z3000, à 1 500 UU du centre, au milieu de chaque côté, entre deux lignes de rampes) :

| θ | 0° | 30° | 60° | 90° | 120° | 150° | 210° | 240° | 270° | 300° |
|---|---|---|---|---|---|---|---|---|---|---|
| Pièce | X86 | H80 | X98 | T83 | S82 | X100 | H85 | X91 | T81 | S84 |

**Plant X** : attique (Z0) à θ 2,7° · 62,7° · 122,7° · 242,7° · 302,7° ; toit de cage (Z2400) à θ 33,6° · 93,6° · 153,6° · 213,6° · 273,6° · 333,6°.

## 7. Couverture : tous les angles

### 7.1 Secteurs verticaux (coupe radiale au milieu d'un côté)

| Couche | Site min → max | Limite |
|---|---|---|
| L1 | −51,1° → +89,9° | en bas, le haut du mur de rive ; plus bas, l'attique A entre les lames |
| D4 (tour) | −18,4° → +89,9° | en bas, le bord du toit de cage à D5 ; elle tire par-dessus l'appentis et la casquette |
| DESSUS | −7,7° → +89,9°, sur 360° | le bord de la toiture pleine |
| JUPE-ext | −89,9° → +89,9° vers la mer | aucune |
| JUPE-int | −89,9° → +9,7° vers le piton | dessous de la base |
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
| Sous la plateforme, au piton (3 000, −1 500) | **5** | 6,4 | 3 |
| Mer, au pied du piton (6 500, −1 500) | **6** | 10,6 | 0 |
| Paliers et ligne de pics (4 300, −150) | **1** | 1,0 | 1 |
| Attique, sous la pente A (3 300, 150) | **2** | 4,2 | 2 |
| Pente A et overhang (3 700, 1 000) | **4** | 5,8 | 4 |
| Toit de cage, poche au pied de la tour (2 550, 2 550) | **1** | 1,6 | 1 |
| Toit du pod (1 300, 4 200) | **4** | 4,0 | 4 |
| Ciel au-dessus de la base (2 000, 7 500) | **4** | 4,0 | 0 |
| Approche à 7 000 UU (7 000, 2 000) | **10** | 16,1 | 0 |

**Chaque direction est couverte par au moins une tourelle**, hors des points au-dessus du trou (le gouffre a ses propres tourelles). Deux zones sont tenues par une seule tourelle à la fois, et des défenses à courte portée la complètent :
- **paliers** : la Heavy de rive de chaque côté. Sur les côtés E0, la Tesla de rive s'y ajoute, et les pics partout. Une tourelle de rive ne voit que son côté du dodécagone : c'est pour cela qu'il y en a une par côté ;
- **poche au pied de la tour** : l'anneau D4 de son côté, plus les 6 Plant X et les 2 Tesla de la tour.

Pour passer à 2 tourelles partout dans ces deux zones, il faudrait 12 tourelles de plus sur la rive et 12 sur la tour, à prendre sur L1. Réglage en tête du script (§3).

Carte complète : `plans/couverture.png` (rouge : moins de 2) et `donnees/05_couverture.csv`.

## 8. Plan de câblage : 2 générateurs Tek

| Source | Position | Rôle | Portée à régler |
|---|---|---|---|
| **Générateur Tek n°2** (mezzanine) | (−900 ; 0), Z1800 | **23 Tek** : L1 entre 2 170 et 3 740 UU, tour D4 entre 1 540 et 3 270 UU, dessus à 2 170 UU | **≥ 3 800 UU** |
| **Générateur Tek n°1** (hall) | (900 ; 1 559), Z0 | réplicateur, forge à vapeur, labo, puis secours | maximum |

- Les **Tek** exigent un générateur Tek.
- Les **Heavy et Tesla** sont électriques. Distances au générateur le plus proche :

| Couche | Distance (UU) |
|---|---|
| Jupe | 2 780 à 5 600 |
| Rive | 2 180 à 4 790 |
| L1 | 2 040 à 3 620 |
| Bord du trou | 1 620 à 3 440 |
| Tour D4 | 1 880 à 3 120 |
| Dessus | 1 530 à 2 650 |

- Le trou coupe la boucle de câbles de la galerie (anneau 8) à l'avant : elle devient un arc ouvert de θ ≈ 205° à 155°.
- Si les sphères ne couvrent pas tout, posez des câbles électriques :
  - boucle sous le plancher Z1800 ;
  - descentes par les cadres du fût ;
  - liaison vers la jupe par la bande sous l'overhang.

  Il faut alors un générateur électrique, absent de votre liste et non compté au module 07.
- Plant X : tuyaux d'eau jusqu'aux carrés de culture (attique, toit de cage, dessus), ou réservoirs.

⚠ Vérifiez en jeu la sphère de portée des générateurs Tek au réglage maximal.

## 9. Réglages et munitions

| Tourelle | Portée | Cibles | Munitions |
|---|---|---|---|
| Heavy | Haute | survivants + créatures apprivoisées non alliées | balles de fusil avancé |
| Tek | Haute | idem | fragments d'élément |
| Tesla | — | idem ; mode brûlure, étourdissement ou vulnérabilité | cristal |
| Plant Species X | — | tout ce qui n'est pas de la tribu | eau + engrais |

## 10. Contrôles

- [ ] 100 emplacements : 52 Heavy, 23 Tek, 10 Tesla, 15 Plant X.
- [ ] Jupe : 11 tournées vers le piton, 5 vers la mer. Rive : 1 Heavy par côté, 5 Tesla (côtés E0).
- [ ] L1 : 26 tourelles, Tek et Heavy alternées autour du cercle ; 27 cadres doubles aux autres positions.
- [ ] Tour D4 : 1 tourelle par côté + 2 Tesla au niveau 8 ; 6 Plant X au pied de la tour.
- [ ] 8 tourelles sur les murs de bord du trou, toutes tournées vers le gouffre.
- [ ] Dessus : 2 Heavy, 2 Tek, 2 Tesla, 4 Plant X, sous le toit en rampes.
- [ ] 79 murs de chaume démolis ; les tourelles et les murs posés au-dessus restent en place.
- [ ] Les 23 Tek sont alimentées par le générateur n°2.
- [ ] Réserve : 28 Heavy, 12 Tek, 0 Tesla ; zone d'exclusion d'environ 50 fondations respectée (le cap de 100 est plein).
