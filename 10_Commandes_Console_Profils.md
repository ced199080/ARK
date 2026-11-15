# Module 10 — Commandes console graphiques et profils

Ce module décrit les commandes console graphiques d'**ARK: Survival Ascended** (moteur Unreal Engine 5) que vous utilisez, puis propose des profils prêts à coller dans la console, séparés par `|`.

## 1. À savoir avant de coller une ligne

1. **L'ordre compte.** Une ligne s'exécute de gauche à droite. Si une commande apparaît deux fois, c'est la dernière qui compte.
2. **Les `sg.…` réécrivent tout leur groupe.** `sg.FoliageQuality`, `sg.TextureQuality` et `sg.GlobalIlluminationQuality` remettent les variables de leur groupe à la valeur du niveau choisi. Par exemple, `sg.FoliageQuality` remet `grass.DensityScale` et `foliage.DensityScale`. Placez-les **en tête de ligne**, avant les réglages fins.
3. **`show …` et `stat fps` sont des bascules** : un appel cache, l'appel suivant réaffiche. Si la ligne est relancée, ils reviennent à l'état de départ. Dans les profils ci-dessous, ils sont mis à part.
4. **Les valeurs « d'origine »** sont celles d'Unreal Engine 5 en qualité Épique. ARK peut en changer certaines dans ses propres fichiers de qualité, et le menu Options > Graphismes les réécrit. Pour revenir **exactement** à l'origine : réappliquez vos options graphiques dans le menu, ou relancez le jeu.
5. **Durée** : tout s'efface quand vous quittez le jeu. Deux réglages ne reviennent qu'en relançant le jeu : `ark.MaxActiveDestroyedMeshGeoCollectionCount` et `wp.Runtime.OverrideRuntimeSpatialHashLoadingRange`.
6. **Serveurs** : depuis la mise à jour 35.6 (février 2024), Wildcard désactive des commandes qui donnent un avantage visuel, et en désactive d'autres au fil des patchs. Certaines lignes peuvent donc ne rien faire sur votre serveur. Voir à travers le décor (rochers, terrain, végétation) peut être considéré comme un exploit selon les règles du serveur, avec un risque de bannissement : vérifiez les règles avant d'utiliser les profils SCANNER et EFFACEMENT MAX.
7. **Commande inconnue** : une variable que le jeu ne connaît pas est ignorée, sans bloquer le reste de la ligne.

Légende de la colonne **Gain** : gain d'images par seconde quand on baisse la valeur. **Fort**, **moyen**, **faible**, **aucun** ; **coûte** veut dire que la valeur haute fait perdre des FPS.

## 2. Tableau des commandes

### 2.1 Affichage et image

| Commande | Effet | Mini | Maxi | Origine | Gain | Remarques |
|---|---|---|---|---|---|---|
| `stat fps` | Affiche les FPS et le temps d'image | — | — | caché | aucun | Bascule : un 2e appel cache le compteur |
| `t.MaxFPS` | Limite d'images par seconde | 0 (= sans limite) | pas de maxi | réglage du menu | — | En stream, une limite (ex. 120) laisse de la marge à l'encodeur |
| `r.VSync` | Synchronisation verticale | 0 | 1 | réglage du menu | — | 0 : moins de latence, risque de déchirure de l'image |
| `r.ScreenPercentage` | Résolution de rendu, en % de l'écran | 25 en pratique | 200 (au-dessus de 100 : suréchantillonnage, très lourd) | 100 (réglage « Résolution » du menu) | **fort** | Image floue sous 70. Si DLSS ou FSR est actif, c'est lui qui pilote la résolution |
| `gamma` | Luminosité de l'affichage | 0,5 | 5 | 2,2 | aucun | `gamma` sans valeur remet 2,2. Nuits et grottes plus claires ; au-dessus de 3, l'image se délave. Certains serveurs bloquent la commande |
| `r.Tonemapper.Sharpen` | Netteté de l'image | 0 | 10 | 0 | aucun | 0,5 à 1,5 : net ; 2 : halos ; 3 et plus : grain. Utile quand `r.ScreenPercentage` est sous 100 |

### 2.2 Ciel, brouillard et lumière

