# Module 08 — Revue de constructibilité

Cette revue répond à trois questions :
- les plans se posent-ils en jeu ?
- les rampes ont-elles de quoi les tenir ?
- a-t-on oublié des murs de chaume à démolir ?

Elle compare les plans aux templates que vous m'avez donnés (zip *Construction ARK*). Elle contrôle aussi chaque pièce des 8 plans : collisions, appuis et chaume.

Ces contrôles font désormais partie du générateur. À chaque régénération, il refuse d'écrire des plans si :
- une pièce entre dans une autre ;
- une rampe n'est pas tenue ;
- quelque chose repose sur du chaume.

## 1. Verdict

| Question | Avant cette revue | Maintenant |
|---|---|---|
| Collisions entre pièces | **292 recouvrements réels**. Les deux principaux : le 4e rang de la pente A entre dans la cage (179), et des lames se croisent aux arêtes (80). Le jeu aurait refusé ces pièces | **0**, sur 4 864 pièces. Seul contact admis : le niveau bas de la jupe, contre la tranche des fondations de l'anneau 15 (§5) |
| Rampes tenues | **Non : 176 rampes mal tenues** au regard de la règle des tours. 62 au sommet du toit, sur des lignes de 7 à 9 lames sans appui intermédiaire. 94 au bout de l'overhang, dont les lames pendaient l'une à l'autre. 20 à la casquette, accrochées au-delà du sommet du plancher. En plus, le mur de jupe qui portait l'overhang flottait, et des lignes prenaient appui sur l'emplacement vide d'une Tesla | **Oui, comme sur les tours** : chaque ligne part d'un appui, monte librement au plus 6 lames, et ne pend jamais de plus d'une lame (§3) |
| Murs de chaume | 96, un par tourelle. Mais 10 lignes de rampes prenaient appui sur l'emplacement des Tesla de rive, et 1 colonne de murs de bord avait 2 chaumes superposés | **96**, listés dans `donnees/08_chaume_a_demolir.csv`. Rien d'autre n'est en chaume, et rien ne repose sur du chaume seul (§4) |
| Différence de coût | — | **+741 lingots et +373 pâte** : 104 poteaux et 94 poutres d'appui, moins 195 rampes impossibles à poser (module 07 §1 bis). Option `--appuis prudent` : +8 099 lingots et +2 637 pâte |

## 2. Comparaison avec vos templates

| Template | Ce qu'il montre | Ce que les plans en reprennent |
|---|---|---|
| **481** *Large.Plat.Base* (SkunkHD) | Étoile de fondations carrés + triangles. Sous la plateforme, un anneau de murs dont 23 sont en chaume (gabarits) | Le pavage, pièce pour pièce (`--verifier-481`). Son anneau inférieur et ses 23 murs de chaume ne font pas partie de nos plans |
| **1201** *100 turret 11x11* (P1agueTV) | Toit à 2 pans, 144 rampes inclinées, en lignes sur les arêtes des tuiles. Chaque ligne part d'un **pilier fin posé sur le mur d'égout**, au-dessus d'un treillis de 241 piliers fins couchés. Sur un pan, les lignes finissent sur un pilier fin de faîtage, porté par une poutre couchée entre les pignons en escalier. **Sur l'autre pan, elles montent librement, 5 lames au-dessus de leur appui.** Une lame déborde en porte-à-faux au bord du toit. 98 tourelles **fixées dans des cadres doubles, sans chaume** | Position des rampes : pivot au milieu, z = bas + 290, yaw = θ − 90°. Règles d'appui (§3). La variante « Right » des rampes ne fait que changer le côté de la lame |
| **1809** *merry chistmas* (IchmagPizza) | 182 rampes en lignes posées **sur les joints des murs**. Chaque ligne part d'une **poutre fine** (Flat Thin Pillar couché) à l'égout : il y en a 364 à z 3 990. Sur un pan, les lignes de 7 lames finissent sur un pilier fin debout sur la poutre de faîtage, et leur dernière lame dépasse d'une lame ; **sur l'autre pan, elles montent librement : 6 lames depuis la poutre d'égout.** 86 murs de chaume pour 85 tourelles : **78 ont un cadre de porte posé dessus**. 186 plafonds de chaume servent de gabarit sous 88 grands coffres | Lignes sur les joints des murs (pente A, overhang). Poutres fines sous le débord. Montée libre de 6 lames au plus, 7 lames au plus entre deux appuis. Cadre double L2 posé sur le chaume de L1, comme sur la tour |
| **2727** *Straight Heavy* | 1 mur de chaume + 1 Heavy, pivot 10 UU devant le mur, pitch −89,5°, roll −90° | Identique pour les 96 tourelles |
| **2901 / 2902 / 2903** (mho) | Pile de 2 demi-piliers z 15 / 165, `snapOverrides [0, 1]`, plantée au sommet commun de pièces | Pile d'ancrage du plan 1, 1 demi-pilier z 315 sur les autres plans |
| **704 / 701** | Cercles de piliers, 1 rang | Colonnade (1 pilier / 1 vide) |

