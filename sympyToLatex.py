#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sympy import symbols, sqrt, Poly, latex
x = symbols('x')

def set_to_latex(intervalles, **settings):
    return latex(intervalles, **settings).replace(r'\left(',r'\left]')\
    .replace(r'\right)',r'\right[').replace(r', \infty',r', +\infty')\
    .replace(r',',r';').replace(r'.',r',').replace(r'\log',r'\ln')

def getExt(p, x0, x1):
    try:
        d = Poly(p.diff(x))
        liste_y = [p.replace(x, x0)]\
            + [round(p.replace(x, k), 2) for k in d.real_roots() if x0 < k < x1]\
            + [p.replace(x, x1)]
    except: liste_y = [p.replace(x, x0), p.replace(x, x1)]
    return [min(liste_y), max(liste_y)]


def polySympyToTikz(p):
    # Hypothese est faite que l'unique variable est x.
    c0 = p.replace(x, 0)
    q = p - c0
    dictionnaire = p.as_coefficients_dict()
    return str(q) + "+(" + str(float(c0)) + ')'


def listeFpmToTikz(listeFpm, context=None, contexteTikz=False):
    fpm = listeFpm[0]
    valeursY = []
    for p in fpm:
        valeursY.extend(getExt(p[2], p[0][0], p[0][1]))
    minY = min(valeursY) - 0.5
    maxY = max(valeursY) + 0.5
    minX = fpm[0][0][0]
    maxX = fpm[-1][0][1]
    if context == 'complet':
        minX = minX - 3
        maxX = maxX + 3
        minY = min(-maxY, minY - 3)
        maxY = max(maxY + 3, -minY)
    instructions = ""
    if not contexteTikz:
        instructions += r"\begin{center}" + '\n'
        instructions += r"\begin{tikzpicture}[scale=1]" + '\n'
    instructions += r"\tkzInit[xmin={},xmax={},ymin={},ymax={}]".format(
        minX, maxX, minY, maxY) + '\n'
    instructions += r"\tkzGrid[sub,subxstep=.1,subystep=.1]" + '\n'
    instructions += r"\tkzDrawXY[label={}]" + '\n'
    instructions += r"\tkzDrawXY[label={}]" + '\n'
    instructions += r"\node[below] at (1,0) {$1$};" + '\n'
    instructions += r"\node[left] at (0,1) {$1$};" + '\n'
    instructions += r"\node[below left] at (0,0) {$O$};" + '\n'
    # Il serait nécessaire de pouvoir donner une couleur et un style aux
    # tracés.
    for fpm in listeFpm:
        for p in fpm:
            if context == 'avecPoints':
                instructions += r"\node at ({},{}){{$\times$}};".format(
                    p[0][0], p[1][0]) + '\n'
            instructions += r"\tkzFct [thick,samples=400,domain={}:{}] {{{}}}".format(
                p[0][0], p[0][1], polySympyToTikz(p[2])) + '\n'
        p = fpm[-1]
        if context == 'avecPoints':
                instructions += r"\node at ({},{}){{$\times$}};".format(
                    p[0][1], p[1][1]) + '\n'
        instructions += '\n'

    if not contexteTikz:
        instructions += r"\end{tikzpicture}" + '\n'
        instructions += r"\end{center}" + '\n'
    return instructions


def fpmToTikz(fpm, context=None, contexteTikz=False):
    return listeFpmToTikz([fpm], context, contexteTikz)


def fpmEtTangentesTikz(fpm, noeuds):
    instructions = r"\begin{center}" + '\n'
    instructions += r"\begin{tikzpicture}[scale=1]" + '\n'
    instructions += fpmToTikz(fpm, None, True)
    for x0 in noeuds:
        for fct in fpm:
            if fct[0][0] <= x0 < fct[0][1]:
                y0 = fct[2].replace(x, x0)
                coeff = fct[2].diff(x).replace(x, x0)
                Dx = 2 / sqrt(coeff**2 + 1)
                y1 = y0 - Dx * coeff
                y2 = y0 + Dx * coeff
                print x0
                instructions += r"\node at ({},{}){{{}}};"\
                    .format(x0, y0, r'$\times$') + '\n'
                instructions +=\
                    r"\draw[thick,latex-latex] ({},{})--({},{});"\
                    .format(round(x0 - Dx, 4), round(y1, 4), round(x0 + Dx, 4), round(y2, 4)) + '\n'
    instructions += r"\end{tikzpicture}" + '\n'
    instructions += r"\end{center}" + '\n'
    return instructions
if __name__ == '__main__' :
    print [ext for ext in getExt(x**2 - 2, -2, 5)]
