# Module 06 — Trou à l'avant et plans par zone

Ce module couvre trois points :
- l'adaptation de la construction au **trou** (gouffre) à l'avant de la plateforme, d'après votre image annotée ;
- la **petite plateforme verte** au milieu du trou, posée pour un projet futur ;
- le découpage du projet en **11 plans Template Hammer par zone**, plus une rehausse en option. Le sol, puis chaque anneau du bord vers le centre, puis la tour du pod et son toit, et enfin la défense.

Templates : `templates/plans/`. Coordonnées pièce par pièce, dans l'ordre des entrées de chaque template : `donnees/Plan_*.csv`. Murs de bord du trou : `donnees/06_bord_du_trou.csv`.

![Trou et plans](plans/plan_trou_et_plans.png)

## 1. Le trou

### Relevé

Deux relevés de votre part sont enregistrés dans `references/` :

| Fichier | Contenu | Rôle |
|---|---|---|
| `Trou_points_ancrage.json` | votre export *trou* : 60 fondations posées en jeu + 1 demi-pilier (le pilier de référence) | recalage du repère |
| `Trou_fondations.json` | les fondations de votre image annotée : **blanc = à retirer** (124), **vert = plateforme** (10) | emprise du trou |

Le script recale l'export à chaque génération. Il pose votre demi-pilier sur le pilier de référence du projet (la pile d'ancrage en (0 ; 300)), puis cherche la rotation qui fait retomber les fondations sur l'étoile.

| Contrôle | Résultat |
|---|---|
| Rotation de votre export par rapport au projet | **−150°** |
| Fondations retrouvées sur l'étoile, à moins de 5 UU | **60 / 60** |
| Fondations du relevé tombées dans une fondation blanche | **0** |

### Emprise

Le trou est à l'avant, centré sur θ = 180°. Il entame le pod dès l'anneau 4 (x ≈ −1 120) et s'élargit jusqu'au bord de la plateforme, entre θ ≈ 155° et θ ≈ 205°.

| Anneau | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | **Total** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Fondations retirées (blanc) | 5 | 5 | 9 | 8 | 11 | 7 | 8 | 8 | 16 | 13 | 18 | 16 | **124** (40 carrés + 84 triangles) |
| Plateforme (vert) | — | — | — | — | — | 2 | 5 | 3 | — | — | — | — | **10** (5 carrés + 5 triangles) |

⚠ Si une fondation est mal classée, corrigez sa clé `[anneau, côté, index]` dans `references/Trou_fondations.json` et régénérez. Tout le reste suit.

## 2. La plateforme verte

- **10 fondations** au milieu du trou, sur les anneaux 9 à 11, posées au niveau Z0 **avec le sol (plan 1)**.
- **Rien n'est accroché dessus** : pour le script, elle compte comme le trou.
- Elle n'est reliée à la base par aucune arête : posez-la en Template Hammer et vérifiez en solo que le jeu l'accepte. Si vous ne la voulez pas encore, supprimez ces 10 fondations après la pose (repère `plateforme verte`).

## 3. Adaptation de la construction

### Bord du trou

| Élément | Hors du trou | Au droit du trou |
|---|---|---|
| Sol | étoile complète, paliers −150 et −300 | **124 fondations retirées** ; la plateforme verte reste |
| Tour du pod D4, fût D5, cadres L2, rive D7, jupe | inchangés | coupés là où ils passent au-dessus du trou |
| **Murs de bord du trou** | — | **22 arêtes** entre une fondation gardée (anneaux ≤ 13) et le trou ; chaque mur ferme la coupe jusqu'à l'enveloppe (tableau suivant) |
| Mezzanine, galeries, plancher de toit | pièces pleines | pièces au-dessus du trou retirées ; le bord est porté par les murs de bord |
| Toit, appentis, casquette, pente A, overhang | rampes inclinées | **aucune rampe au-dessus du trou**, sauf les casquettes du trou |

**Murs de bord** (`donnees/06_bord_du_trou.csv`) :

