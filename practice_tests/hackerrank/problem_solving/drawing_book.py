# From: https://www.hackerrank.com/challenges/drawing-book/problem
#!/bin/python3

import os
import sys
import math

#
# Complete the pageCount function below.
#
def pageCount(n, p):
    beginning = math.floor(p/2)
    if n%2==0:
        end = math.floor((n-p+1)/2)
    else:
        end = math.floor((n-p)/2)
    return min(beginning, end)


if __name__ == '__main__':

    n = int(input())
    if 1<=n<=10e5: pass
    else: raise Exception('Error: n')
    
    p = int(input())
    if 1<=p<=n: pass
    else: raise Exception('Error: p')

    result = pageCount(n, p)

    print(result)