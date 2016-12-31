#!/usr/bin/python
# -*- coding: utf8 -*-
from __future__ import division
from fractions import gcd
import ast
import re


def str_to_ast(string):
    'create a python internal syntax tree from the one line string given'
    # Implicit multiplications are correctly parsed except those such as 'x(x+1)'
    # to accept expressions such as '3x' or "22 Y"
    pattern1 = re.compile(r'([0-9\)])\ *([a-zA-Z\(])|(\))\ *([a-zA-Z0-9])')
    pattern2 = re.compile(r'(\))\ *([a-zA-Z0-9])')
    # I did not manage to substitute the 2 patterns in one pass
    string = re.sub(pattern2,'\g<1>*\g<2>',string)
    string = re.sub(pattern1,'\g<1>*\g<2>',string)
    return ast.parse(string).body[0].value
        
def ast_to_maths_expr(tree):
    'create a math exprs from the python internal ast given'
    # Recursion to improve
    if isinstance(tree, ast.Num) :
        return Num(tree.n)
    if isinstance(tree, ast.Name) :
        return Symbol(tree.id)
    if isinstance(tree, ast.BinOp) :
        if isinstance(tree.op, ast.Add) :
            action = Add
        elif isinstance(tree.op, ast.Sub) :
            action = Sub
        elif isinstance(tree.op, ast.Mult) :
            action = Mult
        elif isinstance(tree.op, ast.Div) :
            action = Frac
        elif tree.op.__class__ in [ast.BitXor, ast.Pow] :
            action = Pow
        else :
            action = BinaryOp
        return  action(ast_to_maths_expr(tree.left),
                       ast_to_maths_expr(tree.right))


class Expr(object):
    
    def __add__(self, other) :
        if isinstance(self,Expr) and isinstance(other,Expr) :
            return Add(self, other)
        elif other.__class__ in [int, float] :
            return Add(self, Num(other))
    
    def __radd__(self, other) :
        if other.__class__ in [int, float] :
            return Add(Num(other), self)
    
    def __sub__(self, other) :
        if isinstance(self,Expr) and isinstance(other,Expr) :
            return Sub(self, other)
        elif other.__class__ in [int, float] :
            return Sub(self, Num(other))
    
    def __rsub__(self, other) :
        if other.__class__ in [int, float] :
            return Sub(Num(other), self)
    
    def __mul__(self, other) :
        if isinstance(self,Expr) and isinstance(other,Expr) :
            return Mult(self, other)
        elif other.__class__ in [int, float] :
            return Mult(self, Num(other))
    
    def __rmul__(self, other) :
        if other.__class__ in [int, float] :
            return Mult(Num(other), self)
            
    def __truediv__(self, other) :
        if isinstance(self,Expr) and isinstance(other,Expr) :
            return Frac(self, other)
        elif other.__class__ in [int, float] :
            return Frac(self, Num(other))
    
    def __rtruediv__(self, other) :
        if other.__class__ in [int, float] :
            return Frac(Num(other), self)
            
    def __pow__(self, other) :
        if isinstance(self,Expr) and isinstance(other,Expr) :
            return Pow(self, other)
        elif other.__class__ in [int, float] :
            return Pow(self, Num(other))
    
    def __rpow__(self, other) :
        if other.__class__ in [int, float] :
            return Pow(Num(other), self)
            
class Num(Expr) :

    def __init__(self, number):
        self.n = number
        self.explicitly_const = True
        
    def __eq__(self, other) :
        if isinstance(other,Num) :
            return self.n == other.n
        else :
            return False
        
    def evaluate(self) :
        return Num(self.n)
        
    def to_infix(self, head = True) :
        if self.n > 0 or head == True :
            return str(self.n)
        else :
            return '(' + str(self.n) + ')'
    
    def to_frac(self) :
        return Frac(self.n,1)
    
    def subs(self,var,val):
        return self
    
    def expand(self):
        return self
    
class Symbol(Expr) :
    
    def __init__(self,string, explicitly_const = False) :
        self.id = string
        self.explicitly_const = explicitly_const
        
    def __eq__(self,other):
        if isinstance(other,Symbol) and self.id == other.id :
            return True
        else : return False
        
    def to_infix(self, head = True) :
        return str(self.id)
        
    def subs(self,var,val) :
        if self == var :
            return Num(val)
        else :
            return self

