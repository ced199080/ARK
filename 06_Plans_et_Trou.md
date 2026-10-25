# Module 06 — Trou à l'avant, plateforme future et 8 plans

Ce module couvre trois points :
- l'adaptation de la construction au **trou** (gouffre) à l'avant de la plateforme, d'après votre image annotée ;
- la **petite plateforme verte** au milieu du trou, posée pour un projet futur ;
- le découpage du projet en **8 plans Template Hammer** :
  - le sol des anneaux 12 à 15 ;
  - les murs, rampes et tourelles des anneaux 12 à 15 ;
  - les parties centrales ;
  - la plateforme verte.

Votre Coeur Base n'est plus dans le projet : le centre est repris à zéro. Toutes les pentes restent en **rampes inclinées**, et le toit est la pyramide de rampes de la version précédente (module 02 §8).

Templates : `templates/plans/`. Coordonnées pièce par pièce, avec la phase : `donnees/Plan_*.csv`. Murs de bord du trou : `donnees/06_bord_du_trou.csv`.

![Trou et plans](plans/plan_trou_et_plans.png)

## 1. Le trou

### Relevé

Deux relevés de votre part sont enregistrés dans `references/` :

| Fichier | Contenu | Rôle |
|---|---|---|
| `Trou_points_ancrage.json` | votre export *trou* : 60 fondations posées en jeu + 1 demi-pilier (le pilier de référence) | recalage du repère |
| `Trou_fondations.json` | les fondations de votre image annotée : **blanc = à retirer** (124), **vert = plateforme** (10) | emprise du trou |

Le script recale l'export à chaque génération. Il pose votre demi-pilier sur le pilier de référence du projet (la pile d'ancrage en (0 ; 300), demi-pilier du bas), puis cherche la rotation qui fait retomber les fondations sur l'étoile.

| Contrôle | Résultat |
|---|---|
| Rotation de votre export par rapport au projet | **−150°** |
| Fondations retrouvées sur l'étoile, à moins de 5 UU | **60 / 60** |
| Cotes | vos fondations à z 340 / 190 / 40 retombent sur Z 0 / −150 / −300, les deux paliers de bord |
| Fondations du relevé tombées dans une fondation blanche | **0** |

### Emprise

Le trou est à l'avant, centré sur θ = 180°. Il entame le pod dès l'anneau 4 (x ≈ −1 120) et s'élargit jusqu'au bord de la plateforme, entre θ ≈ 155° et θ ≈ 205°.

| Anneau | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | **Total** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Fondations retirées (blanc) | 5 | 5 | 9 | 8 | 11 | 7 | 8 | 8 | 16 | 13 | 18 | 16 | **124** (40 carrés + 84 triangles) |
| Plateforme (vert) | — | — | — | — | — | 2 | 5 | 3 | — | — | — | — | **10** (5 carrés + 5 triangles) |

⚠ Si une fondation est mal classée, corrigez sa clé `[anneau, côté, index]` dans `references/Trou_fondations.json` et régénérez. Le côté k est celui de normale 30°·k (le côté 6 regarde θ 180°), l'index part de θ croissants. Tout le reste suit : sol, murs, rampes, toit, tourelles, bilan.

## 2. La plateforme verte (plan 8)

- **10 fondations** au milieu du trou, dans l'axe θ 180°, sur les anneaux 9 à 11 (x ≈ −2 500 à −3 300). Elles sont posées au niveau Z0, comme le reste du centre.
- **Rien n'est accroché dessus** : ni mur, ni pilier, ni rampe, ni tourelle. Pour le script, elle compte comme le trou. Aucune pièce des autres plans n'est posée au-dessus.
- Elle est entourée de fondations retirées : elle n'est reliée à la base par aucune arête. Elle est dans son propre plan, `Plan_8_plateforme_future_anneaux_9-11.json`, avec le pilier de référence.
- ⚠ Isolée au-dessus du gouffre, elle ne s'accroche à rien : posez-la en **Template Hammer** et vérifiez en solo que le jeu l'accepte.

## 3. Adaptation de la construction

### Bord du trou

| Élément | Hors du trou | Au droit du trou |
|---|---|---|
| Sol | étoile complète, paliers −150 et −300 | **124 fondations retirées** ; la plateforme verte reste (plan 8) |
| Mur de pod D4, fût D5, cadres L2, rive D7 | inchangés | coupés là où ils passent au-dessus du trou |
| **Murs de bord du trou** | — | **22 arêtes** entre une fondation gardée (anneaux ≤ 13) et le trou. Chaque mur ferme la coupe jusqu'à l'enveloppe (détail ci-dessous). **136 murs + 12 emplacements de tourelles** |
| Mezzanine Z1800, plancher de toit Z2400, galeries | pièces pleines | pièces au-dessus du trou retirées ; le bord est porté par les murs de bord |
| Piliers PA / PB, colonnade | 120 piliers, cercle de rayon 3 600 | piliers PA / PB tous gardés (les sommets du bord restent appuyés) ; colonnade interrompue (36 positions), et 2 colonnes retirées parce qu'elles heurtaient le mur de chaume d'une tourelle TROU |
| Toit, casquette, pente A, overhang | rampes inclinées | **aucune rampe au-dessus du trou**, sauf la casquette du trou ci-dessous |
| Mur de jupe, pics, Tesla de rive | 4 478,5 (bord D8) / 4 068,7 / D7 | interrompus |

