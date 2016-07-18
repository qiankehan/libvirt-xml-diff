#!/usr/bin/python3
from lxml import etree
import os
os.chdir("./libvirt/docs/schemas/")
def parse_include(tree):
    rng_tree=tree
    if rng_tree.xpath('//ns:include', namespaces={'ns':'http://relaxng.org/ns/structure/1.0'}) == []:
        return rng_tree
    for include in rng_tree.xpath('//ns:include', namespaces={'ns':'http://relaxng.org/ns/structure/1.0'}):
        included_children=etree.parse(include.attrib['href']).getroot().getchildren()
        rng_tree.getroot().remove(rng_tree.find('ns:include', namespaces={'ns':'http://relaxng.org/ns/structure/1.0'}))
        for child in included_children:
            if child.tag != '{http://relaxng.org/ns/structure/1.0}' + 'start':
                rng_tree.getroot().append(child)
    return parse_include(rng_tree)

if __name__=='__main__':
    tree=etree.parse("/exports/projects/rng-diff/examples/patch/0007237301586aa90f58a7cc8d7cb29a16b00470-1332203610/domaincommon.rng.new")
    for j in tree.xpath("//define//ref"):
        print(tree.getpath(j.xpath('ancestor::define')[0]))
        print(tree.getpath(j))
#print(tree.xpath('ns:define', namespaces={'ns':'http://relaxng.org/ns/structure/1.0'}))

#map(lambda x: print(etree._ElementTree.getpath(x)), tree.findall('//ns:element', namespaces={'ns':'http://relaxng.org/ns/structure/1.0'}))
#for ele in tree.findall('.//ns:define', namespaces={'ns':'http://relaxng.org/ns/structure/1.0'}):
#    print(tree.xpath("/{http://relaxng.org/ns/structure/1.0}grammar/{http://relaxng.org/ns/structure/1.0}define[1]")
