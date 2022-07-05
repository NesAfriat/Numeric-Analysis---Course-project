"""
In this assignment you should find the area enclosed between the two given functions.
The rightmost and the leftmost x values for the integration are the rightmost and 
the leftmost intersection points of the two functions. 

The functions for the numeric answers are specified in MOODLE. 

#a - simpson
#b- simpson


This assignment is more complicated than Assignment1 and Assignment2 because: 
    1. You should work with float32 precision only (in all calculations) and minimize the floating point errors. 
    2. You have the freedom to choose how to calculate the area between the two functions. 
    3. The functions may intersect multiple times. Here is an example: 
        https://www.wolframalpha.com/input/?i=area+between+the+curves+y%3D1-2x%5E2%2Bx%5E3+and+y%3Dx
    4. Some of the functions are hard to integrate accurately. 
       You should explain why in one of the theoretical questions in MOODLE. 

"""
import sys

import numpy as np
import time
import random

import assignment2


class Assignment3:
    def __init__(self):
        """
        Here goes any one time calculation that need to be made before 
        solving the assignment for specific functions. 
        """

        pass



    def integrate(self, f: callable, a: float, b: float, n: int) -> np.float32:
        """
        Integrate the function f in the closed range [a,b] using at most n 
        points. Your main objective is minimizing the integration error. 
        Your secondary objective is minimizing the running time. The assignment
        will be tested on variety of different functions. 
        
        Integration error will be measured compared to the actual value of the 
        definite integral. 
        
        Note: It is forbidden to call f more than n times. 

        Parameters
        ----------
        f : callable. it is the given function
        a : float
            beginning of the integration range.
        b : float
            end of the integration range.
        n : int
            maximal number of points to use.

        Returns
        -------
        np.float32
            The definite integral of f between a and b
        """

        # Simpson's 1/3
        if(n%2==1):
            newN= n-1
        else:
            newN= n-2
        step = (b - a) / newN
        eve=0
        odd=0
        for i in range(1, newN):
            j = a + i * step
            func = f(j)
            if i % 2 == 0:
                eve = eve + func
            else:
                odd = odd + func
        integration = (f(a) + f(b)+(2*eve)+(4*odd)) * step / 3
        return np.float32(integration)


    def areabetween(self, f1: callable, f2: callable) -> np.float32:
        """
        Finds the area enclosed between two functions. This method finds 
        all intersection points between the two functions to work correctly. 
        
        Example: https://www.wolframalpha.com/input/?i=area+between+the+curves+y%3D1-2x%5E2%2Bx%5E3+and+y%3Dx

        Note, there is no such thing as negative area. 
        
        In order to find the enclosed area the given functions must intersect 
        in at least two points. If the functions do not intersect or intersect 
        in less than two points this function returns NaN.  
        This function may not work correctly if there is infinite number of 
        intersection points. 
        

        Parameters
        ----------
        f1,f2 : callable. These are the given functions

        Returns
        -------
        np.float32
            The area between function and the X axis

        """
        ass2= assignment2.Assignment2()
        inters =ass2.intersections(f1 , f2, 1, 100, 0.002)
        length= len(inters)
        sum= 0
        for i in range(0,length-1):
            sum= sum+ np.float32(abs(self.integrate(f1,inters[i],inters[i+1], 500)-(self.integrate(f2,inters[i],inters[i+1],500))))
        result = np.float32(sum)

        return result


##########################################################################


import unittest
from sampleFunctions import *
from tqdm import tqdm


class TestAssignment3(unittest.TestCase):

    def test_integrate_float32(self):
        ass3 = Assignment3()
        f1 = np.poly1d([-1, 0, 1])
        r = ass3.integrate(f1, -1, 1, 10)

        self.assertEquals(r.dtype, np.float32)

    def test_integrate_hard_case(self):
        ass3 = Assignment3()
        f1 = lambda x: 2.0 ** (1 / (x ** 2)) * np.sin(1 / x)
        r = ass3.integrate(f1, 0.09, 10, 20)
        true_result = -7.78662 * 10 ** 33
        self.assertGreaterEqual(0.001, abs((r - true_result) / true_result))

    def test_integrate_hard_case2(self):
        ass3 = Assignment3()
        f1 = lambda x: np.sin(100 / x)
        r = ass3.integrate(f1, 0.09, 10, 20)
        true_result = -0.8946105807309636
        self.assertGreaterEqual(0.001, abs((r - true_result) / true_result))

    def test_areeBetween1(self):
        print("testArea")
        ass3 = Assignment3()
        f1, f2 = lambda x: -6 * (x - 7) * 4 + 24 * x - 29, lambda x: x * 2 - 10 * x - 5
        T = time.time()
        X = ass3.areabetween(f1,f2)
        T = time.time() - T
        print(T)
        print(X)
        expected=54252
        print("expected:",expected)
        print("error= ",abs(X-expected))

    def test_areeBetween2(self):
        print("testArea")
        ass3 = Assignment3()
        f1, f2 = lambda x: x**2, lambda x: x * 2 - 10 * x - 5
        T = time.time()
        X = ass3.areabetween(f1, f2)
        T = time.time() - T
        print(T)
        print(X)
        expected = 373824
        print("expected:", expected)
        print("error= ", abs(X - expected))

    def test_areeBetween3(self):
        print("testArea")
        ass3 = Assignment3()
        f1, f2 = lambda x:x**2 , lambda x: np.sin(100 / x)
        T = time.time()
        X = ass3.areabetween(f1, f2)
        T = time.time() - T
        print(T)
        print(X)
        expected = 333283
        print("expected:", expected)
        print("error= ", abs(X - expected))
if __name__ == "__main__":
    unittest.main()
