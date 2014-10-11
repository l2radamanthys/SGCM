#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
import codecs

def normalice(cad):
    cad = cad.replace('�', '\\\'a')
    cad = cad.replace('�', '\\\'e')
    cad = cad.replace('�', '\\\'{\i}')
    cad = cad.replace('�', '\\\'o')
    cad = cad.replace('�', '\\\'u')
    cad = cad.replace('�', '\\~n')
    return cad
#iso-8859-1'
data = open(argv[1], 'r').readlines()
out = open(argv[1]+'-out.txt', 'w')
for line in data:
    line = normalice(line)

    out.write(line)
    print line,

out.close()


