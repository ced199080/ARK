#!/usr/bin/env python3
"""Générateur de la forteresse circulaire Ø30 sur Metal Cliff Platform (ARK: Survival Ascended).

Produit, à partir d'une seule géométrie paramétrée :
  - les templates Template Hammer (JSON, même schéma que les exports Wikily.gg), en 8 plans : sol des anneaux 12-15,
    murs / rampes / tourelles des anneaux 12-15, puis sol, pod, cage, toit et tourelles du centre, et la petite
    plateforme du trou,
  - l'adaptation au trou (gouffre) à l'avant : fondations relevées sur l'image annotée (references/Trou_fondations.json),
    recalées sur le relevé en jeu references/Trou_points_ancrage.json,
  - les tableaux de coordonnées (CSV) pour la pose manuelle,
  - la matrice des tourelles (scénario B : cap 100, Tesla comptées) avec ordre de pose et murs de chaume de pose,
  - le bilan matières,
  - la liste des murs de chaume à démolir en jeu (donnees/08_chaume_a_demolir.csv),
  - les plans PNG (si matplotlib est installé).
Avant d'écrire, il contrôle la constructibilité : rien au-dessus du trou, aucune pièce qui en traverse une autre
(verifier_collisions), chaque rampe tenue par ses appuis comme sur les tours 1201 / 1809 (verifier_appuis).

Usage :
    python3 outils/forteresse.py                       # tout régénérer
    python3 outils/forteresse.py --debord 1            # overhang d'une seule structure au-delà de la plateforme
    python3 outils/forteresse.py --colonnade 3600      # rayon de la colonnade circulaire
    python3 outils/forteresse.py --trou autre.json     # autre relevé du trou (retirees / plateforme)
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
    porte-à-faux, comme sur les tours ; voir consolider_rampes().
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
    cage_niveaux=2,            # étages de la cage
    casquette=1,               # rangs de casquette en porte-à-faux devant la cage
    debord=2,                  # rangs de rampes dans le vide, accrochés à la jupe (1 ou 2)
    pod_niveaux=8,             # hauteur du mur de pod (murs) -> Z 2400 = toit de cage (plancher de toit commun)
    mezzanine=1800.0,          # plancher technique du pod = sol de la galerie L1 (6 murs libres dessous)
    jupe=True,                 # jupe basse sous l'overhang (tourelles sous la plateforme)
    colonnade_rayon=3600.0,    # colonnade circulaire sous la pente A, entièrement sur les anneaux 12-13
    # trou (gouffre) à l'avant : fondations retirées (blanc) et petite plateforme (vert), relevées sur l'image annotée
    anneau_ext=12,             # anneaux 12 à 15 : plans 1 et 2 ; anneaux 0 à 11 : plans du centre
    trou='references/Trou_fondations.json',
    trou_releve='references/Trou_points_ancrage.json',     # points d'ancrage posés en jeu (export Template Hammer)
    colonnade_hauteur=300.0,   # 1 pilier de haut, comme les cercles de piliers 704 / 701 (au lieu de monter sous la pente)
    largeur_pilier=2 * math.pi * 600 / 96,   # 39,27 UU : 48 piliers à r=600 (template 704) = 1 pilier / 1 vide
    colonnade_passages=(30, 90, 150, 210, 270, 330),   # 1 passage par part (axe des portes du fût)
    colonnade_largeur_passage=300.0,
    appuis='tours',            # appuis des rampes : 'tours' (comme les tours 1201 / 1809) ou 'prudent' (poteau en bout)
    cap=100, tesla_comptee=True,             # scénario B retenu
    inventaire=(80, 35, 10),                 # Heavy, Tek, Tesla disponibles
)
ANCRE = (0.0, F)               # sommet de l'hexagone central à θ = 90° : pilier de référence de tous les plans
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
    'replicateur': 'Réplicateur Tek', 'forge_vapeur': 'Forge à vapeur (Steam Forge)',
    'megalab': 'Labo de fortune (Makeshift Megalab)', 'stockage_dedie': 'Stockage dédié Tek (Tek Dedicated Storage)',
    'coffre_fort': 'Coffre-fort (Vault)', 'generateur_tek': 'Générateur Tek',
}

# Coût unitaire : MI=lingot de métal, PC=pâte cimentée, EL=électroniques, PO=polymère, CR=cristal, EM=élément,
# CU=cuir, FI=fibre, CH=chaume, BO=bois. est=True : estimation (pièce absente des sources consultées).
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
    ou t = ±150, ±450… (demi=True : sur les joints des murs, comme les lignes de rampes des tours, ce qui laisse le
    milieu des murs libre pour les tourelles). Chaque ligne part de l'ancre et s'arrête à la première lame au-dessus
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
    """Hauteur (en murs) d'un mur de bord du trou : il ferme la coupe jusqu'à l'enveloppe.

    Dans la cage et le pod (ρ ≤ D5) : jusqu'au plancher de toit Z2400. Au-delà : jusque sous la pente A, au moins la
    hauteur de la rive.
    """
    if r <= apo(5) + 1:
        return p['pod_niveaux']
    z_pente = p['rive_niveaux'] * F + apo(7) - r
    return max(p['rive_niveaux'], math.ceil((z_pente - 1) / F))


def groupe_bord(p, r):
    """Plan d'un mur de bord du trou : anneaux 12-13 -> plan 2 ; couloir et attique -> plan 5 (cage) ; pod -> plan 4."""
    if r > apo(6) + 1:
        return 'ext'
    return 'cage' if r > apo(4) + 1 else 'pod'


def bande(x0, y0, ang, long, larg=20.0):
    """Rectangle mince (lame de rampe, mur vu de dessus) partant de (x0, y0) dans la direction ang."""
    nx, ny = vec(ang)
    dx, dy = -ny * larg / 2, nx * larg / 2
    x1, y1 = x0 + long * nx, y0 + long * ny
    return [(x0 - dx, y0 - dy), (x1 - dx, y1 - dy), (x1 + dx, y1 + dy), (x0 + dx, y0 + dy)]


def casquette_trou(p):
    """Casquette du bord du trou : la toiture en rampes se prolonge au-dessus du gouffre, comme la casquette de D5.

    Une lame par mur de bord qui monte jusqu'au plancher de toit (Z2400) : elle part du haut du mur et descend de
    300 UU vers le gouffre (Z2400 -> 2100), au-dessus des tourelles reposées face au trou. Les lames qui
    croiseraient un mur de bord, la casquette de D5 ou une autre lame (angles rentrants du trou) ne sont pas posées.
    Renvoie [(x pivot, y pivot, normale vers le trou, θ)].
    """
    hauts = [m for m in bords_trou(p) if niveaux_bord_trou(p, m[3]) == p['pod_niveaux']]
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
        L = bande(x, y, nu, F)
        if any(se_coupent(L, o) for o in obstacles + lames + murs[:j] + murs[j + 1:]):
            continue
        lames.append(L)
        out.append((x + 150 * vec(nu)[0], y + 150 * vec(nu)[1], nu, th))
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


def volume(cle, x, y, z, yaw, noyau=False):
    """Volume d'une pièce posée (z : cote template), ou son noyau. None : pièce non contrôlée."""
    c = 1.0 if noyau else 0.0
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

    def ajouter(self, ref, cle, x, y, z, yaw):
        S = volume(cle, x, y, z, yaw)
        if S is None:
            return
        self.p[ref] = (cle, x, y, S, volume(cle, x, y, z, yaw, noyau=True))
        for c in self._cases(S):
            self.grille.setdefault(c, set()).add(ref)

    def retirer(self, ref):
        if ref in self.p:
            for c in self._cases(self.p[ref][3]):
                self.grille[c].discard(ref)
            del self.p[ref]

    def heurts(self, ref, piece=None, seuil=0.5):
        """Refs en collision avec la pièce `ref` (ou avec `piece` = (cle, x, y, z, yaw) pas encore posée)."""
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
            if {cle, c2} & {'heavy', 'tek', 'tesla'} and 'chaume_mur' in (cle, c2) and math.hypot(x - x2, y - y2) < 15:
                continue                               # une tourelle et son mur de chaume de pose
            if max(K.penetre(S2), S.penetre(K2)) > seuil:
                out.append(r)
        return out


def surfaces(modules):
    """Dessus des fondations et des plafonds posés (hors plateforme verte, où rien n'est accroché) : (poly, z template)."""
    out = []
    for _, m in modules:
        for e, (cle, *_), gr in zip(m.entries, m.lignes, m.groupes):
            if cle in ('fond', 'fond_tri', 'plafond', 'plafond_tri', 'trappe') and gr != 'plateforme':
                l, r = e['loc'], e['rot']
                poly = polygone(dict(type='tri' if cle.endswith('_tri') else 'carre', x=l['x'], y=l['y'], yaw=r['yaw']))
                out.append((poly, l['z'] + (50 if cle.startswith('fond') else 0)))
    return out


