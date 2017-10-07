import random

a = ['A', 'C', 'G', 'T']

l = [100, 1000, 100000]

for sequence in l:
    s = ''
    for i in range(sequence):
        s += random.choice(a)
    f = open('blast_sequences/s_' + str(sequence), mode='w')
    f.write(s)
    f.close()
