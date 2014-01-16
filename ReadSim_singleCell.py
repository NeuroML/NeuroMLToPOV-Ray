# -*- coding: utf-8 -*-
import os.path
import shutil
#
#   A simple file for reading nC sims
#
#   Author: Matteo Farinella
#   (based on ReadSim.py by Padraig Gleeson)
#
#   This file has been developed as part of the neuroConstruct project
#   This work has been funded by the Medical Research Council and Wellcome Trust
#
#

import sys
import os

maxTime = 100
skip = 50

dirname="./"
'''
#find a name and create a new folder for the movie data
dirname = "movie"
index = 0
while os.path.isdir(dirname):
   index = index + 1
   dirname = "movie_"+str(index)
os.mkdir(dirname)
'''

def main (args):

    ## Open the time.dat file & get time points

    time_file = open("time.dat", 'r')

    times = []

    prefix = args[1]
    
    #copy in the new directory the files created by NeuroML2PovRay converter
    ####shutil.copy(prefix+"_cells.inc", dirname) 
    ####shutil.copy(prefix+"_net.inc", dirname) 

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
        cell_ref = file_name[:-4]
        pop_name = cell_ref[:cell_ref.rfind('_')]

        if populations.count(pop_name)==0 : populations.append(pop_name)

        file = open(file_name)
        
        volt = []
        t=0.0
        
        while t<=maxTime:
            line = file.readline()
            #print "Saving time %f"%(t)
            volt.append(getColorForVolts(float(line)))
            for i in range(skip-1):
                line = file.readline()
                t=t+dt
            t=t+dt

        volts[cell_ref] = volt

    t=0
    index = 0
    
    #give the single frames an alphabetical order
    maxind = "00000"
    ind = "00000"

    bat_file_name = dirname+"/"+"%s_pov.bat"%(prefix)
    bat_file = open(bat_file_name, 'w')

    sh_file_name = dirname+"/"+"%s_pov.sh"%(prefix)
    sh_file = open(sh_file_name, 'w')
    
    #modifying cells file instead of net file (main difference from ReadSim.py)
    while t<=maxTime:

        ind = maxind[0:len(maxind)-len(str(index))] #compute index indentation

        print "\n----  Exporting for time: %f  ----\n"%t
        in_file = open(prefix+"_cells.inc")
        out_file_name = dirname+"/"+prefix+"_cells.inc"+ind+str(index)
        out_file = open(out_file_name, 'w')
        
        for line in in_file:
            if line.strip().startswith("//"):
                ref = line.strip()[2:]
                if volts.has_key(ref):
                    vs = volts[ref]
                    out_file.write("    "+vs[index]+"//"+ref+" t= "+ind+str(t)+"\n")
                else:
                    out_file.write("//No ref: "+ref+"\n")


            else:
                out_file.write(line)
            
        in_file.close()
        out_file.close()
        print "Written file: %s for time: %f"%(out_file_name, t)
        
        in_file = open(prefix+".pov")
        out_file_name = dirname+"/%s_T%s%i.pov"%(prefix, ind, index)
        out_file = open(out_file_name, 'w')
        

        for line in in_file:
            pre = '%s_cells.inc'%prefix
            post = '%s_cells.inc%s%i'%(prefix, ind, index)
            if line.find(pre)>=0:
                out_file.write(line.replace(pre,post))
            else:
                clock = 0.1 * t/maxTime
                out_file.write(line.replace("clock", str(clock)))

        print "Written file: %s for time: %f"%(out_file_name, t)
        in_file.close()
        out_file.close()

        toEx = os.path.realpath(out_file_name)
        #print toEx

        bat_file.write("C:\\Users\\Padraig\\AppData\\Local\\Programs\\POV-Ray\\v3.7\\bin\\pvengine.exe %s /nr /exit\n"%toEx)
        sh_file.write("povray %s\n"%toEx)

        #subprocess.call(["C:\Users\Padraig\AppData\Local\Programs\POV-Ray\v3.7\bin\pvengine.exe", toEx , "/exit"])
        #exit_code = os.waitpid(process.pid, 0)
        #output = process.communicate()[0]
        
        index=index+1
        t=t+stepTime


    print "All populations: "+str(populations)
    #print "All refs: "+str(volts.keys())
    #print volts["GranuleCells_69"]

    #print volts.keys() #to see if the colors are actually changing

def getColorForVolts(v):
    maxV = 40.0
    minV = -80.0

    fract = (v - minV)/(maxV - minV)
    maxCol = [1,1,0]
    minCol = [0,0.2,0]
    return "pigment { color rgb <%f,%f,%f> } // %f"%(minCol[0] + fract*(maxCol[0] - minCol[0]),\
                                                     minCol[1] + fract*(maxCol[1] - minCol[1]),\
                                                     minCol[2] + fract*(maxCol[2] - minCol[2]), v)

if __name__ == '__main__':
    main(sys.argv)

