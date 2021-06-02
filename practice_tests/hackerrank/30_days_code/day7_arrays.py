#!/bin/python3

import math
import os
import random
import re
import sys



if __name__ == '__main__':
    n = int(input())
    
    if 1 <= n <= 1000: pass
    else: raise Exception('Hola')

    arr = list(map(int, input().rstrip().split()))

    for i,j in enumerate(arr):
        if 1 <= j <= 10000: pass
        else: raise Exception('Hola')
        print(arr[-(i+1)], end=' ')