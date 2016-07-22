#!/usr/bin/env python3
import re
import os
import GenDiff
import sys
RELAX_RG = ['basictypes.rng', 'capability.rng', 'domaincaps.rng', 'domaincommon.rng', 'domain.rng', 'domainsnapshot.rng', 'interface.rng', 'Makefile.am',
            'networkcommon.rng', 'network.rng', 'nodedev.rng', 'nwfilter.rng', 'secret.rng', 'storagecommon.rng', 'storagepool.rng', 'storagevol.rng']
for j in RELAX_RG:
    file_old = '/exports/projects/rng-diff/examples/' + sys.argv[1] + '/' + j
    file_new = '/exports/projects/rng-diff/examples/' + sys.argv[2] + '/' + j
    print(j + '----------------------------------------')
    array = sorted(list(filter(lambda y: re.match(
        '.*define.*', y[1]) is not None, GenDiff.getDiff(file_old, file_new))), key=lambda x: x[1])
    if array == []:
        print('    File no change\n')
        continue
    changed_def = list(set(map(GenDiff.getDef, [i[1] for i in array])))
    for xpath in changed_def:
        print(xpath + ' Affects' + '--------------------')
        for affect in GenDiff.genAffectPathAll(GenDiff.genReferTreeFromXpath(xpath,
                                                                             file_new, '/exports/projects/rng-diff/examples/' + sys.argv[2])):
            print('    ' + affect)
    print('\n')