| Position de l'arête | Arêtes | Hauteur | Matériau | Plan |
|---|---|---|---|---|
| Pod (jusqu'à D4) | 10 | 9 murs, Z0 → 2700, + 1 dans la couronne (+ 1 par rehausse) | **murs pleins** (la tour) | 5 et 9 |
| Couloir (D4 → D5) | 4 | 8 murs, Z0 → 2400 (toit de cage) | cadres doubles | 6 |
| Entre D5 et D7 | 8 | 6 à 3 murs, jusque sous la pente A | cadres doubles | 4 |

En tout : **160 murs et cadres + 8 murs de chaume** de tourelles reposées.

### Toitures adaptées au trou

1. **Toit du pod** (plan 10) : chaque ligne de lames s'arrête à sa première rampe au-dessus du trou. Le plancher de toit s'arrête sur les murs de bord du pod, et la couronne les prolonge : la tour reste fermée.
2. **Casquettes du trou** : une lame part du haut de chaque mur de bord et descend de 300 UU au-dessus du gouffre, comme la casquette de D5.
   - Couloir : **4 lames**, Z2400 → 2100, dans le plan 6.
   - Pod : **8 lames**, Z3000 → 2700 sur la couronne, dans le plan 10.
   - Les lames des angles rentrants du trou croiseraient un mur ou une lame voisine : elles ne sont pas posées.
3. **Appentis, casquette de D5, pente A, overhang et débord** : ils s'arrêtent au bord du trou. Ce qui glisse tombe dans le gouffre.

## 4. Tourelles reposées face au gouffre

Le trou supprime des emplacements de tourelles : L1, jupe, rive et anneau D4. Ils sont **reposés sur les murs de bord, face au gouffre**, chacun sur une colonne de murs différente :

| Couche | Tourelles | Où | Plan du chaume | Plan de la tourelle |
|---|---|---|---|---|
| **TROU** | 3 Heavy (Z0) + 1 Tesla (Z300) | murs de bord entre D5 et D7, les plus proches du bord de la plateforme | 4 | 7 |
| **TROU-L1** | 2 Tek + 1 Heavy (Z1800) | murs de bord du couloir et du pod, niveau 6 ; on les recharge depuis la galerie et la mezzanine | 6 ou 5 | 7 |
| **TROU-D4** | 1 Tek (Z2400) | mur de bord du pod, niveau 8, comme l'anneau D4 | 5 | 8 |

Détail : module 05 §6.

## 5. Les 11 plans par zone

Chaque plan a **2 000 entrées au plus** (limite de Template Hammer). Dans chaque plan, les pièces sont rangées du bas vers le haut, **chacune après ce qui la porte**. Les plans se posent dans l'ordre : aucun plan ne s'appuie sur un plan posé après lui. Le générateur le vérifie (module 08 §5).

| Plan | Fichier `templates/plans/` | Contenu | Entrées | Lingots | Pâte | Calage |
|---|---|---|---|---|---|---|
| **1** | `Plan_01_sol_complet.json` | tout le sol : 344 fondations + 684 triangles (paliers et plateforme verte compris), sans le trou | 1 030 | 34 300 | 10 632 | pile d'ancrage (2 demi-piliers) |
| 2 | `Plan_02_colonnade_option.json` | **option** : colonnade de 226 piliers sous la pente A | 227 | 5 650 | 1 582 | pile |
| **3** | `Plan_03_bord_D8-D7.json` | **bord D8 → D7** : rive (132 cadres doubles), jupe (166 cadres doubles), overhang et débord (356 rampes), 83 poteaux sur les paliers (123 piliers fins, 43 demi-piliers fins), 94 poutres fines, 32 murs de chaume (rive et jupe) | 947 | 14 844 | 4 108 | pile |
| **4** | `Plan_04_D7-D5_pente_A.json` | **D7 → D5** : pente A (208 rampes), 146 poteaux de stabilité (563 piliers fins), murs de bord du trou (32 cadres doubles), 4 murs de chaume | 808 | 10 615 | 3 100 | pile |
| **5** | `Plan_05_tour_du_pod_D4.json` | **tour du pod** : 348 murs pleins + 17 cadres doubles (portes), 89 murs de bord du trou, 216 piliers PA/PB, 6 escaliers, mezzanine (255 plafonds), 14 murs de chaume (anneau D4) | 946 | 23 085 | 6 480 | pile |
| **6** | `Plan_06_D5-D4_cage_et_appentis.json` | **D5 → D4** : fût, L1 et L2 (398 cadres doubles), murs de bord du couloir (29 cadres doubles), galeries (426 pièces), casquette (53 rampes), appentis (53 rampes, 53 poteaux), casquette du trou (4 rampes), 29 murs de chaume (L1) | 1 046 | 22 749 | 6 366 | pile |
| **7** | `Plan_07_tourelles_D8-D4.json` | **défense D8 → D4** : 44 Heavy, 15 Tek, 6 Tesla, 5 carrés de culture | 71 | — | — | pile |
| **8** | `Plan_08_tourelles_perimetre_pod.json` | **défense du périmètre du pod** : 6 Heavy, 6 Tek, 2 Tesla, 6 carrés de culture | 21 | — | — | pile |
| **9** | `Plan_09_toiture_pleine_D4-centre.json` | **toiture pleine D4 → centre** : couronne (40 murs de D4 + 10 murs de bord), 24 piliers PA/PB, plancher de toit (260 plafonds + 1 trappe) | 335 | 8 027 | 2 258 | **mur A** |
| **10** | `Plan_10_toit_en_rampes_D4-centre.json` | **toit en rampes D4 → centre** : mur C, 170 rampes, 96 poteaux (288 piliers fins), casquette du trou (8 rampes) | 467 | 5 905 | 1 693 | **mur C** |
| **11** | `Plan_11_tourelles_dessus.json` | **défense du dessus** : mur B, 2 Heavy, 2 Tek, 2 Tesla, 4 carrés de culture | 11 | 25 | 7 | **mur B** |
| option | `Option_rehausse_pod_+1_niveau.json` | **+1 niveau de tour** : 52 murs pleins, 24 piliers | 76 | 1 900 | 532 | **mur A** |

Les lingots et la pâte ne comprennent pas les tourelles, déjà dans votre inventaire, ni les murs de chaume et les carrés de culture (bois, chaume, fibre, pierre ; module 07).

**Calage**
- **Pile d'ancrage** : le plan 1 pose la pile de 2 demi-piliers en (0 ; 300), sur votre pilier de référence (`snapOverrides [0,1]`). Les plans 2 à 8 ont 1 demi-pilier qui se pose sur cette pile (`snapOverrides [0]`).
- **Mur de référence** : les plans 9, 10, 11 et la rehausse se calent sur le haut de la tour, à n'importe quelle hauteur. Leur pièce de référence est un mur de D4 du côté θ 90° (A, B ou C, module 02 §8.1), à snapper sur le haut du mur de la tour.

**Ordre de pose**
1. **Plan 1** : tout le sol. Si votre étoile centrale est déjà posée, sautez les pièces déjà en place et **retirez celles qui tombent dans le trou** (anneaux 4 à 7, côté θ 180°).
2. **Plan 2** si vous gardez la colonnade (sinon, sautez-le).
3. **Plan 3** (bord D8 → D7), puis **plan 4** (D7 → D5) : la pente A s'appuie sur la rive.
4. **Plan 5** (tour du pod), puis **plan 6** (cage et appentis) : les galeries s'accrochent à la tour.
5. **Plan 7** et **plan 8** : les tourelles se posent sur leurs murs de chaume, déjà en place.
6. **Rehausse** (option), autant de fois que vous voulez de niveaux de tour.
7. **Plan 9** (toiture pleine), sur le mur A. Ensuite le **plan 10** (toit en rampes), sur le mur C, et le **plan 11** (tourelles du dessus), sur le mur B, dans l'ordre que vous voulez.
8. À la main :
   - démolition des 79 murs de chaume (`donnees/08_chaume_a_demolir.csv`) ;
   - 74 murs de pics (`donnees/03_ligne_pics.csv`) ;
   - portes doubles dans les cadres à fermer, échelles ;
   - graines de Plant X, eau et engrais ;
   - équipements (module 07) ;
   - démolition de la pile d'ancrage.

**Points d'appui entre plans** :
- la pente A (plan 4) part du haut de la rive (plan 3) ;
- les poteaux de l'overhang et de la pente A sont debout sur le sol (plan 1) ;
- les poteaux de l'appentis (plan 6) sont sur le toit de cage du même plan ;
- ceux du toit (plan 10) sont sur le plancher de toit (plan 9) ;
- les murs de chaume sont dans les plans de zone ; les murs et cadres posés au-dessus d'eux sont donc tenus dès la pose de leur zone ;
- la couronne (plan 9) se pose sur le haut de la tour (plan 5 ou rehausse), et au-dessus des murs de chaume de l'anneau D4.

## 6. Contrôles

- [ ] Plan 1 posé : aucune fondation dans le trou (124 manquantes), contour D8 complet ailleurs, plateforme verte en place.
- [ ] Murs de bord du trou fermés de la rive à la rive : pleins dans le pod, cadres doubles ailleurs.
- [ ] Casquettes du trou : 4 lames sur le couloir, 8 sur la couronne ; aucune autre rampe au-dessus du trou.
- [ ] 8 tourelles face au gouffre ; 100 emplacements en tout (module 05).
- [ ] Plans 9, 10 et 11 calés sur les murs A, C et B : plancher et toit centrés sur la tour.
- [ ] Contrôles du générateur (module 08) : aucune collision, chaque ligne de rampes sur ses appuis, chaque pièce après ce qui la porte, plan après plan.
