# From: https://www.hackerrank.com/challenges/kangaroo/problem
#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the kangaroo function below.
def kangaroo(x1, v1, x2, v2):
    if v2>v1: return 'NO'  # Porque con una tasa menor nunca va a alcanzarlo
    if v2==v1: return 'NO'  # Porque con una tasa menor nunca va a alcanzarlo
    if (x1-x2)%(v2-v1)==0: return 'YES'  # Solving for the equation
    else: return 'NO'


if __name__ == '__main__':

    input_str = input().split()

    x1 = int(input_str[0])
    v1 = int(input_str[1])
    x2 = int(input_str[2])
    v2 = int(input_str[3])

    if 0<=x1<x2<=10000: pass
    else: raise Exception('Error with location')

    if (1<=v1<=10000)&(1<=v2<=10000): pass
    else: raise Exception('Error with rate')

    result = kangaroo(x1, v1, x2, v2)

    print(result)
