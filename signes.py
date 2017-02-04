#!/usr/bin/python
# -*- coding: utf-8 -*-
from sympy import symbols, latex, Eq, Pow

from sympyToLatex import set_to_latex
x = symbols('x')

### Fonction auxiliaires

def signe(expr, val):
    var = expr.free_symbols.pop()
    res = expr.subs(var, val)
    if res > 0 :
        return '+'
    else :
        return '-'
        
def separation(expr,val):
    var = expr.free_symbols.pop()
    res = expr.subs(var, val)
    if res == 0 :
        return 'z'
    else :
        return 't'

def ligne_signe(expr, valeurs):
    ligne = r"\tkzTabLine { ,"
    ligne += signe(expr, valeurs[0]-1)
    ligne += ','
    ligne += separation(expr, valeurs[0])
    ligne += ','
    for val1, val2 in zip(valeurs, valeurs[1:]) :
        ligne += signe(expr,(val1 + val2)/2)
        ligne += ','
        ligne += separation(expr,val2)
        ligne += ','
    ligne += signe(expr, valeurs[-1]+1)
    ligne += ", }"
    return ligne
### Fonctions principales

# if isinstance(arg, Pow) and arg.args[1] == -1 :
        # print arg.args[0]

def signe_produit_et_quotient(expr):
    var = expr.free_symbols.pop()
    vals_notables = Eq(expr,0).as_set()
    ## ajout des valeurs interdites des facteurs au dénominateur
    for arg in expr.args :
        if isinstance(arg, Pow) and arg.args[1] == -1 :
            vals_notables = \
                        vals_notables.union(Eq(arg.args[0],0).as_set())
    vals_notables = list(vals_notables)
    vals_notables.sort()
    figure = r'''\begin{tikzpicture}
\onslide<+->
\tkzTabInit[lgt=4,espcl=1.5]
'''
    figure += "{{${}$ /1,".format(latex(var))+'\n'
    facteurs = list(expr.args)
    facteurs.reverse()
    for facteur in facteurs :
        if isinstance(facteur, Pow) and facteur.args[1] == -1 :
            facteur = facteur.args[0]
        figure += " Signe de ${}$ /1,".format(latex(facteur))+'\n'
    figure +=" Signe de ${}$ /1}}".format(latex(expr)) + '\n'
    figure +="{{$-\infty$, {}, $+\infty$}}".format(
        ', '.join([latex(r,mode='inline') \
                            for r in vals_notables])) + '\n'
    for facteur in facteurs :
        if isinstance(facteur, Pow) and facteur.args[1] == -1 :
            facteur = facteur.args[0]
        figure += r'\onslide<+->{' \
               + ligne_signe(facteur,vals_notables) + '}\n'
    figure += r'\onslide<+->{' \
           + ligne_signe(expr,vals_notables) + '}\n'
    figure += r"\end{tikzpicture}\\"'\n'
    return figure

def resolution_inequation_produit_et_quotient(ineq):
    if ineq.args[0] == 0 :
        expr = ineq.args[1]
    elif ineq.args[1] == 0 :
        expr = ineq.args[0]
    #resolution = latex(ineq,mode = 'inline')+'\n'
    resolution = signe_produit_et_quotient(expr)
    var = expr.free_symbols.pop()
    resolution += r'\onslide<+->{'
    resolution += '$'+ latex(var) + r'\in' + set_to_latex(ineq.as_set()) + '$}'
    return resolution
    
def main():
    ex35 = [(-2*x+3)*(-3*x-5),
    (2*x+14)*(6*x+24),
    (5*x-65)*(7-2*x),
    (-3*x-72)*(-4*x-96)]
    #for pdt in ex35 :
        #print r'\begin{frame}'
        #print signe_produit_et_quotient(pdt)
        #print r'\end{frame}'
    ex = [
    (2*x+3)*(-3*x-5)>0,
    (x**2+3)*(2*x+5)<=0,
    (5*x-65)*(7-2*x)>=0,
    ((3*x-4)*(x+1))<0
    ]
    for ineq in ex :
        print str(ineq).replace('**','^').replace('*',' ')
    for ineq in ex :
        print r'\begin{{frame}}{{{}}}'.format(
                                    latex(ineq,mode = 'inline'))
        print r'\pause'
        print resolution_inequation_produit_et_quotient(ineq)
        print r'\end{frame}'
if __name__=='__main__':
    main()
