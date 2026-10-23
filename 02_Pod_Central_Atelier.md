# Module 02 — Pod central de production (Coeur Base, Ø15, hall de 6 murs, cône étanche)

Template : `templates/02_pod_central.json`, réparti dans les phases :
- **P2** : Coeur Base niveau 1, mur de pod niveaux 0-5, piliers PA bas ;
- **P3** : Coeur Base niveau 2, escalier prolongé, mezzanine ;
- **P6** : mur niveaux 6-9, piliers hauts, cône, capuchon.

Source du noyau : `references/Coeur_Base.json` (votre template *Coeur Base*). Coordonnées : `donnees/02_pod_central.csv`. Plan : `plans/plan_pod.png`.

![Plan du pod](plans/plan_pod.png)

## 1. Volumes

| Élément | Cotes | Remarque |
|---|---|---|
| **Coeur Base** (centre du cercle) | rayon ≤ 900 UU, Z0 → Z600 (2 niveaux) | votre template, reposé tel quel au centre de l'étoile |
| **Escalier central** | (129,9 ; −75), de Z0 à Z1800 | escalier du Coeur Base prolongé jusqu'à la mezzanine |
| Emprise du pod | Dodécagone **D4** : apothème 2 239,2 UU, Ø 14,93 fondations entre plats | c'est l'étoile existante (anneaux 1 à 7) |
| **Hall d'atelier** | Z0 → Z1800 : **6 murs pleins de hauteur libre** autour du Coeur Base | aucun plancher intermédiaire |
| Mezzanine / étage technique | Z1800 → Z3000 (4 murs) | même niveau que la galerie de tourelles |
| Cône | Z3000 → Z5100, 7 rangs de toits à 45° | fermé et étanche |
| Capuchon et pointe | plafond à Z5100 + 4 demi-toits → sommet Z5250 | — |

## 2. Coeur Base intégré au centre

Votre template est repris **entrée par entrée** : coordonnées, rotations, skins, couleurs et nom du coffre « Matiere Premiere 1 » sont conservés. Son origine (0 ; 0) coïncide avec le centre de l'étoile, et ses cotes Z suivent déjà la même convention (fondation z 40, mur z 240).

**Seule modification.** Ses 10 fondations sont retirées. Elles suivent une grille carrée tournée de −30°, incompatible avec l'étoile, et la chevauchaient. Les murs du Coeur Base reposent donc sur les fondations de l'étoile (anneaux 1 à 3). Ce n'est pas une accroche d'arête : **la pose se fait en Template Hammer**, comme le template d'origine.

