# Module 08 — Revue de constructibilité

Cette revue répond à quatre questions :
- les plans se posent-ils en jeu, dans l'ordre, sans pièce posée avant ce qui la porte ?
- les rampes ont-elles de quoi les tenir, et tiennent-elles encore si un appui est détruit ?
- a-t-on oublié des murs de chaume à démolir ?
- le toit calé sur un mur de D4 reste-t-il bon si la tour est rehaussée ?

Elle compare les plans aux templates que vous m'avez donnés (zip *Construction ARK*) et contrôle chaque pièce des 11 plans.

Ces contrôles font partie du générateur. À chaque régénération, il refuse d'écrire les plans si l'un de ces cas se présente :
- une pièce entre dans une autre ;
- une rampe n'est pas tenue ;
- une pièce passe avant ce qui la porte ;
- un plan dépasse 2 000 entrées.

## 1. Verdict

| Question | Résultat |
|---|---|
| **Rampes non posées dans le secteur d'essai** | **Corrigé d'après 3 essais en jeu** (§3.1). Une lame ne tient qu'à la tête d'un poteau de piliers fins posé sur un coin de fondation ou de plafond, ou au centre d'une fondation carrée ; ni le haut d'un mur ni un pilier dans un joint ne la tiennent. Chaque ligne est placée pour que ses jonctions tombent sur ces points, et tient sur ses poteaux |
| Collisions entre pièces | **0 sur 4 998 pièces** (les 11 plans, colonnade comprise), sans aucun contact admis (§5). Tour rehaussée d'un niveau : **0 sur 5 074 pièces** |
| Rampes tenues | **Oui** : 668 rampes sur 165 lignes, 193 poteaux ; 3 lames pendues au plus sous un poteau, 6 au plus au-dessus (§3) |
| Rampes qui tiennent si un poteau est détruit | **En partie** : 28 lignes ont 2 poteaux (toit 114 lames sur 164, pente A 12 sur 215). Les autres n'ont qu'un point de pose possible sous leurs jonctions : si leur poteau est détruit, elles tombent (§3.3) |
| Ordre de pose | Plan après plan, chaque pièce après ce qui la porte : aucun plan ne s'appuie sur un plan posé plus tard (§6) |
| Taille des plans | 11 à 1 201 entrées, sous la limite de 2 000 |
| Murs de chaume | **79**, un par tourelle verticale, listés dans `donnees/08_chaume_a_demolir.csv`. Ils sont dans les plans de zone, à leur place dans les murs. Rien d'autre n'est en chaume, et rien ne repose sur du chaume seul (§4) |

## 2. Comparaison avec vos templates

| Template | Ce qu'il montre | Ce que les plans en reprennent |
|---|---|---|
| **481** *Large.Plat.Base* (SkunkHD) | Étoile de fondations carrés + triangles | Le pavage, pièce pour pièce (`--verifier-481`) |
| **1201** *100 turret 11x11* (P1agueTV) | **873 cadres de porte doubles** comme murs ; toit à 2 pans en lignes de rampes inclinées ; chaque ligne part d'un pilier fin sur l'égout, monte librement de 5 lames sur un pan, finit sur un pilier fin de faîtage sur l'autre | Cadres doubles partout sauf la tour du pod. Position des rampes : pivot au milieu, z = bas + 290, yaw = θ − 90°. Règles d'appui (§3) |
| **1809** *merry chistmas* (IchmagPizza) | **802 cadres doubles** ; rampes en lignes sur les joints des murs, poutres fines d'égout, pilier fin de faîtage, 6 lames libres sur un pan ; 86 murs de chaume dont **78 portent un cadre de porte** | Lignes de lames au pas de 300 UU, 6 lames libres au plus au-dessus d'un appui, 7 entre deux appuis. Cadre double posé sur le chaume de L1 et de la rive, comme sur la tour |
| **1584** *Small PvP Tower* | Tour à étages, **19 grands carrés de culture** (Plant X) sur les planchers et les toits, tourelles autour | Carrés de culture de Plant X : pivot 10 UU au-dessus du plancher (`CropPlotLarge_SM`, et `CropPlotMedium_SM` dans la poche du toit de cage) |
| **2727** *Straight Heavy* | 1 mur de chaume + 1 Heavy, pivot 10 UU devant le mur, pitch −89,5°, roll −90° | Identique pour les 71 Heavy et Tek verticales et les 8 Tesla sur chaume, toutes au-dessus de Z0 |
| **2901 / 2902 / 2903** (mho) | Pile de 2 demi-piliers z 15 / 165, `snapOverrides [0, 1]` | Pile d'ancrage du plan 1, 1 demi-pilier z 315 sur les plans 2 à 8 |
| **704 / 701** | Cercles de piliers, 1 rang | Colonnade, en option (plan 2) |

