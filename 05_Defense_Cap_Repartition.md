# Module 05 — Plan de câblage et matrice balistique (Heavy / Tek / Tesla, turret cap)

Templates :
- `templates/05_tourelles_scenario_A.json` (cap 100, Tesla non comptées) ;
- `templates/05_tourelles_scenario_B.json` (cap 100, Tesla comptées) ;
- `templates/05_tourelles_scenario_C.json` (cap ≥ 125).

Liste maîtresse : `donnees/05_matrice_tourelles.csv`, avec les 125 emplacements, l'ordre de pose et la colonne oui/réserve de chaque scénario. Plan : `plans/plan_tourelles.png`.

![Plan des tourelles et câblage](plans/plan_tourelles.png)

## 1. Règle du turret cap

| Paramètre serveur | Valeur officielle documentée | Effet |
|---|---|---|
| `bLimitTurretsInRange` | true | active la limite |
| `LimitTurretsRange` | **10 000 UU** (≈ 33,3 fondations) | rayon de la **sphère** de comptage |
| `LimitTurretsNum` | **100** | tourelles au plus dans la sphère |

- **Ce qui compte** : tourelles auto, Heavy, Tek et Plant Species X.
- **Bobine Tesla** : ajoutée à ASA au patch 52.5 ; aucune source ne dit si elle compte. ⚠ Testez en solo, ce qui décide entre le scénario A et le scénario B.
- **Procédure de calcul** (règle documentée sur ASE et reprise par ASA ; à confirmer sur votre serveur) : à la pose d'une tourelle T, le jeu compte les tourelles existantes à moins de 10 000 UU de T, distance 3D. Si ce nombre atteint le cap, la pose est refusée.

## 2. Pourquoi le cap est global sur cette base

Le script calcule toutes les distances entre les 125 emplacements :

| Mesure | Valeur |
|---|---|
| Distance 3D maximale entre deux emplacements | **9 414 UU** (< 10 000) |
| Rayon horizontal maximal d'un emplacement (jupe) | 4 707 UU |
| Distance minimale d'une tourelle étrangère pour ne compter dans aucune sphère de la base (même altitude) | **14 707 UU ≈ 49 fondations du centre** |

**Conséquences**
1. Chaque tourelle de la forteresse est dans la sphère de toutes les autres : **on ne peut pas dépasser 100 tourelles comptées**, quelle que soit leur répartition.
2. « Étirer » les tourelles sur les cadres périphériques ne crée pas de place. Cela sert à deux choses :
   - éviter qu'une tourelle **extérieure** (avant-poste, alliés, tour voisine) mange le quota d'un seul secteur ;
   - si la pose est interrompue (cap atteint plus tôt que prévu), garder une couverture régulière : d'où l'ordre de pose du §5.
3. **Zone d'exclusion.** Aucune autre tourelle de votre tribu à moins de **≈ 49 fondations du centre** à la même altitude. Selon la configuration du serveur, des tourelles d'autres tribus peuvent aussi compter : posez la défense complète avant d'être encerclé.
4. **Les Heavy en surplus** (15 en A, 25 en B) vont au coffre de la mezzanine comme **stock de remplacement**, ou sur un avant-poste à plus de 49 fondations.

## 3. Scénarios

| Scénario | Réglage | Heavy | Tek | Tesla | Posées par couche (Jupe / L1 / L2 / Rive) | Réserve |
|---|---|---|---|---|---|---|
| **A** | cap 100, Tesla non comptées | **65** | **35** | **10** | 24 / 60 / 16 / 10 | 15 Heavy |
| **B** | cap 100, Tesla comptées | **55** | **35** | **10** | 24 / 60 / 6 / 10 | 25 Heavy |
| **C** | cap ≥ 125 (serveur modifié) | **80** | **35** | **10** | 24 / 60 / 31 / 10 | 0 |

