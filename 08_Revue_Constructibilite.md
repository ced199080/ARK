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
| Collisions entre pièces | **0 sur 5 652 pièces** (les 11 plans, colonnade comprise), sans aucun contact admis : plus rien n'est accroché sous les fondations (§5). Tour rehaussée d'un niveau : **0 sur 5 728 pièces** |
| Rampes tenues, comme sur les tours | **Oui** : 758 rampes, chaque ligne part d'un appui, au plus 3 lames entre deux appuis, aucune lame pendue de plus d'une lame (§3) |
| Rampes qui tiennent si un appui est détruit | **Toutes les lignes montantes** : toit du pod 170 lames sur 170, pente A 208 sur 208, appentis 53 sur 53. Les lames qui pendent d'une seule lame (casquettes, bout de l'overhang et du débord) restent comme sur les tours (§3.3) |
| Ordre de pose | Plan après plan, chaque pièce après ce qui la porte : aucun plan ne s'appuie sur un plan posé plus tard (§6) |
| Taille des plans | 11 à 1 046 entrées, sous la limite de 2 000 |
| Murs de chaume | **79**, un par tourelle verticale, listés dans `donnees/08_chaume_a_demolir.csv`. Ils sont dans les plans de zone, à leur place dans les murs. Rien d'autre n'est en chaume, et rien ne repose sur du chaume seul (§4) |

## 2. Comparaison avec vos templates

| Template | Ce qu'il montre | Ce que les plans en reprennent |
|---|---|---|
| **481** *Large.Plat.Base* (SkunkHD) | Étoile de fondations carrés + triangles | Le pavage, pièce pour pièce (`--verifier-481`) |
| **1201** *100 turret 11x11* (P1agueTV) | **873 cadres de porte doubles** comme murs ; toit à 2 pans en lignes de rampes inclinées ; chaque ligne part d'un pilier fin sur l'égout, monte librement de 5 lames sur un pan, finit sur un pilier fin de faîtage sur l'autre | Cadres doubles partout sauf la tour du pod. Position des rampes : pivot au milieu, z = bas + 290, yaw = θ − 90°. Règles d'appui (§3) |
| **1809** *merry chistmas* (IchmagPizza) | **802 cadres doubles** ; rampes en lignes sur les joints des murs, poutres fines d'égout, pilier fin de faîtage, 6 lames libres sur un pan ; 86 murs de chaume dont **78 portent un cadre de porte** | Lignes sur les joints des murs (pente A, overhang). Cadre double posé sur le chaume de L1 et de la rive, comme sur la tour |
| **1584** *Small PvP Tower* | Tour à étages, **19 grands carrés de culture** (Plant X) sur les planchers et les toits, tourelles autour | Carrés de culture de Plant X : pivot 10 UU au-dessus du plancher (`CropPlotLarge_SM`, et `CropPlotMedium_SM` dans la poche du toit de cage) |
| **2727** *Straight Heavy* | 1 mur de chaume + 1 Heavy, pivot 10 UU devant le mur, pitch −89,5°, roll −90° | Identique pour les 71 Heavy et Tek verticales et les 8 Tesla sur chaume, toutes au-dessus de Z0 |
| **2901 / 2902 / 2903** (mho) | Pile de 2 demi-piliers z 15 / 165, `snapOverrides [0, 1]` | Pile d'ancrage du plan 1, 1 demi-pilier z 315 sur les plans 2 à 8 |
| **704 / 701** | Cercles de piliers, 1 rang | Colonnade, en option (plan 2) |

## 3. Appuis des rampes

### 3.1 Règle, relevée sur les tours

1. Une **ligne** est une file de rampes posées bout à bout, au pas de 300 UU.
2. Elle **part d'un appui** : le haut d'un mur ou d'un cadre métal ; le bord d'un plancher ou d'une fondation (pas la plateforme verte) ; le bout d'une poutre fine ; la tête d'un pilier.
3. **Ligne qui monte** (toit, pente A, appentis) : au plus **6 lames** au-dessus du dernier appui ; au plus **7 lames** entre deux appuis (tour 1809).
4. **Ligne qui pend** (casquette, overhang, débord, casquettes du trou) : **une seule lame en porte-à-faux** (lame de rive de la tour 1201). Au-delà, un poteau ou une poutre fine sous la jonction.
5. **Le chaume n'est jamais un appui** : il est démoli.
6. Deux lames qui se croisent ne peuvent pas être posées toutes les deux. Le script retire la plus éloignée de son appui, **en bout de ligne** : chaque ligne reste continue depuis son appui.

### 3.2 Poteaux de stabilité (mode `stable`, défaut)

Vous avez demandé des poteaux de piliers fins sous les jonctions de lames, en plus de ceux des tours, pour que les rampes tiennent en cas de destruction. Chaque **ligne montante** reçoit donc un poteau sous la jonction 1, puis une jonction sur trois (4, 7…) et sous son bout haut :

