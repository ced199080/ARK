# Module 05 — Plan de câblage et matrice balistique (scénario B : cap 100, Tesla comptées)

Template : `templates/05_tourelles_scenario_B.json` (phase **P7**). Chaque tourelle y est précédée de son **mur de chaume de pose**, à démolir en jeu.
Liste maîtresse : `donnees/05_matrice_tourelles.csv`. Elle donne l'ordre de pose, le type, la couche, les coordonnées du mur de chaume et de la tourelle, et le sens de tir.
Plan : `plans/plan_tourelles.png`.

![Plan des tourelles et câblage](plans/plan_tourelles.png)

## 1. Règle du turret cap

| Paramètre serveur | Valeur officielle documentée | Effet |
|---|---|---|
| `bLimitTurretsInRange` | true | active la limite |
| `LimitTurretsRange` | **10 000 UU** (≈ 33,3 fondations) | rayon de la **sphère** de comptage |
| `LimitTurretsNum` | **100** | tourelles au plus dans la sphère |

- **Ce qui compte** : tourelles auto, Heavy, Tek et Plant Species X.
- **Tesla** : vous avez retenu le scénario B, où **les bobines Tesla comptent**. C'est l'hypothèse prudente.
- **Procédure** : à la pose d'une tourelle T, le jeu compte les tourelles déjà posées à moins de 10 000 UU de T, distance 3D. La pose est refusée si le cap est atteint.

## 2. Le cap est global sur cette base

| Mesure (calculée sur les 100 tourelles posées) | Valeur |
|---|---|
| Distance 3D maximale entre deux tourelles | **9 692 UU** (< 10 000) |
| Rayon horizontal maximal d'une tourelle (jupe) | 4 846 UU |
| Distance minimale d'une tourelle étrangère pour ne compter dans aucune sphère de la base | **14 846 UU ≈ 49,5 fondations du centre** |

- Chaque tourelle voit toutes les autres : **100 tourelles au total**, quelle que soit leur répartition.
- La distribution circonférentielle (§5) ne fait pas gagner de place. Elle garantit une couverture régulière si le cap bloque plus tôt que prévu, par exemple à cause d'une tourelle extérieure.
- Gardez une zone d'exclusion d'environ 50 fondations autour du centre pour toute autre tourelle de votre tribu.

## 3. Scénario B retenu

| | Heavy | Tek | Tesla | Total compté |
|---|---|---|---|---|
| Inventaire | 80 | 35 | 10 | — |
| **Posées** | **55** | **35** | **10** | **100** |
| Réserve (coffre de la mezzanine, ou avant-poste à plus de 50 fondations) | 25 | 0 | 0 | — |

| Couche | Emplacement | Dotation |
|---|---|---|
| **JUPE-int** | sous la jupe, regard vers le piton et le dessous de la plateforme | 18 Heavy |
| **JUPE-ext** | sous la jupe, regard vers la mer | 12 Heavy |
| **L1** | cage, étage 1 (ligne D5) | 35 Tek + 25 Heavy |
| **RIVE** | rive niveau 1 (ligne D7), regard sur la bande décaissée | 10 Tesla |

## 4. Montage vertical : mur de chaume puis tourelle

Toutes les tourelles sont montées comme dans le template fourni *Straight Heavy* (2727) et dans les tours 1201/1809 :
- un **mur de chaume** occupe l'emplacement ;
- la tourelle est fixée sur sa face côté tir, **pivot à 10 UU** du plan du mur, à mi-hauteur ;
- le mur de chaume est **démoli** ensuite.

| Type | pitch | yaw | roll | Référence |
|---|---|---|---|---|
| Heavy, Tek | −89,5° | θ_tir + 90° | −90° | template 2727 (pitch −89,503°, roll −90°) |
| Tesla | 0° | θ_tir + 90° | −90° | Tesla latérales des tours 1201 et 1809 |

θ_tir est la direction du tir : la normale extérieure du côté, ou l'opposé pour les tourelles de jupe tournées vers le piton. Dans le JSON, chaque paire « mur de chaume » + « tourelle » se suit, dans l'ordre de pose.