def dessus_sous(surf, x, y, z):
    """Cote template de la plus haute surface sous le point (x, y, z), ou None (vide, trou)."""
    hauts = [zt for poly, zt in surf if zt <= z + 1 and _dans_poly(poly, x, y, -1.0)]
    return max(hauts) if hauts else None


APPUI_LIGNES = {'toit': 'poteau', 'casquette': 'poteau', 'pente A': 'poteau', 'overhang': 'poteau', 'debord': 'poutre',
                'casquette du trou': None}
MONTANTES = ('toit', 'pente A')          # lignes ancrées en bas, qui montent ; les autres pendent de leur ancrage
PORTEE_MAX = 7                 # lames entre deux appuis (tour 1809 : 7 lames de la poutre d'égout au poteau de faîtage)
LIBRE_MAX = 6                  # lames montantes au-dessus du dernier appui, bout haut libre (tours 1201 et 1809 : 6)


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
       - 'prudent' : en plus, chaque ligne montante finit sur un poteau sous son bout haut (poteau de faîtage).
       Poteau : piliers fins debout sur le plancher ou la fondation sous la jonction. Débord dans le vide : poutre fine
       posée sur le niveau bas de la jupe. Une ligne qu'on ne peut pas appuyer est raccourcie.
    Renvoie un résumé chiffré.
    """
    E = Encombrement()
    info = {}
    for mi, (_, m) in enumerate(modules):
        for e, (cle, *_, rep_), meta in zip(m.entries, m.lignes, m.metas):
            l, r = e['loc'], e['rot']
            E.ajouter(id(e), cle, l['x'], l['y'], l['z'], r['yaw'])
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
    stats = {'poteaux': 0, 'pilier_fin': 0, 'demi_pilier_fin': 0, 'poutre_fine': 0, 'raccourcies': 0}

    def jonctions(key, n):
        out = []
        for j, ref in lignes[key][:n]:
            l, r = lames_ent[ref]['loc'], lames_ent[ref]['rot']
            bas, haut = bouts_lame(l['x'], l['y'], l['z'], r['yaw'])
            ancre_, loin = (bas, haut) if key[0] not in ('casquette', 'overhang', 'debord') else (haut, bas)
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
        return out if all(not E.heurts(None, piece=q) for q in out) else None

    def poutre(key, J0, J1):
        # poutre fine couchée de J0 à J1, à la cote de J1, posée sur un mur dont le haut est à cette cote sous J0
        if not any(abs(zt - J1[2]) < 2 and abs((J0[0] - xm) * vec(yw)[0] + (J0[1] - ym) * vec(yw)[1]) < 15
                   and abs(-(J0[0] - xm) * vec(yw)[1] + (J0[1] - ym) * vec(yw)[0]) <= F / 2 + 1
                   for xm, ym, zt, yw in murs_hauts):
            return None
        q = ('poutre_fine', (J0[0] + J1[0]) / 2, (J0[1] + J1[1]) / 2, J1[2], 30 * key[1] + 90)
        return [q] if not E.heurts(None, piece=q) else None

    def besoins(key, m):
        """Jonctions à appuyer (n° depuis l'ancrage, 0 = ancrage), de la solution la plus légère à la plus lourde."""
        if key[0] in MONTANTES and p['appuis'] == 'tours':
            if m <= LIBRE_MAX:
                return [[]]
            return [[j] for j in range(max(1, m - LIBRE_MAX), min(m, PORTEE_MAX) + 1)]
        if m <= 1:
            return [[]]
        out = []
        for jf in (m, m - 1):
            out += ([[jf, jm] for jm in (jf // 2, jf // 2 - 1, jf // 2 + 1)] if jf > PORTEE_MAX else [[jf]])
        return out

    for key in sorted(lignes):
        regle = APPUI_LIGNES[key[0]]
        while limite[key] > 1 and regle:
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
    # écriture : lames retirées, appuis ajoutés (avant les rampes : ils sont posés d'abord)
    for mi, (_, m) in enumerate(modules):
        m.retirer([i for i, e in enumerate(m.entries) if id(e) in retraits])
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


# Recouvrements admis : la pile d'ancrage est plantée au sommet commun de fondations (comme les cercles de
# fondations 2901-2903) ; le niveau bas de la jupe pend sous le bord de l'anneau 15, contre la tranche des fondations.
def _admis(a, b):
    for u, v in ((a, b), (b, a)):
        if u[7].startswith('ancre') and v[2] in ('fond', 'fond_tri'):
            return 'ancre'
        if u[7].startswith('jupe mur niv0') and v[2] in ('fond', 'fond_tri'):
            return 'jupe sous la plateforme'
    return None


def verifier_collisions(plans):
    """Aucune pièce des 8 plans n'entre dans une autre (noyau contre volume), hors recouvrements admis."""
    P_ = _pieces_plans(plans)
    E = Encombrement()
    for n, q in enumerate(P_):
        E.ajouter(n, q[2], q[3], q[4], q[5], q[6])
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
    print(f"  Collisions : aucune sur {len(P_)} pièces (recouvrements admis : "
          + ', '.join(f'{k} {v}' for k, v in sorted(admis.items())) + ')')
    return admis


def _dist_seg(px, py, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    u = max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - x1 - u * dx, py - y1 - u * dy)


def verifier_appuis(plans, mode='tours'):
    """Chaque rampe inclinée tient comme sur les tours 1201 / 1809 : ses lames s'enchaînent bout à bout en lignes ; une
    jonction est appuyée si elle repose sur le haut d'un mur ou d'un cadre métal (pas de chaume : il est démoli), sur le
    bord d'un plancher ou d'une fondation (pas la plateforme verte), sur la tête d'un pilier ou sur le bout d'une poutre
    fine. Une lame doit être entre deux appuis distants d'au plus 7 lames, ou pendre d'un appui qu'elle touche
    (porte-à-faux d'une seule lame), ou monter librement au plus 6 lames au-dessus d'un appui (mode 'tours' ; en mode
    'prudent', une seule). Renvoie les statistiques des lignes."""
    P_ = _pieces_plans(plans)
    seg, pts = [], []
    for cle_p, n, cle, x, y, z, yaw, rep_ in P_:
        if cle in ('mur', 'cadre_double'):
            lx, ly = vec(yaw + 90)
            seg.append((x - F / 2 * lx, y - F / 2 * ly, x + F / 2 * lx, y + F / 2 * ly, z + F / 2))
        elif cle in ('fond', 'fond_tri', 'plafond', 'plafond_tri', 'trappe') and cle_p != 'plateforme':
            poly = polygone(dict(type='tri' if cle.endswith('_tri') else 'carre', x=x, y=y, yaw=yaw))
            zt = z + (50 if cle.startswith('fond') else 0)
            seg += [(*poly[i], *poly[(i + 1) % len(poly)], zt) for i in range(len(poly))]
        elif cle in ('pilier', 'pilier_fin', 'demi_pilier', 'demi_pilier_fin') and not rep_.startswith('ancre'):
            pts.append((x, y, z + (F / 4 if cle.startswith('demi') else F / 2)))
        elif cle == 'poutre_fine':
            lx, ly = vec(yaw + 90)
            pts += [(x - F / 2 * lx, y - F / 2 * ly, z), (x + F / 2 * lx, y + F / 2 * ly, z)]

    def appuye(q):
        return (any(abs(q[2] - zt) < 12 and _dist_seg(q[0], q[1], x1, y1, x2, y2) < 15 for x1, y1, x2, y2, zt in seg)
                or any(abs(q[2] - c[2]) < 12 and math.hypot(q[0] - c[0], q[1] - c[1]) < 25 for c in pts))

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
    libre_max = LIBRE_MAX if mode == 'tours' else 1
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
    print(f'  Appuis ({mode}) : {len(lames)} rampes ; portée maxi entre appuis {max(portees)} lames, {consoles} pendues '
          f'd\'une lame à leur appui, montée libre maxi {max(libres)} lames')
    return dict(mode=mode, rampes=len(lames), portee_max=max(portees), pendues=consoles, montee_libre_max=max(libres),
                montantes_libres=len(libres) - 1)


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
        out.append(dict(plan=next(f[:6] for k, f, _ in PLANS if k == q[0]), entree=q[1], ordre=s_['ordre'], couche=s_['couche'], tourelle=NOMS[s_['type']],
                        x=q[3], y=q[4], Z_bas=q[5] - Z_TPL - F / 2, dessus=NOMS[dessus[0]] if dessus else 'rien'))
    return sorted(out, key=lambda c: c['ordre'])


def cellule_escalier(x0, y0, yaw):
    """Emprise 300 × 300 de la colonne d'escaliers (axes = yaw de l'escalier)."""
    nx, ny = vec(yaw)
    dx, dy = -ny, nx
    return [(x0 + u * nx + v * dx, y0 + u * ny + v * dy) for u, v in ((-150, -150), (150, -150), (150, 150), (-150, 150))]


# ---------------------------------------------------------------- modules
def module_sol(p):
    """Pavage sans les fondations du trou : anneaux 12 à 15 -> plan 1, centre et anneaux 1 à 11 -> plan 3,
    petite plateforme verte -> plan 8."""
    pieces, contours = pavage(p['anneaux_total'])
    t = Template('01 Sol', 'Pavage carres+triangles en etoile, Ø30 (D8), sans les fondations du trou. Bord abaisse en 2 '
                           f"paliers : anneau 14 (Ø26-Ø28) a -{p['decaissement']:.0f} UU, anneau 15 (Ø28-Ø30) a "
                           f"-{2 * p['decaissement']:.0f} UU. Origine = centre de l'etoile.")
    ancre(t, empilee=True)
    t.phase = 'P1'
    trou = []
    for pc in pieces:
        if piece_dans_trou(p, pc):
            trou.append(pc)
            continue
        t.groupe = ('plateforme' if piece_plateforme(p, pc) else 'sol_ext' if pc['anneau'] >= p['anneau_ext']
                    else 'sol_centre')
        Z = cote_anneau(p, pc['anneau'])
        cle = 'fond' if pc['type'] == 'carre' else 'fond_tri'
        t.add(cle, pc['x'], pc['y'], Z + Z_TPL - 50, pc['yaw'], Z=Z,
              repere=f"anneau {pc['anneau']} cote {pc['cote']} n{pc['idx']}")
    return t, pieces, contours, trou


def module_pod(p, contours):
    t = Template('02 Pod central atelier', 'Mur de pod D4 (48 murs/niveau), colonne d\'escaliers jusqu\'a la mezzanine, '
                                         'piliers porteurs, mezzanine Z1800, plancher de toit Z2400 et toit en rampes '
                                         'inclinees (tours 1201/1809) sur toute la cage D5.')
    ancre(t)
    d4 = contours[p['anneau_pod']]
    zmez = p['mezzanine']
    t.groupe = 'pod'
    # colonne d'escaliers du hall à la mezzanine (à l'ancienne place de l'escalier du Coeur Base)
    xe, ye, yawe = ESCALIER
    for niv in range(int(zmez // F)):
        t.phase = 'P2' if niv == 0 else 'P3'
        t.add('escalier', xe, ye, niv * F + Z_TPL + F / 2, yawe, Z=niv * F, repere=f'escalier niv{niv}')
    # mur de pod : niveaux 0..7 ; 1 porte double au sol par part (côtés E1, index 1) et accès galerie Z1800 (index 1)
    Ztop = p['pod_niveaux'] * F
    assert Ztop == zmez + p['cage_niveaux'] * F, "le mur de pod doit finir au niveau du toit de cage"
    for niv in range(p['pod_niveaux']):
        Zb = niv * F
        t.phase = 'P2' if Zb < zmez else 'P6'
        for x, y, nu, k, i in cotes_contour(d4):
            cle = 'mur'
            if niv == 0 and k % 2 == 1 and i == 1:
                cle = 'cadre_double'
            if Zb == zmez and i == 1:
                cle = 'cadre_double'
            if dans_trou(p, x, y, bord=True):
                continue                       # coupé par le trou : le mur de bord du trou ferme le pod
            t.add(cle, x, y, Zb + Z_TPL + F / 2, nu, Z=Zb, repere=f'pod niv{niv} c{k} p{i}')
    # piliers : couronne PA aux sommets de D2 (Z0 -> 2400), couronne PB aux sommets de D1 (mezzanine -> 2400)
    for nom, n, Zb, Zh in (('PA', 2, 0.0, Ztop), ('PB', 1, zmez, Ztop)):
        R = rayon_coin(n)
        for k in range(12):
            cx, cy = vec(15 + 30 * k)
            if dans_trou(p, R * cx, R * cy):
                continue
            Z = Zb
            while Z + F <= Zh + 1e-6:
                t.phase = 'P2' if Z < zmez else 'P6'
                t.add('pilier', R * cx, R * cy, Z + Z_TPL + F / 2, 0, Z=Z, repere=f'pilier {nom}{k}')
                Z += F
    # mezzanine Z1800 : centre + anneaux 1..7 en plafonds, trémie = pièces traversées par la colonne d'escaliers
    cellule = cellule_escalier(xe, ye, yawe)
    pieces, _ = pavage(p['anneau_pod'], centre=True)
    t.phase = 'P3'
    tremie = []
    for pc in pieces:
        if se_coupent(polygone(pc), cellule):
            tremie.append(pc)
            continue
        if piece_dans_trou(p, pc):
            continue
        cle = 'plafond' if pc['type'] == 'carre' else 'plafond_tri'
        t.add(cle, pc['x'], pc['y'], zmez + Z_TPL, pc['yaw'], Z=zmez, repere=f"mezzanine anneau {pc['anneau']}")
    # plancher de toit Z2400 (centre + anneaux 1..7, sans trémie) puis toit en rampes sur tout le bloc central (D5)
    t.groupe = 'toit'
    t.phase = 'P6'
    for pc in pieces:
        if piece_dans_trou(p, pc):
            continue
        cle = 'plafond' if pc['type'] == 'carre' else 'plafond_tri'
        t.add(cle, pc['x'], pc['y'], Ztop + Z_TPL, pc['yaw'], Z=Ztop, repere=f"plancher de toit anneau {pc['anneau']}")
    pente(t, 'toit', apo(5), Ztop, +1, 'toit rampes', filtre=lambda x, y: dans_trou(p, x, y))
    # casquette du bord du trou : au-dessus des murs de bord qui montent jusqu'au plancher de toit
    for n, (x, y, nu, th) in enumerate(casquette_trou(p)):
        t.add('rampe', x, y, Ztop - F + Z_TPL + 200, nu - 90, Z=Ztop - F, repere=f'casquette du trou θ{th:.1f}',
              meta=dict(sys='casquette du trou', k=n, t=0.0, rang=0, sens=-1))
    t.groupe = 'pod'
    # Zsommet : recalculé après consolidation des rampes (lames en collision retirées)
    return t, dict(Zsommet=Ztop + apo(5) - 50, Ztoit=Ztop, escalier=dict(x=xe, y=ye, yaw=yawe), cellule=cellule,
                   tremie=tremie)


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


def module_rampe(p, contours, tesla_murs):
    t = Template('03 Rive, colonnade, rampes de glisse et overhang',
                 f"Mur de rive D7 ({p['rive_niveaux']} niveaux), colonnade circulaire, {p['rangs_pente_A']} rangs de "
                 f"rampes inclinees vers la cage, overhang 2 + {p['debord']} rangs de rampes (debord accroche a la jupe), "
                 "poteaux et poutres d'appui des rampes, mur de jupe, murs de bord du trou.")
    ancre(t)
    hors_trou = lambda x, y: dans_trou(p, x, y)
    d7 = contours[p['anneau_rive']]
    murs = cotes_contour(d7)
    sas = None                                  # pas de sas (accès par le Tek Teleporter / à ouvrir à la main)
    t.groupe = 'ext'
    t.phase = 'P2'
    for niv in range(p['rive_niveaux']):
        Zb = niv * F
        for j, (x, y, nu, k, i) in enumerate(murs):
            if dans_trou(p, x, y, bord=True):
                continue                       # pas de rive au-dessus du trou : le mur de bord du trou la remplace
            if niv == 1 and j in tesla_murs:
                continue                       # emplacement laissé libre : mur de chaume + Tesla (phase P7)
            t.add('mur', x, y, Zb + Z_TPL + F / 2, nu, Z=Zb, repere=f'rive niv{niv} c{k} p{i}')
    # colonnade circulaire sous la pente A
    col = colonnade(p)
    for c in col['colonnes']:
        for cle, Z in c['elements']:
            dz = F / 2 if cle == 'pilier' else F / 4
            t.add(cle, c['x'], c['y'], Z + Z_TPL + dz, c['theta'], Z=Z, repere=f"colonnade θ{c['theta']:.2f}")
    # pente A : de la rive vers la cage, lignes de lames sur les joints des murs de rive (le milieu des murs reste libre
    # pour les Tesla) ; tout le plan 2 : chaque ligne y est complète, posée depuis son appui sur la rive
    A7 = apo(7)
    Zr = p['rive_niveaux'] * F
    t.phase = 'P4'
    pente(t, 'pente A', A7, Zr, +1, 'pente A', nb=p['rangs_pente_A'], demi=True, filtre=hors_trou)
    # overhang : les mêmes lignes descendent de la rive au-dessus des 2 paliers (poteau sur le palier, voir
    # consolider_rampes) et finissent 40 UU après le bord de plateforme
    pente(t, 'overhang', A7, Zr, -1, 'overhang', nb=2, demi=True, filtre=hors_trou)
    # mur de jupe sur l'arête extérieure de l'anneau 15 (bord D8) : un niveau posé sur le palier, un niveau suspendu
    # dessous ; ses murs de chaume de tourelles pendent encore dessous (module 05)
    A8 = apo(p['anneaux_total'] // 2 + 1)
    Zp = cote_anneau(p, p['anneaux_total'])
    jupe = None
    if p['jupe']:
        for niv, Zb in enumerate((Zp - F, Zp)):
            for x, y, nu, k, i in cotes_contour(contours[p['anneaux_total']]):
                if dans_trou(p, x, y, bord=True):
                    continue
                t.add('mur', x, y, Zb + Z_TPL + F / 2, nu, Z=Zb, repere=f'jupe mur niv{niv} c{k} p{i}')
        # pas de plafond sous l'overhang : ce qui passe entre les rampes doit tomber dans le vide, pas sur un palier
        # au-dessus des tourelles de jupe
        jupe = dict(A=A8, Z=Zp - F, Z_haut=Zp + F)
        # débord : 'debord' rangs dans le vide, ancrés sur le haut de la jupe, sur les joints de ses murs (entre les
        # lignes de l'overhang) ; le 2e rang pend au bout d'une poutre fine posée sur le niveau bas de la jupe
        pente(t, 'debord', A8, Zp + F, -1, 'overhang', nb=p['debord'], filtre=hors_trou, rang0=2)
    A_bout = (A8 + p['debord'] * F) if jupe else A7 + 2 * F
    Z_bout = (Zp + F - p['debord'] * F) if jupe else Zr - 2 * F
    # bord du trou : murs sur les arêtes entre fondations conservées et trou, qui ferment la coupe jusqu'à
    # l'enveloppe ; les tourelles qui tombaient dans le trou (cage L1, jupe, rive) y sont reposées, face au gouffre
    bord = bords_trou(p)
    n_heavy = sum(1 for s_ in (emplacements_jupe(p, jupe) if jupe else []) if dans_trou(p, s_['xm'], s_['ym']))
    n_tesla = sum(1 for j in tesla_murs if dans_trou(p, murs[j][0], murs[j][1], bord=True))
    n_L1 = {'tek': 0, 'heavy': 0}
    for s_ in emplacements_cage(p, contours):
        if dans_trou(p, s_['xm'], s_['ym'], bord=True):
            n_L1[type_L1(s_)] += 1
    trou_slots = emplacements_trou(p, bord, n_heavy, n_tesla, n_L1)
    libres = {(round(s_['xm'], 1), round(s_['ym'], 1), s_['Zb']) for s_ in trou_slots}
    t.phase = 'P2'
    for x, y, nu, r, th in bord:
        t.groupe = groupe_bord(p, r)
        for niv in range(niveaux_bord_trou(p, r)):
            if (round(x, 1), round(y, 1), niv * F) in libres:
                continue
            t.add('mur', x, y, niv * F + Z_TPL + F / 2, nu, Z=niv * F, repere=f'bord du trou niv{niv} θ{th:.1f}')
    t.groupe = 'ext'
    return t, murs, sas, dict(A_bout=A_bout, Z_bout=Z_bout), jupe, col, bord, trou_slots


def module_cage(p, contours):
    t = Template('04 Cage a tourelles et casquette',
                 'Fut D5, galerie 2 niveaux : L1 = 60 emplacements de tourelles (murs de chaume en phase P7), '
                 'L2 = 60 double doorframes ; planchers anneaux 8-9, casquette (le toit en rampes est au module 02).')
    ancre(t)
    t.groupe = 'cage'
    d5 = contours[p['anneau_cage']]
    zmez = p['mezzanine']
    # fût : murs D5 de Z0 à la galerie, 1 porte au sol par part (côtés E1, index 2)
    t.phase = 'P2'
    for niv in range(int(zmez // F)):
        Zb = niv * F
        for x, y, nu, k, i in cotes_contour(d5):
            if dans_trou(p, x, y, bord=True):
                continue                       # coupé par le trou : le mur de bord du trou ferme la cage
            cle = 'cadre_double' if (niv == 0 and k % 2 == 1 and i == 2) else 'mur'
            t.add(cle, x, y, Zb + Z_TPL + F / 2, nu, Z=Zb, repere=f'fut niv{niv} c{k} p{i}')
    # planchers de galerie : anneaux 8 et 9 en plafonds, à chaque niveau + toit de cage
    pieces, _ = pavage(p['anneau_cage'], centre=False)
    gal = [pc for pc in pieces if pc['anneau'] > p['anneau_pod']
           and not (piece_dans_trou(p, pc) or piece_plateforme(p, pc))]
    for niv in range(p['cage_niveaux'] + 1):
        Z = zmez + niv * F
        t.phase = 'P3' if niv == 0 else 'P5'
        for pc in gal:
            cle = 'plafond' if pc['type'] == 'carre' else 'plafond_tri'
            if niv == 1 and pc['type'] == 'carre' and pc['anneau'] == p['anneau_pod'] + 1 \
                    and pc['cote'] % 2 == 1 and pc['idx'] == 0:
                cle = 'trappe'          # trappe + échelle vers la galerie L2
            t.add(cle, pc['x'], pc['y'], Z + Z_TPL, pc['yaw'], Z=Z, repere=f"galerie Z{Z:.0f} anneau {pc['anneau']}")
    # L2 : double doorframes (L1 = emplacements de tourelles, posés en P7 avec leurs murs de chaume)
    t.phase = 'P5'
    Zb = zmez + F
    for x, y, nu, k, i in cotes_contour(d5):
        if dans_trou(p, x, y, bord=True):
            continue
        t.add('cadre_double', x, y, Zb + Z_TPL + F / 2, nu, Z=Zb, repere=f'cage L2 c{k} p{i}')
    # casquette (porte-à-faux) ; au-dessus, le toit en rampes du bloc central (module 02) remplace la reprise
    A5 = apo(5)
    Ztop = zmez + p['cage_niveaux'] * F
    pente(t, 'casquette', A5, Ztop, -1, 'casquette', nb=p['casquette'], filtre=lambda x, y: dans_trou(p, x, y))
    return t, gal


# gabarits de réservation dans le hall du pod (Z0 -> 1800) : (nom, θ, apothème du centre, largeur, profondeur, murs)
GABARITS = [
    ('Réplicateur Tek', 0, 1650, 900, 600, 3),
    ('Générateur Tek n°1 (ateliers)', 60, 1800, 300, 300, 1),
    ('Forge à vapeur', 120, 1650, 900, 900, 3),
    ('Labo de fortune (Megalab)', 240, 1650, 600, 600, 2),
    ('Stockages dédiés', 300, 1600, 1500, 600, 2),
]
# générateurs Tek de la galerie (sur l'anneau 8, niveau L1) et générateurs électriques de secours (attique A,
# entre le fût et la colonnade, hors de l'axe des portes 90°/270°)
GENERATEURS = [('Générateur Tek n°1 (hall)', 60, 1800.0, 0.0), ('Générateur Tek n°2 (mezzanine)', 180, 900.0, 1800.0)]


def equipements(p, contours):
    """Positions des équipements hors plan : machines du hall, générateurs, 20 coffres-forts, 20 stockages dédiés.

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
            for a, t in cases[:n_hall]:
                out.append(dict(cle='stockage_dedie', x=a * nx + t * dx, y=a * ny + t * dy, Z=0.0, yaw=th + 180,
                                lieu='hall'))
    for nom, th, A, Z in GENERATEURS:
        out.append(dict(cle='generateur_tek', x=A * vec(th)[0], y=A * vec(th)[1], Z=Z, yaw=th + 180,
                        lieu='hall' if Z == 0 else 'mezzanine'))
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


def murs_tesla(murs):
    """Index des murs de rive (niveau 1) au milieu des côtés E0 (θ = 0°, 60°…) : 1 Tesla par part."""
    return [j for j, m in enumerate(murs) if m[3] % 2 == 0 and m[4] == 3]


def emplacements_jupe(p, jupe):
    """Murs de chaume suspendus sous le mur de jupe (bord D8, 4 478,5 ; Z -900 -> -600), au milieu d'un mur de jupe.

    Côtés pairs : 3 tourelles (extérieure, intérieure, extérieure) ; côtés impairs : 2 intérieures.
    Les « extérieures » sont sur la face côté mer ; les « intérieures » sur la face côté piton, d'où elles voient le
    dessous de la plateforme. La jupe a 8 murs par côté (milieux à t = ±150, ±450, ±750, ±1 050) : la tourelle
    intérieure des côtés pairs alterne entre t = -150 et t = +150.
    """
    out = []
    Zb = jupe['Z'] - F
    for k in range(12):
        nx, ny = vec(30 * k)
        dx, dy = -ny, nx
        motif = ([(-750, 'ext'), (-150 if k % 4 == 0 else 150, 'int'), (750, 'ext')] if k % 2 == 0
                 else [(-450, 'int'), (450, 'int')])
        for i, (tt, sens) in enumerate(motif):
            A = jupe['A']
            sortie = 30 * k if sens == 'ext' else 30 * k + 180
            out.append(emplacement(A * nx + tt * dx, A * ny + tt * dy, Zb, sortie,
                                   'JUPE-ext' if sens == 'ext' else 'JUPE-int', k, i))
    return out


def type_L1(s):
    """Cage L1 : Tek / Heavy alternées (côté E0 : T H T H T ; côté E1 : H T H T H)."""
    return 'tek' if (s['idx'] % 2 == 0) == (s['cote'] % 2 == 0) else 'heavy'


def emplacements_trou(p, bord, n_heavy, n_tesla, n_L1):
    """Tourelles reposées sur les murs de bord du trou, face au gouffre, pour garder le même nombre de tourelles.

    - n_L1 (Tek et Heavy de la cage coupée) : au niveau 6 (Z1800, celui de L1) des murs de bord intérieurs à D5,
      accessibles depuis la galerie et la mezzanine ; les plus proches de la cage d'abord ;
    - n_heavy (jupe) au niveau 0 et n_tesla (rive) au niveau 1 des murs de bord extérieurs à D5, les plus proches
      du bord de la plateforme d'abord, chacune sur un mur différent : une colonne de murs de bord n'a jamais qu'un
      seul mur de chaume (comme sur la tour 1809, le mur posé au-dessus reste tenu par ses voisins).
    """
    interieurs = sorted((m for m in bord if m[3] <= apo(5) + 1), key=lambda m: -m[3])
    exterieurs = sorted((m for m in bord if m[3] > apo(5) + 1), key=lambda m: -m[3])
    types = []
    nT, nH = n_L1['tek'], n_L1['heavy']
    while nT or nH:                              # alternance Tek / Heavy le long du bord
        if nT >= nH and nT:
            types.append('tek')
            nT -= 1
        else:
            types.append('heavy')
            nH -= 1
    assert len(interieurs) >= len(types), 'pas assez de murs de bord pour reposer les tourelles de la cage'
    assert len(exterieurs) >= n_heavy + n_tesla, 'pas assez de murs de bord pour reposer jupe et Tesla'
    out = []
    for n, ((x, y, nu, r, th), ty) in enumerate(zip(interieurs, types)):
        s_ = emplacement(x, y, p['mezzanine'], nu, 'TROU-L1', round(nu / 30) % 12, n)
        s_['type'] = ty
        out.append(s_)
    for n, (x, y, nu, r, th) in enumerate(exterieurs[:n_heavy]):
        s_ = emplacement(x, y, 0.0, nu, 'TROU', round(nu / 30) % 12, n)
        s_['type'] = 'heavy'
        out.append(s_)
    for n, (x, y, nu, r, th) in enumerate(exterieurs[n_heavy:n_heavy + n_tesla]):
        s_ = emplacement(x, y, F, nu, 'TROU', round(nu / 30) % 12, n)
        s_['type'] = 'tesla'
        out.append(s_)
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


def angle(s):
    return math.degrees(math.atan2(s['y'], s['x'])) % 360


def matrice(p, contours, murs, tesla_murs, jupe, trou_slots):
    nH, nT, nS = p['inventaire']
    L1 = sorted((s for s in emplacements_cage(p, contours) if not dans_trou(p, s['xm'], s['ym'], bord=True)),
                key=angle) + sorted((s for s in trou_slots if s['couche'] == 'TROU-L1'), key=angle)
    J = sorted((s for s in (emplacements_jupe(p, jupe) if jupe else []) if not dans_trou(p, s['xm'], s['ym'])),
               key=angle)
    S = sorted((emplacement(murs[j][0], murs[j][1], F, murs[j][2], 'RIVE', murs[j][3], murs[j][4]) for j in tesla_murs
                if not dans_trou(p, murs[j][0], murs[j][1], bord=True)), key=angle)
    T_h = sorted((s for s in trou_slots if s['couche'] == 'TROU' and s['type'] == 'heavy'), key=angle)
    T_s = sorted((s for s in trou_slots if s['couche'] == 'TROU' and s['type'] == 'tesla'), key=angle)
    # L1 : Tek / Heavy alternées (côté E0 : T H T H T ; côté E1 : H T H T H) = 5 Tek + 5 Heavy par part
    for s in L1:
        if s['couche'] == 'L1':
            s['type'] = type_L1(s)
    for s in J:
        s['type'] = 'heavy'
    for s in S:
        s['type'] = 'tesla'
    besoin = {k: sum(1 for s in L1 + J + S + T_h + T_s if s['type'] == k) for k in ('heavy', 'tek', 'tesla')}
    assert besoin['heavy'] <= nH and besoin['tek'] <= nT and besoin['tesla'] <= nS, besoin
    # priorités : 1 jupe et bord du trou (dessous de la plateforme, gouffre) 2 Tek L1 3 Tesla 4 Heavy L1
    groupes = [('P1 jupe et bord du trou : Heavy', sorted(J + T_h, key=angle)),
               ('P2 L1 Tek', [s for s in L1 if s['type'] == 'tek']),
               ('P3 Tesla (rive et bord du trou)', sorted(S + T_s, key=angle)),
               ('P4 L1 Heavy', [s for s in L1 if s['type'] == 'heavy'])]
    ordre = []
    for nom, g in groupes:
        for i in ordre_vdc(len(g)):
            g[i]['priorite'] = nom
            ordre.append(g[i])
    for n, s in enumerate(ordre, 1):
        s['ordre'] = n
    compte = 0
    for s in ordre:
        compte_s = s['type'] in ('heavy', 'tek') or (s['type'] == 'tesla' and p['tesla_comptee'])
        s['posee'] = not (compte_s and compte >= p['cap'])
        compte += compte_s and s['posee']
    poses = {k: sum(1 for s in ordre if s['posee'] and s['type'] == k) for k in ('heavy', 'tek', 'tesla')}
    reserve = {'heavy': nH - poses['heavy'], 'tek': nT - poses['tek'], 'tesla': nS - poses['tesla']}
    return ordre, poses, reserve


def template_tourelles(nom, ordre):
    t = Template(nom, 'Tourelles verticales (template 2727) : chaque tourelle est precedee de son mur de chaume de pose, '
                      'a demolir en jeu apres la pose. Ordre des entrees = ordre de pose.')
    ancre(t)
    t.phase = 'P7'
    for s in ordre:
        if not s['posee']:
            continue
        t.groupe = 'tourelles_cage' if s['couche'] in ('L1', 'TROU-L1') else 'ext'
        z = s['Zb'] + Z_TPL + F / 2
        rep = f"#{s['ordre']} {s['couche']} c{s['cote']} p{s['idx']}"
        t.add('chaume_mur', s['xm'], s['ym'], z, s['sortie'], Z=s['Zb'], repere=rep + ' (chaume a demolir)')
        rot = ROT_TESLA if s['type'] == 'tesla' else ROT_TOURELLE
        t.add(s['type'], s['x'], s['y'], z, s['sortie'] + 90, Z=s['Zb'], repere=rep, **rot)
    return t


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
        segs.append(((A8, Zp - F), (A8, Zp + F)))
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
    A5, A7 = apo(5), apo(7)
    out = {'L1': secteur_tir(p, ob, A5 + DECALAGE_MONTAGE + SAILLIE_TETE, p['mezzanine'] + F / 2),
           'RIVE': bande_vue(p, ob, A7 + DECALAGE_MONTAGE + SAILLIE_TETE / 2, F * 1.5)}
    if jupe:
        zc = jupe['Z'] - F / 2
        out['JUPE-ext'] = secteur_tir(p, ob, jupe['A'] + DECALAGE_MONTAGE + SAILLIE_TETE, zc)
        out['JUPE-int'] = secteur_tir(p, ob, jupe['A'] - DECALAGE_MONTAGE - SAILLIE_TETE, zc, sens=-1)
    return out


# ---------------------------------------------------------------- découpage en plans (anneaux extérieurs / centre)
ORDRE_PHASES = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7']
PLANS = [
    ('sol_ext', 'Plan_1_sol_anneaux_12-15', 'Sol des anneaux 12 a 15 (paliers de bord), sans le trou'),
    ('ext', 'Plan_2_murs_rampes_tourelles_anneaux_12-15',
     'Anneaux 12 a 15 : rive, bord du trou, colonnade, mur de jupe, appuis, pente A (de la rive vers la cage), overhang '
     'et debord, Tesla et Heavy (murs de chaume de pose a demolir)'),
    ('sol_centre', 'Plan_3_sol_centre_anneaux_0-11', 'Sol du centre : hexagone central et anneaux 1 a 11'),
    ('pod', 'Plan_4_pod_central', 'Pod central : mur de pod, piliers, colonne d\'escaliers, mezzanine Z1800'),
    ('cage', 'Plan_5_cage_et_casquette', 'Cage : fut, bord du trou dans le couloir, galeries, double doorframes L2, casquette'),
    ('toit', 'Plan_6_toit_rampes', 'Plancher de toit Z2400 du pod, toit en rampes inclinees et casquette du bord du trou'),
    ('tourelles_cage', 'Plan_7_tourelles_cage_L1', 'Tourelles verticales L1 de la cage et leurs murs de chaume de pose'),
    ('plateforme', 'Plan_8_plateforme_future_anneaux_9-11',
     'Petite plateforme au milieu du trou (fondations vertes du releve) : rien n\'y est accroche, projet futur'),
]


def assembler_plans(p, modules):
    """Répartit les entrées des modules dans les plans (groupe de chaque entrée), triées par phase.

    Le plan 1 porte la pile d'ancrage (2 demi-piliers) ; les autres, 1 demi-pilier qui se pose dessus.
    """
    plans = {}
    for n, (cle, fichier, desc) in enumerate(PLANS):
        t = Template(fichier.replace('_', ' '), desc + ". Pilier de reference : pile d'ancrage en (0 ; 300).")
        ancre(t, empilee=(n == 0))
        plans[cle] = t
    contenu = {cle: [] for cle, *_ in PLANS}
    for _, m in modules:
        for e, ph, gr, ligne in zip(m.entries, m.phases, m.groupes, m.lignes):
            if ph is None:                      # ancres des modules
                continue
            contenu[gr].append((ph, e, ligne))
    for cle, liste in contenu.items():
        t = plans[cle]
        for ph, e, ligne in sorted(liste, key=lambda v: ORDRE_PHASES.index(v[0])):
            t.phase = ph
            t.entries.append(e)
            t.lignes.append(ligne)
            t.phases.append(ph)
            t.groupes.append(cle)
    return plans


def secteur_test(plans, th0=-15.0, th1=45.0):
    """Template d'essai en solo : toutes les pièces des plans 1, 3, 4, 5, 2, 6 et 7 (dans l'ordre de pose) dont le
    pivot est entre θ0 et θ1, soit 2 côtés et une arête du dodécagone (θ 15°), hors du trou. On y retrouve chaque sorte
    de pièce et d'appui : rive, colonnade, pente A et ses poteaux, overhang et poteaux sur les paliers, jupe, poutres et
    débord, cage, tourelles et murs de chaume, toit et ses poteaux jusqu'au faîtage."""
    t = Template(f'Secteur test θ{th0:.0f}-{th1:.0f}', 'Essai en solo : un secteur de 60 degres de tous les plans, '
                 "dans l'ordre de pose. Pilier de reference : pile d'ancrage en (0 ; 300).")
    ancre(t, empilee=True)
    for cle in ('sol_ext', 'sol_centre', 'pod', 'cage', 'ext', 'toit', 'tourelles_cage'):
        src = plans[cle]
        for e, l_, ph in zip(src.entries, src.lignes, src.phases):
            if l_[5].startswith('ancre'):
                continue
            th = math.degrees(math.atan2(l_[2], l_[1]))
            if th0 <= th <= th1 or math.hypot(l_[1], l_[2]) < 150:
                t.entries.append(e)
                t.lignes.append(l_)
                t.phases.append(ph)
                t.groupes.append(cle)
                t.metas.append(None)
    return t


def verifier_plans(p, plans, modules):
    """Chaque entrée des modules est dans un seul plan ; rien n'est posé au-dessus du trou."""
    total_modules = sum(1 for _, m in modules for ph in m.phases if ph is not None)
    total_plans = sum(1 for t in plans.values() for l in t.lignes if not l[5].startswith('ancre'))
    assert total_modules == total_plans, (total_modules, total_plans)
    for cle, t in plans.items():
        if cle == 'plateforme':
            continue                           # fondations vertes : posées, mais rien d'autre au-dessus
        for cle_p, x, y, Z, yaw, r in t.lignes:
            if r.startswith(('ancre', 'bord du trou', 'casquette du trou')) or ' TROU' in r:
                continue                       # bord du trou : tourelles (pivot 10 UU devant le mur) et casquette en
                                               # porte-à-faux au-dessus du gouffre
            assert not dans_trou(p, x, y), (cle, r, x, y)
    for cle_p, x, y, Z, yaw, r in plans['plateforme'].lignes:
        assert r.startswith('ancre') or cle_p in ('fond', 'fond_tri'), r
    print(f"  {len(plans)} plans, {total_plans} entrées, aucune au-dessus du trou : " +
          ', '.join(f"{cle} {sum(1 for l in t.lignes if not l[5].startswith('ancre'))}" for cle, t in plans.items()))


def bilan_brut(tot):
    """Décompose les produits fabriqués en ressources brutes (recettes ASE/ASA usuelles, à vérifier)."""
    el, po, pc, pe = tot.get('EL', 0), tot.get('PO', 0), tot.get('PC', 0), tot.get('PE', 0)
    mi = tot.get('MI', 0) + el                       # électronique : 1 lingot + 3 perles de silice
    pc_tot = pc + 2 * po                             # polymère : 2 obsidienne + 2 pâte cimentée
    return {'minerai_metal': 2 * mi, 'perles_silice': 3 * el, 'obsidienne': 2 * po,
            'chitine_ou_keratine': 4 * pc_tot, 'pierre': 8 * pc_tot + pe, 'silex': 2 * pe,
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
    fig, ax = plt.subplots(figsize=(15, 8.5))
    A4, A5, A7, A8 = apo(4), apo(5), apo(7), apo(8)
    Zr = p['rive_niveaux'] * F
    zmez = p['mezzanine']
    Zc = zmez + p['cage_niveaux'] * F
    Zsommet = infos_pod['Zsommet']
    ax.fill_between([0, A7], [-100, -100], [0, 0], color='#3f88c5', alpha=.5, label='fondations Z0')
    for (r0, r1, Z), coul in zip(paliers_bord(p), ('#9aa5b1', '#6c757d')):
        ax.fill_between([r0, r1], [Z - 100, Z - 100], [Z, Z], color=coul,
                        label=f'palier de bord Ø{2 * r0 / F:.0f} → Ø{2 * r1 / F:.0f} : Z {Z:.0f}')
    ax.fill_between([-200, A8], [-1000, -1000], [-400, -400], color='#ccc', alpha=.5,
                    label='Metal Cliff Platform (épaisseur indicative)')
    ax.plot([150, 150], [0, zmez], color='#9c6644', lw=4, ls=(0, (1, 1)), label='colonne d\'escaliers jusqu\'à Z1800')
    ax.plot([A4, A4], [0, p['pod_niveaux'] * F], color='#b00', lw=3, label=f"mur de pod D4 ({p['pod_niveaux']} murs)")
    ax.plot([A5, A5], [0, zmez], color='#070', lw=3, label='fût D5 (6 murs)')
    ax.plot([A5, A5], [zmez + F, Zc], color='#0a0', lw=6, ls=(0, (2, 1)), label='L2 : double doorframes')
    ax.plot([A7, A7], [0, F], color='k', lw=3, label='mur de rive D7')
    ax.plot([A7, A7], [F, Zr], color='k', lw=1, ls=':')
    for Z in (zmez, zmez + F, Zc):
        ax.plot([A4, A5], [Z, Z], color='#070', lw=1.5)
    ax.plot([0, A4], [zmez, zmez], color='#b00', lw=1.5, ls='--', label='mezzanine Z1800')
    ax.plot([0, A4], [Zc, Zc], color='#b00', lw=1.5, label=f'plancher de toit Z{Zc:.0f} (pod + cage)')
    R = col['rayon']
    ax.plot([R, R], [0, min(hauteur_pente_A(p, R, 0) - 30, p['colonnade_hauteur'])], color='#6a040f', lw=3,
            label=f"colonnade circulaire r={R:.0f} (1 pilier / 1 vide, {p['colonnade_hauteur']:.0f} UU)")
    lame = dict(lw=3, ls=(0, (1, 0.6)))         # rampes inclinées : lames, tracé en pointillé serré
    ax.plot([A7 - p['rangs_pente_A'] * F, A7 + 2 * F], [Zr + p['rangs_pente_A'] * F, Zr - 2 * F],
            color='#e07a2f', label='pente A + overhang : rampes inclinées (joints des murs de rive)', **lame)
    if jupe:
        ax.plot([jupe['A'], ob['A_bout']], [jupe['Z_haut'], ob['Z_bout']], color='#c1121f',
                label='débord dans le vide : rampes accrochées à la jupe', **lame)
    ax.plot([A5 + p['casquette'] * F, A5], [Zc - p['casquette'] * F, Zc], color='#7b2cbf',
            label='casquette : rampes inclinées', **lame)
    ax.plot([A5, A5 - (Zsommet - Zc)], [Zc, Zsommet], color='#b00', label='toit : rampes inclinées (tours 1201/1809)',
            **lame)
    if jupe:
        ax.plot([jupe['A'], jupe['A']], [jupe['Z'], jupe['Z_haut']], color='#555', lw=2, label='mur de jupe (bord D8)')
    # appuis des rampes dans le plan de coupe (lignes du côté 0 les plus proches de l'axe)
    vus = set()
    for cle, x, y, Zb, Zh in appuis:
        if x > 0 and abs(y) < 160:
            if cle == 'poutre_fine':
                ax.plot([x - 150, x + 150], [Zb, Zb], color='#2a9d8f', lw=3)
            else:
                ax.plot([x, x], [Zb, Zh], color='#2a9d8f', lw=2)
            vus.add(cle)
    ax.plot([], [], color='#2a9d8f', lw=2, label='appuis des rampes : poteaux en piliers fins, poutre fine du débord')
    sec = secteurs(p, ob, jupe)
    yeux = {'L1': (A5 + DECALAGE_MONTAGE + SAILLIE_TETE, zmez + F / 2, 1, 'tab:blue'),
            'RIVE': (A7 + DECALAGE_MONTAGE + SAILLIE_TETE / 2, F * 1.5, 1, '#d4ac0d')}
    if jupe:
        yeux['JUPE-ext'] = (jupe['A'] + DECALAGE_MONTAGE + SAILLIE_TETE, jupe['Z'] - F / 2, 1, 'tab:purple')
        yeux['JUPE-int'] = (jupe['A'] - DECALAGE_MONTAGE - SAILLIE_TETE, jupe['Z'] - F / 2, -1, 'tab:pink')
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
    ax.set_ylim(-1600, max(5800, Zsommet + 300))
    ax.set_aspect('equal')
    ax.grid(True, lw=0.3)
    ax.set_xlabel('distance au centre le long de la normale 0° (UU)')
    ax.set_ylabel('Z (UU) — 0 = dessus des fondations intérieures')
    ax.set_title('Coupe radiale type (côté E0, θ=0°) — tourelles verticales et secteurs de tir')
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
    styles = {'heavy': ('s', '#c0392b'), 'tek': ('^', '#2471a3'), 'tesla': ('*', '#d4ac0d')}
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
    for nom, th, A, Z in GENERATEURS:
        c, s_ = vec(th)
        ax.plot(A * c, A * s_, 'D', color='#2a9d8f' if Z == 0 else '#76c7c0', ms=10, mec='k')
    ax.plot([], [], 'D', color='#2a9d8f', mec='k', label='Générateur Tek n°1 (hall, Z0)')
    ax.plot([], [], 'D', color='#76c7c0', mec='k', label='Générateur Tek n°2 (mezzanine, Z1800)')
    for nom, (mk, co) in styles.items():
        ax.plot([], [], mk, color=co, label=NOMS[nom])
    ax.plot([], [], 's', color='#c0392b', mec='k', label='Heavy de jupe tournée vers le piton (bord noir)')
    ax.plot([], [], 's', color='#c0392b', mec='k', mew=1.5, ms=9,
            label='tourelle reposée sur un mur de bord du trou, face au gouffre (grande)')
    ax.plot([], [], color='#c0392b', lw=2, label='murs de bord du trou')
    n_pos = sum(1 for s in ordre if s['posee'])
    ax.set_aspect('equal')
    ax.set_title(f'Tourelles verticales — scénario B ({n_pos} posées) — trait = sens de tir ; numéros = ordre de pose '
                 '(hors L1)', fontsize=10)
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
    for n, coul, nom in ((2, '#000', f'piliers PA (Z0 -> {Zt:.0f})'), (1, '#666', f"piliers PB (Z{p['mezzanine']:.0f} -> {Zt:.0f})")):
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
    ax.plot([], [], color='#c0392b', lw=3, label='murs de bord du trou (Z0 → 2400)')
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
    """Gauche : sol découpé en plans (1 = anneaux 12-15, 3 = centre, 8 = plateforme verte), trou et relevé du joueur.
    Droite : détail du trou avec murs de bord et tourelles reposées face au gouffre."""
    plt, MPoly = _mpl()
    if not plt:
        return
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(22, 11))
    sols = (('sol_ext', '#3f88c5'), ('sol_centre', '#e07a2f'), ('plateforme', '#2e9e4f'))
    for ax in (ax1, ax2):
        for cle, coul in sols:
            for c_, x, y, Z, yaw, r in plans[cle].lignes:
                if c_ in ('fond', 'fond_tri'):
                    pc = dict(type='carre' if c_ == 'fond' else 'tri', x=x, y=y, yaw=yaw)
                    a = .85 if (Z or 0) == 0 else .5
                    if ax is ax2 and cle != 'plateforme':
                        a = .25
                    ax.add_patch(MPoly(polygone(pc), closed=True, fc=coul, ec='#333', lw=0.2, alpha=a))
        for pc in trou:
            ax.add_patch(MPoly(polygone(pc), closed=True, fc='#f4d4d0', ec='#c0392b', lw=0.6, ls='--'))
        if releve:
            pts = [(X, Y) for X, Y, Z, ok in releve[4]]
            ax.plot([x for x, y in pts], [y for x, y in pts], 'k.', ms=4)
        ax.plot(*ANCRE, 'k+', ms=14, mew=2)
    n_pla = sum(1 for l in plans['plateforme'].lignes if l[0] in ('fond', 'fond_tri'))
    ax1.plot([], [], 's', color='#3f88c5', label='plan 1 : sol anneaux 12-15 (paliers plus clairs)')
    ax1.plot([], [], 's', color='#e07a2f', label='plan 3 : sol du centre (anneaux 0-11)')
    ax1.plot([], [], 's', color='#2e9e4f', label=f'plan 8 : plateforme future ({n_pla} fondations, rien dessus)')
    ax1.plot([], [], 's', mfc='#f4d4d0', mec='#c0392b', label=f'trou : {len(trou)} fondations retirées')
    if releve:
        ax1.plot([], [], 'k.', label=f'relevé du joueur : {releve[1]}/{releve[2]} fondations retrouvées')
    ax1.plot([], [], 'k+', label='pilier de référence (0 ; 300)')
    ax1.set_aspect('equal')
    ax1.set_xlim(-5400, 5400)
    ax1.set_ylim(-5400, 5400)
    ax1.legend(loc='lower left', fontsize=9)
    ax1.set_title("Sol en 3 plans et trou à l'avant (relevé du joueur : blanc = retiré, vert = plateforme)")
    # détail du trou : contours D4 (pod), D5 (cage), D7 (rive) au niveau 0, murs de bord, tourelles
    def trait(ax, x, y, nu, **kw):
        nx, ny = vec(nu)
        dx, dy = -ny, nx
        ax.plot([x - 150 * dx, x + 150 * dx], [y - 150 * dy, y + 150 * dy], **kw)
    for cle, debut, coul in (('pod', 'pod niv0', '#555'), ('cage', 'fut niv0', '#7d3c98'), ('ext', 'rive niv0', 'k')):
        for c_, x, y, Z, yaw, r in plans[cle].lignes:
            if c_ in ('mur', 'cadre_double') and r.startswith(debut):
                trait(ax2, x, y, yaw, color=coul, lw=2)
    for x, y, nu, r, th in bord:
        trait(ax2, x, y, nu, color='#c0392b', lw=3)
        nx, ny = vec(nu)
        ax2.annotate(str(niveaux_bord_trou(p, r)), (x - 70 * nx, y - 70 * ny), fontsize=7, ha='center', va='center')
    marq = {'heavy': ('s', '#c0392b'), 'tek': ('^', '#2471a3'), 'tesla': ('*', '#d4ac0d')}
    for cle in ('ext', 'tourelles_cage'):
        for c_, x, y, Z, yaw, r in plans[cle].lignes:
            if c_ in marq:
                mk, co = marq[c_]
                ax2.plot(x, y, mk, color=co, ms=11 if 'TROU' in r else 7, mec='k', mew=1.6 if 'TROU' in r else .5)
    for c_, x, y, Z, yaw, r in plans['ext'].lignes:
        if c_ == 'pilier' and r.startswith('colonnade'):
            ax2.plot(x, y, '.', color='#6a040f', ms=2)
    for c_, x, y, Z, yaw, r in plans['toit'].lignes:
        if r.startswith('casquette du trou'):
            nx, ny = vec(yaw + 90)
            ax2.plot([x - 150 * nx, x + 150 * nx], [y - 150 * ny, y + 150 * ny], color='#e67e22', lw=2.5)
    ax2.plot([], [], color='#e67e22', lw=2.5, label='casquette du trou (rampes Z2400 → 2100, plan 6)')
    ax2.plot([], [], color='#c0392b', lw=3, label='murs de bord du trou (chiffre = hauteur en murs)')
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


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--racine', default=RACINE)
    ap.add_argument('--debord', type=int, choices=(1, 2), default=2)
    ap.add_argument('--casquette', type=int, choices=(1, 2), default=1)
    ap.add_argument('--decaissement', type=float, default=150.0)
    ap.add_argument('--colonnade', type=float, default=P['colonnade_rayon'], help='rayon de la colonnade (UU)')
    ap.add_argument('--trou', default=P['trou'], help='fondations du trou (JSON : retirees / plateforme)')
    ap.add_argument('--appuis', choices=('tours', 'prudent'), default=P['appuis'],
                    help="appuis des rampes : comme les tours (défaut) ou un poteau au bout de chaque ligne montante")
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
    pod, infos_pod = module_pod(p, contours)
    murs_rive = cotes_contour(contours[p['anneau_rive']])
    tesla_murs = murs_tesla(murs_rive)
    rampe, murs, sas, ob, jupe, col, bord, trou_slots = module_rampe(p, contours, set(tesla_murs))
    cage, gal = module_cage(p, contours)
    ordre, poses, reserve = matrice(p, contours, murs, tesla_murs, jupe, trou_slots)
    tourelles = template_tourelles('Tourelles verticales (cap 100, Tesla comptees)', ordre)

    modules = [('sol', sol), ('pod', pod), ('rive', rampe), ('cage', cage), ('tourelles', tourelles)]
    conso = consolider_rampes(p, modules)
    print(f"  Rampes : {conso['retraits']} ; appuis : {conso['poteaux']} poteaux ({conso['pilier_fin']} piliers fins, "
          f"{conso['demi_pilier_fin']} demi-piliers fins), {conso['poutre_fine']} poutres fines, "
          f"{conso['raccourcies']} lignes raccourcies faute d'appui")
    infos_pod['Zsommet'] = max(Z + F for cle, x, y, Z, yaw, r in pod.lignes if cle == 'rampe' and r.startswith('toit'))
    col['colonnes'] = [c for c in col['colonnes'] if any(cle == 'pilier' and abs(x - c['x']) < 1 and abs(y - c['y']) < 1
                                                         for cle, x, y, Z, yaw, r in rampe.lignes)]
    verifier_encombrements(p, infos_pod, col, ordre)
    plans = assembler_plans(p, modules)
    verifier_plans(p, plans, modules)
    admis = verifier_collisions(plans)
    appuis = verifier_appuis(plans, p['appuis'])
    chaume = chaume_a_demolir(plans, ordre)
    rep_plans = os.path.join(rep_t, 'plans')
    os.makedirs(rep_plans, exist_ok=True)
    for cle, fichier, desc in PLANS:
        plans[cle].ecrire(os.path.join(rep_plans, fichier + '.json'))
    rep_test = os.path.join(rep_t, 'test')
    os.makedirs(rep_test, exist_ok=True)
    essai = secteur_test(plans)
    essai.ecrire(os.path.join(rep_test, 'Secteur_test_theta_-15_45.json'))
    print(f"  Secteur d'essai θ -15° → 45° : {len(essai.entries)} entrées (templates/test/)")
    equip = equipements(p, contours)

    # CSV de pose : un par plan
    for cle, fichier, desc in PLANS:
        t = plans[cle]
        ecrire_csv(os.path.join(rep_d, fichier + '.csv'),
                   [(i, NOMS[c], ph, round(x, 1), round(y, 1), '' if Z is None else round(Z, 1), round(yaw % 360, 1),
                     round(math.degrees(math.atan2(y, x)) % 360, 2), round(math.hypot(x, y), 1), r)
                    for i, ((c, x, y, Z, yaw, r), ph) in enumerate(zip(t.lignes, t.phases))],
                   ['entree', 'piece', 'phase', 'x', 'y', 'Z_plan', 'yaw', 'theta', 'rayon', 'repere'])
    ecrire_csv(os.path.join(rep_d, '05_matrice_tourelles.csv'),
               [(s['ordre'], s['priorite'], NOMS[s['type']], s['couche'], s['cote'], s['idx'], round(angle(s), 2),
                 round(s['xm'], 1), round(s['ym'], 1), round(s['Zb'], 1), round(s['x'], 1), round(s['y'], 1),
                 round(s['Zb'] + F / 2, 1), round(s['sortie'] % 360, 1), 'oui' if s['posee'] else 'reserve')
                for s in ordre],
               ['ordre', 'priorite', 'type', 'couche', 'cote', 'index', 'theta', 'x_chaume', 'y_chaume',
                'Z_bas_chaume', 'x_tourelle', 'y_tourelle', 'Z_tourelle', 'sens_de_tir', 'posee'])
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
               [(n, round(x, 1), round(y, 1), round(nu, 1), round(r, 1), round(th, 2), niveaux_bord_trou(p, r))
                for n, (x, y, nu, r, th) in enumerate(bord)],
               ['n', 'x', 'y', 'yaw_vers_le_trou', 'rho', 'theta', 'hauteur_murs'])

    # synthèse
    dmax, rmax = distances(ordre)
    syn = {'parametres': {k: v for k, v in p.items()}, 'apothemes': {f'D{m}': round(apo(m), 1) for m in range(1, 9)},
           'rayons_coins': {f'D{m}': round(rayon_coin(m), 1) for m in range(1, 9)},
           'overhang': ob, 'jupe': jupe, 'Z_plancher_toit': infos_pod['Ztoit'], 'Z_sommet_toit': infos_pod['Zsommet'],
           'paliers_bord': [dict(anneau=p['anneau_rive'] + i + 1, apo_E0_int=round(a, 1), apo_E0_ext=round(b, 1), Z=Z)
                            for i, (a, b, Z) in enumerate(paliers_bord(p))],
           'trou': {'fondations_retirees': {'carres': sum(1 for pc in trou if pc['type'] == 'carre'),
                                            'triangles': sum(1 for pc in trou if pc['type'] == 'tri'),
                                            'par_anneau': {a_: sum(1 for pc in trou if pc['anneau'] == a_)
                                                           for a_ in sorted({pc['anneau'] for pc in trou})}},
                    'plateforme': sorted(list(k) for k in charger_trou(p)['plateforme']),
                    'murs_de_bord': {'aretes': len(bord), 'murs': sum(niveaux_bord_trou(p, r) for *_, r, th in bord)},
                    'releve': None if not releve else {'rotation': releve[0], 'retrouvees': releve[1],
                                                       'total': releve[2], 'dans_le_trou': releve[3]}},
           'tourelles': {'posees': poses, 'reserve': reserve,
                         'par_couche': {cch: sum(1 for s in ordre if s['posee'] and s['couche'] == cch)
                                        for cch in ('JUPE-int', 'JUPE-ext', 'L1', 'RIVE', 'TROU', 'TROU-L1')}},
           'cap': {'distance_max_entre_tourelles': round(dmax, 1), 'rayon_max_tourelle': round(rmax, 1),
                   'distance_min_avant_poste': round(10000 + rmax, 1)},
           'secteurs': secteurs(p, ob, jupe),
           'colonnade': {k: (round(v, 3) if isinstance(v, float) else v) for k, v in col.items() if k != 'colonnes'},
           'escalier': {**infos_pod['escalier'], 'marches': int(p['mezzanine'] // F)},
           'tremie': [dict(anneau=pc['anneau'], type=pc['type'], x=round(pc['x'], 1), y=round(pc['y'], 1))
                      for pc in infos_pod['tremie']],
           'pics': {'nombre': len(pics), 'apotheme_ligne': round(apo(7) + 150, 1), 'Z': -p['decaissement']}}
    syn['constructibilite'] = {
        'rampes_retirees': conso['retraits'], 'lignes_raccourcies_faute_d_appui': conso['raccourcies'],
        'appuis': {'poteaux': conso['poteaux'], 'piliers_fins': conso['pilier_fin'],
                   'demi_piliers_fins': conso['demi_pilier_fin'], 'poutres_fines': conso['poutre_fine']},
        'controle_appuis': appuis, 'recouvrements_admis': admis,
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
    syn['generateurs'] = [dict(nom=n, theta=th, x=round(A * vec(th)[0], 1), y=round(A * vec(th)[1], 1), Z=Z)
                          for n, th, A, Z in GENERATEURS]

    def sans_ancre(t):
        c = {}
        for cle, *_, r in t.lignes:
            if not r.startswith('ancre'):
                c[cle] = c.get(cle, 0) + 1
        return c

    syn['plans'] = {}
    structure = {}
    for cle, fichier, desc in PLANS:
        c = sans_ancre(plans[cle])
        syn['plans'][fichier] = {'total': sum(c.values()), 'pieces': c,
                                 'bilan': bilan({k: v for k, v in c.items() if k not in ('heavy', 'tek', 'tesla')})}
        for k, v in c.items():
            structure[k] = structure.get(k, 0) + v
    tourelles_n = {k: structure.pop(k, 0) for k in ('heavy', 'tek', 'tesla')}
    chaume = {'chaume_mur': structure.pop('chaume_mur', 0)}
    nb_eq = {}
    for q in equip:
        nb_eq[q['cle']] = nb_eq.get(q['cle'], 0) + 1
    nb_ancres = sum(1 for t in plans.values() for *_, r in t.lignes if r.startswith('ancre'))
    postes = {'structure': structure, 'tourelles_chaume': chaume, 'tourelles': tourelles_n,
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

    print(json.dumps({v: syn['plans'][v]['total'] for v in syn['plans']}, indent=1))
    print(json.dumps(syn['tourelles'], indent=1, ensure_ascii=False))
    print(json.dumps(syn['cap'], indent=1), syn['secteurs'])


if __name__ == '__main__':
    main()
