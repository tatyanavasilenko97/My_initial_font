#!/usr/bin/python3
#-*- coding: UTF-8 -*-
import numpy as np
from numpy import pi


class BezierCurve:
    def __init__(self, knots, values, segments_count):
        self.n = len(knots)
        self.knots = knots
        self.values = values
        self.segments_count = segments_count
        
        if (len(knots) != len(values)):
            raise ValueError("knots and values should be same length")
        if (self.n % 4 != 0):
            raise ValueError("knots and values should have length divided by 4")
        if (self.n / 4 != segments_count):
            raise ValueError("knots and values should have length divided by segments_count(%d)" % segments_count)

        self.A = np.zeros((self.segments_count, 2, 4))
        for seg, i in zip(range(self.segments_count), range(0, self.n, 4)):
            self.A[seg] = knots[i : i+4], values[i : i+4]

    def value(self, x):
        if (x < 0.0) and (x > self.segments_count):
            raise ValueError("{%f} not in curve" % x)
        
        segment_number = min(int(np.floor(x)), self.segments_count - 1)
        t = x - segment_number
        t_i = np.array([
            (1 - t) ** 3,
            3 * ((1 - t) ** 2) * t,
            3 * (1 - t) * (t ** 2),
            t ** 3
        ])

        return t_i.dot(self.A[segment_number][0]), t_i.dot(self.A[segment_number][1])

    def control_points(self):
        return self.A
        lst = []
        lst2 = []
        lst3 = []
        for x_array, y_array in self.A:
            curve = dict()
            curve["p0"] = dict(x=x_array[0],y=y_array[0])
            curve["p1"] = dict(x=x_array[1],y=y_array[1])
            curve["p2"] = dict(x=x_array[2],y=y_array[2])
            curve["p3"] = dict(x=x_array[3],y=y_array[3])
            lst.append(curve)
            lst2.append(x_array.tolist())
            lst3.append(y_array.tolist())
            print(x_array.tolist())
            print(y_array.tolist())
        print(lst2)
        print(lst3)
        #with open('data.txt', 'w') as outfile:
        #    json.dump(lst, outfile)