Les templates qui ne servent pas aux plans sont restés de côté : Coeur Base, écuries, gacha, bases moyennes, cercles antigrav.

## 3. Appuis des rampes

### 3.1 Règle, relevée sur les tours

1. Une **ligne** est une file de rampes posées bout à bout, au pas de 300 UU.
2. Elle **part d'un appui** :
   - le haut d'un mur ou d'un cadre métal ;
   - le bord d'un plancher ou d'une fondation (pas la plateforme verte, où rien n'est accroché) ;
   - le bout d'une poutre fine ;
   - la tête d'un pilier.
3. **Ligne qui monte depuis son appui** (toit, pente A) :
   - au plus **6 lames** au-dessus du dernier appui, bout haut libre, comme sur un pan de chaque tour ;
   - au-delà, un **poteau** de piliers fins (Pillar_Thin_Metal, 300 UU, plus un demi-pilier fin pour 150 UU) debout sur le plancher sous une jonction ;
   - au plus **7 lames** entre deux appuis (tour 1809).
4. **Ligne qui pend de son appui** (casquette, overhang, débord) : **une seule lame en porte-à-faux** (lame de rive de la tour 1201). Au-delà, un poteau ou une poutre fine sous la jonction.
5. **Le chaume n'est jamais un appui** : il est démoli.
6. Deux lames qui se croisent, aux arêtes ou contre un mur, ne peuvent pas être posées toutes les deux. Le script retire la plus éloignée de son appui, **en bout de ligne** : chaque ligne reste continue depuis son appui.

**Option `--appuis prudent`** : chaque ligne qui monte finit en plus sur un poteau sous son bout haut, comme le pan « faîtage » des tours.
- Coût : 200 poteaux au lieu de 104, soit 732 piliers fins au lieu de 166 : +7 358 lingots et +2 264 pâte.
- À choisir si, en essai, une ligne libre s'effondre.

### 3.2 Résultat, pente par pente (défaut `--appuis tours`)

| Pente | Plan | Rampes | Point de départ | Appuis ajoutés | Ce qui reste libre |
|---|---|---|---|---|---|
| Toit | 6 | 263 | bord du plancher Z2400, à D5 | **21 poteaux** (43 piliers fins) sur le plancher Z2400 : 3 piliers sous la 3e jonction des 11 lignes de 9 lames, 1 pilier sous la 1re jonction des 10 lignes de 7 lames | au plus 6 lames montantes au-dessus d'un appui |
| Casquette de D5 | 5 | 53 | bord du plancher Z2400 | — | 1 lame pendue, comme à la tour 1201 |
| Casquette du trou | 6 | 12 | haut des murs de bord (Z2400) | — | 1 lame pendue |
| Pente A | 2 et 5 | 208 (3 rangs) | haut de la rive, sur les joints des murs | — | 3 lames montantes au plus |
| Overhang | 2 | 168 | haut de la rive | **83 poteaux** sur les paliers : 2 piliers fins sur le palier 2, ou 1 pilier fin + 1 demi-pilier fin sur la marche de l'anneau 14 | r−2 : 1 lame pendue |
| Débord | 2 | 188 | haut de la jupe, sur les joints de ses murs | **94 poutres fines** sorties du niveau bas de la jupe (Z −300) | r−4 : 1 lame pendue |
| **Total** | | **892** | | **104 poteaux, 94 poutres** | |

Le contrôle `verifier_appuis` reprend chaque rampe des 8 plans, sans se servir de la façon dont elles ont été générées. Résultat :
- aucune rampe sans appui ;
- au plus 3 lames entre deux appuis ;
- 244 lames pendues d'une lame à leur appui ;
- au plus 6 lames montantes au-dessus d'un appui.

Plans : `plans/plan_rampes.png` (points rouges : poteaux ; traits rouges : poutres) et `plans/coupe_radiale.png`.

### 3.3 Ce qui a changé dans la forme des pentes

- **Pente A en 3 rangs.** Le 4e rang finissait 80 UU derrière le fût, à Z1800. Il traversait 53 murs du fût, 73 murs de chaume de L1 et 53 pièces du plancher de galerie.
- **Lignes de la pente A et de l'overhang sur les joints des murs de rive** (t = ±150, ±450…), comme sur la tour 1809. Le milieu des murs reste libre : les Tesla de rive sont entre deux lignes. Avant, la lame d'overhang de t = 0 passait à travers chaque Tesla, et les deux lignes de t = 0 prenaient appui sur l'emplacement de la Tesla, vide en phase P4 et en chaume ensuite.
- **Overhang** : ses 4 rangs pendaient de la rive, chacun accroché au précédent. Les 2 premiers ont maintenant un poteau sur le palier ; les 2 rangs dans le vide sont accrochés à la jupe (débord).
- **Casquette de D5** : 5 lignes par côté au lieu de 7. Les lignes de t = ±900 pendaient au-delà du sommet du plancher, sans rien pour les tenir.
- **Toit** : aux 12 arêtes, les lignes de deux côtés voisins se croisaient (80 lames en tout, sur toutes les pentes). Elles s'arrêtent maintenant une à une, si bien que le toit a 5 lignes par côté en bas, 3 au milieu et 1 au faîtage. Ce qui passe entre les lames tombe toujours sur le plancher fermé Z2400.
- **Mur de jupe** : il était à 4 518,7, 40 UU au-delà du bord des fondations, sans rien dessous. Ses 9 murs par côté se croisaient aux angles. Il est maintenant **sur l'arête extérieure de l'anneau 15** (bord D8), avec 8 murs par côté : le niveau haut est posé sur le palier 2, le niveau bas pend dessous.
- **Débord** : les 2 rangs dans le vide sont maintenant accrochés au haut de la jupe, sur des lignes décalées de 150 UU. Le 2e rang pend au bout d'une poutre fine. Le débord finit 600 UU au-delà du bord de la plateforme (640 avant).

## 4. Murs de chaume à démolir en jeu

Liste complète, dans l'ordre de pose : `donnees/08_chaume_a_demolir.csv`. Elle donne le plan, le n° d'entrée dans le JSON, la tourelle portée et ce qui est posé au-dessus. Dans chaque plan, le mur de chaume est l'entrée juste avant sa tourelle.

| Plan | Couche | Murs de chaume | Posé au-dessus du chaume | Après démolition |
|---|---|---|---|---|
| 7 | L1 (cage, Z1800 → 2100) | 53 | un cadre double L2 | le cadre tient par ses voisins et le plancher de galerie Z2100, comme les 78 cadres posés sur du chaume à la tour 1809 |
| 7 | TROU-L1 (murs de bord, niveau 6) | 7 | le mur de bord du niveau 7 | tenu par ses voisins et le plancher de toit Z2400 |
| 2 | JUPE-int / JUPE-ext | 16 / 10 | — (le chaume pend sous le niveau bas de la jupe) | la tourelle seule |
| 2 | RIVE (Tesla, niveau 1) | 5 | rien | ouverture de 300 × 300 avec la Tesla au nu du mur (module 03 §2). Les lames voisines prennent appui sur les murs métal de part et d'autre |
| 2 | TROU (murs de bord, niveau 0 ou 1) | 5 | les niveaux supérieurs du mur de bord | **un seul chaume par colonne** : la Tesla S66 est maintenant sur un autre mur que les Heavy (avant, 1 colonne avait 2 chaumes superposés) |
| **Total** | | **96** | | |

- **Rien d'autre n'est en chaume dans les plans.** La tour 1809 utilise aussi 186 plafonds de chaume comme gabarits sous ses coffres ; ici, les équipements sont posés sur de vrais planchers (module 07 §3).
- Le contrôle des appuis ne compte jamais le chaume : aucune rampe, aucun poteau, aucune poutre ne dépend d'un mur de chaume.
- Démolissez les murs de chaume **après** la pose de leur tourelle, plan par plan. Testez d'abord sur une seule tourelle que celle-ci et ce qui est posé au-dessus restent en place.

## 5. Collisions

**Méthode.** Le générateur donne à chaque pièce un volume :
- mur 300 × 300 × 20 ;
- pilier 40 × 40, pilier fin 20 × 20 ;
- plafond 15 d'épaisseur ;
- rampe : lame de 10 × 100 au-dessus de sa ligne de base ;
- tourelle : bloc devant son mur de chaume.

Il donne aussi à chaque pièce un **noyau** : son volume sans les bords qui se touchent normalement au snap (arêtes de plancher, bouts de mur, tête et flancs de pilier, bouts de lame). Deux pièces sont **en collision** quand le noyau de l'une entre dans le volume de l'autre. C'est le cas que le jeu refuse (« obstrué »).

**Avant cette revue**, sur la version du trou (même contrôle) :

| Recouvrement | Paires | Cause |
|---|---|---|
| 4e rang de la pente A × fût, chaume L1, plancher de galerie | 179 | rang trop long de 80 UU |
| Lame × lame aux 12 arêtes (toit, pente A, overhang) | 80 | lignes qui dépassaient l'arête de leur côté |
| Mur de jupe × mur de jupe aux angles | 20 | 9 murs par côté pour un côté de 8,07 murs |
| Lame de pente A × mur de bord du trou | 6 | lame posée au ras du bord |
| Lame d'overhang × Tesla de rive | 5 | ligne de t = 0 au droit de la Tesla |
| Chaume d'une tourelle TROU × pilier de colonnade | 2 | — |
| **Total** | **292** | |

**Maintenant : 0 collision sur 4 864 pièces.** Contact admis : les 83 murs du niveau bas de la jupe, suspendus contre la tranche des fondations de l'anneau 15 (10 UU de recouvrement).

⚠ Les dimensions sont des hypothèses, à ± 10-20 UU des formes réelles du jeu. Le contrôle garantit qu'aucune pièce n'en traverse franchement une autre, pas que le jeu accepte chaque contact.

## 6. Ce que je ne peux pas vérifier d'ici : essai en solo

| Point | Pourquoi c'est incertain | Repli |
|---|---|---|
| Template Hammer pose-t-il une pièce qui en touche une autre, ou sans snap ? | Je n'ai trouvé aucune documentation sur son comportement. Les templates fournis ont été construits en jeu, puis exportés | Poser le plan concerné en premier ; ou à la main |
| Une ligne de 6 lames tient-elle libre au-dessus de son appui ? | C'est ce que montrent les tours. Mais leurs lignes partent d'une poutre fine ou d'un pilier fin, et les nôtres d'un haut de mur ou d'un bord de plancher | `--appuis prudent` : un poteau au bout de chaque ligne |
| La poutre fine sort de 300 UU du niveau bas de la jupe | Sur les tours, les poutres reposent toujours sur des murs | `--debord 1` : plus de poutre, le débord n'a qu'une lame |
| Le niveau bas de la jupe pend sous le bord de l'anneau 15 | La tour 481 a des murs sous sa plateforme, mais on ne sait pas comment ils tiennent | Garder seulement le niveau haut, et suspendre les chaumes de jupe dessous |
| Les tourelles et les cadres L2 restent en place après la démolition du chaume | Comportement de la tour 1809 et du template 2727 | Laisser le chaume |

**Template d'essai :** `templates/test/Secteur_test_theta_-15_45.json`, 907 entrées.
- Il prend toutes les pièces des plans 1, 3, 4, 5, 2, 6 et 7, dans cet ordre de pose, entre θ −15° et 45°, avec la pile d'ancrage.
- Cela fait 2 côtés et une arête du dodécagone.
- On y trouve chaque sorte de pièce et d'appui : rive, colonnade, pente A, overhang et ses poteaux sur les paliers, jupe, poutres et débord, cage, 16 tourelles (10 Heavy, 5 Tek, 1 Tesla) avec leurs 16 murs de chaume, toit et ses poteaux.

Posez-le en solo, sur la même plateforme. Notez les pièces refusées (leurs coordonnées sont dans `donnees/Plan_*.csv`), puis démolissez un mur de chaume. Au bord du secteur, quelques pièces peuvent manquer d'appui, puisque leur voisin est hors du secteur.

## 7. Revue du code (`outils/forteresse.py`)

| Défaut | Correction |
|---|---|
| `rang_rampes()` posait des rangs indépendants, sans contrôle de collision ni d'appui. Une lame pouvait dépasser l'arête de 150 UU et croiser la lame voisine | `pente()` pose des **lignes** continues depuis leur appui ; `consolider_rampes()` retire les lames en collision en bout de ligne et pose les poteaux et les poutres |
| `rangs_pente_A = 4` : le dernier rang entrait dans le fût, et la doc le présentait comme voulu (« passe 80 UU derrière la ligne du fût ») | 3 rangs |
| `rang_dodeca()` arrondissait au supérieur le nombre de murs par côté (« les pièces se chevauchent aux arêtes ») : les murs de jupe se croisaient aux angles | Supprimée ; la jupe est sur les arêtes de l'anneau 15 |
| Jupe à `A7 + 2F`, hors de toute arête de fondation | Bord D8 (`apo(8)`) |
| `emplacements_trou()` mettait les Heavy (niveau 0) et la Tesla (niveau 1) sur les mêmes murs | Murs distincts |
| La casquette prenait des lames au-delà du sommet de D5 | Une ligne doit partir de son côté (`|t| ≤ A·tan 15°`) |
| Commentaire faux dans `plan_rampes()` (« sens de montée vers le centre » pour `yaw + 90`, qui pointe vers le bas) | Corrigé |
| Aucun contrôle de constructibilité | `verifier_collisions()`, `verifier_appuis()`, `chaume_a_demolir()` ; le script s'arrête si un contrôle échoue |

Options vérifiées : `--appuis prudent`, `--casquette 2` et `--debord 1` passent les mêmes contrôles.
