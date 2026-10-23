#!/usr/bin/env python3
"""Générateur de la forteresse circulaire Ø30 sur Metal Cliff Platform (ARK: Survival Ascended).

Produit, à partir d'une seule géométrie paramétrée :
  - les templates Template Hammer (JSON, même schéma que les exports Wikily.gg) de chaque module,
  - les tableaux de coordonnées (CSV) pour la pose manuelle,
  - la matrice des tourelles avec l'ordre de pose et le calcul du turret cap,
  - le bilan matières,
  - les plans PNG (si matplotlib est installé).

Usage :
    python3 outils/forteresse.py                       # tout régénérer (overhang 2)
    python3 outils/forteresse.py --debord 1            # overhang d'une seule structure au-delà de la plateforme
    python3 outils/forteresse.py --verifier-481 template-481-building-0.json

Conventions (mesurées dans les templates fournis, voir README_Notice_Montage.md §Conventions) :
  - 1 fondation = 300 UU, triangle de côté 300 (hauteur H = 259,81 UU).
  - Origine (0,0) = centre de l'étoile. Angle θ = atan2(y, x) en degrés = yaw Unreal.
  - Z « plan » = cote d'un plancher, 0 = dessus des fondations intérieures.
    z template = Z + 90 (plancher), Z + 40 pour le pivot d'une fondation, Z_bas + 240 pour un mur.
  - Triangle (fondation/plafond) : pivot à mi-hauteur, yaw = direction base -> pointe.
  - Toit incliné (45°) : centre à 150 UU à l'intérieur de son bord bas et 150 UU au-dessus, yaw = sens de montée.
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


def apo(n):
    """Apothème (distance centre -> milieu de côté) du dodécagone régulier D(n) de côté n fondations."""
    return K * n


def rayon_coin(n):
    """Distance centre -> sommet du dodécagone D(n)."""
    return F * n / (2 * math.sin(math.radians(15)))


def vec(deg):
    a = math.radians(deg)
    return math.cos(a), math.sin(a)


# ---------------------------------------------------------------- paramètres du projet
P = dict(
    anneaux_total=15,          # D8 : Ø 29,86 fondations entre plats
    anneau_pod=7,              # D4 : Ø 14,93 (pod central, = étoile SkunkHD 481)
    anneau_cage=9,             # D5 : ligne des double doorframes
    anneau_rive=13,            # D7 : mur de rive
    decaissement=150.0,        # abaissement des 2 derniers anneaux (14-15)
    rive_niveaux=2,            # hauteur du mur de rive (murs)
    rangs_pente_A=4,           # rangs de toit entre la rive et la cage
    cage_niveaux=2,            # étages de double doorframes
    casquette=1,               # rangs de casquette en porte-à-faux devant la cage
    debord=2,                  # rangs de toit au-delà du bord de plateforme (1 ou 2)
    pod_niveaux=10,            # hauteur du mur de pod (murs) -> Z 3000
    mezzanine=1800.0,          # plancher technique du pod = sol de la galerie L1 (6 murs libres dessous)
    jupe=True,                 # jupe basse sous l'overhang (tourelles suspendues)
    recul_siege=50.0,          # recul du pivot des tourelles derrière la ligne des double doorframes
)

# ---------------------------------------------------------------- classes Unreal (chemins relevés dans les templates fournis)
C = {
    'fond': '/Game/PrimalEarth/Structures/Metal/Floor_Metal.Floor_Metal_C',
    'fond_tri': '/Game/PrimalEarth/StructuresPlus/Structures/Foundations/Triangle/Metal/BP_TriFoundation_Metal.BP_TriFoundation_Metal_C',
    'plafond': '/Game/PrimalEarth/Structures/Metal/Ceiling_Metal.Ceiling_Metal_C',
    'plafond_tri': '/Game/PrimalEarth/StructuresPlus/Structures/Ceilings/Triangle/Metal/BP_TriCeiling_Metal.BP_TriCeiling_Metal_C',
    'mur': '/Game/PrimalEarth/Structures/Metal/Wall_Metal.Wall_Metal_C',
    'mur_fenetre': '/Game/PrimalEarth/Structures/Metal/WindowWall_Metal.WindowWall_Metal_C',
    'cadre_double': '/Game/PrimalEarth/StructuresPlus/Structures/Doorframes_Double/Metal/BP_DoubleDoorframe_Metal.BP_DoubleDoorframe_Metal_C',
    'pilier': '/Game/PrimalEarth/Structures/Metal/Pillar_Metal.Pillar_Metal_C',
    'trappe': '/Game/PrimalEarth/Structures/Metal/Ceiling_Doorway_Metal.Ceiling_Doorway_Metal_C',
    'demi_pilier': '/Game/PrimalEarth/Structures/Tileset/Pillars/Half/Pillar_Half_Metal.Pillar_Half_Metal_C',
    'toit': '/Game/PrimalEarth/CoreBlueprints/Items/Structures/Roofs/Metal/MetalRoof_SM.MetalRoof_SM_C',
    'demi_toit': '/Game/PrimalEarth/Structures/Tileset/RoofHalf/BP_Roof_Half_Metal.BP_Roof_Half_Metal_C',
    'heavy': '/Game/PrimalEarth/Structures/BuildingBases/StructureTurretBaseBP_Heavy.StructureTurretBaseBP_Heavy_C',
    'tek': '/Game/PrimalEarth/Structures/BuildingBases/StructureTurretTek.StructureTurretTek_C',
    'tesla': '/Game/Packs/Steampunk/Structures/TeslaCoil/StructureBP_TeslaCoil.StructureBP_TeslaCoil_C',
}
NOMS = {
    'fond': 'Fondation métal', 'fond_tri': 'Fondation triangle métal', 'plafond': 'Plafond métal',
    'plafond_tri': 'Plafond triangle métal', 'mur': 'Mur métal', 'mur_fenetre': 'Mur fenêtre métal',
    'cadre_double': 'Cadre de porte double métal', 'pilier': 'Pilier métal', 'trappe': 'Plafond à trappe métal', 'demi_pilier': 'Demi-pilier métal',
    'toit': 'Toit incliné métal', 'demi_toit': 'Demi-toit métal', 'heavy': 'Tourelle lourde (Heavy)',
    'tek': 'Tourelle Tek', 'tesla': 'Bobine Tesla', 'pics': 'Mur de pics métal',
}

# Coût unitaire : MI=lingot de métal, PC=pâte cimentée, EL=électroniques, PO=polymère, CR=cristal, EM=élément,
# CU=cuir, FI=fibre. '~' = estimation (pièce absente des sources consultées), à confirmer à l'établi.
COUTS = {
    'fond': dict(MI=50, PC=15), 'fond_tri': dict(MI=25, PC=8), 'plafond': dict(MI=35, PC=10),
    'plafond_tri': dict(MI=18, PC=5, est=True), 'mur': dict(MI=25, PC=7),
    'mur_fenetre': dict(MI=25, PC=7, est=True), 'cadre_double': dict(MI=25, PC=7, est=True),
    'pilier': dict(MI=25, PC=7), 'trappe': dict(MI=35, PC=10, est=True), 'demi_pilier': dict(MI=13, PC=4, est=True), 'toit': dict(MI=35, PC=10),
    'demi_toit': dict(MI=18, PC=5, est=True),
    'heavy': dict(MI=540, PC=200, EL=270, PO=70),      # 1 tourelle auto (140/50/70/20) + 400/150/200/50
    'tek': dict(MI=100, PC=50, EL=100, PO=50, EM=3),
    'tesla': dict(MI=500, CR=200, EL=100, PO=300),
    'pics': dict(MI=25, CU=20, FI=30),
}


# ---------------------------------------------------------------- template Hammer
class Template:
    def __init__(self, nom, description):
        self.nom, self.description = nom, description
        self.entries, self.snap = [], []
        self.lignes = []          # pour les CSV : (classe, x, y, Z_plan, yaw, repère)
        self.phase, self.phases = None, []

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
    """Repère central : 2 demi-piliers empilés (template sol) ou 1 demi-pilier posé dessus (autres modules)."""
    if empilee:
        t.add('demi_pilier', 0, 0, 15, 0, Z=-75, repere='ancre basse')
        t.add('demi_pilier', 0, 0, 165, 0, Z=75, repere='ancre haute')
        t.snap = [0, 1]
    else:
        t.add('demi_pilier', 0, 0, 315, 0, Z=225, repere='ancre module (se pose sur l\'ancre du sol)')
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
    arrondi au supérieur : les pièces se chevauchent aux arêtes (noues) au lieu de laisser un jour.
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


def rang_toit(t, A_bas, Z_bas, repere):
    """Un rang de toits à 45° dont le bord bas est sur l'apothème A_bas à la cote Z_bas, montée vers le centre."""
    for x, y, nu, k, i in rang_dodeca(A_bas, F / 2):
        t.add('toit', x, y, Z_bas + Z_TPL + F / 2, nu + 180, Z=Z_bas, repere=f'{repere} c{k} p{i}')