| Niveau | Contenu repris | Phase |
|---|---|---|
| 1 (Z0 → 300) | 17 murs extérieurs, 1 porte secrète d'entrée (θ ≈ 26°), 2 portes secrètes intérieures (au centre et en (259,8 ; −150)), 1 escalier, 1 coffre | P2 |
| plancher Z300 | 40 plafonds triangles + 5 plafonds (avec la trémie de l'escalier) | P3 |
| 2 (Z300 → 600) | 18 murs | P3 |

**Le centre du cercle.** Les deux portes secrètes intérieures forment la **cage d'escalier**, une cellule de 300 × 300 centrée en (129,9 ; −75) dont les axes sont tournés de −30°. La porte au centre exact (0 ; 0) en est un côté.

**Orientation.**
- Elle reste celle de l'export (`coeur_rotation = 0`) : les murs du Coeur Base restent parallèles aux arêtes de l'étoile, et son entrée regarde θ ≈ 26°, entre le réplicateur (0°) et le Tek Generator des ateliers (60°).
- `--coeur-rotation` permet de le tourner. Utilisez un multiple de 60° pour garder ce parallélisme ; par exemple 240° oriente l'entrée vers 266°, dans l'axe du sas et des portes à 270°.

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

- **48 positions par niveau** (12 côtés × 4), **10 niveaux** de Z0 à Z3000, soit 464 murs + 16 cadres de porte doubles.

| Niveau | Z | Ouvertures |
|---|---|---|
| 0 | 0 → 300 | **2 cadres doubles côté θ 90°** et **2 côté θ 270°** (positions 1-2) : hall ↔ couloir annulaire |
| 1 à 5 | 300 → 1800 | aucune |
| **6** | 1800 → 2100 | **12 cadres doubles** (position 1 de chaque côté) : mezzanine ↔ galerie de tourelles |
| 7 à 9 | 2100 → 3000 | aucune ; la reprise de toiture (module 04) s'encastre de 40 UU à Z ≈ 2960 |

## 5. Système porteur à piliers intérieurs

| Couronne | Position | Hauteur | Pièces | Rôle |
|---|---|---|---|---|
| **PA** | 12 coins de D2 : rayon 1 159,1, θ = 15° + 30°·k | Z0 → 4050 : 13 piliers + 1 demi-pilier | 156 + 12 | porte la mezzanine, puis le cône ; entoure le Coeur Base |
| **PB** | 12 coins de D1 : rayon 579,6, θ = 15° + 30°·k | Z1800 → 4650 : 9 piliers + 1 demi-pilier | 108 + 12 | porte le haut du cône ; posés sur la mezzanine, ils ne gênent ni le Coeur Base ni l'escalier |

- Il reste un jeu de 70 UU (PA) et 29 UU (PB) sous le cône. En Template Hammer, il n'a aucun effet.
- La colonnade circulaire entre le pod et les pics est décrite au module 03 §3.

## 6. Gabarits de placement des machines (hall Z0 → 1800)

Ce sont des zones de réservation, pas les cotes exactes des maillages. Elles commencent à 1 200 UU du centre, au-delà du Coeur Base et des piliers PA.

| Machine | Branche θ | Centre (x ; y) | Gabarit | Hauteur réservée | Énergie / carburant |
|---|---|---|---|---|---|
| **Réplicateur Tek** | 0° | (1 650 ; 0) | 3 × 2 fondations | 3 murs | à vérifier (Tek Generator du hall à proximité) |
| Tek Generator (ateliers) | 60° | (900 ; 1 558,8) | 1 × 1 | 1 mur | élément |
| **Forge industrielle** (ou variante « vapeur ») | 120° | (−825 ; 1 428,9) | 3 × 3 | 3 murs | carburant de la forge |
| Tek Teleporter (accès principal) | 180° | (−1 700 ; 0) | 1 × 1 | 1 mur | élément |
| **Laboratoire de chimie** | 240° | (−875 ; −1 515,5) | 2 × 1 | 2 murs | électrique |
| Stockage / Dedicated Storage | 300° | (875 ; −1 515,5) | 3 × 1 | 2 murs | — |

## 7. Mezzanine Z1800

Elle reprend le centre et les anneaux 1 à 7 en plafonds, **moins la trémie de l'escalier** : 94 plafonds + 188 plafonds triangles.

## 8. Toiture conique fermée et étanche

| Rang | Apothème du bord bas | Z bas → haut | Toits par côté | Total |
|---|---|---|---|---|
| r0 | 2 239,2 (sur le mur de pod) | 3000 → 3300 | 4 | 48 |
| r1 | 1 939,2 | 3300 → 3600 | 4 | 48 |
| r2 | 1 639,2 | 3600 → 3900 | 3 | 36 |
| r3 | 1 339,2 | 3900 → 4200 | 3 | 36 |
| r4 | 1 039,2 | 4200 → 4500 | 2 | 24 |
| r5 | 739,2 | 4500 → 4800 | 2 | 24 |
| r6 | 439,2 | 4800 → 5100 | 1 | 12 |
| capuchon + pointe | plafond centré à Z5100 + 4 demi-toits | 5100 → 5250 | — | 5 |

- Les toits se chevauchent aux 12 arêtes, comme dans les templates 563 et 717 : aucun jour.
- Le capuchon ferme l'ouverture résiduelle du rang 6, qui fait 144 UU au plus.
- Contrôle : de l'intérieur, aucune lumière ne doit passer.

## 9. Contrôles de fin de module

- [ ] Coeur Base : 35 murs, 3 portes secrètes, coffre « Matiere Premiere 1 », plancher Z300. Ses fondations ne sont pas posées (l'étoile les remplace).
- [ ] 6 escaliers empilés de Z0 à Z1800 ; la trémie de la mezzanine est ouverte au-dessus.
- [ ] 6 murs libres sous la mezzanine autour du Coeur Base.
- [ ] 4 cadres doubles au sol (θ 90° / 270°) et 12 à Z1800.
- [ ] 24 colonnes de piliers PA/PB.
- [ ] Cône : 228 toits + capuchon + 4 demi-toits, sans jour.