## 3. Appuis des rampes

### 3.1 Ce qui tient une lame : 3 essais en jeu

Le relevé des tours 1201 et 1809 ne suffisait pas : dans le secteur d'essai, aucune rampe ne s'est posée. Trois essais courts en solo (`templates/test/Essai_rampes*.json`) ont donné les règles :

| Essai | Cas | Se pose ? |
|---|---|---|
| 1 | V1, V3 : poteau de piliers fins sur un coin de fondation, lames accrochées à sa tête | **oui** |
| 1 | V0 : pilier fin dans le joint d'un mur + poutre fine, sans poteau | non |
| 1 | V2 : poteau à 40 UU d'une arête | non |
| 2 | E5 : poteau sur un coin de fondation, lame qui monte depuis sa tête | **oui** |
| 2 | E1, E2, E4 : haut d'un mur, pilier fin dans le joint posé sur le mur du dessous | non |
| 2 | E3 : pilier fin debout sur le haut du mur (tour 1201) | non |
| 3 | G1 : **3 lames pendues à la suite** sous un poteau | **oui** |
| 3 | G3 : poteau sur la **pointe d'une fondation triangle** | **oui** |
| 3 | G4 : poteau sur un **coin de plafond** (sans pilier dessous) | **oui** |
| 3 | G7 : poteau au **centre d'une fondation** | **oui** |
| 3 | G8 : lame **pendue** à la tête d'un poteau | **oui** |
| 3 | G2 : poteau terminé par un **demi-pilier fin** | non (pas de lame) |
| 3 | G5 : colonne de piliers fins **dans le joint d'un mur**, depuis la fondation | non (pas de lame) |
| 3 | G6 : poteau au **milieu d'une arête** | non (le pilier fin ne se pose pas) |
| 3 | G9 : lame sur le **bord d'un plafond** | non |

**Règles du générateur** :
1. Une **ligne** est une file de lames bout à bout, au pas de 300 UU ; ses lames s'enchaînent.
2. Elle tient sur des **poteaux** : des **piliers fins entiers** (pas de demi-pilier fin), debout sur la surface juste dessous, sur un **coin de fondation** (carrée ou triangle), le **centre d'une fondation carrée** ou un **coin de plafond**, sans toucher un mur ni une autre pièce. Leur tête est une jonction de la ligne.
3. Une lame tient entre deux poteaux (**7 lames** au plus, tour 1809), pendue sous un poteau (**3 lames** au plus, essai G1) ou au-dessus du dernier (**6 lames** au plus, tours 1201 et 1809).
4. Rien d'autre n'est un appui : ni le haut d'un mur, ni le bord d'un plancher, ni un pilier dans un joint, ni le chaume.
5. Template Hammer **saute** une pièce qui n'a pas d'appui, mais **s'arrête** sur une pièce gênée par un obstacle (relief, structure déjà là) : c'est ce qui a arrêté le 2ᵉ essai, et sans doute le secteur à 677.

### 3.2 Placement des lignes et des poteaux (`consolider_rampes`)

Les rampes forment 3 **nappes** à 45° : rampes extérieures (pente A, overhang, débord), casquette et appentis, toit du pod. Pour chaque côté de chaque nappe, le générateur :
- essaie deux positions de lignes (t = 0, ±300… ou t = ±150, ±450…) ;
- pour chaque ligne, essaie les décalages s de 0 à 300 UU vers l'extérieur (donc vers le haut) qui font tomber une jonction au-dessus d'un point de pose ;
- garde, par ligne, le décalage qui tient le plus de lames (puis celui qui donne 2 poteaux), et par côté la position qui tient le plus de lames ;
- retire les lames qui se croisent aux arêtes du dodécagone, en coupant la ligne qui en perd le moins ;
- choisit les poteaux de chaque ligne : le jeu le plus léger qui la tient ; en mode `stable` (défaut), d'abord le plus léger qui la tient encore si l'un d'eux est détruit, quand il en existe un. `--appuis tours` : le jeu le plus léger ; `--appuis prudent` : stable, et 1 lame au plus au-dessus du dernier poteau.

### 3.3 Résultat, nappe par nappe

