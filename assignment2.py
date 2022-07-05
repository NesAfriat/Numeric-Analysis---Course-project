"""
In this assignment you should find the intersection points for two functions.
"""
import sys

import numpy as np
import time
import random
from collections.abc import Iterable


class Assignment2:
    def __init__(self):
        """
        Here goes any one time calculation that need to be made before 
        solving the assignment for specific functions. 
        """

        pass



    def falsePosition(self,func,x0, x1, maxerr):
        flag = True
        while flag:
            func0= func(x0)
            func1= func(x1)
            x2 = x0 - (x1 - x0) * func0 / (func1 - func0)
            func2= func(x2)
            if (func1 * func2) < 0:
                x1 = x2
            else:
                x0 = x2
            flag =  maxerr < abs(func(x2))
        return x2

    def intersections(self, f1: callable, f2: callable, a: float, b: float, maxerr=0.001) -> Iterable:
        """
        Find as many intersection points as you can. The assignment will be
        tested on functions that have at least two intersection points, one
        with a positive x and one with a negative x.
        
        This function may not work correctly if there is infinite number of
        intersection points. 


        Parameters
        ----------
        f1 : callable
            the first given function
        f2 : callable
            the second given function
        a : float
            beginning of the interpolation range.
        b : float
            end of the interpolation range.
        maxerr : float
            An upper bound on the difference between the
            function values at the approximate intersection points.


        Returns
        -------
        X : iterable of approximate intersection Xs such that for each x in X:
            |f1(x)-f2(x)|<=maxerr.

        """


        newFunc= lambda x : f1(x)-f2(x)
        flag=1
        ans= []
        eps= 0.000001
        leftP=a
        rightP=a+maxerr+eps
        while(leftP<=b):
            length= len(ans)
            lFunc=newFunc(leftP)
            if (abs(lFunc) < maxerr):
                        ans.append(leftP)
                        leftP =  rightP
                        rightP = leftP + maxerr + eps
                        flag=2
            elif(lFunc*newFunc(rightP)<0):
                newX= self.falsePosition(newFunc,leftP,rightP,maxerr)
                if(length<1 or (abs(newX-ans[length-1])>maxerr)):
                    ans.append(newX)
                    leftP= newX + maxerr +eps
                    rightP = leftP + maxerr +eps
                    flag = 2
            else:
                if(flag ==3):
                    leftP=leftP-maxerr/2
                    rightP= leftP+maxerr+eps
                    flag=4
                else:
                    flag = flag+1
                    leftP = rightP
                    rightP = rightP+ maxerr + eps


        return ans


##########################################################################


import unittest
from sampleFunctions import *
from tqdm import tqdm


class TestAssignment2(unittest.TestCase):

    def test_sqr(self):

        ass2 = Assignment2()

        f1 = lambda x: np.sin(100 / x)
        f2 = lambda x: 0
        T = time.time()
        X = ass2.intersections(f1, f2, 1, 4, maxerr=0.001)
        T = time.time() - T
        print(T)
        print(X)
        print(len(X))
        for x in X:
            self.assertGreaterEqual(0.001, abs(f1(x) - f2(x)))
        for i in range(len(X) - 1):
            self.assertLess(0.001, abs(X[i] - X[i + 1]))

    def test_sqr2(self):
        print("test2")
        ass2 = Assignment2()
        f1, f2 = lambda x: x**2, lambda x: 0
        T = time.time()
        X = ass2.intersections(f1, f2, -1, 4, maxerr=0.001)
        T = time.time() - T
        print(T)
        print(X)
        print(len(X))
        for x in X:
            self.assertGreater(0.001, abs(f1(x) - f2(x)))
        for i in range(len(X)-1):
            self.assertLess(0.001, abs(X[i]-X[i+1]))


    def test_sqr1(self):
        print("test1")
        ass2 = Assignment2()
        f1, f2 = lambda x: -6 * (x - 7) * 4 + 24 * x - 29, lambda x: x * 2 - 10 * x - 5
        T = time.time()
        X = ass2.intersections(f1, f2, -100, 100, maxerr=0.001)
        T = time.time() - T
        print(T)
        print(X)
        print(len(X))
        for x in X:
            self.assertGreaterEqual(0.001, abs(f1(x) - f2(x)))
        for i in range(len(X) - 1):
            self.assertLess(0.001, abs(X[i] - X[i + 1]))



    def test_poly(self):

        ass2 = Assignment2()

        f1, f2 = randomIntersectingPolynomials(10)

        X = ass2.intersections(f1, f2, 1, 21, maxerr=0.001)
        print(X)

        for x in X:
            self.assertGreaterEqual(0.001, abs(f1(x) - f2(x)))

if __name__ == "__main__":
    unittest.main()
