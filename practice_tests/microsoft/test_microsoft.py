

import collections, numpy

def precision_recall(data, drawn, target='a'):
    TP = drawn.count(target)
    FP = len(drawn) - TP
    TN = data.count(target)
    FN = len(data) - TN

    precision = TP / (TP + FP)
    recall = TP / (TP + FN)

    F1 = 2 * ((precision * recall) / (precision + recall))
    return precision, recall, F1


data = ['a', 'b', 'c', 'a', 'b', 'b']
drawn = ['a', 'b', 'c']
print(precision_recall(data, drawn))