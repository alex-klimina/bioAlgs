from __future__ import print_function
import itertools
import sys


def similarity(s1, s2):
    """
    >>> similarity('A', 'A')
    2
    >>> similarity('C', 'T')
    -3
    """
    if s1 == s2:
        return 2
    else:
        return -3


def local_alighnment(s1, s2):
    """
    :param s1:
    :param s2:
    :return:
    >>> local_alighnment("", "")
    ('', '')

    >>> local_alighnment("", "ACTG")
    ('----', 'ACTG')

    >>> local_alighnment("AACT", "")
    ('AACT', '----')

    >>> local_alighnment("ACGT", "ACGT")
    ('ACGT', 'ACGT')

    >>> local_alighnment("ACTGATTCA", "ACGCATCA")
    ('ACTG-ATTCA', 'AC-GCAT-CA')

    >>> local_alighnment("tccCAGTTATGTCAGgggacacgagcatgcagagac", "aattgccgccgtcgttttcagCAGTTATGTCAGatc")
    ('                  TCCCAGTTATGTCAGGGGACACGAGCATGCAGAGAC', 'AATTGCCGCCGTCGTTTTCAGCAGTTATGTCAGATC                  ')
    """


    gap_penalty = -2

    s1 = s1.upper()
    s2 = s2.upper()

    if s1 is "":
        a_s1 = ''
        for _ in itertools.repeat(None, len(s2)):
            a_s1 += '-'
        return a_s1, s2

    if s2 is "":
        a_s2 = ''
        for _ in itertools.repeat(None, len(s1)):
            a_s2 += '-'
        return s1, a_s2

    grid = [[(0, 'gap') for x in range(len(s1)+1)] for x in range(len(s2)+1)]
    for row in range(len(s2)+1):
        for column in range(len(s1)+1):
            if row == 0:
                grid[row][column] = (gap_penalty * column, 'delete')
            if column == 0:
                grid[row][column] = (gap_penalty * row, 'insert')
            if row != 0 and column != 0:
                match = grid[row-1][column-1][0] + similarity(s2[row-1], s1[column-1])
                insert = grid[row-1][column][0] + gap_penalty
                delete = grid[row][column-1][0] + gap_penalty
                begin = 0

                max_value = max(match, insert, delete, begin)

                if max_value is match:
                    grid[row][column] = (max_value, 'match')
                if max_value is insert:
                    grid[row][column] = (max_value, 'insert')
                if max_value is delete:
                    grid[row][column] = (max_value, 'delete')
                if max_value is begin:
                    grid[row][column] = (max_value, 'begin')


    finished = False
    end = (len(s2), len(s1))
    max_path = 0
    for row in range(len(s2)+1):
        for column in range(len(s1)+1):
            max_path = max(max_path, grid[row][column][0])
    for row in range(len(s2)+1):
        for column in range(len(s1)+1):
            # print(row, column, max_path, grid[row][column])
            if max_path == grid[row][column][0]:
                end = (row, column)



    a_s1 = s1[end[1]:]
    a_s2 = s2[end[0]:]
    if len(a_s1) > len(a_s2):
        a_s2 += ' '*(len(a_s1) - len(a_s2))
    else:
        a_s1 += ' '*(len(a_s2) - len(a_s1))


    while not finished:
        if grid[end[0]][end[1]][1] is 'match':
            a_s1 = s1[end[1] - 1] + a_s1
            a_s2 = s2[end[0] - 1] + a_s2
            end = (end[0]-1, end[1]-1)
        elif grid[end[0]][end[1]][1] is 'insert':
            a_s1 = '-' + a_s1
            a_s2 = s2[end[0] - 1] + a_s2
            end = (end[0]-1, end[1])
        elif grid[end[0]][end[1]][1] is 'delete':
            a_s1 = s1[end[1] - 1] + a_s1
            a_s2 = '-' + a_s2
            end = (end[0], end[1]-1)
        if grid[end[0]][end[1]][0] == 0:
            if end[1] < end[0]:
                a_s1 = ' '*(end[0] - end[1]) + s1[:end[1]] + a_s1
                a_s2 = s2[:end[0]] + a_s2
            else:
                a_s1 = s1[:end[1]] + a_s1
                a_s2 = ' '*(end[1] - end[0]) + s2[:end[0]] + a_s2
            end = (0,0)
        if end == (0,0):
            finished = True

    return a_s1, a_s2


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    alignment = local_alighnment(sys.argv[1], sys.argv[2])

    print(alignment[0])
    for i in range(len(alignment[0])):
        if alignment[0][i] == alignment[1][i]:
            print('|', end='')
        else:
            print(' ', end='')
    print()
    print(alignment[1])
