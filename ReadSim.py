# -*- coding: utf-8 -*-
import os.path
#
#   A simple file for reading nC sims
#
#   Author: Padraig Gleeson
#
#   This file has been developed as part of the neuroConstruct project
#   This work has been funded by the Medical Research Council and Wellcome Trust
#
#

import sys
import os

maxTime = 20
skip = 5

maxV = 30
minV = -75.0

povArgs = "-D Antialias=On "

def main (args):

    ## Open the time.dat file & get time points

    time_file = open("time.dat", 'r')

    times = []

    prefix = args[1]

    for line in time_file:
        if len(line.strip()) > 0 :
            t = float(line)
            times.append(t)

    dt = times[1]-times[0]
    stepTime = (skip+1)*dt
    print "There are %i time points. Max: %f ms, dt: %f"%(len(times),times[-1], dt)

    file_names = os.listdir('.')

    populations = []

    volts = {}

    for file_name in file_names:

      if file_name.endswith('.dat') and file_name.find('_')>0:
        print "Looking at file: %s"%file_name
        cell_ref = file_name[:-4]
        pop_name = cell_ref[:cell_ref.rfind('_')]

        if populations.count(pop_name)==0 : populations.append(pop_name)

        file = open(file_name)
        
        volt = []
        t=0.0
        
        while t<=maxTime:
            line = file.readline()
            #print "line: [%s]"%line
            #print "Saving time %f"%(t)
            volt.append(getColorForVolts(float(line)))
            for i in range(skip-1):
                line = file.readline()
                t=t+dt
            t=t+dt

        volts[cell_ref] = volt


    t=0
    index = 0

    bat_file_name = "%s_pov.bat"%(prefix)
    bat_file = open(bat_file_name, 'w')

    sh_file_name = "%s_pov.sh"%(prefix)
    sh_file = open(sh_file_name, 'w')
    
    while t<=maxTime:
        print "\n----  Exporting for time: %f  ----\n"%t
        in_file = open(prefix+"_net.inc")
        out_file_name = prefix+"_net.inc"+str(index)
        out_file = open(out_file_name, 'w')
        
        for line in in_file:
            if line.strip().startswith("//"):
                ref = line.strip()[2:]
                if volts.has_key(ref):
                    vs = volts[ref]
                    out_file.write("    "+vs[index]+"//"+ref+" t= "+str(t)+"\n")
                else:
                    out_file.write("No ref: "+ref+"\n")


            else:
                out_file.write(line)
            
        in_file.close()
        out_file.close()
        print "Written file: %s for time: %f"%(out_file_name, t)
        
        in_file = open(prefix+".pov")
        out_file_name = "%s_T%i.pov"%(prefix, index)
        out_file = open(out_file_name, 'w')
        
        
        clock = 0.5 * t/maxTime

        pre = '%s_net.inc'%prefix
        pre = pre.split('/')[-1]
        post = '%s_net.inc%i'%(prefix,index)
        post = post.split('/')[-1]

        print "Swapping %s for %s"%(pre, post)

        for line in in_file:
            if line.find(pre)>=0:
                out_file.write(line.replace(pre,post))
            else:
                out_file.write(line.replace("clock", str(clock)))

        print "Written file: %s for time: %f"%(out_file_name, t)
        in_file.close()
        out_file.close()

        toEx = os.path.realpath(out_file_name)
        #print toEx

        bat_file.write("C:\\Users\\Padraig\\AppData\\Local\\Programs\\POV-Ray\\v3.7\\bin\\pvengine.exe %s /nr /exit\n"%toEx)
        sh_file.write("povray %s %s\n"%(povArgs,toEx) )

        #subprocess.call(["C:\Users\Padraig\AppData\Local\Programs\POV-Ray\v3.7\bin\pvengine.exe", toEx , "/exit"])
        #exit_code = os.waitpid(process.pid, 0)
        #output = process.communicate()[0]
        
        index=index+1
        t=t+stepTime


    print "All populations: "+str(populations)
    #print "All refs: "+str(volts.keys())
    #print volts["GranuleCells_69"]

def getColorForVolts(v):

    fract = (v - minV)/(maxV - minV)
    if fract<0: fract = 0
    if fract>1: fract = 1
    maxCol = [1,1,0]
    minCol = [0,0.6,0]
    return "pigment { color rgb <%f,%f,%f> } // %f"%(minCol[0] + fract*(maxCol[0] - minCol[0]),\
                                                     minCol[1] + fract*(maxCol[1] - minCol[1]),\
                                                     minCol[2] + fract*(maxCol[2] - minCol[2]), v)


def getRainbowColorForVolts(v):

    fract = (v - minV)/(maxV - minV)
    #maxCol = [0.6,1,1]
    #minCol = [0,1,1]
    hue = 359 - (120 * fract)
    return "pigment { color CHSL2RGB(<%f,100,50>) } // %f"%( hue , v)

if __name__ == '__main__':
    main(sys.argv)

