import itertools

import sys


def similarity(s1, s2):
    """
    >>> similarity('A', 'A')
    2
    >>> similarity('C', 'T')
    -3
    """
    # similarity_matrix = {'A': {'A': 1, 'C': -1, 'G': -1, 'T': -1},
    #                      'C': {'A': -1, 'C': 1, 'G': -1, 'T': -1},
    #                      'G': {'A': -1, 'C': -1, 'G': 1, 'T': -1},
    #                      'T': {'A': -1, 'C': -1, 'G': -1, 'T': 1}}

    similarity_matrix = {'A': {'A': 2, 'C': -3, 'G': -3, 'T': -3},
                         'C': {'A': -3, 'C': 2, 'G': -3, 'T': -3},
                         'G': {'A': -3, 'C': -3, 'G': 2, 'T': -10},
                         'T': {'A': -3, 'C': -3, 'G': -10, 'T': 2}}

    return similarity_matrix[s1][s2]


def global_alighnment(s1, s2, gap_penalty=-2 ):
    """
    :param s1:
    :param s2:
    :return:
    >>> global_alighnment("", "")
    ('', '')

    >>> global_alighnment("", "ACTG")
    ('----', 'ACTG')

    >>> global_alighnment("AACT", "")
    ('AACT', '----')

    >>> global_alighnment("ACGT", "ACGT")
    ('ACGT', 'ACGT')

    >>> global_alighnment("GCATGCA", "GATTACA", -2)
    ('GCATG-CA', 'G-ATTACA')

    >>> global_alighnment("ACTGATTCA", "ACGCATCA", -2)
    ('ACTG-ATTCA', 'AC-GCAT-CA')
    """

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

                max_value = max(match, insert, delete)

                if max_value is match:
                    grid[row][column] = (max_value, 'match')
                if max_value is insert:
                    grid[row][column] = (max_value, 'insert')
                if max_value is delete:
                    grid[row][column] = (max_value, 'delete')

    a_s1 = ''
    a_s2 = ''
    finished = False
    end = (len(s2), len(s1))
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
        if end == (0,0):
            finished = True

    return a_s1, a_s2


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    alignment = global_alighnment(sys.argv[1], sys.argv[2])
    print(alignment[0])
    print(alignment[1])




