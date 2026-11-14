# Mod « Couleurs génétiques » : étude technique de la coloration native d'ASA

Projet : potions qui changent les **Color IDs** d'un dinosaure apprivoisé dans ARK: Survival Ascended, de façon permanente et **transmissible par la reproduction native**.
Première mission : comprendre le système natif avant de créer quoi que ce soit. Rien n'est encore créé dans le DevKit.

## 0. Ce qui a été examiné, et comment lire ce document

**Fichiers du projet** : le dépôt ne contient pas encore de fichier de mod (le reste du dépôt concerne la forteresse et ses templates). Il n'y a donc rien à analyser de ce côté.

**Source principale** : les en-têtes C++ d'**AsaApi** (API serveur d'ASA, `github.com/ArkServerApi/AsaApi`). Ils sont générés à partir des symboles de l'exécutable du serveur ASA. Ils donnent, pour chaque classe du jeu, le **nom exact** des champs et des fonctions, leurs **types** et leurs **paramètres**. Les lignes utiles sont recopiées dans [`references/AsaApi_extraits_couleurs.txt`](references/AsaApi_extraits_couleurs.txt).

Limite importante : ces en-têtes prouvent qu'une fonction **existe dans le jeu**, mais pas qu'elle est **exposée en Blueprint** dans le DevKit. Ça, seul le DevKit peut le dire (étape 0 ci-dessous).

**Sources secondaires** : les wikis et pages de mods (ark.wiki.gg, CurseForge, arkserverapi.wiki) ne sont pas joignables depuis mon environnement. Les règles d'hérédité et les plages d'ID viennent donc de résultats de recherche (sites communautaires). Elles sont signalées comme telles.

| Repère | Signification |
|---|---|
| ✅ | vérifié dans les en-têtes ASA (nom, type, paramètres) |
| ⚠️ | à confirmer dans le DevKit (exposition Blueprint, nom exact du nœud) |
| 🧪 | à confirmer en jeu par un test |
| 📖 | source communautaire, non vérifiée ici |
| ❌ | à ne pas utiliser pour ce mod |

---

## 1. Comment ARK stocke les couleurs d'un dinosaure

Les couleurs sont des **numéros** (Color IDs), pas des couleurs RVB. Le dinosaure garde **un numéro par région**.

