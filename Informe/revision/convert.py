#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
import codecs

def normalice(cad):
    cad = cad.replace('á', '\\\'a')
    cad = cad.replace('é', '\\\'e')
    cad = cad.replace('í', '\\\'{\i}')
    cad = cad.replace('ó', '\\\'o')
    cad = cad.replace('ú', '\\\'u')
    cad = cad.replace('ñ', '\\~n')
    return cad
#iso-8859-1'
data = open(argv[1], 'r').readlines()
out = open(argv[1]+'-out.txt', 'w')
for line in data:
    line = normalice(line)

    out.write(line)
    print line,

out.close()


