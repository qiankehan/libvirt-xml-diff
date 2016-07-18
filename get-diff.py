#!/bin/python3
import os
import re
import sys
from lxml import etree

'''
Get diff list from xmldiff
'''


def getDiff(file_old, file_new):
    return list(map(lambda x: re.sub(r'(^\[|\] *(\n|$\Z))', '', x.replace(' ', '', 1)).split(',', 2), os.popen("xmldiff " + file_old + ' ' + file_new + "|awk '!/^\]/{printf $0" ";next;}1'").readlines()))

'''
Get the included relationship in rngs
'''


def getInclude(schema_dir):
    os.chdir(schema_dir)
    rngs = os.listdir('.')
    result = {}
    for i in rngs:
        result[i] = list(filter(lambda x: i in open(x).read(), rngs))
        result[i].append(i)
    return result

'''
Get the definition from element path
'''


def getDef(path):
    return re.match('^.*define[^/]*', path).group()


def getReferedDef(def_xpath, rng, schema_dir):
    result = {}
    include_dict = getInclude(schema_dir)
    for name in n:
        for file_include in include_dict[name_file[name]]:
            tree = etree.parse(file_include)
            for element in tree.findall("//ref[@name='" + name + "']"):
                parent_def = element.xpath("ancestor-or-self::xmlns:define")[0]
                result[parent_def.attrib["name"]] = file_include
    return result


def expandReferTree(ref_tree, include_dict):
    leaves = list(filter(lambda x: len(x) == 0, ref_tree.getroot().iter('*')))
    for leaf in leaves:
        for rng in include_dict[leaf.attrib["rng"]]:
            for element in etree.parse(rng).findall("//ref[@name='" + leaf.tag + "']"):
                parent_def = element.xpath("ancestor-or-self::define")
                if parent_def == []:
                    return None
                leaf.append(etree.Element(
                    parent_def[0].attrib["name"], rng=rng, desc=genDescPath(element)))
    return ref_tree


def expandReferTreeAll(ref_tree, include_dict):
    return expandReferTree(ref_tree, include_dict) if ref_tree == expandReferTree(ref_tree, include_dict) else expandReferTreeAll(expandReferTree(ref_tree, include_dict))

def genDescPath(child_ele):
    parent=child_ele.getparent() 
    if parent is None or parent.tag == 'define':
        return ''
    else:
        return genDescPath(parent)+'/'+parent.get('name')+'(' + parent.tag + ')' if parent.tag in ['element', 'attribute'] else genDescPath(parent)+'/' + parent.tag

def genReferTreeFromXpath(xpath, rng, schema_dir):
    define_name=etree.parse(rng).xpath(getDef(xpath))[0].get('name')
    return expandReferTreeAll(etree.ElementTree(etree.Element(define_name, rng=os.path.basename(rng))),getInclude(schema_dir))
    
def genAffectPath(refer_leaf):
    return refer_leaf.get('desc')+genAffectPath(refer_leaf.getparent()) if 'desc' in refer_leaf.attrib else refer_leaf.tag

def genAffectPathAll(refer_tree):
#    print('debug begin:')
#    for i in refer_tree.getroot().iter('*'):
#        print(etree.tostring(i, pretty_print=True, encoding='unicode'))
#    print('debug end')
    return list(map(genAffectPath ,list(filter(lambda x: x.getchildren() == [],refer_tree.getroot().iter('*')))))
'''
Convert non-namespace xpath to libvirt-rng namespace xpath
'''


def libvirtXPathConvert(xpath):
    return xpath.replace('/', '/xmlns:')


if __name__ == '__main__':
#    print(etree.tostring(expandReferTreeAll(etree.ElementTree(etree.Element("uint8", rng="basictypes.rng")),getInclude("./libvirt/docs/schemas")).getroot(), pretty_print=True, encoding='unicode'))
    i=genReferTreeFromXpath('/grammar[1]/define[82]/optional[1]', '/exports/projects/rng-diff/examples/patch/00ce10c700993e054532baca28d0c0d2b22c5571-1457623997/domaincommon.rng', '/exports/projects/rng-diff/examples/patch/00ce10c700993e054532baca28d0c0d2b22c5571-1457623997')
    print(etree.tostring(i,pretty_print=True, encoding='unicode'))
    for j in list(filter(lambda x: x.getchildren() == [],i.getroot().iter('*'))):
        print(etree.tostring(j,pretty_print=True,encoding='unicode'))
    print(genAffectPathAll(i))
    print(len(genAffectPathAll(i)))
    #tree=etree.parse("/exports/projects/rng-diff/examples/patch/0007237301586aa90f58a7cc8d7cb29a16b00470-1332203610/domaincommon.rng.new")