| Donnée (classe `APrimalDinoCharacter`) | Type | Rôle |
|---|---|---|
| `ColorSetIndices` ✅ | 6 octets (`uint8[6]`, valeurs 0 à 255) | **le Color ID de chaque région** : c'est la donnée à modifier |
| `ColorSetNames` ✅ | 6 `FName` | un nom par région (rôle exact non vérifié : probablement le nom de la couleur ou de la région pour l'affichage) |
| `RandomColorSetsMale` / `RandomColorSetsFemale` / `SpawnerColorSets` ✅ | classe `UPrimalColorSet` | les jeux de couleurs **tirés à l'apparition** d'un sauvage (palette de l'espèce) |
| `bUseColorization` ✅ | booléen | l'espèce utilise la colorisation |

La **palette** (le RVB de chaque ID) est globale, dans `UPrimalGameData` : `ColorDefinitions` et `MasterColorTable` ✅, avec `GetColorForDefinition(int DefinitionIndex)` ✅.

L'apparence est **calculée à partir des IDs** : `SetupColorization()`, `RefreshColorization(bool bForceRefresh)`, `ReassertColorization()` ✅. Le matériau du dinosaure n'est qu'un affichage des 6 numéros. Changer le matériau ne change pas les numéros, et donc rien de ce qui est sauvegardé ou transmis.

**Persistance** : en jeu normal, les couleurs d'un dinosaure survivent au redémarrage, au cryopod et au transfert. Comme `ColorSetIndices` est le seul stockage de couleur propre au dinosaure trouvé dans sa classe, c'est lui qui est sauvegardé. Modifier ce tableau, c'est modifier ce qui est sauvegardé. 🧪 À prouver par le test de l'étape 4.

**Trois systèmes à ne pas confondre avec les Color IDs** :

- ❌ La **peinture** (pinceau, pulvérisateur et teintures) : `AllowPaintingColorRegions`, `PaintingAllowedUVRanges`, `EnablePaintMode` ✅. C'est une texture peinte par-dessus, pas un Color ID. Elle n'est pas héritée.
- ❌ Le **buff de couleur** `ColorOverrideBuff` ✅ : un buff qui remplace les couleurs à l'affichage pendant un temps (`ColorOverrideBuffDeactivateTime`). Il est temporaire et visuel.
- Les **couleurs d'objets** (`UPrimalItem.ItemColorID`, `int16[6]`) ✅ : elles concernent les objets et les structures, pas les dinosaures.

## 2. Les six régions de couleur

- Les régions sont numérotées de **0 à 5** : c'est l'indice du tableau `ColorSetIndices`.
- Chaque espèce décide **quelles régions elle utilise** et **ce que chacune colore** (corps, ventre, crête, motifs…). Une espèce peut en utiliser moins de six.
- `GetUsesColorizationRegion(int RegionIndex)` ✅ indique si l'espèce utilise une région.
- Dans une région **non utilisée**, l'ID peut être écrit mais rien ne change à l'écran (📖 c'est aussi ce que constatent les joueurs avec la commande admin).
- Pour le Rex, les régions utilisées seront relevées au test de l'étape 1.

## 3. Comment modifier un Color ID depuis un Blueprint

| Fonction (classe `APrimalDinoCharacter`) | Existe dans ASA | Exposée en Blueprint | Verdict |
|---|---|---|---|
| `ForceUpdateColorSets(int ColorRegion, int ColorSet)` | ✅ | ⚠️ à confirmer | **candidate n° 1** : change **une région** ; c'est la fonction qu'appellent les plugins serveur pour recolorer un dino (plugin DinoColors, ASE : une boucle de 0 à 5 sur `ForceUpdateColorSets_Implementation(i, couleur)`) |
| `MulticastUpdateAllColorSets(Color0 … Color5)` | ✅ | ⚠️ | d'après son nom, **diffuse** les 6 couleurs aux clients ; ne garantit pas l'écriture côté serveur : pas notre fonction principale |
| `SetColorizationData(TArray<uint8>)` / `GetColorizationData()` | ✅ | ⚠️ | lecture et écriture de toutes les couleurs d'un coup ; format exact inconnu : utile plus tard pour **copier une configuration**, après test |
| `CopyColorizationFromDino(APrimalDinoCharacter* OtherDino)` | ✅ | ⚠️ | copie les couleurs d'un autre dino : utile plus tard |
| `BPRefreshColorization()` / `RefreshColorization(bool)` | ✅ | ⚠️ | recalcule l'affichage, au besoin, après le changement |
| `ClearColorSetIndices()` | ✅ | ⚠️ | remet les couleurs à zéro : pas pour nous |
| Écrire directement la variable `ColorSetIndices` | ✅ (la variable existe) | ⚠️ | déconseillé : on contournerait la mise à jour de l'affichage et la diffusion aux clients |
| `SetTargetDinoColor(int ColorRegion, int ColorID)` | ✅ mais dans `UShooterCheatManager` | ❌ | **commande admin**, pas une fonction Blueprint : elle n'existe que dans le gestionnaire de triche d'un joueur admin et vise ce qu'il regarde. Le nœud « Execute Console Command » ne convient pas non plus (il faut être admin). On s'en sert **uniquement pour les tests** |

`ForceUpdateColorSets` existe aussi en version `ForceUpdateColorSets_Implementation`. Ce suffixe indique une fonction Unreal (UFUNCTION) à implémentation native : soit un événement natif Blueprint, soit une fonction réseau. Elle est donc probablement visible en Blueprint, mais ce n'est **pas prouvé** tant qu'on ne l'a pas vue dans le DevKit.

## 4. La fonction qui applique une couleur à un dinosaure ciblé

Proposition : **`ForceUpdateColorSets` appelée une fois par région** (6 appels au plus), **sur le serveur**, sur la référence du dinosaure.
Le « ciblage » ne passe pas par la visée du joueur : le dinosaure est **le propriétaire de l'inventaire** dans lequel la potion est utilisée (voir l'architecture, partie 8).

Si `ForceUpdateColorSets` n'est pas exposée dans le DevKit, les solutions de repli, dans l'ordre, sont `SetColorizationData`, puis l'écriture de la variable suivie de `BPRefreshColorization`. On ne choisira qu'après l'étape 0.

## 5. La modification est-elle enregistrée dans les données héritables ?

Ce qui est vérifié ✅ :

1. La reproduction transporte les couleurs **sous la même forme que le dinosaure** : 6 octets.
   - Sur la mère pendant la gestation : `GestationEggColorSetIndices` (`uint8[6]`).
   - Sur l'œuf : `UPrimalItem.EggColorSetIndices` (`uint8[6]`).
   - À la naissance : `StaticCreateBabyDino_v2(…, EggColorSetIndices, …)` crée le bébé à partir de ce tableau.
2. Dans la classe du dinosaure, il n'existe **pas d'autre tableau de couleurs** (pas de « couleurs génétiques » séparées des couleurs affichées). Les couleurs de l'œuf ne peuvent donc venir que des `ColorSetIndices` des parents.

Ce qui reste à prouver :

- 📖 Les couleurs posées par la commande admin `SetTargetDinoColor` sont transmises aux petits (plusieurs guides communautaires le disent).
- 🧪 `ForceUpdateColorSets` écrit bien dans `ColorSetIndices`. Son nom et son usage dans les plugins serveur le montrent, mais son code n'est pas lisible. La preuve sera faite par la reproduction (étape 4).

**Piège à retenir** : les couleurs du petit sont **copiées au moment de l'accouplement** (dans `GestationEggColorSetIndices` ou dans l'œuf). Une femelle déjà fécondée ou un œuf déjà pondu garde les anciennes couleurs. La potion doit être utilisée **avant** l'accouplement.

## 6. Comment les couleurs passent aux bébés

- **Moment** : à l'accouplement (`UpdateMating`, `DoMate` ✅), le jeu calcule les 6 couleurs du petit et les range dans l'œuf (`SpawnEgg` ✅ → `EggColorSetIndices`) ou dans la gestation (`GestationEggColorSetIndices`). À l'éclosion ou à la naissance, `StaticCreateBabyDino_v2` les applique au bébé.
- **Règle** 📖 : pour **chaque région, indépendamment**, le petit prend la couleur du père ou celle de la mère, environ une chance sur deux.
- **Mutations** : les compteurs existent (`RandomMutationsMale`, `RandomMutationsFemale`, `GestationEggNumberOfMutationsApplied` pour 12 stats) ✅. 📖 Une mutation ajoute des niveaux à une stat **et change la couleur d'une région au hasard**. Le mod ne touche à aucun de ces compteurs, donc les mutations continuent de fonctionner. 🧪 À vérifier à l'étape 4.
- **Bébés sauvages d'ASA** : `SetupWildBaby_SetFakeInheritedColorsFromOneParent` ✅ donne à un bébé sauvage les couleurs d'un seul parent. Ce n'est pas notre cas (dinos apprivoisés), mais ça confirme que l'hérédité lit les couleurs des parents.

Conclusion : **pas besoin de système génétique parallèle**. Si les 6 octets du parent sont changés, la reproduction native fait le reste.

## 7. Limites, en particulier pour les dinos moddés

- **Région non utilisée** : l'octet est écrit (et transmis) sans rien changer à l'écran. Je propose de **n'écrire que les régions utilisées** par l'espèce (`GetUsesColorizationRegion`, si elle est exposée). On garde ainsi des données « comme le jeu les produirait ».
- **Espèce sans colorisation** (`bUseColorization` faux) ou **matériau qui ne lit pas les couleurs standard** (certains dinos moddés, variantes à effets : émissifs, camouflage…) : les données changent, mais pas forcément l'apparence. À vérifier au cas par cas.
- **Mods qui imposent leurs couleurs** dans leur propre Blueprint (à l'apparition, à l'apprivoisement, à la sortie du cryopod) : ils peuvent écraser nos couleurs. Notre mod ne peut rien y faire.
- **Espèces qui ne se reproduisent pas** (`bPreventMating` ✅) : pas d'hérédité possible.
- **Plage d'ID** : un octet, de 0 à 255 ✅. 📖 0 = pas de couleur ; environ 1 à 100 = couleurs de dinos ; environ 128 à 254 = teintes de teinture (« Coloring »), **numérotées autrement qu'en ASE** (un guide donne le rouge de teinture à 212 en ASE et à 131 en ASA) ; 255 à éviter. Les ID de chaque potion seront choisis par un essai en jeu, pas recopiés d'une liste ASE.
- **Partie non dédiée** (hôte + client) : 📖 un mod ASA de coloration (Dino Painter) indique qu'il ne marche pas dans ce mode. On testera ce cas en plus du solo et du serveur dédié.

## 8. Architecture proposée

```
PrimalItemConsumable_PotionCouleur_Base   (parent : classe de consommable vanilla, à confirmer à l'étape 0)
│  Réglages : utilisable dans l'inventaire d'un dino, consommé à l'utilisation
│  Variable  CouleursRegions : tableau de 6 entiers (-1 = ne pas toucher la région)
│  Fonction  PeutColorer(Dino, Joueur) -> booléen        (apprivoisé, vivant, même tribu)
│  Fonction  AppliquerCouleurs(Dino, Couleurs) -> booléen (la SEULE qui écrit des couleurs)
│  Événement d'utilisation (à identifier à l'étape 2) :
│      serveur seulement -> dino = propriétaire de l'inventaire -> PeutColorer -> AppliquerCouleurs
│
├── PrimalItemConsumable_PotionCouleur_Rouge   (enfant SANS graphe : 6 x l'ID rouge, nom, icône)
├── … Bleue, Verte, Jaune, Noire, Blanche, Violette, Orange, Rose, Dorée   (plus tard, même principe)
├── plus tard : Bicolore = un autre enfant, avec un autre tableau (ex. [rouge, noir, rouge, noir, -1, -1])
├── plus tard : Kit = un objet qui donne plusieurs potions
└── plus tard : Échantillon = lit les 6 IDs d'un dino, les garde dans l'objet, les rend avec AppliquerCouleurs
```

**Pourquoi utiliser la potion dans l'inventaire du dinosaure** (comme un objet vanilla qu'on donne à un dino) :