| Nappe | Plan | Lignes | Rampes | Poteaux | Lames qui tiennent si un poteau est détruit |
|---|---|---|---|---|---|
| Rampes extérieures (pente A, overhang, débord) | 4 | 75 | **388** (215 + 133 + 40) | **79** (210 piliers fins) : 2 piliers au centre d'une fondation du palier 2, ou 3 à 4 piliers sur un coin de fondation de l'attique | 12 |
| Casquette et appentis | 6 | 58 | **116** | **58** (202 piliers fins) : 1 pilier sur un coin du toit de cage, ou 7 piliers sur un coin de fondation de l'attique | 0 |
| Toit du pod | 10 | 32 | **164** | **56** (96 piliers fins) sur des coins du plancher de toit | 114 |
| **Total** | | **165** | **668** | **193** (508 piliers fins) | |

Avant ce correctif, il y avait 777 rampes, mais aucune ne pouvait se poser. Les lignes perdues sont celles qui n'ont aucun point de pose sous leurs jonctions ; la casquette du trou est supprimée pour cette raison.

Le contrôle `verifier_appuis` reprend chaque rampe des plans, sans se servir de la façon dont elles ont été générées : aucune rampe sans appui, au plus 1 lame entre deux poteaux, 289 lames pendues sous un poteau (3 au plus), 6 lames au plus au-dessus du dernier poteau. Plans : `plans/plan_rampes.png` et `plans/coupe_radiale.png` (la coupe trace les nappes sans le décalage des lignes).

## 4. Murs de chaume à démolir en jeu

Liste complète, dans l'ordre de pose des tourelles : `donnees/08_chaume_a_demolir.csv`. Elle donne le plan, le n° d'entrée dans le JSON, la tourelle portée et ce qui est posé au-dessus.

**Nouveau : les murs de chaume sont dans les plans de zone**, à leur place dans la colonne de murs. Ce qui est posé au-dessus tient donc dès la pose de la zone. La tourelle se pose ensuite, avec le plan de défense, sur son mur de chaume déjà en place.

| Plan | Couche | Murs de chaume | Au-dessus du chaume | Après démolition |
|---|---|---|---|---|
| 3 | RIVE (niveau 1) | 16 | rien | ouverture de 300 × 300, la tourelle au nu du mur |
| 3 | RIVE (niveau 0) | 11 | le cadre double du niveau 1 | tenu par ses voisins, comme les cadres de la tour 1809 |
| 4 | TROU (murs de bord, niveau 0 ou 1) | 3 | les cadres doubles du mur de bord | **un seul chaume par colonne** |
| 5 | D4, TROU-D4 et TROU-L1 (tour et murs de bord du pod) | 13 + 1 + 2 | un mur plein de la tour, de la couronne ou de la rehausse | tenu par ses voisins |
| 6 | L1 et TROU-L1 | 31 + 2 | un cadre double L2 ou un cadre de bord | tenu par ses voisins et le plancher de galerie Z2100 |
| **Total** | | **79** | | |

- **Rien d'autre n'est en chaume.** Le contrôle des appuis ne compte jamais le chaume : aucune rampe, aucun poteau, aucune poutre ne dépend d'un mur de chaume.
- Démolissez les murs de chaume **après** la pose de leur tourelle. Testez d'abord sur une seule tourelle que celle-ci et ce qui est posé au-dessus restent en place.

## 5. Collisions

**Méthode.** Le générateur donne à chaque pièce un volume :
- mur ou cadre 300 × 300 × 20 ;
- pilier 40 × 40, pilier fin 20 × 20 ;
- plafond 15 d'épaisseur ;
- rampe : lame de 10 × 100 au-dessus de sa ligne de base ;
- tourelle : bloc devant son mur de chaume, ou debout sur son plancher ;
- carré de culture : 300 × 300 × 60 (grand), 220 × 220 × 60 (moyen).

Il donne aussi à chaque pièce un **noyau** : son volume sans les bords qui se touchent normalement au snap (arêtes de plancher, bouts de mur, tête et flancs de pilier, bouts de lame). Deux pièces sont **en collision** quand le noyau de l'une entre dans le volume de l'autre : c'est le cas que le jeu refuse (« obstrué »). Les poteaux des rampes, qui ne se snappent qu'à leur point de pose, sont contrôlés de tout leur volume (§3.2).

**Résultat : 0 collision sur 4 998 pièces**, colonnade comprise, sans contact admis. Les poteaux sont contrôlés de tout leur volume : ils ne touchent ni mur, ni pilier, ni tourelle, ni carré de culture, ni lame d'une autre ligne. Les cages du noyau (module 02 §6.1) n'entrent ni dans la colonne d'escaliers ni dans les piliers PB, qui sont à leurs coins.

