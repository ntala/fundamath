#!/usr/bin/python
# -*- coding: utf8 -*-

import expressions as expr
import unittest
tree1 = expr.ast_to_maths_expr(expr.str_to_ast('3+7'))
print tree1.to_infix()
class expressionsTestCase(unittest.TestCase):
    def test_equality(self):
        num1 = expr.Num(3)
        num2 = expr.Num(3)
        prod1 = expr.Num(3) * 2
        prod2 = expr.Num(3) * 2
        sum1 = expr.Num(3) + 2
        prod3 = expr.Symbol('x') * 2
        prod4 = 3 * expr.Symbol('x')
        prod5 = 3 * expr.Symbol('x')
        self.assert_(num1 == num2)
        self.assert_(prod1 == prod2)
        self.assertFalse(prod1 == sum1)
        self.assertFalse(prod3 == prod4)
        self.assertTrue(prod4 == prod5)

        
    def test_leftExpand(self):
        self.assertEqual((expr.Symbol('x')*(expr.Num(3)+4))\
                          .leftExpand(),
                          expr.Symbol('x')*3 + expr.Symbol('x')*4)
        
    #def test_rightExpand(self):
        #self.assertEqual(expr.Mult(expr.Add(3,'x'),'x').rightExpand(),expr.Add(expr.Mult(3,'x'),expr.Mult('x','x')))
    
    #def test_expand(self):
        #self.assertEqual(expr.Mult(expr.Add(3,'x'),'x').expand(),expr.Add(expr.Mult(3,'x'),expr.Mult('x','x')))
        #self.assertEqual(expr.Mult('x',expr.Add(3,4)).leftExpand(),expr.Add(expr.Mult('x',3),expr.Mult('x',4)))
        
    #def test_factorise(self):
        #self.assertEqual(expr.Add(expr.Mult('x',3),expr.Mult('x',5)).factorise(),expr.Mult('x',expr.Add(3,5)))
        #self.assertEqual(expr.Sub(expr.Mult('x',3),expr.Mult('x',5)).factorise(),expr.Mult('x',expr.Sub(3,5)))
        #self.assertEqual(expr.Add(expr.Mult('x',3),expr.Mult(5,'x')).factorise(),expr.Mult('x',expr.Add(3,5)))
        #self.assertEqual(expr.Add(expr.Mult(3,'x'),expr.Mult('x',5)).factorise(),expr.Mult('x',expr.Add(3,5)))
        #self.assertEqual(expr.Add(expr.Mult(3,'x'),expr.Mult(5,'x')).factorise(),expr.Mult('x',expr.Add(3,5)))
        #self.assertEqual(expr.Sub (expr.Pow (expr.Add (expr.Mult (2, 'x'), 3), 2), expr.Pow(5,2)).factorise(),expr.Mult(expr.Add(expr.Add(expr.Mult (2, 'x'), 3),5),expr.Sub(expr.Add(expr.Mult (2, 'x'), 3),5)))
    
    #def test_toPower(self):
        #self.assertEqual(expr.Mult(expr.Pow(expr.Add('x', 3),3),expr.Add('x', 3)).toPower(),expr.Pow(expr.Add('x', 3),expr.Add(3, 1)))
        #self.assertEqual(expr.Mult(expr.Add('x', 3),expr.Pow(expr.Add('x', 3),3)).toPower(),expr.Pow(expr.Add('x', 3),expr.Add(3, 1)))
        #self.assertEqual(expr.Mult(expr.Add('x', 3),expr.Add('x', 3)).toPower(),expr.Pow(expr.Add('x', 3),2))
        #self.assertEqual(expr.Mult(3, 3).toPower(),expr.Pow(3,2))
        #self.assertEqual(expr.Mult(3, 'x').toPower(),expr.Mult(3, 'x'))
        #self.assertEqual(expr.Mult(expr.Pow('x', 3),expr.Pow('x',2)).toPower(),expr.Pow('x',expr.Add(3,2)))
    
    #def test_simplify(self):
        #self.assertEqual(expr.Add(expr.Frac(3,5),expr.Frac(4,5)).simplify(),expr.Frac(expr.Add(3,4),5))
    
    #def test_simplify_sqrt(self):
        #self.assertEqual(expr.Sqrt(expr.Pow(3,2)).simplify(),3)
        #self.assertEqual(expr.Sqrt(16).simplify(),expr.Sqrt(expr.Pow(4,2)))
        
    #def test_doubleDist(self):
        #A=expr.Mult(expr.Add(3,expr.Mult(2,'x')),expr.Sub(expr.Mult(5,'x'),3))
        #B=expr.Add(expr.Sub(expr.Mult(3,expr.Mult(5,'x')),expr.Mult(3,3)),expr.Sub(expr.Mult(expr.Mult(2,'x'),expr.Mult(5,'x')),expr.Mult(expr.Mult(2,'x'),3)))
        #self.assertEqual(A.doubleDist(),B)
            
    #somme6= expr.Add (expr.Mult (152, 'x'), 58)
    #print(somme6.show())
    #AS1=expr.AlgebraicSum([expr.Pow(3,2),expr.Mult(2,expr.Mult(3,'x')),expr.Pow('x',2)])
if __name__ == '__main__':
    unittest.main()