- le serveur sait **exactement** quel dinosaure est visé (le propriétaire de l'inventaire) : pas de visée, pas de trace, pas de décalage réseau ;
- le jeu limite déjà **nativement** l'accès à l'inventaire d'un dinosaure (en général à sa tribu). C'est une première barrière de permission, et `PeutColorer` en ajoute une seconde ;
- l'utilisation d'un objet est **exécutée par le serveur** (`ServerRequestInventoryUseItem` → `ServerUseInventoryItem` ✅) : on écrit les couleurs côté serveur, et le jeu les diffuse aux clients.

**Candidats natifs pour l'événement d'utilisation** (`UPrimalItem`) ✅, ⚠️ exposition à confirmer :

- `BlueprintUsed()` : événement appelé quand l'objet est utilisé ;
- `BPPrimalDinoCharacterConsumedItem(APrimalDinoCharacter* DinoCharacter)`, activé par la case `bUseBPPrimalDinoCharacterConsumedItem` : il reçoit **directement le dinosaure**. C'est le plus prometteur ;
- `BPCanUse(bool bIgnoreCooldown)` (case `bBPCanUse`) : pour refuser l'utilisation avant consommation ;
- réglages de l'objet : `bAllowUseInInventory`, `bAllowRemoteUseInInventory`, `bConsumeItemOnUse`, `bPreventDinoAutoConsume` (pour que le dino ne la mange pas tout seul) ;
- pour retrouver le dinosaure ou le joueur : `OwnerInventory`, `LastOwnerPlayer`.

**Candidats pour les permissions** ✅, ⚠️ exposition à confirmer : `BPIsTamed()`, `TamingTeamID` comparé à l'équipe du joueur (le champ d'équipe habituel d'ARK, `TargetingTeam`, n'apparaît pas dans ces en-têtes : à chercher dans le DevKit), `CanOrder(APrimalCharacter* FromCharacter, bool bBuildingStructures)` (respecte les rangs de tribu), et `AllowColoringBy(APlayerController* ForPC, UObject* anItem)`, la vérification native utilisée pour la coloration par un joueur avec un objet.