# ---------------------------------------------------------------- modules
def module_sol(p, extension_seule=False):
    pieces, contours = pavage(p['anneaux_total'])
    nom = '01b Extension sol D4->D8' if extension_seule else '01 Sol D8 complet'
    t = Template(nom, 'Pavage carres+triangles en etoile, Ø30 (D8). Anneaux 14-15 abaisses de '
                      f"{p['decaissement']:.0f} UU. Origine = centre de l'etoile.")
    if not extension_seule:
        ancre(t, empilee=True)
    t.phase = 'P1'
    for pc in pieces:
        if extension_seule and pc['anneau'] <= p['anneau_pod']:
            continue
        bas = pc['anneau'] > p['anneaux_total'] - 2
        Z = -p['decaissement'] if bas else 0.0
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
    t = Template('02 Pod central atelier', 'Mur de pod D4 (48 murs/niveau), piliers porteurs, mezzanine a Z1800, '
                                         'cone 12 pans + capuchon.')
    ancre(t)
    d4 = contours[p['anneau_pod']]
    zmez = p['mezzanine']
    # mur de pod : niveaux 0..9 ; portes doubles au sol (θ=90/270, index 1-2) et accès galerie à Z1800 (index 1)
    for niv in range(p['pod_niveaux']):
        Zb = niv * F
        t.phase = 'P2' if Zb < zmez else 'P6'
        for x, y, nu, k, i in cotes_contour(d4):
            cle = 'mur'
            if niv == 0 and nu in (90, 270) and i in (1, 2):
                cle = 'cadre_double'
            if Zb == zmez and i == 1:
                cle = 'cadre_double'
            t.add(cle, x, y, Zb + Z_TPL + F / 2, nu, Z=Zb, repere=f'pod niv{niv} c{k} p{i}')
    # piliers : couronne PA aux sommets de D2 (Z0 -> 4050), couronne PB aux sommets de D1 (Z1800 -> 4650)
    for nom, n, Zb, Zh in (('PA', 2, 0.0, 4050.0), ('PB', 1, zmez, 4650.0)):
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
    # mezzanine Z1800 : anneaux 1..7 en plafonds (centre hexagonal laissé ouvert = trémie d'accès)
    pieces, _ = pavage(p['anneau_pod'], centre=False)
    t.phase = 'P3'
    for pc in pieces:
        cle = 'plafond' if pc['type'] == 'carre' else 'plafond_tri'
        t.add(cle, pc['x'], pc['y'], zmez + Z_TPL, pc['yaw'], Z=zmez, repere=f"mezzanine anneau {pc['anneau']}")
    # cône : rangs de toits depuis le haut du mur de pod
    Ztop = p['pod_niveaux'] * F
    A = apo(4)
    j = 0
    t.phase = 'P6'
    while A - F > 0:
        rang_toit(t, A, Ztop + j * F, f'cone r{j}')
        A -= F
        j += 1
    Zcap = Ztop + j * F
    t.add('plafond', 0, 0, Zcap + Z_TPL, 0, Z=Zcap, repere='capuchon')
    for k in range(4):
        cx, cy = vec(90 * k)
        t.add('demi_toit', cx * F / 4, cy * F / 4, Zcap + Z_TPL + F / 4, 90 * k + 180, Z=Zcap, repere='pointe')
    return t, Zcap