| Couche | Mur de chaume (Z bas → haut, z template) | Pivot de la tourelle |
|---|---|---|
| L1 | ligne D5 (apothème 2 799,0), Z1800 → 2100, z 2040 | apothème 2 809,0, z 2040 |
| RIVE | ligne D7 (3 918,7), Z300 → 600, z 540 | apothème 3 928,7, z 540 |
| JUPE-ext | sous le mur d'about (4 518,7), suspendu de Z −900 à −600, z −660 | apothème 4 528,7 (vers la mer) |
| JUPE-int | sous la jonction des plafonds s1/s2 (4 818,7), suspendu de Z −900 à −600, z −660 | apothème 4 808,7 (vers le piton) |

Répartition de la jupe :
- côtés pairs (0°, 60°…) : extérieure à t = −600, intérieure à t = 0, extérieure à t = +600 ;
- côtés impairs (30°, 90°…) : intérieures à t = ±600.

⚠ **À valider en solo** :
1. Qu'un mur de chaume s'accroche bien sous un plafond ou sous un mur. C'est le cas de la jupe ; sinon, pose en Template Hammer.
2. Que la tourelle reste en place après démolition du chaume.

## 5. Ordre de pose : distribution circonférentielle

À l'intérieur de chaque priorité, l'ordre suit la suite de van der Corput sur l'angle (0°, 180°, 90°, 270°…) : une pose interrompue reste répartie sur 360°.

| Priorité | Ordres | Contenu | Raison |
|---|---|---|---|
| P1 | 1-30 | 30 Heavy de jupe | seule défense du dessous de la plateforme |
| P2 | 31-65 | 35 Tek en L1 | seule couche qui tire au-dessus de l'horizon (+38°) |
| P3 | 66-75 | 10 Tesla de rive | seule couverture de la bande au pied de la rive |
| P4 | 76-100 | 25 Heavy en L1 | complètent L1 |

**Procédure**
1. Toutes les structures P1 à P6 sont posées.
2. Importez `05_tourelles_scenario_B.json`, ou posez à la main dans l'ordre du CSV : mur de chaume, puis tourelle.
3. Si une pose est refusée **avant** la 100ᵉ, une tourelle étrangère est dans la sphère : cherchez-la dans un rayon de 50 fondations.
4. Contrôle final : 55 + 35 + 10 = 100.
5. Démolissez les 100 murs de chaume.

## 6. Matrice détaillée

L1 : positions p0 à p4 des 5 emplacements du côté, dans le sens des θ croissants. H = Heavy, T = Tek, suivi du n° d'ordre.
Jupe : sens (ext = vers la mer, int = vers le piton) et n° d'ordre, dans l'ordre t = −600 → +600.

| Côté (θ) | L1 p0 | p1 | p2 | p3 | p4 | Jupe |
|---|---|---|---|---|---|---|
| 0° | H79 | T41 | T31 | H76 | T49 | ext 23, int 1, ext 16 |
| 30° | H89 | T40 | T58 | H83 | T36 | int 9, int 24 |
| 60° | H95 | T54 | H80 | T45 | T62 | ext 5, int 20, ext 13 |
| 90° | H92 | T34 | H86 | T52 | T43 | int 28, int 3 |
| 120° | H98 | T60 | H78 | T38 | H91 | ext 18, int 11, ext 26 |
| 150° | T56 | T47 | H85 | T64 | H97 | int 7, int 22 |
| 180° | T33 | T51 | H82 | T42 | H94 | ext 15, int 30, ext 2 |
| 210° | T59 | H88 | T37 | T55 | H100 | int 17, int 10 |
| 240° | T46 | H77 | T63 | T35 | H90 | ext 25, int 6, ext 21 |
| 270° | T53 | H84 | T44 | H96 | T61 | int 14, int 29 |
| 300° | T39 | H81 | T57 | H93 | T48 | ext 4, int 19, ext 12 |
| 330° | T65 | H87 | T32 | H99 | T50 | int 27, int 8 |

Les Tek et les Heavy alternent sur L1 par diffusion d'erreur, avec 5 ou 6 Tek par secteur de 60°.

**Tesla de rive** (ordres 66-75) : θ ≈ 0° (66) · 34,4° (71) · 72,9° (69) · 107,1° (74) · 145,6° (68) · 180° (73) · 214,4° (70) · 252,9° (75) · 287,1° (67) · 325,6° (72).

