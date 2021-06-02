#!/bin/python3

import math
import os
import random
import re
import sys



if __name__ == '__main__':
    t = int(input())

    if (t<1)|(t>10):
        raise Exception('Integer Exception')
       
    for i in range(t):
        str1 = str(input())
        if (len(str1)<2)|(len(str1)>10000):
            raise Exception('String Exception')
        for i, s in enumerate(str1):
            if i%2==0: print(s, end='')
        print(' ', end='')
        for i, s in enumerate(str1):
            if i%2!=0: print(s, end='')
        print(' ')