**Solutions écartées** :

| Solution | Raison |
|---|---|
| Modifier le matériau | ❌ visuel seulement, ni sauvegardé ni transmis |
| Buff de couleur (`ColorOverrideBuff`) | ❌ temporaire |
| Commande admin (`SetTargetDinoColor`) | ❌ réservée aux admins ; utile seulement pour tester |
| Système génétique maison | ❌ inutile : la reproduction native copie déjà les 6 octets |
| Potion utilisée depuis l'inventaire du joueur en visant le dino | plus complexe (trace, réseau) et moins sûr |

## 9. Plan des étapes (une à la fois, avec ta validation entre chaque)

| Étape | Objectif | Résultat attendu |
|---|---|---|
| **0** | Vérifier dans le DevKit quels nœuds existent vraiment (rien à créer qu'un Blueprint de brouillon) | liste des nœuds disponibles, avec leurs noms exacts |
| **1** | Prouver l'hérédité native **sans mod** : 2 Rex vanilla, commande admin, reproduction | un bébé qui a reçu une couleur posée par commande |
| 2 | Créer le Blueprint parent et identifier l'événement d'utilisation (Print String côté serveur) | savoir quel événement se déclenche, et où |
| 3 | `PeutColorer`, `AppliquerCouleurs`, potion rouge enfant | un Rex devient rouge |
| 4 | Persistance et génétique : déconnexion, cryopod, redémarrage, reproduction, mutations | bébés rouges, mutations normales |
| 5 | Multijoueur : serveur dédié, partie non dédiée, autre tribu (refus) | aucun écart client / serveur |
| 6 | Les 9 autres potions (enfants), puis bicolores, kits, échantillons | — |

### Étape 0 : à faire dans le DevKit (vérification seulement)

1. Dans le **Content Browser**, dans le dossier de ton mod, crée un dossier `_Brouillon`. Clic droit → **Blueprint Class** → déplie **All Classes** → tape `PrimalItem`. **Note (ou fais une capture de) toutes les classes proposées** qui contiennent `Consumable`.
2. Cherche dans le Content Browser un consommable vanilla qu'on utilise dans l'inventaire d'un dino (par exemple `Mutagen`, s'il existe dans ton DevKit). Ouvre-le et note :
   - **Class Settings** → *Parent Class* ;
   - **Class Defaults** : les cases cochées parmi *Allow Use In Inventory*, *Allow Remote Use In Inventory*, *Consume Item On Use*, *Use BP Primal Dino Character Consumed Item*, *Prevent Dino Auto Consume*, *BP Can Use* ;
   - **Event Graph** : les événements utilisés.
