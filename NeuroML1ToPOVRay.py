#
#   A file for converting NeuroML files (including cells & network structure)
#   into POVRay files for 3D rendering
#
#   Author: Padraig Gleeson & Matteo Farinella
#
#   This file has been developed as part of the neuroConstruct project
#   This work has been funded by the Medical Research Council and Wellcome Trust
#
#
 
import sys
import random
from xml.dom import minidom  

import argparse

_WHITE = "<1,1,1,0.55>"
_BLACK = "<0,0,0,0.55>"
_GREY = "<0.85,0.85,0.85,0.55>"


def process_args():
    """ 
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description="A file for converting NeuroML version 1.8.1 files into POVRay files for 3D rendering")

    parser.add_argument('neuroml_file', type=str, metavar='<NeuroML file>', 
                        help='NeuroML (version 1.8.1) file to be converted to PovRay format')
                        
    parser.add_argument('-split',
                        action='store_true',
                        default=False,
                        help="If this is specified, generate separate pov files for cells & network. Default is false")


    parser.add_argument('-background', 
                        type=str,
                        metavar='<background colour>',
                        default=_WHITE,
                        help='Colour of background, e.g. <0,0,0,0.55>')

    parser.add_argument('-movie',
                        action='store_true',
                        default=False,
                        help="If this is specified, generate a ini file for generating a sequence of frames for a movie of the 3D structure")

    parser.add_argument('-frames', 
                        type=int,
                        metavar='<frames>',
                        default=36,
                        help='Number of frames in movie')
                        
    parser.add_argument('-posx', 
                        type=float,
                        metavar='<position offset x>',
                        default=0,
                        help='Offset position in x dir (0 is centre, 1 is top)')
    parser.add_argument('-posy', 
                        type=float,
                        metavar='<position offset y>',
                        default=0,
                        help='Offset position in y dir (0 is centre, 1 is top)')
    parser.add_argument('-posz', 
                        type=float,
                        metavar='<position offset z>',
                        default=0,
                        help='Offset position in z dir (0 is centre, 1 is top)')
                        
    parser.add_argument('-viewx', 
                        type=float,
                        metavar='<view offset x>',
                        default=0,
                        help='Offset viewing point in x dir (0 is centre, 1 is top)')
    parser.add_argument('-viewy', 
                        type=float,
                        metavar='<view offset y>',
                        default=0,
                        help='Offset viewing point in y dir (0 is centre, 1 is top)')
    parser.add_argument('-viewz', 
                        type=float,
                        metavar='<view offset z>',
                        default=0,
                        help='Offset viewing point in z dir (0 is centre, 1 is top)')

    parser.add_argument('-scalex', 
                        type=float,
                        metavar='<scale position x>',
                        default=1,
                        help='Scale position from network in x dir')
    parser.add_argument('-scaley', 
                        type=float,
                        metavar='<scale position y>',
                        default=1.5,
                        help='Scale position from network in y dir')
    parser.add_argument('-scalez', 
                        type=float,
                        metavar='<scale position z>',
                        default=1,
                        help='Scale position from network in z dir')

    parser.add_argument('-plane',
                        action='store_true',
                        default=False,
                        help="If this is specified, add a 2D plane below cell/network")
    
    return parser.parse_args()

def main (argv):

    args = process_args()
        
    xmlfile = args.neuroml_file

    pov_file_name = xmlfile.replace(".xml", ".pov").replace(".nml1", ".pov").replace(".nml", ".pov")

    pov_file = open(pov_file_name, "w")


    header='''
/*
POV-Ray file generated from NeuroML network
*/
#version 3.6;

#include "colors.inc"

background {rgbt %s}

light_source {
  <500,200,500>
  color rgb <1,1,1>
}

light_source {
  <-500,-200,500>
  color rgb <1,1,1>
}
light_source {
  <500,-200,-500>
  color rgb <1,1,1>
}
light_source {
  <-500,-200,-500>
  color rgb <1,1,1>
}


    \n''' ###    end of header


    pov_file.write(header%(args.background))

    cells_file = pov_file
    net_file = pov_file
    splitOut = False

    cf = pov_file_name.replace(".pov", "_cells.inc")
    nf = pov_file_name.replace(".pov", "_net.inc")

    if args.split:
        splitOut = True
        cells_file = open(cf, "w")
        net_file = open(nf, "w")
        print "Saving into %s and %s and %s"%(pov_file_name, cf, nf)

    print "Converting XML file: %s to %s"%(xmlfile, pov_file_name)

    xmldoc = minidom.parse(xmlfile)

    
    neuroml = xmldoc.getElementsByTagName('neuroml')[0]

    cellsElement = neuroml.getElementsByTagName('cells')[0]
    
    cellElements = cellsElement.getElementsByTagName('cell')

    minXc = 1e9
    minYc = 1e9
    minZc = 1e9
    maxXc = -1e9
    maxYc = -1e9
    maxZc = -1e9

    minX = 1e9
    minY = 1e9
    minZ = 1e9
    maxX = -1e9
    maxY = -1e9
    maxZ = -1e9

    declaredcells = {}

    print "There are %i cells in the file"%len(cellElements)

    for cell in cellElements:
        #print dir(cell)
        cellName = cell.getAttribute('name')
        print "Handling cell: %s"%cellName

        
        declaredcell = "cell_"+cellName

        declaredcells[cellName] = declaredcell

        cells_file.write("#declare %s = \n"%declaredcell)
        cells_file.write("union {\n")

        prefix = ""
        if len(cell.getElementsByTagName('mml:segments')) > 0:
            prefix="mml:"

        segments = cell.getElementsByTagName(prefix+'segments')[0]

        distpoints = {}

        for segment in segments.getElementsByTagName(prefix+'segment'):

            id = int(segment.getAttribute('id'))

            distal = segment.getElementsByTagName(prefix+'distal')[0]

            x = float(distal.getAttribute('x'))
            y = float(distal.getAttribute('y'))
            z = float(distal.getAttribute('z'))
            r = float(distal.getAttribute('diameter'))/2.0

            if x<minXc: minXc=x
            if y<minYc: minYc=y
            if z<minZc: minZc=z

            if x>maxXc: maxXc=x
            if y>maxYc: maxYc=y
            if z>maxZc: maxZc=z

            distalpoint = "<%f, %f, %f>, %f "%(x,y,z,r)

            distpoints[id] = distalpoint

            proximalpoint = ""
            if len(segment.getElementsByTagName(prefix+'proximal'))>0:
                proximal = segment.getElementsByTagName(prefix+'proximal')[0]
                proximalpoint = "<%f, %f, %f>, %f "%(float(proximal.getAttribute('x')),float(proximal.getAttribute('y')),float(proximal.getAttribute('z')),float(proximal.getAttribute('diameter'))/2.0)
            else:

                parent = int(segment.getAttribute('parent'))
                proximalpoint = distpoints[parent]

            shape = "cone"
            if proximalpoint == distalpoint:
                shape = "sphere"
                proximalpoint = ""


            cells_file.write("    %s {\n"%shape)
            cells_file.write("        %s\n"%distalpoint)
            if len(proximalpoint): cells_file.write("        %s\n"%proximalpoint)

            cells_file.write("        //%s_%s.%s\n"%('CELL_GROUP_NAME','0', id))
            cells_file.write("    }\n")

        cells_file.write("    pigment { color rgb <%f,%f,%f> }\n"%(random.random(),random.random(),random.random()))

        cells_file.write("}\n\n")


    if splitOut:
        pov_file.write("#include \""+cf+"\"\n\n")
        pov_file.write("#include \""+nf+"\"\n\n")

    popsElement = neuroml.getElementsByTagName('populations')[0]

    popElements = popsElement.getElementsByTagName('population')

    print "There are %i populations in the file"%len(popElements)

    for pop in popElements:

        name = pop.getAttribute('name')
        celltype = pop.getAttribute('cell_type')
        instances = pop.getElementsByTagName('instance')

        info = "Population: %s has %i cells of type: %s"%(name,len(instances),celltype)
        print info

        colour = "1"
        if len(pop.getElementsByTagName('meta:properties')) > 0:
            props = pop.getElementsByTagName('meta:properties')
            if len(props[0].getElementsByTagName('meta:property')) > 0:

                for prop in props[0].getElementsByTagName('meta:property'):

                    if len(prop.getElementsByTagName('meta:tag'))>0 and prop.getElementsByTagName('meta:tag')[0].childNodes[0].data == 'color':
                        #print prop.getElementsByTagName('meta:tag')[0].childNodes
                        colour = prop.getElementsByTagName('meta:value')[0].childNodes[0].data
                        colour = colour.replace(" ", ",")
                    elif prop.hasAttribute('tag') and prop.getAttribute('tag') == 'color':
                        colour = prop.getAttribute('value')
                        colour = colour.replace(" ", ",")
                    print "Colour determined to be: "+colour


        net_file.write("\n\n/* "+info+" */\n\n")

        for instance in instances:

            location = instance.getElementsByTagName('location')[0]
            id = instance.getAttribute('id')
            net_file.write("object {\n")
            net_file.write("    %s\n"%declaredcells[celltype])
            x = float(location.getAttribute('x'))
            y = float(location.getAttribute('y'))
            z = float(location.getAttribute('z'))

            if x+minXc<minX: minX=x+minXc
            if y+minYc<minY: minY=y+minYc
            if z+minZc<minZ: minZ=z+minZc

            if x+maxXc>maxX: maxX=x+maxXc
            if y+maxYc>maxY: maxY=y+maxYc
            if z+maxZc>maxZ: maxZ=z+maxZc

            net_file.write("    translate <%s, %s, %s>\n"%(x,y,z))

            if colour == '1':
                colour = "%f,%f,%f"%(random.random(),random.random(),random.random())

            if colour is not None:
                net_file.write("    pigment { color rgb <%s> }"%(colour))

            net_file.write("\n    //%s_%s\n"%(name, id)) 

            net_file.write("}\n")


    plane = '''
plane {
   y, vv(-1)
   pigment {checker color rgb 1.0, color rgb 0.8 scale 20}
}
'''

    footer='''

#declare minX = %f;
#declare minY = %f;
#declare minZ = %f;

#declare maxX = %f;
#declare maxY = %f;
#declare maxZ = %f;

#macro uu(xx)
    0.5 * (maxX *(1+xx) + minX*(1-xx))
#end

#macro vv(xx)
    0.5 * (maxY *(1+xx) + minY*(1-xx))
#end

#macro ww(xx)
    0.5 * (maxZ *(1+xx) + minZ*(1-xx))
#end

// Trying to view box
camera {
  location < uu(%s + %s * sin (clock * 2 * 3.141)) , vv(%s + %s * sin (clock * 2 * 3.141)) , ww(%s + %s * cos (clock * 2 * 3.141)) >
  look_at < uu(%s + 0) , vv(%s + 0.05+0.3*sin (clock * 2 * 3.141)) , ww(%s + 0)>
}

%s
    \n'''%(minX,minY,minZ,maxX,maxY,maxZ, args.posx, args.scalex, args.posy, args.scaley, args.posz, args.scalez, args.viewx, args.viewy, args.viewz, (plane if args.plane else "")) ###    end of footer


    pov_file.write(footer)

    pov_file.close()

    if args.movie:
        ini_file_name = pov_file_name.replace(".pov", "_movie.ini")
    
        ini_movie = '''
Antialias=On

+W800 +H600 
        
Antialias_Threshold=0.3
Antialias_Depth=4

Input_File_Name=%s

Initial_Frame=1
Final_Frame=%i
Initial_Clock=0
Final_Clock=1

Cyclic_Animation=on
Pause_when_Done=off
        
        '''
        ini_file = open(ini_file_name, 'w')
        ini_file.write(ini_movie%(pov_file_name, args.frames))
        ini_file.close()
        
        print("Created file for generating %i movie frames at: %s"%(args.frames,ini_file_name))


if __name__ == '__main__':
    main(sys.argv)

