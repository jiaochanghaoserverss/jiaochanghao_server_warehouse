#!/usr/bin/python 
# -*- coding: utf-8 -*-  

# ----------------------------------#
# longest common string            #
# ----------------------------------#
def lcs(left, right):
    """
    longest common string
    dynamic programming
    if without lcs, return empty string
    """
    (left_len, right_len, left_lcspos, lcs_len) = (len(left), len(right), 0, 0)
    matrix = []
    for row in range(left_len + 1):
        matrix.append([0] * (right_len + 1))

    for row in range(0, left_len):
        for col in range(0, right_len):
            if left[row] == right[col]:
                matrix[row + 1][col + 1] = matrix[row][col] + 1
                if matrix[row + 1][col + 1] > lcs_len:
                    lcs_len = matrix[row + 1][col + 1]
                    left_lcspos = row + 1 - lcs_len
            else:
                matrix[row][col] = 0

    return left[left_lcspos:left_lcspos + lcs_len]


# ----------------------------------#
# String edit distance/similarity  #
# ----------------------------------#
def levenshtein(a, b):
    """
    edit distance/levenshtein distance between a and b
    """
    if len(a) == 0:
        return len(b)
    if len(b) == 0:
        return len(a)
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n

    current = list(range(n + 1))
    for i in range(1, m + 1):
        previous, current = current, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete = previous[j] + 1, current[j - 1] + 1
            change = previous[j - 1]
            if a[j - 1] != b[i - 1]:
                change = change + 2
            current[j] = min(add, delete, change)
    return current[n]


def similarity(a, b):
    """
    similarity between a and b
    """
    t = len(a) + len(b)
    if t == 0:
        return 0.0
    mx = max(len(a), len(b))
    mn = min(len(a), len(b))
    ld = levenshtein(a, b)
    return float(t - ld) / float(t)
