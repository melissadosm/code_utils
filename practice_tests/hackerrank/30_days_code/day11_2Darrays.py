#!/bin/python3

import math
import os
import random
import re
import sys
import numpy as np

def sum_hourglass(hourglass):
    return sum(hourglass)

if __name__ == '__main__':
    arr = []

    for _ in range(6):
        arr.append(list(map(int, input().rstrip().split())))

    arr = np.stack(arr, axis=0 )

    for i in range(3):
        for j in range(3):
            print(sum_hourglass(arr[i:i+3, j:j+3]))