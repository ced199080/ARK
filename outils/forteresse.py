#!/usr/bin/env python3
"""Générateur de la forteresse circulaire Ø30 sur Metal Cliff Platform (ARK: Survival Ascended).

Produit, à partir d'une seule géométrie paramétrée :
  - les templates Template Hammer (JSON, même schéma que les exports Wikily.gg), par module et par phase,
  - les tableaux de coordonnées (CSV) pour la pose manuelle,
  - la matrice des tourelles (scénario B : cap 100, Tesla comptées) avec ordre de pose et murs de chaume de pose,
  - le bilan matières,
  - les plans PNG (si matplotlib est installé).

Usage :
    python3 outils/forteresse.py                       # tout régénérer
    python3 outils/forteresse.py --debord 1            # overhang d'une seule structure au-delà de la plateforme
    python3 outils/forteresse.py --colonnade 2520      # rayon de la colonnade circulaire
    python3 outils/forteresse.py --verifier-481 template-481-building-0.json

Conventions (mesurées dans les templates fournis, voir README_Notice_Montage.md §2) :
  - 1 fondation = 300 UU, triangle de côté 300 (hauteur H = 259,81 UU).
  - Origine (0,0) = centre de l'étoile et du Coeur Base. Angle θ = atan2(y, x) en degrés = yaw Unreal.
  - Z « plan » = cote d'un plancher, 0 = dessus des fondations intérieures.
    z template = Z + 90 (plancher), Z + 40 pour le pivot d'une fondation, Z_bas + 240 pour un mur.
  - Triangle (fondation/plafond) : pivot à mi-hauteur, yaw = direction base -> pointe.
  - Aucun toit incliné (on tiendrait debout dessus) : toutes les pentes à 45° sont en rampes inclinées (Sloped
    Railing, tours 1201/1809), en lames au pas de 300 UU ; voir rang_rampes().
  - Tourelle « verticale » (template 2727, tours 1201/1809) : fixée sur la face extérieure d'un mur de chaume
    (Thatch_Wall_Small) qui occupe l'emplacement ; pivot 10 UU devant le plan du mur, à mi-hauteur ;
    Heavy/Tek : pitch -89,5°, yaw = θ_sortie + 90°, roll -90° ; Tesla : pitch 0°, yaw = θ_sortie + 90°, roll -90°.
    Le mur de chaume est démoli en jeu après la pose.
"""
import argparse
import copy
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
    rangs_pente_A=4,           # rangs de toit entre la rive et la cage
    cage_niveaux=2,            # étages de la cage
    casquette=1,               # rangs de casquette en porte-à-faux devant la cage
    debord=2,                  # rangs de toit au-delà du bord de plateforme (1 ou 2)
    pod_niveaux=8,             # hauteur du mur de pod (murs) -> Z 2400 = toit de cage (plancher de toit commun)
    mezzanine=1800.0,          # plancher technique du pod = sol de la galerie L1 (6 murs libres dessous)
    jupe=True,                 # jupe basse sous l'overhang (tourelles sous la plateforme)
    coeur='references/Coeur_Base.json',   # template Coeur Base fourni (noyau + escalier, centré sur l'origine)
    coeur_rotation=0.0,        # rotation du Coeur Base autour du centre (multiples de 60° conseillés)
    colonnade_rayon=3360.0,    # colonnade circulaire sous la pente A (entre le pod et les pics)
    colonnade_hauteur=300.0,   # 1 pilier de haut, comme les cercles de piliers 704 / 701 (au lieu de monter sous la pente)
    largeur_pilier=2 * math.pi * 600 / 96,   # 39,27 UU : 48 piliers à r=600 (template 704) = 1 pilier / 1 vide
    colonnade_passages=(30, 90, 150, 210, 270, 330),   # 1 passage par part (axe des portes du fût)
    colonnade_largeur_passage=300.0,
    cap=100, tesla_comptee=True,             # scénario B retenu
    inventaire=(80, 35, 10),                 # Heavy, Tek, Tesla disponibles
    parts=6,                                 # l'ensemble = 6 parts égales de 60°
    part_debut=-14.5,                        # part 1 : θ ∈ [-14,5° ; 45,5°[ -> côtés 0° (E0) et 30° (E1), coins 15° et 45°
)
ANCRE = (0.0, F)               # sommet de l'hexagone central à θ = 90° (hors des pièces du Coeur Base)
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
CLASSE_VERS_CLE = {v.split('.')[-1]: k for k, v in C.items()}
NOMS = {
    'fond': 'Fondation métal', 'fond_tri': 'Fondation triangle métal', 'plafond': 'Plafond métal',
    'plafond_tri': 'Plafond triangle métal', 'mur': 'Mur métal', 'cadre_double': 'Cadre de porte double métal',
    'pilier': 'Pilier métal', 'trappe': 'Plafond à trappe métal', 'demi_pilier': 'Demi-pilier métal',
    'rampe': 'Rampe inclinée métal (Sloped Railing)', 'escalier': 'Escalier métal (Coeur Base)',
    'porte_secrete': 'Porte secrète métal (Coeur Base)', 'coffre': 'Coffre (Coeur Base)',
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
        self.groupe, self.groupes = 'part', []      # 'part' : réparti dans les 6 parts ; 'noyau' : posé une fois

    def add(self, cle, x, y, z_tpl, yaw, Z=None, repere='', pitch=0.0, roll=0.0):
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

    def add_brut(self, entree, cle, Z, repere):
        """Reprend une entrée d'un template existant telle quelle (skin, couleurs, nom de coffre conservés)."""
        self.entries.append(entree)
        l, r = entree['loc'], entree['rot']
        self.lignes.append((cle, l['x'], l['y'], Z, r['yaw'], repere))
        self.phases.append(self.phase)
        self.groupes.append(self.groupe)

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
    """Repère : 2 demi-piliers empilés (phase P1) ou 1 demi-pilier posé dessus (autres phases).

    Il est placé au sommet de l'hexagone central à θ = 90° (0 ; 300) et non au centre exact, occupé par la porte
    secrète centrale du Coeur Base.
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


def rang_dodeca(A, decalage=0.0):
    """Pièces de 300 le long d'un dodécagone régulier d'apothème A (bord bas d'un toit, ligne de murs...).

    Renvoie (x, y, normale, côté, index) des centres situés à A - decalage. Le nombre de pièces par côté est
    arrondi au supérieur : les pièces se chevauchent aux arêtes au lieu de laisser un jour.
    """
    n = math.ceil(2 * A * TAN15 / F - 1e-6)
    out = []
    for k in range(12):
        nx, ny = vec(30 * k)
        dx, dy = -ny, nx
        for i in range(n):
            t = (-n / 2 + i + 0.5) * F
            out.append(((A - decalage) * nx + t * dx, (A - decalage) * ny + t * dy, 30 * k, k, i))
    return out


def rang_rampes(t, A_bas, Z_bas, repere):
    """Un rang de rampes inclinées (Sloped Railing, tours 1201 / 1809) sur une pente à 45° qui part de l'apothème
    A_bas à la cote Z_bas et monte vers le centre. Aucun toit incliné : on ne tient pas debout sur des lames.

    Sur chaque côté, les rampes sont au pas de 300 UU (t = 0, ±300…). Les rangs d'une même pente retombent sur les
    mêmes t : chaque lame est continue du bas jusqu'en haut. Une lame peut dépasser l'arête du côté de 150 UU au
    plus, si bien que l'écart entre lames reste ≤ 300 UU aux 12 arêtes.
    Cotes relevées sur la tour 1201 : pivot au milieu de la rampe (150 UU en retrait du bas) et à z template
    Z_bas + 290 ; yaw = normale du côté - 90° (montée vers le centre).
    """
    a = A_bas - F / 2
    n = int((a * TAN15 + F / 2) // F + 1e-9)
    for k in range(12):
        nx, ny = vec(30 * k)
        dx, dy = -ny, nx
        for i in range(-n, n + 1):
            t.add('rampe', a * nx + i * F * dx, a * ny + i * F * dy, Z_bas + Z_TPL + 200, 30 * k - 90,
                  Z=Z_bas, repere=f'{repere} c{k} t{i}')


def toit_rampes(t, A, Zd, repere):
    """Toit en rampes inclinées sur un plancher fermé Zd de contour D(A), jusqu'au faîtage (12 pans).

    Le rang de rive (150 UU devant le bord du plancher, comme sur la tour 1201) est la casquette du module 04 :
    le toit commence donc au bord du plancher. Renvoie la cote du sommet.
    """
    j = 0
    while A - j * F - F / 2 > 0:
        rang_rampes(t, A - j * F, Zd + j * F, f'{repere} r{j}')
        j += 1
    return Zd + A - 50


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


# ---------------------------------------------------------------- Coeur Base
def charger_coeur(p):
    chemin = p['coeur'] if os.path.isabs(p['coeur']) else os.path.join(RACINE, p['coeur'])
    d = json.load(open(chemin, encoding='utf-8'))
    rot = p['coeur_rotation']
    c, s = vec(rot)
    out = []
    for e in d['entries']:
        cls = e['structure'].split('.')[-1]
        e = copy.deepcopy(e)
        x, y = e['loc']['x'], e['loc']['y']
        e['loc']['x'], e['loc']['y'] = round(x * c - y * s, 3), round(x * s + y * c, 3)
        e['rot']['yaw'] = round(ecart(e['rot']['yaw'] + rot, 0), 3)
        out.append((CLASSE_VERS_CLE.get(cls), cls, e))
    return d, out


def cellule_escalier(e):
    """Emprise 300 × 300 de l'escalier du Coeur Base (axes = yaw de l'escalier)."""
    nx, ny = vec(e['rot']['yaw'])
    dx, dy = -ny, nx
    x0, y0 = e['loc']['x'], e['loc']['y']
    return [(x0 + u * nx + v * dx, y0 + u * ny + v * dy) for u, v in ((-150, -150), (150, -150), (150, 150), (-150, 150))]


# ---------------------------------------------------------------- modules
def module_sol(p, extension_seule=False):
    pieces, contours = pavage(p['anneaux_total'])
    nom = '01b Extension sol D4->D8' if extension_seule else '01 Sol D8 complet'
    t = Template(nom, 'Pavage carres+triangles en etoile, Ø30 (D8). Bord abaisse en 2 paliers : anneau 14 (Ø26-Ø28) a '
                      f"-{p['decaissement']:.0f} UU, anneau 15 (Ø28-Ø30) a -{2 * p['decaissement']:.0f} UU. "
                      "Origine = centre de l'etoile.")
    if not extension_seule:
        ancre(t, empilee=True)
    t.phase = 'P1'
    for pc in pieces:
        if extension_seule and pc['anneau'] <= p['anneau_pod']:
            continue
        Z = cote_anneau(p, pc['anneau'])
        cle = 'fond' if pc['type'] == 'carre' else 'fond_tri'
        t.add(cle, pc['x'], pc['y'], Z + Z_TPL - 50, pc['yaw'], Z=Z,
              repere=f"anneau {pc['anneau']} cote {pc['cote']} n{pc['idx']}")
    if extension_seule:
        # tuile d'accroche : premier carré de l'anneau 8 sur le côté θ=30°
        for i, e in enumerate(t.lignes):
            if e[5].startswith('anneau 8 cote 1 n0'):
                t.snap = [i]
                break
    return t, pieces, contours


def module_pod(p, contours):
    t = Template('02 Pod central atelier', 'Coeur Base au centre (escalier prolonge jusqu\'a la mezzanine), mur de pod '
                                         'D4 (48 murs/niveau), piliers porteurs, mezzanine Z1800, plancher de toit '
                                         'Z2400 et toit en rampes inclinees (tours 1201/1809) sur toute la cage D5.')
    ancre(t)
    d4 = contours[p['anneau_pod']]
    zmez = p['mezzanine']
    # Coeur Base : tout sauf ses 10 fondations (grille tournée de -30°, incompatible avec l'étoile qui les remplace)
    _, coeur = charger_coeur(p)
    escalier = None
    t.groupe = 'noyau'
    for cle, cls, e in coeur:
        if cls == 'Floor_Metal_C' or cle == 'coffre':     # fondations remplacées par l'étoile ; coffre = équipement
            continue
        z = e['loc']['z']
        t.phase = 'P2' if z <= 240 else 'P3'
        t.add_brut(e, cle, z - Z_TPL - (150 if cle in ('mur', 'porte_secrete', 'escalier') else 0),
                   f'coeur {cls}')
        if cle == 'escalier':
            escalier = e
    # escalier prolongé de Z300 à la mezzanine (empilé sur celui du Coeur Base)
    t.phase = 'P3'
    nb_marches = int(zmez // F)
    for niv in range(1, nb_marches):
        e = copy.deepcopy(escalier)
        e['loc']['z'] = escalier['loc']['z'] + niv * F
        t.add_brut(e, 'escalier', niv * F, f'escalier prolonge niv{niv}')
    t.groupe = 'part'
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
            t.add(cle, x, y, Zb + Z_TPL + F / 2, nu, Z=Zb, repere=f'pod niv{niv} c{k} p{i}')
    # piliers : couronne PA aux sommets de D2 (Z0 -> 2400), couronne PB aux sommets de D1 (mezzanine -> 2400)
    for nom, n, Zb, Zh in (('PA', 2, 0.0, Ztop), ('PB', 1, zmez, Ztop)):
        R = rayon_coin(n)
        for k in range(12):
            cx, cy = vec(15 + 30 * k)
            Z = Zb
            while Z + F <= Zh + 1e-6:
                t.phase = 'P2' if Z < zmez else 'P6'
                t.add('pilier', R * cx, R * cy, Z + Z_TPL + F / 2, 0, Z=Z, repere=f'pilier {nom}{k}')
                Z += F
            if Z < Zh - 1:
                t.phase = 'P6'
                t.add('demi_pilier', R * cx, R * cy, Z + Z_TPL + F / 4, 0, Z=Z, repere=f'pilier {nom}{k} (demi)')
    # mezzanine Z1800 : centre + anneaux 1..7 en plafonds, trémie = pièces traversées par la cage d'escalier
    cellule = cellule_escalier(escalier)
    pieces, _ = pavage(p['anneau_pod'], centre=True)
    t.phase = 'P3'
    tremie = []
    for pc in pieces:
        if se_coupent(polygone(pc), cellule):
            tremie.append(pc)
            continue
        cle = 'plafond' if pc['type'] == 'carre' else 'plafond_tri'
        t.groupe = 'noyau' if pc['anneau'] <= 1 else 'part'     # centre de la mezzanine (trémie) : noyau
        t.add(cle, pc['x'], pc['y'], zmez + Z_TPL, pc['yaw'], Z=zmez, repere=f"mezzanine anneau {pc['anneau']}")
    t.groupe = 'part'
    # plancher de toit Z2400 (centre + anneaux 1..7, sans trémie) : il ferme le pod au niveau du toit de cage
    t.phase = 'P6'
    for pc in pieces:
        cle = 'plafond' if pc['type'] == 'carre' else 'plafond_tri'
        t.add(cle, pc['x'], pc['y'], Ztop + Z_TPL, pc['yaw'], Z=Ztop, repere=f"plancher de toit anneau {pc['anneau']}")
    # toit en rampes inclinées sur tout le bloc central (pod + cage, contour D5), à la place du cône et de la reprise
    Zsommet = toit_rampes(t, apo(5), Ztop, 'toit rampes')
    return t, dict(Zsommet=Zsommet, Ztoit=Ztop, coeur=coeur, escalier=escalier, cellule=cellule, tremie=tremie)


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
    t = Template('03 Rive, colonnade, pente de glisse et overhang',
                 f"Mur de rive D7 ({p['rive_niveaux']} niveaux), colonnade circulaire, {p['rangs_pente_A']} rangs de "
                 f"rampes inclinees jusqu'a la cage, overhang {2 + p['debord']} rangs de rampes (dont {p['debord']} "
                 "au-dela de la plateforme), mur de jupe.")
    ancre(t)
    d7 = contours[p['anneau_rive']]
    murs = cotes_contour(d7)
    sas = None                                  # pas de sas : 6 parts égales (accès par le Tek Teleporter / à ouvrir à la main)
    t.phase = 'P2'
    for niv in range(p['rive_niveaux']):
        Zb = niv * F
        for j, (x, y, nu, k, i) in enumerate(murs):
            if niv == 1 and j in tesla_murs:
                continue                       # emplacement laissé libre : mur de chaume + Tesla (phase P7)
            cle = 'cadre_double' if (niv == 0 and j == sas) else 'mur'
            t.add(cle, x, y, Zb + Z_TPL + F / 2, nu, Z=Zb, repere=f'rive niv{niv} c{k} p{i}')
    # colonnade circulaire sous la pente A
    col = colonnade(p)
    for c in col['colonnes']:
        for cle, Z in c['elements']:
            dz = F / 2 if cle == 'pilier' else F / 4
            t.add(cle, c['x'], c['y'], Z + Z_TPL + dz, c['theta'], Z=Z, repere=f"colonnade θ{c['theta']:.2f}")
    # pente A : de la rive vers la cage
    A7 = apo(7)
    Zr = p['rive_niveaux'] * F
    t.phase = 'P4'
    for j in range(p['rangs_pente_A']):
        rang_rampes(t, A7 - j * F, Zr + j * F, f'pente A r{j}')
    # overhang : 2 rangs au-dessus du décaissement + 'debord' rangs dans le vide
    for j in range(1, 3 + p['debord']):
        rang_rampes(t, A7 + j * F, Zr - j * F, f'overhang r-{j}')
    A_bout = A7 + (2 + p['debord']) * F
    Z_bout = Zr - (2 + p['debord']) * F
    jupe = None
    if p['jupe'] and p['debord'] >= 2:          # avec 1 seul rang dans le vide, la chute frôlerait les tourelles
        A_j = A7 + 2 * F
        nb = int(round((Zr - 2 * F - Z_bout) / F))
        for niv in range(nb):
            Zb = Z_bout + niv * F
            for x, y, nu, k, i in rang_dodeca(A_j):
                t.add('mur', x, y, Zb + Z_TPL + F / 2, nu, Z=Zb, repere=f'jupe mur niv{niv} c{k} p{i}')
        # pas de plafond sous l'overhang : ce qui passe entre les rampes doit tomber dans le vide, pas sur un palier
        # au-dessus des tourelles de jupe
        jupe = dict(A=A_j, Z=Z_bout)
    return t, murs, sas, dict(A_bout=A_bout, Z_bout=Z_bout), jupe, col


def module_cage(p, contours):
    t = Template('04 Cage a tourelles et casquette',
                 'Fut D5, galerie 2 niveaux : L1 = 60 emplacements de tourelles (murs de chaume en phase P7), '
                 'L2 = 60 double doorframes ; planchers anneaux 8-9, casquette (le toit en rampes est au module 02).')
    ancre(t)
    d5 = contours[p['anneau_cage']]
    zmez = p['mezzanine']
    # fût : murs D5 de Z0 à la galerie, 2 portes au sol (θ=90/270, index 2)
    t.phase = 'P2'
    for niv in range(int(zmez // F)):
        Zb = niv * F
        for x, y, nu, k, i in cotes_contour(d5):
            cle = 'cadre_double' if (niv == 0 and k % 2 == 1 and i == 2) else 'mur'
            t.add(cle, x, y, Zb + Z_TPL + F / 2, nu, Z=Zb, repere=f'fut niv{niv} c{k} p{i}')
    # planchers de galerie : anneaux 8 et 9 en plafonds, à chaque niveau + toit de cage
    pieces, _ = pavage(p['anneau_cage'], centre=False)
    gal = [pc for pc in pieces if pc['anneau'] > p['anneau_pod']]
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
        t.add('cadre_double', x, y, Zb + Z_TPL + F / 2, nu, Z=Zb, repere=f'cage L2 c{k} p{i}')
    # casquette (porte-à-faux) ; au-dessus, le toit en rampes du bloc central (module 02) remplace la reprise
    A5 = apo(5)
    Ztop = zmez + p['cage_niveaux'] * F
    for j in range(p['casquette'], 0, -1):
        rang_rampes(t, A5 + j * F, Ztop - j * F, f'casquette r-{j}')
    return t, gal


# gabarits de réservation dans le hall du pod (Z0 -> 1800) : (nom, θ, apothème du centre, largeur, profondeur, murs)
GABARITS = [
    ('Réplicateur Tek', 0, 1650, 900, 600, 3),
    ('Générateur Tek n°1 (ateliers)', 60, 1800, 300, 300, 1),
    ('Forge à vapeur', 120, 1650, 900, 900, 3),
    ('Labo de fortune (Megalab)', 240, 1650, 600, 600, 2),
    ('3 stockages dédiés', 300, 1750, 900, 300, 2),
]
# générateurs Tek de la galerie (sur l'anneau 8, niveau L1) et générateurs électriques de secours (attique A,
# entre le fût et la colonnade, hors de l'axe des portes 90°/270°)
GENERATEURS = [('Générateur Tek n°1 (hall)', 60, 1800.0, 0.0), ('Générateur Tek n°2 (mezzanine)', 180, 900.0, 1800.0)]


def equipements(infos_pod, contours):
    """Positions des équipements hors plan : machines du hall, générateurs, 20 coffres-forts, 20 stockages dédiés.

    Mezzanine : 36 emplacements contre la face intérieure du mur de pod (positions 0, 2 et 3 de chaque côté ; la
    position 1 est l'accès galerie) -> 19 coffres-forts + 17 stockages dédiés en alternance. Le 20e coffre-fort est
    celui du Coeur Base (position d'origine) ; les 3 derniers stockages dédiés vont dans le hall (θ 300°).
    """
    out = []
    for nom, th, A, lg, pf, hm in GABARITS:
        cle = {'Réplicateur Tek': 'replicateur', 'Forge à vapeur': 'forge_vapeur',
               'Labo de fortune (Megalab)': 'megalab'}.get(nom)
        if cle:
            out.append(dict(cle=cle, x=A * vec(th)[0], y=A * vec(th)[1], Z=0.0, yaw=th + 180, lieu='hall'))
        elif nom.startswith('3 stockages'):
            nx, ny = vec(th)
            dx, dy = -ny, nx
            for t in (-300, 0, 300):
                out.append(dict(cle='stockage_dedie', x=A * nx + t * dx, y=A * ny + t * dy, Z=0.0, yaw=th + 180,
                                lieu='hall'))
    for nom, th, A, Z in GENERATEURS:
        out.append(dict(cle='generateur_tek', x=A * vec(th)[0], y=A * vec(th)[1], Z=Z, yaw=th + 180,
                        lieu='hall' if Z == 0 else 'mezzanine'))
    vault = next(e for cle, cls, e in infos_pod['coeur'] if cle == 'coffre')
    out.append(dict(cle='coffre_fort', x=vault['loc']['x'], y=vault['loc']['y'], Z=0.0, yaw=vault['rot']['yaw'],
                    lieu='Coeur Base (Matiere Premiere 1)'))
    places = sorted(((x, y, nu, k, i) for x, y, nu, k, i in cotes_contour(contours[7]) if i != 1),
                    key=lambda m: math.degrees(math.atan2(m[1], m[0])) % 360)
    for n, (x, y, nu, k, i) in enumerate(places):
        nx, ny = vec(nu)
        cle = 'coffre_fort' if (n % 2 == 0 or n == len(places) - 1) else 'stockage_dedie'
        out.append(dict(cle=cle, x=x - 150 * nx, y=y - 150 * ny, Z=1800.0, yaw=nu + 180, lieu='mezzanine'))
    return out


def tableau_anneaux(p):
    pieces, contours = pavage(p['anneaux_total'])
    lignes = []
    for r in range(1, p['anneaux_total'] + 1):
        pr = [pc for pc in pieces if pc['anneau'] == r]
        a, L = contours[r]
        zone = ('pod' if r <= p['anneau_pod'] else f"palier {r - p['anneau_rive']}" if r > p['anneau_rive']
                else 'couronne')
        lignes.append(dict(anneau=r, carres_sur='E0 (0°,60°…)' if r % 2 else 'E1 (30°,90°…)',
                           carres=sum(pc['type'] == 'carre' for pc in pr),
                           tri_ext=sum(pc['type'] == 'tri' and pc['idx'] < L[pc['cote']] - 1 for pc in pr),
                           triangles=sum(pc['type'] == 'tri' for pc in pr),
                           par_cote_E0=L[0], par_cote_E1=L[1], apo_E0=round(a[0], 1), apo_E1=round(a[1], 1),
                           zone=zone, Z=cote_anneau(p, r)))
    return lignes


PHASES = {'P1': 'Fondations (sol D8 + 2 paliers de bord)',
          'P2': 'Piliers et murs porteurs (Coeur Base niv. 1, piliers PA, colonnade, pod, fut, rive)',
          'P3': 'Plafonds intermediaires (Coeur Base niv. 2, escalier, mezzanine + galerie Z1800)',
          'P4': 'Rampes de glisse : pente A et overhang en rampes inclinees, mur de jupe',
          'P5': 'Cage : planchers 2100/2400, double doorframes L2, casquette en rampes',
          'P6': 'Pod haut et toit : murs 1800-2400, piliers hauts, plancher de toit Z2400, rampes inclinees',
          'P7': 'Tourelles verticales et leurs murs de chaume de pose (scenario B)'}


def templates_phases(modules):
    out = {}
    for ph, nom in PHASES.items():
        t = Template(f'{ph} {nom}', f'Phase {ph} de la notice de montage.')
        ancre(t, empilee=(ph == 'P1'))
        out[ph] = t
    for _, m in modules:
        for e, ph, ligne in zip(m.entries, m.phases, m.lignes):
            if ph in out:
                out[ph].entries.append(e)
                out[ph].lignes.append(ligne)
                out[ph].phases.append(ph)
    return out


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
    """Murs de chaume suspendus sous le mur de jupe (4 518,7 ; Z -900 -> -600).

    Côtés pairs : 3 tourelles (extérieure, intérieure, extérieure) ; côtés impairs : 2 intérieures.
    Les « extérieures » sont sur la face côté mer ; les « intérieures » sur la face côté piton, d'où elles voient le
    dessous de la plateforme.
    """
    out = []
    Zb = jupe['Z'] - F
    for k in range(12):
        nx, ny = vec(30 * k)
        dx, dy = -ny, nx
        motif = [(-600, 'ext'), (0, 'int'), (600, 'ext')] if k % 2 == 0 else [(-600, 'int'), (600, 'int')]
        for i, (tt, sens) in enumerate(motif):
            A = jupe['A']
            sortie = 30 * k if sens == 'ext' else 30 * k + 180
            out.append(emplacement(A * nx + tt * dx, A * ny + tt * dy, Zb, sortie,
                                   'JUPE-ext' if sens == 'ext' else 'JUPE-int', k, i))
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


def matrice(p, contours, murs, tesla_murs, jupe):
    nH, nT, nS = p['inventaire']
    L1 = sorted(emplacements_cage(p, contours), key=angle)
    J = sorted(emplacements_jupe(p, jupe), key=angle) if jupe else []
    S = sorted((emplacement(murs[j][0], murs[j][1], F, murs[j][2], 'RIVE', murs[j][3], murs[j][4]) for j in tesla_murs),
               key=angle)
    # L1 : Tek / Heavy alternées (côté E0 : T H T H T ; côté E1 : H T H T H) = 5 Tek + 5 Heavy par part
    for s in L1:
        s['type'] = 'tek' if (s['idx'] % 2 == 0) == (s['cote'] % 2 == 0) else 'heavy'
    for s in J:
        s['type'] = 'heavy'
    for s in S:
        s['type'] = 'tesla'
    besoin = {k: sum(1 for s in L1 + J + S if s['type'] == k) for k in ('heavy', 'tek', 'tesla')}
    assert besoin['heavy'] <= nH and besoin['tek'] <= nT and besoin['tesla'] <= nS, besoin
    # priorités : 1 jupe (sous-plateforme) 2 Tek L1 3 Tesla (pied de rive) 4 Heavy L1
    groupes = [('P1 jupe Heavy', J), ('P2 L1 Tek', [s for s in L1 if s['type'] == 'tek']),
               ('P3 rive Tesla', S), ('P4 L1 Heavy', [s for s in L1 if s['type'] == 'heavy'])]
    ordre = []
    for nom, g in groupes:
        for i in ordre_vdc(len(g)):
            g[i]['priorite'] = nom
            ordre.append(g[i])
    for n, s in enumerate(ordre, 1):
        s['ordre'] = n
    compte, posees = 0, []
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
    if p['jupe'] and p['debord'] >= 2:
        segs.append(((A7 + 2 * F, ob['Z_bout']), (A7 + 2 * F, Zr - 2 * F)))   # mur de jupe
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


# ---------------------------------------------------------------- découpage en 6 parts égales
ORDRE_PHASES = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7']


def numero_part(p, x, y):
    th = (math.degrees(math.atan2(y, x)) - p['part_debut'] + 1e-6) % 360
    return int(th // (360 / p['parts']))


def decouper(p, modules):
    """Répartit les entrées 'part' des modules dans les 6 parts (par l'angle de leur centre) ; 'noyau' à part."""
    n = p['parts']
    struct = [[] for _ in range(n)]
    tour = [[] for _ in range(n)]
    noyau = []
    for _, m in modules:
        for e, ph, gr, ligne in zip(m.entries, m.phases, m.groupes, m.lignes):
            if ph is None:                      # ancres des modules
                continue
            if gr == 'noyau':
                noyau.append((ph, e, ligne))
                continue
            k = numero_part(p, e['loc']['x'], e['loc']['y'])
            (tour if ph == 'P7' else struct)[k].append((ph, e, ligne))
    out = {}
    for k in range(n):
        a0 = p['part_debut'] + k * 360 / n
        for genre, liste in (('structure', struct[k]), ('tourelles', tour[k])):
            t = Template(f'Part {k + 1}-{n} {genre} (theta {a0:.0f} a {a0 + 360 / n:.0f} deg)',
                         f'Part {k + 1} sur {n} : {genre}. Les {n} parts sont identiques a une rotation de '
                         f'{360 / n:.0f} deg pres ; toutes se posent sur la pile d\'ancrage (0 ; 300).')
            ancre(t, empilee=(k == 0 and genre == 'structure'))
            for ph, e, ligne in sorted(liste, key=lambda v: ORDRE_PHASES.index(v[0])):
                t.phase = ph
                t.entries.append(e)
                t.lignes.append(ligne)
                t.phases.append(ph)
                t.groupes.append('part')
            out[(k, genre)] = t
    t = Template('Noyau central (pose une fois)', 'Coeur Base sans fondations ni coffre, escalier prolonge, centre de la '
                                                 'mezzanine avec tremie.')
    ancre(t)
    for ph, e, ligne in sorted(noyau, key=lambda v: ORDRE_PHASES.index(v[0])):
        t.entries.append(e)
        t.lignes.append(ligne)
        t.phases.append(ph)
        t.groupes.append('noyau')
    out['noyau'] = t
    return out


def verifier_parts(p, parts):
    """Chaque part, tournée de -60°·k, doit retrouver exactement la part 1 (classe, x, y, z à 1 UU près)."""
    n = p['parts']

    def cles(t, rot):
        c, s_ = vec(-rot)
        out = {}
        for e, ligne in zip(t.entries, t.lignes):
            if ligne[5].startswith('ancre'):
                continue
            x, y = e['loc']['x'], e['loc']['y']
            xr, yr = x * c - y * s_, x * s_ + y * c
            out.setdefault((e['structure'], round(e['loc']['z'])), []).append((xr, yr))
        return out

    for genre in ('structure', 'tourelles'):
        ref = cles(parts[(0, genre)], 0)
        for k in range(1, n):
            autre = cles(parts[(k, genre)], k * 360 / n)
            assert ref.keys() == autre.keys(), (genre, k)
            for cle, pts in ref.items():
                restants = list(autre[cle])
                assert len(restants) == len(pts), (genre, k, cle)
                for x, y in pts:
                    j = min(range(len(restants)), key=lambda j: math.hypot(restants[j][0] - x, restants[j][1] - y))
                    assert math.hypot(restants[j][0] - x, restants[j][1] - y) < 1.0, (genre, k, cle, x, y)
                    restants.pop(j)
    hors_ancre = {g: sum(1 for l in parts[(0, g)].lignes if not l[5].startswith('ancre')) for g in ('structure', 'tourelles')}
    print(f"  {n} parts identiques à une rotation près : structure ({hors_ancre['structure']} pièces) "
          f"et tourelles ({hors_ancre['tourelles']} entrées) par part")


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
    # Coeur Base dans la couronne de piliers PA et hors de l'ancre
    rmax = max(math.hypot(e['loc']['x'], e['loc']['y']) for cle, cls, e in infos_pod['coeur'] if cls != 'Floor_Metal_C')
    msgs.append(f'Coeur Base : rayon max {rmax:.0f} UU < piliers PA {rayon_coin(2):.0f} UU')
    assert rmax < rayon_coin(2) - 100
    d_ancre = min(math.hypot(e['loc']['x'] - ANCRE[0], e['loc']['y'] - ANCRE[1])
                  for cle, cls, e in infos_pod['coeur'] if cls != 'Floor_Metal_C' and e['loc']['z'] <= 240)
    msgs.append(f'Ancre (0 ; 300) : {d_ancre:.0f} UU de la pièce la plus proche du Coeur Base au niveau 1')
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


def plans(rep, p, pieces, ordre, ob, jupe, infos_pod, col):
    plt, MPoly = _mpl()
    if not plt:
        return
    # --- plan de calpinage
    fig, ax = plt.subplots(figsize=(13, 13))
    for pc in pieces:
        r = pc['anneau']
        if r > p['anneau_rive']:
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
                 f"gris foncé = palier 15 (-{2 * p['decaissement']:.0f})", fontsize=10)
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
    ax.add_patch(plt.Rectangle((0, 0), 900, 600, fc='#ffd166', ec='#9c6644', lw=1.5, label='Coeur Base (2 niveaux)'))
    ax.plot([150, 150], [0, zmez], color='#9c6644', lw=4, ls=(0, (1, 1)), label='escalier prolongé jusqu\'à Z1800')
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
    ax.plot([A7 - p['rangs_pente_A'] * F + 50, ob['A_bout'] + 50], [Zr + p['rangs_pente_A'] * F + 50, ob['Z_bout'] + 50],
            color='#e07a2f', label='pente A + overhang : rampes inclinées', **lame)
    ax.plot([A5 + p['casquette'] * F + 50, A5 + 50], [Zc - p['casquette'] * F + 50, Zc + 50], color='#7b2cbf',
            label='casquette : rampes inclinées', **lame)
    ax.plot([A5 + 50, 150], [Zc + 50, Zsommet], color='#b00', label='toit : rampes inclinées (tours 1201/1809)', **lame)
    if jupe:
        ax.plot([jupe['A'], jupe['A']], [jupe['Z'], Zr - 2 * F], color='#555', lw=2, label='mur de jupe')
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
    styles = {'heavy': ('s', '#c0392b'), 'tek': ('^', '#2471a3'), 'tesla': ('*', '#d4ac0d')}
    for s in ordre:
        if not s['posee']:
            continue
        mk, co = styles[s['type']]
        ax.plot(s['x'], s['y'], mk, color=co, ms=7, mec='k' if s['couche'] == 'JUPE-int' else co)
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
    ax.plot([R8 * c for c, s_ in pts], [R8 * s_ for c, s_ in pts], color='#2a9d8f', lw=1.2, ls='--',
            label='boucle de câbles galerie (Z1800, anneau 8)')
    for k in range(12):
        c, s_ = vec(15 + 30 * k)
        r2 = (apo(7) + 600) / math.cos(math.radians(15))
        ax.plot([R8 * c, r2 * c], [R8 * s_, r2 * s_], color='#2a9d8f', lw=0.8, ls=':')
    for nom, th, A, Z in GENERATEURS:
        c, s_ = vec(th)
        ax.plot(A * c, A * s_, 'D', color='#2a9d8f' if 'Tek' in nom else '#6c757d', ms=10, mec='k')
    ax.plot([], [], 'D', color='#2a9d8f', mec='k', label='Tek Generator (galerie, Z1800)')
    ax.plot([], [], 'D', color='#6c757d', mec='k', label='Générateur électrique de secours (attique, Z0)')
    for nom, (mk, co) in styles.items():
        ax.plot([], [], mk, color=co, label=NOMS[nom])
    ax.plot([], [], 's', color='#c0392b', mec='k', label='Heavy de jupe tournée vers le piton (bord noir)')
    ax.set_aspect('equal')
    ax.set_title('Tourelles verticales — scénario B (100 posées) — trait = sens de tir ; numéros = ordre de pose '
                 '(jupe et Tesla)', fontsize=10)
    ax.legend(loc='lower left', fontsize=8)
    fig.savefig(os.path.join(rep, 'plan_tourelles.png'), dpi=80, bbox_inches='tight')
    plt.close(fig)


def plan_pod(rep, p, infos_pod):
    plt, MPoly = _mpl()
    if not plt:
        return
    fig, ax = plt.subplots(figsize=(11, 11))
    pieces, contours = pavage(p['anneau_pod'])
    for pc in pieces:
        ax.add_patch(MPoly(polygone(pc), closed=True, fc='#f6e3d0' if pc['type'] == 'tri' else '#efcfae',
                           ec='#bbb', lw=0.3))
    for x, y, nu, k, i in cotes_contour(contours[7]):
        porte = k % 2 == 1 and i == 1
        ax.plot(x, y, 's', color='#2a9d8f' if porte else '#b00', ms=9 if porte else 4)
    Zt = p['pod_niveaux'] * F
    for n, coul, nom in ((2, '#000', f'piliers PA (Z0 -> {Zt:.0f})'), (1, '#666', f"piliers PB (Z{p['mezzanine']:.0f} -> {Zt:.0f})")):
        R = rayon_coin(n)
        pts = [vec(15 + 30 * k) for k in range(12)]
        ax.plot([R * c for c, s_ in pts], [R * s_ for c, s_ in pts], 'o', color=coul, ms=9, label=nom)
    # Coeur Base (niveau 1)
    for cle, cls, e in infos_pod['coeur']:
        if e['loc']['z'] > 240 or cle not in ('mur', 'porte_secrete'):
            continue
        nx, ny = vec(e['rot']['yaw'])
        dx, dy = -ny, nx
        x0, y0 = e['loc']['x'], e['loc']['y']
        ax.plot([x0 - 150 * dx, x0 + 150 * dx], [y0 - 150 * dy, y0 + 150 * dy],
                color='#9c6644' if cle == 'mur' else '#e63946', lw=3 if cle == 'mur' else 4)
    cel = infos_pod['cellule']
    ax.add_patch(MPoly(cel, closed=True, fc='#ffd166', ec='#9c6644', lw=1.5, alpha=.8))
    ax.annotate('escalier\n(Z0 → 1800)', (infos_pod['escalier']['loc']['x'], infos_pod['escalier']['loc']['y']),
                ha='center', va='center', fontsize=7)
    for pc in infos_pod['tremie']:
        ax.add_patch(MPoly(polygone(pc), closed=True, fc='none', ec='#7b2cbf', lw=1.5, ls='--'))
    ax.plot([], [], color='#9c6644', lw=3, label='Coeur Base : murs (2 niveaux)')
    ax.plot([], [], color='#e63946', lw=4, label='Coeur Base : portes secrètes')
    ax.plot([], [], color='#7b2cbf', lw=1.5, ls='--', label='trémie de la mezzanine Z1800 (au-dessus de l\'escalier)')
    ax.plot(*ANCRE, 'k+', ms=12, label='ancre Template Hammer (0 ; 300)')
    for nom, th, A, lg, pf, hm in GABARITS:
        nx, ny = vec(th)
        dx, dy = -ny, nx
        cx, cy = A * nx, A * ny
        coins = [(cx + u * nx + v * dx, cy + u * ny + v * dy) for u, v in
                 ((-pf / 2, -lg / 2), (pf / 2, -lg / 2), (pf / 2, lg / 2), (-pf / 2, lg / 2))]
        ax.add_patch(MPoly(coins, closed=True, fc='#3f88c5', alpha=.35, ec='#1d4e89', lw=1.5))
        ax.annotate(f'{nom}\n{lg / F:.0f}×{pf / F:.0f} F, {hm} murs', (cx, cy), ha='center', va='center', fontsize=8)
    ax.plot([], [], 's', color='#2a9d8f', ms=9, label='portes doubles du hall (1 par part)')
    ax.plot([], [], 's', color='#b00', ms=4, label='mur de pod D4 (48 / niveau)')
    ax.set_aspect('equal')
    ax.set_xlim(-2600, 2600)
    ax.set_ylim(-2600, 2600)
    ax.set_title('Pod central — hall Z0→1800 : Coeur Base au centre, piliers, portes et gabarits machines', fontsize=10)
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
        nx, ny = vec(yaw + 90)                   # sens de montée (vers le centre)
        ax.plot([x - 150 * nx, x + 150 * nx], [y - 150 * ny, y + 150 * ny], color=cmap((Z - zmin) / (zmax - zmin)),
                lw=1.2)
    for m, coul, nom in ((4, '#b00', 'D4 mur de pod'), (5, '#070', 'D5 cage'), (7, '#000', 'D7 rive'),
                         (8, '#555', 'D8 bord de plateforme')):
        _dodeca(ax, m, color=coul, lw=1, label=nom)
    ax.plot([], [], color=cmap(0.0), lw=2, label=f'rampe la plus basse (Z {zmin:.0f}, bout de l\'overhang)')
    ax.plot([], [], color=cmap(1.0), lw=2, label=f'rampe la plus haute (Z {zmax:.0f}, faîtage)')
    ax.set_aspect('equal')
    ax.set_xlim(-5400, 5400)
    ax.set_ylim(-5400, 5400)
    ax.set_title(f'Rampes inclinées (Sloped Railing), aucun toit incliné : {len(rampes)} rampes en lames au pas de '
                 '300 UU — toit, casquette, pente A et overhang', fontsize=10)
    ax.legend(loc='lower left', fontsize=8)
    fig.savefig(os.path.join(rep, 'plan_rampes.png'), dpi=80, bbox_inches='tight')
    plt.close(fig)


def plan_parts(rep, p, parts, col):
    plt, MPoly = _mpl()
    if not plt:
        return
    couleurs = ['#e07a2f', '#3f88c5', '#2a9d8f', '#7b2cbf', '#d4ac0d', '#c0392b']
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(22, 11))
    for k in range(p['parts']):
        t = parts[(k, 'structure')]
        for e, (cle, x, y, Z, yaw, r) in zip(t.entries, t.lignes):
            if cle in ('fond', 'fond_tri'):
                pc = dict(type='carre' if cle == 'fond' else 'tri', x=x, y=y, yaw=yaw)
                ax1.add_patch(MPoly(polygone(pc), closed=True, fc=couleurs[k], ec='#333', lw=0.2, alpha=.75))
        a0 = p['part_debut'] + k * 60
        c, s_ = vec(a0)
        ax1.plot([0, 5300 * c], [0, 5300 * s_], color='k', lw=1.5)
        cm, sm = vec(a0 + 30)
        ax1.annotate(f'Part {k + 1}', (3000 * cm, 3000 * sm), ha='center', va='center', fontsize=14,
                     fontweight='bold', color='w')
    ax1.plot(*ANCRE, 'k+', ms=14)
    ax1.set_aspect('equal')
    ax1.set_xlim(-5400, 5400)
    ax1.set_ylim(-5400, 5400)
    ax1.set_title(f"Les 6 parts égales (sol) — limites θ = {p['part_debut']}° + 60°·k ; + = pile d'ancrage")
    # part 1 détaillée
    t = parts[(0, 'structure')]
    for e, (cle, x, y, Z, yaw, r) in zip(t.entries, t.lignes):
        if cle in ('fond', 'fond_tri'):
            pc = dict(type='carre' if cle == 'fond' else 'tri', x=x, y=y, yaw=yaw)
            fc = '#f2d0a9' if Z == 0 else '#9aa5b1' if Z > -1.5 * p['decaissement'] else '#6c757d'
            ax2.add_patch(MPoly(polygone(pc), closed=True, fc=fc, ec='#999', lw=0.3))
    styles = {'mur': ('#000', 1.2), 'cadre_double': ('#0a0', 2.5)}
    for e, (cle, x, y, Z, yaw, r) in zip(t.entries, t.lignes):
        if cle in styles and (Z or 0) in (0.0, 1800.0) and not r.startswith('jupe'):
            nx, ny = vec(yaw)
            dx, dy = -ny, nx
            col_, lw = styles[cle]
            if cle == 'cadre_double' and Z == 0:
                col_ = '#e63946'
            ax2.plot([x - 150 * dx, x + 150 * dx], [y - 150 * dy, y + 150 * dy], color=col_, lw=lw)
        elif cle in ('pilier', 'demi_pilier') and Z == 0:
            ax2.plot(x, y, 'o', color='#6a040f', ms=2 if r.startswith('colonnade') else 6)
    tt = parts[(0, 'tourelles')]
    marq = {'heavy': ('s', '#c0392b'), 'tek': ('^', '#2471a3'), 'tesla': ('*', '#d4ac0d')}
    for e, (cle, x, y, Z, yaw, r) in zip(tt.entries, tt.lignes):
        if cle in marq:
            mk, co = marq[cle]
            ax2.plot(x, y, mk, color=co, ms=9, mec='k' if 'JUPE-int' in r else co)
    for nom, (mk, co) in marq.items():
        ax2.plot([], [], mk, color=co, label=NOMS[nom])
    ax2.plot([], [], color='#e63946', lw=2.5, label='portes au sol (pod θ≈26°, fût θ 30°)')
    ax2.plot([], [], color='#0a0', lw=2.5, label='accès galerie Z1800 (mur de pod)')
    ax2.plot([], [], 'o', color='#6a040f', ms=3, label='colonnade (passage à θ 30°) et piliers PA')
    for a in (p['part_debut'], p['part_debut'] + 60):
        c, s_ = vec(a)
        ax2.plot([0, 5300 * c], [0, 5300 * s_], color='k', lw=1.5)
    ax2.set_aspect('equal')
    ax2.set_xlim(-300, 5400)
    ax2.set_ylim(-1700, 5000)
    ax2.legend(loc='upper left', fontsize=8)
    ax2.set_title(f"Part 1 (θ {p['part_debut']}° → {p['part_debut'] + 60}°) : sol, murs, piliers, "
                  '16 tourelles (5 Tek + 10 Heavy + 1 Tesla)')
    fig.savefig(os.path.join(rep, 'plan_6_parts.png'), dpi=70, bbox_inches='tight')
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--racine', default=RACINE)
    ap.add_argument('--debord', type=int, choices=(1, 2), default=2)
    ap.add_argument('--casquette', type=int, choices=(1, 2), default=1)
    ap.add_argument('--decaissement', type=float, default=150.0)
    ap.add_argument('--colonnade', type=float, default=P['colonnade_rayon'], help='rayon de la colonnade (UU)')
    ap.add_argument('--coeur-rotation', type=float, default=0.0)
    ap.add_argument('--verifier-481', metavar='JSON')
    a = ap.parse_args()
    p = dict(P, debord=a.debord, casquette=a.casquette, decaissement=a.decaissement, colonnade_rayon=a.colonnade,
             coeur_rotation=a.coeur_rotation)
    racine = os.path.abspath(a.racine)
    rep_t, rep_d, rep_p = (os.path.join(racine, d) for d in ('templates', 'donnees', 'plans'))
    for d in (rep_t, os.path.join(rep_t, 'phases'), rep_d, rep_p):
        os.makedirs(d, exist_ok=True)
    if a.verifier_481 and not verifier_481(a.verifier_481):
        sys.exit('Le pavage ne correspond pas au template 481.')

    sol, pieces, contours = module_sol(p)
    ext, _, _ = module_sol(p, extension_seule=True)
    verifier_pavage(pieces)
    for m in (4, 5, 7, 8):
        aa, LL = contours[2 * m - 1]
        assert all(abs(x - apo(m)) < 1e-6 for x in aa) and all(l == m for l in LL), m
    pod, infos_pod = module_pod(p, contours)
    murs_rive = cotes_contour(contours[p['anneau_rive']])
    tesla_murs = murs_tesla(murs_rive)
    rampe, murs, sas, ob, jupe, col = module_rampe(p, contours, set(tesla_murs))
    cage, gal = module_cage(p, contours)
    ordre, poses, reserve = matrice(p, contours, murs, tesla_murs, jupe)
    tourelles = template_tourelles('05 Tourelles verticales (6 parts x 16, cap 100 Tesla comptees)', ordre)
    verifier_encombrements(p, infos_pod, col, ordre)

    modules = [('01_sol_D8_complet', sol), ('01b_sol_extension_D4_D8', ext), ('02_pod_central', pod),
               (f'03_rive_colonnade_pente_overhang{p["debord"]}', rampe), ('04_cage_casquette', cage),
               ('05_tourelles_scenario_B', tourelles)]
    phases = templates_phases([m for m in modules if m[0] != '01b_sol_extension_D4_D8'])
    for ph, t in phases.items():
        t.ecrire(os.path.join(rep_t, 'phases', f'{ph}.json'))
    for nom, t in modules:
        t.ecrire(os.path.join(rep_t, nom + '.json'))
    parts = decouper(p, [m for m in modules if m[0] != '01b_sol_extension_D4_D8'])
    verifier_parts(p, parts)
    os.makedirs(os.path.join(rep_t, 'parts'), exist_ok=True)
    for cle, t in parts.items():
        nom = 'Noyau_central' if cle == 'noyau' else f'Part_{cle[0] + 1}_{cle[1]}'
        t.ecrire(os.path.join(rep_t, 'parts', nom + '.json'))
    equip = equipements(infos_pod, contours)

    # CSV de pose
    for nom, t in modules:
        ecrire_csv(os.path.join(rep_d, nom + '.csv'),
                   [(i, NOMS[c], round(x, 1), round(y, 1), '' if Z is None else round(Z, 1), round(yaw % 360, 1),
                     round(math.degrees(math.atan2(y, x)) % 360, 2), round(math.hypot(x, y), 1), rep)
                    for i, (c, x, y, Z, yaw, rep) in enumerate(t.lignes)],
                   ['entree', 'piece', 'x', 'y', 'Z_plan', 'yaw', 'theta', 'rayon', 'repere'])
    ecrire_csv(os.path.join(rep_d, '05_matrice_tourelles.csv'),
               [(s['ordre'], s['priorite'], NOMS[s['type']], s['couche'], s['cote'], s['idx'], round(angle(s), 2),
                 round(s['xm'], 1), round(s['ym'], 1), round(s['Zb'], 1), round(s['x'], 1), round(s['y'], 1),
                 round(s['Zb'] + F / 2, 1), round(s['sortie'] % 360, 1), 'oui' if s['posee'] else 'reserve')
                for s in ordre],
               ['ordre', 'priorite', 'type', 'couche', 'cote', 'index', 'theta', 'x_chaume', 'y_chaume',
                'Z_bas_chaume', 'x_tourelle', 'y_tourelle', 'Z_tourelle', 'sens_de_tir', 'posee'])
    ecrire_csv(os.path.join(rep_d, '06_part_1_structure.csv'),
               [(i, NOMS[c], ph, round(x, 1), round(y, 1), '' if Z is None else round(Z, 1), round(yaw % 360, 1), r)
                for i, ((c, x, y, Z, yaw, r), ph) in enumerate(zip(parts[(0, 'structure')].lignes,
                                                                     parts[(0, 'structure')].phases))],
               ['entree', 'piece', 'phase', 'x', 'y', 'Z_plan', 'yaw', 'repere'])
    ecrire_csv(os.path.join(rep_d, '07_equipements.csv'),
               [(n, NOMS[q['cle']], q['lieu'], round(q['x'], 1), round(q['y'], 1), q['Z'], round(q['yaw'] % 360, 1))
                for n, q in enumerate(equip)],
               ['n', 'equipement', 'lieu', 'x', 'y', 'Z_plan', 'yaw'])
    ecrire_csv(os.path.join(rep_d, '03_ligne_pics.csv'),
               [(n, round(x + 150 * vec(nu)[0], 1), round(y + 150 * vec(nu)[1], 1), -p['decaissement'], nu, k, i)
                for n, (x, y, nu, k, i) in enumerate(murs)],
               ['n', 'x', 'y', 'Z_plan', 'yaw', 'cote', 'index'])
    ecrire_csv(os.path.join(rep_d, '03_colonnade.csv'),
               [(n, round(c['theta'], 3), round(c['x'], 1), round(c['y'], 1), len(c['elements']),
                 sum(1 for e in c['elements'] if e[0] == 'pilier'), sum(1 for e in c['elements'] if e[0] == 'demi_pilier'),
                 round(c['sommet'], 1), round(c['toit'], 1)) for n, c in enumerate(col['colonnes'])],
               ['n', 'theta', 'x', 'y', 'pieces', 'piliers', 'demi_piliers', 'Z_sommet', 'Z_toit'])

    # synthèse
    dmax, rmax = distances(ordre)
    syn = {'parametres': {k: v for k, v in p.items()}, 'apothemes': {f'D{m}': round(apo(m), 1) for m in range(1, 9)},
           'rayons_coins': {f'D{m}': round(rayon_coin(m), 1) for m in range(1, 9)},
           'overhang': ob, 'jupe': jupe, 'Z_plancher_toit': infos_pod['Ztoit'], 'Z_sommet_toit': infos_pod['Zsommet'],
           'paliers_bord': [dict(anneau=p['anneau_rive'] + i + 1, apo_E0_int=round(a, 1), apo_E0_ext=round(b, 1), Z=Z)
                            for i, (a, b, Z) in enumerate(paliers_bord(p))], 'modules': {},
           'tourelles': {'posees': poses, 'reserve': reserve,
                         'par_couche': {cch: sum(1 for s in ordre if s['posee'] and s['couche'] == cch)
                                        for cch in ('JUPE-int', 'JUPE-ext', 'L1', 'RIVE')}},
           'cap': {'distance_max_entre_tourelles': round(dmax, 1), 'rayon_max_tourelle': round(rmax, 1),
                   'distance_min_avant_poste': round(10000 + rmax, 1)},
           'secteurs': secteurs(p, ob, jupe),
           'colonnade': {k: (round(v, 3) if isinstance(v, float) else v) for k, v in col.items() if k != 'colonnes'},
           'escalier': {'x': infos_pod['escalier']['loc']['x'], 'y': infos_pod['escalier']['loc']['y'],
                        'yaw': infos_pod['escalier']['rot']['yaw'], 'marches': int(p['mezzanine'] // F)},
           'tremie': [dict(anneau=pc['anneau'], type=pc['type'], x=round(pc['x'], 1), y=round(pc['y'], 1))
                      for pc in infos_pod['tremie']],
           'pics': {'nombre': len(murs), 'apotheme_ligne': round(apo(7) + 150, 1), 'Z': -p['decaissement']},
           'sas_rive': {'index_mur': sas}}
    syn['colonnade']['colonnes'] = len(col['colonnes'])
    syn['colonnade']['pieces'] = sum(len(c['elements']) for c in col['colonnes'])
    syn['colonnade']['hauteurs'] = sorted({round(c['sommet']) for c in col['colonnes']})
    for nom, t in modules:
        c = t.compte()
        syn['modules'][nom] = {'pieces': c, 'total': len(t.entries), 'bilan': bilan(c)}
    syn['phases'] = {ph: {'total': len(t.entries), 'pieces': t.compte(), 'bilan': bilan(t.compte())}
                     for ph, t in phases.items()}
    syn['anneaux'] = tableau_anneaux(p)
    syn['gabarits'] = [dict(nom=n, theta=th, apotheme=A, largeur=lg, profondeur=pf, hauteur_murs=hm,
                            x=round(A * vec(th)[0], 1), y=round(A * vec(th)[1], 1))
                       for n, th, A, lg, pf, hm in GABARITS]
    syn['generateurs'] = [dict(nom=n, theta=th, x=round(A * vec(th)[0], 1), y=round(A * vec(th)[1], 1), Z=Z)
                          for n, th, A, Z in GENERATEURS]
    var = {}
    for cq in (1, 2):
        pv = dict(p, casquette=cq)
        var[f'casquette{cq}'] = {'L1': secteur_tir(pv, ob, apo(5) + DECALAGE_MONTAGE + SAILLIE_TETE,
                                                   pv['mezzanine'] + F / 2),
                                 'degagement_chute_casquette': round(cq * F - DECALAGE_MONTAGE, 1)}
    syn['variantes'] = var
    # bilan complet : 6 parts + noyau + pics + équipements
    nb_eq = {}
    for q in equip:
        nb_eq[q['cle']] = nb_eq.get(q['cle'], 0) + 1
    def sans_ancre(t):
        c = {}
        for cle, *_, r in t.lignes:
            if not r.startswith('ancre'):
                c[cle] = c.get(cle, 0) + 1
        return c

    part_s, part_t, noy = sans_ancre(parts[(0, 'structure')]), sans_ancre(parts[(0, 'tourelles')]), sans_ancre(parts['noyau'])
    nb_ancres = sum(1 for t in parts.values() for *_, r in t.lignes if r.startswith('ancre'))
    postes = {
        'part_structure': {k: v * p['parts'] for k, v in part_s.items()},
        'part_tourelles_chaume': {'chaume_mur': part_t.get('chaume_mur', 0) * p['parts']},
        'tourelles': {k: part_t.get(k, 0) * p['parts'] for k in ('heavy', 'tek', 'tesla')},
        'noyau': noy, 'ancres_temporaires': {'demi_pilier': nb_ancres}, 'pics': {'pics': len(murs)},
        'equipements': nb_eq}
    # les ancres (1 demi-pilier par template, 2 pour la part 1) sont comptées dans les demi-piliers
    syn['bilan_complet'] = {nom: {'pieces': c, 'bilan': bilan(c)} for nom, c in postes.items()}
    tot_sans, tot_avec = {}, {}
    for nom, v in syn['bilan_complet'].items():
        for r, q in v['bilan'].items():
            tot_avec[r] = tot_avec.get(r, 0) + q
            if nom != 'tourelles':
                tot_sans[r] = tot_sans.get(r, 0) + q
    syn['bilan_total'] = {'sans_tourelles': tot_sans, 'avec_tourelles': tot_avec,
                          'brut_sans_tourelles': bilan_brut(tot_sans), 'brut_avec_tourelles': bilan_brut(tot_avec)}
    syn['parts'] = {'nombre': p['parts'], 'debut': p['part_debut'],
                    'structure_par_part': {'total': sum(part_s.values()), 'pieces': part_s, 'bilan': bilan(part_s)},
                    'tourelles_par_part': {'total': sum(part_t.values()), 'pieces': part_t, 'bilan': bilan(part_t)},
                    'noyau': {'total': sum(noy.values()), 'pieces': noy, 'bilan': bilan(noy)}}
    with open(os.path.join(rep_d, 'synthese.json'), 'w', encoding='utf-8') as f:
        json.dump(syn, f, ensure_ascii=False, indent=1)
    plans(rep_p, p, pieces, ordre, ob, jupe, infos_pod, col)
    plan_pod(rep_p, p, infos_pod)
    plan_rampes(rep_p, p, [m for m in modules if m[0] != '01b_sol_extension_D4_D8'])
    plan_parts(rep_p, p, parts, col)

    print(json.dumps({k: v['total'] for k, v in syn['modules'].items()}, indent=1))
    print(json.dumps(syn['tourelles'], indent=1, ensure_ascii=False))
    print(json.dumps(syn['cap'], indent=1), syn['secteurs'])


if __name__ == '__main__':
    main()