Avec `--debord 1`, la jupe n'est pas construite : avec un seul rang dans le vide, la chute passerait à 150 UU des tourelles suspendues. Les 24 Heavy de jupe passent alors en L2, et **le dessous de la plateforme n'est plus couvert**. C'est pourquoi `--debord 2` est le réglage par défaut.

## 4. Couches de défense (répartition géométrique)

| Couche | Emplacement | Montage | Dotation | Zone couverte, sans équivalent ailleurs |
|---|---|---|---|---|
| **JUPE** | Sous les plafonds s1 de la jupe : apothème 4 668,7, Z −600, 2 par côté (t = ±600, soit θ du côté ± 7,32°) | Suspendue : z template −510, roll 180° | 24 Heavy | **Dessous de la plateforme**, flancs du piton, surface de la mer, chute en sortie d'overhang |
| **L1** | Cage étage 1 : sièges de l'anneau 9 à Z1800 | Debout : z 1900 | 35 Tek + 25 Heavy | Horizon et volants en approche (jusqu'à +27,2° de site), loin au sol et en mer |
| **L2** | Cage étage 2 : Z2100 | Debout : z 2200 | 31 Heavy au plus (16 en A, 6 en B) | Tir plongeant de −19,0° à −49,9° : fente de tir, zone de chute devant la cage, mer proche |
| **RIVE** | 150 UU derrière les 10 murs-fenêtres de la rive : apothème 3 768,7, Z0 | Debout : z 100 | 10 Tesla | **Bande décaissée au pied de la rive**, angle mort de toutes les tourelles (avec les pics) |

Les Tek sont en L1 : c'est la seule couche qui tire au-dessus de l'horizon, et leur allonge y est la plus utile. Les Heavy de L2 saturent la fente et la zone de chute.

## 5. Ordre de pose : procédure de distribution circonférentielle

Les tourelles sont posées par **priorité**. À l'intérieur de chaque priorité, l'ordre suit la suite de van der Corput sur l'angle : 0°, 180°, 90°, 270°, 45°… Ainsi, une pose interrompue à n'importe quel moment reste répartie sur 360°.

| Priorité | Ordres | Contenu | Raison |
|---|---|---|---|
| P1 | 1-24 | 24 Heavy de jupe | seule défense du dessous de la plateforme, dont la perte ferait tomber toute la base |
| P2 | 25-59 | 35 Tek en L1 | anti-aérien et longue portée |
| P3 | 60-69 | 10 Tesla de rive | seule couverture de la bande au pied du mur |
| P4 | 70-94 | 25 Heavy en L1 | complète L1 (5 tourelles par côté) |
| P5 | 95-125 | 31 Heavy en L2 | jusqu'au cap : 95-110 en A, 95-100 en B, 95-125 en C |

**Procédure en jeu**
1. Posez toutes les structures (P1 à P6 de la notice) **avant** la première tourelle.
2. Importez le template du scénario. En pose manuelle, suivez la colonne `ordre` du CSV.
3. Si une pose est refusée **avant** le rang attendu (101 en A, 91 en B), une tourelle étrangère est dans la sphère :
   - relevez-la (rayon ≈ 49 fondations autour du centre) ;
   - ou basculez sur le scénario inférieur. Les places déjà posées restent valables : chaque scénario est un préfixe de l'ordre de pose.
4. Comptez une fois à la fin : `heavy + tek (+ tesla si comptées) = 100`.

## 6. Matrice détaillée de la cage (L1 / L2)

Notation : H = Heavy, T = Tek, suivi du n° d'ordre de pose. L2 : entre parenthèses, les scénarios où la tourelle est posée ; « · » = niche vide (porte double).
Positions p0 à p4 : les 5 cadres du côté, dans le sens des θ croissants. Coordonnées : module 04 §5 et CSV.

