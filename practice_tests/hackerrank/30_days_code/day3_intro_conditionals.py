#!/bin/python3

import math
import os
import random
import re
import sys

def n_print(n):
    if n%2!=0: print('Weird')
    else:
        if (n>=2)&(n<=5): print('Not Weird')
        if (n>=6)&(n<=20): print('Weird')
        if (n>20): print('Not Weird') 


if __name__ == '__main__':
    N = int(input())
    if ((N<1)|(N>100)):
        raise Exception("Integer constraint") 
    n_print(N)