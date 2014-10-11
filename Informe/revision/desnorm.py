#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv

def normalice(cad):
    cad = cad.replace('\\\'a', 'á')
    cad = cad.replace('\\\'e', 'é')
    cad = cad.replace('\\\'{\i}', 'í')
    cad = cad.replace('\\\'o', 'ó')
    cad = cad.replace('\\\'u', 'ú')
    cad = cad.replace('\\~n', 'ñ')
    return cad

data = open(argv[1], 'r').readlines()
out = open(argv[1]+'-out.txt', 'w')
for line in data:
    line = normalice(line)
    out.write(line)
    print line,

out.close()


