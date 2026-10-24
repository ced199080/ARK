# Module 02 — Pod central de production (Coeur Base, Ø15, machines hautes au centre)

Template : `templates/02_pod_central.json`, réparti dans les phases :
- **P2** : Coeur Base niveau 1, mur de pod (4 niveaux), piliers PA ;
- **P3** : Coeur Base niveau 2.

Le plancher de toit Z1200, qui couvre aussi le pod, et le toit bas en rampes sont au module 04.

Source du noyau : `references/Coeur_Base.json` (votre template *Coeur Base*). Coordonnées : `donnees/02_pod_central.csv`, `donnees/07_equipements.csv`. Plan : `plans/plan_pod.png`.

![Plan du pod](plans/plan_pod.png)

## 1. Profil bas : les éléments les plus hauts au centre

Toute la base est couverte par **un seul plancher de toit, à Z1200 (4 murs)**. Au-dessus, il n'y a que des rampes basses, jusqu'à Z1550 environ (module 04). La version précédente culminait à Z5150.

| Élément | Cotes | Remarque |
|---|---|---|
| **Coeur Base** (centre du cercle) | rayon ≤ 900 UU, Z0 → Z600 (2 niveaux) | votre template, reposé tel quel au centre de l'étoile |
| Emprise du pod | Dodécagone **D4** : apothème 2 239,2 UU, Ø 14,93 fondations entre plats | c'est l'étoile existante (anneaux 1 à 7) |
| **Hall du pod** | Z0 → Z1200 : **4 murs de hauteur libre** | les machines les plus hautes (réplicateur Tek, forge) ont besoin de 3 murs |
| Hall extérieur | entre le pod et la rive, Z0 → Z1200 | stockage, colonnade, accès à la galerie de tourelles (module 04) |
| Plancher de toit | Z1200, sur toute la base | module 04 |

Il n'y a plus de mezzanine ni d'escalier prolongé jusqu'à Z1800 : aucun étage au-dessus du hall. Le stockage passe au sol, dans le hall extérieur, et la galerie de tourelles se rejoint par des trappes (module 04).

## 2. Coeur Base intégré au centre

Votre template est repris **entrée par entrée** : coordonnées, rotations, skins et couleurs sont conservés. Il forme le **noyau central**, posé une seule fois (module 06 §3). Son origine (0 ; 0) coïncide avec le centre de l'étoile, et ses cotes Z suivent déjà la même convention (fondation z 40, mur z 240).

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
- le plancher de toit est à Z1200, 600 UU au-dessus du sommet du Coeur Base (Z600).

**Pile d'ancrage Template Hammer.** Elle est en (0 ; 300), à l'intérieur de la pièce du niveau 1, à 300 UU de toute pièce du Coeur Base. On l'atteint par la porte d'entrée. Démolissez-la à la fin.

## 3. Mur de pod (D4)

- **48 positions par niveau** (12 côtés × 4), **4 niveaux** de Z0 à Z1200, soit 186 murs + 6 cadres de porte doubles.
- Niveau 0 : **6 cadres doubles**, 1 par part (côtés E1, position 1 : θ ≈ 26°, 86°, 146°…), entre le hall du pod et le hall extérieur.
- Le plancher de toit Z1200 se pose sur le haut du mur.

## 4. Système porteur

| Élément | Position | Hauteur | Pièces | Rôle |
|---|---|---|---|---|
| **Piliers PA** | 12 coins de D2 : rayon 1 159,1, θ = 15° + 30°·k | Z0 → 1200 : 4 piliers | 48 | portent le plancher de toit au-dessus du hall ; entourent le Coeur Base |
| Poteaux D5 et D6 | coins de D5 (2 897,8) et de D6 (3 477,4) | Z0 → 1200 | 96 | portent le plancher de toit au-dessus du hall extérieur (module 04) |

Les anciens piliers PB (sur la mezzanine) sont supprimés : sans mezzanine, ils tomberaient dans le Coeur Base. Le centre du plancher est à 4 travées des piliers PA.

## 5. Machines et stockage

Les gabarits sont des zones de réservation, pas les cotes exactes des maillages. Ils commencent à 1 150 UU du centre, au-delà du Coeur Base et des piliers PA. **Les machines les plus hautes sont au centre de la base**, dans le hall du pod :

| Machine | Branche θ | Centre (x ; y) | Gabarit | Hauteur réservée | Énergie / carburant |
|---|---|---|---|---|---|
| **Réplicateur Tek** | 0° | (1 650 ; 0) | 3 × 2 fondations | 3 murs | à vérifier |
| **Générateur Tek n°1** | 60° | (900 ; 1 558,8) | 1 × 1 | 1 mur | élément |
| **Forge à vapeur** (Steam Forge) | 120° | (−800 ; 1 385,6) | 3 × 3 | 3 murs | élément (forge alimentée à l'élément) |
| **Labo de fortune** (Makeshift Megalab) | 180° | (−1 650 ; 0) | 2 × 2 | 2 murs | à vérifier |
| **Générateur Tek n°2** | 240° | (−900 ; −1 558,8) | 1 × 1 | 1 mur | élément |
| 3 stockages dédiés Tek | 300° | (875 ; −1 515,5) | 3 × 1 | 2 murs | — |

- La forge à vapeur occupe la place d'une forge industrielle. Si vous posez une forge industrielle à la place, elle tient dans le même gabarit.
- **Stockage** : 19 coffres-forts et 17 stockages dédiés en alternance, au sol, contre la **face extérieure** du mur de pod, dans le hall extérieur. Ils sont aux positions 0, 2 et 3 de chaque côté ; la position 1 est la porte du pod, ou un passage. Le 20ᵉ coffre-fort est celui du Coeur Base. Positions exactes : `donnees/07_equipements.csv`.
- **Générateurs Tek** : chacun alimente les machines et la moitié la plus proche des 30 Tek de la cage. Le plus éloigné est à 4 272 UU (module 05 §8).

## 6. Contrôles de fin de module

- [ ] Coeur Base (noyau) : 35 murs, 3 portes secrètes, 1 escalier, plancher Z300. Ses fondations ne sont pas posées (l'étoile les remplace) ; son coffre est reposé à la main.
- [ ] Mur de pod : 4 niveaux, 6 cadres doubles au sol (1 par part).
- [ ] 12 colonnes de piliers PA, de Z0 à Z1200.
- [ ] Machines au centre ; 36 emplacements de stockage libres contre la face extérieure du pod.
