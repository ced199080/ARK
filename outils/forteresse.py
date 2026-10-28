#!/usr/bin/env python3
"""Générateur de la forteresse circulaire Ø30 sur Metal Cliff Platform (ARK: Survival Ascended).

Produit, à partir d'une seule géométrie paramétrée :
  - les templates Template Hammer (JSON, même schéma que les exports Wikily.gg), un plan par zone (voir PLANS) : sol
    complet, colonnade (option), bord D8 -> D7, D7 -> D5, tour du pod D4, D5 -> D4 (cage et appentis), puis les
    tourelles (D8 -> D4, périmètre du pod, dessus) et le toit D4 -> centre (toiture pleine, toit en rampes), calé sur
    un mur de D4 pour suivre la hauteur du pod ; une rehausse du pod (+1 niveau) en option,
  - l'adaptation au trou (gouffre) à l'avant : fondations relevées sur l'image annotée (references/Trou_fondations.json),
    recalées sur le relevé en jeu references/Trou_points_ancrage.json,
  - les tableaux de coordonnées (CSV) pour la pose manuelle,
  - la matrice de défense (cap 100 : Heavy, Tek, Tesla et Plant Species X comptées) avec ordre de pose, murs de chaume
    de pose et contrôle de couverture (couverture()),
  - le bilan matières,
  - la liste des murs de chaume à démolir en jeu (donnees/08_chaume_a_demolir.csv),
  - les plans PNG (si matplotlib est installé).
Avant d'écrire, il contrôle la constructibilité : rien au-dessus du trou, aucune pièce qui en traverse une autre
(verifier_collisions), chaque rampe tenue par ses appuis comme sur les tours 1201 / 1809, avec des poteaux en plus pour
qu'une ligne tienne encore si un appui est détruit (verifier_appuis), chaque pièce posée après ce qui la porte, plan
après plan (ordre_de_pose), 2 000 entrées au plus par plan.

Usage :
    python3 outils/forteresse.py                       # tout régénérer
    python3 outils/forteresse.py --colonnade 3600      # rayon de la colonnade circulaire
    python3 outils/forteresse.py --trou autre.json     # autre relevé du trou (retirees / plateforme)
    python3 outils/forteresse.py --appuis tours        # appuis des rampes comme les tours, sans poteaux de stabilité
    python3 outils/forteresse.py --verifier-481 template-481-building-0.json

Conventions (mesurées dans les templates fournis, voir README_Notice_Montage.md §2) :
  - 1 fondation = 300 UU, triangle de côté 300 (hauteur H = 259,81 UU).
  - Origine (0,0) = centre de l'étoile. Angle θ = atan2(y, x) en degrés = yaw Unreal.
  - Z « plan » = cote d'un plancher, 0 = dessus des fondations intérieures.
    z template = Z + 90 (plancher), Z + 40 pour le pivot d'une fondation, Z_bas + 240 pour un mur.
  - Triangle (fondation/plafond) : pivot à mi-hauteur, yaw = direction base -> pointe.
  - Aucun toit incliné (on tiendrait debout dessus) : toutes les pentes à 45° sont en rampes inclinées (Sloped
    Railing, tours 1201/1809), en lignes de lames au pas de 300 UU ; voir pente(). Chaque ligne part d'un appui (haut
    de mur, bord de plancher) et finit sur un poteau en piliers fins, au plus 7 lames entre deux appuis et 1 lame en
    porte-à-faux, comme sur les tours ; en mode 'stable' (défaut), chaque ligne montante reçoit en plus des poteaux
    sous ses jonctions 1, 4, 7… et sous son bout haut ; voir consolider_rampes().
  - Murs : cadres de porte doubles (BP_DoubleDoorframe_Metal, comme les tours 1201/1809) partout, sauf la tour du pod
    (D4 et ses murs de bord du trou) en murs pleins, percés de ses portes.
  - Tourelle « verticale » (template 2727, tours 1201/1809) : fixée sur la face extérieure d'un mur de chaume
    (Thatch_Wall_Small) qui occupe l'emplacement ; pivot 10 UU devant le plan du mur, à mi-hauteur ;
    Heavy/Tek : pitch -89,5°, yaw = θ_sortie + 90°, roll -90° ; Tesla : pitch 0°, yaw = θ_sortie + 90°, roll -90°.
    Le mur de chaume est démoli en jeu après la pose.
"""
import argparse
import csv
import json
import math
import os
import sys

# ---------------------------------------------------------------- géométrie de base
F = 300.0                                   # côté d'une fondation
H = F * math.sqrt(3) / 2                    # hauteur d'un triangle (259.81)
K = (2 + math.sqrt(3)) / 2 * F              # apothème du dodécagone D(n) par unité de côté (559.81)
TAN15 = math.tan(math.radians(15))
Z_TPL = 90.0                                # z template du dessus des fondations intérieures
RACINE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))


def apo(n):
    """Apothème (distance centre -> milieu de côté) du dodécagone régulier D(n) de côté n fondations."""
    return K * n


def rayon_coin(n):
    """Distance centre -> sommet du dodécagone D(n)."""
    return F * n / (2 * math.sin(math.radians(15)))


def vec(deg):
    a = math.radians(deg)
    return math.cos(a), math.sin(a)


def ecart(a, b):
    """Écart angulaire signé a - b ramené dans ]-180, 180]."""
    return ((a - b + 180) % 360) - 180


# ---------------------------------------------------------------- paramètres du projet
P = dict(
    anneaux_total=15,          # D8 : Ø 29,86 fondations entre plats
    anneau_pod=7,              # D4 : Ø 14,93 (pod central, = étoile SkunkHD 481)
    anneau_cage=9,             # D5 : ligne de la cage (L1 tourelles, L2 double doorframes)
    anneau_rive=13,            # D7 : mur de rive
    decaissement=150.0,        # hauteur d'un palier de bord : anneau 14 (Ø26 -> Ø28) à -150, anneau 15 (Ø28 -> Ø30) à -300
    rive_niveaux=2,            # hauteur du mur de rive (murs)
    rangs_pente_A=3,           # rangs de rampes entre la rive et la cage (un 4e entrerait de 80 UU dans le fût)
    cage_niveaux=2,            # étages de la cage : L1 (tourelles) et L2 (cadres doubles) -> toit de cage Z2400
    casquette=1,               # rangs de casquette en porte-à-faux devant la cage
    debord=1,                  # rangs de rampes dans le vide, accrochés au haut de la jupe (1 : pend d'une lame,
                               # posable en vanilla ; 2 : le 2e rang n'a pas d'appui sans jupe sous les fondations,
                               # le script le retire)
    pod_niveaux=9,             # tour du pod (murs pleins) : Z0 -> 2700 ; le niveau 8 (Z2400 -> 2700), au-dessus du toit
                               # de cage, porte l'anneau de tourelles D4 ; la couronne et le toit se posent dessus
    mezzanine=1800.0,          # plancher technique du pod = sol de la galerie L1 (6 murs libres dessous)
    jupe=True,                 # mur de jupe au bord D8, posé sur le palier 2 (aucune pièce sous le niveau des fondations)
    colonnade_rayon=3600.0,    # colonnade circulaire sous la pente A, entièrement sur les anneaux 12-13
    # trou (gouffre) à l'avant : fondations retirées (blanc) et petite plateforme (vert), relevées sur l'image annotée
    anneau_ext=12,             # anneaux 12 à 15 : bord (couleur du plan du sol)
    trou='references/Trou_fondations.json',
    trou_releve='references/Trou_points_ancrage.json',     # points d'ancrage posés en jeu (export Template Hammer)
    colonnade_hauteur=300.0,   # 1 pilier de haut, comme les cercles de piliers 704 / 701 (au lieu de monter sous la pente)
    largeur_pilier=2 * math.pi * 600 / 96,   # 39,27 UU : 48 piliers à r=600 (template 704) = 1 pilier / 1 vide
    colonnade_passages=(30, 90, 150, 210, 270, 330),   # 1 passage par part (axe des portes du fût)
    colonnade_largeur_passage=300.0,
    appuis='stable',           # appuis des rampes : 'stable' (comme les tours, plus des poteaux pour qu'une ligne tienne
                               # encore si un appui est détruit), 'tours' (comme les tours 1201 / 1809) ou 'prudent'
    cap=100, tesla_comptee=True, plante_x_comptee=True,   # cap moteur : 100 tourelles, Tesla et Plant Species X comprises
    inventaire=(80, 35, 10),                 # Heavy, Tek, Tesla disponibles
    tesla_rive_E1=(),                        # côtés E1 de la rive qui recevraient aussi une Tesla (ex. (1, 3, 9, 11))
    rive_heavy=True,                         # deux Heavy par côté de la rive (paliers, ligne de pics et mer ; chacune ne voit
                                             # que son côté), aux niveaux 0 et 1, sur des colonnes de murs différentes ; elles
                                             # remplacent les tourelles de jupe, qui étaient sous le niveau des fondations
    ecart_tourelles=300.0,                   # écart minimal entre deux tourelles (pivots), contrôlé par defense()
    d4_tesla=(2, 10),                        # côtés du pod qui portent une Tesla en plus de leur tourelle (θ 60°, 300°)
    dessus=('plante_x', 'heavy', 'plante_x', 'tek', 'tesla', 'plante_x', 'heavy', 'plante_x', 'tek', 'tesla'),
    dessus_apotheme=1500.0,                  # tourelles et carrés de culture du dessus, sur le plancher de toit
    portee_tir=(4200.0, 6000.0),             # portée Heavy / Tek en réglage Medium et High (14 et 20 fondations)
    plafond_structures=8400,                 # 10 500 structures moins 20 % de réserve (mobilier, câbles, ajouts)
    hauteur_max_murs=70,
    portee_plafond_max=2,                    # cases au plus entre un plafond et un appui relié au sol
)
ANCRE = (0.0, F)               # sommet de l'hexagone central à θ = 90° : pilier de référence de tous les plans
# Murs de référence des plans du haut du pod (toit, tourelles du dessus, rehausse), qui suivent la hauteur de la tour :
# murs de D4 du côté θ 90° (côté k = 3, face à la pile d'ancrage), au-dessus de la porte du hall (index 1, x = +150)
# et à sa droite vus de l'extérieur (index 2 et 3, x = −150 et −450). Chacun se snappe sur le haut du mur de pod du
# dessous.
REF_MURS = {'A': (3, 1), 'B': (3, 2), 'C': (3, 3)}
ESCALIER = (129.907, -75.004, -119.998)   # colonne d'escaliers du pod (x, y, yaw), à l'ancienne place du Coeur Base
DECALAGE_MONTAGE = 10.0        # pivot de la tourelle devant le plan du mur de chaume (template 2727)
ROT_TOURELLE = dict(pitch=-89.50334669626278, roll=-90.00000277871618)   # template 2727 « Straight Heavy »
ROT_TESLA = dict(pitch=0.0, roll=-90.0)                                    # Tesla latérales des tours 1201/1809
SAILLIE_TETE = 100.0           # hypothèse : centre de la tête de tourelle à 100 UU devant le pivot (calcul des secteurs)

# ---------------------------------------------------------------- classes Unreal (chemins relevés dans les templates fournis)
C = {
    'fond': '/Game/PrimalEarth/Structures/Metal/Floor_Metal.Floor_Metal_C',
    'fond_tri': '/Game/PrimalEarth/StructuresPlus/Structures/Foundations/Triangle/Metal/BP_TriFoundation_Metal.BP_TriFoundation_Metal_C',
    'plafond': '/Game/PrimalEarth/Structures/Metal/Ceiling_Metal.Ceiling_Metal_C',
    'plafond_tri': '/Game/PrimalEarth/StructuresPlus/Structures/Ceilings/Triangle/Metal/BP_TriCeiling_Metal.BP_TriCeiling_Metal_C',
    'mur': '/Game/PrimalEarth/Structures/Metal/Wall_Metal.Wall_Metal_C',
    'cadre_double': '/Game/PrimalEarth/StructuresPlus/Structures/Doorframes_Double/Metal/BP_DoubleDoorframe_Metal.BP_DoubleDoorframe_Metal_C',
    'pilier': '/Game/PrimalEarth/Structures/Metal/Pillar_Metal.Pillar_Metal_C',
    'trappe': '/Game/PrimalEarth/Structures/Metal/Ceiling_Doorway_Metal.Ceiling_Doorway_Metal_C',
    'demi_pilier': '/Game/PrimalEarth/Structures/Tileset/Pillars/Half/Pillar_Half_Metal.Pillar_Half_Metal_C',
    'pilier_fin': '/Game/PrimalEarth/Structures/Tileset/Pillars/Thin/Pillar_Thin_Metal.Pillar_Thin_Metal_C',
    'demi_pilier_fin': '/Game/PrimalEarth/Structures/Tileset/Pillars/Half_Thin/Pillar_Half_Thin_Metal.Pillar_Half_Thin_Metal_C',
    'poutre_fine': '/Game/PrimalEarth/Structures/Tileset/Pillars/Flat_Thin/Pillar_Flat_Thin_Metal.Pillar_Flat_Thin_Metal_C',
    'rampe': '/Game/PrimalEarth/Structures/Tileset/Railings/Metal/StructureBP_Railing_Sloped_Metal.StructureBP_Railing_Sloped_Metal_C',
    'escalier': '/Game/PrimalEarth/Structures/BuildingBases/StairSM_Metal.StairSM_Metal_C',
    'porte_secrete': '/Game/PrimalEarth/Structures/Tileset/SecretDoorways/StructureBP_Door_Secret_Metal.StructureBP_Door_Secret_Metal_C',
    'coffre': '/Game/PrimalEarth/Structures/StorageBox_Huge.StorageBox_Huge_C',
    'chaume_mur': '/Game/PrimalEarth/Structures/Thatch/Thatch_Wall_Small.Thatch_Wall_Small_C',
    'stockage_dedie': '/Game/PrimalEarth/StructuresPlus/Misc/DedicatedStorage/BP_DedicatedStorage.BP_DedicatedStorage_C',
    'heavy': '/Game/PrimalEarth/Structures/BuildingBases/StructureTurretBaseBP_Heavy.StructureTurretBaseBP_Heavy_C',
    'tek': '/Game/PrimalEarth/Structures/BuildingBases/StructureTurretTek.StructureTurretTek_C',
    'tesla': '/Game/Packs/Steampunk/Structures/TeslaCoil/StructureBP_TeslaCoil.StructureBP_TeslaCoil_C',
    'crop': '/Game/PrimalEarth/Structures/Wooden/CropPlotLarge_SM.CropPlotLarge_SM_C',      # tour 1584
    'crop_m': '/Game/PrimalEarth/Structures/Wooden/CropPlotMedium_SM.CropPlotMedium_SM_C',  # tour 1584
}
NOMS = {
    'fond': 'Fondation métal', 'fond_tri': 'Fondation triangle métal', 'plafond': 'Plafond métal',
    'plafond_tri': 'Plafond triangle métal', 'mur': 'Mur métal', 'cadre_double': 'Cadre de porte double métal',
    'pilier': 'Pilier métal', 'trappe': 'Plafond à trappe métal', 'demi_pilier': 'Demi-pilier métal',
    'pilier_fin': 'Pilier fin métal (Thin Pillar)', 'demi_pilier_fin': 'Demi-pilier fin métal (Half Thin Pillar)',
    'poutre_fine': 'Pilier fin couché métal (Flat Thin Pillar)',
    'rampe': 'Rampe inclinée métal (Sloped Railing)', 'escalier': 'Escalier métal',
    'porte_secrete': 'Porte secrète métal', 'coffre': 'Coffre',
    'chaume_mur': 'Mur de chaume (gabarit de pose, à démolir)', 'heavy': 'Tourelle lourde (Heavy)',
    'tek': 'Tourelle Tek', 'tesla': 'Bobine Tesla', 'pics': 'Mur de pics métal',
    'crop': 'Grand carré de culture (Plant Species X)', 'crop_m': 'Carré de culture moyen (Plant Species X)',
    'boite_munitions': 'Boîte de munitions (Ammo Box)',
    'replicateur': 'Réplicateur Tek', 'forge_vapeur': 'Forge à vapeur (Steam Forge)',
    'megalab': 'Labo de fortune (Makeshift Megalab)', 'stockage_dedie': 'Stockage dédié Tek (Tek Dedicated Storage)',
    'coffre_fort': 'Coffre-fort (Vault)', 'generateur_tek': 'Générateur Tek',
}

# Coût unitaire : MI=lingot de métal, PC=pâte cimentée, EL=électroniques, PO=polymère, CR=cristal, EM=élément,
# CU=cuir, FI=fibre, CH=chaume, BO=bois, PI=pierre. est=True : estimation (pièce absente des sources consultées).
COUTS = {
    'fond': dict(MI=50, PC=15), 'fond_tri': dict(MI=25, PC=8), 'plafond': dict(MI=35, PC=10),
    'plafond_tri': dict(MI=18, PC=5, est=True), 'mur': dict(MI=25, PC=7),
    'cadre_double': dict(MI=25, PC=7, est=True), 'pilier': dict(MI=25, PC=7),
    'trappe': dict(MI=35, PC=10, est=True), 'demi_pilier': dict(MI=13, PC=4, est=True),
    'pilier_fin': dict(MI=13, PC=4, est=True), 'demi_pilier_fin': dict(MI=7, PC=2, est=True),
    'poutre_fine': dict(MI=13, PC=4, est=True),
    'rampe': dict(MI=12, PC=3, est=True), 'escalier': dict(MI=50, PC=15, est=True),
    'porte_secrete': dict(MI=25, PC=7, est=True), 'coffre': dict(),          # mobilier : hors bilan
    'chaume_mur': dict(CH=7, FI=4, BO=4, est=True),
    'heavy': dict(MI=540, PC=200, EL=270, PO=70),      # 1 tourelle auto (140/50/70/20) + 400/150/200/50
    'tek': dict(MI=100, PC=50, EL=100, PO=50, EM=3),
    'tesla': dict(MI=500, CR=200, EL=100, PO=300),
    'pics': dict(MI=25, CU=20, FI=30),
    'crop': dict(BO=40, CH=50, FI=40, PI=100, est=True),     # graine de Plant Species X en plus (marais)
    'crop_m': dict(CH=20, FI=30, PI=50, est=True),           # ark.wiki.gg (Medium Crop Plot)
    'boite_munitions': dict(est=True),                       # coût non trouvé : à relever à l'établi
    # équipements (hors plan) : PN = perle noire, HU = huile, PE = poudre étincelante
    'replicateur': dict(EM=100, MI=5000, CR=600, PN=150, PO=800),
    'forge_vapeur': dict(MI=3250, CR=500, PC=600, EL=200, PO=1000),
    'megalab': dict(MI=450, PC=300, PE=100, CR=250, PO=150, EL=20),
    'stockage_dedie': dict(EM=3, PN=4, MI=125, CR=75, PO=55),
    'coffre_fort': dict(MI=500, PC=100, HU=70, PO=90, est=True),     # une seule source
    'generateur_tek': dict(EM=30, MI=2400, CR=250, PN=120, PO=500),
}


# ---------------------------------------------------------------- template Hammer
class Template:
    def __init__(self, nom, description):
        self.nom, self.description = nom, description
        self.entries, self.snap = [], []
        self.lignes = []          # pour les CSV : (classe, x, y, Z_plan, yaw, repère)
        self.phase, self.phases = None, []
        self.groupe, self.groupes = None, []        # plan de destination (voir PLANS)
        self.metas = []           # rampes : ligne de lames et rang (voir pente())

    def add(self, cle, x, y, z_tpl, yaw, Z=None, repere='', pitch=0.0, roll=0.0, meta=None):
        self.entries.append({
            'structure': C[cle],
            'loc': {'x': round(x, 3), 'y': round(y, 3), 'z': round(z_tpl, 3)},
            'rot': {'pitch': pitch, 'yaw': round(((yaw + 180) % 360) - 180, 3), 'roll': roll},
            'bIsFlipped': False, 'variant': 'None', 'skin': 'None', 'skinId': 0, 'skinVariant': 0,
            'skinData': {'floatParams': [], 'stringParams': [], 'objectParams': [], 'nameParams': []},
            'colors': [], 'containerName': '', 'miscEntryData': '',
        })
        self.lignes.append((cle, x, y, Z, yaw, repere))
        self.phases.append(self.phase)
        self.groupes.append(self.groupe)
        self.metas.append(meta)

    def retirer(self, indices):
        garder = [i for i in range(len(self.entries)) if i not in set(indices)]
        for nom in ('entries', 'lignes', 'phases', 'groupes', 'metas'):
            setattr(self, nom, [getattr(self, nom)[i] for i in garder])

    def reordonner(self, ordre):
        for nom in ('entries', 'lignes', 'phases', 'groupes', 'metas'):
            setattr(self, nom, [getattr(self, nom)[i] for i in ordre])

    def add_brut(self, entree, cle, Z, repere):
        """Reprend une entrée d'un template existant telle quelle (skin, couleurs, nom de coffre conservés)."""
        self.entries.append(entree)
        l, r = entree['loc'], entree['rot']
        self.lignes.append((cle, l['x'], l['y'], Z, r['yaw'], repere))
        self.phases.append(self.phase)
        self.groupes.append(self.groupe)
        self.metas.append(None)

    def compte(self):
        out = {}
        for cle, *_ in self.lignes:
            out[cle] = out.get(cle, 0) + 1
        return out

    def ecrire(self, chemin):
        data = {'dataVersion': 1, 'name': self.nom, 'creator': 'Forteresse ASA (generateur)',
                'description': self.description, 'miscData': '', 'snapOverrides': self.snap,
                'entries': self.entries}
        with open(chemin, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, separators=(',', ':'))


def ancre(t, empilee=False):
    """Pilier de référence : 2 demi-piliers empilés (plan 1) ou 1 demi-pilier posé dessus (autres plans).

    Il est au sommet de l'hexagone central à θ = 90° (0 ; 300), là où était déjà la pile d'ancrage : c'est aussi le
    repère du relevé du trou (references/Trou_points_ancrage.json).
    """
    x, y = ANCRE
    if empilee:
        t.add('demi_pilier', x, y, 15, 0, Z=-75, repere='ancre basse')
        t.add('demi_pilier', x, y, 165, 0, Z=75, repere='ancre haute')
        t.snap = [0, 1]
    else:
        t.add('demi_pilier', x, y, 315, 0, Z=225, repere='ancre module (se pose sur l\'ancre du sol)')
        t.snap = [0]


# ---------------------------------------------------------------- pavage dodécagonal carrés + triangles
def pavage(nb_anneaux, centre=True):
    """Croissance anneau par anneau de l'étoile à branches radiales (identique au template SkunkHD 481).

    Le contour courant est un dodécagone équiangle décrit par (apothème a[k], longueur L[k]) pour les 12
    normales θ = 30·k. Anneau impair : carrés sur les côtés E0 (θ ≡ 0 mod 60), trapèzes de triangles sur E1.
    Anneau pair : l'inverse. Après l'anneau 2m-1 le contour est le dodécagone régulier D(m).
    """
    a = [H if k % 2 == 0 else F for k in range(12)]
    L = [1 if k % 2 == 0 else 0 for k in range(12)]
    pieces = []
    if centre:
        for k in range(0, 12, 2):
            nx, ny = vec(30 * k)
            pieces.append(dict(type='tri', x=nx * H / 2, y=ny * H / 2, yaw=30 * k + 180, anneau=0, cote=k, idx=0))
    contours = {0: (a[:], L[:])}
    for r in range(1, nb_anneaux + 1):
        for k in range(12):
            nu = 30 * k
            nx, ny = vec(nu)
            dx, dy = -ny, nx
            carre = (k % 2 == 0) == (r % 2 == 1)
            if carre:
                for i in range(L[k]):
                    t = (-L[k] / 2 + i + 0.5) * F
                    pieces.append(dict(type='carre', x=(a[k] + F / 2) * nx + t * dx, y=(a[k] + F / 2) * ny + t * dy,
                                       yaw=nu, anneau=r, cote=k, idx=i))
                a[k] += F
            else:
                for i in range(L[k]):                       # triangles pointe vers l'extérieur
                    t = (-L[k] / 2 + i + 0.5) * F
                    pieces.append(dict(type='tri', x=(a[k] + H / 2) * nx + t * dx, y=(a[k] + H / 2) * ny + t * dy,
                                       yaw=nu, anneau=r, cote=k, idx=i))
                for j in range(L[k] + 1):                   # triangles pointe vers l'intérieur
                    t = (-(L[k] + 1) / 2 + j + 0.5) * F
                    pieces.append(dict(type='tri', x=(a[k] + H / 2) * nx + t * dx, y=(a[k] + H / 2) * ny + t * dy,
                                       yaw=nu + 180, anneau=r, cote=k, idx=L[k] + j))
                a[k] += H
                L[k] += 1
        contours[r] = (a[:], L[:])
    return pieces, contours


def polygone(pc):
    """Contour (x, y) d'une pièce du pavage."""
    nx, ny = vec(pc['yaw'])
    dx, dy = -ny, nx
    pts = ([(-150, -150), (150, -150), (150, 150), (-150, 150)] if pc['type'] == 'carre'
           else [(H / 2, 0), (-H / 2, 150), (-H / 2, -150)])
    return [(pc['x'] + u * nx + v * dx, pc['y'] + u * ny + v * dy) for u, v in pts]


