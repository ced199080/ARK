# Module 02 — Pod central de production (Ø15, hall de 6 murs, cône étanche)

Template : `templates/02_pod_central.json`. Il est réparti dans les phases **P2** (mur niveaux 0-5, piliers PA bas), **P3** (mezzanine) et **P6** (mur niveaux 6-9, piliers hauts, cône, capuchon).
Coordonnées : `donnees/02_pod_central.csv`. Plan : `plans/plan_pod.png`.

![Plan du pod](plans/plan_pod.png)

## 1. Volumes

| Élément | Cotes | Remarque |
|---|---|---|
| Emprise | Dodécagone **D4** : apothème 2 239,2 UU, Ø 14,93 fondations entre plats, 15,45 entre coins | C'est l'étoile existante (anneaux 1 à 7) |
| **Hall d'atelier** | Z0 → Z1800 : **6 murs pleins de hauteur libre** | Aucun plancher intermédiaire |
| Mezzanine / étage technique | Z1800 → Z3000 (4 murs) | Plancher au niveau de la galerie de tourelles L1 |
| Cône | Z3000 → Z5100, 7 rangs de toits à 45° | Fermé et étanche |
| Capuchon et pointe | plafond à Z5100 + 4 demi-toits → sommet Z5250 | Rien de plat sur lequel se poser |

## 2. Mur de pod (D4)

- **48 positions par niveau** (12 côtés × 4), sur **10 niveaux** de Z0 à Z3000, soit 480 positions : 464 murs + 16 cadres de porte doubles.
- Chaque mur s'accroche sur l'arête de l'anneau 7, ou sur le mur du dessous.

| Niveau | Z | Ouvertures |
|---|---|---|
| 0 | 0 → 300 | **2 cadres doubles côté θ 90°** et **2 côté θ 270°** (positions 1 et 2 du côté) → hall ↔ couloir annulaire |
| 1 à 5 | 300 → 1800 | aucune |
| **6** | 1800 → 2100 | **12 cadres doubles**, position 1 de chaque côté → mezzanine ↔ galerie de tourelles L1 |
| 7 à 9 | 2100 → 3000 | aucune ; la reprise de toiture du module 04 s'encastre de 40 UU dans le niveau 9, à Z ≈ 2960 |

Exemple, côté θ = 0° (x = 2 239,2) : les 4 murs sont centrés en y = −450, −150, +150, +450, avec z template = Z_bas + 240 et yaw 0°.
Pour un autre côté k, appliquez une rotation de 30·k°.

## 3. Système porteur à piliers intérieurs

Les piliers sont posés aux **coins des dodécagones** D2 et D1, qui sont des sommets du pavage. Chaque pilier s'accroche donc sur un coin de fondation, puis sur un coin de plafond.

| Couronne | Position | Hauteur | Pièces | Rôle |
|---|---|---|---|---|
| **PA** | 12 coins de D2 : rayon 1 159,1 UU, θ = 15° + 30°·k | Z0 → **4050** : 13 piliers + 1 demi-pilier chacun | 156 piliers + 12 demi-piliers | Porte la mezzanine (Z1800), puis le cône |
| **PB** | 12 coins de D1 : rayon 579,6 UU, θ = 15° + 30°·k | Z1800 → **4650** : 9 piliers + 1 demi-pilier chacun | 108 piliers + 12 demi-piliers | Porte le haut du cône ; posés sur la mezzanine, ils laissent le hall libre |

Coordonnées du premier pilier PA (θ = 15°) : (1 119,6 ; 300,0). Pilier PB (θ = 15°) : (559,8 ; 150,0).

**Jeu sous le cône.** Le cône passe à Z 4 119,6 au-dessus de PA et à Z 4 679,4 au-dessus de PB, soit 70 et 29 UU au-dessus du dernier demi-pilier. En Template Hammer, ce jeu n'a aucun effet. En pose manuelle, une accroche toit-sur-pilier peut l'exiger : terminez alors chaque colonne par un pilier fin (Pillar Thin).

**Couloir annulaire au sol** (entre D4 et D5, sous la galerie) : il est porté par le mur de pod et le fût (module 04). Il ne demande aucun pilier.

## 4. Gabarits de placement des machines (hall Z0 → 1800)

Ce sont des **zones de réservation**, pas les cotes exactes des maillages. Chaque gabarit est un rectangle aligné sur sa branche θ. Sa largeur est mesurée tangentiellement, sa profondeur radialement, et il laisse ≥ 80 UU de passage aux piliers PA et ≥ 140 UU au mur.