**Hauteur des murs de bord** (`donnees/06_bord_du_trou.csv`) :

| Position de l'arête | Arêtes | Hauteur | Plan |
|---|---|---|---|
| Pod et couloir (jusqu'à D5) | 14 | **8 murs**, Z0 → 2400 : jusqu'au plancher de toit | 4 (pod) ou 5 (couloir) |
| Entre D5 et D6 | 4 | 6 puis 5 murs, jusque sous la pente A | 5 |
| Anneaux 12-13 | 4 | 4 puis 3 murs, jusque sous la pente A | 2 |

### Toiture en rampes adaptée

1. **Pyramide du toit** (plan 6). Chaque ligne de lames s'arrête à sa première rampe au-dessus du trou : 263 rampes au lieu de 300. Le plancher de toit Z2400 s'arrête sur les murs de bord, et ces murs montent justement jusqu'à Z2400 : le bloc central reste fermé. Les poteaux du toit sont tous sur le plancher, aucun au-dessus du gouffre.
2. **Casquette du trou** (plan 6, nouveau). Le long des 14 murs de bord qui montent à Z2400, une lame de rampe part du haut du mur et descend de 300 UU au-dessus du gouffre, de Z2400 à Z2100. C'est la même règle que la casquette de D5 (module 04 §5) : ce qui glisse sur le toit passe devant les tourelles du bord et tombe dans le trou. **12 lames.** Les 2 lames des angles rentrants du trou (θ ≈ 172° et 197°) croiseraient un mur ou une lame voisine : elles ne sont pas posées.
3. **Casquette de D5, pente A, overhang et débord.** Ils s'arrêtent au bord du trou : 53, 208 et 356 rampes (au lieu de 60, 240 et 408). Ce qui glisse tombe directement dans le gouffre.

**Pourquoi fermer la base sur le bord du gouffre.** Le trou est une défense naturelle : rien ne tient au-dessus. Mais il ouvre un passage par le dessous de la plateforme et une face de la base sans glacis. On ferme donc la base sur le bord du trou par des murs pleins de toute la hauteur, et on y repose les tourelles qui tombaient dans le trou, tournées vers le gouffre.

## 4. Tourelles : 96, comme avant

Le trou supprime 12 emplacements : 7 de la cage L1 (côté 150° p4, côté 180° en entier, côté 210° p0), 4 Heavy de jupe et 1 Tesla de rive. Ils sont **reposés sur les murs de bord, face au gouffre** :

| Couche | Emplacements | Où | Plan |
|---|---|---|---|
| **TROU-L1** | 3 Tek + 4 Heavy | murs de bord du pod et du couloir, **niveau 6 (Z1800 → 2100)**, celui de L1. On les recharge depuis la mezzanine et la galerie. La casquette du trou passe au-dessus | 7 |
| **TROU** | 4 Heavy au niveau 0 (Z0 → 300) + 1 Tesla au niveau 1 (Z300 → 600), sur 5 murs différents | murs de bord les plus proches du bord de la plateforme (θ ≈ 159° à 205°) | 2 |

| Couche | Plan | Heavy | Tek | Tesla |
|---|---|---|---|---|
| L1 (cage), hors trou | 7 | 26 | 27 | — |
| **TROU-L1** (bord du trou, Z1800) | 7 | **4** | **3** | — |
| Jupe, hors trou | 2 | 26 | — | — |
| Rive, hors trou | 2 | — | — | 5 |
| **TROU** (bord du trou, Z0 / Z300) | 2 | **4** | — | **1** |
| **Total** | | **60** | **30** | **6** |

Le cap reste respecté : 96 tourelles, toutes à moins de 9 101 UU les unes des autres (module 05). La réserve reste de 20 Heavy, 5 Tek et 4 Tesla.

## 5. Les 8 plans

Chaque plan contient le **pilier de référence**. Le plan 1 pose la pile de 2 demi-piliers en (0 ; 300) (`snapOverrides [0,1]`). Les plans 2 à 8 ont 1 demi-pilier qui se pose sur cette pile (`snapOverrides [0]`). Dans chaque plan, les pièces sont triées par phase : sol → murs et piliers → plafonds → rampes → cage → toit → tourelles.

| Plan | Fichier `templates/plans/` | Contenu | Pièces | Lingots | Pâte |
|---|---|---|---|---|---|
| **1** | `Plan_1_sol_anneaux_12-15.json` | sol des anneaux 12 à 15 : 147 fondations + 294 triangles, dont les paliers à −150 (anneau 14) et −300 (anneau 15), sans le trou | 441 | 14 700 | 4 557 |
| **2** | `Plan_2_murs_rampes_tourelles_anneaux_12-15.json` | anneaux 12 à 15 : rive (143 murs), murs de bord du trou (10), colonnade (226 piliers), mur de jupe (166), appuis (83 poteaux sur les paliers : 123 piliers fins + 43 demi-piliers fins ; 94 poutres fines), **toute la pente A** (208 rampes, de la rive vers la cage), overhang et débord (356 rampes), puis **36 murs de chaume + 30 Heavy + 6 Tesla** | 1 441 | 23 515 | 6 461 |
| **3** | `Plan_3_sol_centre_anneaux_0-11.json` | sol du centre : hexagone central et anneaux 1 à 11, sans le trou ni la plateforme (192 fondations + 385 triangles) | 577 | 19 225 | 5 960 |
| **4** | `Plan_4_pod_central.json` | pod : mur de pod (319 murs + 17 cadres doubles), murs de bord du trou dans le pod (77), piliers PA/PB (120), colonne de 6 escaliers, mezzanine Z1800 (255 plafonds) | 794 | 19 660 | 5 521 |
| **5** | `Plan_5_cage_et_casquette.json` | cage : fût (312 murs + 6 cadres), murs de bord du trou dans le couloir (49), galeries Z1800 / 2100 / 2400 (426 pièces, dont 5 trappes), 53 cadres doubles L2, casquette (53 rampes) | 899 | 21 201 | 5 934 |
| **6** | `Plan_6_toit_rampes.json` | plancher de toit Z2400 du pod (261), 21 poteaux (43 piliers fins), toit en rampes inclinées (263) et **casquette du trou (12 rampes)** | 579 | 10 036 | 2 737 |
| **7** | `Plan_7_tourelles_cage_L1.json` | **60 murs de chaume + 30 Tek + 30 Heavy** : cage L1 (53) et bord du trou au niveau L1 (7) | 120 | — | — |
| **8** | `Plan_8_plateforme_future_anneaux_9-11.json` | **plateforme verte** : 5 fondations + 5 triangles, rien dessus | 10 | 375 | 115 |

Les lingots et la pâte des plans 2 et 7 ne comprennent pas les tourelles, déjà dans votre inventaire.

**Ordre de pose conseillé**
1. Plan 1, puis plan 3 : tout le sol. Si votre étoile centrale est déjà posée, sautez dans le plan 3 les pièces déjà en place, et **retirez celles qui tombent dans le trou** (anneaux 4 à 7, côté θ 180°).
2. Plan 4 (pod), puis plan 5 (cage).
3. Plan 2 : rive, bord du trou extérieur, colonnade, rampes extérieures, jupe et tourelles extérieures.
4. Plan 6 : plancher de toit, toit et casquette du trou.
5. Plan 7 : tourelles de la cage et du bord du trou (niveau L1).
6. Plan 8 : la plateforme verte, quand vous en aurez besoin.
7. À la main : démolition des 96 murs de chaume (liste et ordre : `donnees/08_chaume_a_demolir.csv`), 74 murs de pics (`donnees/03_ligne_pics.csv`), portes doubles, échelles, équipements (module 07), puis démolition de la pile d'ancrage.

⚠ Les plans s'appuient les uns sur les autres :
- la pente A est entière dans le plan 2 : chaque ligne de lames y est posée depuis son appui sur la rive ;
- les poteaux de l'overhang (plan 2) sont debout sur les paliers (plan 1), ceux du toit (plan 6) sur le plancher Z2400 du même plan ;
- la Tesla S66 du bord du trou (plan 2) est sur un mur de bord du couloir (plan 5) : posez le plan 5 avant le plan 2 ;
- les murs de bord des anneaux 12-13 (plan 2) reposent sur l'anneau 11 (plan 3) ;
- la casquette du trou (plan 6) s'accroche en haut des murs de bord (plans 4 et 5).
Si Template Hammer refuse des pièces faute d'appui, posez d'abord le plan concerné.

## 6. Contrôles

- [ ] Plans 1 et 3 posés : aucune fondation dans le trou (124 manquantes), contour D8 complet ailleurs.
- [ ] Plateforme verte : 10 fondations, rien dessus.
- [ ] Murs de bord du trou fermés de la rive à la rive, 8 niveaux dans le pod et le couloir ; plancher de toit fermé.
- [ ] Casquette du trou : 12 lames au-dessus du gouffre ; aucune autre rampe au-dessus du trou.
- [ ] 12 tourelles face au gouffre (7 à Z1800, 5 à Z0 / Z300) ; 96 tourelles en tout.
- [ ] 96 murs de chaume démolis ; les tourelles restent en place.
- [ ] Contrôles du générateur (module 08) : aucune collision entre pièces, chaque ligne de rampes sur ses appuis, rien ne repose sur un mur de chaume.