| Ligne | Poteaux | Si un appui est détruit |
|---|---|---|
| 1 lame (appentis) | bout haut | la lame pend du poteau, ou monte libre depuis le haut de D5 |
| 3 lames (pente A) | jonctions 1 et 3 | 1 lame pendue sous la jonction 1, ou 3 lames entre deux appuis |
| 7 lames (toit) | jonctions 1, 4 et 7 | au plus 6 lames entre deux appuis, ou 3 libres |

- Si un poteau ne peut pas être posé (une lame d'un autre pan passe à cet endroit), le script en décale un, en gardant la redondance. Les 178 lignes montantes ont toutes leurs poteaux.
- **Contrôle strict des poteaux** : un poteau ne se snappe à aucun mur. Il ne doit toucher aucun mur, pilier, tourelle ni carré de culture, de tout son volume.
- Les poteaux de la pente A remplacent la colonnade, qui passe en option : elle ne gêne aucun d'eux.
- `--appuis tours` : les règles des tours seules, sans poteau de stabilité. `--appuis prudent` : un poteau sous le bout haut de chaque ligne montante.

### 3.3 Résultat, pente par pente

| Pente | Plan | Rampes | Point de départ | Appuis | Lames qui tiennent si un appui est détruit |
|---|---|---|---|---|---|
| Toit du pod | 10 | 170 | haut de la couronne (Z3000) | **96 poteaux** (288 piliers fins) sur le plancher de toit | **170 / 170** |
| Appentis | 6 | 53 | haut de D5 (Z2400) | **53 poteaux** (1 pilier fin) sur le toit de cage | **53 / 53** |
| Pente A | 4 | 208 | haut de la rive, sur les joints des cadres | **146 poteaux** (563 piliers fins) sur le sol | **208 / 208** |
| Casquette de D5 | 6 | 53 | haut de D5 | — | 1 lame pendue, comme à la tour 1201 |
| Casquettes du trou | 6 et 10 | 12 | haut des murs de bord | — | 1 lame pendue |
| Overhang | 3 | 168 | haut de la rive | **83 poteaux** sur les paliers (123 piliers fins, 43 demi-piliers fins) | le bout r−2 pend d'une lame |
| Débord | 3 | 94 | haut de la jupe (Z0) | — | 1 lame pendue (`--debord 1`) |
| **Total** | | **758** | | **378 poteaux** | |

Le contrôle `verifier_appuis` reprend chaque rampe des plans, sans se servir de la façon dont elles ont été générées. Résultat :
- aucune rampe sans appui ;
- au plus 3 lames entre deux appuis ;
- 244 lames pendues d'une lame à leur appui ;
- aucune lame libre au-dessus de son dernier appui : toutes les lignes montantes finissent sur un poteau.

La redondance est contrôlée lame par lame : chaque appui de la ligne est retiré tour à tour, et le contrôle vérifie que la lame reste dans les règles. Plans : `plans/plan_rampes.png` et `plans/coupe_radiale.png`.

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

Il donne aussi à chaque pièce un **noyau** : son volume sans les bords qui se touchent normalement au snap (arêtes de plancher, bouts de mur, tête et flancs de pilier, bouts de lame). Deux pièces sont **en collision** quand le noyau de l'une entre dans le volume de l'autre : c'est le cas que le jeu refuse (« obstrué »). Les poteaux de stabilité, qui ne se snappent à rien, sont contrôlés de tout leur volume (§3.2).

**Résultat : 0 collision sur 5 652 pièces**, colonnade comprise, sans contact admis. Les cages du noyau (§ module 02 §6.1) n'entrent ni dans la colonne d'escaliers ni dans les piliers PB, qui sont à leurs coins.

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

**Template d'essai :** `templates/test/Secteur_test_theta_-15_45.json`, 1 047 entrées.
- Il prend toutes les pièces entre θ −15° et 45° (2 côtés et une arête du dodécagone), dans l'ordre de pose des plans, avec la pile d'ancrage.
- On y trouve chaque sorte de pièce et d'appui : rive et jupe en cadres doubles, pente A et ses poteaux de stabilité, overhang et poteaux sur les paliers, débord, cage, appentis, tour du pod et toit, 13 murs de chaume, 8 Heavy (dont les 2 de rive d'un côté), 5 Tek, 1 Tesla, 2 grands carrés de culture et 1 moyen.
- Le toit y est à sa hauteur par défaut, calé sur la pile.

Posez-le en solo, sur la même plateforme. Notez les pièces refusées (leurs coordonnées sont dans `donnees/Plan_*.csv`), puis démolissez un mur de chaume. Au bord du secteur, quelques pièces peuvent manquer d'appui, puisque leur voisin est hors du secteur.

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

Options vérifiées, avec les mêmes contrôles, tour rehaussée comprise : `--appuis tours` (4 795 structures), `--appuis prudent` (5 259), `--casquette 2` (6 063), `--colonnade 2560` (5 619). `--debord 2` n'a plus d'effet : sans niveau de jupe sous les fondations, le 2e rang n'a pas d'appui et le script le retire (94 lignes raccourcies).
