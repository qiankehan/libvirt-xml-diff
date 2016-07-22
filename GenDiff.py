#!/bin/python3
'''
The module of rng diff
'''
import os
import re
from lxml import etree
import pdb

'''
Get diff list from xmldiff
Return: a list of the result in xmldiff [operation, xpath, contents]
'''


def getDiff(file_old, file_new):
    cmd = "xmldiff " + file_old + ' ' + file_new + \
        r"""|awk '!/^\]/{printf $0" ";next;}1' | sed 's/ \[/\n[/g'|grep '\[[a-z]'"""
    return list(map(lambda x: re.sub(r'(^\[|\] *(\n|$\Z))', '', x.replace(' ', '', 1)).split(',', 2), os.popen(cmd).readlines()))

'''
Get the included relationship in rngs
'''


def getInclude(schema_dir):
    owd = os.getcwd()
    os.chdir(schema_dir)
    rngs = os.listdir('.')
    result = {}
    for i in rngs:
        result[i] = list(filter(lambda x: i in open(x).read(), rngs))
        result[i].append(i)
    os.chdir(owd)
    return result

'''
Get the definition from element path
'''


def getDef(path):
    return re.match('^.*define[^/]*', path).group()



def expandReferTree(ref_tree, schema_dir):
    include_dict=getInclude(schema_dir)
    os.chdir(schema_dir)
    leaves = list(filter(lambda x: len(x) == 0, ref_tree.getroot().iter('*')))
    for leaf in leaves:
        for rng in include_dict[leaf.attrib["rng"]]:
            for element in etree.parse(rng).findall("//ref[@name='" + leaf.tag + "']"):
                parent_def = element.xpath("ancestor-or-self::define")
                if parent_def == []:
                    return ref_tree
                leaf.append(etree.Element(
                    parent_def[0].attrib["name"], rng=rng, desc=genDescPath(element)))
    return expandReferTree(expandReferTree(ref_tree,schema_dir),schema_dir)

def genDescPath(child_ele):
    parent = child_ele.getparent()
    if parent is None or parent.tag == 'define':
        return ''
    else:
        return genDescPath(parent) + '/' + parent.get('name') + '(' + parent.tag + ')' if parent.tag in ['element', 'attribute'] else genDescPath(parent) + '/' + parent.tag


def genReferTreeFromXpath(xpath, rng, schema_dir):
    define_name = etree.parse(rng).xpath(getDef(xpath))[0].get('name')
    return expandReferTree(etree.ElementTree(etree.Element(define_name, rng=os.path.basename(rng))), schema_dir)


def genAffectPath(refer_leaf):
    return refer_leaf.get('desc') + genAffectPath(refer_leaf.getparent()) if 'desc' in refer_leaf.attrib else '/' + refer_leaf.tag


def genAffectPathAll(refer_tree):
    return list(map(genAffectPath, list(filter(lambda x: x.getchildren() == [], refer_tree.getroot().iter('*')))))
'''
Convert non-namespace xpath to libvirt-rng namespace xpath
'''



if __name__ == '__main__':
    i = genReferTreeFromXpath('/grammar[1]/define[20]', '/exports/projects/rng-diff/examples/v1.3.2/storagepool.rng', '/exports/projects/rng-diff/examples/v1.3.2')
    print(etree.tostring(i, pretty_print=True, encoding='unicode'))
    print(genAffectPathAll(i))
    # tree=etree.parse("/exports/projects/rng-diff/examples/patch/0007237301586aa90f58a7cc8d7cb29a16b00470-1332203610/domaincommon.rng.new")u