class BinaryOp(Expr):
    
    def __init__(self,leftArg,rightArg):
        self.leftArg = leftArg
        self.rightArg = rightArg
        self.explicitly_const = leftArg.explicitly_const and \
                                rightArg.explicitly_const
    #def evaluate(self):
        #return self
    
    def subs(self,var,val) :
        a = self.leftArg
        b = self.rightArg
        Op = self.__class__
        if a == var and b == var:
            return Op(Num(val),Num(val))
        elif a == var :
            return Op(Num(val),b)
        elif b == var:
            return Op(a,Num(val))
        else :
            return Op(a.subs(var,val),b.subs(var,val))
            
            
    def evaluate_one_step(self):
        a = self.leftArg
        b = self.rightArg
        Op = self.__class__
        if isinstance (a,Num) and isinstance (b,Num) :
            return self.evaluate()
        elif isinstance(a,BinaryOp) and isinstance(b,BinaryOp) :
            return Op(a.evaluate_one_step(),b.evaluate_one_step())
        elif isinstance(a,BinaryOp):
            return Op(a.evaluate_one_step(),b)
        elif isinstance(b,BinaryOp):
            return Op(a,b.evaluate_one_step())
        
    def expand(self):
        node=self
        Op=self.__class__
        a = self.leftArg
        b = self.rightArg
        if isinstance(a,BinaryOp):
            a=a.expand()
        if isinstance(b,BinaryOp):
            b=b.expand()
        return Op(a,b)

    def simplify(self):
        node=self
        Op=self.__class__
        a = self.leftArg
        b = self.rightArg
        if isinstance(a,BinaryOp):
            a=a.simplify()
        if isinstance(b,BinaryOp):
            b=b.simplify()
        return Op(a,b)
        
    def __eq__(op1,op2):
        if op1.__class__.__name__== op2.__class__.__name__ :
            a1=op1.leftArg
            b1=op1.rightArg
            a2=op2.leftArg
            b2=op2.rightArg
            return a1==a2 and b1==b2
        else : return False
        
    #def to_infix(self, head = True):
        #pass
           

class MultOrDiv(BinaryOp):
    pass
    
class Mult(MultOrDiv):
    def evaluate(self):
        return Num(self.leftArg.n * self.rightArg.n)
        
    def to_infix(self,head = True):
        a = self.leftArg
        b = self.rightArg
        if isinstance(a,AddOrSub) :
            str_a = '(' + a.to_infix(head = True) + ')'
        else :
            str_a = a.to_infix(head)
        if isinstance(b,AddOrSub) :
            str_b = '(' + b.to_infix(head = True) + ')'
        else :
            str_b = b.to_infix(head = False)
        return str_a + ' * ' + str_b
        
    def leftExpand(self):
        node=self
        if isinstance(self.rightArg,AddOrSub):
            Op=self.rightArg.__class__
            k=self.leftArg
            a=self.rightArg.leftArg
            b=self.rightArg.rightArg
            # node = k(a Op b)
            e = Mult(k,a)
            f = Mult(k,b)
            if isinstance(a,AddOrSub) :
                e = e.leftExpand()
            if isinstance(b,AddOrSub) :
                f = f.leftExpand()
            node = Op(e,f)
        return node
    
    def rightExpand(self):
        node=self
        if isinstance(self.leftArg,AddOrSub):
            Op=self.leftArg.__class__
            k=self.rightArg
            a=self.leftArg.leftArg
            b=self.leftArg.rightArg
            # node = (a Op b)k
            e = Mult(a,k)
            f = Mult(b,k)
            if isinstance(a,AddOrSub) :
                e = e.rightExpand()
            if isinstance(b,AddOrSub) :
                f = f.rightExpand()
            node = Op(e,f)
        return node
        
    def expand(self):
        l=self.leftExpand()
        if isinstance(l,Mult):
            return l.rightExpand()
        else :
            return l
            
    def doubleDist(self):
        node=self
        A=self.leftArg
        B=self.rightArg
        if isinstance(A,AddOrSub) and isinstance(B,AddOrSub):
            ## node = (a Op1 b) (c Op2 d)
            Op1=A.__class__
            a=A.leftArg
            b=A.rightArg
            
            Op2=B.__class__
            c=B.leftArg
            d=B.rightArg
            
            node=Op1(Op2(Mult (a,c),Mult(a,d)),Op2(Mult (b,c),Mult(b,d)))
            ## node = ac Op2 ad Op1 (bc Op2 bd)
        return node
        
        
    def toPower(self):
        node=self
        if isinstance(self.leftArg,Pow) \
        and self.leftArg.leftArg == self.rightArg :
            a=self.leftArg.leftArg
            k=self.leftArg.rightArg
            node=Pow(a,Add(k,1))
            
        elif isinstance(self.rightArg,Pow) \
        and self.rightArg.leftArg == self.leftArg :
            a=self.rightArg.leftArg
            k=self.rightArg.rightArg
            node=Pow(a,Add(k,1))
            
        elif isinstance(self.leftArg,Pow) \
        and isinstance(self.rightArg,Pow) \
        and self.leftArg.leftArg == self.rightArg.leftArg :
            a=self.leftArg.leftArg
            m=self.leftArg.rightArg
            n=self.rightArg.rightArg
            node=Pow(a,Add(m,n))
                 
        elif self.leftArg == self.rightArg :
            node=Pow(self.leftArg,2)
        return node
    
    def simplify(self):
        node=self
        a = self.leftArg
        b = self.rightArg
        if isinstance(a,int) and isinstance(b,int):
            node=a*b
        else :
            dev=node.expand()
            if not dev == node :
                node=dev
            else :
                node=BinaryOp.simplify(self)
        return node
        

