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


width = 800
height = 600
scale_font = 1

font = cv2.FONT_HERSHEY_PLAIN
font_colour = (255,255,255)


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
                        
    parser.add_argument('-left', 
                        type=str, 
                        metavar='<left info>', 
                        default='',
                        help='Text on left')
                        
    parser.add_argument('-frames', 
                        type=int,
                        metavar='<frames>',
                        default=100,
                        help='Number of frames')
                        
    parser.add_argument('-name', 
                        type=str, 
                        metavar='<Movie name>', 
                        default='output',
                        help='Movie name')
                        
    return parser.parse_args()


def generate_volt_scale(img, x, y, height, width, num):
    for i in range(num):
        ww = int(float(width)/num)
        xx = int(x + i * ww)
        fract = 1 - (float(i)/num + .5/num)
        hue = (270 * (1-fract))/360
        rgb = colorsys.hls_to_rgb(hue, 0.5, 1)
        rgb = tuple([int(256*rr) for rr in rgb])
        c1 = (xx,y)
        c2 = (xx+ww,y+height)
        #print "Fract: %f - hue: %f - RGB: %s - %s - %s"%(fract, hue, rgb, c1, c2)
        cv2.rectangle(img,c1,c2,rgb,3)
        
    

    
def main (argv):
    
    args = process_args()
    
    print("Making a movie....")
    
    img_files_pre = []
    img_files_post = []

    gen_images = True
    gen_movie = False
    
    #gen_images = False
    gen_movie = True
    
    pref = args.prefix+'_T00' 

    if gen_images:

        for i in range(args.frames+1):
            index = str(i)
            while len(index)<3: index="0"+index
            img_files_pre.append("%s%s.png"%(pref,index))
            

        for i in range(len(img_files_pre)):
            img_file = img_files_pre[i]
            img = cv2.imread(img_file)
            print("Read in file: %s"%img_file)
            show = False
            if show:
                cv2.imshow('Image: '+img_file,img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            t = args.startTime + i*float(args.endTime-args.startTime)/args.frames
            
            cv2.putText(img,'Time: %.3f ms'%t,(width-150,50), font, 1,font_colour,scale_font)
            cv2.putText(img,'%imV  :  %imV'%(args.minV, args.maxV),(100,50), font, 1,font_colour,scale_font)

            cv2.putText(img,args.title,(150,height-50), font, 1,font_colour,scale_font)
            cv2.putText(img,args.left,(15,height/2), font, 1,font_colour,scale_font)

            generate_volt_scale(img, 100, 65, 12, 150, 70)
            new_file = args.name+'_'+img_file
            cv2.imwrite(new_file,img)
            print("Written %s"%new_file)



    if gen_movie:

        for i in range(args.frames+1):
            index = str(i)
            while len(index)<3: index="0"+index
            img_files_post.append("%s_%s%s.png"%(args.name,pref,index))

        imgs = []

        for i in range(len(img_files_post)):
            img_file = img_files_post[i]
            img = cv2.imread(img_file)
            print("Read in %s"%img_file)
            imgs.append(img)

        format = 'avi'
        #format = 'mpg'
        format = 'divx'

        fps = 24
        if format is 'avi':
            fourcc = cv.CV_FOURCC('X','V','I','D')
            mov_file = args.name+'.avi'
            out = cv2.VideoWriter(mov_file,fourcc, fps, (width,height))
        if format is 'divx':
            fourcc = cv.CV_FOURCC('D','I','V','X')
            mov_file = args.name+'.avi'
            out = cv2.VideoWriter(mov_file,fourcc, fps, (width,height))
        if format is 'mpg':
            fourcc = cv.CV_FOURCC('M','J','P','G')
            mov_file = args.name+'.mpg'
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