def module_rampe(p, contours):
    t = Template('03 Rive, pente de glisse et overhang',
                 f"Mur de rive D7 ({p['rive_niveaux']} niveaux), {p['rangs_pente_A']} rangs de toits jusqu'a la cage, "
                 f"overhang {2 + p['debord']} rangs (dont {p['debord']} au-dela de la plateforme), jupe basse.")
    ancre(t)
    d7 = contours[p['anneau_rive']]
    murs = cotes_contour(d7)
    # embrasures Tesla : 10 murs-fenêtres répartis à ~36°, niveau 1
    emb = set()
    for kk in range(10):
        cible = 36 * kk
        best = min(range(len(murs)), key=lambda j: abs(((math.degrees(math.atan2(murs[j][1], murs[j][0])) - cible
                                                         + 180) % 360) - 180))
        emb.add(best)
    sas = next(j for j, m in enumerate(murs) if m[2] == 270 and m[4] == 3)
    emb.discard(sas)
    t.phase = 'P2'
    for niv in range(p['rive_niveaux']):
        Zb = niv * F
        for j, (x, y, nu, k, i) in enumerate(murs):
            cle = 'mur_fenetre' if (niv == 0 and j in emb) else 'mur'
            if niv == 0 and j == sas:
                cle = 'cadre_double'
            t.add(cle, x, y, Zb + Z_TPL + F / 2, nu, Z=Zb, repere=f'rive niv{niv} c{k} p{i}')
    # pente A : de la rive vers la cage
    A7 = apo(7)
    Zr = p['rive_niveaux'] * F
    t.phase = 'P4'
    for j in range(p['rangs_pente_A']):
        rang_toit(t, A7 - j * F, Zr + j * F, f'pente A r{j}')
    # overhang : 2 rangs au-dessus du décaissement + 'debord' rangs dans le vide
    for j in range(1, 3 + p['debord']):
        rang_toit(t, A7 + j * F, Zr - j * F, f'overhang r-{j}')
    A_bout = A7 + (2 + p['debord']) * F
    Z_bout = Zr - (2 + p['debord']) * F
    jupe = None
    if p['jupe'] and p['debord'] >= 2:          # avec 1 seul rang dans le vide, la chute frôlerait les tourelles
        t.phase = 'P4'
        # jupe : mur d'about à l'aplomb de l'overhang r-3, plafonds sous les rangs dans le vide
        A_j = A7 + 2 * F
        nb = int(round((Zr - 2 * F - Z_bout) / F))
        for niv in range(nb):
            Zb = Z_bout + niv * F
            for x, y, nu, k, i in rang_dodeca(A_j):
                t.add('mur', x, y, Zb + Z_TPL + F / 2, nu, Z=Zb, repere=f'jupe mur niv{niv} c{k} p{i}')
        for r in range(p['debord']):
            for x, y, nu, k, i in rang_dodeca(A_j + (r + 1) * F, F / 2):
                t.add('plafond', x, y, Z_bout + Z_TPL, nu, Z=Z_bout, repere=f'jupe plafond s{r + 1} c{k} p{i}')
        jupe = dict(A=A_j, Z=Z_bout)
    return t, murs, sorted(emb), dict(A_bout=A_bout, Z_bout=Z_bout), jupe


