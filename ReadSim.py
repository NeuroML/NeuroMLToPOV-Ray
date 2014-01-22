# -*- coding: utf-8 -*-
import os.path
#
#   A simple file for reading nC sims
#
#   Author: Padraig Gleeson & Matteo Farinella
#
#   This file has been developed as part of the neuroConstruct project
#   This work has been funded by the Medical Research Council and Wellcome Trust
#
#

import sys
import os
import argparse


povArgs = "-D Antialias=On Antialias_Threshold=0.3 Antialias_Depth=4"

def process_args():
    """ 
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description="A file for overlaying POVRay files generated from NeuroML by NeuroML2POVRay.py with cell activity (e.g. as generated from a neuroConstruct simulation)")

    parser.add_argument('prefix', type=str, metavar='<network prefix>', 
                        help='Prefix for files in PovRay, e.g. use PREFIX is files are PREFIX.pov, PREFIX_net.inc, etc.')
                        

    parser.add_argument('-maxV', 
                        type=float,
                        metavar='<maxV>',
                        default=50.0,
                        help='Max voltage for colour scale in mV')

    parser.add_argument('-minV', 
                        type=float,
                        metavar='<minV>',
                        default=-90.0,
                        help='Min voltage for colour scale in mV')

    parser.add_argument('-maxTime', 
                        type=float,
                        metavar='<maxTime>',
                        default=100,
                        help='Max time to display until in ms')

    parser.add_argument('-rotations', 
                        type=float,
                        metavar='<rotations>',
                        default=0.5,
                        help='Number of rotations to complete in movie')

    parser.add_argument('-skip', 
                        type=int,
                        metavar='<skip>',
                        default=50,
                        help='Number of time points to skip before generating the next frame')

    parser.add_argument('-singlecell',
                        action='store_true',
                        default=False,
                        help="If this is specified, visualise activity in a single cell, with dat files for each segment")

    parser.add_argument('-rainbow',
                        action='store_true',
                        default=False,
                        help="If this is specified, use a rainbow based colouring of the cell activity (still in development...)")

    return parser.parse_args()

def main (argv):

    args = process_args()

    ## Open the time.dat file & get time points

    time_file = open("time.dat", 'r')

    times = []

    for line in time_file:
        if len(line.strip()) > 0 :
            t = float(line)
            times.append(t)

    dt = times[1]-times[0]
    stepTime = (args.skip+1)*dt
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
        
        while t<=args.maxTime:
            line = file.readline()
            #print "line: [%s]"%line
            #print "Saving time %f"%(t)
            colour = getRainbowColorForVolts(float(line), args) if args.rainbow else getColorForVolts(float(line), args)
            volt.append(colour)
            for i in range(args.skip-1):
                line = file.readline()
                t=t+dt
            t=t+dt

        volts[cell_ref] = volt
        print "Saved data for cell ref %s"%cell_ref


    t=0
    index = 0

    #give the single frames an alphabetical order
    maxind = "00000"
    ind = "00000"

    bat_file_name = "%s_pov.bat"%(args.prefix)
    bat_file = open(bat_file_name, 'w')

    sh_file_name = "%s_pov.sh"%(args.prefix)
    sh_file = open(sh_file_name, 'w')
    
    while t<=args.maxTime:
        print "\n----  Exporting for time: %f  ----\n"%t

        if not args.singlecell:

            in_file = open(args.prefix+"_net.inc")
            out_file_name = args.prefix+"_net.inc"+str(index)
            out_file = open(out_file_name, 'w')

            for line in in_file:
                if line.strip().startswith("//"):
                    ref = line.strip()[2:]
                    if volts.has_key(ref):
                        vs = volts[ref]
                        out_file.write("         "+vs[index]+"//"+ref+" t= "+str(t)+"\n")
                    else:
                        out_file.write("No ref: "+ref+"\n")


                else:
                    out_file.write(line)

            in_file.close()
            out_file.close()
            print "Written file: %s for time: %f"%(out_file_name, t)

            in_file = open(args.prefix+".pov")
            out_file_name = "%s_T%i.pov"%(args.prefix, index)
            out_file = open(out_file_name, 'w')

            clock = args.rotations * t/args.maxTime

            pre = '%s_net.inc'%args.prefix
            pre = pre.split('/')[-1]
            post = '%s_net.inc%i'%(args.prefix,index)
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

            bat_file.write("C:\\Users\\Padraig\\AppData\\Local\\Programs\\POV-Ray\\v3.7\\bin\\pvengine.exe %s /nr /exit\n"%toEx)
            sh_file.write("povray %s %s\n"%(povArgs,toEx) )

        else:

            ind = maxind[0:len(maxind)-len(str(index))] #compute index indentation

            in_file = open(args.prefix+"_cells.inc")
            out_file_name = args.prefix+"_cells.inc"+ind+str(index)
            out_file = open(out_file_name, 'w')

            for line in in_file:
                if line.strip().startswith("//"):
                    ref = line.strip()[2:]
                    if volts.has_key(ref):
                        vs = volts[ref]
                        out_file.write("         "+vs[index]+"//"+ref+" t= "+ind+str(t)+"\n")
                    else:
                        out_file.write("//No ref: "+ref+"\n")


                else:
                    out_file.write(line)

            in_file.close()
            out_file.close()
            print "Written file: %s for time: %f"%(out_file_name, t)

            in_file = open(args.prefix+".pov")
            out_file_name = "%s_T%s%i.pov"%(args.prefix, ind, index)
            out_file = open(out_file_name, 'w')


            for line in in_file:
                pre = '%s_cells.inc'%args.prefix
                post = '%s_cells.inc%s%i'%(args.prefix, ind, index)
                if line.find(pre)>=0:
                    out_file.write(line.replace(pre,post))
                else:
                    clock = args.rotations * t/args.maxTime
                    out_file.write(line.replace("clock", str(clock)))

            print "Written file: %s for time: %f"%(out_file_name, t)
            in_file.close()
            out_file.close()

            toEx = os.path.realpath(out_file_name)

            bat_file.write("C:\\Users\\Padraig\\AppData\\Local\\Programs\\POV-Ray\\v3.7\\bin\\pvengine.exe %s /nr /exit\n"%toEx)
            sh_file.write("povray %s %s\n"%(povArgs,toEx) )

        index=index+1
        t=t+stepTime


    print "All populations: "+str(populations)

def getColorForVolts(v, args):

    fract = (v - args.minV)/(args.maxV - args.minV)
    if fract<0: fract = 0
    if fract>1: fract = 1
    maxCol = [1,1,0]
    minCol = [0,0.3,0]
    return "pigment { color rgb <%f,%f,%f> } // v = %f"%(minCol[0] + fract*(maxCol[0] - minCol[0]),\
                                                     minCol[1] + fract*(maxCol[1] - minCol[1]),\
                                                     minCol[2] + fract*(maxCol[2] - minCol[2]), v)


def getRainbowColorForVolts(v, args):

    fract = (v - args.minV)/(args.maxV - args.minV)
    if fract<0: fract = 0.0
    if fract>1: fract = 1.0
    #maxCol = [0.6,1,1]
    #minCol = [0,1,1]
    hue = 359 - (120 * (1.0-fract))
    return "pigment { color CHSL2RGB(<%f,1,0.5>) } // v = %f, fract = %f"%( hue , v, fract)

if __name__ == '__main__':
    main(sys.argv)

