# From: https://www.hackerrank.com/challenges/climbing-the-leaderboard/problem

#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'climbingLeaderboard' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts following parameters:
#  1. INTEGER_ARRAY ranked
#  2. INTEGER_ARRAY player
#

def puestos_leaderboard(ranked):
    ranked = sorted(ranked, reverse=True)
    puesto = 1
    puestos = []
    for i, j in enumerate(ranked):
        if i==0: puestos.append(puesto)
        else:
            if ranked[i-1] == j:
                puestos.append(puesto)
            else:
                puesto += 1
                puestos.append(puesto)
    return puestos

def climbingLeaderboard(ranked, player):
    # Write your code here
    ranked_iter = list(ranked.copy())
    track_puestos = []
    for i in player:
        ranked_iter = sorted(ranked_iter+[i], reverse=True)
        puestos = puestos_leaderboard(ranked_iter)
        pos = ranked_iter.index(i)
        track_puestos.append(puestos[pos])
    return track_puestos

if __name__ == '__main__':

    ranked_count = int(input().strip())
    if 1<=ranked_count<=2e5: pass
    else: raise Exception('Error ranked count')

    ranked = list(map(int, input().rstrip().split()))

    player_count = int(input().strip())
    if 1<=player_count<=2e5: pass
    else: raise Exception('Error ranked count')

    player = list(map(int, input().rstrip().split()))

    result = climbingLeaderboard(ranked, player)
    for i in result:
        print(i)