def module_cage(p, contours):
    t = Template('04 Cage a tourelles et casquette',
                 'Fut D5, galerie 2 niveaux en double doorframes (60/niveau), planchers anneaux 8-9, casquette.')
    ancre(t)
    d5 = contours[p['anneau_cage']]
    zmez = p['mezzanine']
    # fût : murs D5 de Z0 à la galerie, 2 portes au sol (θ=90/270, index 2)
    t.phase = 'P2'
    for niv in range(int(zmez // F)):
        Zb = niv * F
        for x, y, nu, k, i in cotes_contour(d5):
            cle = 'cadre_double' if (niv == 0 and nu in (90, 270) and i == 2) else 'mur'
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
                    and pc['cote'] in (1, 5, 9) and pc['idx'] == 0:
                cle = 'trappe'          # trappe + échelle vers la galerie L2
            t.add(cle, pc['x'], pc['y'], Z + Z_TPL, pc['yaw'], Z=Z, repere=f"galerie Z{Z:.0f} anneau {pc['anneau']}")
    # double doorframes
    t.phase = 'P5'
    for niv in range(p['cage_niveaux']):
        Zb = zmez + niv * F
        for x, y, nu, k, i in cotes_contour(d5):
            t.add('cadre_double', x, y, Zb + Z_TPL + F / 2, nu, Z=Zb, repere=f'cage L{niv + 1} c{k} p{i}')
    # casquette (porte-à-faux) + reprise jusqu'au mur de pod
    A5 = apo(5)
    Ztop = zmez + p['cage_niveaux'] * F
    t.phase = 'P5'
    for j in range(p['casquette'], 0, -1):
        rang_toit(t, A5 + j * F, Ztop - j * F, f'casquette r-{j}')
    t.phase = 'P6'
    j = 0
    while A5 - j * F > apo(4) + 1:
        rang_toit(t, A5 - j * F, Ztop + j * F, f'reprise r{j}')
        j += 1
    return t, gal


# gabarits de réservation dans le hall du pod (Z0 -> 1800) : (nom, θ, apothème du centre, largeur, profondeur, murs)
GABARITS = [
    ('Réplicateur Tek', 0, 1650, 900, 600, 3),
    ('Tek Generator (ateliers)', 60, 1800, 300, 300, 1),
    ('Forge industrielle', 120, 1650, 900, 900, 3),
    ('Tek Teleporter (accès principal)', 180, 1700, 300, 300, 1),
    ('Laboratoire de chimie', 240, 1750, 600, 300, 2),
    ('Stockage / Dedicated Storage', 300, 1750, 900, 300, 2),
]
# générateurs Tek de la galerie (sur l'anneau 8, niveau L1) et générateurs électriques de secours (attique A)
GENERATEURS = [('Tek Generator galerie', th, apo(4) + 150, 1800.0) for th in (90, 210, 330)] + \
              [('Générateur électrique secours', th, apo(5) + 450, 0.0) for th in (90, 270)]


def tableau_anneaux(p):
    pieces, contours = pavage(p['anneaux_total'])
    lignes = []
    for r in range(1, p['anneaux_total'] + 1):
        pr = [pc for pc in pieces if pc['anneau'] == r]
        a, L = contours[r]
        zone = ('pod' if r <= p['anneau_pod'] else 'décaissement' if r > p['anneaux_total'] - 2 else 'couronne')
        lignes.append(dict(anneau=r, carres_sur='E0 (0°,60°…)' if r % 2 else 'E1 (30°,90°…)',
                           carres=sum(pc['type'] == 'carre' for pc in pr),
                           tri_ext=sum(pc['type'] == 'tri' and pc['idx'] < L[pc['cote']] - 1 for pc in pr),
                           triangles=sum(pc['type'] == 'tri' for pc in pr),
                           par_cote_E0=L[0], par_cote_E1=L[1], apo_E0=round(a[0], 1), apo_E1=round(a[1], 1),
                           zone=zone, Z=-p['decaissement'] if zone == 'décaissement' else 0))
    return lignes


def templates_phases(modules):
    noms = {'P1': 'Fondations (sol D8 + decaissement)', 'P2': 'Piliers et murs porteurs (Z0-1800)',
            'P3': 'Plafonds intermediaires Z1800 (mezzanine + galerie)',
            'P4': 'Rampes : pente A, overhang et jupe basse',
            'P5': 'Cage : double doorframes L1/L2, planchers 2100/2400, casquette',
            'P6': 'Pod haut et dome : murs 1800-3000, piliers hauts, reprise, cone, capuchon'}
    out = {}
    for ph, nom in noms.items():
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


# ---------------------------------------------------------------- tourelles
def sieges_cage(p, contours, niveau):
    """Sièges derrière chaque double doorframe : carré (côtés E0) ou triangle pointe intérieure (côtés E1)."""
    d5 = contours[p['anneau_cage']]
    A5 = apo(5)
    Z = p['mezzanine'] + (niveau - 1) * F
    out = []
    for x, y, nu, k, i in cotes_contour(d5):
        recul = p['recul_siege']
        nx, ny = vec(nu)
        out.append(dict(x=x - recul * nx, y=y - recul * ny, Z=Z, yaw=nu, couche=f'L{niveau}', cote=k, idx=i,
                        suspendue=False))
    return out


def sieges_jupe(p, jupe, par_cote=2):
    """Tourelles suspendues sous le 1er rang de plafonds de jupe (450 UU en retrait du bord de chute)."""
    out = []
    A_c = jupe['A'] + F / 2
    n = math.ceil(2 * (jupe['A'] + F) * TAN15 / F - 1e-6)
    choix = [n // 2 - 2, n // 2 + 2] if par_cote == 2 else [n // 2]
    for k in range(12):
        nx, ny = vec(30 * k)
        dx, dy = -ny, nx
        for i in choix:
            tt = (-n / 2 + i + 0.5) * F
            out.append(dict(x=A_c * nx + tt * dx, y=A_c * ny + tt * dy, Z=jupe['Z'], yaw=30 * k, couche='JUPE',
                            cote=k, idx=i, suspendue=True))
    return out


def sieges_tesla(p, murs, emb):
    out = []
    for j in emb:
        x, y, nu, k, i = murs[j]
        nx, ny = vec(nu)
        out.append(dict(x=x - F / 2 * nx, y=y - F / 2 * ny, Z=0.0, yaw=nu, couche='RIVE', cote=k, idx=i,
                        suspendue=False))
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


def matrice(p, contours, murs, emb, jupe, inventaire=(80, 35, 10)):
    nH, nT, nS = inventaire
    L1 = sorted(sieges_cage(p, contours, 1), key=angle)
    L2 = sorted(sieges_cage(p, contours, 2), key=angle)
    J = sorted(sieges_jupe(p, jupe), key=angle) if jupe else []
    S = sorted(sieges_tesla(p, murs, emb), key=angle)
    # couche L1 : Tek (horizon / anti-aérien) + Heavy intercalées ; L2 : Heavy restantes réparties
    types_L1 = repartir(len(L1), {'tek': nT, 'heavy': len(L1) - nT})
    for s, ty in zip(L1, types_L1):
        s['type'] = ty
    for s in J:
        s['type'] = 'heavy'
    for s in S:
        s['type'] = 'tesla'
    reste_H = nH - len(J) - sum(1 for s in L1 if s['type'] == 'heavy')
    pas = len(L2) / reste_H
    choisis = {int(i * pas) for i in range(reste_H)}
    for i, s in enumerate(L2):
        s['type'] = 'heavy' if i in choisis else None
    L2 = [s for s in L2 if s['type']]
    # priorités : 1 jupe (sous-plateforme) 2 Tek L1 3 Tesla (pied de rive) 4 Heavy L1 5 Heavy L2
    groupes = [('P1 jupe Heavy', J), ('P2 L1 Tek', [s for s in L1 if s['type'] == 'tek']),
               ('P3 rive Tesla', S), ('P4 L1 Heavy', [s for s in L1 if s['type'] == 'heavy']),
               ('P5 L2 Heavy', L2)]
    ordre = []
    for nom, g in groupes:
        for i in ordre_vdc(len(g)):
            g[i]['priorite'] = nom
            ordre.append(g[i])
    for n, s in enumerate(ordre, 1):
        s['ordre'] = n
    return ordre


def appliquer_cap(ordre, cap, tesla_compte):
    compte = 0
    out = []
    for s in ordre:
        compte_s = s['type'] in ('heavy', 'tek') or (s['type'] == 'tesla' and tesla_compte)
        if compte_s and compte >= cap:
            out.append((s, False))
            continue
        if compte_s:
            compte += 1
        out.append((s, True))
    return out


def template_tourelles(nom, poses):
    t = Template(nom, 'Tourelles seules, a poser apres les modules 03 et 04 (ordre = ordre de pose).')
    ancre(t)
    for s, ok in poses:
        if not ok:
            continue
        z = s['Z'] + Z_TPL + (0 if s['suspendue'] else 10)
        t.add(s['type'], s['x'], s['y'], z, s['yaw'], Z=s['Z'], roll=180.0 if s['suspendue'] else 0.0,
              repere=f"#{s['ordre']} {s['couche']} c{s['cote']} p{s['idx']}")
    return t


def distances(ordre):
    pts = [(s['x'], s['y'], s['Z']) for s in ordre]
    dmax = 0.0
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            dmax = max(dmax, math.dist(pts[i], pts[j]))
    rmax = max(math.hypot(x, y) for x, y, _ in pts)
    return dmax, rmax


# ---------------------------------------------------------------- balistique (coupe radiale, côté E0, θ=0)
def obstacles(p, ob):
    A7, A5, A4 = apo(7), apo(5), apo(4)
    Zr = p['rive_niveaux'] * F
    zmez = p['mezzanine']
    Ztop = zmez + p['cage_niveaux'] * F
    segs = [
        ((A7 - p['rangs_pente_A'] * F, Zr + p['rangs_pente_A'] * F), (ob['A_bout'], ob['Z_bout'])),   # pente A + overhang
        ((A5 + p['casquette'] * F, Ztop - p['casquette'] * F), (A4, Ztop + (A5 - A4))),                # casquette + reprise
        ((apo(7), -p['decaissement']), (apo(8), -p['decaissement'])),                                    # décaissement
    ]
    if p['jupe'] and p['debord'] >= 2:
        segs.append(((A7 + 2 * F, ob['Z_bout']), (ob['A_bout'], ob['Z_bout'])))
        segs.append(((A7 + 2 * F, ob['Z_bout']), (A7 + 2 * F, Zr - 2 * F)))
    return segs


def coupe(seg, r0, z0, ang):
    """Intersection du rayon (r0,z0)+t(cos,sin), t>0, avec un segment."""
    (x1, y1), (x2, y2) = seg
    dx, dz = math.cos(ang), math.sin(ang)
    ex, ez = x2 - x1, y2 - y1
    den = dx * ez - dz * ex
    if abs(den) < 1e-12:
        return None
    t = ((x1 - r0) * ez - (y1 - z0) * ex) / den
    u = ((x1 - r0) * dz - (y1 - z0) * dx) / den
    return t if (t > 1 and 0 <= u <= 1) else None


def secteur_tir(p, ob, r0, z0, plancher=None):
    segs = obstacles(p, ob)
    if plancher is not None:                    # plancher de galerie sous la tourelle (anneaux 8-9)
        segs.append(((apo(4), plancher), (apo(5), plancher)))
    libres = []
    for deci in range(-899, 900):
        ang = math.radians(deci / 10)
        if all(coupe(s, r0, z0, ang) is None for s in segs):
            libres.append(deci / 10)
    if not libres:
        return None
    return min(libres), max(libres)


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
    polys = []
    for pc in pieces:
        nx, ny = vec(pc['yaw'])
        dx, dy = -ny, nx
        pts = ([(-150, -150), (150, -150), (150, 150), (-150, 150)] if pc['type'] == 'carre'
               else [(H / 2, 0), (-H / 2, 150), (-H / 2, -150)])
        polys.append(Polygon([(pc['x'] + u * nx + v * dx, pc['y'] + u * ny + v * dy) for u, v in pts]))
    U = unary_union(polys)
    tot = sum(q.area for q in polys)
    aire_d8 = 3 * (2 + math.sqrt(3)) * (8 * F) ** 2
    print(f'Pavage : {len(pieces)} pièces, recouvrement {tot - U.area:.1f} UU², aire {U.area:.0f} '
          f'(D8 théorique {aire_d8:.0f}), trous {aire_d8 - U.area:.1f} UU²')


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


def plans(rep, p, pieces, contours, ordre, ob, jupe, murs, emb, Zcap):
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from matplotlib.patches import Polygon as MPoly
    except ImportError:
        print('matplotlib absent : plans PNG non générés')
        return
    # --- plan de calpinage
    fig, ax = plt.subplots(figsize=(13, 13))
    for pc in pieces:
        nx, ny = vec(pc['yaw'])
        dx, dy = -ny, nx
        pts = ([(-150, -150), (150, -150), (150, 150), (-150, 150)] if pc['type'] == 'carre'
               else [(H / 2, 0), (-H / 2, 150), (-H / 2, -150)])
        poly = [(pc['x'] + u * nx + v * dx, pc['y'] + u * ny + v * dy) for u, v in pts]
        r = pc['anneau']
        if r > p['anneaux_total'] - 2:
            fc = '#9aa5b1'
        elif r <= p['anneau_pod']:
            fc = '#f2b880' if pc['type'] == 'tri' else '#e07a2f'
        else:
            fc = '#9cc7e8' if pc['type'] == 'tri' else '#3f88c5'
        ax.add_patch(MPoly(poly, closed=True, fc=fc, ec='#333', lw=0.3))
    for m, nom, coul in ((4, 'D4 mur de pod', '#b00'), (5, 'D5 cage', '#070'), (7, 'D7 rive', '#000'),
                         (8, 'D8 bord plateforme', '#555')):
        cs = [vec(15 + 30 * k) for k in range(13)]
        R = rayon_coin(m)
        ax.plot([R * c for c, s in cs], [R * s for c, s in cs], color=coul, lw=2 if m != 8 else 1,
                ls='-' if m != 8 else '--', label=f'{nom} (apothème {apo(m):.0f} UU)')
    for k in range(12):
        c, s = vec(30 * k)
        ax.annotate(f'{30 * k}°', (5100 * c, 5100 * s), ha='center', va='center', fontsize=10,
                    color='#3f88c5' if k % 2 == 0 else '#a05a00')
        ax.plot([0, 4700 * c], [0, 4700 * s], color='#888', lw=0.5, ls=':')
    for k in range(0, 12, 2):
        c, s = vec(30 * k)
        for r in (1, 3, 5, 7, 9, 11, 13, 15):
            pass
    ax.plot(0, 0, 'k+', ms=14)
    ax.set_xlim(-5400, 5400)
    ax.set_ylim(-5400, 5400)
    ax.set_aspect('equal')
    ax.set_title('Plan de calpinage Ø30 (D8) — carrés foncés / triangles clairs ; orange = pod (anneaux 1-7), '
                 'bleu = couronne (8-13), gris = décaissement -150 (14-15)', fontsize=10)
    ax.legend(loc='lower left', fontsize=9)
    ax.set_xlabel('x (UU)  — axe 0° = branche de carrés E0')
    ax.set_ylabel('y (UU)')
    fig.savefig(os.path.join(rep, 'plan_calpinage.png'), dpi=80, bbox_inches='tight')
    plt.close(fig)

    # --- coupe radiale (θ = 0°, côté E0)
    fig, ax = plt.subplots(figsize=(15, 8.5))
    A4, A5, A7, A8 = apo(4), apo(5), apo(7), apo(8)
    Zr = p['rive_niveaux'] * F
    zmez = p['mezzanine']
    Zc = zmez + p['cage_niveaux'] * F
    ax.fill_between([0, A7], [-100, -100], [0, 0], color='#3f88c5', alpha=.5, label='fondations Z0')
    ax.fill_between([A7, A8], [-250, -250], [-150, -150], color='#9aa5b1', label='décaissement -150')
    ax.fill_between([-200, A8], [-700, -700], [-250, -250], color='#ccc', alpha=.5, label='Metal Cliff Platform (épaisseur indicative)')
    ax.plot([A4, A4], [0, p['pod_niveaux'] * F], color='#b00', lw=3, label='mur de pod D4 (10 murs)')
    ax.plot([A5, A5], [0, zmez], color='#070', lw=3, label='fût D5 (6 murs)')
    ax.plot([A5, A5], [zmez, Zc], color='#0a0', lw=6, ls=(0, (2, 1)), label='double doorframes L1/L2')
    ax.plot([A7, A7], [0, Zr], color='k', lw=3, label='mur de rive D7 (2 murs)')
    for Z in (zmez, zmez + F, Zc):
        ax.plot([A4, A5], [Z, Z], color='#070', lw=1.5)
    ax.plot([0, A4], [zmez, zmez], color='#b00', lw=1.5, ls='--', label='mezzanine Z1800')
    ax.plot([A7 - p['rangs_pente_A'] * F, ob['A_bout']], [Zr + p['rangs_pente_A'] * F, ob['Z_bout']],
            color='#e07a2f', lw=3, label='pente A + overhang (toits 45°)')
    ax.plot([A5 + p['casquette'] * F, A4 - 40], [Zc - p['casquette'] * F, Zc + (A5 - A4) + 40], color='#7b2cbf', lw=3,
            label='casquette + reprise')
    ax.plot([A4, 0], [p['pod_niveaux'] * F, Zcap], color='#b00', lw=2, label='cône du pod')
    if jupe:
        ax.plot([jupe['A'], ob['A_bout']], [jupe['Z'], jupe['Z']], color='#555', lw=2, label='jupe (plafonds)')
        ax.plot([jupe['A'], jupe['A']], [jupe['Z'], Zr - 2 * F], color='#555', lw=2)
    rs = A5 - p['recul_siege']
    for pid, (r, z, pl, coul) in {'L1': (rs, zmez + 120, zmez, 'tab:blue'),
                                  'L2': (rs, zmez + F + 120, zmez + F, 'tab:red'),
                                  'JUPE': (jupe['A'] + 150 if jupe else 0, (jupe['Z'] if jupe else 0) - 120, None,
                                           'tab:purple')}.items():
        sect = secteur_tir(p, ob, r, z, pl)
        if not sect:
            continue
        for a in sect:
            ax.plot([r, r + 6000 * math.cos(math.radians(a))], [z, z + 6000 * math.sin(math.radians(a))], color=coul,
                    lw=0.8, ls='--')
        ax.plot(r, z, 'o', color=coul, ms=8, label=f'{pid} : secteur {sect[0]:+.1f}° / {sect[1]:+.1f}°')
    ax.annotate('pics (bande protégée)', (A7 + 150, -150), xytext=(A7 - 900, -900), arrowprops=dict(arrowstyle='->'))
    ax.annotate('Tesla (embrasure)', (A7 - 150, 150), xytext=(A7 - 1500, 500), arrowprops=dict(arrowstyle='->'))
    ax.annotate('chute -> abysse', (ob['A_bout'], ob['Z_bout']), xytext=(ob['A_bout'] + 200, ob['Z_bout'] - 900),
                arrowprops=dict(arrowstyle='->'))
    ax.set_xlim(-200, 7000)
    ax.set_ylim(-1600, 5800)
    ax.set_aspect('equal')
    ax.grid(True, lw=0.3)
    ax.set_xlabel('distance au centre le long de la normale 0° (UU)')
    ax.set_ylabel('Z (UU) — 0 = dessus des fondations intérieures')
    ax.set_title('Coupe radiale type (côté E0, θ=0°) et secteurs de tir verticaux')
    ax.legend(loc='upper right', fontsize=8)
    fig.savefig(os.path.join(rep, 'coupe_radiale.png'), dpi=80, bbox_inches='tight')
    plt.close(fig)

    # --- plan des tourelles
    fig, ax = plt.subplots(figsize=(12, 12))
    styles = {'heavy': ('s', '#c0392b'), 'tek': ('^', '#2471a3'), 'tesla': ('*', '#d4ac0d')}
    for s in ordre:
        mk, co = styles[s['type']]
        dec = {'L1': 0, 'L2': 120, 'JUPE': 0, 'RIVE': 0}[s['couche']]
        nx, ny = vec(s['yaw'])
        ax.plot(s['x'] + dec * nx, s['y'] + dec * ny, mk, color=co, ms=7 if s['couche'] != 'L2' else 5,
                mec='k' if s['couche'] == 'L2' else co)
        if s['ordre'] <= 24 or s['couche'] == 'RIVE':
            ax.annotate(str(s['ordre']), (s['x'] + dec * nx, s['y'] + dec * ny), fontsize=6, xytext=(3, 3),
                        textcoords='offset points')
    for m, coul in ((4, '#b00'), (5, '#070'), (7, '#000'), (8, '#555')):
        cs = [vec(15 + 30 * k) for k in range(13)]
        R = rayon_coin(m)
        ax.plot([R * c for c, s in cs], [R * s for c, s in cs], color=coul, lw=1)
    # plan de câblage (schéma) : boucle de galerie sur l'anneau 8, descentes vers la rive / la jupe aux 12 arêtes
    R8 = apo(4) + 150
    cs = [vec(30 * k) for k in range(13)]
    ax.plot([R8 / math.cos(math.radians(15)) * c for c, s_ in [vec(15 + 30 * k) for k in range(13)]],
            [R8 / math.cos(math.radians(15)) * s_ for c, s_ in [vec(15 + 30 * k) for k in range(13)]],
            color='#2a9d8f', lw=1.2, ls='--', label='boucle de câbles galerie (Z1800, anneau 8)')
    for k in range(12):
        c, s_ = vec(15 + 30 * k)
        r1, r2 = R8 / math.cos(math.radians(15)), (apo(7) + 600) / math.cos(math.radians(15))
        ax.plot([r1 * c, r2 * c], [r1 * s_, r2 * s_], color='#2a9d8f', lw=0.8, ls=':')
    for nom, th, A, Z in GENERATEURS:
        c, s_ = vec(th)
        ax.plot(A * c, A * s_, 'D', color='#2a9d8f' if 'Tek' in nom else '#6c757d', ms=10, mec='k')
    ax.plot([], [], 'D', color='#2a9d8f', mec='k', label='Tek Generator (galerie, Z1800)')
    ax.plot([], [], 'D', color='#6c757d', mec='k', label='Générateur électrique de secours (attique, Z0)')
    for nom, (mk, co) in styles.items():
        ax.plot([], [], mk, color=co, label=NOMS[nom])
    ax.set_aspect('equal')
    ax.set_title('Matrice des tourelles (inventaire complet) et plan de câblage — L2 décalé de 120 UU pour la '
                 'lisibilité ; numéros = ordre de pose (jupe + Tesla)', fontsize=10)
    ax.legend(loc='lower left', fontsize=8)
    fig.savefig(os.path.join(rep, 'plan_tourelles.png'), dpi=80, bbox_inches='tight')
    plt.close(fig)


def plan_pod(rep, p):
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from matplotlib.patches import Polygon as MPoly
    except ImportError:
        return
    fig, ax = plt.subplots(figsize=(11, 11))
    pieces, contours = pavage(p['anneau_pod'])
    for pc in pieces:
        nx, ny = vec(pc['yaw'])
        dx, dy = -ny, nx
        pts = ([(-150, -150), (150, -150), (150, 150), (-150, 150)] if pc['type'] == 'carre'
               else [(H / 2, 0), (-H / 2, 150), (-H / 2, -150)])
        ax.add_patch(MPoly([(pc['x'] + u * nx + v * dx, pc['y'] + u * ny + v * dy) for u, v in pts], closed=True,
                           fc='#f6e3d0' if pc['type'] == 'tri' else '#efcfae', ec='#bbb', lw=0.3))
    for x, y, nu, k, i in cotes_contour(contours[7]):
        porte = nu in (90, 270) and i in (1, 2)
        ax.plot(x, y, 's', color='#2a9d8f' if porte else '#b00', ms=9 if porte else 4)
    for n, coul, nom in ((2, '#000', 'piliers PA (Z0 -> 4050)'), (1, '#666', 'piliers PB (Z1800 -> 4650)')):
        R = rayon_coin(n)
        pts = [vec(15 + 30 * k) for k in range(12)]
        ax.plot([R * c for c, s_ in pts], [R * s_ for c, s_ in pts], 'o', color=coul, ms=9, label=nom)
    hexa = [vec(30 + 60 * k) for k in range(7)]
    ax.plot([F * c for c, s_ in hexa], [F * s_ for c, s_ in hexa], color='#7b2cbf', lw=2,
            label='trémie mezzanine (ascenseur / échelle)')
    for nom, th, A, lg, pf, hm in GABARITS:
        nx, ny = vec(th)
        dx, dy = -ny, nx
        cx, cy = A * nx, A * ny
        coins = [(cx + u * nx + v * dx, cy + u * ny + v * dy) for u, v in
                 ((-pf / 2, -lg / 2), (pf / 2, -lg / 2), (pf / 2, lg / 2), (-pf / 2, lg / 2))]
        ax.add_patch(MPoly(coins, closed=True, fc='#3f88c5', alpha=.35, ec='#1d4e89', lw=1.5))
        ax.annotate(f'{nom}\n{lg / F:.0f}×{pf / F:.0f} F, {hm} murs', (cx, cy), ha='center', va='center', fontsize=8)
    ax.plot([], [], 's', color='#2a9d8f', ms=9, label='portes doubles du hall (θ 90° / 270°)')
    ax.plot([], [], 's', color='#b00', ms=4, label='mur de pod D4 (48 / niveau)')
    ax.set_aspect('equal')
    ax.set_xlim(-2600, 2600)
    ax.set_ylim(-2600, 2600)
    ax.set_title('Pod central — hall Z0→1800 (6 murs libres) : piliers, portes et gabarits machines', fontsize=10)
    ax.legend(loc='lower left', fontsize=8)
    fig.savefig(os.path.join(rep, 'plan_pod.png'), dpi=80, bbox_inches='tight')
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--racine', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    ap.add_argument('--debord', type=int, choices=(1, 2), default=2)
    ap.add_argument('--casquette', type=int, choices=(1, 2), default=1)
    ap.add_argument('--decaissement', type=float, default=150.0)
    ap.add_argument('--recul', type=float, default=50.0, help='recul des tourelles derrière les cadres (UU)')
    ap.add_argument('--verifier-481', metavar='JSON')
    a = ap.parse_args()
    p = dict(P, debord=a.debord, casquette=a.casquette, decaissement=a.decaissement, recul_siege=a.recul)
    racine = os.path.abspath(a.racine)
    rep_t, rep_d, rep_p = (os.path.join(racine, d) for d in ('templates', 'donnees', 'plans'))
    for d in (rep_t, rep_d, rep_p):
        os.makedirs(d, exist_ok=True)
    if a.verifier_481 and not verifier_481(a.verifier_481):
        sys.exit('Le pavage ne correspond pas au template 481.')

    sol, pieces, contours = module_sol(p)
    ext, _, _ = module_sol(p, extension_seule=True)
    verifier_pavage(pieces)
    for m in (4, 5, 7, 8):
        aa, LL = contours[2 * m - 1]
        assert all(abs(x - apo(m)) < 1e-6 for x in aa) and all(l == m for l in LL), m
    pod, Zcap = module_pod(p, contours)
    rampe, murs, emb, ob, jupe = module_rampe(p, contours)
    cage, gal = module_cage(p, contours)
    ordre = matrice(p, contours, murs, emb, jupe)

    modules = [('01_sol_D8_complet', sol), ('01b_sol_extension_D4_D8', ext), ('02_pod_central', pod),
               (f'03_rive_pente_overhang{p["debord"]}', rampe), ('04_cage_casquette', cage)]
    scenarios = [('A', 'cap 100, Tesla non comptee', 100, False), ('B', 'cap 100, Tesla comptee', 100, True),
                 ('C', 'cap >= 125 (serveur modifie)', 125, True)]
    poses = {}
    for code, lib, cap, tc in scenarios:
        poses[code] = appliquer_cap(ordre, cap, tc)
        modules.append((f'05_tourelles_scenario_{code}', template_tourelles(f'05 Tourelles scenario {code} ({lib})',
                                                                            poses[code])))
    phases = templates_phases(modules[:1] + modules[2:5])
    os.makedirs(os.path.join(rep_t, 'phases'), exist_ok=True)
    for ph, t in phases.items():
        t.ecrire(os.path.join(rep_t, 'phases', f'{ph}.json'))
    for nom, t in modules:
        t.ecrire(os.path.join(rep_t, nom + '.json'))

    # CSV de pose
    for nom, t in modules:
        ecrire_csv(os.path.join(rep_d, nom + '.csv'),
                   [(i, NOMS[c], round(x, 1), round(y, 1), '' if Z is None else round(Z, 1), round(yaw % 360, 1),
                     round(math.degrees(math.atan2(y, x)) % 360, 2), round(math.hypot(x, y), 1), rep)
                    for i, (c, x, y, Z, yaw, rep) in enumerate(t.lignes)],
                   ['entree', 'piece', 'x', 'y', 'Z_plan', 'yaw', 'theta', 'rayon', 'repere'])
    ecrire_csv(os.path.join(rep_d, '05_matrice_tourelles.csv'),
               [(s['ordre'], s['priorite'], NOMS[s['type']], s['couche'], s['cote'], s['idx'],
                 round(angle(s), 2), round(s['x'], 1), round(s['y'], 1), round(s['Z'], 1),
                 'suspendue' if s['suspendue'] else 'debout',
                 *('oui' if ok else 'reserve' for code in 'ABC' for s2, ok in poses[code] if s2 is s))
                for s in ordre],
               ['ordre', 'priorite', 'type', 'couche', 'cote', 'index', 'theta', 'x', 'y', 'Z_plan', 'montage',
                'scenario_A', 'scenario_B', 'scenario_C'])

    # synthèse
    syn = {'parametres': p, 'apothemes': {f'D{m}': round(apo(m), 1) for m in range(1, 9)},
           'rayons_coins': {f'D{m}': round(rayon_coin(m), 1) for m in range(1, 9)},
           'overhang': ob, 'jupe': jupe, 'Z_capuchon': Zcap, 'modules': {}, 'tourelles': {}}
    for nom, t in modules:
        c = t.compte()
        syn['modules'][nom] = {'pieces': c, 'total': len(t.entries), 'bilan': bilan(c)}
    for code, lib, cap, tc in scenarios:
        pl = [s for s, ok in poses[code] if ok]
        syn['tourelles'][code] = {
            'libelle': lib, 'posees': {k: sum(1 for s in pl if s['type'] == k) for k in ('heavy', 'tek', 'tesla')},
            'reserve': {k: sum(1 for s, ok in poses[code] if not ok and s['type'] == k) for k in ('heavy', 'tek', 'tesla')},
            'par_couche': {cch: sum(1 for s in pl if s['couche'] == cch) for cch in ('JUPE', 'L1', 'L2', 'RIVE')}}
    dmax, rmax = distances(ordre)
    syn['cap'] = {'distance_max_entre_tourelles': round(dmax, 1), 'rayon_max_tourelle': round(rmax, 1),
                  'distance_min_avant_poste': round(10000 + rmax, 1)}
    syn['secteurs'] = {
        'L1': secteur_tir(p, ob, apo(5) - p['recul_siege'], p['mezzanine'] + 120, p['mezzanine']),
        'L2': secteur_tir(p, ob, apo(5) - p['recul_siege'], p['mezzanine'] + F + 120, p['mezzanine'] + F),
        'JUPE': secteur_tir(p, ob, jupe['A'] + 150, jupe['Z'] - 120) if jupe else None}
    syn['pics'] = {'nombre': len(murs), 'apotheme_ligne': round(apo(7) + 150, 1), 'Z': -p['decaissement']}
    syn['embrasures_tesla'] = [{'mur': j, 'cote': murs[j][3], 'index': murs[j][4],
                                'theta': round(math.degrees(math.atan2(murs[j][1], murs[j][0])) % 360, 1)} for j in emb]
    with open(os.path.join(rep_d, 'synthese.json'), 'w', encoding='utf-8') as f:
        json.dump(syn, f, ensure_ascii=False, indent=1)
    ecrire_csv(os.path.join(rep_d, '03_ligne_pics.csv'),
               [(n, round(x + 150 * vec(nu)[0], 1), round(y + 150 * vec(nu)[1], 1), -p['decaissement'], nu, k, i)
                for n, (x, y, nu, k, i) in enumerate(murs)],
               ['n', 'x', 'y', 'Z_plan', 'yaw', 'cote', 'index'])
    plans(rep_p, p, pieces, contours, ordre, ob, jupe, murs, emb, Zcap)
    plan_pod(rep_p, p)
    syn['phases'] = {ph: {'total': len(t.entries), 'pieces': t.compte()} for ph, t in phases.items()}
    syn['anneaux'] = tableau_anneaux(p)
    syn['gabarits'] = [dict(nom=n, theta=th, apotheme=A, largeur=lg, profondeur=pf, hauteur_murs=hm,
                            x=round(A * vec(th)[0], 1), y=round(A * vec(th)[1], 1))
                       for n, th, A, lg, pf, hm in GABARITS]
    syn['generateurs'] = [dict(nom=n, theta=th, x=round(A * vec(th)[0], 1), y=round(A * vec(th)[1], 1), Z=Z)
                          for n, th, A, Z in GENERATEURS]
    var = {}
    for cq in (1, 2):
        for db in (1, 2):
            pv = dict(p, casquette=cq, debord=db)
            obv = dict(A_bout=apo(7) + (2 + db) * F, Z_bout=pv['rive_niveaux'] * F - (2 + db) * F)
            var[f'casquette{cq}_debord{db}'] = {
                'L1': secteur_tir(pv, obv, apo(5) - pv['recul_siege'], pv['mezzanine'] + 120, pv['mezzanine']),
                'L2': secteur_tir(pv, obv, apo(5) - pv['recul_siege'], pv['mezzanine'] + F + 120,
                                  pv['mezzanine'] + F),
                'bout_overhang': (round(obv['A_bout'], 1), obv['Z_bout']),
                'degagement_chute_casquette': round(cq * F + pv['recul_siege'], 1)}
    syn['variantes'] = var
    with open(os.path.join(rep_d, 'synthese.json'), 'w', encoding='utf-8') as f:
        json.dump(syn, f, ensure_ascii=False, indent=1)

    print(json.dumps({k: v['total'] for k, v in syn['modules'].items()}, indent=1))
    print(json.dumps(syn['tourelles'], indent=1, ensure_ascii=False))
    print(json.dumps(syn['cap'], indent=1), syn['secteurs'])


if __name__ == '__main__':
    main()
