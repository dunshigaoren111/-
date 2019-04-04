from xml.dom.minidom import parse
import xml.dom.minidom
import json

TMX="./TMX/"
textdata="./textdata/"

def parseXml(xmlfile,gwfile,xhfile):
    gw_file=open(gwfile,'a',encoding='utf-8')
    xh_file = open(xhfile, 'a', encoding='utf-8')
    DOMTree = parse(xmlfile)
    tmx = DOMTree.documentElement
    body=tmx.getElementsByTagName("body")[0]
    tus=body.getElementsByTagName("tu")

    for tu in tus:
        tuvs=tu.getElementsByTagName("tuv")
        seg_gw=tuvs[0].getElementsByTagName("seg")[0]
        gw =seg_gw.childNodes[0].data.strip("\t\n")
        spli_gw=split_sen(gw)
        gw_file.write(spli_gw+'\n')
        seg_xh = tuvs[1].getElementsByTagName("seg")[0]
        xh = seg_xh.childNodes[0].data.strip("\t\n")
        spli_xh = split_sen(xh)
        xh_file.write(spli_xh + '\n')

    gw_file.close()
    xh_file.close()


def split_sen(string):
    spl_sen=''
    for i in range(len(string)):
        if(string[i]!=' 'and string[i]!='\n' and i!=len(string)-1):
            spl_sen+=string[i]+' '
        else:
            spl_sen += string[i]
    return spl_sen

def tmxTotext():
    gwfile = textdata +"train.txt.gw"
    xhfile = textdata + "train.txt.xh"
    for i in range(83):
        xmlfile=TMX+str(i)+".tmx"
        parseXml(xmlfile, gwfile, xhfile)
# tmxTotext()