class AddOrSub(BinaryOp):
    
    def getCommonFactorIfAny(self):#a refactoriser pour renvoyer le "chemin" vers les facteurs communs.
        node=None
        if isinstance(self.leftArg,Mult) \
        and isinstance(self.rightArg,Mult):
            a = self.leftArg.leftArg
            b = self.leftArg.rightArg
            c = self.rightArg.leftArg
            d = self.rightArg.rightArg
            if a in [c,d] :
                node = a
            elif b in [c,d] :
                node=b
        return node

    def factorise(self):
        node=self
        Op=self.__class__
        if isinstance(self.leftArg,Mult) \
        and isinstance(self.rightArg,Mult):
            a = self.leftArg.leftArg
            b = self.leftArg.rightArg
            c = self.rightArg.leftArg
            d = self.rightArg.rightArg
            # (a * b) Op (c * d)
            if a == c :
                node=Mult(a, Op(b,d))
            elif a == d :
                node=Mult(a, Op(b,c))
            elif b == c :
                node=Mult(b, Op(a,d))
            elif b == d :
                node=Mult(d, Op(a,c))
        return node
    
    def simplify(self):
        node=self
        Op=self.__class__
        
        if isinstance(self.leftArg,Frac) \
        and isinstance(self.rightArg,Frac) :
        #in this case, we have : a/b +c/d
            a = self.leftArg.leftArg
            b = self.leftArg.rightArg
            c = self.rightArg.leftArg
            d = self.rightArg.rightArg
            if b == d :
                node = Frac(Op(a,c),d)
            elif b == 1 :
                node=Op(Frac(Mult(a,d),Mult(b,d)),Frac(c,d))
            elif d == 1 :
                node=Op(Frac(a,b),Frac(Mult(c,b),Mult(d,b)))
            elif isinstance(b,int) and isinstance(d,int):
                dd=b*d//gcd(b,d)
                k1=dd//b
                k2=dd//c
                if k1  != 1 :
                    f1=Frac(Mult(a,k1),Mult(b,k1))
                else : 
                    f1=Frac(a,b)
                if k2  != 1 :
                    f2=Frac(Mult(c,k2),Mult(d,k2))
                else :
                    f2=Frac(c,d)
                node = Op(f1,f2)
        elif isinstance(self.leftArg,Frac) \
        and isinstance(self.rightArg,int) :
            node = Op(self.leftArg,Frac(self.rightArg,1))         
        elif isinstance(self.leftArg,int) \
        and isinstance(self.rightArg,Frac) :
            node = Op(Frac(self.leftArg,1),self.rightArg)
        
        else :
            node=BinaryOp.simplify(self)
        return node

class Add(AddOrSub):
    
    def evaluate(self):
        """
        return the addition's result
        must be called by a numbers' addition"""
        return Num(self.leftArg.n + self.rightArg.n)
        
    def to_infix(self,head = True):
        a = self.leftArg
        b = self.rightArg
        str_a = a.to_infix(head)
        str_b = b.to_infix(head = False)
        return str_a + ' + ' + str_b
    
    def simplify(self):
        node=self
        a = self.leftArg
        b = self.rightArg
        if isinstance(a,int) and isinstance(b,int):
            node=a+b
        else :
            node=AddOrSub.simplify(self)
        return node

        

