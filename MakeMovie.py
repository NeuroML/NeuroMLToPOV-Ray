import cv2
import cv
import colorsys
'''

            STILL IN DEVELOPMENT

            NOT YET A GENERAL PURPOSE SCRIPT!!!
            
            NEEDS MORE WORK...

'''

import argparse
import sys
import os

frames = 476
frames = 72

width = 1600
height = 1200



def process_args():
    """ 
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description="A file for overlaying POVRay files generated from NeuroML by NeuroML2POVRay.py with cell activity (e.g. as generated from a neuroConstruct simulation)")

    parser.add_argument('prefix', 
                        type=str, 
                        metavar='<network prefix>', 
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

    parser.add_argument('-startTime', 
                        type=float,
                        metavar='<startTime>',
                        default=0,
                        help='Time in ms at which to start overlaying the simulation activity')
                        
    parser.add_argument('-endTime', 
                        type=float,
                        metavar='<endTime>',
                        default=100,
                        help='End time of simulation activity in ms')
                        
    parser.add_argument('-title', 
                        type=str, 
                        metavar='<title>', 
                        default='Movie generated from neuroConstruct simulation',
                        help='Title for movie')
                        
    return parser.parse_args()


def generate_volt_scale(img, x, y, height, width, num):
    for i in range(num):
        ww = int(float(width)/num)
        xx = int(x + i * ww)
        fract = 1 - (float(i)/num + .5/num)
        hue = (270 * (1-fract))/350
        rgb = colorsys.hls_to_rgb(hue, 0.5, 1)
        rgb = tuple([int(255*rr) for rr in rgb])
        c1 = (xx,y)
        c2 = (xx+ww,y+height)
        #print "%f - %f - %s - %s - %s"%(fract, hue, rgb, c1, c2)
        cv2.rectangle(img,c1,c2,rgb,4)
        
    

    
def main (argv):
    
    args = process_args()
    
    print("Making a movie....")
    
    img_files = []

    gen_images = False
    gen_movie = True
    
    pref = args.prefix+'_T00' 

    if gen_images:
        

        for i in range(frames+1):
            index = str(i)
            while len(index)<3: index="0"+index
            img_files.append("%s%s.png"%(pref,index))

        for i in range(len(img_files)):
            img_file = img_files[i]
            img = cv2.imread(img_file)
            print("Read in %s"%img_file)
            show = False
            if show:
                cv2.imshow('Image: '+img_file,img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            font = cv2.FONT_HERSHEY_PLAIN
            t = args.startTime + i*float(args.endTime-args.startTime)/frames
            font_colour = (255,255,255)
            cv2.putText(img,'Time: %.3f ms'%t,(width-300,100), font, 2,font_colour,2)
            cv2.putText(img,'%imV  :  %imV'%(args.minV, args.maxV),(300,100), font, 2,font_colour,2)

            cv2.putText(img,args.title,(300,height-100), font, 2,font_colour,2)

            generate_volt_scale(img, 300, 130, 25, 300, 70)
            new_file = 'm_'+img_file
            cv2.imwrite(new_file,img)
            print("Written %s"%new_file)

            img_files = []


    if gen_movie:

        for i in range(frames+1):
            index = str(i)
            while len(index)<3: index="0"+index
            img_files.append("m_%s%s.png"%(pref,index))

        imgs = []

        for i in range(len(img_files)):
            img_file = img_files[i]
            img = cv2.imread(img_file)
            print("Read in %s"%img_file)
            imgs.append(img)

        format = 'avi'
        #format = 'mpg'
        format = 'divx'

        fps = 24
        if format is 'avi':
            fourcc = cv.CV_FOURCC('X','V','I','D')
            mov_file = 'output.avi'
            out = cv2.VideoWriter(mov_file,fourcc, fps, (width,height))
        if format is 'divx':
            fourcc = cv.CV_FOURCC('D','I','V','X')
            mov_file = 'output.avi'
            out = cv2.VideoWriter(mov_file,fourcc, fps, (width,height))
        if format is 'mpg':
            fourcc = cv.CV_FOURCC('M','J','P','G')
            mov_file = 'output.mpg'
            out = cv2.VideoWriter(mov_file,fourcc, fps, (width,height))

        f = 0
        for img in imgs:
            print("Writing frame %i"%f)
            f+=1
            out.write(img)

        out.release()
        print("Saved movie file %s"%mov_file)


    print "Done!"



if __name__ == '__main__':
    main(sys.argv)