| Côté (θ) | L1 p0 | p1 | p2 | p3 | p4 | L2 p0 | p1 | p2 | p3 | p4 |
|---|---|---|---|---|---|---|---|---|---|---|
| 0° | H73 | T35 | T25 | H70 | T43 | H110 (A,C) | · | H95 (A,B,C) | H111 (C) | · |
| 30° | H83 | T34 | T52 | H77 | T30 | H103 (A,C) | · | H119 (C) | · | H99 (A,B,C) |
| 60° | H89 | T48 | H74 | T39 | T56 | · | H115 (C) | · | H107 (A,C) | · |
| 90° | H86 | T28 | H80 | T46 | T37 | H123 (C) | · | H97 (A,B,C) | · | H113 (C) |
| 120° | H92 | T54 | H72 | T32 | H85 | · | H105 (A,C) | · | H121 (C) | · |
| 150° | T50 | T41 | H79 | T58 | H91 | H101 (A,C) | · | H117 (C) | · | H109 (A,C) |
| 180° | T27 | T45 | H76 | T36 | H88 | · | H125 (C) | H96 (A,B,C) | · | H112 (C) |
| 210° | T53 | H82 | T31 | T49 | H94 | · | H104 (A,C) | · | H120 (C) | · |
| 240° | T40 | H71 | T57 | T29 | H84 | H100 (A,B,C) | · | H116 (C) | · | H108 (A,C) |
| 270° | T47 | H78 | T38 | H90 | T55 | · | H124 (C) | · | H98 (A,B,C) | · |
| 300° | T33 | H75 | T51 | H87 | T42 | H114 (C) | · | H106 (A,C) | · | H122 (C) |
| 330° | T59 | H81 | T26 | H93 | T44 | · | H102 (A,C) | · | H118 (C) | · |

L1 alterne les Tek et les Heavy par diffusion d'erreur : jamais plus de 2 Tek consécutives. Chaque secteur de 60° contient 5 ou 6 Tek et 4 ou 5 Heavy.

**Jupe** (24 Heavy, ordres 1-24) : 2 par côté, θ = 30°·k ± 7,32°.
**Tesla** (ordres 60-69) : θ ≈ 0° · 34,6° · 73,4° · 106,6° · 145,5° · 180° · 214,6° · 253,4° · 286,6° · 325,5°.

## 7. Couverture 360° et zones d'ombre

**Couverture en azimut.** Chaque niche couvre ≈ 130° avec le recul par défaut de 50 UU, et ≈ 180° au nu du cadre (module 04 §5). Les sièges sont espacés de ≈ 6° en L1 et en L2, et de 15° en moyenne dans la jupe. Une cible lointaine est donc vue par ≈ 20 tourelles de L1 à la fois, quel que soit son azimut : pas de trou en azimut.