class Sub(AddOrSub):
    
    def evaluate(self):
        return Num(self.leftArg.n - self.rightArg.n)
        
    def to_infix(self, head = True):
        a = self.leftArg
        b = self.rightArg
        str_a = a.to_infix(head)
        if isinstance(b,AddOrSub) :
            str_b = '(' + b.to_infix(head = True) + ')'
        else :
            str_b = b.to_infix(head = False)
        return str_a + ' - ' + str_b
           
    def factorise(self):# à modifier pour séparer les différents type de factorisation
        node=AddOrSub.factorise(self)
        if isinstance(self.leftArg,Pow) \
        and isinstance(self.rightArg,Pow):
            if self.leftArg.rightArg == 2 \
            and self.rightArg.rightArg ==2:
                a=self.leftArg.leftArg
                b=self.rightArg.leftArg
                node=Mult(Add(a,b),Sub(a,b))
        return node
        
    def expand(self) :
        """
        expand the substraction with nested AddOrSub flatten it
        >>> expr = Num(5)-(Num(4)-(Num(4)+3-6)+2)
        >>> expr.to_infix()
        5 - (4 - (4 + 3 - 6) + 2)
        >>> expr.expand().to_infix()
        5 - 4 + 4 + 3 - 6 - 2
        # Maybe a bit too quick and strong
        # 5 - 4 + (4 + 3 - 6) - 2
        # could be better
        """
        a = self.leftArg
        b = self.rightArg
        if isinstance(b, Add) :
            c = b.leftArg
            d = b.rightArg
            # self = a -(c+d)
            return (a - c).expand() - d
            # ((a - c) - d)
        elif isinstance(b, Sub) :
            c = b.leftArg
            d = b.rightArg
            # self = a -(c-d)
            return (a - c).expand() + d
            # ((a - c) + d)
        else :
            return Sub(a.expand(),b.expand())
            
    def simplify(self):
        node=self
        a = self.leftArg
        b = self.rightArg
        if isinstance(a,Num) and isinstance(b,Num):
            node=a-b
        else :
            node=AddOrSub.simplify(self)
        return node
        
class Div(MultOrDiv):
    
    #def evaluate(self):
        #return self.leftArg / self.rightArg
    
    def to_infix(self,head = True):
        a = self.leftArg
        b = self.rightArg
        if isinstance(a,AddOrSub) :
            str_a = '(' + a.to_infix(head = True) + ')'
        else :
            str_a = a.to_infix(head)
        if b.__class__ in (AddOrSub,Mult) :
            str_b = '(' + b.to_infix(head = True) + ')'
        else :
            str_b = b.to_infix(head = False)
        return str_a + ' / ' + str_b
    
class Frac(Div):
    def toInverse(self):
        return Frac(self.rightArg,self.leftArg)
    
    def simplify(self):
        node=self
        a = self.leftArg
        b = self.rightArg
        if isinstance(b,int) and b==1 :
            node=a
        elif isinstance(a,int) and isinstance(b,int):
            d=gcd(a,b)
            node=Frac(a//d,b//d)
        elif isinstance(b,Frac):
            node=Mult(a,b.toInverse())
        elif isinstance(a,Mult) and isinstance(b,Mult):
            if a.leftArg == b.leftArg :
                node = Frac(a.rightArg,b.rightArg)
            if a.leftArg == b.rightArg :
                node = Frac(a.rightArg,b.leftArg)
            if a.rightArg == b.leftArg :
                node = Frac(a.leftArg,b.rightArg)
            if a.rightArg == b.rightArg :
                node = Frac(a.leftArg,b.leftArg)
        else :
            node=BinaryOp.simplify(self)
        return node
    
    
        
class Pow(BinaryOp):
    
    def evaluate(self):
        return Num(self.leftArg.n ** self.rightArg.n)
    
    def to_infix(self,head = True):
        a = self.leftArg
        b = self.rightArg
        if a.__class__ not in [Num,Symbol] \
        or (isinstance(a,Num) and a.n < 0) :
            str_a = '(' + a.to_infix(head = True) + ')'
        else :
            str_a = a.to_infix(head)
        if b.__class__ not in [Num,Symbol] :
            str_b = '(' + b.to_infix(head = True) + ')'
        else :
            str_b = b.to_infix(head = False)
        return str_a + ' ^ ' + str_b




class UnaryOp(Expr):
    
    def __init__(self,arg):
        self.arg=arg
        self.explicitly_const = arg.explicitly_const
    
    def __eq__(op1,op2):
        if op1.__class__.__name__== op2.__class__.__name__ :
            a1=op1.arg
            a2=op2.arg
            return a1==a2
        else : return False
        
        
    def show(self):
        a=self.arg
        string='('+self.__class__.__name__+' '
        if isinstance(a,int) : 
            string+=str(a)
        elif isinstance(a,str) :
            string+=a
        else :
            string+=a.show()
        string+=')'
        return string

class Sqrt(UnaryOp):
    
    def simplify(self):
        node = self
        if isinstance(self.arg,Pow) :
            n=self.arg.leftArg
            k=self.arg.rightArg
            if k == 2 and isinstance(n,int) and n>0 :
                node=n
                
        elif isinstance(self.arg,int):
            i=2
            r=None
            while i*i<=self.arg :
                if self.arg % (i*i) == 0 :
                    r=i
                i=i+1
            if r and r*r == self.arg :
                node=Sqrt(Pow(r,2))
            elif r :
                node=Sqrt(Prod(r^2,self.arg % r^2))
        
        return node 

class Opp(UnaryOp):
    pass

class Inv(UnaryOp):
    pass
        
class AlgebraicSum(Expr):
    def __init__(self,args=[]):
        self.args=args
    
if __name__=="__main__":
    pass
    
    