3. Crée dans `_Brouillon` un Blueprint enfant de la classe consommable trouvée (nom : `BP_Brouillon_Test`). Dans son Event Graph : clic droit → **décoche « Context Sensitive »** → cherche un par un : `Force Update Color Sets`, `Color Set Indices`, `Colorization Data`, `Uses Colorization Region`, `Refresh Colorization`, `Copy Colorization`, `Allow Coloring By`, `Can Order`, `Is Tamed`, `Targeting Team`, `Owner Inventory`, `Last Owner Player`. Pour chacun : trouvé ou pas ? Si trouvé, pose-le et **survole-le** : l'info-bulle donne la classe cible (« Target is … ») et les paramètres. Une capture par nœud suffit.
4. Dans le panneau **My Blueprint** → *Functions* → **Override** : capture de la liste des événements proposés (cherche `Blueprint Used`, `Primal Dino Character Consumed Item`, `BP Can Use`, `On Item Consumed`).

Envoie-moi les captures ou la liste : la suite (nœuds exacts, branchements) sera écrite sur ces noms-là, pas sur des suppositions.

### Étape 1 : test en jeu, sans mod

Le but est de prouver, avant d'écrire une ligne de Blueprint, que la reproduction native transmet une couleur changée après coup.

1. Partie solo ou serveur local **sans aucun mod**, triche activée. Pour accélérer, mets au maximum les réglages d'accouplement, d'éclosion et de croissance (intervalle d'accouplement, vitesse d'éclosion, vitesse de maturation des bébés).
2. Fais apparaître des Rex apprivoisés jusqu'à avoir un mâle et une femelle : `cheat SummonTamed Rex_Character_BP_C` (le nom de la commande est vérifié ✅, le nom de classe du Rex est celui habituel d'ARK, à confirmer).
3. Fais une capture des deux Rex **avant**.
4. En regardant la **femelle**, pour chaque région de 0 à 5 : `cheat SetTargetDinoColor <région> 1`. En regardant le **mâle** : `cheat SetTargetDinoColor <région> 2`. 📖 Les listes publiques donnent 1 = rouge et 2 = bleu ; ce qui compte, c'est que les deux couleurs soient bien différentes. Note les régions qui ne changent rien à l'écran : ce sont les régions non utilisées par le Rex.
5. Active l'accouplement sur les deux, laisse-les s'accoupler, fais éclore l'œuf (`cheat HatchEgg` existe ✅ ; son usage exact est à essayer), puis recommence pour avoir **au moins 5 bébés**.
6. **Résultat attendu** : chaque région des bébés est rouge (mère) ou bleue (père), jamais la couleur d'origine des parents. Si c'est le cas, l'hérédité native lit bien les Color IDs modifiés.

---

*Sources : en-têtes AsaApi (`APrimalDinoCharacter.h`, `APrimalCharacter.h`, `UPrimalItem.h`, `UShooterCheatManager.h`, `UPrimalGameData.h`, `UPrimalInventoryComponent.h`, `AShooterPlayerController.h`), extraits dans `references/` ; plugin DinoColors (Michidu/Ark-Server-Plugins, ASE) ; résultats de recherche sur les Color IDs, l'hérédité des couleurs et les mods de coloration d'ASA (sites communautaires, non consultés directement).*
