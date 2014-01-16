#
#   A simple file for converting NeuroML to POVRay files
#
#   Author: Padraig Gleeson
#
#   This file has been developed as part of the neuroConstruct project
#   This work has been funded by the Medical Research Council and Wellcome Trust
#
#
 
import sys
import os
import random
from xml.dom import minidom  


# Needed for usage information
myFileName = 'NeuroML2POVRay.py'



def usageInfo():

    print "Usage: \n\n"+  \
              "      python "+myFileName+" neuromlFile [-s]\n"


def main (args):
      
    if len(args) == 1:
        usageInfo()
        exit()
        
    xmlfile = args[1]

    outFile = xmlfile.replace(".xml", ".pov").replace(".nml1", ".pov").replace(".nml", ".pov")

    out_file = open(outFile, "w")

    cells_file = out_file
    net_file = out_file
    splitOut = False

    cf = outFile.replace(".pov", "_cells.inc")
    nf = outFile.replace(".pov", "_net.inc")

    if len(args)>2:
        splitOut = True
        cells_file = open(cf, "w")
        net_file = open(nf, "w")

    print "Converting XML file: %s to %s"%(xmlfile, outFile)

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

            distalpoint = "<%f, %f, %f>, %f \n"%(x,y,z,r)

            distpoints[id] = distalpoint

            proximalpoint = ""
            if len(segment.getElementsByTagName(prefix+'proximal'))>0:
                proximal = segment.getElementsByTagName(prefix+'proximal')[0]
                proximalpoint = "<%f, %f, %f>, %f \n"%(float(proximal.getAttribute('x')),float(proximal.getAttribute('y')),float(proximal.getAttribute('z')),float(proximal.getAttribute('diameter'))/2.0)
            else:

                parent = int(segment.getAttribute('parent'))
                proximalpoint = distpoints[parent]

            shape = "cone"
            if proximalpoint == distalpoint:
                shape = "sphere"
                proximalpoint = ""


            cells_file.write("    %s {\n"%shape)
            cells_file.write("        %s"%distalpoint)
            cells_file.write("        %s"%proximalpoint)
            cells_file.write("    //%s_%s.%s\n"%('CGnRT','0', id))
            cells_file.write("    }\n")

        cells_file.write("pigment { color rgb <%f,%f,%f> }"%(random.random(),random.random(),random.random()))

        cells_file.write("}\n\n")

        '''
            <xsl:for-each select="mml:segments/mml:segment">

                <xsl:variable name="proximal">
                    <xsl:choose>
                        <xsl:when test="count(mml:proximal) &gt; 0">&lt;<xsl:value-of select="mml:proximal/@x"/>, <xsl:value-of select="mml:proximal/@y"/>, <xsl:value-of select="mml:proximal/@z"/>>, <xsl:value-of select="number(mml:proximal/@diameter) div 2"/></xsl:when>
                        <xsl:otherwise><xsl:variable name="parent"><xsl:value-of select="@parent"/></xsl:variable>
                        <xsl:for-each select="../mml:segment[@id = $parent]">&lt;<xsl:value-of select="mml:distal/@x"/>, <xsl:value-of select="mml:distal/@y"/>, <xsl:value-of select="mml:distal/@z"/>>, <xsl:value-of select="number(mml:distal/@diameter) div 2"/>
                        </xsl:for-each></xsl:otherwise>
                    </xsl:choose>
                </xsl:variable>

                <xsl:variable name="distal">&lt;<xsl:value-of select="mml:distal/@x"/>, <xsl:value-of select="mml:distal/@y"/>, <xsl:value-of select="mml:distal/@z"/>>, <xsl:value-of select="number(mml:distal/@diameter) div 2"/>
                </xsl:variable>

        <xsl:if test="count(mml:proximal) &gt; 0">
        sphere { <xsl:value-of select="$proximal"/> }
        </xsl:if>
        sphere { <xsl:value-of select="$distal"/> }
                <xsl:choose>
                    <xsl:when test="substring-before($distal, '>,') = substring-before($proximal, '>,')">// same point...</xsl:when>
                    <xsl:otherwise>
        cone {
        <xsl:value-of select="$proximal"/><xsl:text>
        </xsl:text><xsl:value-of select="$distal"/>
        }
                    </xsl:otherwise>
                </xsl:choose>

            </xsl:for-each>
        <xsl:variable name="colScale"><xsl:value-of select="position() div count(../nml:cell)"/></xsl:variable>
        pigment { color rgb &lt;<xsl:value-of select="$colScale"/>,<xsl:value-of select="$colScale"/>,0.5> }'''

    if splitOut:
        out_file.write("#include \""+cf+"\"\n\n")
        out_file.write("#include \""+nf+"\"\n\n")

    popsElement = neuroml.getElementsByTagName('populations')[0]

    popElements = popsElement.getElementsByTagName('population')

    print "There are %i populations in the file"%len(popElements)

    for pop in popElements:

        name = pop.getAttribute('name')
        celltype = pop.getAttribute('cell_type')
        instances = pop.getElementsByTagName('instance')

        info = "Population: %s has %i cells of type: %s"%(name,len(instances),celltype)
        print info

        net_file.write("/* "+info+"*/\n\n")

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
            net_file.write("    //%s_%s\n"%(name, id))
            net_file.write("}\n")


    lenX = (maxX-minX)
    lenY = (maxY-minY)
    lenZ = (maxZ-minZ)

    midX = minX + lenX
    midY = minY + lenY
    midZ = minZ + lenZ

    lookAt = "<%f,%f, %f>"%(midX,midY,midZ)
    loc = "<%f,%f, %f>"%(minX-lenX/4,maxY,minZ-lenZ/4)

    header='''
/*
POV-Ray file generated from NeuroML network
*/
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
  //Padraig coordinates:
  //location < uu(1 * sin (clock * 2 * 3.141)) , vv(0.7*sin (clock * 2 * 3.141)) , ww(2.5* cos (clock * 2 * 3.141)) >
  //look_at < uu(0.1) , vv(0.05+0.3*sin (clock * 2 * 3.141)) , ww(0.04)>
  //location < uu(1.5) , vv(1) , ww(1.5) >
  //look_at <uu(0),vv(0),ww(0)>

  //Matteo coordinates:
  location < (maxX-minX)/3 , (maxY-minY)/3 , -(maxY-minY)*1.5 >
  look_at <uu(0),vv(0),ww(0)>
}

light_source {
  <1000,2000,2000>
  color rgb <1,1,1>
}

light_source {
  <-1000,200,-2000>
  color rgb <1,1,1>
}

/*
plane {
   y, -500
   pigment {checker color rgb 1.0, color rgb 0.9 scale 20}
}*/
    \n'''%(minX,minY,minZ,maxX,maxY,maxZ)


    out_file.write(header)
    
    out_file.close()

        



if __name__ == '__main__':
    main(sys.argv)