| Machine | Branche θ | Centre (x ; y) | Gabarit (largeur × profondeur) | Hauteur réservée | Énergie / carburant |
|---|---|---|---|---|---|
| **Réplicateur Tek** | 0° | (1 650 ; 0) | 3 × 2 fondations (900 × 600) | 3 murs | à vérifier en jeu (Tek Generator du hall à 1 800 UU) |
| Tek Generator (ateliers) | 60° | (900 ; 1 558,8) | 1 × 1 | 1 mur | élément |
| **Forge industrielle** (ou variante « vapeur » du pack Steampunk) | 120° | (−825 ; 1 428,9) | 3 × 3 (900 × 900) | 3 murs | carburant de la forge ; pas de câble |
| Tek Teleporter (accès principal) | 180° | (−1 700 ; 0) | 1 × 1 | 1 mur | élément |
| **Laboratoire de chimie** | 240° | (−875 ; −1 515,5) | 2 × 1 (600 × 300) | 2 murs | électrique (Tek Generator du hall ou câble) |
| Stockage / Dedicated Storage | 300° | (875 ; −1 515,5) | 3 × 1 (900 × 300) | 2 murs | — |

Notes d'aménagement :
- Les gabarits sont sur les **branches de carrés** (E0). Les machines s'y posent donc sur des fondations carrées, et l'on évite de les centrer sur un triangle.
- Les portes du hall (θ 90° et 270°) tombent entre deux gabarits : la circulation reste libre.
- La forge et le réplicateur dépassent largement 1 mur de haut. Les 6 murs libres laissent de la place pour une cheminée, un ascenseur ou un dino de manutention.
- **Trémie centrale.** L'hexagone central de la mezzanine (côté 300, soit 600 entre coins opposés) reste ouvert : posez un ascenseur (Elevator Track) ou une échelle de Z0 à Z1800.

## 5. Mezzanine Z1800

- Elle reprend les anneaux 1 à 7 en plafonds (**96 plafonds + 186 plafonds triangles**) et laisse ouvert l'hexagone central.
- Elle se prolonge sans marche par le plancher de galerie L1 (anneaux 8-9, module 04) au travers des 12 cadres doubles du niveau 6.
- Usage : coffre, réserves de munitions au plus près des tourelles, Tek Generators de galerie (module 05 §7).

## 6. Toiture conique fermée et étanche

Chaque rang est un dodécagone de toits. Son bord bas est sur l'apothème A, il monte de 300 UU vers le centre, et il compte ⌈2·A·tan 15° / 300⌉ toits par côté. Les toits se chevauchent aux 12 arêtes, comme dans les templates 563 et 717 fournis : aucun jour n'est possible.

| Rang | Apothème du bord bas (UU) | Z bas → haut | Toits par côté | Total |
|---|---|---|---|---|
| r0 | 2 239,2 (sur le mur de pod) | 3000 → 3300 | 4 | 48 |
| r1 | 1 939,2 | 3300 → 3600 | 4 | 48 |
| r2 | 1 639,2 | 3600 → 3900 | 3 | 36 |
| r3 | 1 339,2 | 3900 → 4200 | 3 | 36 |
| r4 | 1 039,2 | 4200 → 4500 | 2 | 24 |
| r5 | 739,2 | 4500 → 4800 | 2 | 24 |
| r6 | 439,2 | 4800 → 5100 | 1 | 12 |
| capuchon | plafond 300 × 300 centré, Z5100 | — | — | 1 |
| pointe | 4 demi-toits (centres à ±75 UU du centre, yaw vers le centre) | 5100 → 5250 | — | 4 |

**Étanchéité.**
- Le plafond capuchon ferme l'ouverture résiduelle du rang 6 : apothème 139,2 UU, ≤ 144 UU au coin, couverte par le carré de ±150.
- Le chevauchement aux arêtes laisse une petite lèvre de 20 à 30 UU, comme sur tous les dômes Template Hammer. Elle est trop faible pour qu'on s'y tienne.

Contrôle : depuis la mezzanine, éteignez les lumières et vérifiez qu'aucun jour n'apparaît aux arêtes.

**Glisse.** Un dino largué sur le cône descend à 45° jusqu'au mur de pod (Z3000), tombe de 40 UU sur la reprise (module 04), puis suit la chaîne de glisse décrite au module 03 §6.

## 7. Option : intégrer « Coeur Base » (template fourni)

Le template *Coeur Base* est un noyau de 2 niveaux : 35 murs, 3 portes secrètes, un escalier, un grand coffre. Son rayon maximal est de 900 UU.
- Il tient **à l'intérieur de la couronne PA** (rayon 1 159) et sous la mezzanine (son sommet est à Z600).
- Son plancher de 10 fondations suit une grille tournée de −30°, qui **chevauche les anneaux 1 à 3**. Supprimez donc ses entrées 18 à 27 (les `Floor_Metal`) avant l'import.
- Ses murs ne suivent pas les arêtes du pavage : pose en Template Hammer uniquement, centré sur la pile d'ancrage.
- Il occupe la trémie centrale : déplacez alors l'ascenseur au gabarit 300°.

## 8. Contrôles de fin de module

- [ ] 6 murs libres sous la mezzanine, partout.
- [ ] 4 cadres doubles au sol (θ 90° / 270°) et 12 à Z1800.
- [ ] 24 colonnes de piliers (12 PA depuis Z0, 12 PB depuis Z1800).
- [ ] Cône : 228 toits + capuchon + 4 demi-toits, sans jour visible de l'intérieur.
