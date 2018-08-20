import sys
import os
import cv2
import numpy as np
import math
import random

def captureSubimage(image, x, y, length, height, prefix, index, location):
    for blankX in range(0, length):
        for blankY in range(0, height):
            blankImage[blankY,blankX] = image[y-math.floor(height/2)+blankY, x-math.floor(length/2)+blankX]
    cv2.imwrite("./"+prefix+str(length)+"x"+str(height)+"/"+location+"/image"+str(index)+".png", blankImage)
    f = open("./"+prefix+str(length)+"x"+str(height)+"/log.txt", "a")
    f.write(location +" "+str(index)+" recorded from pixel " + str(x-length) +","+ str(y-height) +"\n")
def main():
    #scan for help parameter
    help = False;
    for x in sys.argv:
        if x == "--help" or x == "-h":
            help = True
    if help or len(sys.argv) == 1:
        print("python splitImage.py sourceImage referenceImage length height")
        sys.exit()

    #define length and width of the sub images
    length = int(sys.argv[3])
    width = int(sys.argv[4])
    global blankImage
    blankImage = np.zeros((length, width, 3), np.uint8)
    #make a directory to hold the subimages.
    prefix=sys.argv[1][sys.argv[1].rfind("/")+1:sys.argv[1].rfind('.')]
    if os.path.isdir("./"+prefix+str(length)+"x"+str(width)):
        print("directory exists. some files may be overwritten.")
    else:
        os.mkdir("./"+prefix+str(length)+"x"+str(width))

    if os.path.isdir("./"+prefix+str(length)+"x"+str(width)+"/error") == False:
        os.mkdir("./"+prefix+str(length)+"x"+str(width)+"/error")
    if os.path.isdir("./"+prefix+str(length)+"x"+str(width)+"/vein") == False:
        os.mkdir("./"+prefix+str(length)+"x"+str(width)+"/vein")
    #read the image. gif need to be read as a video then converted to an image
    if ".gif" not in sys.argv[1]:
        sourceImage = cv2.imread(sys.argv[1])
    else:
        ret, sourceImage = cv2.VideoCapture(sys.argv[1]).read()

    if ".gif" not in sys.argv[2]:
        referenceImage = cv2.imread(sys.argv[2])
    else:
        ret, referenceImage = cv2.VideoCapture(sys.argv[2]).read()

    cv2.imwrite("./"+prefix+str(length)+"x"+str(width)+"/originalimage.png", sourceImage)
    cv2.imwrite("./"+prefix+str(length)+"x"+str(width)+"/referenceimage.png", referenceImage)
    #iterate over every pixel and make a subimage from white ones
    imageWidth, imageLength, channels = sourceImage.shape
    sourceImage = cv2.copyMakeBorder(sourceImage, width, width, length, length, cv2.BORDER_CONSTANT, (0,0,0))
    referenceImage = cv2.copyMakeBorder(referenceImage, width, width, length, length, cv2.BORDER_CONSTANT, (0,0,0))
    subImageNumberVein = 0
    subImageNumberError = 0
    for x in range(length,imageLength+length):
        for y in range(width, imageWidth+width):
            #capture white pixels
            if min(referenceImage[y,x]) == 255:
                captureSubimage(sourceImage, x, y, length, width, prefix, subImageNumberVein, "vein")
                subImageNumberVein = subImageNumberVein+1
            else:
                rand = random.randint(1,11)
                if rand == 5:
                    captureSubimage(sourceImage, x, y, length, width, prefix, subImageNumberError, "error")
                    subImageNumberError = subImageNumberError+1


main()