| Commande | Effet | Mini | Maxi | Origine | Gain | Remarques |
|---|---|---|---|---|---|---|
| `r.VolumetricCloud` | Nuages volumétriques | 0 | 1 | 1 | **moyen à fort** | 0 : ciel sans nuages volumétriques |
| `r.VolumetricFog` | Brouillard volumétrique (brume, rayons dans la brume) | 0 | 1 | 1 | moyen | 0 : vue plus dégagée |
| `r.Fog` | Brouillard de distance et de hauteur | 0 | 1 | 1 | faible | 0 : on voit plus loin et plus net |
| `r.SkyAtmosphere` | Atmosphère du ciel (couleur du ciel, voile bleuté au loin) | 0 | 1 | 1 | faible | 0 : ciel sombre ou uni, éclairage changé. Déconseillé |
| `r.LightShaftQuality` | Rayons de soleil (god rays) | 0 | 1 | 1 | faible | 2 donne la même chose que 1 |
| `r.SkylightIntensityMultiplier` | Force de la lumière ambiante du ciel | 0 | pas de maxi (5 en pratique) | 1 | aucun | Plus clair la nuit et dans l'ombre ; au-dessus de 3, le jour est surexposé |
| `r.EyeAdaptationQuality` | Exposition automatique (adaptation de l'œil) | 0 | 3 | 2 | faible | 0 : exposition figée, plus d'éblouissement en sortie de grotte, mais les grottes ne s'éclaircissent plus |

### 2.3 Post-traitement

| Commande | Effet | Mini | Maxi | Origine | Gain | Remarques |
|---|---|---|---|---|---|---|
| `r.BloomQuality` | Halo autour des lumières | 0 | 5 | 5 | faible | 0 : lumières et explosions moins éblouissantes |
| `r.LensFlareQuality` | Reflets d'objectif | 0 | 3 | 2 | faible | |
| `r.DepthOfFieldQuality` | Flou de profondeur | 0 | 4 | 2 | faible | |
| `r.MotionBlurQuality` | Flou de mouvement | 0 | 4 | 4 | faible | 0 : image nette en tournant la caméra |
| `r.MotionBlur.Amount` | Force du flou de mouvement, prioritaire sur le jeu | 0 | 1 | −1 (= réglage du jeu) | faible | Doublon de `r.MotionBlurQuality 0` |
| `r.PostProcessing.DisableMaterials` | Coupe les matériaux de post-traitement (filtres plein écran du jeu) | 0 | 1 | 0 | faible à moyen | Les effets coupés dépendent des cartes. Sans valeur, la commande affiche seulement la valeur actuelle |

### 2.4 Ombres

| Commande | Effet | Mini | Maxi | Origine | Gain | Remarques |
|---|---|---|---|---|---|---|
| `r.ShadowQuality` | Qualité des ombres dynamiques | 0 | 5 | 5 | **fort** | 0 : plus d'ombres dynamiques ; joueurs et dinos plus faciles à voir dans les zones ombragées |
| `r.Shadow.Virtual.Enable` | Ombres virtuelles (VSM), très lourdes | 0 | 1 | 1 | **fort** | 0 : retour aux ombres en cascades |
| `r.Shadow.CSM.MaxCascades` | Nombre de cascades d'ombres du soleil | 0 | 10 (le moteur accepte 16) | selon la qualité des ombres | moyen | Ne sert que si `r.Shadow.Virtual.Enable 0`. 0 : plus d'ombre du soleil |
| `r.DistanceFieldShadowing` | Ombres lointaines (champs de distance) | 0 | 1 | 1 | moyen | |
| `r.ContactShadows` | Petites ombres de contact | 0 | 1 | 1 | faible | |
| `show DynamicShadows` | Affiche ou cache toutes les ombres dynamiques | — | — | affiché | **fort** | Bascule. Doublon de `r.ShadowQuality 0` |

### 2.5 Éclairage global et reflets (Lumen)

| Commande | Effet | Mini | Maxi | Origine | Gain | Remarques |
|---|---|---|---|---|---|---|
| `sg.GlobalIlluminationQuality` | Groupe qualité de l'éclairage global | 0 | 4 (cinéma) | réglage du menu (3 = Épique) | **fort** | Réécrit Lumen et l'occlusion ambiante : à mettre en tête de ligne. En Bas et Moyen, Lumen est en général coupé |
| `r.DynamicGlobalIlluminationMethod` | Méthode d'éclairage indirect : 0 aucune, 1 Lumen, 2 SSGI (écran) | 0 | 2 | 1 (Lumen) | **fort** | 0 : la lumière du ciel n'est plus bloquée par les parois, les intérieurs et les grottes deviennent plus clairs mais plats |
| `r.Lumen.DiffuseIndirect.Allow` | Autorise l'éclairage indirect Lumen | 0 | 1 | 1 | **fort** | Même effet que la ligne au-dessus, côté Lumen |
| `r.Lumen.Reflections.Allow` | Reflets Lumen | 0 | 1 | 1 | moyen | 0 : reflets remplacés par les reflets écran (SSR), s'ils sont actifs |
| `r.SSR.Quality` | Reflets écran | 0 | 4 | 3 | faible à moyen | Sert surtout quand les reflets Lumen sont coupés |
| `r.AOQuality` | Occlusion ambiante par champs de distance (assombrit les coins) | 0 | 2 | 2 | moyen | Sert surtout sans Lumen. 0 : coins et dessous de structures plus clairs |

### 2.6 Herbe et végétation

| Commande | Effet | Mini | Maxi | Origine | Gain | Remarques |
|---|---|---|---|---|---|---|
| `sg.FoliageQuality` | Groupe qualité de la végétation | 0 | 4 (cinéma) | réglage du menu (3 = Épique) | moyen | Remet `grass.DensityScale` et `foliage.DensityScale` : à mettre en tête de ligne |
| `grass.Enable` | Herbe du terrain | 0 | 1 | 1 | **moyen à fort** | 0 : plus d'herbe, joueurs couchés visibles |
| `grass.DensityScale` | Densité de l'herbe | 0 | 1 | 1 | moyen | |
| `grass.SizeScale` | Taille de l'herbe (variable propre à ARK) | 0 | 1 | 1 | faible | 0,5 : herbe rase. Inutile avec `grass.Enable 0` |
| `grass.CullDistanceScale` | Distance d'affichage de l'herbe | 0 | 1 (plus : plus loin, coûte) | 1 | moyen | |
| `foliage.DensityScale` | Densité des plantes peintes qui acceptent la réduction (petites plantes, buissons) | 0 | 1 | 1 | moyen | Les arbres ne sont en général pas concernés |
| `foliage.CullAll` | Cache toute la végétation peinte : arbres, buissons, souvent des rochers | 0 | 1 | 0 | **fort** | Avantage visuel très net, donc parmi les commandes visées par Wildcard. Les collisions restent : on bute sur des arbres invisibles |
| `foliage.CullDistanceScale` | Distance d'affichage de la végétation | 0 | 1 | 1 | moyen | **À vérifier** : pas sûr que cette variable existe dans ARK |
| `show InstancedFoliage` | Affiche ou cache la végétation peinte | — | — | affiché | **fort** | Bascule. Proche de `foliage.CullAll 1` |
| `show InstancedGrass` | Affiche ou cache l'herbe | — | — | affiché | moyen | Bascule. Doublon de `grass.Enable 0` |
| `show InstancedStaticMeshes` | Affiche ou cache tous les objets instanciés (rochers et décor répété, parfois des éléments de structures) | — | — | affiché | moyen | Bascule. À tester : si des structures disparaissent aussi, relancez la commande |

### 2.7 Distance, détail et textures

| Commande | Effet | Mini | Maxi | Origine | Gain | Remarques |
|---|---|---|---|---|---|---|
| `r.ViewDistanceScale` | Distance à laquelle les objets disparaissent (multiplicateur) | 0,4 en pratique | pas de maxi (3 en pratique) | 1 | **coûte au-dessus de 1** | Au-dessus de 1 : structures et objets visibles plus loin. Sous 1 : gain de FPS, mais ils disparaissent plus tôt |
| `r.StaticMeshLODDistanceScale` | Distance de passage aux modèles simplifiés (LOD) | 0,5 en pratique | 4 en pratique | 1 | faible à moyen | Au-dessus de 1 : simplifie plus tôt (gain). Ne touche pas les objets Nanite |
| `r.Nanite.MaxPixelsPerEdge` | Finesse des modèles Nanite (taille des triangles à l'écran) | 1 en pratique | 4 en pratique (le moteur accepte beaucoup plus) | 1 | moyen | 2 : gain visible, peu de perte ; 4 : formes grossières |
| `r.DetailMode` | Petits objets de décor et effets de détail | 0 | 2 | 2 | faible | |
| `sg.TextureQuality` | Qualité des textures | 0 | 4 (cinéma) | réglage du menu (3 = Épique) | faible (moyen si la carte a peu de mémoire vidéo) | 0 : textures floues |
| `r.MipMapLODBias` | Biais de netteté des textures | −15 | 15 | 0 | faible | Positif : plus flou. **À vérifier** : variable de mise au point, peut être sans effet dans le jeu publié |

### 2.8 Eau

| Commande | Effet | Mini | Maxi | Origine | Gain | Remarques |
|---|---|---|---|---|---|---|
| `r.Water.SingleLayer.Reflection` | Reflets de la surface de l'eau | 0 | 1 | 1 | moyen près de l'eau | |
| `r.Water.SingleLayer` | Rendu de l'eau en couche unique | 0 | 1 | 1 | moyen près de l'eau | 0 : la surface devient transparente ou partielle |
| `r.Water.WaterMesh.EnableRendering` | Surface de l'océan et des lacs | 0 | 1 | 1 | moyen | 0 : surface invisible, on voit le fond |
| `r.Water.EnableUnderwaterPostProcess` | Voile et teinte sous l'eau | 0 | 1 | 1 | faible | 0 : on voit loin sous l'eau |
| `r.Water.SingleLayer.OptimizedClear` | Optimisation interne du rendu de l'eau | 0 | 1 | 1 | aucun | Rien de visible : inutile |

### 2.9 Monde (World Partition) et ARK

| Commande | Effet | Mini | Maxi | Origine | Gain | Remarques |
|---|---|---|---|---|---|---|
| `wp.Runtime.HLOD` | Versions simplifiées du décor lointain (HLOD) | 0 | 1 | 1 | faible à moyen | 0 : montagnes, rochers et forêts lointains disparaissent ; les structures et créatures que le serveur vous envoie restent visibles |
| `wp.Runtime.OverrideRuntimeSpatialHashLoadingRange -range=N` | Force la distance de chargement du décor, en unités du jeu (100 = 1 m) | — | — | celle de la carte | moyen, avec des saccades | `-range=2000` : rien n'est chargé au-delà de 20 m. Risques : trous dans le décor, chutes, recalages. Retour : relancer le jeu |
| `ark.MaxActiveDestroyedMeshGeoCollectionCount` | Nombre de débris de destruction affichés en même temps (variable propre à ARK) | 0 | non documenté | non documentée | moyen en raid | 0 : pas de débris quand une structure ou un rocher casse. Retour : relancer le jeu |

### 2.10 Commandes de vos lignes à retirer

| Commande | Problème |
|---|---|
| `r.grass.DesityQualityLevel 0` | Faute de frappe (« Desity ») : ignorée. La variable proche, `r.grass.DensityQualityLevel`, ne sert à rien avec `grass.Enable 0` |
| `r.Color.Grading 0` | Pas une variable connue du moteur : probablement ignorée |
| `wp.Runtime.HLOD.ForceDisable 1` | Existence non vérifiée ; `wp.Runtime.HLOD 0` fait déjà le travail |
| `r.Lumen.Reflections.Contrast 0` | Inutile quand `r.Lumen.Reflections.Allow 0` est dans la même ligne |
| `r.EarlyZPass 0` | Pré-passe de profondeur (0 à 3, origine 3). Peut faire **perdre** des FPS et créer des défauts avec Nanite : à retirer |
| `r.LightCulling.Quality 0` | Tri des lumières (0 ou 1, origine 1). Gain négligeable, peut mal éclairer l'eau et le verre : à retirer |
| `r.Water.SingleLayer.OptimizedClear 0` | Rien de visible : à retirer |
| `r.PostProcessing.DisableMaterials` (sans valeur) | Affiche seulement la valeur : il faut `0` ou `1` |

## 3. Ce que font vos 11 lignes

| Ligne | Début | Profil probable | Problèmes |
|---|---|---|---|
| 1 | `r.grass.DesityQualityLevel 0 \| grass.sizeScale 0 …` | Effacement max | `r.Nanite.MaxPixelsPerEdge` 3 puis 1 puis 2 : c'est 2 qui compte. `r.DistanceFieldShadowing` 0 puis 1 : les ombres lointaines sont **réactivées**. `r.SkylightIntensityMultiplier` 5 puis 3 : c'est 3. `sg.GlobalIlluminationQuality 1` est après `r.Lumen.DiffuseIndirect.Allow 1` : c'est le groupe qui décide. 4 `show` et `stat fps` : bascules. Les 8 commandes du §2.10 |
| 2 | `r.VolumetricCloud 0 \| r.shadowquality 0 …` | Scanner | 5 commandes en double (sans conséquence). 4 `show` : bascules. `r.MipMapLODBias 0` = valeur d'origine, ne change rien |
| 3 | `Stat FPS \| … r.ScreenPercentage 75` | PvP normal | `sg.FoliageQuality 2` est **après** `grass.DensityScale 0.5` et `foliage.DensityScale 0.5` : il les remet à la valeur du groupe (0,8 dans le moteur), vos 0,5 sont perdus. `r.LightShaftQuality 2` = 1 |
| 4 | `r.VolumetricFog 0 \| r.Fog 0 \| r.Water…` | Eau translucide | Correcte |
| 5 | Reset eau | Reset eau | Remet aussi le brouillard et `gamma 2.2` : relancez ensuite votre profil |
| 6 | `Stat FPS \| … r.ScreenPercentage 100 \| Gamma 2.2` | Reset | Ne remet pas le décor lointain (`wp.Runtime.HLOD`), l'eau, la lumière du ciel (`r.SkylightIntensityMultiplier`) ni les bascules `show` |
| 7 | `Stat FPS \| … r.ScreenPercentage 100 \| Gamma 3` | Raid / ultra | Correcte ; `foliage.CullAll 1` |
| 8 | `Stat FPS \| … r.ScreenPercentage 50 \| Gamma 4` | Ultra | `r.SkyAtmosphere 0` : ciel sombre ou uni. `r.ViewDistanceScale 0.75` : objets lointains cachés plus tôt, le contraire de « visibilité max ». `r.EyeAdaptationQuality 0` : grottes plus sombres |
| 9 | `Stat FPS \| … r.ScreenPercentage 70` | Raid | `r.MipMapLODBias 1` à vérifier |
| 10 | `Stat FPS \| … r.ScreenPercentage 85` | PvP normal | Correcte ; ne touche ni aux ombres ni à Lumen (ceux du menu restent) |
| 11 | `t.MaxFPS 0 \| … Gamma 2.5` | Stream | Correcte |

Dernier point commun : à part le reset, aucune ligne ne remet le décor lointain ni l'eau. Après la ligne 1 ou 2, ils restent cachés quand vous passez à un autre profil.

## 4. Profils proposés

Chaque profil donne une valeur à **toutes** les variables du tableau ci-dessous. Vous pouvez donc passer de l'un à l'autre dans n'importe quel ordre, avec le même résultat. Les `sg.…` sont en tête, et il n'y a ni `show` ni `stat fps` dans les lignes.

Lancez `stat fps` une seule fois, à part, pour afficher le compteur.

### 4.1 Comparatif

| Variable | Stream | PvP normal | Raid PvP | Ultra PvP | Scanner | Cave | Reset |
|---|---|---|---|---|---|---|---|
| `sg.TextureQuality` | 3 | 3 | 2 | 0 | 2 | 1 | 3 |
| `sg.GlobalIlluminationQuality` | 3 | 2 | 1 | 0 | 0 | 0 | 3 |
| `r.ScreenPercentage` | 100 | 85 | 75 | 60 | 100 | 75 | 100 |
| `gamma` | 2.2 | 3 | 3 | 4 | 4 | 4 | 2.2 |
| `r.Tonemapper.Sharpen` | 0.5 | 1 | 1.5 | 2 | 1.5 | 1.5 | 0 |
| `r.VolumetricCloud` | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| `r.VolumetricFog` / `r.Fog` | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| `r.LightShaftQuality` | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| `r.SkylightIntensityMultiplier` | 1 | 1.5 | 2 | 3 | 3 | 4 | 1 |
| `r.BloomQuality` | 4 | 0 | 0 | 0 | 0 | 0 | 5 |
| `r.LensFlareQuality` | 1 | 0 | 0 | 0 | 0 | 0 | 2 |
| `r.DepthOfFieldQuality` / `r.MotionBlurQuality` | 0 | 0 | 0 | 0 | 0 | 0 | 2 / 4 |
| `r.PostProcessing.DisableMaterials` | 0 | 0 | 1 | 1 | 1 | 1 | 0 |
| Lumen (`r.DynamicGlobalIlluminationMethod`, `…DiffuseIndirect.Allow`) | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| `r.Lumen.Reflections.Allow` | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| `r.SSR.Quality` | 3 | 0 | 0 | 0 | 0 | 0 | 3 |
| `r.AOQuality` | 2 | 1 | 0 | 0 | 0 | 0 | 2 |
| `r.ShadowQuality` | 4 | 2 | 0 | 0 | 0 | 0 | 5 |
| `r.Shadow.Virtual.Enable` | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| `r.Shadow.CSM.MaxCascades` | 4 | 2 | 0 | 0 | 0 | 0 | 4 |
| `r.DistanceFieldShadowing` | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| `r.ContactShadows` | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| `grass.Enable` | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| `grass.DensityScale` / `SizeScale` / `CullDistanceScale` | 1 | 0.5 / 0.6 / 0.6 | 0 | 0 | 0 | 0 | 1 |
| `foliage.DensityScale` | 1 | 0.6 | 0.25 | 0 | 0 | 0.25 | 1 |
| `foliage.CullAll` | 0 | 0 | 0 | **1** | **1** | 0 | 0 |
| `r.ViewDistanceScale` | 1 | 1 | 1.5 | 1 | **3** | 1 | 1 |
| `r.StaticMeshLODDistanceScale` | 1 | 1.25 | 1.5 | 2 | 1 | 1.5 | 1 |
| `r.Nanite.MaxPixelsPerEdge` | 1 | 2 | 3 | 4 | 2 | 3 | 1 |
| `r.DetailMode` | 2 | 1 | 0 | 0 | 0 | 0 | 2 |
| `r.Water.SingleLayer.Reflection` | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| `wp.Runtime.HLOD` | 1 | 1 | 1 | 1 | **0** | 1 | 1 |
| `ark.MaxActiveDestroyedMeshGeoCollectionCount` | — | — | 0 | 0 | 0 | 0 | relancer le jeu |

Communs à tous : `t.MaxFPS 0`, `r.VSync 0`, `r.SkyAtmosphere 1`, `r.EyeAdaptationQuality 2`.

### 4.2 STREAM / VIDÉO — qualité préservée

Image fidèle pour les spectateurs. Seuls le flou, les ombres de contact et un peu de bloom sont réduits. Pour laisser de la marge à l'encodeur, remplacez `t.MaxFPS 0` par `t.MaxFPS 120`.

```
sg.TextureQuality 3 | sg.GlobalIlluminationQuality 3 | t.MaxFPS 0 | r.VSync 0 | r.ScreenPercentage 100 | gamma 2.2 | r.Tonemapper.Sharpen 0.5 | r.SkyAtmosphere 1 | r.VolumetricCloud 1 | r.VolumetricFog 1 | r.Fog 1 | r.LightShaftQuality 1 | r.SkylightIntensityMultiplier 1 | r.EyeAdaptationQuality 2 | r.BloomQuality 4 | r.LensFlareQuality 1 | r.DepthOfFieldQuality 0 | r.MotionBlurQuality 0 | r.PostProcessing.DisableMaterials 0 | r.DynamicGlobalIlluminationMethod 1 | r.Lumen.DiffuseIndirect.Allow 1 | r.Lumen.Reflections.Allow 1 | r.SSR.Quality 3 | r.AOQuality 2 | r.ShadowQuality 4 | r.Shadow.Virtual.Enable 1 | r.Shadow.CSM.MaxCascades 4 | r.DistanceFieldShadowing 1 | r.ContactShadows 0 | grass.Enable 1 | grass.DensityScale 1 | grass.SizeScale 1 | grass.CullDistanceScale 1 | foliage.DensityScale 1 | foliage.CullAll 0 | r.ViewDistanceScale 1 | r.StaticMeshLODDistanceScale 1 | r.Nanite.MaxPixelsPerEdge 1 | r.DetailMode 2 | r.Water.SingleLayer.Reflection 1 | wp.Runtime.HLOD 1
```

### 4.3 PVP NORMAL — avantage léger

Plus de brouillard, de nuages ni de bloom ; herbe à moitié ; ombres et Lumen gardés en qualité moyenne. Le jeu reste beau, nuits et grottes comprises.

```
sg.TextureQuality 3 | sg.GlobalIlluminationQuality 2 | t.MaxFPS 0 | r.VSync 0 | r.ScreenPercentage 85 | gamma 3 | r.Tonemapper.Sharpen 1 | r.SkyAtmosphere 1 | r.VolumetricCloud 0 | r.VolumetricFog 0 | r.Fog 0 | r.LightShaftQuality 0 | r.SkylightIntensityMultiplier 1.5 | r.EyeAdaptationQuality 2 | r.BloomQuality 0 | r.LensFlareQuality 0 | r.DepthOfFieldQuality 0 | r.MotionBlurQuality 0 | r.PostProcessing.DisableMaterials 0 | r.DynamicGlobalIlluminationMethod 1 | r.Lumen.DiffuseIndirect.Allow 1 | r.Lumen.Reflections.Allow 0 | r.SSR.Quality 0 | r.AOQuality 1 | r.ShadowQuality 2 | r.Shadow.Virtual.Enable 0 | r.Shadow.CSM.MaxCascades 2 | r.DistanceFieldShadowing 0 | r.ContactShadows 0 | grass.Enable 1 | grass.DensityScale 0.5 | grass.SizeScale 0.6 | grass.CullDistanceScale 0.6 | foliage.DensityScale 0.6 | foliage.CullAll 0 | r.ViewDistanceScale 1 | r.StaticMeshLODDistanceScale 1.25 | r.Nanite.MaxPixelsPerEdge 2 | r.DetailMode 1 | r.Water.SingleLayer.Reflection 0 | wp.Runtime.HLOD 1
```

### 4.4 RAID PVP — performance + visibilité

Lumen et ombres coupés : gros gain de FPS et zones ombragées éclairées. Pas d'herbe ni de débris de destruction. Les structures et tourelles restent visibles plus loin (`r.ViewDistanceScale 1.5`).

```
sg.TextureQuality 2 | sg.GlobalIlluminationQuality 1 | t.MaxFPS 0 | r.VSync 0 | r.ScreenPercentage 75 | gamma 3 | r.Tonemapper.Sharpen 1.5 | r.SkyAtmosphere 1 | r.VolumetricCloud 0 | r.VolumetricFog 0 | r.Fog 0 | r.LightShaftQuality 0 | r.SkylightIntensityMultiplier 2 | r.EyeAdaptationQuality 2 | r.BloomQuality 0 | r.LensFlareQuality 0 | r.DepthOfFieldQuality 0 | r.MotionBlurQuality 0 | r.PostProcessing.DisableMaterials 1 | r.DynamicGlobalIlluminationMethod 0 | r.Lumen.DiffuseIndirect.Allow 0 | r.Lumen.Reflections.Allow 0 | r.SSR.Quality 0 | r.AOQuality 0 | r.ShadowQuality 0 | r.Shadow.Virtual.Enable 0 | r.Shadow.CSM.MaxCascades 0 | r.DistanceFieldShadowing 0 | r.ContactShadows 0 | grass.Enable 0 | grass.DensityScale 0 | grass.SizeScale 0 | grass.CullDistanceScale 0 | foliage.DensityScale 0.25 | foliage.CullAll 0 | r.ViewDistanceScale 1.5 | r.StaticMeshLODDistanceScale 1.5 | r.Nanite.MaxPixelsPerEdge 3 | r.DetailMode 0 | r.Water.SingleLayer.Reflection 0 | wp.Runtime.HLOD 1 | ark.MaxActiveDestroyedMeshGeoCollectionCount 0
```

### 4.5 ULTRA PVP — FPS max / visibilité max

Tout est coupé, végétation peinte comprise (`foliage.CullAll 1` : attention aux arbres invisibles qui gardent leur collision). Résolution à 60 % ; mettez `r.ScreenPercentage 50` si le PC est faible, mais les joueurs lointains deviennent flous. Le ciel reste allumé (`r.SkyAtmosphere 1`) : le couper ne rapporte presque rien.

```
sg.TextureQuality 0 | sg.GlobalIlluminationQuality 0 | t.MaxFPS 0 | r.VSync 0 | r.ScreenPercentage 60 | gamma 4 | r.Tonemapper.Sharpen 2 | r.SkyAtmosphere 1 | r.VolumetricCloud 0 | r.VolumetricFog 0 | r.Fog 0 | r.LightShaftQuality 0 | r.SkylightIntensityMultiplier 3 | r.EyeAdaptationQuality 2 | r.BloomQuality 0 | r.LensFlareQuality 0 | r.DepthOfFieldQuality 0 | r.MotionBlurQuality 0 | r.PostProcessing.DisableMaterials 1 | r.DynamicGlobalIlluminationMethod 0 | r.Lumen.DiffuseIndirect.Allow 0 | r.Lumen.Reflections.Allow 0 | r.SSR.Quality 0 | r.AOQuality 0 | r.ShadowQuality 0 | r.Shadow.Virtual.Enable 0 | r.Shadow.CSM.MaxCascades 0 | r.DistanceFieldShadowing 0 | r.ContactShadows 0 | grass.Enable 0 | grass.DensityScale 0 | grass.SizeScale 0 | grass.CullDistanceScale 0 | foliage.DensityScale 0 | foliage.CullAll 1 | r.ViewDistanceScale 1 | r.StaticMeshLODDistanceScale 2 | r.Nanite.MaxPixelsPerEdge 4 | r.DetailMode 0 | r.Water.SingleLayer.Reflection 0 | wp.Runtime.HLOD 1 | ark.MaxActiveDestroyedMeshGeoCollectionCount 0
```

### 4.6 RATHOLES / BASES CACHÉES — SCANNER

Pleine résolution pour repérer les détails. Plus de végétation ni de décor lointain (`wp.Runtime.HLOD 0`), objets visibles très loin (`r.ViewDistanceScale 3`), grottes éclairées (Lumen coupé, lumière du ciel × 3, `gamma 4`). Voir le point 6 du §1 sur les règles des serveurs.

```
sg.TextureQuality 2 | sg.GlobalIlluminationQuality 0 | t.MaxFPS 0 | r.VSync 0 | r.ScreenPercentage 100 | gamma 4 | r.Tonemapper.Sharpen 1.5 | r.SkyAtmosphere 1 | r.VolumetricCloud 0 | r.VolumetricFog 0 | r.Fog 0 | r.LightShaftQuality 0 | r.SkylightIntensityMultiplier 3 | r.EyeAdaptationQuality 2 | r.BloomQuality 0 | r.LensFlareQuality 0 | r.DepthOfFieldQuality 0 | r.MotionBlurQuality 0 | r.PostProcessing.DisableMaterials 1 | r.DynamicGlobalIlluminationMethod 0 | r.Lumen.DiffuseIndirect.Allow 0 | r.Lumen.Reflections.Allow 0 | r.SSR.Quality 0 | r.AOQuality 0 | r.ShadowQuality 0 | r.Shadow.Virtual.Enable 0 | r.Shadow.CSM.MaxCascades 0 | r.DistanceFieldShadowing 0 | r.ContactShadows 0 | grass.Enable 0 | grass.DensityScale 0 | grass.SizeScale 0 | grass.CullDistanceScale 0 | foliage.DensityScale 0 | foliage.CullAll 1 | r.ViewDistanceScale 3 | r.StaticMeshLODDistanceScale 1 | r.Nanite.MaxPixelsPerEdge 2 | r.DetailMode 0 | r.Water.SingleLayer.Reflection 0 | wp.Runtime.HLOD 0 | ark.MaxActiveDestroyedMeshGeoCollectionCount 0
```

Si `foliage.CullAll` ne fait rien sur votre serveur, lancez **une seule fois** cette bascule (relancez-la pour réafficher) :

```
show InstancedFoliage | show InstancedGrass
```

### 4.7 EFFACEMENT MAX — voir à travers le décor

À lancer **après** le Scanner, une seule fois. `show InstancedStaticMeshes` cache les rochers et le décor répété (bascule). La distance de chargement passe à 20 m : rien n'est chargé au-delà.

```
show InstancedStaticMeshes | wp.Runtime.OverrideRuntimeSpatialHashLoadingRange -range=2000
```

Risques : trous dans le décor, chutes et recalages, saccades. Si des structures disparaissent aussi, relancez `show InstancedStaticMeshes`. Pour revenir : relancez `show InstancedStaticMeshes`, puis **relancez le jeu** pour la distance de chargement.

### 4.8 EAU translucide — version très agressive

À lancer **par-dessus** un profil. Plus de surface d'eau, de reflets, de voile sous l'eau ni de brouillard : on voit le fond et les créatures aquatiques de loin. Il devient difficile de voir où est la surface.

```
r.Water.WaterMesh.EnableRendering 0 | r.Water.SingleLayer 0 | r.Water.SingleLayer.Reflection 0 | r.Water.EnableUnderwaterPostProcess 0 | r.VolumetricFog 0 | r.Fog 0 | gamma 4
```

### 4.9 RESET EAU

Remet seulement l'eau. **Relancez ensuite votre profil** : il remet le brouillard, le gamma et les reflets de l'eau à ses propres valeurs.

```
r.Water.WaterMesh.EnableRendering 1 | r.Water.SingleLayer 1 | r.Water.SingleLayer.Reflection 1 | r.Water.EnableUnderwaterPostProcess 1
```

### 4.10 CAVE — gain de FPS, visuel dégradé

Pour les grottes : Lumen et occlusion coupés, donc la lumière du ciel entre dans la grotte ; lumière du ciel × 4, `gamma 4`. L'exposition automatique est gardée (`r.EyeAdaptationQuality 2`), c'est elle qui éclaircit l'intérieur. Textures basses et modèles simplifiés : l'image est moins belle.

```
sg.TextureQuality 1 | sg.GlobalIlluminationQuality 0 | t.MaxFPS 0 | r.VSync 0 | r.ScreenPercentage 75 | gamma 4 | r.Tonemapper.Sharpen 1.5 | r.SkyAtmosphere 1 | r.VolumetricCloud 0 | r.VolumetricFog 0 | r.Fog 0 | r.LightShaftQuality 0 | r.SkylightIntensityMultiplier 4 | r.EyeAdaptationQuality 2 | r.BloomQuality 0 | r.LensFlareQuality 0 | r.DepthOfFieldQuality 0 | r.MotionBlurQuality 0 | r.PostProcessing.DisableMaterials 1 | r.DynamicGlobalIlluminationMethod 0 | r.Lumen.DiffuseIndirect.Allow 0 | r.Lumen.Reflections.Allow 0 | r.SSR.Quality 0 | r.AOQuality 0 | r.ShadowQuality 0 | r.Shadow.Virtual.Enable 0 | r.Shadow.CSM.MaxCascades 0 | r.DistanceFieldShadowing 0 | r.ContactShadows 0 | grass.Enable 0 | grass.DensityScale 0 | grass.SizeScale 0 | grass.CullDistanceScale 0 | foliage.DensityScale 0.25 | foliage.CullAll 0 | r.ViewDistanceScale 1 | r.StaticMeshLODDistanceScale 1.5 | r.Nanite.MaxPixelsPerEdge 3 | r.DetailMode 0 | r.Water.SingleLayer.Reflection 0 | wp.Runtime.HLOD 1 | ark.MaxActiveDestroyedMeshGeoCollectionCount 0
```

### 4.11 RESET / RETOUR AU RENDU NORMAL

Remet tout aux valeurs du moteur en qualité Épique, eau et commandes de vos anciennes lignes comprises (`r.MipMapLODBias`, `r.EarlyZPass`, `r.LightCulling.Quality`, `foliage.CullDistanceScale`, `r.MotionBlur.Amount`). Si votre menu n'est pas en Épique, remplacez le 3 des deux `sg.…` par votre niveau (0 Bas, 1 Moyen, 2 Haut).

```
sg.TextureQuality 3 | sg.GlobalIlluminationQuality 3 | t.MaxFPS 0 | r.VSync 0 | r.ScreenPercentage 100 | gamma 2.2 | r.Tonemapper.Sharpen 0 | r.SkyAtmosphere 1 | r.VolumetricCloud 1 | r.VolumetricFog 1 | r.Fog 1 | r.LightShaftQuality 1 | r.SkylightIntensityMultiplier 1 | r.EyeAdaptationQuality 2 | r.BloomQuality 5 | r.LensFlareQuality 2 | r.DepthOfFieldQuality 2 | r.MotionBlurQuality 4 | r.MotionBlur.Amount -1 | r.PostProcessing.DisableMaterials 0 | r.DynamicGlobalIlluminationMethod 1 | r.Lumen.DiffuseIndirect.Allow 1 | r.Lumen.Reflections.Allow 1 | r.SSR.Quality 3 | r.AOQuality 2 | r.ShadowQuality 5 | r.Shadow.Virtual.Enable 1 | r.Shadow.CSM.MaxCascades 4 | r.DistanceFieldShadowing 1 | r.ContactShadows 1 | grass.Enable 1 | grass.DensityScale 1 | grass.SizeScale 1 | grass.CullDistanceScale 1 | foliage.DensityScale 1 | foliage.CullAll 0 | foliage.CullDistanceScale 1 | r.ViewDistanceScale 1 | r.StaticMeshLODDistanceScale 1 | r.Nanite.MaxPixelsPerEdge 1 | r.DetailMode 2 | r.MipMapLODBias 0 | r.EarlyZPass 3 | r.LightCulling.Quality 1 | r.Water.SingleLayer 1 | r.Water.SingleLayer.Reflection 1 | r.Water.SingleLayer.OptimizedClear 1 | r.Water.WaterMesh.EnableRendering 1 | r.Water.EnableUnderwaterPostProcess 1 | wp.Runtime.HLOD 1
```

Le reset ne peut pas remettre :
- **les bascules `show …`** que vous avez lancées : relancez chacune une fois ;
- **les débris** (`ark.MaxActiveDestroyedMeshGeoCollectionCount`) et **la distance de chargement** (`wp.Runtime.OverrideRuntimeSpatialHashLoadingRange`) : relancez le jeu.

Le plus sûr reste de réappliquer vos options graphiques dans le menu.

### 4.12 PC RYZEN 5 3600 / RX 5700 XT 8 Go / 16 Go — trois profils et réinitialisation

Trois profils pour cette configuration, en 1080p, du plus beau au plus rapide. Comme les autres, ils règlent tous les mêmes variables : passez de l'un à l'autre sans réinitialiser.

| Variable | Gain minimum | Gain intermédiaire | Gain maximum | Réinitialiser |
|---|---|---|---|---|
| `sg.TextureQuality` | 2 | 2 | 1 | 3 |
| `sg.GlobalIlluminationQuality` | 2 | 1 | 0 | 3 |
| `r.ScreenPercentage` | 100 | 85 | 70 | 100 |
| `gamma` | 2.2 | 2.5 | 2.5 | 2.2 |
| `r.Tonemapper.Sharpen` | 0.5 | 1 | 1.5 | 0 |
| `r.VolumetricCloud` / `r.VolumetricFog` | 1 | 0 | 0 | 1 |
| `r.Fog` | 1 | 1 | 0 | 1 |
| `r.LightShaftQuality` | 1 | 0 | 0 | 1 |
| `r.SkylightIntensityMultiplier` | 1 | 1 | 1.5 | 1 |
| `r.BloomQuality` | 3 | 2 | 0 | 5 |
| `r.LensFlareQuality` | 1 | 0 | 0 | 2 |
| `r.DepthOfFieldQuality` / `r.MotionBlurQuality` | 0 | 0 | 0 | 2 / 4 |
| `r.PostProcessing.DisableMaterials` | 0 | 0 | 1 | 0 |
| Lumen (`r.DynamicGlobalIlluminationMethod`, `…DiffuseIndirect.Allow`) | 1 | 0 | 0 | 1 |
| `r.Lumen.Reflections.Allow` | 0 | 0 | 0 | 1 |
| `r.SSR.Quality` | 2 | 1 | 0 | 3 |
| `r.AOQuality` | 2 | 1 | 0 | 2 |
| `r.ShadowQuality` | 3 | 2 | 0 | 5 |
| `r.Shadow.Virtual.Enable` | 0 | 0 | 0 | 1 |
| `r.Shadow.CSM.MaxCascades` | 3 | 2 | 0 | 4 |
| `r.DistanceFieldShadowing` | 1 | 0 | 0 | 1 |
| `r.ContactShadows` | 0 | 0 | 0 | 1 |
| `grass.Enable` | 1 | 1 | 0 | 1 |
| `grass.DensityScale` / `SizeScale` / `CullDistanceScale` | 0.8 / 1 / 0.8 | 0.5 / 0.6 / 0.5 | 0 | 1 |
| `foliage.DensityScale` | 0.8 | 0.6 | 0 | 1 |
| `r.ViewDistanceScale` | 1 | 1 | 0.8 | 1 |
| `r.StaticMeshLODDistanceScale` | 1 | 1.25 | 1.5 | 1 |
| `r.Nanite.MaxPixelsPerEdge` | 1 | 2 | 3 | 1 |
| `r.DetailMode` | 2 | 1 | 0 | 2 |
| `r.Water.SingleLayer.Reflection` | 1 | 0 | 0 | 1 |
| `ark.MaxActiveDestroyedMeshGeoCollectionCount` | 0 | 0 | 0 | relancer le jeu |

Communs aux quatre lignes : `t.MaxFPS 0`, `r.VSync 0`, `r.SkyAtmosphere 1`, `r.EyeAdaptationQuality 2`, `foliage.CullAll 0`, `wp.Runtime.HLOD 1`.

Ce qui coûte le plus sur cette configuration :

| Réglage | Pourquoi sur ce PC |
|---|---|
| Lumen coupé (`r.DynamicGlobalIlluminationMethod 0`) | La RX 5700 XT n'a pas de ray tracing matériel : Lumen tourne en logiciel et coûte très cher. C'est le plus gros gain |
| Occlusion gardée (`r.AOQuality 1`) | Sans Lumen, elle garde les intérieurs et les grottes un peu sombres, sinon tout devient plat |
| Ombres virtuelles coupées, ombres classiques en qualité 2 | Les ombres virtuelles sont lourdes en calcul et en mémoire vidéo |
| `sg.TextureQuality 2` | 8 Go de mémoire vidéo : en Épique, ARK la remplit et l'image saccade |
| Nuages et brouillard volumétriques coupés | Gros gain sur la carte graphique ; le brouillard simple (`r.Fog 1`), presque gratuit, est gardé |
| Pas de débris (`ark.MaxActiveDestroyedMeshGeoCollectionCount 0`) | Le Ryzen 5 3600 limite dans les bases et en raid : moins de débris, moins de chutes de FPS |
| `r.ScreenPercentage` sous 100 + `r.Tonemapper.Sharpen` | Gain net sur la carte graphique ; en 1080p, l'image reste propre jusqu'à 70 environ |

#### Gain minimum — garder un beau jeu

Garde Lumen pour l'éclairage, les nuages, le brouillard et les ombres lointaines, en pleine résolution. Coupe seulement ce qui coûte beaucoup pour peu de différence à l'écran : ombres virtuelles, reflets Lumen, flou, débris. Textures en qualité 2 à cause des 8 Go de mémoire vidéo.

```
sg.TextureQuality 2 | sg.GlobalIlluminationQuality 2 | t.MaxFPS 0 | r.VSync 0 | r.ScreenPercentage 100 | gamma 2.2 | r.Tonemapper.Sharpen 0.5 | r.SkyAtmosphere 1 | r.VolumetricCloud 1 | r.VolumetricFog 1 | r.Fog 1 | r.LightShaftQuality 1 | r.SkylightIntensityMultiplier 1 | r.EyeAdaptationQuality 2 | r.BloomQuality 3 | r.LensFlareQuality 1 | r.DepthOfFieldQuality 0 | r.MotionBlurQuality 0 | r.PostProcessing.DisableMaterials 0 | r.DynamicGlobalIlluminationMethod 1 | r.Lumen.DiffuseIndirect.Allow 1 | r.Lumen.Reflections.Allow 0 | r.SSR.Quality 2 | r.AOQuality 2 | r.ShadowQuality 3 | r.Shadow.Virtual.Enable 0 | r.Shadow.CSM.MaxCascades 3 | r.DistanceFieldShadowing 1 | r.ContactShadows 0 | grass.Enable 1 | grass.DensityScale 0.8 | grass.SizeScale 1 | grass.CullDistanceScale 0.8 | foliage.DensityScale 0.8 | foliage.CullAll 0 | r.ViewDistanceScale 1 | r.StaticMeshLODDistanceScale 1 | r.Nanite.MaxPixelsPerEdge 1 | r.DetailMode 2 | r.Water.SingleLayer.Reflection 1 | wp.Runtime.HLOD 1 | ark.MaxActiveDestroyedMeshGeoCollectionCount 0
```

#### Gain intermédiaire — tous les jours

Lumen coupé (le plus gros gain sur cette carte), occlusion gardée pour que les intérieurs restent un peu sombres, nuages et brouillard volumétriques coupés, herbe à moitié, résolution 85 %.

```
sg.TextureQuality 2 | sg.GlobalIlluminationQuality 1 | t.MaxFPS 0 | r.VSync 0 | r.ScreenPercentage 85 | gamma 2.5 | r.Tonemapper.Sharpen 1 | r.SkyAtmosphere 1 | r.VolumetricCloud 0 | r.VolumetricFog 0 | r.Fog 1 | r.LightShaftQuality 0 | r.SkylightIntensityMultiplier 1 | r.EyeAdaptationQuality 2 | r.BloomQuality 2 | r.LensFlareQuality 0 | r.DepthOfFieldQuality 0 | r.MotionBlurQuality 0 | r.PostProcessing.DisableMaterials 0 | r.DynamicGlobalIlluminationMethod 0 | r.Lumen.DiffuseIndirect.Allow 0 | r.Lumen.Reflections.Allow 0 | r.SSR.Quality 1 | r.AOQuality 1 | r.ShadowQuality 2 | r.Shadow.Virtual.Enable 0 | r.Shadow.CSM.MaxCascades 2 | r.DistanceFieldShadowing 0 | r.ContactShadows 0 | grass.Enable 1 | grass.DensityScale 0.5 | grass.SizeScale 0.6 | grass.CullDistanceScale 0.5 | foliage.DensityScale 0.6 | foliage.CullAll 0 | r.ViewDistanceScale 1 | r.StaticMeshLODDistanceScale 1.25 | r.Nanite.MaxPixelsPerEdge 2 | r.DetailMode 1 | r.Water.SingleLayer.Reflection 0 | wp.Runtime.HLOD 1 | ark.MaxActiveDestroyedMeshGeoCollectionCount 0
```

#### Gain maximum — FPS avant tout

Tout est coupé : éclairage global, occlusion, ombres, brouillard, herbe et petites plantes. Résolution 70 % avec netteté 1,5, textures en qualité 1, objets simplifiés plus tôt. Le décor s'arrête un peu plus près (`r.ViewDistanceScale 0.8`) pour soulager le processeur. Sans Lumen ni occlusion, la lumière du ciel n'est plus bloquée : grottes et intérieurs sont clairs, mais l'image est plate. Les arbres restent affichés : `foliage.CullAll 1` ferait encore gagner, mais on bute alors sur des arbres invisibles.

```
sg.TextureQuality 1 | sg.GlobalIlluminationQuality 0 | t.MaxFPS 0 | r.VSync 0 | r.ScreenPercentage 70 | gamma 2.5 | r.Tonemapper.Sharpen 1.5 | r.SkyAtmosphere 1 | r.VolumetricCloud 0 | r.VolumetricFog 0 | r.Fog 0 | r.LightShaftQuality 0 | r.SkylightIntensityMultiplier 1.5 | r.EyeAdaptationQuality 2 | r.BloomQuality 0 | r.LensFlareQuality 0 | r.DepthOfFieldQuality 0 | r.MotionBlurQuality 0 | r.PostProcessing.DisableMaterials 1 | r.DynamicGlobalIlluminationMethod 0 | r.Lumen.DiffuseIndirect.Allow 0 | r.Lumen.Reflections.Allow 0 | r.SSR.Quality 0 | r.AOQuality 0 | r.ShadowQuality 0 | r.Shadow.Virtual.Enable 0 | r.Shadow.CSM.MaxCascades 0 | r.DistanceFieldShadowing 0 | r.ContactShadows 0 | grass.Enable 0 | grass.DensityScale 0 | grass.SizeScale 0 | grass.CullDistanceScale 0 | foliage.DensityScale 0 | foliage.CullAll 0 | r.ViewDistanceScale 0.8 | r.StaticMeshLODDistanceScale 1.5 | r.Nanite.MaxPixelsPerEdge 3 | r.DetailMode 0 | r.Water.SingleLayer.Reflection 0 | wp.Runtime.HLOD 1 | ark.MaxActiveDestroyedMeshGeoCollectionCount 0
```

#### Réinitialiser

La même ligne que le reset du §4.11 : elle remet tout aux valeurs du moteur en qualité Épique, eau et commandes de vos anciennes lignes comprises. Si votre menu n'est pas en Épique, remplacez le 3 des deux `sg.…` par votre niveau (0 Bas, 1 Moyen, 2 Haut).

```
sg.TextureQuality 3 | sg.GlobalIlluminationQuality 3 | t.MaxFPS 0 | r.VSync 0 | r.ScreenPercentage 100 | gamma 2.2 | r.Tonemapper.Sharpen 0 | r.SkyAtmosphere 1 | r.VolumetricCloud 1 | r.VolumetricFog 1 | r.Fog 1 | r.LightShaftQuality 1 | r.SkylightIntensityMultiplier 1 | r.EyeAdaptationQuality 2 | r.BloomQuality 5 | r.LensFlareQuality 2 | r.DepthOfFieldQuality 2 | r.MotionBlurQuality 4 | r.MotionBlur.Amount -1 | r.PostProcessing.DisableMaterials 0 | r.DynamicGlobalIlluminationMethod 1 | r.Lumen.DiffuseIndirect.Allow 1 | r.Lumen.Reflections.Allow 1 | r.SSR.Quality 3 | r.AOQuality 2 | r.ShadowQuality 5 | r.Shadow.Virtual.Enable 1 | r.Shadow.CSM.MaxCascades 4 | r.DistanceFieldShadowing 1 | r.ContactShadows 1 | grass.Enable 1 | grass.DensityScale 1 | grass.SizeScale 1 | grass.CullDistanceScale 1 | foliage.DensityScale 1 | foliage.CullAll 0 | foliage.CullDistanceScale 1 | r.ViewDistanceScale 1 | r.StaticMeshLODDistanceScale 1 | r.Nanite.MaxPixelsPerEdge 1 | r.DetailMode 2 | r.MipMapLODBias 0 | r.EarlyZPass 3 | r.LightCulling.Quality 1 | r.Water.SingleLayer 1 | r.Water.SingleLayer.Reflection 1 | r.Water.SingleLayer.OptimizedClear 1 | r.Water.WaterMesh.EnableRendering 1 | r.Water.EnableUnderwaterPostProcess 1 | wp.Runtime.HLOD 1
```

Elle ne remet pas les bascules `show …` (relancez chacune une fois), ni les débris et la distance de chargement (relancez le jeu). Le plus sûr reste de réappliquer vos options graphiques dans le menu.

Ajustements :
- **encore trop lent sur le terrain** (la carte graphique limite) : passez au profil au-dessus ; au-delà du gain maximum, `r.ScreenPercentage 60` ;
- **saccades dans les bases ou en raid** (le processeur limite, baisser la résolution n'y change presque rien) : `r.ViewDistanceScale 0.8 | foliage.DensityScale 0.4` ;
- **FPS qui varient beaucoup** : bloquez-les un peu sous la moyenne (ex. `t.MaxFPS 60`) : l'image est plus régulière ;
- **FSR activé dans le menu** : retirez `r.ScreenPercentage 85` de la ligne, c'est FSR qui choisit la résolution ;
- **16 Go de mémoire** : ARK en demande davantage, fermez le navigateur et les applications lourdes pendant le jeu.

## 5. Sources et limites

Les plages et valeurs d'origine viennent du moteur Unreal Engine 5 ; elles n'ont pas pu être vérifiées en jeu. Quatre commandes sont marquées « à vérifier » : `foliage.CullDistanceScale`, `r.MipMapLODBias`, `wp.Runtime.HLOD.ForceDisable` et `r.Color.Grading`. Les commandes propres à ARK (`grass.SizeScale`, `ark.MaxActiveDestroyedMeshGeoCollectionCount`) ne sont pas documentées par Wildcard.

- `grass.SizeScale` (origine 1, 0,1 à 0,9 pour raccourcir l'herbe) : discussions Steam d'ARK: Survival Ascended, [guide Ginx](https://www.ginx.tv/en/remove-grass-foliage), [guide GameSkinny](https://www.gameskinny.com/tips/ark-survival-ascended-console-commands-for-better-performance/).
- Commandes d'avantage visuel désactivées par Wildcard (mise à jour 35.6) : [notes de version 35.6](https://en.shiftdelete.net/ark-survival-ascended-update-35-6-patch-notes), [wiki ARK, patch 35.6](https://ark.wiki.gg/wiki/ARK:_Survival_Ascended/Patch/35.6).