**Couverture en site** (coupe au milieu d'un côté, `donnees/synthese.json` → `secteurs`) :

| Couche | Site min → max | Ce qui n'est pas vu | Qui le couvre |
|---|---|---|---|
| L1 | −46,7° → +27,2° | le ciel au-dessus de +27,2° ; la bande sous l'overhang | volants hauts : la glisse les rend inoffensifs (§ module 03) ; bande : Tesla + pics |
| L2 | −49,9° → −19,0° | tout ce qui est au-dessus de −19° | L1 |
| Jupe | −90° → +14,9° vers l'extérieur ; dessous de la plateforme vers l'intérieur | la toiture (masquée par l'overhang) | L1 et L2 |
| Rive (Tesla) | portée de la bobine depuis l'embrasure | — | — |

**Dessous de la plateforme (« sans zone d'ombre »)**
- Les tourelles de jupe pendent sous Z −600, 190 UU au-delà du bord de plateforme. Elles voient :
  - vers le bas, la mer et le pied du piton, jusqu'à la verticale ;
  - vers l'intérieur, la sous-face de la plateforme, à condition que celle-ci soit au-dessus de Z −600.
- Tous les 15° en moyenne, une tourelle de jupe couvre la sous-face, en croisant ses tirs avec celle du côté opposé.
- ⚠ Mesurez en solo l'épaisseur réelle de votre Metal Cliff Platform. Si sa sous-face descend sous Z −600, relevez la jupe ou ajoutez une couronne de tourelles suspendues sous la plateforme (hors cap : non prévu).

## 8. Plan de câblage (alimentation)

| Source | Position | Alimente | Portée minimale à régler |
|---|---|---|---|
| **Tek Generator galerie n°1** | anneau 8, θ 90° : (0 ; 2 389,2), Z1800 | Tek de L1 et Heavy de L1/L2, secteur 30°-150° | ≈ 2 600 UU (≈ 9 fondations), pour la tourelle la plus éloignée du secteur |
| **Tek Generator galerie n°2** | θ 210° : (−2 069,1 ; −1 194,6), Z1800 | secteur 150°-270° | idem |
| **Tek Generator galerie n°3** | θ 330° : (2 069,1 ; −1 194,6), Z1800 | secteur 270°-30° | idem |
| Tek Generator ateliers | hall, θ 60° : (900 ; 1 558,8), Z0 | labo de chimie, Tek Teleporter, éclairage | — |
| **Générateur électrique de secours n°1 / n°2** | attique A, θ 90° et 270° : (0 ; ±3 249), Z0 | Tesla de rive ; jupe et cage si un Tek Generator tombe | — |

- **Tek turrets** : elles exigent l'alimentation d'un **Tek Generator** (élément). Les 3 générateurs de galerie se recouvrent : la perte de l'un d'eux ne coupe aucune Tek si leur portée atteint ≈ 3 900 UU.
- **Heavy et Tesla** : électriques. Elles sont alimentées par les Tek Generators s'ils sont à portée, et sinon par câble :
  - **boucle de galerie** : câbles sous le plancher Z1800, le long de l'anneau 8 (tracé pointillé sur le plan) ;
  - **12 descentes**, une par arête, dans l'attique A jusqu'à la rive (Tesla) ;
  - vers la jupe, passage par le sas (θ 270°), sous l'overhang le long de la bande, puis boucle dans le caisson de jupe. Comptez 3 300 UU de câble entre la galerie et une tourelle de jupe.
- ⚠ **À vérifier en jeu.**
  - Le rayon réel des Tek Generators au réglage maximal : affichez la sphère.
  - Le besoin électrique de la Tesla : wikily.gg indique une alimentation et des munitions en cristal.
  - Si la sphère d'un Tek Generator de galerie n'atteint pas la jupe (≈ 3 300 UU en 3D), le câble devient l'alimentation principale de la jupe.

## 9. Réglages et munitions

| Tourelle | Portée | Cibles | Munitions | Remarque |
|---|---|---|---|---|
| Heavy | Haute | survivants + créatures apprivoisées non alliées (+ sauvages si la zone est infestée) | balles de fusil avancé | jupe et L2 : tir rapproché sur ce qui tombe |
| Tek | Haute | idem | fragments d'élément | L1 : allonge et anti-volant |
| Tesla | — | idem ; mode à choisir parmi brûlure, étourdissement et vulnérabilité (wikily.gg) | cristal | l'étourdissement immobilise les assaillants dans les pics |

Gardez au coffre de la mezzanine : les tourelles de réserve, des munitions pour un rechargement complet de chaque couche, de l'élément pour les 4 Tek Generators, et de l'essence pour les 2 générateurs de secours.

## 10. Contrôles de fin de module

- [ ] Nombre de tourelles posées conforme au scénario. Le compteur du cap n'a pas bloqué avant le rang prévu.
- [ ] Chaque Tek alimentée (voyant actif). Heavy et Tesla alimentées.
- [ ] Les 24 tourelles de jupe pendent sous les plafonds s1, avec le canon sous la sous-face de la plateforme.
- [ ] Les niches vides de L2 sont fermées par des portes doubles.
- [ ] Les tourelles de réserve sont stockées et la zone d'exclusion de 49 fondations est respectée.
