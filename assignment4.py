"""
In this assignment you should fit a model function of your choice to data 
that you sample from a given function. 


#least square of bezzier

The sampled data is very noisy so you should minimize the mean least squares 
between the model you fit and the data points you sample.  

During the testing of this assignment running time will be constrained. You
receive the maximal running time as an argument for the fitting method. You 
must make sure that the fitting function returns at most 5 seconds after the 
allowed running time elapses. If you take an iterative approach and know that 
your iterations may take more than 1-2 seconds break out of any optimization 
loops you have ahead of time.

Note: You are NOT allowed to use any numeric optimization libraries and tools 
for solving this assignment. 

"""
import sys

import numpy
import numpy as np
import time
import random


class Assignment4A:
    def __init__(self):
        """
        Here goes any one time calculation that need to be made before 
        solving the assignment for specific functions. 
        """

        pass

    def fit(self, f: callable, a: float, b: float, d:int, maxtime: float) -> callable:
        """
        Build a function that accurately fits the noisy data points sampled from
        some closed shape. 
        
        Parameters
        ----------
        f : callable. 
            A function which returns an approximate (noisy) Y value given X. 
        a: float
            Start of the fitting range
        b: float
            End of the fitting range
        d: int 
            The expected degree of a polynomial matching f
        maxtime : float
            This function returns after at most maxtime seconds. 

        Returns
        -------
        a function:float->float that fits f between a and b
        """
        #take as many samples as possible of (x,y)
        def collectPoint(f,a,b):
            pt = random.uniform(a,b)
            return (pt,f(pt))

        """
            Returns the inverse of a matrix.
            params: The matrix
            returns: The inverse of A
                 """
        def invertMatrix(A):
            AC = A.copy()
            n = len(A)
            I = np.identity(n)
            ind = list(range(n))
            for m in range(0,n):
                diag = 1/AC[m][m]
                for j in range(0,n):
                    AC[m][j] *= diag
                    I[m][j] *= diag
                for i in ind[0:m] + ind[m + 1:]:
                    row = AC[i][m]
                    for j in range(0,n):
                        I[i][j] = I[i][j] - row * I[m][j]
                        AC[i][j] = AC[i][j] - row * AC[m][j]
            return I

        flag=True
        startT=time.time()
        points= [(a, f(a)),(b,f(b))]
        while(flag):
            length= len(points)
            i=0
            while(i<length-1):
                points.insert(i+1,collectPoint(f,points[i][0],points[i+1][0]))
                i=i+2
                length=length+1
                if(time.time()-startT>=0.6*maxtime):
                    flag=False
                    break
        points= np.array(points)

        #create the A matrix first col - xs, rest (d-1) - 1's
        arrX= np.array([x[0] for x in points], dtype= np.longdouble)
        AT=np.array([np.ones(len(arrX))])
        for i in range(1,d+1):
            temp= np.array([np.float_power(arrX,i)],dtype= np.longdouble)
            AT=np.row_stack((temp, AT))
        A= AT.transpose()
        #create b matrix - 1 col the y values
        B = np.array([y[1] for y in points],dtype= np.longdouble)
        #create AT*A
        ATA= np.dot(AT,A)
        #create AT*B
        ATB= np.dot(AT,B)
        #solve AT*A= AT*B with ranking or solve
        invRight= np.dot(invertMatrix(ATA),ATB)
        X=invRight
        p=np.poly1d(X)
        result = lambda x: p(x)
        return result


##########################################################################


import unittest
from sampleFunctions import *
from tqdm import tqdm


class TestAssignment4(unittest.TestCase):
    
    def test_return(self):
        f = NOISY(0.01)(poly(1,1,1))
        ass4 = Assignment4A()
        T = time.time()
        shape = ass4.fit(f=f, a=0, b=1, d=10, maxtime=5)
        T = time.time() - T
        self.assertLessEqual(T, 5)

    def test_delay(self):
        f = DELAYED(7)(NOISY(0.01)(poly(1,1,1)))

        ass4 = Assignment4A()
        T = time.time()
        shape = ass4.fit(f=f, a=0, b=1, d=10, maxtime=5)
        T = time.time() - T
        self.assertGreaterEqual(T, 5)

    def test_err(self):
        f = poly(1,1,1)
        nf = NOISY(1)(f)
        ass4 = Assignment4A()
        T = time.time()
        ff = ass4.fit(f=nf, a=0, b=1, d=10, maxtime=5)
        T = time.time() - T
        mse=0
        for x in np.linspace(0,1,1000):            
            self.assertNotEquals(f(x), nf(x))
            mse+= (f(x)-ff(x))**2
        mse = mse/1000
        print(mse)


        



if __name__ == "__main__":
    unittest.main()
