"""
In this assignment you should fit a model function of your choice to data 
that you sample from a contour of given shape. Then you should calculate
the area of that shape. 


#sort by x and y
#polygon

The sampled data is very noisy so you should minimize the mean least squares 
between the model you fit and the data points you sample.  

During the testing of this assignment running time will be constrained. You
receive the maximal running time as an argument for the fitting method. You 
must make sure that the fitting function returns at most 5 seconds after the 
allowed running time elapses. If you know that your iterations may take more 
than 1-2 seconds break out of any optimization loops you have ahead of time.

Note: You are allowed to use any numeric optimization libraries and tools you want
for solving this assignment. 
Note: !!!Despite previous note, using reflection to check for the parameters 
of the sampled function is considered cheating!!! You are only allowed to 
get (x,y) points from the given shape by calling sample(). 
"""

import sys
import numpy as np
import time
import random
from functionUtils import AbstractShape
import math
from scipy.interpolate import splprep, splev


def findArea(points, length):
    area = 0
    for i in range(0, length - 1):
        curr = points[i]
        next = points[(i + 1)]
        mid = (curr[1] + next[1]) / 2
        area = area + np.float32((mid * (next[0] - curr[0])))
    curr = points[length - 1]
    next = points[0]
    mid = (curr[1] + next[1]) / 2
    area = area + np.float32((mid * (next[0] - curr[0])))
    return np.float32(abs(area))

    pt_center[0] = pt_center[0] / length
    pt_center[1] = pt_center[1] / length

    sorted = []
    for pt in points:
        sorted[0] = points[0] - pt_center[0]
        sorted[1] = points[1] - pt_center[1]
        sorted.append((pt[0], pt[1]))
    return points




class MyShape(AbstractShape):
    # change this class with anything you need to implement the shape
    def __init__(self,ass5,points,area):
        self.ass5=ass5
        self.points= points
        self.sArea=area
        self.usedPoints=[]
    def contour(self, n):
        if(n>len(self.points)):
            return self.points
        else:
            pts=[]
            for i in range(n):
                pts.append(self.points[i])
        return pts

    def area(self):
        return self.sArea

    def sample(self):
        flag=False
        while not flag:
            i = random.randint(0, len(self.points))
            point = self.points[i]
            flag= point not in self.usedPoints
        self.usedPoints.append(point)
        return point






class Assignment5:
    def __init__(self):
        """
        Here goes any one time calculation that need to be made before 
        solving the assignment for specific functions. 
        """

        pass

    def area(self, contour: callable, maxerr=0.001)->np.float32:
        """
        Compute the area of the shape with the given contour. 

        Parameters
        ----------
        contour : callable
            Same as AbstractShape.contour 
        maxerr : TYPE, optional
            The target error of the area computation. The default is 0.001.

        Returns
        -------
        The area of the shape.
    """

        startT = time.time()
        lastArea= 0
        Flag=False
        length=200
        while(not Flag and length<=10000):
            points = contour(length)
            currArea= findArea(points,len(points))
            if(abs(currArea-lastArea)<maxerr):
                Flag=True
            elif(time.time()-startT>0.5):
                points = contour(10000)
                lastArea= findArea(points,10000)
                break
            else:
                lastArea=currArea
                length = length * 2


        return np.float32(abs(lastArea))

    
    def fit_shape(self, sample: callable, maxtime: float) -> AbstractShape:
        """
        Build a function that accurately fits the noisy data points sampled from
        some closed shape. 
        
        Parameters
        ----------
        sample : callable. 
            An iterable which returns a data point that is near the shape contour.
        maxtime : float
            This function returns after at most maxtime seconds. 

        Returns
        -------
        An object extending AbstractShape. 
        """




        length = 10000
        points = []
        sumx=0
        sumy=0
        for x in range(0,length):
            p = sample()
            sumx+=p[0]
            sumy+=p[1]
            points.append(p)
        points=np.array(points,dtype=np.longdouble)
        midPoint = [sumx/length, sumy/length]

        def clockwiseangle_Sort(point):
            vector = [point[0] - midPoint[0], point[1] - midPoint[1]]
            distance = math.hypot(vector[0], vector[1])
            if distance == 0:
                return -math.pi, 0
            angle = math.atan2(vector[0] / distance, vector[1] / distance)
            if angle < 0:
                return math.pi*2 + angle, distance
            return angle, distance

        points=np.array(sorted(points,key=clockwiseangle_Sort))
        ass5= Assignment5()
        area= findArea(points,length)
        result = MyShape(ass5,points,area)
        return result


##########################################################################


import unittest
from sampleFunctions import *
from tqdm import tqdm


class TestAssignment5(unittest.TestCase):

    def test_return(self):
        circ = noisy_circle(cx=1, cy=1, radius=1, noise=0.1)
        ass5 = Assignment5()
        T = time.time()
        shape = ass5.fit_shape(sample=circ, maxtime=5)
        T = time.time() - T
        self.assertTrue(isinstance(shape, AbstractShape))
        self.assertLessEqual(T, 5)

    def test_delay(self):
        circ = noisy_circle(cx=1, cy=1, radius=1, noise=0.1)

        def sample():
            time.sleep(7)
            return circ()

        ass5 = Assignment5()
        T = time.time()
        shape = ass5.fit_shape(sample=sample, maxtime=5)
        T = time.time() - T
        self.assertTrue(isinstance(shape, AbstractShape))
        self.assertGreaterEqual(T, 5)

    def test_circle_area(self):
        circ = noisy_circle(cx=1, cy=1, radius=1, noise=0.1)
        ass5 = Assignment5()
        T = time.time()
        shape = ass5.fit_shape(sample=circ, maxtime=30)
        T = time.time() - T
        a = shape.area()
        self.assertLess(abs(a - np.pi), 0.01)
        self.assertLessEqual(T, 32)

    def test_bezier_fit(self):
        circ = noisy_circle(cx=1, cy=1, radius=1, noise=0.1)
        ass5 = Assignment5()
        T = time.time()
        shape = ass5.fit_shape(sample=circ, maxtime=30)
        T = time.time() - T
        a = shape.area()
        self.assertLess(abs(a - np.pi), 0.01)
        self.assertLessEqual(T, 32)



if __name__ == "__main__":
   unittest.main()
