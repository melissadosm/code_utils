# From: https://www.hackerrank.com/challenges/between-two-sets/problem
#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'getTotalX' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER_ARRAY a
#  2. INTEGER_ARRAY b
#

def getTotalX(a, b):
    # Write your code here
    low = a[-1]
    high = b[0]
    fin_low = []
    fin_high = []
    for i in range(low, high+1):
        div_low = True
        for l in a:
            if i%l!=0: 
                div_low = False
                break
        if div_low: fin_low.append(i)

    for i in fin_low:
        mult_high = True
        for l in b:
            if l%i!=0: 
                mult_high = False
                break
        if mult_high: fin_high.append(i)
    return len(fin_high)
    

if __name__ == '__main__':

    first_multiple_input = input().rstrip().split()

    n = int(first_multiple_input[0])
    m = int(first_multiple_input[1])
    if (1<=n<=10) & (1<=m<=10): pass
    else: raise Exception('Error')

    arr = list(map(int, input().rstrip().split()))
    brr = list(map(int, input().rstrip().split()))
    if any(a < 1 for a in arr) | any(b < 1 for b in arr): raise Exception('Error')
    if any(a > 100 for a in arr) | any(b > 100 for b in arr): raise Exception('Error')
    
    total = getTotalX(arr, brr)

    print(total)