⚠ Les dimensions sont des hypothèses, à ± 10-20 UU des formes réelles du jeu. Le contrôle garantit qu'aucune pièce n'en traverse franchement une autre, pas que le jeu accepte chaque contact.

## 6. Ordre de pose et plans calés sur un mur

**Plan après plan.** Le générateur déduit de la géométrie ce qui porte chaque pièce (`porteurs()`) :
- le mur du dessous ;
- l'arête d'un plancher ;
- la tête d'un pilier ;
- le haut d'un mur sous le bout d'une lame ;
- le mur de chaume d'une tourelle.

Il ne retient que les porteurs posés dans le même plan ou dans un plan précédent, puis range chaque plan du bas vers le haut, chaque pièce après ses porteurs. Une pièce sans porteur posé avant elle arrête le script.

**Plans calés sur un mur de D4** (toiture pleine, toit en rampes, tourelles du dessus, rehausse) :
- leur pièce de référence est un mur de D4 qui se snappe sur le haut de la tour ;
- les murs A, B et C sont 3 places distinctes de la couronne. La toiture pleine laisse B et C vides, et les plans 11 et 10 les remplissent : aucun plan n'en recouvre un autre ;
- **tour rehaussée** : le générateur ajoute la rehausse et monte les plans 9 à 11 de 300 UU, puis refait les contrôles. Résultat : 0 collision, appuis bons, ordre de pose bon.

## 7. Ce que je ne peux pas vérifier d'ici : essai en solo

| Point | Pourquoi c'est incertain | Repli |
|---|---|---|
| Template Hammer pose-t-il une pièce qui en touche une autre, ou sans snap ? | Aucune documentation sur son comportement. Les templates fournis ont été construits en jeu, puis exportés | Poser le plan concerné en premier ; ou à la main |
| Le mur de référence se snappe sur le haut du mur de la tour | Pose d'un template sur un mur existant, à valider | Poser le mur de référence à la main, puis le template en placement libre |
| Une tourelle se fixe sur un mur de chaume posé par un autre plan | Les templates fournis posent le chaume et la tourelle ensemble | Poser les deux à la main avec le template 2727 |
| La boîte de munitions (pièce récente) : chemin de classe, coût, portée réelle | Pas dans les templates fournis ni dans les sources consultées | Elle n'est pas dans les plans : posez-la à la main dans sa cage |
| Les tourelles et les murs posés au-dessus restent en place après la démolition du chaume | Comportement de la tour 1809 et du template 2727 | Laisser le chaume |
| Un carré de culture se pose sur un plafond métal et une graine de Plant X y pousse | La tour 1584 en pose sur des plafonds et des toits en pierre | Grand carré de culture posé à la main |

