# Module 02 — Pod central de production (Coeur Base, Ø15, hall de 6 murs, toit en rampes)

Template : `templates/02_pod_central.json`, réparti dans les phases :
- **P2** : Coeur Base niveau 1, mur de pod niveaux 0-5, piliers PA bas ;
- **P3** : Coeur Base niveau 2, escalier prolongé, mezzanine ;
- **P6** : mur niveaux 6-7, piliers hauts, plancher de toit Z2400, toit en rampes inclinées.

Source du noyau : `references/Coeur_Base.json` (votre template *Coeur Base*). Coordonnées : `donnees/02_pod_central.csv`. Plans : `plans/plan_pod.png`, `plans/plan_toit_rampes.png`.

![Plan du pod](plans/plan_pod.png)

## 1. Volumes

| Élément | Cotes | Remarque |
|---|---|---|
| **Coeur Base** (centre du cercle) | rayon ≤ 900 UU, Z0 → Z600 (2 niveaux) | votre template, reposé tel quel au centre de l'étoile |
| **Escalier central** | (129,9 ; −75), de Z0 à Z1800 | escalier du Coeur Base prolongé jusqu'à la mezzanine |
| Emprise du pod | Dodécagone **D4** : apothème 2 239,2 UU, Ø 14,93 fondations entre plats | c'est l'étoile existante (anneaux 1 à 7) |
| **Hall d'atelier** | Z0 → Z1800 : **6 murs pleins de hauteur libre** autour du Coeur Base | aucun plancher intermédiaire |
| Mezzanine / étage technique | Z1800 → Z2400 (2 murs) | même niveau que la galerie de tourelles |
| **Plancher de toit** | Z2400, sur tout le pod | au niveau du toit de cage : un seul plancher fermé du centre jusqu'à D5 |
| **Toit en rampes inclinées** | Z2400 → Z5150, sur tout le contour D5 (pod + cage) | comme le toit des tours 1201 / 1809 ; remplace le cône et la reprise |

## 2. Coeur Base intégré au centre

Votre template est repris **entrée par entrée** : coordonnées, rotations, skins et couleurs sont conservés. Il forme avec l'escalier et le centre de la mezzanine le **noyau central**, posé une seule fois (module 06 §3). Son origine (0 ; 0) coïncide avec le centre de l'étoile, et ses cotes Z suivent déjà la même convention (fondation z 40, mur z 240).

**Modifications.** Le coffre « Matiere Premiere 1 » est sorti du template : c'est un équipement, posé à sa place d'origine et compté dans les 20 coffres-forts (module 07). Ses 10 fondations sont retirées. Elles suivent une grille carrée tournée de −30°, incompatible avec l'étoile, et la chevauchaient. Les murs du Coeur Base reposent donc sur les fondations de l'étoile (anneaux 1 à 3). Ce n'est pas une accroche d'arête : **la pose se fait en Template Hammer**, comme le template d'origine.

