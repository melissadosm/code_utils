# From: https://www.hackerrank.com/challenges/grading/problem
#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'gradingStudents' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts INTEGER_ARRAY grades as parameter.
#

def gradingStudents(grades):
    # Write your code here
    final_grades = []
    for i in grades:
        if i < 38:
            final = i
        elif 5 - (i%5) < 3:
            final = i+(5-(i%5))
        else:
            final = i
        final_grades.append(final)
    return final_grades

if __name__ == '__main__':
    grades_count = int(input().strip())
    if (1<=grades_count<=60): pass
    else: raise Exception('Wrong')

    grades = []

    for _ in range(grades_count):
        grades_item = int(input().strip())
        if (0<=grades_item<=100): pass
        else: raise Exception('Wrong')
        grades.append(grades_item)

    result = gradingStudents(grades)

    [print(i) for i in result]