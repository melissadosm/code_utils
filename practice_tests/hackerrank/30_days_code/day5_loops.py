#!/bin/python3

import math
import os
import random
import re
import sys



if __name__ == '__main__':
    n = int(input())

    if (n<2)|(n>20):
        raise Exception('Constraint')

    for i in range(1,11):
        mult = n * i
        print('{0} x {1} = {2}'.format(n, i, mult))