| Niveau | Contenu repris | Phase |
|---|---|---|
| 1 (Z0 → 300) | 17 murs extérieurs, 1 porte secrète d'entrée (θ ≈ 26°), 2 portes secrètes intérieures (au centre et en (259,8 ; −150)), 1 escalier (le coffre est à poser à la main) | P2 |
| plancher Z300 | 40 plafonds triangles + 5 plafonds (avec la trémie de l'escalier) | P3 |
| 2 (Z300 → 600) | 18 murs | P3 |

**Le centre du cercle.** Les deux portes secrètes intérieures forment la **cage d'escalier**, une cellule de 300 × 300 centrée en (129,9 ; −75) dont les axes sont tournés de −30°. La porte au centre exact (0 ; 0) en est un côté.

**Orientation.**
- Elle reste celle de l'export (`coeur_rotation = 0`) : les murs du Coeur Base restent parallèles aux arêtes de l'étoile, et son entrée regarde θ ≈ 26°, juste en face de la porte du hall de la part 1 (θ ≈ 26°).
- `--coeur-rotation` permet de le tourner. Avec un multiple de 60°, le parallélisme est conservé et l'entrée reste face à une porte du hall, puisqu'il y en a une par part.

**Encombrement** (contrôlé par le script) :
- rayon maximal 900 UU, contre 1 159 UU pour la couronne de piliers PA : 259 UU de passage ;
- les machines commencent à 1 200 UU ;
- la mezzanine est à Z1800, au-dessus du sommet du Coeur Base (Z600).

**Pile d'ancrage Template Hammer.** Elle est en (0 ; 300), à l'intérieur de la pièce du niveau 1, à 300 UU de toute pièce du Coeur Base. On l'atteint par la porte d'entrée. Démolissez-la à la fin (notice P8).

## 3. Escalier central prolongé

L'escalier du Coeur Base est prolongé, à la verticale, jusqu'à la mezzanine.

| Marche | Z | z template | Origine |
|---|---|---|---|
| 1 | 0 → 300 | 240 | Coeur Base |
| 2 à 6 | 300 → 1800 | 540 · 840 · 1140 · 1440 · 1740 | ajoutées (copies exactes : même x, y, yaw −120°) |

- **Trémie de la mezzanine** : le script retire les 6 pièces du plancher Z1800 traversées par la cellule d'escalier. Ce sont 4 triangles du centre et 2 carrés de l'anneau 1 (θ 0° et θ 300°), tracés en violet sur le plan. On sort de l'escalier directement sur la mezzanine, puis on gagne la galerie de tourelles par les 12 cadres du niveau 6 du mur de pod.
- Au-dessus du Coeur Base (Z600 → 1800), l'escalier monte en colonne libre dans le hall. Fermez-le si besoin par 4 murs : il reste 259 UU entre la cage et les piliers PA.

## 4. Mur de pod (D4)

- **48 positions par niveau** (12 côtés × 4), **8 niveaux** de Z0 à Z2400, soit 366 murs + 18 cadres de porte doubles (3 par part).

| Niveau | Z | Ouvertures |
|---|---|---|
| 0 | 0 → 300 | **6 cadres doubles**, 1 par part (côtés E1, position 1 : θ ≈ 26°, 86°, 146°…) : hall ↔ couloir annulaire |
| 1 à 5 | 300 → 1800 | aucune |
| **6** | 1800 → 2100 | **12 cadres doubles** (position 1 de chaque côté) : mezzanine ↔ galerie de tourelles |
| 7 | 2100 → 2400 | aucune ; le plancher de toit Z2400 se pose dessus |

## 5. Système porteur à piliers intérieurs

| Couronne | Position | Hauteur | Pièces | Rôle |
|---|---|---|---|---|
| **PA** | 12 coins de D2 : rayon 1 159,1, θ = 15° + 30°·k | Z0 → 2400 : 8 piliers | 96 | porte la mezzanine et le plancher de toit ; entoure le Coeur Base |
| **PB** | 12 coins de D1 : rayon 579,6, θ = 15° + 30°·k | Z1800 → 2400 : 2 piliers | 24 | porte le centre du plancher de toit ; posés sur la mezzanine, ils ne gênent ni le Coeur Base ni l'escalier |
- La colonnade circulaire entre le pod et les pics est décrite au module 03 §3.

## 6. Gabarits de placement des machines (hall Z0 → 1800)

Ce sont des zones de réservation, pas les cotes exactes des maillages. Elles commencent à 1 200 UU du centre, au-delà du Coeur Base et des piliers PA.

| Machine | Branche θ | Centre (x ; y) | Gabarit | Hauteur réservée | Énergie / carburant |
|---|---|---|---|---|---|
| **Réplicateur Tek** | 0° | (1 650 ; 0) | 3 × 2 fondations | 3 murs | à vérifier |
| **Générateur Tek n°1** | 60° | (900 ; 1 558,8) | 1 × 1 | 1 mur | élément |
| **Forge à vapeur** (Steam Forge) | 120° | (−825 ; 1 428,9) | 3 × 3 | 3 murs | élément (forge alimentée à l'élément) |
| *libre* (circulation, ou Tek Teleporter en option) | 180° | (−1 700 ; 0) | — | — | — |
| **Labo de fortune** (Makeshift Megalab) | 240° | (−825 ; −1 428,9) | 2 × 2 | 2 murs | à vérifier |
| 3 stockages dédiés Tek | 300° | (875 ; −1 515,5) | 3 × 1 | 2 murs | — |

Sur la mezzanine (Z1800) se trouvent le **générateur Tek n°2** en (−900 ; 0), puis **19 coffres-forts et 17 stockages dédiés** en alternance contre le mur de pod. Le 20ᵉ coffre-fort est celui du Coeur Base. Positions exactes : `donnees/07_equipements.csv` et module 07.

## 7. Mezzanine Z1800

Elle reprend le centre et les anneaux 1 à 7 en plafonds, **moins la trémie de l'escalier** : 94 plafonds + 188 plafonds triangles.

## 8. Toit en rampes inclinées (comme les tours 1201 / 1809)

Le cône de 228 toits, son capuchon et la reprise de la cage sont remplacés par :
1. un **plancher de toit fermé à Z2400** sur le pod (96 plafonds + 192 triangles). Il prolonge le toit de cage (module 04) : le bloc central a un seul plancher étanche du centre jusqu'à D5 ;
2. au-dessus, un **toit en rampes inclinées** (`StructureBP_Railing_Sloped_Metal`, la pièce des tours 1201 et 1809).

**Principe relevé sur la tour 1201.**
- Le toit est fait de **lames** : des files de rampes inclinées, parallèles à la pente, espacées de 300 UU.
- Chaque rampe monte de 300 UU sur 300 UU. La rampe suivante est 300 UU plus loin vers le faîtage et 300 UU plus haut.
- La première rampe a son pivot **150 UU devant le bord du plancher** et **10 UU sous son dessus** (z template = Z plancher + 80). Elle déborde comme une rive de toit.
- On ne peut ni se poser, ni tenir debout sur des lames : un dino largué n'y trouve aucune surface. Ce qui passe entre deux lames tombe sur le plancher fermé Z2400.

**Adaptation au dodécagone.** Il y a 12 pans, un par côté de D5. Sur chaque pan, les lames sont aux positions t = 0, ±300, ±600 le long du côté. Une lame s'arrête au faîtage, ou dès que sa rampe suivante sortirait de son pan.

| Rang | Apothème du pivot | Z plancher → rampe | Lames par pan | Rampes |
|---|---|---|---|---|
| r0 | 2 949,0 (150 devant D5) | 2400 | 5 | 60 |
| r1 | 2 649,0 | 2700 | 5 | 60 |
| r2 | 2 349,0 | 3000 | 5 | 60 |
| r3 | 2 049,0 | 3300 | 3 | 36 |
| r4 | 1 749,0 | 3600 | 3 | 36 |
| r5 | 1 449,0 | 3900 | 3 | 36 |
| r6 | 1 149,0 | 4200 | 3 | 36 |
| r7 | 849,0 | 4500 | 1 | 12 |
| r8 | 549,0 | 4800 | 1 | 12 |
| r9 | 249,0 | 5100 | 1 | 12 |
| **Total** | | sommet ≈ Z5150 | | **360** |

- Rotation : **yaw = θ du pan − 90°** ; la rampe monte vers le centre, comme les rampes `Sloped` de la tour 1201 (yaw −90° sur le pan θ = 0°).
- Le premier rang passe au-dessus de la casquette (module 04 §5), à environ 50 UU, parallèlement à elle.
- Coût : une rampe vaut environ **12 lingots + 3 pâte**, contre 35 + 10 pour un toit. ⚠ Le coût de la rampe inclinée est une estimation : c'est celui de la rambarde métal (Metal Railing).
- ⚠ À valider en solo : le décalage de 150 UU et de 10 UU vient du template 1201, posé sur des cadres de porte. Si la première rampe apparaît trop haute ou trop basse au-dessus de la casquette, corrigez `- 100` dans `toit_rampes()` et régénérez.

## 9. Contrôles de fin de module

- [ ] Coeur Base (noyau) : 35 murs, 3 portes secrètes, plancher Z300. Ses fondations ne sont pas posées (l'étoile les remplace) ; son coffre est reposé à la main.
- [ ] 6 escaliers empilés de Z0 à Z1800 ; la trémie de la mezzanine est ouverte au-dessus.
- [ ] 6 murs libres sous la mezzanine autour du Coeur Base.
- [ ] 6 cadres doubles au sol (1 par part) et 12 à Z1800.
- [ ] 24 colonnes de piliers PA/PB, toutes arrêtées à Z2400.
- [ ] Plancher de toit Z2400 fermé, sans jour.
- [ ] Toit : 360 rampes en 12 pans, lames au pas de 300 UU.