## 7. Couverture 360° et zones d'ombre

**Azimut.**
- Une tourelle verticale couvre le demi-espace devant sa façade : ≈ 180° en azimut.
- Les 60 tourelles de L1 sont espacées d'environ 6° : une cible lointaine est vue par environ 30 tourelles de L1 à la fois, quel que soit son azimut.

**Site** (coupe au milieu d'un côté, `donnees/synthese.json` → `secteurs`) :

| Couche | Couverture | Limite |
|---|---|---|
| L1 | −49,0° → +38,2° | pente A en bas, bout de casquette en haut |
| JUPE-ext | −89,9° → +17,0° vers la mer | plafond de jupe au-dessus |
| JUPE-int | −89,9° → +37,2° vers le piton et le dessous de la plateforme | plafond de jupe ; la sous-face de la plateforme n'est pas modélisée |
| Tesla | toute la bande décaissée, de 3 919 à 4 479 UU | poche fermée : toit au-dessus, bande au-dessous |

**Zones d'ombre traitées**
- **Pied de rive** (bande décaissée) : invisible pour L1 et la jupe ; couvert par les 10 Tesla et les 84 pics.
- **Dessous de la plateforme** : 18 Heavy tournées vers le piton, 1 à 2 par côté. ⚠ Elles doivent être plus basses que la sous-face de la plateforme : mesurez son épaisseur en solo.
- **Mer au pied du piton** : 12 Heavy tournées vers l'extérieur, plus L1 jusqu'à −49°.
- **Ciel au-dessus de +38°** : non couvert. La glisse en toits rend les largages inefficaces (module 03 §7).

## 8. Plan de câblage (alimentation)

| Source | Position | Alimente | Portée minimale |
|---|---|---|---|
| **Tek Generator galerie n°1, n°2, n°3** | anneau 8 à Z1800, θ 90° (0 ; 2 389,2), 210° (−2 069,1 ; −1 194,6) et 330° (2 069,1 ; −1 194,6) | Tek et Heavy de L1, par secteur de 120° | ≈ 2 600 UU ; ≈ 3 900 UU pour que les secteurs se recouvrent |
| Tek Generator ateliers | hall, θ 60° | labo, Tek Teleporter | — |
| **Générateur électrique de secours n°1 / n°2** | attique A, entre le fût et la colonnade : θ 80° et 260°, rayon 3 050, Z0 | Tesla de rive, jupe ; cage si un Tek Generator tombe | — |

- **Tek** : elles exigent l'alimentation d'un **Tek Generator**.
- **Heavy et Tesla** : électriques. Le câblage suit ce tracé :
  - boucle de câbles sous le plancher Z1800, le long de l'anneau 8 ;
  - 12 descentes, une par arête, dans l'attique A ;
  - accès à l'anneau extérieur de l'attique (Tesla) par les 2 passages de la colonnade, à 90° et 270° ;
  - vers la jupe : sas à 270°, puis la bande sous l'overhang, puis le caisson de jupe ; environ 3 300 UU de câble.
- ⚠ Vérifiez en jeu :
  - la portée réelle des Tek Generators (affichez la sphère) ;
  - le besoin électrique de la Tesla.

## 9. Réglages et munitions

| Tourelle | Portée | Cibles | Munitions |
|---|---|---|---|
| Heavy | Haute | survivants + créatures apprivoisées non alliées | balles de fusil avancé |
| Tek | Haute | idem | fragments d'élément |
| Tesla | — | idem ; mode brûlure, étourdissement ou vulnérabilité | cristal |

En stock dans le coffre de la mezzanine : 25 Heavy de réserve, munitions, élément pour les 4 Tek Generators, essence pour les 2 générateurs de secours.

## 10. Contrôles de fin de module

- [ ] 100 tourelles posées : 55 Heavy, 35 Tek, 10 Tesla. Le cap n'a pas bloqué avant la 100ᵉ.
- [ ] Chaque tourelle tire vers l'extérieur ; les 18 de jupe « int » tirent vers le piton.
- [ ] 100 murs de chaume démolis ; les tourelles restent en place.
- [ ] Toutes les tourelles alimentées.
- [ ] 25 Heavy en réserve ; zone d'exclusion d'environ 50 fondations respectée.
