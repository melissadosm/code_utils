#!/bin/python3

import math
import os
import random
import re
import sys


def base2(n):
    bin = format(n, 'b') # Built in function for binary: https://docs.python.org/3/library/functions.html
    bin_str = len(max(str(bin).split('0')))  # Finding the longest consecutive numbers
    return bin_str


if __name__ == '__main__':
    n = int(input())
    print(base2(n))
