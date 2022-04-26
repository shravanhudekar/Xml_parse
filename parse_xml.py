from fileinput import lineno
import xml.etree.ElementTree as ET
from xml.dom import minidom

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def setElements(node,line,data):
    L = ET.SubElement(node,"lineToCover")
    L.set("lineNumber", line)
    if data == "Code range fully covered":
        L.set("covered", "true")

    elif data == "Code range partially covered":
        L.set("covered", "true")
        L.set("branchesToCover", "2")
        L.set("coveredBranches", "1")

    else:
        L.set("covered", "false")
    return node
    #end of function call


def GenXml():

    # parse an xml file by name
    file = minidom.parse('models.xml')

    # we make root element
    root = ET.Element("coverage")
    root.set("version", "1")

    #use getElementsByTagName() to get tag of modules
    models = file.getElementsByTagName('Module')

    #temp=[]
    prev = ""
    for path in models:    
        #use getElementsByTagName() to get tag of SourceFile and Line
        filename=path.getElementsByTagName('SourceFile')
        StepPoint = path.getElementsByTagName('StepPoint')
        
        for n in filename:
            #data of tag SourceFile
            p=n.firstChild.data
            fileNode = ET.Element("file")
            fileNode.set("path", p)
            
            for step in StepPoint:
                line=step.getElementsByTagName('Line')
                coverage=step.getElementsByTagName('Coverage')
                
                for c in coverage: 
                    for m in line:
                        
                        #data of tag line i.e. line no. storing in temp
                        lineno=(m.firstChild.data)

                        # check if prev & current line no. is same
                        if lineno != prev:

                            # if line tag consist of range eg: 173-256
                            if '-' in lineno:
                                #split temp extract range
                                x=lineno.split('-')
                                first=int(x[0])
                                last=int(x[1])

                                #create subelement for each line
                                for r in range(first,last+1): 
                                    fileNode=setElements(fileNode,str(r),c.firstChild.data)

                            else:   
                                fileNode=setElements(fileNode,lineno,c.firstChild.data)
                        
                        prev = lineno

        root.append(fileNode)

    tree = ET.ElementTree(root)
    indent(root)

    tree.write("IAR_Coverage.xml", encoding ='utf-8', xml_declaration = True)

GenXml()