**Essai court des départs de ligne :** `templates/test/Essai_rampes.json`, 50 entrées, à poser sur un sol plat (pas de pile d'ancrage). Il compare 4 façons de faire partir une ligne (`donnees/08_essai_rampes.csv` donne le n° de chaque entrée) :

| Variante | Entrées | Départ de la ligne | Attendu |
|---|---|---|---|
| V0 | 0 à 12 | copie de la tour 1809 : pilier fin dans le joint, poutre fine sous la 1re lame | se pose |
| V1 | 13 à 27 | **générateur** : pilier fin dans le joint, poteau sous la jonction 1 | se pose |
| V2 | 28 à 35 | poteau de piliers fins posé librement sur une fondation, à 40 UU d'une arête (comme certains poteaux de la pente A) | à vérifier |
| V3 | 36 à 49 | ancien départ, sur le haut des cadres sans pilier fin | ne se pose pas |

**Résultat en jeu** (de gauche à droite en regardant vers le haut des rampes : V0, V1, V2, V3) : **V1 et V3 se posent entièrement, V0 et V2 non.**
- Ce qui fait tenir les lames, c'est le **poteau de piliers fins debout sur un coin de fondation** sous la jonction 1 (V1 et V3) ; la lame r0 pend de sa tête, la lame pendante et r1 s'enchaînent.
- Le pilier fin dans le joint ne suffit pas seul (V0, qui n'a pas de poteau) ; le haut d'un mur non plus.
- Un poteau qui n'est pas sur un point de snap ne porte rien (V2).
- Conséquence : beaucoup de poteaux du générateur sont à 40 UU d'une arête (pente A sur les côtés E1, overhang sur le palier 2, toit), et le débord et la casquette n'ont aucun poteau. Avant de les replacer, le 2ᵉ essai dit précisément où un poteau peut se poser et ce qui porte une lame.

**2ᵉ essai :** `templates/test/Essai_rampes_2.json`, 118 entrées (`donnees/08_essai_rampes_2.csv`). 9 cas isolés, de gauche à droite en regardant vers le haut des rampes ; au coin arrière gauche de chaque cas, une pile de n demi-piliers métal donne son numéro :

| Cas | Ce qui est testé |
|---|---|
| E1 | pilier fin dans le joint d'un mur (tête au haut du mur), 1 lame montante |
| E2 | pilier fin dans le joint, 1 lame pendante vers l'extérieur |
| E3 | pilier fin debout **sur** le haut du mur, au joint (tour 1201), 1 lame pendue à sa tête et 1 montante |
| E4 | haut du mur seul, au joint, 1 lame montante |
| E5 | poteau d'1 pilier fin sur un coin de fondation, 1 lame montante depuis sa tête |
| E6 | poteau de 2 piliers fins sur un coin de fondation, 1 lame pendue à sa tête |
| E7 | poteau de 2 piliers fins au milieu d'une arête de fondation, 1 lame montante |
| E8 | poteau de 2 piliers fins au centre d'une fondation, 1 lame montante |
| E9 | poteau de 2 piliers fins à 40 UU d'une arête, sans lame : le poteau seul se pose-t-il ? |

**Résultat en jeu** : E1 à E4 incomplets, E5 complet ; la pose s'est **arrêtée** sur la 3ᵉ fondation de E6, à 45 m du début d'un essai de 76 m de long, très probablement sur le relief. Template Hammer **saute** une pièce sans appui (les lames) mais **s'arrête** sur une pièce gênée par un obstacle (relief, structure déjà là). Acquis :
- une lame tient à la tête d'un poteau de piliers fins debout sur un **coin de fondation**, qu'elle monte depuis la tête (E5) ou qu'elle y pende (V1, V3) ; les lames voisines de la ligne s'enchaînent ;
- ne tiennent pas une lame : le haut d'un mur (E4), un pilier fin dans le joint posé sur le mur du dessous (E1, E2, V0), un pilier fin debout sur le haut du mur (E3).

**3ᵉ essai :** `templates/test/Essai_rampes_3.json`, 127 entrées (`donnees/08_essai_rampes_3.csv`, vue de dessus : `plans/essai_rampes_3.png`). Compact : 3 rangées de 3 cas, environ 48 × 24 m ; pile de n demi-piliers = cas n. En regardant vers le haut des rampes, de gauche à droite : rangée proche G1 G2 G3, rangée du milieu G4 G5 G6, rangée du fond G7 G8 G9.

| Cas | Ce qui est testé | Sert à |
|---|---|---|
| G1 | poteau de 4 piliers fins sur un coin, **3 lames pendues à la suite** | overhang et débord |
| G2 | poteau d'1 pilier fin + 1 **demi-pilier fin** (tête à Z450), 1 lame montante | poteaux sur les paliers (Z −150) |
| G3 | poteau sur la **pointe d'une fondation triangle**, 1 lame montante | côtés à triangles du dodécagone |
| G4 | poteau sur un **coin de plafond** (Z300, sans pilier dessous), 1 lame montante | toit, appentis |
| G5 | **colonne** de piliers fins dans le joint d'un mur **depuis la fondation**, posée avant les cadres ; 1 lame montante, 1 pendante | départ des lignes sur la rive et la jupe |
| G6 | poteau au **milieu d'une arête** de fondation | plus de positions de poteaux |
| G7 | poteau au **centre** d'une fondation | idem |
| G8 | poteau sur un coin, 1 lame **pendue** à sa tête | casquette |
| G9 | 1 lame posée sur le **bord d'un plafond**, sans poteau | départs sur les planchers |

**Résultat en jeu** : G1, G3, G4, G7 et G8 complets ; G2, G5 et G9 sans lame ; G6 sans lame ni pilier fin. Règles qui en découlent : §3.1.

**Template d'essai :** `templates/test/Secteur_test_theta_-15_45.json`, 920 entrées.
- Il prend toutes les pièces entre θ −15° et 45° (2 côtés et une arête du dodécagone, coins compris), dans l'ordre de pose des plans, avec la pile d'ancrage.
- **Il est autonome** : une pièce dont le porteur est hors du secteur, ou un plafond à plus de 2 cases d'un appui relié au sol dans le secteur, est retirée. L'ancien secteur en contenait 9 (le centre de la mezzanine et du plancher de toit, dont les piliers étaient hors du secteur) ; il n'en reste plus.
- **`donnees/08_secteur_test.csv`** numérote chaque entrée (0 = 1re pièce) avec son plan, sa pièce, sa position et son repère. Si la pose s'arrête après N pièces, donnez-moi N et la dernière pièce visible : la ligne N du CSV est la pièce qui bloque, si aucune pièce n'a été sautée avant.
- On y trouve chaque sorte de pièce et d'appui : rive et jupe en cadres doubles, rampes extérieures et leurs poteaux (attique et palier 2), cage, casquette et appentis, tour du pod et toit, 120 rampes sur 104 piliers fins de poteaux, 13 murs de chaume, 8 Heavy (dont les 2 de rive d'un côté), 5 Tek, 1 Tesla, 2 grands carrés de culture et 1 moyen.
- Le toit y est à sa hauteur par défaut, calé sur la pile.

Posez-le en solo, sur la même plateforme. Notez les pièces refusées (`donnees/08_secteur_test.csv`), puis démolissez un mur de chaume.

## 8. Revue du code (`outils/forteresse.py`)

| Point | Ce qui a été fait |
|---|---|
| Découpage | `PLANS` : 11 plans par zone, avec la référence de chacun (pile ou mur A, B, C) ; option `rehausse()` |
| Ordre de pose | `ordre_de_pose()` range les pièces plan après plan, puis du bas vers le haut. `porteurs()` écarte les porteurs posés dans un plan suivant, puis cherche un voisin déjà posé. Les anciennes phases par hauteur et la cage seule sont remplacées par les plans |
| Poteaux | mode `stable` : `jeu_stable()`, `jeux_stables()` et `redondant()` choisissent les jonctions ; contrôle strict des poteaux isolés (`heurts(strict=True)`) ; la colonnade s'efface devant eux |
| Redondance | `verifier_appuis()` compte, lame par lame, les rampes qui tiennent encore si un appui de leur ligne est détruit |
| Défense | `defense()` : cap de 100 avec les Plant X, L1 qui complète le cap, emplacements du trou ; `couverture()` : contrôle de couverture en 3D |
| Murs de chaume | posés dans le plan de leur zone (`zone_chaume()`), pour que ce qui est posé au-dessus tienne dès la pose de la zone |
| Limites moteur | les appuis au sol des plafonds sont contrôlés sur la base finie (tous les plans posés) |
| Correction | en mode `stable`, le contrôle de redondance prenait la règle « prudent » (1 lame libre au plus) au lieu de celle des tours (6) |
| Excel | `outils/bilan_xlsx.py` est maintenant dans le dépôt (il était hors du dépôt) |
| Audit : rien sous Z0 | jupe d'un seul niveau sur le palier 2 (`geometrie_jupe`), tourelles de jupe supprimées, 2 Heavy de rive par côté (`defense()`), contrôle : aucune tourelle sous Z0 ; débord d'une lame par défaut |
| Audit : écart entre tourelles | `defense()` et `emplacements_trou()` refusent deux tourelles à moins de `ecart_tourelles` (300 UU, une largeur de mur) |
| Audit : noyau | `cages_noyau()` : 2 générateurs Tek et 2 boîtes de munitions sur l'anneau 1, en cage (`NOYAU`) ; stockages du hall avec allée d'une fondation (contrôle) |
| Audit : carrés de culture | volume réel du grand carré (300 UU) ; carré moyen (`crop_m`) dans la poche du toit de cage |
| Rampes sur poteaux | `nappe()` déclare les 3 nappes de rampes ; `consolider_rampes()` choisit la position et le décalage de chaque ligne et ses poteaux sur les points de pose (`points_poteaux()`), d'après les essais en jeu ; `porteurs()` et `verifier_appuis()` n'acceptent que la tête d'un pilier fin comme appui de lame ; 3 lames pendues au plus (`PENDUES_MAX`) ; plus de pilier dans les joints, de poutre fine ni de demi-pilier fin |

Options vérifiées, avec les mêmes contrôles, tour rehaussée comprise : `--appuis tours` (4 969 structures, 165 poteaux), `--appuis prudent` (4 377 : il ne garde que 256 lames, déconseillé), `--casquette 2` (5 147, 177 lames de casquette et d'appentis), `--debord 2` (416 rampes extérieures), `--colonnade 2560` (4 967).