def se_coupent(A, B, marge=1.0):
    """Test des axes séparateurs pour deux polygones convexes (contact simple = pas d'intersection)."""
    for poly in (A, B):
        for i in range(len(poly)):
            (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
            ax_, ay_ = y2 - y1, x1 - x2
            n = math.hypot(ax_, ay_)
            pa = [(ax_ * x + ay_ * y) / n for x, y in A]
            pb = [(ax_ * x + ay_ * y) / n for x, y in B]
            if max(pa) <= min(pb) + marge or max(pb) <= min(pa) + marge:
                return False
    return True


def cotes_contour(contour):
    """Positions des murs le long d'un contour : (x, y, yaw, côté, index)."""
    a, L = contour
    out = []
    for k in range(12):
        nx, ny = vec(30 * k)
        dx, dy = -ny, nx
        for i in range(L[k]):
            t = (-L[k] / 2 + i + 0.5) * F
            out.append((a[k] * nx + t * dx, a[k] * ny + t * dy, 30 * k, k, i))
    return out


def pente(t, systeme, A_ancre, Z_ancre, sens, repere, nb=None, demi=False, filtre=None, groupe=None, rang0=0):
    """Lignes de rampes inclinées (Sloped Railing, tours 1201 / 1809) sur une pente à 45°, ancrées sur le dodécagone
    d'apothème A_ancre à la cote Z_ancre (dessus d'un mur, bord d'un plancher). Aucun toit incliné : on tiendrait
    debout dessus.

    sens=+1 : la pente monte vers le centre depuis l'ancre (toit, pente A) ; sens=-1 : elle descend vers l'extérieur
    (casquette, overhang, débord). Les lames forment des lignes radiales au pas de 300 UU : t = 0, ±300… (demi=False)
    ou t = ±150, ±450… (demi=True). Chaque ligne doit partir d'un JOINT de murs (côté pair : demi=False ; impair :
    demi=True) : en jeu, une lame perpendiculaire à un mur ne se pose pas sur son haut, il lui faut la tête du pilier
    fin posé dans le joint (tour 1809 : 52 départs sur 52), que consolider_rampes ajoute. Chaque ligne part de l'ancre et s'arrête à la première lame au-dessus
    du trou (filtre) ou qui dépasserait l'arête du côté de plus de 150 UU : une ligne est toujours continue depuis son
    appui. Les lames qui se croisent aux arêtes ou heurtent une structure sont retirées ensuite, en bout de ligne, et les
    lignes reçoivent leurs poteaux (consolider_rampes).
    nb : nombre de rangs (None : jusqu'au faîtage). groupe(a) : plan de la lame selon l'apothème de son pivot.
    Cotes relevées sur la tour 1201 : pivot au milieu de la rampe et à z template Z_bas + 290 ; yaw = normale - 90°.
    """
    pas = F / 2 if demi else 0.0
    i_max = int((A_ancre * TAN15 + 1e-6 - pas) // F)
    for k in range(12):
        nx, ny = vec(30 * k)
        dx, dy = -ny, nx
        for tt in sorted({s_ * (pas + i * F) for i in range(i_max + 1) for s_ in (-1, 1)}):
            j = 0
            while nb is None or j < nb:
                A_bas = A_ancre - j * F if sens > 0 else A_ancre + (j + 1) * F
                Z_bas = Z_ancre + j * F if sens > 0 else Z_ancre - (j + 1) * F
                a = A_bas - F / 2
                if a <= 0 or abs(tt) > a * TAN15 + F / 2 + 1e-6:
                    break
                x, y = a * nx + tt * dx, a * ny + tt * dy
                if filtre and filtre(x, y):
                    break
                if groupe:
                    t.groupe = groupe(a)
                rang = f'r{j}' if sens > 0 else f'r-{j + 1 + rang0}'
                t.add('rampe', x, y, Z_bas + Z_TPL + 200, 30 * k - 90, Z=Z_bas, repere=f'{repere} {rang} c{k} t{tt:+.0f}',
                      meta=dict(sys=systeme, k=k, t=tt, rang=j, sens=sens))
                j += 1


def bouts_lame(x, y, z_tpl, yaw):
    """Extrémités de la ligne de base d'une rampe inclinée : (bas, haut), en (x, y, z template)."""
    ox, oy = vec(yaw + 90)                      # vers le bas de la pente
    return (x + F / 2 * ox, y + F / 2 * oy, z_tpl - 200), (x - F / 2 * ox, y - F / 2 * oy, z_tpl + 100)


def cote_anneau(p, r):
    """Cote Z du dessus des fondations de l'anneau r : 0 jusqu'à la rive (D7, Ø26), puis un palier de plus par anneau.

    Anneau 14 (Ø26 -> Ø28) : -decaissement ; anneau 15 (Ø28 -> Ø30) : -2 x decaissement.
    """
    return -p['decaissement'] * max(0, r - p['anneau_rive'])


def paliers_bord(p):
    """Paliers abaissés en coupe sur un côté E0 : [(apothème intérieur, apothème extérieur, Z), ...]."""
    _, cont = pavage(p['anneaux_total'], centre=False)
    return [(cont[r - 1][0][0], cont[r][0][0], cote_anneau(p, r))
            for r in range(p['anneau_rive'] + 1, p['anneaux_total'] + 1)]


def hauteur_pente_A(p, x, y):
    """Cote du dessus de la pente A à la verticale de (x, y) (toits dodécagonaux à 45°)."""
    proj = max(x * vec(30 * k)[0] + y * vec(30 * k)[1] for k in range(12))
    return p['rive_niveaux'] * F + apo(7) - proj


# ---------------------------------------------------------------- trou (gouffre à l'avant de la structure)
TROU = {}                      # cache du relevé : clés des fondations retirées / de la plateforme, polygones


def rho(x, y):
    """Rayon « dodécagonal » de (x, y) : apothème du dodécagone régulier qui passe par ce point."""
    return max(x * c + y * s for c, s in (vec(30 * k) for k in range(12)))


def cle_piece(pc):
    return pc['anneau'], pc['cote'], pc['idx']


def charger_trou(p):
    """Fondations du trou, relevées sur l'image annotée par le joueur (references/Trou_fondations.json) :
    'retirees' (en blanc) ne sont pas posées ; 'plateforme' (en vert) sont posées, mais rien n'y est accroché."""
    if TROU.get('chemin') == p['trou']:
        return TROU
    chemin = p['trou'] if os.path.isabs(p['trou']) else os.path.join(RACINE, p['trou'])
    d = json.load(open(chemin, encoding='utf-8'))
    ret, pla = {tuple(k) for k in d['retirees']}, {tuple(k) for k in d['plateforme']}
    pieces, _ = pavage(p['anneaux_total'])
    TROU.clear()
    TROU.update(chemin=p['trou'], retirees=ret, plateforme=pla,
                polys=[polygone(pc) for pc in pieces if cle_piece(pc) in ret | pla],
                gardees=[polygone(pc) for pc in pieces if cle_piece(pc) not in ret | pla])
    return TROU


def piece_dans_trou(p, pc):
    """Fondation retirée (en blanc sur le relevé) : elle n'est pas posée."""
    return cle_piece(pc) in charger_trou(p)['retirees']


def piece_plateforme(p, pc):
    """Fondation de la petite plateforme (en vert) : posée, mais rien n'est accroché dessus."""
    return cle_piece(pc) in charger_trou(p)['plateforme']


def _dans_poly(poly, x, y, marge):
    """Polygone convexe parcouru dans le sens trigonométrique : le point est à plus de `marge` UU de chaque côté
    vers l'intérieur (marge négative : tolérance vers l'extérieur)."""
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
        if ((x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)) / math.hypot(x2 - x1, y2 - y1) < marge:
            return False
    return True


def dans_trou(p, x, y, bord=False):
    """Point au-dessus du trou ou de la plateforme verte : rien n'y est posé.

    bord=False : le point doit être à l'intérieur du trou, arêtes et sommets entre deux fondations du trou compris
    (pièces centrées : plafonds, rampes, piliers ; un pilier à un sommet du bord reste en place).
    bord=True : un point sur le bord du trou compte aussi (murs, cadres, emplacements de tourelles : le mur de bord
    du trou les remplace).
    Au-delà du bord de la plateforme (overhang, jupe), le point est ramené sur le dernier anneau.
    """
    T = charger_trou(p)
    r = rho(x, y)
    if r > apo(p['anneaux_total'] // 2 + 1) - 1:
        k = (apo(p['anneaux_total'] // 2 + 1) - 100) / r
        x, y, bord = x * k, y * k, False
    if not any(_dans_poly(poly, x, y, -1.0) for poly in T['polys']):
        return False
    if bord or any(_dans_poly(poly, x, y, 1.0) for poly in T['polys']):
        return True
    return not any(_dans_poly(poly, x, y, -1.0) for poly in T['gardees'])


def bords_trou(p):
    """Arêtes entre une fondation conservée sous la rive (anneaux ≤ 13) et une fondation du trou ou de la plateforme.

    Renvoie [(x, y, normale vers le trou, ρ, θ)] triés par angle : un mur de bord par arête.
    """
    pieces, _ = pavage(p['anneaux_total'])
    T = charger_trou(p)
    trou_ou_pla = lambda q: cle_piece(q) in T['retirees'] | T['plateforme']
    aretes = {}
    for pc in pieces:
        poly = polygone(pc)
        for i in range(len(poly)):
            (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
            aretes.setdefault((round((x1 + x2) / 2, 1), round((y1 + y2) / 2, 1)), []).append((pc, (x1, y1), (x2, y2)))
    out = []
    for lst in aretes.values():
        if len(lst) != 2:
            continue
        dedans = [q for q, *_ in lst if not trou_ou_pla(q)]
        trou = [q for q, *_ in lst if trou_ou_pla(q)]
        if len(dedans) != 1 or len(trou) != 1 or dedans[0]['anneau'] > p['anneau_rive']:
            continue
        _, (x1, y1), (x2, y2) = lst[0]
        xm, ym = (x1 + x2) / 2, (y1 + y2) / 2
        nu = math.degrees(math.atan2(-(x2 - x1), y2 - y1))
        if vec(nu)[0] * (trou[0]['x'] - xm) + vec(nu)[1] * (trou[0]['y'] - ym) < 0:
            nu += 180
        out.append((xm, ym, nu % 360, rho(xm, ym), math.degrees(math.atan2(ym, xm)) % 360))
    return sorted(out, key=lambda m: m[4])


def niveaux_bord_trou(p, r):
    """Hauteur (en murs) d'un mur de bord du trou, posée avec sa zone : il ferme la coupe jusqu'à l'enveloppe.

    Dans le pod (ρ ≤ D4) : jusqu'au haut de la tour, Z2700 (la couronne du toit en ajoute un, chaque rehausse aussi).
    Dans le couloir (D4 < ρ ≤ D5) : jusqu'au toit de cage Z2400. Au-delà : jusque sous la pente A, au moins la hauteur
    de la rive.
    """
    if r <= apo(4) + 1:
        return p['pod_niveaux']
    if r <= apo(5) + 1:
        return int(p['mezzanine'] // F) + p['cage_niveaux']
    z_pente = p['rive_niveaux'] * F + apo(7) - r
    return max(p['rive_niveaux'], math.ceil((z_pente - 1) / F))


def groupe_bord(p, r):
    """Plan d'un mur de bord du trou : entre D5 et D7 -> D7-D5 ; couloir -> D5-D4 ; pod -> tour du pod."""
    if r > apo(5) + 1:
        return 'D7-D5'
    return 'D5-D4' if r > apo(4) + 1 else 'pod'


def bande(x0, y0, ang, long, larg=20.0):
    """Rectangle mince (lame de rampe, mur vu de dessus) partant de (x0, y0) dans la direction ang."""
    nx, ny = vec(ang)
    dx, dy = -ny * larg / 2, nx * larg / 2
    x1, y1 = x0 + long * nx, y0 + long * ny
    return [(x0 - dx, y0 - dy), (x1 - dx, y1 - dy), (x1 + dx, y1 + dy), (x0 + dx, y0 + dy)]


def casquette_trou(p, hauts):
    """Casquette du bord du trou : la toiture en rampes se prolonge au-dessus du gouffre, comme la casquette de D5.

    Une lame par mur de bord de `hauts` (murs du couloir, jusqu'au toit de cage Z2400 ; murs du pod, jusqu'au haut de
    la couronne) : elle part du haut du mur, à l'un de ses bouts (joint : pilier fin de départ), et descend de 300 UU
    vers le gouffre, au-dessus des tourelles reposées face
    au trou. Les lames qui croiseraient un mur de bord, la casquette de D5 ou une autre lame (angles rentrants du trou)
    ne sont pas posées. Renvoie [(x pivot, y pivot, normale vers le trou, θ)].
    """
    murs = [bande(x - 150 * vec(nu + 90)[0], y - 150 * vec(nu + 90)[1], nu + 90, F) for x, y, nu, r, th in hauts]
    a = apo(p['anneau_cage'] // 2 + 1) + F / 2
    n = int((a * TAN15 + F / 2) // F + 1e-9)
    obstacles = []
    for k in range(12):
        nx, ny = vec(30 * k)
        for i in range(-n, n + 1):
            x, y = a * nx - i * F * ny, a * ny + i * F * nx
            if not dans_trou(p, x, y):
                obstacles.append(bande(x - 150 * nx, y - 150 * ny, 30 * k, F))
    out, lames = [], []
    for j, (x, y, nu, r, th) in enumerate(hauts):
        for sg in (1, -1):                      # au bout du mur (joint, où se pose le pilier fin de départ)
            xe, ye = x + sg * F / 2 * vec(nu + 90)[0], y + sg * F / 2 * vec(nu + 90)[1]
            L = bande(xe, ye, nu, F)
            if any(se_coupent(L, o) for o in obstacles + lames + murs[:j] + murs[j + 1:]):
                continue
            lames.append(L)
            out.append((xe + 150 * vec(nu)[0], ye + 150 * vec(nu)[1], nu, th))
            break
    return out


def releve_trou(p):
    """Recale le relevé des points d'ancrage (export Template Hammer du joueur) sur le repère du projet.

    Le demi-pilier du relevé est le pilier de référence : on le pose sur ANCRE (ancre basse, z 15) et on cherche la
    rotation (multiple de 30°) qui fait retomber ses fondations sur l'étoile. Renvoie (rotation, nb retrouvées,
    nb total, nb dans les fondations retirées, [(X, Y, Z, retrouvée)]).
    """
    chemin = p['trou_releve'] if os.path.isabs(p['trou_releve']) else os.path.join(RACINE, p['trou_releve'])
    if not os.path.exists(chemin):
        return None
    d = json.load(open(chemin, encoding='utf-8'))
    pil = next(e for e in d['entries'] if 'Pillar' in e['structure'])
    fonds = [e for e in d['entries'] if e['structure'].endswith(('Floor_Metal_C', 'BP_TriFoundation_Metal_C'))]
    pieces, _ = pavage(p['anneaux_total'])
    meilleur = None
    for phi in range(-180, 180, 30):
        c, s_ = vec(phi)
        px, py = pil['loc']['x'], pil['loc']['y']
        tx, ty = ANCRE[0] - (px * c - py * s_), ANCRE[1] - (px * s_ + py * c)
        pts, trouves, dans = [], 0, 0
        for e in fonds:
            x, y = e['loc']['x'], e['loc']['y']
            X, Y = x * c - y * s_ + tx, x * s_ + y * c + ty
            Z = e['loc']['z'] - pil['loc']['z'] + 15 - (Z_TPL - 50)
            pc = min(pieces, key=lambda q: math.hypot(q['x'] - X, q['y'] - Y))
            ok = math.hypot(pc['x'] - X, pc['y'] - Y) < 5 and abs(Z - cote_anneau(p, pc['anneau'])) < 5
            trouves += ok
            dans += ok and piece_dans_trou(p, pc)
            pts.append((X, Y, Z, ok))
        if meilleur is None or trouves > meilleur[1]:
            meilleur = (phi, trouves, len(fonds), dans, pts)
    return meilleur


# ---------------------------------------------------------------- volumes : collisions et appuis (constructibilité)
# Encombrements (UU) : mur, cadre, mur de chaume 300 × 300 × 20 ; pilier 40 × 40 ; pilier fin 20 × 20 ; poutre fine
# (pilier fin couché) 300 × 20 × 20 ; rampe inclinée = lame de 10 UU d'épaisseur et 100 UU de haut au-dessus de sa ligne
# de base ; tourelle = bloc devant son mur de chaume (Heavy / Tek 140 × 110 × 110, Tesla 250 × 150 × 150).
# Chaque pièce a un noyau : son volume sans les bords qui se recouvrent normalement au snap (arêtes de plafond et de
# fondation, bouts et haut de mur, têtes de pilier, bouts de lame). Deux pièces sont en collision quand le noyau de l'une
# entre dans le volume de l'autre : c'est ce que le jeu refuse (« obstrué »).
def _moins(a, b):
    return a[0] - b[0], a[1] - b[1], a[2] - b[2]


def _vect(a, b):
    return a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]


def _scal(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _unit(a):
    n = math.sqrt(_scal(a, a))
    return None if n < 1e-9 else (a[0] / n, a[1] / n, a[2] / n)


class Solide:
    """Polyèdre convexe : sommets, normales de faces, directions d'arêtes (test des axes séparateurs)."""

    def __init__(self, sommets, normales, aretes):
        self.s = sommets
        self.n = [u for u in map(_unit, normales) if u]
        self.a = [u for u in map(_unit, aretes) if u]
        xs, ys, zs = zip(*sommets)
        self.bb = (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs))

    def penetre(self, autre):
        """Profondeur de recouvrement minimale (0 : séparés)."""
        b1, b2 = self.bb, autre.bb
        if b1[1] <= b2[0] or b2[1] <= b1[0] or b1[3] <= b2[2] or b2[3] <= b1[2] or b1[5] <= b2[4] or b2[5] <= b1[4]:
            return 0.0
        mini = 1e9
        for ax in self.n + autre.n + [u for u in (_unit(_vect(a, b)) for a in self.a for b in autre.a) if u]:
            pa = [_scal(ax, q) for q in self.s]
            pb = [_scal(ax, q) for q in autre.s]
            ov = min(max(pa), max(pb)) - max(min(pa), min(pb))
            if ov <= 0:
                return 0.0
            mini = min(mini, ov)
        return mini


def _prisme(poly, z0, z1, retrait=2.0):
    """Prisme vertical sur un polygone convexe, rétréci de `retrait` (contacts francs tolérés)."""
    cx = sum(q[0] for q in poly) / len(poly)
    cy = sum(q[1] for q in poly) / len(poly)
    pp = []
    for x, y in poly:
        d = math.hypot(x - cx, y - cy)
        k = max(0.0, d - retrait) / d if d else 0.0
        pp.append((cx + (x - cx) * k, cy + (y - cy) * k))
    z0, z1 = z0 + 2, z1 - 2
    ar = [(pp[(i + 1) % len(pp)][0] - pp[i][0], pp[(i + 1) % len(pp)][1] - pp[i][1], 0.0) for i in range(len(pp))]
    return Solide([(x, y, z0) for x, y in pp] + [(x, y, z1) for x, y in pp],
                  [(0, 0, 1)] + [(a[1], -a[0], 0.0) for a in ar], ar + [(0, 0, 1)])


def _boite(cx, cy, cz, yaw, lx, ly, lz, rx=0.0, ry=0.0, rz=0.0):
    """Boîte centrée : lx le long de yaw, ly en travers, lz verticale ; rx, ry, rz : retraits du noyau."""
    nx, ny = vec(yaw)
    dx, dy = -ny, nx
    hx, hy = max(1.0, lx / 2 - rx - 2), max(1.0, ly / 2 - ry - 2)
    poly = [(cx + u * nx + v * dx, cy + u * ny + v * dy) for u, v in ((-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy))]
    return _prisme(poly, cz - lz / 2 + rz, cz + lz / 2 - rz, 0.0)


def _lame(x, y, z, yaw, bout=0.0):
    """Rampe inclinée : lame verticale de 10 × 100 UU au-dessus de sa ligne de base (bas -> haut)."""
    B, T = bouts_lame(x, y, z, yaw)
    ox, oy = vec(yaw + 90)
    r = 2.0 + bout
    B = (B[0] - r * ox, B[1] - r * oy, B[2] + r)
    T = (T[0] + r * ox, T[1] + r * oy, T[2] - r)
    lx, ly = -oy * 5, ox * 5
    s_ = [(q[0] + sg * lx, q[1] + sg * ly, q[2] + dz) for q in (B, T) for sg in (-1, 1) for dz in (2.0, 98.0)]
    u, l, v = _moins(T, B), (lx, ly, 0.0), (0.0, 0.0, 1.0)
    return Solide(s_, [_vect(u, l), _vect(l, v), _vect(v, u)], [u, l, v])


def debout(cle, rep_):
    """Tourelle ou Tesla posée debout sur un plancher (dessus du pod), et non sur la face d'un mur de chaume."""
    return cle in ('heavy', 'tek', 'tesla') and ' DESSUS ' in rep_


def volume(cle, x, y, z, yaw, noyau=False, droite=False):
    """Volume d'une pièce posée (z : cote template), ou son noyau. None : pièce non contrôlée.
    droite=True : tourelle debout sur un plancher (bloc de 110 × 110 × 150 au-dessus du pivot, Tesla 150 × 150 × 250).
    Carrés de culture : grand 300 × 300 × 60, moyen 220 × 220 × 60 au-dessus du pivot (hypothèses prudentes)."""
    if droite:
        return _boite(x, y, z + 125, yaw, 150, 150, 250) if cle == 'tesla' else _boite(x, y, z + 75, yaw, 110, 110, 150)
    c = 1.0 if noyau else 0.0
    if cle in ('crop', 'crop_m'):
        a = 300 if cle == 'crop' else 220
        return _boite(x, y, z + 30, yaw, a, a, 60, 5 * c, 5 * c, 5 * c)
    if cle in ('fond', 'fond_tri', 'plafond', 'plafond_tri', 'trappe'):
        poly = polygone(dict(type='tri' if cle.endswith('_tri') else 'carre', x=x, y=y, yaw=yaw))
        if cle.startswith('fond'):
            return _prisme(poly, z - 150, z + 50 - 20 * c, 2 + 30 * c)
        return _prisme(poly, z - 15 - 2 * c, z + 2 * c, 2 + 30 * c)
    if cle in ('mur', 'cadre_double', 'chaume_mur'):
        return _boite(x, y, z, yaw, 20, 300, 300, ry=30 * c, rz=25 * c)
    # pilier : son noyau est son axe (un pilier se snappe au bout des murs et aux coins des planchers)
    if cle == 'pilier':
        return _boite(x, y, z, yaw, 40, 40, 300, 19 * c, 19 * c, 25 * c)
    if cle == 'demi_pilier':
        return _boite(x, y, z, yaw, 40, 40, 150, 19 * c, 19 * c, 25 * c)
    if cle == 'pilier_fin':
        return _boite(x, y, z, yaw, 20, 20, 300, 9 * c, 9 * c, 25 * c)
    if cle == 'demi_pilier_fin':
        return _boite(x, y, z, yaw, 20, 20, 150, 9 * c, 9 * c, 25 * c)
    if cle == 'poutre_fine':                       # couchée en travers de son yaw, comme un mur
        return _boite(x, y, z - 10, yaw, 20, 300, 20, ry=30 * c)
    if cle == 'escalier':
        return _boite(x, y, z, yaw, 300, 300, 300, 20 * c, 20 * c, 20 * c)
    if cle == 'rampe':
        return _lame(x, y, z, yaw, bout=40 * c)
    if cle in ('heavy', 'tek', 'tesla'):           # tête devant le mur de chaume : sortie = yaw - 90
        sx, sy = vec(yaw - 90)
        prof, larg = (250, 150) if cle == 'tesla' else (140, 110)
        return _boite(x + sx * prof / 2, y + sy * prof / 2, z, yaw - 90, prof, larg, larg)
    return None


class Encombrement:
    """Pièces posées indexées sur une grille de 400 UU ; heurts(ref) : pièces en collision avec une pièce."""

    def __init__(self):
        self.p, self.grille = {}, {}

    @staticmethod
    def _cases(S):
        b = S.bb
        return [(gx, gy) for gx in range(int(b[0] // 400), int(b[1] // 400) + 1)
                for gy in range(int(b[2] // 400), int(b[3] // 400) + 1)]

    def ajouter(self, ref, cle, x, y, z, yaw, droite=False):
        S = volume(cle, x, y, z, yaw, droite=droite)
        if S is None:
            return
        self.p[ref] = (cle, x, y, S, volume(cle, x, y, z, yaw, noyau=True, droite=droite))
        for c in self._cases(S):
            self.grille.setdefault(c, set()).add(ref)

    def retirer(self, ref):
        if ref in self.p:
            for c in self._cases(self.p[ref][3]):
                self.grille[c].discard(ref)
            del self.p[ref]

    def heurts(self, ref, piece=None, seuil=0.5, strict=False, ignorer=None):
        """Refs en collision avec la pièce `ref` (ou avec `piece` = (cle, x, y, z, yaw) pas encore posée).
        strict : volume entier contre volume entier pour les murs, piliers, escaliers, tourelles et carrés de culture
        (poteau isolé, qui ne se snappe à aucun d'eux) ; les planchers et les lames qu'il porte restent au noyau.
        ignorer(ref) : pièces à ne pas compter."""
        if piece:
            cle, x, y, z, yaw = piece
            S, K = volume(cle, x, y, z, yaw), volume(cle, x, y, z, yaw, noyau=True)
        else:
            cle, x, y, S, K = self.p[ref]
        out = []
        for r in set().union(*(self.grille.get(c, set()) for c in self._cases(S))):
            if r == ref:
                continue
            c2, x2, y2, S2, K2 = self.p[r]
            if ignorer and ignorer(r):
                continue
            if {cle, c2} & {'heavy', 'tek', 'tesla'} and 'chaume_mur' in (cle, c2) and math.hypot(x - x2, y - y2) < 15:
                continue                               # une tourelle et son mur de chaume de pose
            if strict and c2 not in ('rampe',) + SOLS:
                if S.penetre(S2) > seuil:
                    out.append(r)
            elif max(K.penetre(S2), S.penetre(K2)) > seuil:
                out.append(r)
        return out


def surfaces(modules):
    """Dessus des fondations et des plafonds posés (hors plateforme verte, où rien n'est accroché) : (poly, z template)."""
    out = []
    for _, m in modules:
        for e, (cle, *_, rep_) in zip(m.entries, m.lignes):
            if cle in ('fond', 'fond_tri', 'plafond', 'plafond_tri', 'trappe') and not plateforme(rep_):
                l, r = e['loc'], e['rot']
                poly = polygone(dict(type='tri' if cle.endswith('_tri') else 'carre', x=l['x'], y=l['y'], yaw=r['yaw']))
                out.append((poly, l['z'] + (50 if cle.startswith('fond') else 0)))
    return out


def dessus_sous(surf, x, y, z):
    """Cote template de la plus haute surface sous le point (x, y, z), ou None (vide, trou)."""
    hauts = [zt for poly, zt in surf if zt <= z + 1 and _dans_poly(poly, x, y, -1.0)]
    return max(hauts) if hauts else None


APPUI_LIGNES = {'toit': 'poteau', 'casquette': 'poteau', 'pente A': 'poteau', 'overhang': 'poteau', 'debord': 'poutre',
                'appentis': 'poteau', 'casquette du trou': None}
MONTANTES = ('toit', 'pente A', 'appentis')   # lignes ancrées en bas, qui montent ; les autres pendent de leur ancrage
PORTEE_MAX = 7                 # lames entre deux appuis (tour 1809 : 7 lames de la poutre d'égout au poteau de faîtage)
LIBRE_MAX = 6                  # lames montantes au-dessus du dernier appui, bout haut libre (tours 1201 et 1809 : 6)


def plateforme(rep_):
    """Pièce de la petite plateforme verte du trou : posée, mais rien n'y est accroché."""
    return rep_.startswith('plateforme')


def jeu_stable(m):
    """Mode 'stable' : jonctions d'une ligne montante de m lames qui reçoivent un poteau (0 = ancrage) : la 1re, puis une
    sur trois, et le bout haut. Si un appui est détruit (le mur d'ancrage ou un poteau), la ligne reste dans les règles
    des tours : 1 lame pendue au plus, 7 lames au plus entre deux appuis, 6 lames libres au plus au-dessus du dernier."""
    return sorted({j for j in range(1, m + 1) if (j - 1) % 3 == 0} | {m})


def lame_tient(i, S, libre_max=LIBRE_MAX):
    """La lame n° i d'une ligne (comptée depuis le bas) reste-t-elle dans les règles des tours avec les jonctions
    appuyées S (0 = jonction du bas) : entre deux appuis à 7 lames au plus, pendue d'une lame sous un appui, ou libre
    à libre_max lames au plus au-dessus du dernier appui ?"""
    bas = [s for s in S if s <= i]
    haut = [s for s in S if s >= i + 1]
    if bas and haut:
        return min(haut) - max(bas) <= PORTEE_MAX
    if haut:
        return min(haut) == i + 1
    return bool(bas) and i + 1 - max(bas) <= libre_max


def redondant(m, poteaux):
    """Une ligne montante de m lames, ancrée en bas, avec des poteaux sous les jonctions `poteaux`, tient-elle encore
    si l'un de ses appuis (l'ancrage ou un poteau) est détruit ?"""
    S = {0} | set(poteaux)
    return all(lame_tient(i, S - {s}) for s in S for i in range(m))


def jeux_stables(m):
    """Jeux de poteaux redondants pour une ligne de m lames, du plus proche de jeu_stable(m) au plus éloigné (même
    nombre de poteaux) : si un poteau ne peut pas être posé, on en décale un."""
    import itertools
    base = jeu_stable(m)
    jeux = [list(c) for c in itertools.combinations(range(1, m + 1), len(base)) if redondant(m, c)]
    return sorted(jeux, key=lambda c: (sum(abs(a - b) for a, b in zip(c, base)), c))


def consolider_rampes(p, modules):
    """Rend les rampes constructibles, comme sur les tours 1201 / 1809 :

    1. retire les colonnes de colonnade qui gênent une autre pièce (tourelle, mur de bord du trou…) ;
    2. retire les lames qui heurtent une structure ou une autre lame (arêtes du dodécagone, bord du trou), toujours en
       bout de ligne : chaque ligne reste continue depuis son appui (dessus de mur, bord de plancher) ;
    3. pose les appuis. Sur les tours, chaque ligne de lames part d'un appui (poutre fine d'égout, pilier fin) ; elle
       finit sur un poteau de faîtage en piliers fins, au plus 7 lames plus loin, ou monte librement jusqu'à 6 lames
       au-dessus de son appui (un pan sur deux des tours 1201 et 1809) ; une seule lame pend en porte-à-faux (lame de rive
       de la 1201). D'où, avec p['appuis'] :
       - 'tours' : une ligne montante (toit, pente A) de plus de 6 lames reçoit un poteau sous une jonction, le plus bas
         possible ; une ligne qui pend (casquette, overhang, débord) reçoit un appui pour qu'une seule lame dépasse ;
       - 'prudent' : en plus, chaque ligne montante finit sur un poteau sous son bout haut (poteau de faîtage) ;
       - 'stable' : chaque ligne montante reçoit un poteau sous les jonctions de jeu_stable() (la 1re, une sur trois,
         le bout haut) : elle tient encore si son mur d'ancrage ou l'un de ses poteaux est détruit. Ces poteaux
         remplacent la colonnade sous la pente A. Si l'un d'eux ne peut pas être posé (heurt, pas de plancher), la
         ligne reprend la règle 'tours'.
       Poteau : piliers fins debout sur le plancher ou la fondation sous la jonction. Débord dans le vide : poutre fine
       posée sur le niveau bas de la jupe. Une ligne qu'on ne peut pas appuyer est raccourcie.
    Chaque ligne part de la tête d'un pilier fin posé dans le joint des murs (pilier de départ) ; une ligne dont le
    départ n'est pas sur un joint est retirée.
    Renvoie un résumé chiffré.
    """
    E = Encombrement()
    info = {}
    for mi, (_, m) in enumerate(modules):
        for e, (cle, *_, rep_), meta in zip(m.entries, m.lignes, m.metas):
            l, r = e['loc'], e['rot']
            E.ajouter(id(e), cle, l['x'], l['y'], l['z'], r['yaw'], droite=debout(cle, rep_))
            info[id(e)] = (mi, cle, meta, rep_)
    retraits = {}
    # 1. colonnade : une colonne qui heurte autre chose (hors colonnade et rampes) est retirée
    for ref, (mi, cle, meta, rep_) in info.items():
        if rep_.startswith('colonnade') and ref in E.p and any(
                info[r][1] != 'rampe' and not info[r][3].startswith('colonnade') for r in E.heurts(ref)):
            retraits[ref] = 'colonnade'
            E.retirer(ref)
    # 2. lignes de lames, de l'appui vers le bout libre
    lignes = {}
    for ref, (mi, cle, meta, rep_) in info.items():
        if cle == 'rampe' and meta:
            lignes.setdefault((meta['sys'], meta['k'], meta['t']), []).append((meta['rang'], ref))
    for v in lignes.values():
        v.sort()
    limite = {k: len(v) for k, v in lignes.items()}
    rang_de = {ref: (key, j) for key, v in lignes.items() for j, ref in v}
    lames_ent = {id(e): e for _, m in modules for e in m.entries}

    def depassement(ref):
        key, j = rang_de[ref]
        l = lames_ent[ref]['loc']
        c_, s_ = vec(30 * key[1])
        return abs(key[2]) - (l['x'] * c_ + l['y'] * s_) * TAN15

    def couper(key, j, motif):
        if j < limite[key]:
            for jj, ref in lignes[key][j:limite[key]]:
                E.retirer(ref)
                retraits[ref] = motif
            limite[key] = j

    change = True
    while change:
        change = False
        for key in sorted(lignes):
            for j, ref in lignes[key][:limite[key]]:
                if ref not in E.p:
                    continue
                for r in E.heurts(ref):
                    if info[r][1] != 'rampe' or r not in rang_de:
                        couper(key, j, 'heurte ' + info[r][1])
                        change = True
                        break
                    k2, j2 = rang_de[r]
                    # deux lames qui se croisent : on retire la plus éloignée de son appui, puis celle qui dépasse
                    # le plus l'arête de son côté
                    if (j2, depassement(r), k2) > (j, depassement(ref), key):
                        couper(k2, j2, 'croise une lame')
                    else:
                        couper(key, j, 'croise une lame')
                    change = True
                    break
                if key in limite and j >= limite[key]:
                    break
    # 3. appuis
    surf = surfaces(modules)
    murs_hauts = [(l_[1], l_[2], e['loc']['z'] + F / 2, l_[4]) for _, m in modules
                  for e, l_ in zip(m.entries, m.lignes) if l_[0] in ('mur', 'cadre_double')]
    ajouts = {}
    stats = {'departs': 0, 'poteaux': 0, 'pilier_fin': 0, 'demi_pilier_fin': 0, 'poutre_fine': 0, 'raccourcies': 0,
             'stables': 0, 'stables_manquees': []}

    def jonctions(key, n):
        out = []
        for j, ref in lignes[key][:n]:
            l, r = lames_ent[ref]['loc'], lames_ent[ref]['rot']
            bas, haut = bouts_lame(l['x'], l['y'], l['z'], r['yaw'])
            ancre_, loin = (bas, haut) if key[0] not in ('casquette', 'overhang', 'debord', 'casquette du trou') \
                else (haut, bas)
            if j == 0:
                out.append(ancre_)
            out.append(loin)
        return out

    def poteau(key, J):
        z0 = dessus_sous(surf, J[0], J[1], J[2])
        if z0 is None or J[2] - z0 < F / 2 - 1:
            return None
        h = J[2] - z0
        n3 = int(h // F + 1e-6)
        reste = h - n3 * F
        pieces = [('pilier_fin', z0 + F / 2 + i * F) for i in range(n3)]
        if abs(reste - F / 2) < 1:
            pieces.append(('demi_pilier_fin', z0 + n3 * F + F / 4))
        elif abs(reste) > 1:
            return None
        out = [(cle, J[0], J[1], z, 30 * key[1]) for cle, z in pieces]
        colonnade = lambda r: r in info and info[r][3].startswith('colonnade')     # option : elle s'efface
        return out if all(not E.heurts(None, piece=q, strict=True, ignorer=colonnade) for q in out) else None

    def poutre(key, J0, J1):
        # poutre fine couchée de J0 à J1, à la cote de J1, posée sur un mur dont le haut est à cette cote sous J0
        if not any(abs(zt - J1[2]) < 2 and abs((J0[0] - xm) * vec(yw)[0] + (J0[1] - ym) * vec(yw)[1]) < 15
                   and abs(-(J0[0] - xm) * vec(yw)[1] + (J0[1] - ym) * vec(yw)[0]) <= F / 2 + 1
                   for xm, ym, zt, yw in murs_hauts):
            return None
        q = ('poutre_fine', (J0[0] + J1[0]) / 2, (J0[1] + J1[1]) / 2, J1[2], 30 * key[1] + 90)
        return [q] if not E.heurts(None, piece=q) else None

    def besoins(key, m):
        """Jonctions à appuyer (n° depuis l'ancrage, 0 = ancrage), de la solution la plus légère à la plus lourde ; en
        mode 'stable', le jeu de poteaux de stabilité d'abord."""
        if key[0] in MONTANTES and p['appuis'] in ('tours', 'stable'):
            tours = [[]] if m <= LIBRE_MAX else [[j] for j in range(max(1, m - LIBRE_MAX), min(m, PORTEE_MAX) + 1)]
            return (jeux_stables(m) if p['appuis'] == 'stable' else []) + tours
        if m <= 1:
            return [[]]
        out = []
        for jf in (m, m - 1):
            out += ([[jf, jm] for jm in (jf // 2, jf // 2 - 1, jf // 2 + 1)] if jf > PORTEE_MAX else [[jf]])
        return out

    # départ de chaque ligne : un pilier fin dans le joint des murs, sa tête au point d'ancrage. En jeu, une lame
    # perpendiculaire à un mur ne se pose pas sur son haut : sur les tours 1201 et 1809, chaque ligne part de la tête
    # d'un pilier fin (1809 : pilier fin dans le joint de deux cadres, 52 départs sur 52)
    rang_plan = {cle: n for n, (cle, *_) in enumerate(PLANS)}
    bouts_murs = {}
    for mi, (_, m) in enumerate(modules):
        for e, l_, g in zip(m.entries, m.lignes, m.groupes):
            if l_[0] in ('mur', 'cadre_double'):
                lx, ly = vec(e['rot']['yaw'] + 90)
                for sg in (-1, 1):
                    q = (e['loc']['x'] + sg * F / 2 * lx, e['loc']['y'] + sg * F / 2 * ly, e['loc']['z'] + F / 2)
                    bouts_murs.setdefault(tuple(round(c / 5) for c in q), []).append(
                        (rang_plan.get(g, len(PLANS)), mi, id(e), e['rot']['yaw']))
    departs = {}
    for key in sorted(lignes):
        if not limite[key]:
            continue
        J0 = jonctions(key, 1)[0]
        k0 = tuple(round(c / 5) for c in J0)
        if k0 in departs:
            continue                             # pilier déjà posé pour une autre ligne (pente A et overhang)
        z_pied = J0[2] - F                       # le pilier se pose sur le joint du niveau du dessous, ou un plancher
        if k0 not in bouts_murs or not (tuple(round(c / 5) for c in (J0[0], J0[1], z_pied)) in bouts_murs
                                        or abs((dessus_sous(surf, J0[0], J0[1], z_pied + 1) or -1e9) - z_pied) < 2):
            couper(key, 0, 'pas de joint de murs au départ')
            continue
        _, mi, ref_mur, yaw = min(bouts_murs[k0], key=lambda b: b[0])   # dans le 1er plan posé de ses murs
        q = ('pilier_fin', J0[0], J0[1], J0[2] - F / 2, yaw)
        if E.heurts(None, piece=q):
            couper(key, 0, 'pilier fin de départ impossible')
            continue
        E.ajouter(('depart', key), *q)
        departs[k0] = (mi, ref_mur, q, key)
        stats['departs'] += 1
    for key in sorted(lignes):
        regle = APPUI_LIGNES[key[0]]
        stable = p['appuis'] == 'stable' and key[0] in MONTANTES
        while limite[key] > (0 if stable else 1) and regle:
            m = limite[key]
            J = jonctions(key, m)
            pose = None
            for jeu in besoins(key, m):
                pose = []
                for j in jeu:
                    q = (poutre(key, J[0], J[j]) if j == 1 else None) if regle == 'poutre' else poteau(key, J[j])
                    if not q:
                        pose = None
                        break
                    pose += q
                if pose is not None:
                    break
            if stable and pose is not None:
                if jeu and redondant(m, jeu):
                    stats['stables'] += 1
                else:
                    stats['stables_manquees'].append(f'{key[0]} c{key[1]} t{key[2]:+.0f} ({m} lames)')
            if pose == []:
                break
            if pose:
                ref0 = lignes[key][m - 1][1]
                ajouts.setdefault(info[ref0][0], []).append((key, ref0, pose))
                for n_, q in enumerate(pose):
                    E.ajouter(('appui', key, n_), *q)
                    stats[q[0]] += 1
                stats['poteaux'] += len({(round(q[1]), round(q[2])) for q in pose if q[0] != 'poutre_fine'})
                break
            couper(key, m - 1, 'sans appui possible')
            stats['raccourcies'] += 1
    # colonnade (option) : colonnes que gêne un poteau
    for ref, (mi, cle, meta, rep_) in info.items():
        if rep_.startswith('colonnade') and ref in E.p and any(isinstance(r, tuple) and r[0] == 'appui'
                                                               for r in E.heurts(ref, strict=True)):
            retraits[ref] = 'colonnade (poteau)'
            E.retirer(ref)
    # écriture : lames retirées, appuis ajoutés (avant les rampes : ils sont posés d'abord)
    for mi, (_, m) in enumerate(modules):
        m.retirer([i for i, e in enumerate(m.entries) if id(e) in retraits])
        for mi_, ref_mur, (cle, x, y, z, yaw), key in departs.values():
            if mi_ == mi:                        # dans le plan du mur où il se pose
                i0 = next(i for i, e in enumerate(m.entries) if id(e) == ref_mur)
                m.phase, m.groupe = m.phases[i0], m.groupes[i0]
                if m.groupe in ('toit_rampe', 'tourelles_dessus'):
                    m.phase = m.groupe = 'toiture_pleine'    # joint des murs de référence B, C : avec la couronne
                m.add(cle, x, y, z, yaw, Z=z - Z_TPL - F / 2,
                      repere=f'depart lignes {key[0]} c{key[1]} t{key[2]:+.0f} : pilier fin dans le joint')
        for key, ref0, pose in ajouts.get(mi, []):
            i0 = next(i for i, e in enumerate(m.entries) if id(e) == ref0)
            m.phase, m.groupe = m.phases[i0], m.groupes[i0]
            for cle, x, y, z, yaw in pose:
                nom = 'poutre' if cle == 'poutre_fine' else 'poteau'
                m.add(cle, x, y, z, yaw, Z=z - Z_TPL - (F / 2 if cle == 'pilier_fin' else F / 4 if cle == 'demi_pilier_fin'
                                                        else 0), repere=f'appui {key[0]} c{key[1]} t{key[2]:+.0f} : {nom}')
        m.reordonner([i for i, l_ in enumerate(m.lignes) if l_[0] != 'rampe'] +
                     [i for i, l_ in enumerate(m.lignes) if l_[0] == 'rampe'])
    motifs = {}
    for v in retraits.values():
        motifs[v] = motifs.get(v, 0) + 1
    return dict(retraits=motifs, **stats)


def _pieces_plans(plans):
    """Toutes les entrées des plans (la pile d'ancrage une seule fois) : (plan, n° d'entrée, clé, x, y, z, yaw, repère)."""
    out, ancre_vue = [], set()
    for cle_p, t in plans.items():
        for n, (e, (cle, x, y, Z, yaw, rep_)) in enumerate(zip(t.entries, t.lignes)):
            if rep_.startswith('ancre'):
                k = (cle, round(e['loc']['z']))
                if k in ancre_vue:
                    continue
                ancre_vue.add(k)
            out.append((cle_p, n, cle, e['loc']['x'], e['loc']['y'], e['loc']['z'], e['rot']['yaw'], rep_))
    return out


# Recouvrement admis : la pile d'ancrage est plantée au sommet commun de fondations (comme les cercles de
# fondations 2901-2903).
def _admis(a, b):
    for u, v in ((a, b), (b, a)):
        if u[7].startswith('ancre') and v[2] in ('fond', 'fond_tri'):
            return 'ancre'
    return None


def verifier_collisions(plans, titre=''):
    """Aucune pièce des plans n'entre dans une autre (noyau contre volume), hors recouvrements admis."""
    P_ = _pieces_plans(plans)
    E = Encombrement()
    for n, q in enumerate(P_):
        E.ajouter(n, q[2], q[3], q[4], q[5], q[6], droite=debout(q[2], q[7]))
    vus, erreurs, admis = set(), [], {}
    for n in list(E.p):
        for r in E.heurts(n):
            k = (min(n, r), max(n, r))
            if k in vus:
                continue
            vus.add(k)
            m = _admis(P_[n], P_[r])
            if m:
                admis[m] = admis.get(m, 0) + 1
            else:
                erreurs.append((P_[n], P_[r]))
    for a, b in erreurs[:10]:
        print('  COLLISION', a[0], a[1], a[2], a[7], '<->', b[0], b[1], b[2], b[7])
    assert not erreurs, f'{len(erreurs)} collisions entre pièces des plans'
    print(f"  Collisions{' (' + titre + ')' if titre else ''} : aucune sur {len(P_)} pièces (recouvrements admis : "
          + ', '.join(f'{k} {v}' for k, v in sorted(admis.items())) + ')')
    return admis


def _dist_seg(px, py, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    u = max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - x1 - u * dx, py - y1 - u * dy)


def verifier_appuis(plans, mode='tours'):
    """Chaque rampe inclinée tient comme sur les tours 1201 / 1809 : ses lames s'enchaînent bout à bout en lignes ; une
    jonction est appuyée si elle repose sur la tête d'un pilier (pilier fin de départ dans un joint de murs, poteau) ou
    sur le bout d'une poutre fine : en jeu, une lame perpendiculaire à un mur ne se pose pas sur son haut. Une lame doit être entre deux appuis distants d'au plus 7 lames, ou pendre d'un appui qu'elle touche
    (porte-à-faux d'une seule lame), ou monter librement au plus 6 lames au-dessus d'un appui (modes 'tours' et
    'stable' ; en mode 'prudent', une seule). Compte aussi les lignes qui restent dans ces règles si l'un de leurs
    appuis est détruit (redondance). Renvoie les statistiques des lignes."""
    P_ = _pieces_plans(plans)
    pts = []
    for cle_p, n, cle, x, y, z, yaw, rep_ in P_:
        if cle in ('pilier', 'pilier_fin', 'demi_pilier', 'demi_pilier_fin') and not rep_.startswith('ancre'):
            pts.append((x, y, z + (F / 4 if cle.startswith('demi') else F / 2)))
        elif cle == 'poutre_fine':
            lx, ly = vec(yaw + 90)
            pts += [(x - F / 2 * lx, y - F / 2 * ly, z), (x + F / 2 * lx, y + F / 2 * ly, z)]

    def appuye(q):
        return any(abs(q[2] - c[2]) < 12 and math.hypot(q[0] - c[0], q[1] - c[1]) < 25 for c in pts)

    lames = [(q, bouts_lame(q[3], q[4], q[5], q[6])) for q in P_ if q[2] == 'rampe']
    cle_pt = lambda b: (round(b[0] / 5), round(b[1] / 5), round(b[2] / 5))
    par_bout = {}
    for i, (q, bb) in enumerate(lames):
        for b in bb:
            par_bout.setdefault((cle_pt(b), round(q[6] % 360)), []).append(i)
    appui_pt = {}

    def distance_appui(i, b):
        """Lames à parcourir depuis le bout b de la lame i jusqu'à une jonction appuyée (None : bout libre)."""
        n = 0
        while n <= 20:
            k = cle_pt(b)
            if k not in appui_pt:
                appui_pt[k] = appuye(b)
            if appui_pt[k]:
                return n
            suiv = [j for j in par_bout[(k, round(lames[i][0][6] % 360))] if j != i]
            if not suiv:
                return None
            i = suiv[0]
            b = lames[i][1][1] if cle_pt(lames[i][1][0]) == k else lames[i][1][0]
            n += 1
        return None

    erreurs, portees, consoles, libres = [], [0], 0, [0]
    libre_max = 1 if mode == 'prudent' else LIBRE_MAX
    for i, (q, bb) in enumerate(lames):
        bas, haut = distance_appui(i, bb[0]), distance_appui(i, bb[1])
        if bas is not None and haut is not None:
            portees.append(bas + haut + 1)
            if bas + haut + 1 > PORTEE_MAX:
                erreurs.append((q, 'portée', (bas, haut)))
        elif haut == 0:
            consoles += 1                       # pend d'un appui
        elif bas is not None and bas + 1 <= libre_max:
            libres.append(bas + 1)              # monte librement au-dessus d'un appui
        else:
            erreurs.append((q, 'sans appui', (bas, haut)))
    for q, m, d in erreurs[:10]:
        print('  RAMPE', m, q[0], q[1], q[7], d)
    assert not erreurs, f'{len(erreurs)} rampes mal appuyées'
    # redondance : chaque ligne (chaîne de lames) tient-elle encore si l'un de ses appuis est détruit ?
    vu, lignes = set(), []
    for i0 in range(len(lames)):
        if i0 in vu:
            continue
        comp, file = [], [i0]
        vu.add(i0)
        while file:
            i = file.pop()
            comp.append(i)
            for b in lames[i][1]:
                for j in par_bout[(cle_pt(b), round(lames[i][0][6] % 360))]:
                    if j not in vu:
                        vu.add(j)
                        file.append(j)
        comp.sort(key=lambda i: lames[i][1][0][2])             # du bas vers le haut
        jonctions = [lames[comp[0]][1][0]] + [lames[i][1][1] for i in comp]
        S = {n for n, b in enumerate(jonctions) if appui_pt.setdefault(cle_pt(b), appuye(b))}
        lignes.append(([lames[i][0][7] for i in comp], S))

    systemes = ('toit rampes', 'pente A', 'appentis', 'casquette du trou', 'casquette', 'overhang')
    redondance = {}
    for reps, S in lignes:
        for i, r_ in enumerate(reps):
            r = redondance.setdefault(next(s for s in systemes if r_.startswith(s)), dict(lames=0, redondantes=0))
            r['lames'] += 1
            r['redondantes'] += len(S) >= 2 and all(lame_tient(i, S - {s}, libre_max) for s in S)
    print(f'  Appuis ({mode}) : {len(lames)} rampes ; portée maxi entre appuis {max(portees)} lames, {consoles} pendues '
          f'd\'une lame à leur appui, montée libre maxi {max(libres)} lames ; lames qui tiennent encore si un appui de '
          'leur ligne est détruit : ' + ', '.join(f"{k} {v['redondantes']}/{v['lames']}" for k, v in redondance.items()))
    return dict(mode=mode, rampes=len(lames), portee_max=max(portees), pendues=consoles, montee_libre_max=max(libres),
                montantes_libres=len(libres) - 1, redondance=redondance)


def chaume_a_demolir(plans, ordre):
    """Murs de chaume des tourelles (template 2727) : où ils sont, quelle tourelle ils portent, ce qui est posé
    au-dessus. Rien ne doit en dépendre seul (verifier_appuis ne compte pas le chaume comme appui)."""
    P_ = _pieces_plans(plans)
    par_pos = {}
    for q in P_:
        par_pos.setdefault((round(q[3]), round(q[4]), round(q[5])), []).append(q)
    num = {(round(s['xm']), round(s['ym']), round(s['Zb'])): s for s in ordre if s['posee']}
    out = []
    for q in P_:
        if q[2] != 'chaume_mur':
            continue
        dessus = [v[2] for v in par_pos.get((round(q[3]), round(q[4]), round(q[5] + F)), [])]
        s_ = num[(round(q[3]), round(q[4]), round(q[5] - Z_TPL - F / 2))]
        out.append(dict(plan=next(f[:7] for k, f, *_ in PLANS if k == q[0]), entree=q[1], ordre=s_['ordre'], couche=s_['couche'], tourelle=NOMS[s_['type']],
                        x=q[3], y=q[4], Z_bas=q[5] - Z_TPL - F / 2, dessus=NOMS[dessus[0]] if dessus else 'rien'))
    return sorted(out, key=lambda c: c['ordre'])


def cellule_escalier(x0, y0, yaw):
    """Emprise 300 × 300 de la colonne d'escaliers (axes = yaw de l'escalier)."""
    nx, ny = vec(yaw)
    dx, dy = -ny, nx
    return [(x0 + u * nx + v * dx, y0 + u * ny + v * dy) for u, v in ((-150, -150), (150, -150), (150, 150), (-150, 150))]


# ---------------------------------------------------------------- modules
def module_sol(p):
    """Pavage complet sans les fondations du trou, petite plateforme verte comprise (rien n'y est accroché) : plan 1."""
    pieces, contours = pavage(p['anneaux_total'])
    t = Template('01 Sol', 'Pavage carres+triangles en etoile, Ø30 (D8), sans les fondations du trou. Bord abaisse en 2 '
                           f"paliers : anneau 14 (Ø26-Ø28) a -{p['decaissement']:.0f} UU, anneau 15 (Ø28-Ø30) a "
                           f"-{2 * p['decaissement']:.0f} UU. Origine = centre de l'etoile.")
    ancre(t, empilee=True)
    t.groupe = t.phase = 'sol'
    trou = []
    for pc in pieces:
        if piece_dans_trou(p, pc):
            trou.append(pc)
            continue
        Z = cote_anneau(p, pc['anneau'])
        cle = 'fond' if pc['type'] == 'carre' else 'fond_tri'
        t.add(cle, pc['x'], pc['y'], Z + Z_TPL - 50, pc['yaw'], Z=Z,
              repere=('plateforme verte ' if piece_plateforme(p, pc) else '')
              + f"anneau {pc['anneau']} cote {pc['cote']} n{pc['idx']}")
    return t, pieces, contours, trou


def pod_niveau(p, niv, x, y, k, i):
    """Pièce d'un niveau du mur de pod D4 (tour en murs pleins) : mur, ou cadre double pour ses ouvertures (1 porte
    au sol par part sur les côtés E1, index 1 ; accès aux galeries à Z1800, index 1)."""
    if (niv == 0 and k % 2 == 1 and i == 1) or (niv * F == p['mezzanine'] and i == 1):
        return 'cadre_double'
    return 'mur'


def piliers_centre(p):
    """Colonnes porteuses du pod : PA aux sommets de D2, PB aux sommets de D1 (hors du trou) : (nom, x, y)."""
    out = []
    for nom, n in (('PA', 2), ('PB', 1)):
        R = rayon_coin(n)
        for k in range(12):
            cx, cy = vec(15 + 30 * k)
            if not dans_trou(p, R * cx, R * cy):
                out.append((f'{nom}{k}', R * cx, R * cy))
    return out


def module_pod(p, contours, D):
    """Tour du pod : mur de pod D4 en murs pleins, du sol au niveau pod_niveaux − 1 (Z2700) ; son dernier niveau,
    au-dessus du toit de cage, porte l'anneau de tourelles D4 (emplacements laissés libres : plan des tourelles du
    périmètre). Colonne d'escaliers, piliers PA et PB du sol au haut de la tour, mezzanine Z1800. Les murs de bord du
    trou du pod sont posés avec les autres murs de bord (module_rampe). La couronne, le plancher de toit et le toit se
    posent dessus (module_toit), calés sur un mur de D4 : la tour peut être rehaussée (rehausse())."""
    t = Template('02 Pod central atelier', 'Tour du pod D4 en murs pleins, colonne d\'escaliers jusqu\'a la mezzanine, '
                                         'piliers porteurs, mezzanine Z1800.')
    ancre(t)
    d4 = contours[p['anneau_pod']]
    zmez = p['mezzanine']
    t.groupe = t.phase = 'pod'
    # colonne d'escaliers du hall à la mezzanine (à l'ancienne place de l'escalier du Coeur Base)
    xe, ye, yawe = ESCALIER
    for niv in range(int(zmez // F)):
        t.add('escalier', xe, ye, niv * F + Z_TPL + F / 2, yawe, Z=niv * F, repere=f'escalier niv{niv}')
    Ztop = p['pod_niveaux'] * F
    assert Ztop >= zmez + (p['cage_niveaux'] + 1) * F, "la tour du pod doit dépasser le toit de cage d'un niveau"
    libres = {(round(s['xm'], 1), round(s['ym'], 1), s['Zb']) for s in D['slots'] if s['couche'] == 'D4'}
    for niv in range(p['pod_niveaux']):
        Zb = niv * F
        for x, y, nu, k, i in cotes_contour(d4):
            if dans_trou(p, x, y, bord=True) or (round(x, 1), round(y, 1), Zb) in libres:
                continue                       # coupé par le trou (le mur de bord du trou ferme le pod) ; tourelle
            t.add(pod_niveau(p, niv, x, y, k, i), x, y, Zb + Z_TPL + F / 2, nu, Z=Zb, repere=f'pod niv{niv} c{k} p{i}')
    # piliers PA et PB du sol au haut de la tour : aucun plafond du centre n'est à plus de 2 cases d'un appui relié au
    # sol ; la couronne et chaque rehausse en ajoutent un niveau
    for nom, x, y in piliers_centre(p):
        for niv in range(p['pod_niveaux']):
            t.add('pilier', x, y, niv * F + Z_TPL + F / 2, 0, Z=niv * F, repere=f'pilier {nom}')
    cages_noyau(t, p)
    # mezzanine Z1800 : centre + anneaux 1..7 en plafonds, trémie = pièces traversées par la colonne d'escaliers
    cellule = cellule_escalier(xe, ye, yawe)
    pieces, _ = pavage(p['anneau_pod'], centre=True)
    tremie = []
    for pc in pieces:
        if se_coupent(polygone(pc), cellule):
            tremie.append(pc)
            continue
        if piece_dans_trou(p, pc):
            continue
        cle = 'plafond' if pc['type'] == 'carre' else 'plafond_tri'
        t.add(cle, pc['x'], pc['y'], zmez + Z_TPL, pc['yaw'], Z=zmez, repere=f"mezzanine anneau {pc['anneau']}")
    # Zsommet : recalculé après consolidation des rampes (lames en collision retirées)
    return t, dict(Zsommet=Ztop + F + apo(4), Ztoit=Ztop + F, Zpod=Ztop, escalier=dict(x=xe, y=ye, yaw=yawe),
                   cellule=cellule, tremie=tremie)


def murs_couronne(p, contours, niv):
    """Murs d'un niveau de la tour au-dessus de son haut (couronne ou rehausse) : murs de D4 et murs de bord du trou
    du pod : (x, y, yaw, repère, colonne de référence ou None)."""
    out = []
    for x, y, nu, k, i in cotes_contour(contours[p['anneau_pod']]):
        if dans_trou(p, x, y, bord=True):
            continue
        col = next((c for c, ki in REF_MURS.items() if ki == (k, i)), None)
        out.append((x, y, nu, f'niv{niv} c{k} p{i}', col))
    for x, y, nu, r, th in bords_trou(p):
        if r <= apo(4) + 1:
            out.append((x, y, nu, f'bord du trou niv{niv} θ{th:.1f}', None))
    return out


def module_toit(p, contours):
    """Haut de la tour du pod, calé sur des murs de D4 de référence (REF_MURS) pour suivre la hauteur de la tour :
    - toiture pleine (plan 9) : couronne de murs pleins (D4 et bord du trou du pod) au niveau pod_niveaux, sauf les
      colonnes B et C, niveau supplémentaire des piliers PA et PB, plancher de toit (anneaux 0 à 7) avec une trappe ;
      mur de référence A. Elle ferme le pod seule : toit plat ;
    - toit en rampes (plan 10) : mur C, toit en rampes inclinées de D4 jusqu'au centre et leurs poteaux, posés sur le
      plancher de toit ; casquette du trou au-dessus des murs de bord du pod ;
    - le mur B est le mur de référence des tourelles du dessus (plan 11, module_tourelles)."""
    t = Template('Toit D4-centre', 'Couronne, plancher de toit, toit en rampes inclinees de D4 au centre.')
    ancre(t)
    N = p['pod_niveaux']
    Zc, Ztop = N * F, (N + 1) * F
    for x, y, nu, rep_, col in murs_couronne(p, contours, N):
        t.groupe = t.phase = {'B': 'tourelles_dessus', 'C': 'toit_rampe'}.get(col, 'toiture_pleine')
        rep_ = (f'reference {col} : mur de D4 a snapper sur le haut du mur de pod ({rep_})' if col
                else ('couronne ' if not rep_.startswith('bord') else '') + rep_)
        t.add('mur', x, y, Zc + Z_TPL + F / 2, nu, Z=Zc, repere=rep_)
    t.groupe = t.phase = 'toiture_pleine'
    for nom, x, y in piliers_centre(p):
        t.add('pilier', x, y, Zc + Z_TPL + F / 2, 0, Z=Zc, repere=f'pilier {nom} (couronne)')
    pieces, _ = pavage(p['anneau_pod'], centre=True)
    trappe = (1, 0, 0)                           # carré de l'anneau 1 à θ 0° : échelle depuis la mezzanine
    for pc in pieces:
        if piece_dans_trou(p, pc):
            continue
        cle = 'trappe' if cle_piece(pc) == trappe else 'plafond' if pc['type'] == 'carre' else 'plafond_tri'
        t.add(cle, pc['x'], pc['y'], Ztop + Z_TPL, pc['yaw'], Z=Ztop, repere=f"plancher de toit anneau {pc['anneau']}")
    t.groupe = t.phase = 'toit_rampe'
    pente(t, 'toit', apo(4), Ztop, +1, 'toit rampes', filtre=lambda x, y: dans_trou(p, x, y))   # joints de D4
    hauts = [m for m in bords_trou(p) if m[3] <= apo(4) + 1]
    for n, (x, y, nu, th) in enumerate(casquette_trou(p, hauts)):
        t.add('rampe', x, y, Ztop - F + Z_TPL + 200, nu - 90, Z=Ztop - F, repere=f'casquette du trou θ{th:.1f}',
              meta=dict(sys='casquette du trou', k=n, t=0.0, rang=0, sens=-1))
    return t, dict(Zcouronne=Zc, Ztoit=Ztop)


def rehausse(p, contours):
    """Option : un niveau de plus pour la tour du pod (murs pleins de D4 et du bord du trou, piliers PA et PB), calé sur
    le mur de référence A comme la toiture pleine. À poser autant de fois que voulu avant la toiture pleine ; la
    toiture, le toit en rampes et les tourelles du dessus se posent ensuite sur le haut de la dernière rehausse."""
    N = p['pod_niveaux']
    t = Template('Option rehausse pod +1 niveau',
                 "Un niveau de plus pour la tour du pod (murs pleins D4 et bord du trou, piliers PA/PB). Mur de "
                 "reference A : le mur de D4 du cote θ 90° au-dessus de la porte du hall (x = +150), a snapper sur le "
                 "haut du mur de pod. A poser avant la toiture pleine, autant de fois que voulu.")
    murs = murs_couronne(p, contours, N)
    murs.sort(key=lambda m: m[4] != 'A')
    for x, y, nu, rep_, col in murs:
        t.add('mur', x, y, N * F + Z_TPL + F / 2, nu, Z=N * F,
              repere=(f'reference A : mur de D4 a snapper sur le haut du mur de pod ({rep_})' if col == 'A'
                      else 'rehausse ' + rep_))
    for nom, x, y in piliers_centre(p):
        t.add('pilier', x, y, N * F + Z_TPL + F / 2, 0, Z=N * F, repere=f'pilier {nom} (rehausse)')
    t.snap = [0]
    return t


def colonnade(p):
    """Couronne de piliers sur un vrai cercle, yaw radial (style template 704) : 1 pilier, 1 vide de même largeur.

    Chaque colonne monte de Z0 à la hauteur du mur de rive (colonnade_hauteur), sans dépasser la pente A
    (piliers pleins puis un demi-pilier si la place le permet).
    """
    R = p['colonnade_rayon']
    w = p['largeur_pilier']
    n = 12 * round(2 * math.pi * R / (2 * w) / 12)
    pas = 360.0 / n
    colonnes = []
    for i in range(n):
        th = (i + 0.5) * pas
        if any(abs(ecart(th, o)) * math.pi / 180 * R < p['colonnade_largeur_passage'] / 2
               for o in p['colonnade_passages']):
            continue
        x, y = R * vec(th)[0], R * vec(th)[1]
        if dans_trou(p, x, y):
            continue
        h = min(hauteur_pente_A(p, x, y) - 30, p['colonnade_hauteur'])    # 30 UU de jeu sous le toit
        if R < apo(5):                               # couloir : sous le plancher de galerie Z1800
            h = min(h, p['mezzanine'])
        elements = []
        Z = 0.0
        while Z + F <= h:
            elements.append(('pilier', Z))
            Z += F
        if Z + F / 2 <= h:
            elements.append(('demi_pilier', Z))
            Z += F / 2
        colonnes.append(dict(theta=th, x=x, y=y, elements=elements, sommet=Z, toit=h + 30))
    return dict(rayon=R, n=n, pas_angulaire=pas, pas_arc=2 * math.pi * R / n, colonnes=colonnes)


def geometrie_jupe(p):
    """Mur de jupe sur l'arête extérieure de l'anneau 15 (bord D8) : un seul niveau, posé sur le palier 2 (Z −300 → 0).
    Rien n'est posé sous le niveau des fondations (le niveau suspendu et les tourelles de jupe ont été retirés)."""
    A8 = apo(p['anneaux_total'] // 2 + 1)
    Zp = cote_anneau(p, p['anneaux_total'])
    return dict(A=A8, Z=Zp, Z_haut=Zp + F) if p['jupe'] else None


def module_rampe(p, contours, D):
    """Anneaux extérieurs, en cadres doubles : bord D8 -> D7 (mur de rive, overhang, mur de jupe, débord, leurs appuis),
    colonnade (option), D7 -> D5 (pente A et ses poteaux de stabilité) et murs de bord du trou de chaque zone (ceux du
    pod en murs pleins)."""
    t = Template('03 Rive, colonnade, rampes de glisse et overhang',
                 f"Mur de rive D7 ({p['rive_niveaux']} niveaux), colonnade circulaire, {p['rangs_pente_A']} rangs de "
                 f"rampes inclinees vers la cage, overhang 2 + {p['debord']} rangs de rampes (debord accroche a la jupe), "
                 "poteaux et poutres d'appui des rampes, mur de jupe, murs de bord du trou.")
    ancre(t)
    hors_trou = lambda x, y: dans_trou(p, x, y)
    d7 = contours[p['anneau_rive']]
    murs = cotes_contour(d7)
    libres = {(round(s_['xm'], 1), round(s_['ym'], 1), s_['Zb']) for s_ in D['slots'] if s_['type'] != 'crop'}
    t.groupe = t.phase = 'D8-D7'
    for niv in range(p['rive_niveaux']):
        Zb = niv * F
        for x, y, nu, k, i in murs:
            if dans_trou(p, x, y, bord=True):
                continue                       # pas de rive au-dessus du trou : le mur de bord du trou la remplace
            if (round(x, 1), round(y, 1), Zb) in libres:
                continue                       # emplacement laissé libre : mur de chaume + Tesla (plan des tourelles)
            t.add('cadre_double', x, y, Zb + Z_TPL + F / 2, nu, Z=Zb, repere=f'rive niv{niv} c{k} p{i}')
    # colonnade circulaire sous la pente A (option : les poteaux de stabilité de la pente A la remplacent)
    t.groupe = t.phase = 'colonnade'
    col = colonnade(p)
    for c in col['colonnes']:
        for cle, Z in c['elements']:
            dz = F / 2 if cle == 'pilier' else F / 4
            t.add(cle, c['x'], c['y'], Z + Z_TPL + dz, c['theta'], Z=Z, repere=f"colonnade θ{c['theta']:.2f}")
    # pente A : de la rive vers la cage, lignes de lames sur les joints des murs de rive (le milieu des murs reste libre
    # pour les Tesla)
    A7 = apo(7)
    Zr = p['rive_niveaux'] * F
    t.groupe = t.phase = 'D7-D5'
    pente(t, 'pente A', A7, Zr, +1, 'pente A', nb=p['rangs_pente_A'], demi=True, filtre=hors_trou)
    # overhang : les mêmes lignes descendent de la rive au-dessus des 2 paliers (poteau sur le palier, voir
    # consolider_rampes) et finissent 40 UU après le bord de plateforme
    t.groupe = t.phase = 'D8-D7'
    pente(t, 'overhang', A7, Zr, -1, 'overhang', nb=2, demi=True, filtre=hors_trou)
    jupe = geometrie_jupe(p)
    if jupe:
        Zb = jupe['Z']
        for x, y, nu, k, i in cotes_contour(contours[p['anneaux_total']]):
            if dans_trou(p, x, y, bord=True):
                continue
            t.add('cadre_double', x, y, Zb + Z_TPL + F / 2, nu, Z=Zb, repere=f'jupe mur c{k} p{i}')
        # pas de plafond sous l'overhang : ce qui passe entre les rampes doit tomber dans le vide
        # débord : 'debord' rangs dans le vide, ancrés sur le haut de la jupe, sur les joints de ses murs (entre les
        # lignes de l'overhang) ; avec 2 rangs, le 2e pend au bout d'une poutre fine (Template Hammer)
        pente(t, 'debord', jupe['A'], jupe['Z_haut'], -1, 'overhang', nb=p['debord'], filtre=hors_trou, rang0=2)
    A_bout = (jupe['A'] + p['debord'] * F) if jupe else A7 + 2 * F
    Z_bout = (jupe['Z_haut'] - p['debord'] * F) if jupe else Zr - 2 * F
    # bord du trou : murs sur les arêtes entre fondations conservées et trou, qui ferment la coupe jusqu'à
    # l'enveloppe ; les tourelles qui tombaient dans le trou y sont reposées, face au gouffre (defense())
    bord = bords_trou(p)
    for x, y, nu, r, th in bord:
        t.groupe = t.phase = groupe_bord(p, r)
        for niv in range(niveaux_bord_trou(p, r)):
            if (round(x, 1), round(y, 1), niv * F) in libres:
                continue
            t.add('mur' if r <= apo(4) + 1 else 'cadre_double', x, y, niv * F + Z_TPL + F / 2, nu, Z=niv * F,
                  repere=f'bord du trou niv{niv} θ{th:.1f}')
    return t, murs, dict(A_bout=A_bout, Z_bout=Z_bout), jupe, col, bord


def module_cage(p, contours, D):
    """D5 -> D4 : fût D5 en cadres doubles de Z0 à la galerie, niveau L1 (emplacements de tourelles laissés libres pour
    le plan des tourelles, cadres doubles ailleurs), L2 en cadres doubles, planchers de galerie des anneaux 8-9 (Z1800,
    2100, toit de cage 2400), casquette vers l'extérieur, appentis : 1 rang de rampes qui monte du haut de D5 vers la
    tour du pod, chaque lame sur un poteau de stabilité ; casquette du trou au-dessus des murs de bord du couloir."""
    t = Template('04 Cage a tourelles et casquette',
                 'Fut D5 en cadres doubles, galerie 2 niveaux : L1 = emplacements de tourelles, L2 = cadres doubles ; '
                 'planchers anneaux 8-9, casquette, appentis vers la tour du pod.')
    ancre(t)
    t.groupe = t.phase = 'D5-D4'
    d5 = contours[p['anneau_cage']]
    zmez = p['mezzanine']
    libres = {(round(s['xm'], 1), round(s['ym'], 1), s['Zb']) for s in D['slots'] if s['couche'] == 'L1'}
    # fût et L1 : cadres doubles de Z0 à Z2100, sauf les emplacements des tourelles L1
    for niv in range(int(zmez // F) + 1):
        Zb = niv * F
        for x, y, nu, k, i in cotes_contour(d5):
            if dans_trou(p, x, y, bord=True) or (round(x, 1), round(y, 1), Zb) in libres:
                continue                       # coupé par le trou (le mur de bord du trou ferme la cage) ; tourelle
            rep_ = f'fut niv{niv} c{k} p{i}' if Zb < zmez else f'cage L1 c{k} p{i}'
            t.add('cadre_double', x, y, Zb + Z_TPL + F / 2, nu, Z=Zb, repere=rep_)
    # planchers de galerie : anneaux 8 et 9 en plafonds, à chaque niveau + toit de cage
    pieces, _ = pavage(p['anneau_cage'], centre=False)
    gal = [pc for pc in pieces if pc['anneau'] > p['anneau_pod']
           and not (piece_dans_trou(p, pc) or piece_plateforme(p, pc))]
    for niv in range(p['cage_niveaux'] + 1):
        Z = zmez + niv * F
        for pc in gal:
            cle = 'plafond' if pc['type'] == 'carre' else 'plafond_tri'
            if niv == 1 and pc['type'] == 'carre' and pc['anneau'] == p['anneau_pod'] + 1 \
                    and pc['cote'] % 2 == 1 and pc['idx'] == 0:
                cle = 'trappe'          # trappe + échelle vers la galerie L2
            t.add(cle, pc['x'], pc['y'], Z + Z_TPL, pc['yaw'], Z=Z, repere=f"galerie Z{Z:.0f} anneau {pc['anneau']}")
    # L2 : cadres doubles
    Zb = zmez + F
    for x, y, nu, k, i in cotes_contour(d5):
        if dans_trou(p, x, y, bord=True):
            continue
        t.add('cadre_double', x, y, Zb + Z_TPL + F / 2, nu, Z=Zb, repere=f'cage L2 c{k} p{i}')
    # casquette (porte-à-faux vers l'extérieur) et appentis (vers la tour du pod), ancrés sur le haut de D5
    A5 = apo(5)
    Ztop = zmez + p['cage_niveaux'] * F
    hors_trou = lambda x, y: dans_trou(p, x, y)
    pente(t, 'casquette', A5, Ztop, -1, 'casquette', nb=p['casquette'], demi=True, filtre=hors_trou)   # joints de D5
    pente(t, 'appentis', A5, Ztop, +1, 'appentis', nb=1, demi=True, filtre=hors_trou)
    hauts = [m for m in bords_trou(p) if apo(4) + 1 < m[3] <= apo(5) + 1]
    for n, (x, y, nu, th) in enumerate(casquette_trou(p, hauts)):
        t.add('rampe', x, y, Ztop - F + Z_TPL + 200, nu - 90, Z=Ztop - F, repere=f'casquette du trou θ{th:.1f}',
              meta=dict(sys='casquette du trou', k=100 + n, t=0.0, rang=0, sens=-1))
    return t, gal


# gabarits de réservation dans le hall du pod (Z0 -> 1800) : (nom, θ, apothème du centre, largeur, profondeur, murs)
GABARITS = [
    ('Réplicateur Tek', 0, 1650, 900, 600, 3),
    ('Forge à vapeur', 120, 1650, 900, 900, 3),
    ('Labo de fortune (Megalab)', 240, 1650, 600, 600, 2),
    ('Stockages dédiés', 300, 1600, 1500, 600, 2),
]
# noyau : 2 générateurs Tek (principal et secours) et 2 boîtes de munitions, chacun posé sur une fondation carrée de
# l'anneau 1 (au centre de la base, au plus loin de tous les murs extérieurs) et enfermé dans une cage de murs métal
# (2 murs de haut, porte double côté hall, plafond)
NOYAU = [('Générateur Tek n°1 (principal)', 180, 'generateur_tek'), ('Générateur Tek n°2 (secours)', 240, 'generateur_tek'),
         ('Boîte de munitions n°1', 60, 'boite_munitions'), ('Boîte de munitions n°2', 120, 'boite_munitions')]
A_NOYAU = H + F / 2                              # apothème du centre des carrés de l'anneau 1
GENERATEURS = [(nom, th, A_NOYAU, 0.0) for nom, th, cle in NOYAU if cle == 'generateur_tek']
CAGE_NIVEAUX = 2


def cages_noyau(t, p):
    """Cages du noyau (NOYAU) : murs métal sur les 4 côtés de chaque carré, CAGE_NIVEAUX de haut ; au niveau 0 le
    côté tourné vers le hall est un cadre de porte double (porte à poser) ; plafond au-dessus."""
    pieces, _ = pavage(1, centre=False)
    carres = {pc['cote'] * 30: pc for pc in pieces if pc['type'] == 'carre'}
    for nom, th, cle in NOYAU:
        pc = carres[th]
        assert not piece_dans_trou(p, pc), nom
        for niv in range(CAGE_NIVEAUX):
            for d in (0, 90, 180, 270):
                nu = pc['yaw'] + d
                x, y = pc['x'] + F / 2 * vec(nu)[0], pc['y'] + F / 2 * vec(nu)[1]
                cle_m = 'cadre_double' if niv == 0 and abs(ecart(nu, th)) < 1 else 'mur'
                t.add(cle_m, x, y, niv * F + Z_TPL + F / 2, nu, Z=niv * F, repere=f'cage du noyau θ{th} niv{niv}')
        Zp = CAGE_NIVEAUX * F
        t.add('plafond', pc['x'], pc['y'], Zp + Z_TPL, pc['yaw'], Z=Zp, repere=f'cage du noyau θ{th} plafond')


def equipements(p, contours):
    """Positions des équipements hors plan : machines du hall, noyau (2 générateurs Tek et 2 boîtes de munitions, en
    cage), 20 coffres-forts, 20 stockages dédiés.

    Mezzanine : emplacements contre la face intérieure du mur de pod (positions 0, 2 et 3 de chaque côté ; la
    position 1 est l'accès galerie), sauf ceux que le trou a coupés (31 sur 36) -> 20 coffres-forts répartis
    régulièrement + 11 stockages dédiés. Les autres stockages dédiés vont dans le hall (θ 300°, 2 rangées).
    """
    out = []
    places = sorted(((x, y, nu, k, i) for x, y, nu, k, i in cotes_contour(contours[7]) if i != 1),
                    key=lambda m: math.degrees(math.atan2(m[1], m[0])) % 360)
    places = [m for m in places if not dans_trou(p, m[0], m[1], bord=True)
              and not dans_trou(p, m[0] - 150 * vec(m[2])[0], m[1] - 150 * vec(m[2])[1])]
    n_hall = 40 - len(places)                  # 20 coffres-forts + 20 stockages dédiés au total
    for nom, th, A, lg, pf, hm in GABARITS:
        cle = {'Réplicateur Tek': 'replicateur', 'Forge à vapeur': 'forge_vapeur',
               'Labo de fortune (Megalab)': 'megalab'}.get(nom)
        if cle:
            out.append(dict(cle=cle, x=A * vec(th)[0], y=A * vec(th)[1], Z=0.0, yaw=th + 180, lieu='hall'))
        elif nom.startswith('Stockages'):
            nx, ny = vec(th)
            dx, dy = -ny, nx
            cases = [(A + 150, t) for t in (-450, -150, 150, 450)] + [(A - 150, t) for t in (-600, -300, 0, 300, 600)]
            assert n_hall <= len(cases), n_hall
            # rangée extérieure dos au hall, face au mur de pod ; rangée intérieure face au hall : allée d'au moins
            # une fondation entre la rangée extérieure et le mur de pod
            assert apo(4) - 10 - (A + 300) >= F - 1, "allée de moins d'une fondation derrière les stockages"
            for a, t in cases[:n_hall]:
                out.append(dict(cle='stockage_dedie', x=a * nx + t * dx, y=a * ny + t * dy, Z=0.0,
                                yaw=th if a > A else th + 180, lieu='hall'))
    for nom, th, cle in NOYAU:
        out.append(dict(cle=cle, x=A_NOYAU * vec(th)[0], y=A_NOYAU * vec(th)[1], Z=0.0, yaw=th, lieu='noyau (cage)'))
    types = repartir(len(places), {'coffre_fort': 20, 'stockage_dedie': len(places) - 20})
    for (x, y, nu, k, i), cle in zip(places, types):
        nx, ny = vec(nu)
        out.append(dict(cle=cle, x=x - 150 * nx, y=y - 150 * ny, Z=1800.0, yaw=nu + 180, lieu='mezzanine'))
    for q in out:
        assert not dans_trou(p, q['x'], q['y']), q
    return out


def tableau_anneaux(p):
    pieces, contours = pavage(p['anneaux_total'])
    lignes = []
    for r in range(1, p['anneaux_total'] + 1):
        pr = [pc for pc in pieces if pc['anneau'] == r]
        a, L = contours[r]
        zone = ('pod' if r <= p['anneau_pod'] else f"palier {r - p['anneau_rive']}" if r > p['anneau_rive']
                else 'couronne')
        trou = sum(1 for pc in pr if piece_dans_trou(p, pc))
        lignes.append(dict(anneau=r, carres_sur='E0 (0°,60°…)' if r % 2 else 'E1 (30°,90°…)',
                           carres=sum(pc['type'] == 'carre' for pc in pr),
                           tri_ext=sum(pc['type'] == 'tri' and pc['idx'] < L[pc['cote']] - 1 for pc in pr),
                           triangles=sum(pc['type'] == 'tri' for pc in pr),
                           par_cote_E0=L[0], par_cote_E1=L[1], apo_E0=round(a[0], 1), apo_E1=round(a[1], 1),
                           zone=zone, Z=cote_anneau(p, r), retirees_trou=trou))
    return lignes


# ---------------------------------------------------------------- tourelles verticales
def emplacement(x_mur, y_mur, Zb, sortie, couche, cote, idx):
    """Emplacement de mur occupé par un mur de chaume ; la tourelle est sur sa face côté « sortie »."""
    nx, ny = vec(sortie)
    return dict(xm=x_mur, ym=y_mur, Zb=Zb, sortie=sortie, couche=couche, cote=cote, idx=idx,
                x=x_mur + DECALAGE_MONTAGE * nx, y=y_mur + DECALAGE_MONTAGE * ny, Z=Zb + F / 2)


def emplacements_cage(p, contours):
    """L1 : les 60 emplacements de la ligne D5 entre Z1800 et Z2100, tourelle côté extérieur."""
    return [emplacement(x, y, p['mezzanine'], nu, 'L1', k, i) for x, y, nu, k, i in cotes_contour(contours[p['anneau_cage']])]


def murs_tesla(murs, p):
    """Index des murs de rive (niveau 1) au milieu des côtés E0 (θ = 0°, 60°…), plus ceux des côtés E1 de
    p['tesla_rive_E1'] (aucun par défaut : les Tesla comptent dans le cap de 100)."""
    return [j for j, m in enumerate(murs) if m[4] == 3 and (m[3] % 2 == 0 or m[3] in p['tesla_rive_E1'])]


def choisir(seq, n):
    """n éléments de seq répartis régulièrement (seq dans l'ordre angulaire : une couche reste répartie sur 360°)."""
    assert 0 <= n <= len(seq), (n, len(seq))
    return [seq[int(i * len(seq) / n)] for i in range(n)]


def emplacements_dessus(p):
    """Dessus de la tour : sur le plancher de toit, à l'apothème p['dessus_apotheme'], à t = +150 sur chaque côté hors
    du trou (entre deux lignes de rampes du toit, loin de leurs poteaux) : tourelles et Tesla debout, carrés de culture de
    Plant Species X, dans l'ordre de p['dessus'], répartis autour du cercle. Elles couvrent le toit, le ciel au-dessus du
    centre et le comble (ce qui passe entre les lames ; les lames, espacées de 300 UU, ne masquent pas le tir)."""
    Ztop = (p['pod_niveaux'] + 1) * F
    A = p['dessus_apotheme']
    places = [k for k in range(12) if not dans_trou(p, A * vec(30 * k)[0] + F / 2 * vec(30 * k + 90)[0],
                                                     A * vec(30 * k)[1] + F / 2 * vec(30 * k + 90)[1])]
    out = []
    for n, (k, ty) in enumerate(zip(choisir(places, len(p['dessus'])), p['dessus'])):
        x = A * vec(30 * k)[0] + F / 2 * vec(30 * k + 90)[0]      # t = +150 : entre les lignes t = 0 et t = +300
        y = A * vec(30 * k)[1] + F / 2 * vec(30 * k + 90)[1]
        out.append(dict(xm=x, ym=y, x=x, y=y, Zb=Ztop, Z=Ztop + 75, sortie=30 * k, couche='DESSUS', cote=k, idx=n,
                        type='crop' if ty == 'plante_x' else ty, plan='dessus'))
    return out


def emplacements_d4(p, contours):
    """Anneau de tourelles de la tour du pod : dernier niveau du mur de pod (Z2400 -> 2700), juste au-dessus du toit de
    cage. Une tourelle par côté sur le mur d'index 0 (sinon le premier hors du trou et hors des colonnes de référence),
    Tek et Heavy alternées ; une Tesla en plus sur les côtés p['d4_tesla'] (mur d'index 2). Elles couvrent le toit de
    cage, la poche entre l'appentis et la tour, la casquette et le ciel. Renvoie (emplacements, types des tourelles des
    côtés entièrement coupés par le trou, à reposer sur un mur de bord du pod)."""
    Zb = (p['pod_niveaux'] - 1) * F
    murs = {(k, i): (x, y, nu) for x, y, nu, k, i in cotes_contour(contours[p['anneau_pod']])}
    refs = set(REF_MURS.values())
    libre = lambda k, i: (k, i) not in refs and not dans_trou(p, *murs[(k, i)][:2], bord=True)
    out, coupes = [], []
    for k in range(12):
        ty = 'tek' if k % 2 == 0 else 'heavy'
        i = next((i for i in (0, 3, 1, 2) if libre(k, i)), None)
        if i is None:
            coupes.append(ty)
            continue
        x, y, nu = murs[(k, i)]
        out.append(dict(emplacement(x, y, Zb, nu, 'D4', k, i), type=ty))
        if k in p['d4_tesla']:
            assert libre(k, 2) and i != 2, k
            x, y, nu = murs[(k, 2)]
            out.append(dict(emplacement(x, y, Zb, nu, 'D4', k, 2), type='tesla'))
    return out, coupes


def cultures(p):
    """Carrés de culture de Plant Species X (chaque plante compte dans le cap de 100), au centre d'un carré du pavage :
    - D8 -> D4 : dans l'attique, sous la pente A, carré de l'anneau 11 au milieu des côtés E0 (t = +150), là où tombe
      ce qui passe entre les lames ;
    - périmètre du pod : sur le toit de cage Z2400, au pied de la tour, à hauteur des carrés de l'anneau 8 des côtés
      E1, au milieu du côté (t = 0), entre deux lignes de l'appentis (sur les joints de D5, t = ±150) et leurs
      poteaux."""
    pieces, _ = pavage(p['anneaux_total'])
    out = []
    for anneau, Z, couche, plan in ((11, 0.0, 'X-attique', 'ext'),
                                    (p['anneau_pod'] + 1, p['mezzanine'] + p['cage_niveaux'] * F, 'X-D4', 'd4')):
        for pc in pieces:
            nx, ny = vec(30 * pc['cote'])
            if (pc['anneau'] == anneau and pc['type'] == 'carre' and abs(-ny * pc['x'] + nx * pc['y'] - 150) < 1
                    and not piece_dans_trou(p, pc) and not piece_plateforme(p, pc)):
                x = pc['x'] - (F / 2 * -ny if couche == 'X-D4' else 0)      # X-D4 : ramené à t = 0
                y = pc['y'] - (F / 2 * nx if couche == 'X-D4' else 0)
                out.append(dict(xm=x, ym=y, x=x, y=y, Zb=Z, Z=Z + 30, sortie=pc['yaw'],
                                couche=couche, cote=pc['cote'], idx=pc['idx'], type='crop', plan=plan))
    return out


def emplacements_trou(p, bord, n_heavy, n_tesla, types_L1, types_D4, occupes=()):
    """Tourelles reposées sur les murs de bord du trou, face au gouffre, pour garder le même nombre de tourelles.

    - types_L1 (tourelles de la cage coupées) : au niveau 6 (Z1800, celui de L1) des murs de bord intérieurs à D5,
      accessibles depuis la galerie et la mezzanine ; les plus proches de la cage d'abord ;
    - types_D4 (anneau de la tour coupé) : au dernier niveau de la tour (Z2400) des murs de bord du pod, sur une autre
      colonne que celles de L1 ;
    - n_heavy (jupe) au niveau 0 et n_tesla (rive) au niveau 1 des murs de bord extérieurs à D5, les plus proches
      du bord de la plateforme d'abord, chacune sur un mur différent : une colonne de murs de bord n'a jamais qu'un
      seul mur de chaume (comme sur la tour 1809, le mur posé au-dessus reste tenu par ses voisins).
    Un mur dont la tourelle serait à moins de p['ecart_tourelles'] d'une autre (occupes, ou déjà reposée) est sauté.
    """
    pris_ = list(occupes)

    def libre(m, Zb):
        s = emplacement(m[0], m[1], Zb, m[2], '', 0, 0)
        return all(math.dist((s['x'], s['y'], s['Z']), (o['x'], o['y'], o['Z'])) >= p['ecart_tourelles'] for o in pris_)

    def choisir_murs(murs_, n, Zb):
        out_ = []
        for m in murs_:
            if len(out_) == n:
                break
            if libre(m, Zb):
                out_.append(m)
                pris_.append(emplacement(m[0], m[1], Zb, m[2], '', 0, 0))
        assert len(out_) == n, 'pas assez de murs de bord pour reposer les tourelles'
        return out_
    interieurs = sorted((m for m in bord if m[3] <= apo(5) + 1), key=lambda m: -m[3])
    exterieurs = sorted((m for m in bord if m[3] > apo(5) + 1), key=lambda m: -m[3])
    types = []
    nT, nH = types_L1.count('tek'), types_L1.count('heavy')
    while nT or nH:                              # alternance Tek / Heavy le long du bord
        if nT >= nH and nT:
            types.append('tek')
            nT -= 1
        else:
            types.append('heavy')
            nH -= 1
    assert len(interieurs) >= len(types), 'pas assez de murs de bord pour reposer les tourelles de la cage'
    assert len(exterieurs) >= n_heavy + n_tesla, 'pas assez de murs de bord pour reposer Heavy et Tesla'
    out = []
    for n, ((x, y, nu, r, th), ty) in enumerate(zip(choisir_murs(interieurs, len(types), p['mezzanine']), types)):
        out.append(dict(emplacement(x, y, p['mezzanine'], nu, 'TROU-L1', round(nu / 30) % 12, n), type=ty))
    pris = {(round(s['xm'], 1), round(s['ym'], 1)) for s in out}
    pod = [m for m in interieurs if m[3] <= apo(4) + 1 and (round(m[0], 1), round(m[1], 1)) not in pris]
    Zd4 = (p['pod_niveaux'] - 1) * F
    for n, ((x, y, nu, r, th), ty) in enumerate(zip(choisir_murs(pod, len(types_D4), Zd4), types_D4)):
        out.append(dict(emplacement(x, y, Zd4, nu, 'TROU-D4', round(nu / 30) % 12, n), type=ty))
    ext_h = choisir_murs(exterieurs, n_heavy, 0.0)
    ext_s = choisir_murs([m for m in exterieurs if m not in ext_h], n_tesla, F)
    for n, (x, y, nu, r, th) in enumerate(ext_h):
        out.append(dict(emplacement(x, y, 0.0, nu, 'TROU', round(nu / 30) % 12, n), type='heavy'))
    for n, (x, y, nu, r, th) in enumerate(ext_s):
        out.append(dict(emplacement(x, y, F, nu, 'TROU', round(nu / 30) % 12, n), type='tesla'))
    return out


def ordre_vdc(n):
    """Ordre de van der Corput : 0, 1/2, 1/4, 3/4... -> une pose interrompue reste répartie sur 360°."""
    def vdc(i):
        v, den = 0.0, 1.0
        while i:
            den *= 2
            v += (i % 2) / den
            i //= 2
        return v
    return sorted(range(n), key=lambda i: vdc(i))


def angle(s):
    return math.degrees(math.atan2(s['y'], s['x'])) % 360


def comptee(p, ty):
    """L'emplacement compte-t-il dans le cap des tourelles ? Heavy et Tek toujours ; Tesla et Plant Species X selon le
    serveur (comptées par défaut)."""
    return ty in ('heavy', 'tek') or (ty == 'tesla' and p['tesla_comptee']) or (ty == 'crop' and p['plante_x_comptee'])


def defense(p, contours):
    """Matrice de défense (cap de 100, Tesla et Plant Species X comprises) : 3 plans de tourelles.

    - D8 -> D4 : rive (2 Heavy par côté, niveaux 0 et 1, Tesla au milieu des côtés E0), cage L1 sur D5, tourelles
      reposées sur le bord du trou, Plant X de l'attique. Aucune tourelle sous le niveau des fondations centrales (Z0) ;
    - périmètre du pod : anneau D4 au dernier niveau de la tour, 2 Tesla, Plant X du toit de cage ;
    - dessus : tourelles et Tesla debout, Plant X sur le plancher de toit.
    L1 complète le cap : ses emplacements (60 sur D5) sont pris régulièrement autour du cercle, Tek et Heavy alternées.
    Ordre de pose : rive et bord du trou (Heavy), L1 Tek, Tesla, L1 Heavy, tour, dessus, Plant X ; dans chaque groupe,
    ordre de van der Corput (une pose interrompue reste répartie sur 360°). Deux tourelles sont toujours à
    p['ecart_tourelles'] au moins l'une de l'autre (la tête de l'une ne bloque pas le tir de l'autre)."""
    nH, nT, nS = p['inventaire']
    jupe = geometrie_jupe(p)
    J, J_trou = [], []
    murs = cotes_contour(contours[p['anneau_rive']])
    S = [dict(emplacement(murs[j][0], murs[j][1], F, murs[j][2], 'RIVE', murs[j][3], murs[j][4]), type='tesla')
         for j in murs_tesla(murs, p)]
    if p['rive_heavy']:                      # 2 Heavy par côté : elles voient les paliers de leur côté et la mer
        haut = lambda k: 3 if k % 2 else 1 if k % 4 == 0 else 5          # niveau 1 (la Tesla est au milieu des E0)
        bas = lambda k: (1 if k % 4 == 1 else 5) if k % 2 else (5 if k % 4 == 0 else 1)   # niveau 0, autre colonne
        S += [dict(emplacement(x, y, F, nu, 'RIVE', k, i), type='heavy') for x, y, nu, k, i in murs
              if i == haut(k) and k not in p['tesla_rive_E1']]
        S += [dict(emplacement(x, y, 0.0, nu, 'RIVE', k, i), type='heavy') for x, y, nu, k, i in murs if i == bas(k)]
    S_trou = [s for s in S if dans_trou(p, s['xm'], s['ym'], bord=True)]
    S = [s for s in S if s not in S_trou]
    D4, D4_coupes = emplacements_d4(p, contours)
    DS = emplacements_dessus(p)
    X = cultures(p)
    hors_L1 = J + J_trou + S + S_trou + D4 + DS + X
    n_L1 = p['cap'] - sum(comptee(p, s['type']) for s in hors_L1) - sum(comptee(p, ty) for ty in D4_coupes)
    L1 = choisir(sorted(emplacements_cage(p, contours), key=angle), n_L1)
    for n, s in enumerate(L1):
        s['type'] = 'tek' if n % 2 == 0 else 'heavy'
    L1_trou = [s for s in L1 if dans_trou(p, s['xm'], s['ym'], bord=True)]
    L1 = [s for s in L1 if s not in L1_trou]
    T = emplacements_trou(p, bords_trou(p), len(J_trou) + sum(s['type'] == 'heavy' for s in S_trou),
                          sum(s['type'] == 'tesla' for s in S_trou), [s['type'] for s in L1_trou], D4_coupes,
                          occupes=S + L1 + D4)
    slots = J + S + L1 + D4 + DS + X + T
    tir = [s for s in slots if s['type'] != 'crop']
    ecart = min(math.dist((a['x'], a['y'], a['Z']), (b['x'], b['y'], b['Z'])) for i, a in enumerate(tir) for b in tir[i + 1:])
    assert ecart >= p['ecart_tourelles'] - 20, ecart     # tolérance : coins de la tour (2 côtés à 150°)
    assert all(s['Zb'] >= 0 for s in tir), 'tourelle sous le niveau des fondations centrales'
    for s in slots:
        s.setdefault('plan', 'd4' if s['couche'] in ('D4', 'TROU-D4') else 'ext')
        s['posee'] = True
    besoin = {k: sum(1 for s in slots if s['type'] == k) for k in ('heavy', 'tek', 'tesla', 'crop')}
    assert besoin['heavy'] <= nH and besoin['tek'] <= nT and besoin['tesla'] <= nS, besoin
    par = lambda f: sorted((s for s in slots if f(s)), key=angle)
    groupes = [('P1 rive et bord du trou : Heavy', par(lambda s: s['couche'] in ('RIVE', 'TROU') and s['type'] == 'heavy')),
               ('P2 cage L1 : Tek', par(lambda s: s['couche'] in ('L1', 'TROU-L1') and s['type'] == 'tek')),
               ('P3 Tesla : rive et bord du trou', par(lambda s: s['plan'] == 'ext' and s['type'] == 'tesla')),
               ('P4 cage L1 : Heavy', par(lambda s: s['couche'] in ('L1', 'TROU-L1') and s['type'] == 'heavy')),
               ('P5 tour du pod : anneau D4', par(lambda s: s['plan'] == 'd4' and s['type'] != 'crop')),
               ('P6 dessus : tourelles et Tesla debout', par(lambda s: s['plan'] == 'dessus' and s['type'] != 'crop')),
               ('P7 Plant Species X', par(lambda s: s['type'] == 'crop'))]
    ordre = []
    for nom, g in groupes:
        for i in ordre_vdc(len(g)):
            g[i]['priorite'] = nom
            ordre.append(g[i])
    assert len(ordre) == len(slots) == len({id(s) for s in ordre})
    for n, s in enumerate(ordre, 1):
        s['ordre'] = n
    compte = sum(comptee(p, s['type']) for s in ordre)
    assert compte == p['cap'], (compte, p['cap'])
    poses = {k: sum(1 for s in ordre if s['type'] == k) for k in ('heavy', 'tek', 'tesla', 'crop')}
    reserve = {'heavy': nH - poses['heavy'], 'tek': nT - poses['tek'], 'tesla': nS - poses['tesla']}
    return dict(slots=ordre, ordre=ordre, poses=poses, reserve=reserve, jupe=jupe, n_L1=n_L1 + 0,
                ecart_min=round(ecart, 1))


def zone_chaume(p, s):
    """Plan du mur de chaume d'un emplacement : celui de la zone du mur qu'il remplace. Il y est posé comme gabarit, à
    sa place dans la colonne de murs : ce qui est posé au-dessus tient dès la pose de la zone ; la tourelle se pose
    dessus avec le plan de défense, puis le chaume est démoli."""
    if s['couche'] in ('JUPE-int', 'JUPE-ext', 'RIVE'):
        return 'D8-D7'
    if s['couche'] == 'L1':
        return 'D5-D4'
    if s['couche'] == 'D4':
        return 'pod'
    return groupe_bord(p, rho(s['xm'], s['ym']))      # TROU, TROU-L1, TROU-D4 : murs de bord du trou


def module_tourelles(p, ordre):
    """Les 3 plans de défense : D8 -> D4, périmètre du pod, dessus (groupe de chaque emplacement : s['plan']).
    Tourelles verticales (template 2727) : chaque tourelle se pose sur son mur de chaume de pose (plan de sa zone,
    zone_chaume()), à démolir en jeu ; dessus : tourelles et Tesla debout sur le plancher de toit (pitch 0) ; carrés de
    culture : la graine de Plant Species X est à planter à la main (eau et engrais)."""
    t = Template('Tourelles', 'Tourelles verticales (template 2727) : chaque tourelle est precedee de son mur de chaume '
                              'de pose, a demolir en jeu apres la pose. Ordre des entrees = ordre de pose.')
    ancre(t)
    for s in ordre:
        t.groupe = t.phase = {'ext': 'tourelles_ext', 'd4': 'tourelles_d4', 'dessus': 'tourelles_dessus'}[s['plan']]
        rep = f"#{s['ordre']} {s['couche']} c{s['cote']} p{s['idx']}"
        if s['type'] == 'crop':
            t.add('crop_m' if s['couche'] == 'X-D4' else 'crop', s['x'], s['y'], s['Zb'] + Z_TPL + 10, s['sortie'],
                  Z=s['Zb'],
                  repere=rep + ' (carre de culture : Plant Species X a planter)')
        elif s['couche'] == 'DESSUS':           # debout sur le plancher de toit, sans mur de chaume
            t.add(s['type'], s['x'], s['y'], s['Zb'] + Z_TPL + 10, s['sortie'], Z=s['Zb'], repere=rep)
        else:
            z = s['Zb'] + Z_TPL + F / 2
            t.groupe = t.phase = zone_chaume(p, s)
            t.add('chaume_mur', s['xm'], s['ym'], z, s['sortie'], Z=s['Zb'], repere=rep + ' (chaume a demolir)')
            t.groupe = t.phase = {'ext': 'tourelles_ext', 'd4': 'tourelles_d4'}[s['plan']]
            rot = ROT_TESLA if s['type'] == 'tesla' else ROT_TOURELLE
            t.add(s['type'], s['x'], s['y'], z, s['sortie'] + 90, Z=s['Zb'], repere=rep, **rot)
    return t


def repartir(n, quotas):
    """Diffusion d'erreur : alterne les types le plus régulièrement possible autour du cercle."""
    types = list(quotas)
    fait = {k: 0 for k in types}
    out = []
    for i in range(n):
        k = max(types, key=lambda k: quotas[k] * (i + 1) / n - fait[k])
        out.append(k)
        fait[k] += 1
    return out


def distances(ordre):
    pts = [(s['x'], s['y'], s['Z']) for s in ordre if s['posee']]
    dmax = 0.0
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            dmax = max(dmax, math.dist(pts[i], pts[j]))
    rmax = max(math.hypot(x, y) for x, y, _ in pts)
    return dmax, rmax


# ---------------------------------------------------------------- balistique (coupe radiale, côté E0, θ=0)
def obstacles(p, ob):
    """Surfaces pleines de la coupe. Les rampes inclinées (pente A, overhang, casquette, toit) sont des lames
    espacées de 300 UU : elles ne bloquent ni la vue ni le tir et ne sont donc pas des obstacles."""
    A7 = apo(7)
    Zr = p['rive_niveaux'] * F
    segs = [((0, 0), (A7, 0)),                                     # sol intérieur
            ((A7, 0), (A7, Zr))]                                   # mur de rive
    Zp = 0.0
    for r0, r1, Z in paliers_bord(p):                              # 2 paliers de bord
        segs.append(((r0, Zp), (r0, Z)))
        segs.append(((r0, Z), (r1, Z)))
        Zp = Z
    if p['jupe']:                                                  # mur de jupe, sur le bord D8
        A8, Zp = apo(p['anneaux_total'] // 2 + 1), cote_anneau(p, p['anneaux_total'])
        segs.append(((A8, Zp), (A8, Zp + F)))
    A4, A5 = apo(4), apo(5)
    Zc = p['mezzanine'] + p['cage_niveaux'] * F                     # toit de cage
    Zt = (p['pod_niveaux'] + 1) * F                                # plancher de toit
    segs += [((A5, 0), (A5, Zc)), ((A4, 0), (A4, Zt)), ((0, Zt), (A4, Zt))]   # fût, tour du pod, plancher de toit
    segs += [((A4, Z), (A5, Z)) for Z in (p['mezzanine'], p['mezzanine'] + F, Zc)]   # planchers de galerie
    return segs


def coupe(seg, r0, z0, ang, sens):
    """Intersection du rayon (r0,z0)+t(sens·cos,sin), t>0, avec un segment."""
    (x1, y1), (x2, y2) = seg
    dx, dz = sens * math.cos(ang), math.sin(ang)
    ex, ez = x2 - x1, y2 - y1
    den = dx * ez - dz * ex
    if abs(den) < 1e-12:
        return None
    t = ((x1 - r0) * ez - (y1 - z0) * ex) / den
    u = ((x1 - r0) * dz - (y1 - z0) * dx) / den
    return t if (t > 1 and 0 <= u <= 1) else None


def secteur_tir(p, ob, r0, z0, sens=1):
    """Site minimal et maximal (degrés) des rayons libres depuis (r0, z0), vers l'extérieur (sens=1) ou l'intérieur."""
    segs = obstacles(p, ob)
    libres = [deci / 10 for deci in range(-899, 900)
              if all(coupe(s, r0, z0, math.radians(deci / 10), sens) is None for s in segs)]
    return (min(libres), max(libres)) if libres else None


def bande_vue(p, ob, r0, z0):
    """Parties des 2 paliers de bord vues depuis (r0, z0), palier par palier. La Tesla de rive tire vers le bas, sur
    les paliers : on mesure donc la bande visible et non un secteur."""
    segs = obstacles(p, ob)
    out = []
    for r_in, r_out, zb in paliers_bord(p):
        sol = ((r_in, zb), (r_out, zb))
        vus = []
        for i in range(201):
            r = r_in + (r_out - r_in) * i / 200
            dist = math.hypot(r - r0, zb - z0)
            sens = 1 if r >= r0 else -1
            a = math.atan2(zb - z0, abs(r - r0))
            if all((t := coupe(s, r0, z0, a, sens)) is None or t >= dist - 1 for s in segs if s != sol):
                vus.append(r)
        out.append((round(min(vus), 1), round(max(vus), 1), zb) if vus else None)
    return out


def secteurs(p, ob, jupe):
    A4, A5, A7 = apo(4), apo(5), apo(7)
    Zt = (p['pod_niveaux'] + 1) * F
    out = {'L1': secteur_tir(p, ob, A5 + DECALAGE_MONTAGE + SAILLIE_TETE, p['mezzanine'] + F / 2),
           'RIVE': bande_vue(p, ob, A7 + DECALAGE_MONTAGE + SAILLIE_TETE / 2, F * 1.5),
           'RIVE-H0': secteur_tir(p, ob, A7 + DECALAGE_MONTAGE + SAILLIE_TETE, F / 2),
           'RIVE-H1': secteur_tir(p, ob, A7 + DECALAGE_MONTAGE + SAILLIE_TETE, F * 1.5),
           'D4': secteur_tir(p, ob, A4 + DECALAGE_MONTAGE + SAILLIE_TETE, (p['pod_niveaux'] - 0.5) * F),
           'DESSUS': secteur_tir(p, ob, p['dessus_apotheme'], Zt + 100)}
    return out


# ---------------------------------------------------------------- couverture : chaque angle d'approche est-il couvert ?
# Points cibles : un tous les 10° autour de la base, à la distance et à la cote de chaque zone d'approche.
# Les points d'une zone posée sur la base (sur_base) qui tombent au-dessus du trou ne comptent pas.
ZONES = [('sous la plateforme (piton)', 3000.0, -1500.0, False), ('mer, pied du piton', 6500.0, -1500.0, False),
         ('paliers et ligne de pics', 4300.0, -150.0, True), ('attique, sous la pente A', 3300.0, 150.0, True),
         ('pente A et overhang', 3700.0, 1000.0, True), ('toit de cage, poche D4-D5', 2550.0, 2550.0, True),
         ('toit du pod', 1300.0, 4200.0, True), ('ciel au-dessus de la base', 2000.0, 7500.0, False),
         ('approche à 7 000 UU', 7000.0, 2000.0, False)]


def _traverse(P0, P1, obst):
    """Le segment P0 -> P1 traverse-t-il un obstacle (disque ou anneau horizontal, cylindre vertical) ?"""
    x0, y0, z0 = P0
    dx, dy, dz = P1[0] - x0, P1[1] - y0, P1[2] - z0
    for o in obst:
        if o[0] == 'disque':
            _, z, r0, r1 = o
            if abs(dz) > 1e-9:
                s = (z - z0) / dz
                if 1e-3 < s < 1 - 1e-3 and r0 <= math.hypot(x0 + s * dx, y0 + s * dy) <= r1:
                    return True
        else:
            _, R, za, zb = o
            a, b, c = dx * dx + dy * dy, 2 * (x0 * dx + y0 * dy), x0 * x0 + y0 * y0 - R * R
            if a < 1e-9 or b * b - 4 * a * c < 0:
                continue
            for s in ((-b - math.sqrt(b * b - 4 * a * c)) / (2 * a), (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a)):
                if 1e-3 < s < 1 - 1e-3 and za <= z0 + s * dz <= zb:
                    return True
    return False


def couverture(p, ordre):
    """Nombre de tourelles (Heavy et Tek) qui voient chaque point cible des ZONES, en réglage Medium et High.

    Modèle : murs et planchers pleins approchés par des cylindres et des anneaux (dodécagones pris à leur apothème),
    cadres doubles comptés pleins, lames de rampes transparentes ; une tourelle verticale tire dans le demi-espace
    devant son mur, une tourelle debout dans toutes les directions ; tête 110 UU devant le mur, à mi-hauteur.
    Les Tesla et les Plant X, à courte portée, ne sont pas comptées. Renvoie {zone: {'min', 'moyenne', 'faibles'}}."""
    A4, A5, A7, A8 = apo(4), apo(5), apo(7), apo(8)
    Zc = p['mezzanine'] + p['cage_niveaux'] * F
    Zt = (p['pod_niveaux'] + 1) * F
    paliers = paliers_bord(p)
    obst = [('disque', 0.0, 0.0, A7), ('disque', -600.0, 0.0, A8),            # sol, dessous de la plateforme
            ('disque', p['mezzanine'], 0.0, A5), ('disque', p['mezzanine'] + F, A4, A5), ('disque', Zc, A4, A5),
            ('disque', Zt, 0.0, A4), ('cyl', A7, 0.0, p['rive_niveaux'] * F), ('cyl', A5, 0.0, Zc),
            ('cyl', A4, 0.0, Zt)] + [('disque', Z, r0, r1) for r0, r1, Z in paliers]
    if p['jupe']:
        obst.append(('cyl', A8, cote_anneau(p, p['anneaux_total']), 0.0))
    tetes = []
    for s in ordre:
        if s['type'] not in ('heavy', 'tek'):
            continue
        n = vec(s['sortie'])
        if s['couche'] == 'DESSUS':
            tetes.append(((s['x'], s['y'], s['Zb'] + 100), None))
        else:
            d = DECALAGE_MONTAGE + SAILLIE_TETE
            tetes.append(((s['xm'] + d * n[0], s['ym'] + d * n[1], s['Zb'] + F / 2), n))
    out = {}
    for nom, R, Z, sur_base in ZONES:
        comptes = {}
        for th in range(0, 360, 10):
            cible = (R * vec(th)[0], R * vec(th)[1], Z)
            if sur_base and dans_trou(p, cible[0], cible[1]):
                continue
            vus = [0, 0]
            for T, n in tetes:
                d = (cible[0] - T[0], cible[1] - T[1], cible[2] - T[2])
                L = math.sqrt(_scal(d, d))
                if n and d[0] * n[0] + d[1] * n[1] <= 0.02 * L:
                    continue                      # derrière son mur
                if L > p['portee_tir'][1] or _traverse(T, cible, obst):
                    continue
                vus[1] += 1
                vus[0] += L <= p['portee_tir'][0]
            comptes[th] = vus
        out[nom] = dict(rayon=R, Z=Z, min_medium=min(v[0] for v in comptes.values()),
                        min_high=min(v[1] for v in comptes.values()),
                        moyenne_high=round(sum(v[1] for v in comptes.values()) / len(comptes), 1),
                        faibles_high=[th for th, v in comptes.items() if v[1] < 2], par_angle=comptes)
    return out


# ---------------------------------------------------------------- découpage en plans (anneaux extérieurs / centre)
REFERENCE = {'pile': "Pilier de reference : pile d'ancrage en (0 ; 300)",
             'A': "Mur de reference A : le mur de D4 du cote θ 90° au-dessus de la porte du hall (x = +150), a snapper "
                  "sur le haut du mur de pod",
             'B': "Mur de reference B : le mur de D4 du cote θ 90° a droite du mur A vu de l'exterieur (x = -150), a "
                  "snapper sur le haut du mur de pod",
             'C': "Mur de reference C : le mur de D4 du cote θ 90° a droite du mur B vu de l'exterieur (x = -450), a "
                  "snapper sur le haut du mur de pod"}
PLANS = [
    ('sol', 'Plan_01_sol_complet', 'Sol complet : toutes les fondations, paliers de bord et plateforme verte compris, '
     "sans le trou ; pile d'ancrage", 'pile'),
    ('colonnade', 'Plan_02_colonnade_option', 'Option : colonnade circulaire sous la pente A (les poteaux de stabilite '
     'de la pente A la remplacent)', 'pile'),
    ('D8-D7', 'Plan_03_bord_D8-D7', 'Bord D8 -> D7 : mur de rive et mur de jupe en cadres doubles, overhang et debord '
     'en rampes, poteaux et poutres fines', 'pile'),
    ('D7-D5', 'Plan_04_D7-D5_pente_A', 'D7 -> D5 : pente A en rampes et ses poteaux de stabilite (remplacent la '
     'colonnade), murs de bord du trou en cadres doubles', 'pile'),
    ('pod', 'Plan_05_tour_du_pod_D4', 'Tour du pod D4 en murs pleins (portes en cadres doubles) jusqu\'a Z2700, murs de '
     'bord du trou du pod, piliers PA et PB, escaliers, mezzanine Z1800', 'pile'),
    ('D5-D4', 'Plan_06_D5-D4_cage_et_appentis', 'D5 -> D4 : fut, L1 et L2 en cadres doubles, galeries Z1800/2100/2400, '
     'casquette, appentis en rampes vers la tour et ses poteaux, bord du trou du couloir', 'pile'),
    ('tourelles_ext', 'Plan_07_tourelles_D8-D4', 'Defense D8 -> D4 : Heavy de jupe, Tesla de rive, Tek et Heavy de la '
     "cage L1, tourelles du bord du trou, carres de culture (Plant X) de l'attique ; murs de chaume a demolir", 'pile'),
    ('tourelles_d4', 'Plan_08_tourelles_perimetre_pod', 'Defense du perimetre du pod : anneau de Tek et Heavy sur la '
     'tour (Z2400), 2 Tesla, carres de culture (Plant X) du toit de cage ; murs de chaume a demolir', 'pile'),
    ('toiture_pleine', 'Plan_09_toiture_pleine_D4-centre', 'Toiture pleine D4 -> centre : couronne de murs pleins, '
     'piliers PA et PB, plancher de toit (toit plat ferme, avec une trappe) ; a poser sur le haut de la tour, a toute '
     'hauteur', 'A'),
    ('toit_rampe', 'Plan_10_toit_en_rampes_D4-centre', 'Toit en rampes D4 -> centre : rampes inclinees et leurs poteaux '
     'de piliers fins sous les jonctions de lames, casquette du trou ; se pose sur la toiture pleine', 'C'),
    ('tourelles_dessus', 'Plan_11_tourelles_dessus', 'Defense du dessus : Heavy, Tek et Tesla debout, carres de culture '
     '(Plant X) sur le plancher de toit ; se pose sur la toiture pleine', 'B'),
]


def assembler_plans(p, modules):
    """Répartit les entrées des modules dans les plans (groupe de chaque entrée). Les plans calés sur la pile d'ancrage
    portent 1 demi-pilier qui se pose dessus (le plan 1 : la pile de 2 demi-piliers) ; ceux du haut de la tour portent
    leur mur de référence (REF_MURS) en tête. L'ordre de pose est fixé ensuite (ordonner_plans)."""
    plans = {}
    for n, (cle, fichier, desc, ref) in enumerate(PLANS):
        t = Template(fichier.replace('_', ' '), f'{desc}. {REFERENCE[ref]}.')
        if ref == 'pile':
            ancre(t, empilee=(n == 0))
        plans[cle] = t
    for _, m in modules:
        for e, gr, ligne, meta in zip(m.entries, m.groupes, m.lignes, m.metas):
            if ligne[5].startswith('ancre'):    # ancres des modules
                continue
            t = plans[gr]
            t.entries.append(e)
            t.lignes.append(ligne)
            t.phases.append(gr)
            t.groupes.append(gr)
            t.metas.append(meta)
    for cle, *_, ref in PLANS:
        if ref != 'pile':
            assert sum(l_[5].startswith(f'reference {ref} ') for l_ in plans[cle].lignes) == 1, (cle, ref)
    return plans


def portee_plafonds(P, par):
    """Plafonds de P et, pour chacun, le nombre de cases jusqu'à un appui relié au sol (absent : aucun) : une fondation,
    ou une colonne de murs, de cadres ou de piliers qui descend sans interruption jusqu'à une fondation (le chaume coupe
    la colonne ; la plateforme verte ne compte pas)."""
    au_sol = {i: not plateforme(P[i][7]) for i in range(len(P)) if P[i][2] in ('fond', 'fond_tri')}
    colonnes = sorted((i for i in range(len(P)) if P[i][2] in ('mur', 'cadre_double', 'escalier') + PILIERS),
                      key=lambda i: P[i][5])
    change = True
    while change:
        change = False
        for i in colonnes:
            if not au_sol.get(i) and any(au_sol.get(j) and P[j][2] in ('fond', 'fond_tri', 'mur', 'cadre_double')
                                         + PILIERS for j in par[i]):
                au_sol[i] = change = True
    plaf = [i for i in range(len(P)) if P[i][2] in ('plafond', 'plafond_tri', 'trappe')]
    k5 = lambda *v: tuple(round(c / 5) for c in v)
    aretes = {}
    for i in plaf:
        cle, x, y, z, yaw = P[i][2:7]
        poly = polygone(dict(type='tri' if cle.endswith('_tri') else 'carre', x=x, y=y, yaw=yaw))
        for m in range(len(poly)):
            (x1, y1), (x2, y2) = poly[m], poly[(m + 1) % len(poly)]
            aretes.setdefault(k5((x1 + x2) / 2, (y1 + y2) / 2, z), set()).add(i)
    dist = {i: 0 for i in plaf if any(au_sol.get(j) for j in par[i])}
    file = list(dist)
    while file:
        i = file.pop(0)
        cle, x, y, z, yaw = P[i][2:7]
        poly = polygone(dict(type='tri' if cle.endswith('_tri') else 'carre', x=x, y=y, yaw=yaw))
        for m in range(len(poly)):
            (x1, y1), (x2, y2) = poly[m], poly[(m + 1) % len(poly)]
            for j in aretes[k5((x1 + x2) / 2, (y1 + y2) / 2, z)]:
                if j not in dist:
                    dist[j] = dist[i] + 1
                    file.append(j)
    return plaf, dist


def verifier_limites(p, plans, n_pics, n_equipements):
    """Limites du moteur et règles d'ancrage :
    - structures : bâti (plans, colonnade comprise, tourelles, carrés de culture, pics, équipements)
      ≤ p['plafond_structures'] (10 500 − 20 % de réserve), y compris au pic du chantier (murs de chaume et pile
      d'ancrage pas encore démolis) ;
    - tourelles comptées par le cap (Heavy, Tek ; Tesla si tesla_comptee ; Plant Species X si plante_x_comptee)
      = p['cap'] exactement ;
    - hauteur ≤ p['hauteur_max_murs'] murs au-dessus du sol ;
    - aucun plafond à plus de p['portee_plafond_max'] cases d'un appui relié au sol : une fondation, ou une colonne de
      murs, de cadres ou de piliers qui descend sans interruption jusqu'à une fondation (le chaume, démoli, coupe la
      colonne ; la plateforme verte ne compte pas). Contrôle sur la base finie (tous les plans posés)."""
    P = [q for q in _pieces_plans(plans) if not q[7].startswith('ancre')]
    par, _ = porteurs(P)
    plaf, dist = portee_plafonds(P, par)
    portee = max(dist.get(i, 99) for i in plaf)
    loin = [P[i][7] for i in plaf if dist.get(i, 99) > p['portee_plafond_max']]
    assert not loin, (len(loin), loin[:5])
    n = {}
    for q in P:
        n[q[2]] = n.get(q[2], 0) + 1
    tourelles = sum(n.get(k, 0) for k in ('heavy', 'tek', 'tesla'))
    plantes = n.get('crop', 0) + n.get('crop_m', 0)
    temporaires = n.get('chaume_mur', 0) + sum(1 for t in plans.values() for l_ in t.lignes if l_[5].startswith('ancre'))
    bati = len(P) - n.get('chaume_mur', 0) + n_pics + n_equipements
    pic = bati + temporaires
    comptees = (sum(n.get(k, 0) for k in ('heavy', 'tek')) + (n.get('tesla', 0) if p['tesla_comptee'] else 0)
                + (plantes if p['plante_x_comptee'] else 0))
    zmax = max(q[5] - Z_TPL + (100 if q[2] == 'rampe' else HAUT_PILIER.get(q[2], F) / 2) for q in P)
    assert pic <= p['plafond_structures'], pic
    assert comptees == p['cap'], comptees
    assert zmax <= p['hauteur_max_murs'] * F, zmax
    out = dict(structures_bati=bati, dont_tourelles=tourelles, dont_carres_plante_x=plantes, structures_pic_chantier=pic,
               plafond=p['plafond_structures'], marge=p['plafond_structures'] - bati, tourelles_comptees=comptees,
               tesla_non_comptees=0 if p['tesla_comptee'] else n.get('tesla', 0), hauteur_max_Z=zmax,
               hauteur_max_murs=zmax / F, portee_plafond_max_cases=portee,
               plafonds_par_portee={d: sum(1 for i in plaf if dist[i] == d) for d in sorted(set(dist.values()))})
    print(f"  Limites : {bati} structures de bâti ({pic} au pic du chantier) pour un plafond de {p['plafond_structures']}, "
          f"{comptees} tourelles comptées par le cap (dont {n.get('tesla', 0) if p['tesla_comptee'] else 0} Tesla et "
          f"{plantes} Plant X ; {out['tesla_non_comptees']} Tesla hors cap), hauteur {zmax / F:.0f} murs, "
          f"plafonds à {portee} cases au plus d'un appui au sol")
    return out


def secteur_test(plans, th0=-15.0, th1=45.0, portee_max=2):
    """Template d'essai en solo : toutes les pièces dont le pivot est entre θ0 et θ1 (2 côtés et l'arête θ 15°, hors
    du trou), dans l'ordre de pose des plans (chaque pièce après ses porteurs). On y retrouve chaque sorte de pièce et
    d'appui : rive, colonnade, pente A, overhang et poteaux sur les paliers, jupe, débord, cage, tourelles et murs de
    chaume, toit et ses poteaux.
    Le secteur est autonome : une pièce dont les porteurs sont hors du secteur, ou un plafond à plus de portee_max
    cases d'un appui relié au sol dans le secteur, est retirée (de proche en proche), pour qu'aucune pièce du template
    ne soit refusée faute d'appui. Renvoie (template, nombre de pièces retirées)."""
    t = Template(f'Secteur test θ{th0:.0f}-{th1:.0f}', 'Essai en solo : un secteur de 60 degres de la forteresse, '
                 "dans l'ordre de pose. Pilier de reference : pile d'ancrage en (0 ; 300).")
    ancre(t, empilee=True)
    P, ordre, par = ordre_de_pose(plans)
    src = {(cle, n): (e, l_) for cle, tt in plans.items() for n, (e, l_) in enumerate(zip(tt.entries, tt.lignes))}
    sel = [i for i in ordre if th0 - 0.01 <= math.degrees(math.atan2(P[i][4], P[i][3])) <= th1 + 0.01]  # coins compris
    n0 = len(sel)
    while True:                                  # pièces portées dans le secteur seulement
        Q = [P[i] for i in sel]
        par_q, sans_q = porteurs(Q)
        plaf, dist = portee_plafonds(Q, par_q)
        retirer = set(sans_q) | {k for k in plaf if dist.get(k, 99) > portee_max}
        if not retirer:
            break
        sel = [i for k, i in enumerate(sel) if k not in retirer]
    for i in sel:
        e, l_ = src[(P[i][0], P[i][1])]
        t.entries.append(e)
        t.lignes.append(l_)
        t.phases.append(P[i][0])                 # plan d'origine
        t.groupes.append(None)
        t.metas.append(None)
    return t, n0 - len(sel)


def essai_rampes():
    """Template d'essai court (en solo, sur un sol plat) : comment une ligne de rampes inclinées se pose sur un mur.

    4 variantes côte à côte, chacune sur 4 fondations, devant un mur de 2 cadres doubles sur 2 niveaux (Z0 -> 600) ;
    chaque ligne monte vers +x depuis le joint des cadres (Z600), une lame pend vers l'extérieur :
    - V0 : copie du départ de la tour 1809 : pilier fin dans le joint, poutre fine sous la 1re lame ;
    - V1 : départ du générateur : pilier fin dans le joint, poteau de piliers fins sous la jonction 1 ;
    - V2 : poteau de piliers fins posé librement sur une fondation (40 UU d'une arête, comme les poteaux de la pente A),
      une lame qui pend de sa tête et une qui monte ;
    - V3 : ancien départ, posé directement sur le haut des cadres (sans pilier fin), poteau sous la jonction 1.
    Renvoie (template, [(n° d'entrée, variante, pièce, repère)])."""
    t = Template('Essai rampes : depart des lignes', 'Essai en solo sur sol plat : V0 copie de la tour 1809, '
                 'V1 depart du generateur (pilier fin dans le joint), V2 poteau libre sur fondation, V3 ancien depart '
                 'sans pilier fin. Noter les rampes qui se posent.')
    legende = []

    def add(var, cle, x, y, z, yaw, rep_):
        legende.append((len(t.entries), var, NOMS[cle], rep_))
        t.add(cle, x, y, z, yaw, repere=f'{var} {rep_}')

    for var, yc in (('V0', 0.0), ('V1', 900.0), ('V2', 1800.0), ('V3', 2700.0)):
        x0 = 0.0
        for dx in (150, 450):
            for dy in (-150, 150):
                add(var, 'fond', x0 + dx, yc + dy, 40, 0, 'fondation')
        if var == 'V2':
            xp = x0 + 340                       # 40 UU après l'arête x0 + 300 : pas un point de snap
            for niv in range(2):
                add(var, 'pilier_fin', xp, yc, niv * F + 240, 0, f'poteau libre, niveau {niv}')
            add(var, 'rampe', xp - F / 2, yc, F + 290, 90, 'lame pendue a la tete du poteau')
            add(var, 'rampe', xp + F / 2, yc, 2 * F + 290, 90, 'lame montante sur la tete du poteau')
            continue
        for dy in (-150, 150):
            add(var, 'cadre_double', x0, yc + dy, 240, 180, 'cadre niveau 0')
        if var in ('V0', 'V1'):
            add(var, 'pilier_fin', x0, yc, 540, 180, 'pilier fin dans le joint, niveau 1 (avant les cadres)')
        for dy in (-150, 150):
            add(var, 'cadre_double', x0, yc + dy, 540, 180, 'cadre niveau 1')
        if var == 'V0':
            add(var, 'poutre_fine', x0 + F / 2, yc, 2 * F + 90, -90, 'poutre fine sous la 1re lame (tour 1809)')
        else:
            for niv in range(3):
                add(var, 'pilier_fin', x0 + F, yc, niv * F + 240, 0, f'poteau sous la jonction 1, niveau {niv}')
        add(var, 'rampe', x0 - F / 2, yc, F + 290, 90, 'lame pendue vers l exterieur')
        add(var, 'rampe', x0 + F / 2, yc, 2 * F + 290, 90, 'lame r0 (depart du joint)')
        add(var, 'rampe', x0 + 3 * F / 2, yc, 3 * F + 290, 90, 'lame r1')
    return t, legende


def essai_rampes_2():
    """2e essai court (en solo, sur sol plat), après le 1er : V1 et V3 se posent (poteau de piliers fins sur un coin de
    fondation sous la jonction 1), V0 (pilier fin dans le joint + poutre fine, sans poteau) et V2 (poteau hors d'un
    point de snap) ne se posent pas. Chaque cas est isolé, sur 4 fondations ; en regardant vers le haut des rampes,
    de gauche à droite (vers +y) :
    E1 pilier fin dans le joint du mur (tête au haut du mur), 1 lame montante ;
    E2 pilier fin dans le joint, 1 lame pendante vers l'extérieur ;
    E3 pilier fin debout SUR le haut du mur au joint (tour 1201), 1 lame pendante et 1 montante depuis sa tête ;
    E4 haut du mur seul (joint, sans pilier), 1 lame montante ;
    E5 poteau (1 pilier fin) sur un coin de fondation, 1 lame montante depuis sa tête ;
    E6 poteau (2 piliers fins) sur un coin de fondation, 1 lame pendue à sa tête ;
    E7 poteau (2 piliers fins) au milieu d'une arête de fondation, 1 lame montante ;
    E8 poteau (2 piliers fins) au centre d'une fondation, 1 lame montante ;
    E9 poteau (2 piliers fins) à 40 UU d'une arête, sans lame (le poteau seul se pose-t-il ?).
    Repère : au coin arrière gauche de chaque cas, une pile de n demi-piliers métal (n = numéro du cas).
    Renvoie (template, [(n° d'entrée, cas, pièce, repère)])."""
    t = Template('Essai rampes 2 : appuis des lames', 'Essai en solo sur sol plat, 9 cas E1 a E9 de gauche a droite en '
                 'regardant vers le haut des rampes ; pile de n demi-piliers = cas n. Noter ce qui se pose.')
    legende = []

    def add(cas, cle, x, y, z, yaw, rep_):
        legende.append((len(t.entries), cas, NOMS[cle], rep_))
        t.add(cle, x, y, z, yaw, repere=f'{cas} {rep_}')

    x0 = 0.0
    for n in range(1, 10):
        cas, yc = f'E{n}', (n - 1) * 900.0
        for dx in (150, 450):
            for dy in (-150, 150):
                add(cas, 'fond', x0 + dx, yc + dy, 40, 0, 'fondation')
        for k in range(n):
            add(cas, 'demi_pilier', x0 + 2 * F, yc - F, 165 + k * F / 2, 0, f'repere : demi-pilier {k + 1}/{n}')
        if n <= 4:                              # mur de 2 cadres doubles sur 2 niveaux, joint en (x0, yc)
            for dy in (-150, 150):
                add(cas, 'cadre_double', x0, yc + dy, 240, 180, 'cadre niveau 0')
            if n in (1, 2):
                add(cas, 'pilier_fin', x0, yc, 540, 180, 'pilier fin dans le joint, niveau 1 (avant les cadres)')
            for dy in (-150, 150):
                add(cas, 'cadre_double', x0, yc + dy, 540, 180, 'cadre niveau 1')
            if n == 1 or n == 4:
                add(cas, 'rampe', x0 + F / 2, yc, 2 * F + 290, 90, 'lame montante depuis le joint (Z600 -> 900)')
            elif n == 2:
                add(cas, 'rampe', x0 - F / 2, yc, F + 290, 90, 'lame pendante vers l exterieur (Z300 -> 600)')
            else:
                add(cas, 'pilier_fin', x0, yc, 840, 90, 'pilier fin debout sur le haut du mur au joint (Z600 -> 900)')
                add(cas, 'rampe', x0 - F / 2, yc, 2 * F + 290, 90, 'lame pendue a la tete (Z600 -> 900)')
                add(cas, 'rampe', x0 + F / 2, yc, 3 * F + 290, 90, 'lame montante depuis la tete (Z900 -> 1200)')
            continue
        xp, yp, haut = {5: (x0 + F, yc, 1), 6: (x0 + F, yc, 2), 7: (x0 + F, yc + F / 2, 2), 8: (x0 + F / 2, yc + F / 2, 2),
                        9: (x0 + F + 40, yc, 2)}[n]
        lieu = {5: 'coin de fondation', 6: 'coin de fondation', 7: "milieu d'une arete", 8: 'centre de fondation',
                9: '40 UU d une arete'}[n]
        for niv in range(haut):
            add(cas, 'pilier_fin', xp, yp, niv * F + 240, 0, f'poteau ({lieu}), niveau {niv}')
        zt = haut * F                           # tête du poteau
        if n == 6:
            add(cas, 'rampe', xp - F / 2, yp, zt - F + 290, 90, f'lame pendue a la tete (Z{zt - F:.0f} -> {zt:.0f})')
        elif n != 9:
            add(cas, 'rampe', xp + F / 2, yp, zt + 290, 90, f'lame montante depuis la tete (Z{zt:.0f} -> {zt + F:.0f})')
    return t, legende


def essai_rampes_3():
    """3e essai court (en solo, sur sol plat), compact (3 rangées de 3) pour ne pas buter sur le relief. Acquis des 2
    premiers : une lame tient à la tête d'un poteau de piliers fins debout sur un COIN de fondation (V1, V3, E5) ; ni le
    haut d'un mur, ni un pilier fin dans le joint posé sur le mur du dessous, ni un pilier fin debout sur le haut du
    mur ne la tiennent (V0, E1 à E4). Chaque cas sur 4 fondations ; pile de n demi-piliers = cas n. En regardant vers
    le haut des rampes : rangée proche G1 G2 G3, rangée du milieu G4 G5 G6, rangée du fond G7 G8 G9 (de gauche à
    droite) :
    G1 poteau de 4 piliers fins sur un coin de fondation, 3 lames pendues à la suite (vers l'extérieur) ;
    G2 poteau d'1 pilier fin + 1 demi-pilier fin (tête à Z450) sur un coin, 1 lame montante ;
    G3 poteau de 2 piliers fins sur la pointe d'une fondation triangle, 1 lame montante ;
    G4 poteau d'1 pilier fin sur un coin de PLAFOND (Z300, sans pilier dessous), 1 lame montante ;
    G5 colonne de 2 piliers fins dans le joint d'un mur, depuis la fondation, posée avant les cadres ; 1 lame montante
       et 1 pendante ;
    G6 poteau de 2 piliers fins au milieu d'une arête de fondation, 1 lame montante ;
    G7 poteau de 2 piliers fins au centre d'une fondation, 1 lame montante ;
    G8 poteau de 2 piliers fins sur un coin, 1 lame pendue à sa tête ;
    G9 1 lame montante posée sur le bord d'un plafond (Z300), sans poteau.
    Renvoie (template, [(n° d'entrée, cas, pièce, repère)])."""
    t = Template('Essai rampes 3 : appuis des lames', 'Essai en solo sur sol plat, 3 rangees de 3 cas (G1-G3 devant, '
                 'G7-G9 au fond, de gauche a droite en regardant vers le haut des rampes) ; pile de n demi-piliers = cas '
                 'n. Noter ce qui se pose.')
    legende = []

    def add(cas, cle, x, y, z, yaw, rep_):
        legende.append((len(t.entries), cas, NOMS[cle], rep_))
        t.add(cle, x, y, z, yaw, repere=f'{cas} {rep_}')

    def poteau(cas, x, y, n, lieu, z0=0.0, demi=False):
        for niv in range(n):
            add(cas, 'pilier_fin', x, y, z0 + niv * F + 240, 0, f'poteau ({lieu}), pilier fin {niv + 1}/{n}')
        if demi:
            add(cas, 'demi_pilier_fin', x, y, z0 + n * F + 165, 0, f'poteau ({lieu}), demi-pilier fin')
        return z0 + n * F + (F / 2 if demi else 0)            # cote de la tête

    def lame(cas, x_bas, y, Zb, rep_):                          # lame qui monte vers +x depuis (x_bas, Zb)
        add(cas, 'rampe', x_bas + F / 2, y, Zb + 290, 90, f'{rep_} (Z{Zb:.0f} -> {Zb + F:.0f})')

    def plafonds(cas, x0, yc):                                  # 2 plafonds Z300 sur 4 piliers, milieu sans pilier
        for dx in (0, 2 * F):
            for dy in (0, F):
                add(cas, 'pilier', x0 + dx, yc + dy, 240, 0, 'pilier sous les plafonds')
        for dx in (F / 2, 3 * F / 2):
            add(cas, 'plafond', x0 + dx, yc + F / 2, F + Z_TPL, 0, 'plafond Z300')

    for n in range(1, 10):
        cas = f'G{n}'
        x0, yc = ((n - 1) // 3) * 1500.0, ((n - 1) % 3) * 900.0
        for dx in (150, 450):
            for dy in (-150, 150):
                add(cas, 'fond', x0 + dx, yc + dy, 40, 0, 'fondation')
        for k in range(n):
            add(cas, 'demi_pilier', x0 + 2 * F, yc - F, 165 + k * F / 2, 0, f'repere : demi-pilier {k + 1}/{n}')
        if n == 1:
            zt = poteau(cas, x0, yc, 4, 'coin de fondation')
            for j in range(1, 4):
                lame(cas, x0 - j * F, yc, zt - j * F, f'lame pendue n{j}')
        elif n == 2:
            zt = poteau(cas, x0 + F, yc, 1, 'coin de fondation', demi=True)
            lame(cas, x0 + F, yc, zt, 'lame montante depuis la tete')
        elif n == 3:
            add(cas, 'fond_tri', x0 + 2 * F + H / 2, yc + F / 2, 40, 0, 'fondation triangle sur une arete, pointe vers +x')
            zt = poteau(cas, x0 + 2 * F + H, yc + F / 2, 2, 'pointe du triangle')
            lame(cas, x0 + 2 * F + H, yc + F / 2, zt, 'lame montante depuis la tete')
        elif n == 4:
            plafonds(cas, x0, yc)
            zt = poteau(cas, x0 + F, yc, 1, 'coin de plafond', z0=F)
            lame(cas, x0 + F, yc, zt, 'lame montante depuis la tete')
        elif n == 5:
            for niv in range(2):
                add(cas, 'pilier_fin', x0, yc, niv * F + 240, 180, f'colonne dans le joint, pilier fin {niv + 1}/2')
                for dy in (-150, 150):
                    add(cas, 'cadre_double', x0, yc + dy, niv * F + 240, 180, f'cadre niveau {niv}')
            lame(cas, x0, yc, 2 * F, 'lame montante depuis la tete de la colonne')
            lame(cas, x0 - F, yc, F, 'lame pendante vers l exterieur')
        elif n in (6, 7):
            xp, yp, lieu = (x0 + F, yc + F / 2, "milieu d'une arete") if n == 6 else (x0 + F / 2, yc + F / 2,
                                                                                     'centre de fondation')
            zt = poteau(cas, xp, yp, 2, lieu)
            lame(cas, xp, yp, zt, 'lame montante depuis la tete')
        elif n == 8:
            zt = poteau(cas, x0 + F, yc, 2, 'coin de fondation')
            lame(cas, x0, yc, zt - F, 'lame pendue a la tete')
        else:
            plafonds(cas, x0, yc)
            lame(cas, x0 + 2 * F, yc + F / 2, F, 'lame montante posee sur le bord du plafond')
    return t, legende


# ---------------------------------------------------------------- ordre de pose : plan après plan, du bas vers le haut
TAILLE_MAX = 2000              # entrées par template (limite de Template Hammer constatée en jeu)
MURS = ('mur', 'cadre_double', 'chaume_mur')
PILIERS = ('pilier', 'demi_pilier', 'pilier_fin', 'demi_pilier_fin')
SOLS = ('fond', 'fond_tri', 'plafond', 'plafond_tri', 'trappe')
HAUT_PILIER = {'pilier': F, 'demi_pilier': F / 2, 'pilier_fin': F, 'demi_pilier_fin': F / 2}


def porteurs(P, rang=None):
    """Pour chaque pièce posée, les pièces qui la portent (ce sur quoi elle se snappe), d'après la géométrie :
    - fondation : le sol ;
    - mur, cadre, chaume : le mur du dessous ou l'arête d'un plancher à sa base ; à défaut il pend sous le mur du
      dessus (jupe) ;
    - pilier, escalier : la pièce du dessous, ou le plancher sous son pied ;
    - plafond : un mur ou un pilier sous une arête ou un coin ; à défaut, le plafond voisin déjà porté ;
    - rampe : la tête de pilier ou le bout de poutre sous l'un de ses bouts (jamais un haut de mur : en jeu, la lame
      ne s'y pose pas) ; à défaut, la lame voisine de sa ligne déjà portée ;
    - poutre fine : le mur dont le haut est sous son bout intérieur ; tourelle : son mur de chaume ; tourelle debout,
      carré de culture : le plancher dessous.
    rang : rang de pose du plan de chaque pièce ({plan: rang}) ; un porteur d'un plan posé plus tard n'est pas retenu
    (la pièce est alors portée de proche en proche par un voisin déjà posé).
    Renvoie (liste des porteurs par pièce, pièces sans porteur)."""
    k5 = lambda *v: tuple(round(c / 5) for c in v)
    n = len(P)
    par = [[] for _ in range(n)]
    R = [0] * n if rang is None else [rang[q[0]] for q in P]
    ok = lambda i, js: [j for j in js if R[j] <= R[i]]
    mur_a, pil_a, esc_a = {}, {}, {}            # (x, y, z bas) -> pièce
    aretes, coins, sommets_mur = {}, {}, {}      # (milieu ou coin, z du dessus) -> pièces
    segs = []                                    # hauts de mur et bords de plancher : (x1, y1, x2, y2, z, pièce)
    tetes = []                                   # têtes de pilier et bouts de poutre : (x, y, z, pièce)
    polys = []
    for i, (pl, nn, cle, x, y, z, yaw, rep_) in enumerate(P):
        if cle in MURS:
            mur_a[k5(x, y, z - F / 2)] = i
            if cle != 'chaume_mur':
                lx, ly = vec(yaw + 90)
                segs.append((x - F / 2 * lx, y - F / 2 * ly, x + F / 2 * lx, y + F / 2 * ly, z + F / 2, i))
                aretes.setdefault(k5(x, y, z + F / 2), []).append(i)
                for sg in (-1, 1):
                    sommets_mur.setdefault(k5(x + sg * F / 2 * lx, y + sg * F / 2 * ly, z + F / 2), []).append(i)
        elif cle in PILIERS:
            hp = HAUT_PILIER[cle]
            pil_a[k5(x, y, z - hp / 2)] = i
            if not rep_.startswith('ancre'):
                tetes.append((x, y, z + hp / 2, i))
                coins.setdefault(k5(x, y, z + hp / 2), []).append(i)
        elif cle == 'poutre_fine':
            lx, ly = vec(yaw + 90)
            tetes += [(x - F / 2 * lx, y - F / 2 * ly, z, i), (x + F / 2 * lx, y + F / 2 * ly, z, i)]
        elif cle == 'escalier':
            esc_a[k5(x, y, z - F / 2)] = i
        elif cle in SOLS:
            poly = polygone(dict(type='tri' if cle.endswith('_tri') else 'carre', x=x, y=y, yaw=yaw))
            zt = z + (50 if cle.startswith('fond') else 0)
            polys.append((poly, zt, i))
            if not plateforme(rep_):
                segs += [(*poly[j], *poly[(j + 1) % len(poly)], zt, i) for j in range(len(poly))]
    grille = {}
    for sg in segs:
        for gx in range(int(min(sg[0], sg[2]) // 400), int(max(sg[0], sg[2]) // 400) + 1):
            for gy in range(int(min(sg[1], sg[3]) // 400), int(max(sg[1], sg[3]) // 400) + 1):
                grille.setdefault((gx, gy), []).append(sg)

    def sous(x, y, z):                           # plancher dont le dessus est à z sous (x, y)
        return [i for poly, zt, i in polys if abs(zt - z) < 2 and _dans_poly(poly, x, y, -1.0)]

    def tetes_point(q):
        return [t[3] for t in tetes if abs(q[2] - t[2]) < 12 and math.hypot(q[0] - t[0], q[1] - t[1]) < 25]

    def appuis_point(q):
        return [sg[5] for sg in grille.get((int(q[0] // 400), int(q[1] // 400)), [])
                if abs(q[2] - sg[4]) < 12 and _dist_seg(q[0], q[1], *sg[:4]) < 15] + tetes_point(q)

    plafonds, lames = [], []
    for i, (pl, nn, cle, x, y, z, yaw, rep_) in enumerate(P):
        if cle in ('fond', 'fond_tri') or rep_.startswith('ancre'):
            continue
        if cle in MURS:
            continue                             # murs : plus bas, du bas vers le haut (porté par dessous ou pendu)
        elif cle in PILIERS or cle == 'escalier':
            h = HAUT_PILIER.get(cle, F)
            bas = z - h / 2
            k = k5(x, y, bas)
            r = ok(i, [d[kk] for d in (pil_a, esc_a) for kk in [k5(x, y, bas - F), k5(x, y, bas - F / 2)] if kk in d
                       and d[kk] != i and abs(P[d[kk]][5] + HAUT_PILIER.get(P[d[kk]][2], F) / 2 - bas) < 2])
            par[i] = r or ok(i, sommets_mur.get(k, [])) or ok(i, sous(x, y, bas))   # joint de murs, plancher
        elif cle in SOLS:
            poly = polygone(dict(type='tri' if cle.endswith('_tri') else 'carre', x=x, y=y, yaw=yaw))
            r = []
            for m in range(len(poly)):
                (x1, y1), (x2, y2) = poly[m], poly[(m + 1) % len(poly)]
                r += aretes.get(k5((x1 + x2) / 2, (y1 + y2) / 2, z), [])
                r += coins.get(k5(x1, y1, z), [])
            par[i] = ok(i, r)
            plafonds.append(i)
        elif cle == 'poutre_fine':
            lx, ly = vec(yaw + 90)
            par[i] = ok(i, [j for q in ((x - F / 2 * lx, y - F / 2 * ly, z), (x + F / 2 * lx, y + F / 2 * ly, z))
                            for j in appuis_point(q) if P[j][2] in MURS])
        elif cle == 'rampe':                     # tête de pilier fin ou bout de poutre (pas un haut de mur)
            par[i] = ok(i, [j for q in bouts_lame(x, y, z, yaw) for j in tetes_point(q)])
            lames.append(i)
        elif cle in ('heavy', 'tek', 'tesla'):
            par[i] = ok(i, sous(x, y, z - 10) if debout(cle, rep_) else
                        [j for j in range(n) if P[j][2] == 'chaume_mur' and abs(P[j][5] - z) < 2
                         and math.hypot(P[j][3] - x, P[j][4] - y) < 15][:1])
        elif cle in ('crop', 'crop_m'):
            par[i] = ok(i, sous(x, y, z - 10))

    tenus = set()
    for i in sorted((i for i in range(n) if P[i][2] in MURS), key=lambda i: P[i][5]):
        pl, nn, cle, x, y, z, yaw, rep_ = P[i]
        bas = z - F / 2
        r = ok(i, [j for poly, zt, j in polys if abs(zt - bas) < 2 and any(
            _dist_seg(x, y, *poly[m], *poly[(m + 1) % len(poly)]) < 2 for m in range(len(poly)))])
        if (k := k5(x, y, bas - F)) in mur_a and mur_a[k] in tenus and R[mur_a[k]] <= R[i]:
            r.append(mur_a[k])
        if r:
            tenus.add(i)
            par[i] = r
    for i in sorted((i for i in range(n) if P[i][2] in MURS and not par[i]), key=lambda i: -P[i][5]):
        pl, nn, cle, x, y, z, yaw, rep_ = P[i]
        if (k := k5(x, y, z + F / 2)) in mur_a and R[mur_a[k]] <= R[i]:
            par[i] = [mur_a[k]]                  # pend sous le mur du dessus (jupe)

    def propager(groupe, voisins):
        """Pièces portées de proche en proche (plafonds, lames) : chacune reçoit pour porteur le voisin déjà porté."""
        file = [i for i in groupe if par[i]]
        vu = set(file)
        while file:
            i = file.pop(0)
            for j in voisins(i):
                if j not in vu and not par[j] and R[i] <= R[j]:
                    par[j] = [i]
                    vu.add(j)
                    file.append(j)

    arete_pl = {}
    for i in plafonds:
        pl, nn, cle, x, y, z, yaw, rep_ = P[i]
        poly = polygone(dict(type='tri' if cle.endswith('_tri') else 'carre', x=x, y=y, yaw=yaw))
        for m in range(len(poly)):
            (x1, y1), (x2, y2) = poly[m], poly[(m + 1) % len(poly)]
            arete_pl.setdefault(k5((x1 + x2) / 2, (y1 + y2) / 2, z), []).append(i)

    def vois_pl(i):
        pl, nn, cle, x, y, z, yaw, rep_ = P[i]
        poly = polygone(dict(type='tri' if cle.endswith('_tri') else 'carre', x=x, y=y, yaw=yaw))
        return [j for m in range(len(poly)) for j in arete_pl.get(
            k5((poly[m][0] + poly[(m + 1) % len(poly)][0]) / 2, (poly[m][1] + poly[(m + 1) % len(poly)][1]) / 2, z), [])
                if j != i]
    propager(plafonds, vois_pl)
    bout_l = {}
    for i in lames:
        for q in bouts_lame(*P[i][3:7]):
            bout_l.setdefault((k5(*q), round(P[i][6] % 360)), []).append(i)
    propager(lames, lambda i: [j for q in bouts_lame(*P[i][3:7])
                               for j in bout_l[(k5(*q), round(P[i][6] % 360))] if j != i])
    sans = [i for i in range(n) if not par[i] and P[i][2] not in ('fond', 'fond_tri') and not P[i][7].startswith('ancre')]
    return par, sans


def ordre_de_pose(plans):
    """Toutes les pièces des plans dans un ordre où chacune vient après ce qui la porte : plan après plan (ordre de
    PLANS), et dans chaque plan du bas vers le haut (cote du pied) ; les pièces suspendues suivent leur porteur. Un
    porteur d'un plan posé plus tard ne compte pas : chaque pièce doit être tenue par ce qui est déjà posé."""
    import heapq
    P = [q for q in _pieces_plans(plans) if not q[7].startswith('ancre')]
    rang = {cle: n for n, cle in enumerate(plans)}           # ordre de pose des plans = ordre du dictionnaire
    par, sans = porteurs(P, rang)
    assert not sans, [(P[i][0], P[i][7]) for i in sans[:10]]

    def pied(i):
        pl, nn, cle, x, y, z, yaw, rep_ = P[i]
        if cle == 'rampe':
            return z - 200
        if cle in ('fond', 'fond_tri'):
            return -1e6                          # le sol d'abord
        if cle in SOLS:
            return z - 15
        if cle in ('heavy', 'tek', 'tesla'):
            return z - (10 if debout(cle, rep_) else F / 2)
        if cle in ('poutre_fine', 'crop', 'crop_m'):
            return z - 20
        if rep_.startswith('depart'):
            return z - F / 2 - 1                 # pilier de départ : avant les murs de son niveau (tour 1809)
        return z - (HAUT_PILIER.get(cle, F) / 2)
    enfants = [[] for _ in P]
    reste = [0] * len(P)
    for i, ps in enumerate(par):
        for j in set(ps):
            enfants[j].append(i)
            reste[i] += 1
    cle_tas = lambda i: (rang[P[i][0]], pied(i), P[i][1], i)
    tas = [cle_tas(i) for i in range(len(P)) if reste[i] == 0]
    heapq.heapify(tas)
    ordre = []
    while tas:
        *_, i = heapq.heappop(tas)
        ordre.append(i)
        for j in enfants[i]:
            reste[j] -= 1
            if reste[j] == 0:
                heapq.heappush(tas, cle_tas(j))
    assert len(ordre) == len(P), 'cycle dans les appuis'
    return P, ordre, par


def ordonner_plans(plans):
    """Range les entrées de chaque plan dans l'ordre de pose (ordre_de_pose) : l'ancre ou le mur de référence d'abord,
    puis chaque pièce après ce qui la porte. Vérifie la taille des plans (TAILLE_MAX entrées)."""
    P, ordre, par = ordre_de_pose(plans)
    pos = {(P[i][0], P[i][1]): k for k, i in enumerate(ordre)}
    for cle, t in plans.items():
        tete = [n for n, l_ in enumerate(t.lignes) if l_[5].startswith(('ancre', 'reference'))]
        corps = sorted((n for n in range(len(t.lignes)) if n not in tete), key=lambda n: pos[(cle, n)])
        t.reordonner(tete + corps)
        t.snap = list(range(len(tete))) if tete and t.lignes[0][5].startswith('ancre') else [0] if tete else []
        assert len(t.entries) <= TAILLE_MAX, (cle, len(t.entries))
    return P, ordre, par


def verifier_plans(p, plans, modules):
    """Chaque entrée des modules est dans un seul plan ; rien n'est posé au-dessus du trou ni de la plateforme verte,
    hors fondations de la plateforme."""
    total_modules = sum(1 for _, m in modules for l_ in m.lignes if not l_[5].startswith('ancre'))
    total_plans = sum(1 for t in plans.values() for l_ in t.lignes if not l_[5].startswith('ancre'))
    assert total_modules == total_plans, (total_modules, total_plans)
    for cle, t in plans.items():
        for cle_p, x, y, Z, yaw, r in t.lignes:
            if r.startswith(('ancre', 'bord du trou', 'casquette du trou', 'plateforme')) or ' TROU' in r:
                continue                       # bord du trou : tourelles (pivot 10 UU devant le mur) et casquette en
                                               # porte-à-faux au-dessus du gouffre ; fondations vertes
            assert not dans_trou(p, x, y), (cle, r, x, y)
    print(f"  {len(plans)} plans, {total_plans} entrées, aucune au-dessus du trou : " +
          ', '.join(f"{cle} {len(t.entries)}" for cle, t in plans.items()))


def bilan_brut(tot):
    """Décompose les produits fabriqués en ressources brutes (recettes ASE/ASA usuelles, à vérifier)."""
    el, po, pc, pe = tot.get('EL', 0), tot.get('PO', 0), tot.get('PC', 0), tot.get('PE', 0)
    mi = tot.get('MI', 0) + el                       # électronique : 1 lingot + 3 perles de silice
    pc_tot = pc + 2 * po                             # polymère : 2 obsidienne + 2 pâte cimentée
    return {'minerai_metal': 2 * mi, 'perles_silice': 3 * el, 'obsidienne': 2 * po,
            'chitine_ou_keratine': 4 * pc_tot, 'pierre': 8 * pc_tot + pe + tot.get('PI', 0), 'silex': 2 * pe,
            'cristal': tot.get('CR', 0), 'element': tot.get('EM', 0), 'perles_noires': tot.get('PN', 0),
            'huile': tot.get('HU', 0), 'cuir': tot.get('CU', 0), 'fibre': tot.get('FI', 0),
            'lingots_total': mi, 'pate_totale': pc_tot}


# ---------------------------------------------------------------- vérifications
def verifier_481(chemin):
    d = json.load(open(chemin, encoding='utf-8'))
    ref = [e for e in d['entries'] if e['structure'].endswith(('Floor_Metal_C', 'BP_TriFoundation_Metal_C'))]
    pieces, _ = pavage(7, centre=False)

    def empreinte(x, y, yaw, tri):
        # un triangle se décrit de 3 façons (yaw ±120°) : on compare centroïde + yaw modulo 120
        if tri:
            nx, ny = vec(yaw)
            return x - H / 6 * nx, y - H / 6 * ny, yaw % 120, 120
        return x, y, yaw % 90, 90

    ok = 0
    for pc in pieces:
        gx, gy, gyaw, mod = empreinte(pc['x'], pc['y'], pc['yaw'], pc['type'] == 'tri')
        for e in ref:
            tri = e['structure'].endswith('BP_TriFoundation_Metal_C')
            if (pc['type'] == 'tri') != tri:
                continue
            ex, ey, eyaw, _ = empreinte(e['loc']['x'], e['loc']['y'], e['rot']['yaw'], tri)
            dyaw = (eyaw - gyaw) % mod
            if math.hypot(ex - gx, ey - gy) < 1.0 and min(dyaw, mod - dyaw) < 0.5:
                ok += 1
                break
    print(f'Vérification 481 : {ok}/{len(pieces)} pièces générées retrouvées dans le template ({len(ref)} au sol).')
    return ok == len(pieces) == len(ref)


def verifier_pavage(pieces):
    try:
        from shapely.geometry import Polygon
        from shapely.ops import unary_union
    except ImportError:
        print('shapely absent : contrôle de recouvrement ignoré')
        return
    polys = [Polygon(polygone(pc)) for pc in pieces]
    U = unary_union(polys)
    tot = sum(q.area for q in polys)
    aire_d8 = 3 * (2 + math.sqrt(3)) * (8 * F) ** 2
    print(f'Pavage : {len(pieces)} pièces, recouvrement {tot - U.area:.1f} UU², aire {U.area:.0f} '
          f'(D8 théorique {aire_d8:.0f}), trous {aire_d8 - U.area:.1f} UU²')


def verifier_encombrements(p, infos_pod, col, ordre):
    """Contrôles de non-collision entre éléments ajoutés (distances horizontales minimales)."""
    msgs = []
    # colonne d'escaliers : dégagée de la pile d'ancrage et des piliers PA
    d_ancre = min(math.hypot(x - ANCRE[0], y - ANCRE[1]) for x, y in infos_pod['cellule'])
    msgs.append(f'Colonne d\'escaliers : {d_ancre:.0f} UU de la pile d\'ancrage (0 ; 300)')
    assert d_ancre > 100
    # colonnade : écart aux générateurs de secours et aux Tesla, et hors de la ligne de fût et de rive
    for nom, th, A, Z in GENERATEURS:
        if Z == 0:
            g = (A * vec(th)[0], A * vec(th)[1])
            d = min(math.hypot(c['x'] - g[0], c['y'] - g[1]) for c in col['colonnes'])
            msgs.append(f'{nom} θ{th} : {d:.0f} UU de la colonnade')
            assert d > 150, 'déplacer le générateur (GENERATEURS)'
    for s in ordre:
        if s['couche'] == 'RIVE':
            d = min(math.hypot(c['x'] - s['xm'], c['y'] - s['ym']) for c in col['colonnes'])
            assert d > 300, d
    R = col['rayon']
    attique = rayon_coin(5) + 100 < R < apo(7) - 100
    couloir = rayon_coin(4) + 100 < R < apo(5) - 100
    assert attique or couloir, 'la colonnade doit être dans l\'attique A ou dans le couloir sous la galerie'
    msgs.append(f"Colonnade : {len(col['colonnes'])} colonnes sur {col['n']} positions, pas {col['pas_arc']:.1f} UU, "
                + ('attique A (entre fût et rive)' if attique else 'couloir (entre pod et fût)'))
    for m in msgs:
        print('  ' + m)


# ---------------------------------------------------------------- sorties
def bilan(compteurs):
    tot = {}
    for cle, n in compteurs.items():
        for res, q in COUTS[cle].items():
            if res == 'est':
                continue
            tot[res] = tot.get(res, 0) + q * n
    return tot


def ecrire_csv(chemin, lignes, entete):
    with open(chemin, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(entete)
        w.writerows(lignes)


def _mpl():
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from matplotlib.patches import Polygon as MPoly
        return plt, MPoly
    except ImportError:
        print('matplotlib absent : plans PNG non générés')
        return None, None


def _dodeca(ax, m, **kw):
    cs = [vec(15 + 30 * k) for k in range(13)]
    R = rayon_coin(m)
    ax.plot([R * c for c, s in cs], [R * s for c, s in cs], **kw)


def plans_png(rep, p, pieces, ordre, ob, jupe, infos_pod, col, trou, appuis):
    plt, MPoly = _mpl()
    if not plt:
        return
    # --- plan de calpinage
    fig, ax = plt.subplots(figsize=(13, 13))
    for pc in pieces:
        r = pc['anneau']
        if piece_dans_trou(p, pc):
            ax.add_patch(MPoly(polygone(pc), closed=True, fc='none', ec='#c0392b', lw=0.6, ls='--'))
            continue
        if piece_plateforme(p, pc):
            fc = '#2e9e4f'
        elif r > p['anneau_rive']:
            fc = '#9aa5b1' if r == p['anneau_rive'] + 1 else '#6c757d'
        elif r <= p['anneau_pod']:
            fc = '#f2b880' if pc['type'] == 'tri' else '#e07a2f'
        else:
            fc = '#9cc7e8' if pc['type'] == 'tri' else '#3f88c5'
        ax.add_patch(MPoly(polygone(pc), closed=True, fc=fc, ec='#333', lw=0.3))
    for m, nom, coul in ((4, 'D4 mur de pod', '#b00'), (5, 'D5 cage', '#070'), (7, 'D7 rive', '#000'),
                         (8, 'D8 bord plateforme', '#555')):
        _dodeca(ax, m, color=coul, lw=2 if m != 8 else 1, ls='-' if m != 8 else '--',
                label=f'{nom} (apothème {apo(m):.0f} UU)')
    cs = [vec(c['theta']) for c in col['colonnes']]
    ax.plot([col['rayon'] * c for c, s in cs], [col['rayon'] * s for c, s in cs], '.', color='#6a040f', ms=2,
            label=f"colonnade Ø{2 * col['rayon'] / F:.1f} F ({len(col['colonnes'])} colonnes)")
    for k in range(12):
        c, s = vec(30 * k)
        ax.annotate(f'{30 * k}°', (5100 * c, 5100 * s), ha='center', va='center', fontsize=10,
                    color='#3f88c5' if k % 2 == 0 else '#a05a00')
        ax.plot([0, 4700 * c], [0, 4700 * s], color='#888', lw=0.5, ls=':')
    ax.plot(*ANCRE, 'k+', ms=14)
    ax.set_xlim(-5400, 5400)
    ax.set_ylim(-5400, 5400)
    ax.set_aspect('equal')
    ax.set_title('Plan de calpinage Ø30 (D8) — carrés foncés / triangles clairs ; orange = pod (anneaux 1-7), '
                 f"bleu = couronne (8-13), gris clair = palier 14 (-{p['decaissement']:.0f}), "
                 f"gris foncé = palier 15 (-{2 * p['decaissement']:.0f}) ;\nrouge pointillé = trou ({len(trou)} "
                 "fondations non posées) ; vert = plateforme future (posée, rien dessus)", fontsize=10)
    ax.legend(loc='lower left', fontsize=9)
    ax.set_xlabel('x (UU)  — axe 0° = branche de carrés E0 ; + = ancre (0 ; 300)')
    ax.set_ylabel('y (UU)')
    fig.savefig(os.path.join(rep, 'plan_calpinage.png'), dpi=80, bbox_inches='tight')
    plt.close(fig)

    # --- coupe radiale (θ = 0°, côté E0)
    fig, ax = plt.subplots(figsize=(15, 9))
    A4, A5, A7, A8 = apo(4), apo(5), apo(7), apo(8)
    Zr = p['rive_niveaux'] * F
    zmez = p['mezzanine']
    Zc = zmez + p['cage_niveaux'] * F
    Zpod = p['pod_niveaux'] * F
    Ztoit = Zpod + F
    Zsommet = infos_pod['Zsommet']
    ax.fill_between([0, A7], [-100, -100], [0, 0], color='#3f88c5', alpha=.5, label='fondations Z0 (plan 1)')
    for (r0, r1, Z), coul in zip(paliers_bord(p), ('#9aa5b1', '#6c757d')):
        ax.fill_between([r0, r1], [Z - 100, Z - 100], [Z, Z], color=coul,
                        label=f'palier de bord Ø{2 * r0 / F:.0f} → Ø{2 * r1 / F:.0f} : Z {Z:.0f}')
    ax.fill_between([-200, A8], [-1000, -1000], [-400, -400], color='#ccc', alpha=.5,
                    label='Metal Cliff Platform (épaisseur indicative)')
    ax.plot([150, 150], [0, zmez], color='#9c6644', lw=4, ls=(0, (1, 1)), label='colonne d\'escaliers jusqu\'à Z1800')
    ax.plot([A4, A4], [0, Zpod], color='#b00', lw=4,
            label=f"tour du pod D4, murs pleins ({p['pod_niveaux']} murs, plan 5)")
    ax.plot([A4, A4], [Zpod, Ztoit], color='#b00', lw=4, ls=(0, (2, 1)),
            label='couronne (plan 9, calée sur le mur de référence A)')
    ax.plot([A5, A5], [0, zmez], color='#070', lw=3, ls=(0, (3, 1)), label='fût D5 en cadres doubles (6 niveaux)')
    ax.plot([A5, A5], [zmez + F, Zc], color='#0a0', lw=6, ls=(0, (2, 1)), label='L2 : cadres doubles')
    ax.plot([A7, A7], [0, Zr], color='k', lw=3, ls=(0, (3, 1)), label='mur de rive D7 en cadres doubles')
    for Z in (zmez, zmez + F, Zc):
        ax.plot([A4, A5], [Z, Z], color='#070', lw=1.5)
    ax.plot([0, A4], [zmez, zmez], color='#b00', lw=1.5, ls='--', label='mezzanine Z1800')
    ax.plot([0, A4], [Ztoit, Ztoit], color='#b00', lw=2, label=f'toiture pleine : plancher de toit Z{Ztoit:.0f} (plan 9)')
    R = col['rayon']
    ax.plot([R, R], [0, min(hauteur_pente_A(p, R, 0) - 30, p['colonnade_hauteur'])], color='#6a040f', lw=3, alpha=.4,
            label=f"colonnade r={R:.0f} (option, plan 2)")
    lame = dict(lw=3, ls=(0, (1, 0.6)))         # rampes inclinées : lames, tracé en pointillé serré
    ax.plot([A7 - p['rangs_pente_A'] * F, A7 + 2 * F], [Zr + p['rangs_pente_A'] * F, Zr - 2 * F],
            color='#e07a2f', label='pente A (plan 4) et overhang (plan 3) : rampes inclinées', **lame)
    if jupe:
        ax.plot([jupe['A'], ob['A_bout']], [jupe['Z_haut'], ob['Z_bout']], color='#c1121f',
                label='débord dans le vide : rampes accrochées à la jupe', **lame)
    ax.plot([A5 + p['casquette'] * F, A5 - F], [Zc - p['casquette'] * F, Zc + F], color='#7b2cbf',
            label='casquette et appentis (plan 6) : rampes inclinées', **lame)
    ax.plot([A4, A4 - (Zsommet - Ztoit)], [Ztoit, Zsommet], color='#b00',
            label='toit en rampes D4 → centre (plan 10)', **lame)
    if jupe:
        ax.plot([jupe['A'], jupe['A']], [jupe['Z'], jupe['Z_haut']], color='#555', lw=2, ls=(0, (3, 1)),
                label='mur de jupe (bord D8) en cadres doubles, posé sur le palier')
    # appuis des rampes dans le plan de coupe (lignes du côté 0 les plus proches de l'axe)
    for cle, x, y, Zb, Zh in appuis:
        if x > 0 and abs(y) < 160:
            if cle == 'poutre_fine':
                ax.plot([x - 150, x + 150], [Zb, Zb], color='#2a9d8f', lw=3)
            else:
                ax.plot([x, x], [Zb, Zh], color='#2a9d8f', lw=2)
    ax.plot([], [], color='#2a9d8f', lw=2,
            label='poteaux de piliers fins (jonctions de lames)' + (', poutre fine du débord' if p['debord'] > 1 else ''))
    sec = secteurs(p, ob, jupe)
    yeux = {'L1': (A5 + DECALAGE_MONTAGE + SAILLIE_TETE, zmez + F / 2, 1, 'tab:blue'),
            'RIVE': (A7 + DECALAGE_MONTAGE + SAILLIE_TETE / 2, F * 1.5, 1, '#d4ac0d'),
            'D4': (A4 + DECALAGE_MONTAGE + SAILLIE_TETE, Zpod - F / 2, 1, 'tab:red'),
            'DESSUS': (p['dessus_apotheme'], Ztoit + 100, 1, 'tab:green'),
            'RIVE-H0': (A7 + DECALAGE_MONTAGE + SAILLIE_TETE, F / 2, 1, 'tab:purple')}
    for pid, (r, z, sens, coul) in yeux.items():
        sect = sec.get(pid)
        if not sect:
            continue
        if pid == 'RIVE':                        # tir plongeant : on trace les parties vues des 2 paliers
            for b in sect:
                if b:
                    for rb in b[:2]:
                        ax.plot([r, rb], [z, b[2]], color=coul, lw=0.8, ls='--')
            ax.plot(r, z, 'o', color=coul, ms=8, label='Tesla de rive : ' + ' ; '.join(
                f'Z{b[2]:.0f} vu de {b[0]:.0f} à {b[1]:.0f}' for b in sect if b))
            continue
        for a in sect:
            ax.plot([r, r + sens * 6000 * math.cos(math.radians(a))], [z, z + 6000 * math.sin(math.radians(a))],
                    color=coul, lw=0.8, ls='--')
        ax.plot(r, z, 'o', color=coul, ms=8, label=f'{pid} : secteur {sect[0]:+.1f}° / {sect[1]:+.1f}°')
    ax.annotate('pics (bande protégée)', (A7 + 150, -p['decaissement']), xytext=(A7 - 900, -900), arrowprops=dict(arrowstyle='->'))
    ax.annotate('chute -> abysse', (ob['A_bout'], ob['Z_bout']), xytext=(ob['A_bout'] + 200, ob['Z_bout'] - 900),
                arrowprops=dict(arrowstyle='->'))
    ax.set_xlim(-200, 7000)
    ax.set_ylim(-1600, max(6200, Zsommet + 300))
    ax.set_aspect('equal')
    ax.grid(True, lw=0.3)
    ax.set_xlabel('distance au centre le long de la normale 0° (UU)')
    ax.set_ylabel('Z (UU) — 0 = dessus des fondations intérieures')
    ax.set_title('Coupe radiale type (côté E0, θ=0°) — tour du pod, cage, rampes, tourelles et secteurs de tir')
    ax.legend(loc='upper right', fontsize=7)
    fig.savefig(os.path.join(rep, 'coupe_radiale.png'), dpi=80, bbox_inches='tight')
    plt.close(fig)

    # --- plan des tourelles et câblage
    fig, ax = plt.subplots(figsize=(12, 12))
    for pc in trou:
        ax.add_patch(MPoly(polygone(pc), closed=True, fc='#f4d4d0', ec='#c0392b', lw=0.4, ls='--', alpha=.6))
    for x, y, nu, r, th in bords_trou(p):
        nx, ny = vec(nu)
        ax.plot([x + 150 * ny, x - 150 * ny], [y - 150 * nx, y + 150 * nx], color='#c0392b', lw=2)
    styles = {'heavy': ('s', '#c0392b'), 'tek': ('^', '#2471a3'), 'tesla': ('*', '#d4ac0d'), 'crop': ('P', '#2e9e4f')}
    for s in ordre:
        if not s['posee']:
            continue
        mk, co = styles[s['type']]
        ax.plot(s['x'], s['y'], mk, color=co, ms=9 if 'TROU' in s['couche'] else 7,
                mec='k' if s['couche'] in ('JUPE-int', 'TROU', 'TROU-L1') else co,
                mew=1.5 if 'TROU' in s['couche'] else .5)
        nx, ny = vec(s['sortie'])
        ax.plot([s['x'], s['x'] + 160 * nx], [s['y'], s['y'] + 160 * ny], color=co, lw=0.8)
        if s['couche'] != 'L1':
            ax.annotate(str(s['ordre']), (s['x'], s['y']), fontsize=6, xytext=(3, 3), textcoords='offset points')
    for m, coul in ((4, '#b00'), (5, '#070'), (7, '#000'), (8, '#555')):
        _dodeca(ax, m, color=coul, lw=1)
    cs = [vec(c['theta']) for c in col['colonnes']]
    ax.plot([col['rayon'] * c for c, s in cs], [col['rayon'] * s for c, s in cs], '.', color='#6a040f', ms=1.5,
            label='colonnade circulaire')
    R8 = (apo(4) + 150) / math.cos(math.radians(15))
    pts = [vec(15 + 30 * k) for k in range(13)]
    for k in range(12):                         # boucle de câbles, interrompue au-dessus du trou
        (c1, s1), (c2, s2) = pts[k], pts[k + 1]
        seg = [(R8 * (c1 + (c2 - c1) * u / 20), R8 * (s1 + (s2 - s1) * u / 20)) for u in range(21)]
        for (xa, ya), (xb, yb) in zip(seg, seg[1:]):
            if not dans_trou(p, (xa + xb) / 2, (ya + yb) / 2):
                ax.plot([xa, xb], [ya, yb], color='#2a9d8f', lw=1.2, ls='--')
    ax.plot([], [], color='#2a9d8f', lw=1.2, ls='--', label='boucle de câbles galerie (Z1800, anneau 8)')
    for k in range(12):
        c, s_ = vec(15 + 30 * k)
        r2 = (apo(7) + 600) / math.cos(math.radians(15))
        if not dans_trou(p, (R8 + r2) / 2 * c, (R8 + r2) / 2 * s_, bord=True):
            ax.plot([R8 * c, r2 * c], [R8 * s_, r2 * s_], color='#2a9d8f', lw=0.8, ls=':')
    for nom, th, cle in NOYAU:
        c, s_ = vec(th)
        ax.plot(A_NOYAU * c, A_NOYAU * s_, 'D' if cle == 'generateur_tek' else 'P',
                color='#2a9d8f' if cle == 'generateur_tek' else '#e9c46a', ms=10, mec='k')
    ax.plot([], [], 'D', color='#2a9d8f', mec='k', label='Générateurs Tek principal et secours (noyau, en cage, Z0)')
    ax.plot([], [], 'P', color='#e9c46a', mec='k', label='Boîtes de munitions (noyau, en cage, Z0)')
    for nom, (mk, co) in styles.items():
        ax.plot([], [], mk, color=co, label=NOMS[nom])
    ax.plot([], [], 's', color='#c0392b', mec='k', mew=1.5, ms=9,
            label='tourelle reposée sur un mur de bord du trou, face au gouffre (grande)')
    ax.plot([], [], color='#c0392b', lw=2, label='murs de bord du trou')
    n_pos = sum(1 for s in ordre if s['posee'])
    ax.set_aspect('equal')
    ax.set_title(f'Défense : {n_pos} emplacements (cap de 100, Tesla et Plant X comprises) — trait = sens de tir ; '
                 'numéros = ordre de pose (hors L1)', fontsize=10)
    ax.legend(loc='lower left', fontsize=8)
    fig.savefig(os.path.join(rep, 'plan_tourelles.png'), dpi=80, bbox_inches='tight')
    plt.close(fig)


def plan_pod(rep, p, infos_pod):
    plt, MPoly = _mpl()
    if not plt:
        return
    fig, ax = plt.subplots(figsize=(11, 11))
    pieces, contours = pavage(p['anneau_pod'] + 1)
    for pc in pieces:
        if piece_dans_trou(p, pc):
            ax.add_patch(MPoly(polygone(pc), closed=True, fc='#f4d4d0', ec='#c0392b', lw=0.6, ls='--'))
        elif pc['anneau'] <= p['anneau_pod']:
            ax.add_patch(MPoly(polygone(pc), closed=True, fc='#f6e3d0' if pc['type'] == 'tri' else '#efcfae',
                               ec='#bbb', lw=0.3))
    portes = 0
    for x, y, nu, k, i in cotes_contour(contours[7]):
        if dans_trou(p, x, y, bord=True):
            continue
        porte = k % 2 == 1 and i == 1
        portes += porte
        ax.plot(x, y, 's', color='#2a9d8f' if porte else '#b00', ms=9 if porte else 4)
    for x, y, nu, r, th in bords_trou(p):
        if r <= apo(4) + 1:
            nx, ny = vec(nu)
            ax.plot([x + 150 * ny, x - 150 * ny], [y - 150 * nx, y + 150 * nx], color='#c0392b', lw=3)
    Zt = p['pod_niveaux'] * F
    for n, coul, nom in ((2, '#000', f'piliers PA (Z0 -> {Zt:.0f}, + couronne)'), (1, '#666', f'piliers PB (Z0 -> {Zt:.0f}, + couronne)')):
        R = rayon_coin(n)
        pts = [vec(15 + 30 * k) for k in range(12)]
        pts = [(R * c, R * s_) for c, s_ in pts if not dans_trou(p, R * c, R * s_)]
        ax.plot([x for x, y in pts], [y for x, y in pts], 'o', color=coul, ms=9, label=nom)
    ax.add_patch(MPoly(infos_pod['cellule'], closed=True, fc='#ffd166', ec='#9c6644', lw=1.5, alpha=.8))
    ax.annotate('escaliers\n(Z0 → 1800)', (infos_pod['escalier']['x'], infos_pod['escalier']['y']),
                ha='center', va='center', fontsize=7)
    for pc in infos_pod['tremie']:
        ax.add_patch(MPoly(polygone(pc), closed=True, fc='none', ec='#7b2cbf', lw=1.5, ls='--'))
    ax.plot([], [], color='#7b2cbf', lw=1.5, ls='--', label='trémie de la mezzanine Z1800 (au-dessus des escaliers)')
    ax.plot(*ANCRE, 'k+', ms=12, label='pilier de référence (0 ; 300)')
    carres = {pc['cote'] * 30: pc for pc in pavage(1, centre=False)[0] if pc['type'] == 'carre'}
    for nom, th, cle in NOYAU:
        pc = carres[th]
        ax.add_patch(MPoly(polygone(pc), closed=True, fc='#2a9d8f' if cle == 'generateur_tek' else '#e9c46a',
                           alpha=.6, ec='k', lw=2))
        ax.annotate(nom.replace(' (', '\n('), (pc['x'], pc['y']), ha='center', va='center', fontsize=6)
    ax.plot([], [], 's', color='#2a9d8f', alpha=.6, mec='k', ms=9,
            label=f'cages du noyau : {CAGE_NIVEAUX} murs de haut, porte double côté hall, plafond')
    for nom, th, A, lg, pf, hm in GABARITS:
        nx, ny = vec(th)
        dx, dy = -ny, nx
        cx, cy = A * nx, A * ny
        coins = [(cx + u * nx + v * dx, cy + u * ny + v * dy) for u, v in
                 ((-pf / 2, -lg / 2), (pf / 2, -lg / 2), (pf / 2, lg / 2), (-pf / 2, lg / 2))]
        ax.add_patch(MPoly(coins, closed=True, fc='#3f88c5', alpha=.35, ec='#1d4e89', lw=1.5))
        ax.annotate(f'{nom}\n{lg / F:.0f}×{pf / F:.0f} F, {hm} murs', (cx, cy), ha='center', va='center', fontsize=8)
    ax.plot([], [], 's', color='#2a9d8f', ms=9, label=f'portes doubles du hall ({portes})')
    ax.plot([], [], 's', color='#b00', ms=4, label='mur de pod D4')
    ax.plot([], [], color='#c0392b', lw=3, label=f'murs de bord du trou (Z0 → {Zt:.0f}, + couronne)')
    ax.plot([], [], 's', mfc='#f4d4d0', mec='#c0392b', label='trou (fondations retirées)')
    ax.set_aspect('equal')
    ax.set_xlim(-2600, 2600)
    ax.set_ylim(-2600, 2600)
    ax.set_title('Pod central — hall Z0→1800 : escaliers, piliers, portes, machines ; trou à l\'avant (θ 180°)',
                 fontsize=10)
    ax.legend(loc='lower left', fontsize=8)
    fig.savefig(os.path.join(rep, 'plan_pod.png'), dpi=80, bbox_inches='tight')
    plt.close(fig)


def plan_rampes(rep, p, modules):
    """Vue de dessus de toutes les rampes inclinées (toit, casquette, pente A, overhang) ; couleur = cote du bas."""
    plt, MPoly = _mpl()
    if not plt:
        return
    fig, ax = plt.subplots(figsize=(13, 13))
    rampes = [(x, y, Z, yaw) for _, m in modules for cle, x, y, Z, yaw, r in m.lignes if cle == 'rampe']
    zmin, zmax = min(r[2] for r in rampes), max(r[2] for r in rampes)
    cmap = plt.get_cmap('viridis')
    for x, y, Z, yaw in rampes:
        nx, ny = vec(yaw + 90)                   # axe de la lame (vers le bas de la pente)
        ax.plot([x - 150 * nx, x + 150 * nx], [y - 150 * ny, y + 150 * ny], color=cmap((Z - zmin) / (zmax - zmin)),
                lw=1.2)
    for m, coul, nom in ((4, '#b00', 'D4 mur de pod'), (5, '#070', 'D5 cage'), (7, '#000', 'D7 rive'),
                         (8, '#555', 'D8 bord de plateforme')):
        _dodeca(ax, m, color=coul, lw=1, label=nom)
    pot = {(round(x), round(y)) for _, m in modules for cle, x, y, Z, yaw, r in m.lignes
           if r.startswith('appui') and cle != 'poutre_fine'}
    pou = [(x, y, yaw) for _, m in modules for cle, x, y, Z, yaw, r in m.lignes if cle == 'poutre_fine']
    ax.plot([x for x, y in pot], [y for x, y in pot], 'o', color='#e63946', ms=2.5,
            label=f'poteau en piliers fins sous une jonction de lames ({len(pot)})')
    for x, y, yaw in pou:
        nx, ny = vec(yaw + 90)
        ax.plot([x - 150 * nx, x + 150 * nx], [y - 150 * ny, y + 150 * ny], color='#e63946', lw=2.5)
    ax.plot([], [], color='#e63946', lw=2.5, label=f'poutre fine sous le 2e rang du débord ({len(pou)})')
    ax.plot([], [], color=cmap(0.0), lw=2, label=f'rampe la plus basse (Z {zmin:.0f}, bout de l\'overhang)')
    ax.plot([], [], color=cmap(1.0), lw=2, label=f'rampe la plus haute (Z {zmax:.0f}, faîtage)')
    ax.set_aspect('equal')
    ax.set_xlim(-5400, 5400)
    ax.set_ylim(-5400, 5400)
    ax.set_title(f'Rampes inclinées (Sloped Railing), aucun toit incliné : {len(rampes)} rampes en lignes au pas de '
                 '300 UU, chaque ligne sur un appui — rien au-dessus du trou ni de la plateforme verte', fontsize=10)
    ax.legend(loc='lower left', fontsize=8)
    fig.savefig(os.path.join(rep, 'plan_rampes.png'), dpi=80, bbox_inches='tight')
    plt.close(fig)


def plan_trou(rep, p, plans, trou, bord, releve):
    """Gauche : sol (plan 1, plateforme verte comprise), trou et relevé du joueur.
    Droite : détail du trou avec murs de bord et tourelles reposées face au gouffre."""
    plt, MPoly = _mpl()
    if not plt:
        return
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(22, 11))
    for ax in (ax1, ax2):
        for c_, x, y, Z, yaw, r in plans['sol'].lignes:
            if c_ in ('fond', 'fond_tri'):
                pc = dict(type='carre' if c_ == 'fond' else 'tri', x=x, y=y, yaw=yaw)
                vert = plateforme(r)
                coul = ('#2e9e4f' if vert else '#3f88c5' if int(r.split('anneau ')[1].split()[0]) >= p['anneau_ext']
                        else '#e07a2f')
                a = .85 if (Z or 0) == 0 else .5
                if ax is ax2 and not vert:
                    a = .25
                ax.add_patch(MPoly(polygone(pc), closed=True, fc=coul, ec='#333', lw=0.2, alpha=a))
        for pc in trou:
            ax.add_patch(MPoly(polygone(pc), closed=True, fc='#f4d4d0', ec='#c0392b', lw=0.6, ls='--'))
        if releve:
            pts = [(X, Y) for X, Y, Z, ok in releve[4]]
            ax.plot([x for x, y in pts], [y for x, y in pts], 'k.', ms=4)
        ax.plot(*ANCRE, 'k+', ms=14, mew=2)
    n_pla = sum(1 for l in plans['sol'].lignes if plateforme(l[5]))
    ax1.plot([], [], 's', color='#3f88c5', label='plan 1 : anneaux 12-15 (paliers plus clairs)')
    ax1.plot([], [], 's', color='#e07a2f', label='plan 1 : centre (anneaux 0-11)')
    ax1.plot([], [], 's', color='#2e9e4f', label=f'plan 1 : plateforme future ({n_pla} fondations, rien dessus)')
    ax1.plot([], [], 's', mfc='#f4d4d0', mec='#c0392b', label=f'trou : {len(trou)} fondations retirées')
    if releve:
        ax1.plot([], [], 'k.', label=f'relevé du joueur : {releve[1]}/{releve[2]} fondations retrouvées')
    ax1.plot([], [], 'k+', label='pilier de référence (0 ; 300)')
    ax1.set_aspect('equal')
    ax1.set_xlim(-5400, 5400)
    ax1.set_ylim(-5400, 5400)
    ax1.legend(loc='lower left', fontsize=9)
    ax1.set_title("Sol complet et trou à l'avant (relevé du joueur : blanc = retiré, vert = plateforme)")
    # détail du trou : contours D4 (pod), D5 (cage), D7 (rive) au niveau 0, murs de bord, tourelles
    def trait(ax, x, y, nu, **kw):
        nx, ny = vec(nu)
        dx, dy = -ny, nx
        ax.plot([x - 150 * dx, x + 150 * dx], [y - 150 * dy, y + 150 * dy], **kw)
    for cle, debut, coul in (('pod', 'pod niv0', '#555'), ('D5-D4', 'fut niv0', '#7d3c98'), ('D8-D7', 'rive niv0', 'k')):
        for c_, x, y, Z, yaw, r in plans[cle].lignes:
            if c_ in ('mur', 'cadre_double') and r.startswith(debut):
                trait(ax2, x, y, yaw, color=coul, lw=2)
    for x, y, nu, r, th in bord:
        trait(ax2, x, y, nu, color='#c0392b', lw=3)
        nx, ny = vec(nu)
        ax2.annotate(str(niveaux_bord_trou(p, r) + (r <= apo(4) + 1)), (x - 70 * nx, y - 70 * ny), fontsize=7,
                     ha='center', va='center')
    marq = {'heavy': ('s', '#c0392b'), 'tek': ('^', '#2471a3'), 'tesla': ('*', '#d4ac0d')}
    for cle in ('tourelles_ext', 'tourelles_d4'):
        for c_, x, y, Z, yaw, r in plans[cle].lignes:
            if c_ in marq:
                mk, co = marq[c_]
                ax2.plot(x, y, mk, color=co, ms=11 if 'TROU' in r else 7, mec='k', mew=1.6 if 'TROU' in r else .5)
    for c_, x, y, Z, yaw, r in plans['colonnade'].lignes:
        if c_ == 'pilier' and r.startswith('colonnade'):
            ax2.plot(x, y, '.', color='#6a040f', ms=2)
    for cle in ('D5-D4', 'toit_rampe'):
        for c_, x, y, Z, yaw, r in plans[cle].lignes:
            if r.startswith('casquette du trou'):
                nx, ny = vec(yaw + 90)
                ax2.plot([x - 150 * nx, x + 150 * nx], [y - 150 * ny, y + 150 * ny], color='#e67e22', lw=2.5)
    ax2.plot([], [], color='#e67e22', lw=2.5, label='casquette du trou (rampes : couloir Z2400, pod Z3000 ; plans 6 et 10)')
    ax2.plot([], [], color='#c0392b', lw=3, label='murs de bord du trou (chiffre = hauteur en murs, couronne comprise)')
    ax2.plot([], [], color='#555', lw=2, label='mur de pod D4')
    ax2.plot([], [], color='#7d3c98', lw=2, label='fût de cage D5')
    ax2.plot([], [], color='k', lw=2, label='mur de rive D7')
    ax2.plot([], [], 's', color='#c0392b', mec='k', label='Heavy (gros : reposée sur le bord du trou)')
    ax2.plot([], [], '^', color='#2471a3', mec='k', label='Tek (gros : reposée sur le bord du trou)')
    ax2.plot([], [], '*', color='#d4ac0d', mec='k', label='Tesla (gros : reposée sur le bord du trou)')
    xs = [x for pc in trou for x, y in polygone(pc)] or [-5400, 5400]
    ys = [y for pc in trou for x, y in polygone(pc)] or [-5400, 5400]
    ax2.set_aspect('equal')
    ax2.set_xlim(min(xs) - 700, max(xs) + 400)
    ax2.set_ylim(min(ys) - 400, max(ys) + 400)
    ax2.legend(loc='lower left', fontsize=9)
    ax2.set_title('Détail du trou : murs de bord autour du gouffre et de la plateforme ; tourelles face au gouffre')
    fig.savefig(os.path.join(rep, 'plan_trou_et_plans.png'), dpi=70, bbox_inches='tight')
    plt.close(fig)


def plan_couverture(rep, cov):
    """Carte de couverture : pour chaque zone d'approche et chaque direction (tous les 10°), nombre de tourelles Heavy
    et Tek qui voient le point (réglage High)."""
    plt, MPoly = _mpl()
    if not plt:
        return
    zones = list(cov)
    M = [[cov[z]['par_angle'].get(th, [0, -1])[1] for th in range(0, 360, 10)] for z in zones]
    fig, ax = plt.subplots(figsize=(16, 5.5))
    im = ax.imshow(M, aspect='auto', cmap='YlGn', vmin=0)
    for i, ligne in enumerate(M):
        for j, v in enumerate(ligne):
            ax.text(j, i, 'trou' if v < 0 else str(v), ha='center', va='center', fontsize=6 if v < 0 else 7,
                    color='#888' if v < 0 else '#b00' if v < 2 else '#222')
    ax.set_yticks(range(len(zones)))
    ax.set_yticklabels([f"{z} (r {cov[z]['rayon']:.0f}, Z {cov[z]['Z']:.0f})" for z in zones], fontsize=8)
    ax.set_xticks(range(36))
    ax.set_xticklabels([f'{th}°' for th in range(0, 360, 10)], fontsize=7, rotation=90)
    ax.set_xlabel("direction depuis le centre (θ ; le trou est à 180°)")
    fig.colorbar(im, ax=ax, label='tourelles Heavy / Tek (portée High, 6 000 UU)')
    ax.set_title("Couverture : nombre de tourelles qui voient chaque point d'approche (rouge : moins de 2)", fontsize=10)
    fig.savefig(os.path.join(rep, 'couverture.png'), dpi=80, bbox_inches='tight')
    plt.close(fig)


def verifier_rehausse(p, plans, reh):
    """La tour rehaussée d'un niveau : la rehausse se pose sur le haut de la tour (après les tourelles du périmètre)
    et les plans du haut, calés sur un mur de D4, montent de 300 UU. Refait les contrôles de collisions, d'appuis et
    d'ordre de pose sur cette configuration."""
    import copy
    haut = ('toiture_pleine', 'toit_rampe', 'tourelles_dessus')
    out = {}
    for cle, t in plans.items():
        if cle in haut and 'rehausse' not in out:
            out['rehausse'] = reh
        if cle not in haut:
            out[cle] = t
            continue
        u = Template(t.nom, t.description)
        for e, l_, meta in zip(t.entries, t.lignes, t.metas):
            e2 = copy.deepcopy(e)
            e2['loc']['z'] = round(e2['loc']['z'] + F, 3)
            u.entries.append(e2)
            u.lignes.append((l_[0], l_[1], l_[2], None if l_[3] is None else l_[3] + F, l_[4], l_[5]))
            u.phases.append(cle)
            u.groupes.append(cle)
            u.metas.append(meta)
        out[cle] = u
    admis = verifier_collisions(out, "tour rehaussée d'un niveau")
    appuis = verifier_appuis(out, p['appuis'])
    P, ordre, par = ordre_de_pose(out)
    return dict(entrees=len(reh.entries), pieces=reh.compte(), recouvrements_admis=admis,
                portee_max=appuis['portee_max'], montee_libre_max=appuis['montee_libre_max'])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--racine', default=RACINE)
    ap.add_argument('--debord', type=int, choices=(1, 2), default=P['debord'])
    ap.add_argument('--casquette', type=int, choices=(1, 2), default=1)
    ap.add_argument('--decaissement', type=float, default=150.0)
    ap.add_argument('--colonnade', type=float, default=P['colonnade_rayon'], help='rayon de la colonnade (UU)')
    ap.add_argument('--trou', default=P['trou'], help='fondations du trou (JSON : retirees / plateforme)')
    ap.add_argument('--appuis', choices=('stable', 'tours', 'prudent'), default=P['appuis'],
                    help="appuis des rampes : comme les tours avec des poteaux de stabilité (défaut), comme les tours, "
                         "ou un poteau au bout de chaque ligne montante")
    ap.add_argument('--verifier-481', metavar='JSON')
    a = ap.parse_args()
    p = dict(P, debord=a.debord, casquette=a.casquette, decaissement=a.decaissement, colonnade_rayon=a.colonnade,
             trou=a.trou, appuis=a.appuis)
    racine = os.path.abspath(a.racine)
    rep_t, rep_d, rep_p = (os.path.join(racine, d) for d in ('templates', 'donnees', 'plans'))
    for d in (rep_t, rep_d, rep_p):
        os.makedirs(d, exist_ok=True)
    if a.verifier_481 and not verifier_481(a.verifier_481):
        sys.exit('Le pavage ne correspond pas au template 481.')

    sol, pieces, contours, trou = module_sol(p)
    verifier_pavage(pieces)
    for m in (4, 5, 7, 8):
        aa, LL = contours[2 * m - 1]
        assert all(abs(x - apo(m)) < 1e-6 for x in aa) and all(l == m for l in LL), m
    releve = releve_trou(p)
    if releve:
        print(f'  Relevé du trou : rotation {releve[0]}°, {releve[1]}/{releve[2]} fondations retrouvées sur l\'étoile, '
              f'{releve[3]} dans le trou')
        assert releve[3] == 0, 'des fondations du relevé tombent dans le trou : revoir references/Trou_fondations.json'
    D = defense(p, contours)
    ordre = D['ordre']
    pod, infos_pod = module_pod(p, contours, D)
    rampe, murs, ob, jupe, col, bord = module_rampe(p, contours, D)
    cage, gal = module_cage(p, contours, D)
    toit, infos_toit = module_toit(p, contours)
    tourelles = module_tourelles(p, ordre)

    modules = [('sol', sol), ('pod', pod), ('rive', rampe), ('cage', cage), ('toit', toit), ('tourelles', tourelles)]
    conso = consolider_rampes(p, modules)
    print(f"  Rampes : {conso['retraits']} ; appuis : {conso['poteaux']} poteaux ({conso['pilier_fin']} piliers fins, "
          f"{conso['demi_pilier_fin']} demi-piliers fins), {conso['poutre_fine']} poutres fines, "
          f"{conso['raccourcies']} lignes raccourcies faute d'appui ; mode {p['appuis']} : {conso['stables']} lignes "
          f"montantes avec tous leurs poteaux de stabilité, {len(conso['stables_manquees'])} sans")
    infos_pod['Zsommet'] = max(Z + F for cle, x, y, Z, yaw, r in toit.lignes if cle == 'rampe' and r.startswith('toit'))
    col['colonnes'] = [c for c in col['colonnes'] if any(cle == 'pilier' and abs(x - c['x']) < 1 and abs(y - c['y']) < 1
                                                         for cle, x, y, Z, yaw, r in rampe.lignes)]
    verifier_encombrements(p, infos_pod, col, ordre)
    plans = assembler_plans(p, modules)
    verifier_plans(p, plans, modules)
    ordonner_plans(plans)
    admis = verifier_collisions(plans)
    appuis = verifier_appuis(plans, p['appuis'])
    reh = rehausse(p, contours)
    verif_reh = verifier_rehausse(p, plans, reh)
    chaume = chaume_a_demolir(plans, ordre)
    cov = couverture(p, ordre)
    for nom, c in cov.items():
        print(f"  Couverture {nom} : {c['min_high']} tourelles au moins (High), {c['min_medium']} (Medium), "
              f"moyenne {c['moyenne_high']}" + (f", faibles à {c['faibles_high']}" if c['faibles_high'] else ''))
    rep_plans = os.path.join(rep_t, 'plans')
    os.makedirs(rep_plans, exist_ok=True)
    for f_ in os.listdir(rep_plans):
        if f_.endswith('.json'):
            os.remove(os.path.join(rep_plans, f_))
    for cle, fichier, desc, ref in PLANS:
        plans[cle].ecrire(os.path.join(rep_plans, fichier + '.json'))
    reh.ecrire(os.path.join(rep_plans, 'Option_rehausse_pod_+1_niveau.json'))
    for vieux in ('phases', 'cage'):                 # anciens découpages (par hauteur, cage seule) : remplacés par les plans
        d_ = os.path.join(rep_t, vieux)
        if os.path.isdir(d_):
            for f_ in os.listdir(d_):
                os.remove(os.path.join(d_, f_))
            os.rmdir(d_)
    print('  Plans (≤ 2 000 entrées, chaque pièce après ce qui la porte) : ' +
          ', '.join(f'{fichier[:7]} {len(plans[cle].entries)}' for cle, fichier, *_ in PLANS)
          + f', rehausse {len(reh.entries)}')
    rep_test = os.path.join(rep_t, 'test')
    os.makedirs(rep_test, exist_ok=True)
    essai, hors = secteur_test(plans, portee_max=p['portee_plafond_max'])
    essai.ecrire(os.path.join(rep_test, 'Secteur_test_theta_-15_45.json'))
    fichiers = {cle: fichier for cle, fichier, *_ in PLANS}
    ecrire_csv(os.path.join(rep_d, '08_secteur_test.csv'),
               [(n, fichiers.get(pl, 'pile d\'ancrage'), NOMS.get(cle, cle), round(x, 1), round(y, 1),
                 '' if Z is None else round(Z, 1), rep_)
                for n, ((cle, x, y, Z, yaw, rep_), pl) in enumerate(zip(essai.lignes, essai.phases))],
               ['entree', 'plan', 'piece', 'x', 'y', 'Z_plan', 'repere'])
    print(f"  Secteur d'essai θ -15° → 45° : {len(essai.entries)} entrées (templates/test/), {hors} pièces retirées "
          "faute d'appui dans le secteur")
    essai_r, legende_r = essai_rampes()
    essai_r.ecrire(os.path.join(rep_test, 'Essai_rampes.json'))
    ecrire_csv(os.path.join(rep_d, '08_essai_rampes.csv'), legende_r, ['entree', 'variante', 'piece', 'repere'])
    essai_r2, legende_r2 = essai_rampes_2()
    essai_r2.ecrire(os.path.join(rep_test, 'Essai_rampes_2.json'))
    ecrire_csv(os.path.join(rep_d, '08_essai_rampes_2.csv'), legende_r2, ['entree', 'cas', 'piece', 'repere'])
    essai_r3, legende_r3 = essai_rampes_3()
    essai_r3.ecrire(os.path.join(rep_test, 'Essai_rampes_3.json'))
    ecrire_csv(os.path.join(rep_d, '08_essai_rampes_3.csv'), legende_r3, ['entree', 'cas', 'piece', 'repere'])
    equip = equipements(p, contours)

    # CSV de pose : un par plan, dans l'ordre des entrées du template
    for cle, fichier, desc, ref in PLANS:
        t = plans[cle]
        ecrire_csv(os.path.join(rep_d, fichier + '.csv'),
                   [(i, NOMS.get(c, c), round(x, 1), round(y, 1), '' if Z is None else round(Z, 1), round(yaw % 360, 1),
                     round(math.degrees(math.atan2(y, x)) % 360, 2), round(math.hypot(x, y), 1), r)
                    for i, (c, x, y, Z, yaw, r) in enumerate(t.lignes)],
                   ['entree', 'piece', 'x', 'y', 'Z_plan', 'yaw', 'theta', 'rayon', 'repere'])
    for f_ in os.listdir(rep_d):                      # CSV des anciens plans
        if f_.startswith('Plan_') and f_.endswith('.csv') and f_[:-4] not in {fi for _, fi, *_ in PLANS}:
            os.remove(os.path.join(rep_d, f_))
    ecrire_csv(os.path.join(rep_d, '05_matrice_tourelles.csv'),
               [(s['ordre'], s['priorite'], NOMS['crop_m' if s['couche'] == 'X-D4' else s['type']], s['couche'], s['plan'], s['cote'], s['idx'],
                 round(angle(s), 2), round(s['xm'], 1), round(s['ym'], 1), round(s['Zb'], 1), round(s['x'], 1),
                 round(s['y'], 1), round(s['Z'], 1), round(s['sortie'] % 360, 1)) for s in ordre],
               ['ordre', 'priorite', 'type', 'couche', 'plan', 'cote', 'index', 'theta', 'x_support', 'y_support',
                'Z_bas', 'x_tourelle', 'y_tourelle', 'Z_tourelle', 'sens_de_tir'])
    ecrire_csv(os.path.join(rep_d, '05_couverture.csv'),
               [(nom, c['rayon'], c['Z'], c['min_high'], c['min_medium'], c['moyenne_high'])
                + tuple(c['par_angle'].get(th, ['', 'trou'])[1] for th in range(0, 360, 10)) for nom, c in cov.items()],
               ['zone', 'rayon', 'Z', 'min_high', 'min_medium', 'moyenne_high'] + [f'{th}°' for th in range(0, 360, 10)])
    ecrire_csv(os.path.join(rep_d, '07_equipements.csv'),
               [(n, NOMS[q['cle']], q['lieu'], round(q['x'], 1), round(q['y'], 1), q['Z'], round(q['yaw'] % 360, 1))
                for n, q in enumerate(equip)],
               ['n', 'equipement', 'lieu', 'x', 'y', 'Z_plan', 'yaw'])
    pics = [(x + 150 * vec(nu)[0], y + 150 * vec(nu)[1], nu, k, i) for x, y, nu, k, i in murs]
    pics = [m for m in pics if not dans_trou(p, m[0], m[1])]
    ecrire_csv(os.path.join(rep_d, '03_ligne_pics.csv'),
               [(n, round(x, 1), round(y, 1), -p['decaissement'], nu, k, i) for n, (x, y, nu, k, i) in enumerate(pics)],
               ['n', 'x', 'y', 'Z_plan', 'yaw', 'cote', 'index'])
    ecrire_csv(os.path.join(rep_d, '03_colonnade.csv'),
               [(n, round(c['theta'], 3), round(c['x'], 1), round(c['y'], 1), len(c['elements']),
                 sum(1 for e in c['elements'] if e[0] == 'pilier'), sum(1 for e in c['elements'] if e[0] == 'demi_pilier'),
                 round(c['sommet'], 1), round(c['toit'], 1)) for n, c in enumerate(col['colonnes'])],
               ['n', 'theta', 'x', 'y', 'pieces', 'piliers', 'demi_piliers', 'Z_sommet', 'Z_toit'])
    ecrire_csv(os.path.join(rep_d, '08_chaume_a_demolir.csv'),
               [(c['ordre'], c['plan'], c['entree'], c['couche'], c['tourelle'], round(c['x'], 1), round(c['y'], 1),
                 round(c['Z_bas'], 1), c['dessus']) for c in chaume],
               ['ordre_de_pose', 'plan', 'entree_json', 'couche', 'tourelle_portee', 'x', 'y', 'Z_bas', 'pose_au_dessus'])
    ecrire_csv(os.path.join(rep_d, '06_bord_du_trou.csv'),
               [(n, round(x, 1), round(y, 1), round(nu, 1), round(r, 1), round(th, 2), niveaux_bord_trou(p, r)
                 + (1 if r <= apo(4) + 1 else 0)) for n, (x, y, nu, r, th) in enumerate(bord)],
               ['n', 'x', 'y', 'yaw_vers_le_trou', 'rho', 'theta', 'hauteur_murs'])

    # synthèse
    dmax, rmax = distances(ordre)
    syn = {'parametres': {k: v for k, v in p.items()}, 'apothemes': {f'D{m}': round(apo(m), 1) for m in range(1, 9)},
           'rayons_coins': {f'D{m}': round(rayon_coin(m), 1) for m in range(1, 9)},
           'overhang': ob, 'jupe': jupe, 'Z_haut_tour': infos_pod['Zpod'], 'Z_plancher_toit': infos_toit['Ztoit'],
           'Z_sommet_toit': infos_pod['Zsommet'],
           'murs_de_reference': {c: dict(cote=k, index=i, theta=30 * k, x=round(next(
               x for x, y, nu, kk, ii in cotes_contour(contours[p['anneau_pod']]) if (kk, ii) == (k, i)), 1))
               for c, (k, i) in REF_MURS.items()},
           'paliers_bord': [dict(anneau=p['anneau_rive'] + i + 1, apo_E0_int=round(a, 1), apo_E0_ext=round(b, 1), Z=Z)
                            for i, (a, b, Z) in enumerate(paliers_bord(p))],
           'trou': {'fondations_retirees': {'carres': sum(1 for pc in trou if pc['type'] == 'carre'),
                                            'triangles': sum(1 for pc in trou if pc['type'] == 'tri'),
                                            'par_anneau': {a_: sum(1 for pc in trou if pc['anneau'] == a_)
                                                           for a_ in sorted({pc['anneau'] for pc in trou})}},
                    'plateforme': sorted(list(k) for k in charger_trou(p)['plateforme']),
                    'murs_de_bord': {'aretes': len(bord), 'murs': sum(niveaux_bord_trou(p, r) + (r <= apo(4) + 1)
                                                                       for *_, r, th in bord)},
                    'releve': None if not releve else {'rotation': releve[0], 'retrouvees': releve[1],
                                                       'total': releve[2], 'dans_le_trou': releve[3]}},
           'tourelles': {'posees': D['poses'], 'reserve': D['reserve'], 'L1': D['n_L1'],
                         'par_couche': {cch: {ty: sum(1 for s in ordre if s['couche'] == cch and s['type'] == ty)
                                              for ty in ('heavy', 'tek', 'tesla', 'crop')
                                              if any(s['couche'] == cch and s['type'] == ty for s in ordre)}
                                        for cch in dict.fromkeys(s['couche'] for s in ordre)},
                         'par_plan': {pl: {ty: sum(1 for s in ordre if s['plan'] == pl and s['type'] == ty)
                                           for ty in ('heavy', 'tek', 'tesla', 'crop')}
                                      for pl in ('ext', 'd4', 'dessus')}},
           'cap': {'distance_max_entre_tourelles': round(dmax, 1), 'rayon_max_tourelle': round(rmax, 1),
                   'distance_min_avant_poste': round(10000 + rmax, 1)},
           'secteurs': secteurs(p, ob, jupe),
           'couverture': {nom: {k: v for k, v in c.items() if k != 'par_angle'} for nom, c in cov.items()},
           'colonnade': {k: (round(v, 3) if isinstance(v, float) else v) for k, v in col.items() if k != 'colonnes'},
           'escalier': {**infos_pod['escalier'], 'marches': int(p['mezzanine'] // F)},
           'tremie': [dict(anneau=pc['anneau'], type=pc['type'], x=round(pc['x'], 1), y=round(pc['y'], 1))
                      for pc in infos_pod['tremie']],
           'pics': {'nombre': len(pics), 'apotheme_ligne': round(apo(7) + 150, 1), 'Z': -p['decaissement']}}
    syn['constructibilite'] = {
        'rampes_retirees': conso['retraits'], 'lignes_raccourcies_faute_d_appui': conso['raccourcies'],
        'appuis': {'poteaux': conso['poteaux'], 'piliers_fins': conso['pilier_fin'],
                   'demi_piliers_fins': conso['demi_pilier_fin'], 'poutres_fines': conso['poutre_fine'],
                   'lignes_stables': conso['stables'], 'lignes_sans_tous_leurs_poteaux': conso['stables_manquees']},
        'controle_appuis': appuis, 'recouvrements_admis': admis, 'rehausse': verif_reh,
        'chaume_a_demolir': {'total': len(chaume), 'par_plan': {pl: sum(1 for c in chaume if c['plan'] == pl)
                                                               for pl in sorted({c['plan'] for c in chaume})},
                             'pose_au_dessus': {d: sum(1 for c in chaume if c['dessus'] == d)
                                                for d in sorted({c['dessus'] for c in chaume})}}}
    syn['colonnade']['colonnes'] = len(col['colonnes'])
    syn['colonnade']['pieces'] = sum(len(c['elements']) for c in col['colonnes'])
    syn['anneaux'] = tableau_anneaux(p)
    syn['gabarits'] = [dict(nom=n, theta=th, apotheme=A, largeur=lg, profondeur=pf, hauteur_murs=hm,
                            x=round(A * vec(th)[0], 1), y=round(A * vec(th)[1], 1))
                       for n, th, A, lg, pf, hm in GABARITS]
    syn['noyau'] = [dict(nom=n, equipement=NOMS[c], theta=th, x=round(A_NOYAU * vec(th)[0], 1),
                         y=round(A_NOYAU * vec(th)[1], 1), Z=0.0, cage=f'{CAGE_NIVEAUX} murs + plafond')
                    for n, th, c in NOYAU]

    def sans_ancre(t):
        c = {}
        for cle, *_, r in t.lignes:
            if not r.startswith('ancre'):
                c[cle] = c.get(cle, 0) + 1
        return c

    syn['limites_moteur'] = verifier_limites(p, plans, len(pics), len(equip))
    syn['plans'] = {}
    structure = {}
    for cle, fichier, desc, ref in PLANS:
        c = sans_ancre(plans[cle])
        syn['plans'][fichier] = {'total': sum(c.values()), 'entrees': len(plans[cle].entries), 'reference': ref,
                                 'pieces': c, 'bilan': bilan({k: v for k, v in c.items()
                                                              if k not in ('heavy', 'tek', 'tesla')})}
        if cle == 'colonnade':
            continue                           # option : hors du bilan de base
        for k, v in c.items():
            structure[k] = structure.get(k, 0) + v
    syn['options'] = {'colonnade': syn['plans']['Plan_02_colonnade_option'],
                      'rehausse_par_niveau': {'total': len(reh.entries), 'pieces': reh.compte(),
                                              'bilan': bilan(reh.compte())}}
    tourelles_n = {k: structure.pop(k, 0) for k in ('heavy', 'tek', 'tesla')}
    cultures_n = {k: structure.pop(k) for k in ('crop', 'crop_m') if k in structure}
    chaume_n = {'chaume_mur': structure.pop('chaume_mur', 0)}
    nb_eq = {}
    for q in equip:
        nb_eq[q['cle']] = nb_eq.get(q['cle'], 0) + 1
    nb_ancres = sum(1 for cle, t in plans.items() if cle != 'colonnade' for *_, r in t.lignes if r.startswith('ancre'))
    postes = {'structure': structure, 'cultures': cultures_n, 'tourelles_chaume': chaume_n, 'tourelles': tourelles_n,
              'ancres_temporaires': {'demi_pilier': nb_ancres}, 'pics': {'pics': len(pics)}, 'equipements': nb_eq}
    syn['bilan_complet'] = {nom: {'pieces': c, 'bilan': bilan(c)} for nom, c in postes.items()}
    tot_sans, tot_avec = {}, {}
    for nom, v in syn['bilan_complet'].items():
        for r, q in v['bilan'].items():
            tot_avec[r] = tot_avec.get(r, 0) + q
            if nom != 'tourelles':
                tot_sans[r] = tot_sans.get(r, 0) + q
    syn['bilan_total'] = {'sans_tourelles': tot_sans, 'avec_tourelles': tot_avec,
                          'brut_sans_tourelles': bilan_brut(tot_sans), 'brut_avec_tourelles': bilan_brut(tot_avec)}
    with open(os.path.join(rep_d, 'synthese.json'), 'w', encoding='utf-8') as f:
        json.dump(syn, f, ensure_ascii=False, indent=1)
    appuis_pts = [(c, x, y, Z, Z + (F if c == 'pilier_fin' else F / 2 if c == 'demi_pilier_fin' else 0))
                  for t in plans.values() for c, x, y, Z, yaw, r in t.lignes if r.startswith('appui')]
    plans_png(rep_p, p, pieces, ordre, ob, jupe, infos_pod, col, trou, appuis_pts)
    plan_pod(rep_p, p, infos_pod)
    plan_rampes(rep_p, p, modules)
    plan_trou(rep_p, p, plans, trou, bord, releve)
    plan_couverture(rep_p, cov)

    print(json.dumps({v: syn['plans'][v]['entrees'] for v in syn['plans']}, indent=1))
    print(json.dumps(syn['tourelles'], indent=1, ensure_ascii=False))
    print(json.dumps(syn['cap'], indent=1), syn['secteurs'])


if __name__ == '__main__':
    main()
