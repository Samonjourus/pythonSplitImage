import sys
import os
import cv2
import numpy as np
import math

def processSubregion(src, xMin, xMax, yMin, yMax, overfill):
    if overfill:
        print("handle overfill")
        return
    subSource = src[yMin:yMax,xMin:xMax]
    subReference = referenceImage[yMin:yMax,xMin:xMax]
    #print("w=",yMax-yMin,"l=",xMax-xMin)
    if checkCenterPixel(yMax-yMin, xMax-xMin, subReference):
        print("ok2")
        cv2.imwrite("./"+prefix+"/image"+str(index)+"-1"+".png", subSource)
        cv2.imwrite("./"+prefix+"/image"+str(index)+"-2"+".png", subReference)
    #scv2.imshow("test", test)
    #scv2.waitKey(0)
    #scv2.destroyAllWindows()

def checkCenterPixel(subYHeight, subXLength, refImage):
    #cv2.imshow("ref", refImage)
    #cv2.waitKey(10)
    height3, width3, unused = refImage.shape
    if height3 == 0 or width3 == 0:
        return False
    #print("ymid=",math.floor(height3/2),"xMid=",math.floor(width3/2))
    #print(height3, width3)
    if min(refImage[math.floor(height3/2),math.floor(width3/2)]) == 255:
        print("ok")
        return True
    return False;

help = False;
for x in sys.argv:
    if x == "--help" or x == "-h":
        help = True
if help or len(sys.argv) == 1:
    print("python splitImage.py sourceImage referenceImage length width")
    sys.exit()

#get step image dimensions
samplex = int(sys.argv[3])
sampley = int (sys.argv[4])

prefix=sys.argv[1][sys.argv[1].rfind("/")+1:sys.argv[1].rfind('.')]
print(prefix + "= prefix");
os.mkdir("./"+prefix)
#read source images
if ".gif" not in sys.argv[1]:
    sourceImage = cv2.imread(sys.argv[1])
else:
    ret, sourceImage = cv2.VideoCapture(sys.argv[1]).read()

if ".gif" not in sys.argv[2]:
    referenceImage = cv2.imread(sys.argv[2])
else:
    ret, referenceImage = cv2.VideoCapture(sys.argv[2]).read()

height, width, unused = sourceImage.shape
height2, width2, unused2 = referenceImage.shape

#verify dimensions are the same, else, exit
if np.size(sourceImage, 0) != np.size(referenceImage, 0):
    print("improper dimensions")
    sys.exit()

if np.size(sourceImage, 1) != np.size(referenceImage, 1):
    print("improper dimensions")
    sys.exit()

#source dimensions
y = width
x = height
print(x,"x", y)

xoverfill=False
yoverfill=False

xSteps = x/samplex
if x%samplex:
    xoverfill = True
    print("overfill x")
ySteps = y/sampley
if y%sampley:
    yoverfill=True
    print("overfill y")
index = 0;
for xIndex in range(0,math.floor(xSteps)):
    print("x",xIndex*samplex,":",xIndex*samplex+samplex)
    for yIndex in range(0,math.floor(ySteps)):
        #print("y",yIndex*sampley,":", yIndex*sampley+sampley)
        processSubregion(referenceImage, xIndex*samplex, xIndex*samplex+samplex, yIndex*sampley, yIndex*sampley+sampley, False)
        index = index+1
        #if yIndex == math.floor(ySteps)-1 and yoverfill:
            #print("y",yIndex*sampley+sampley,":", y)
            #processSubregion(referenceImage, xIndex*samplex, xIndex*samplex+samplex, yIndex*sampley+sampley, y, True)
    #print("_____________")
    #if xIndex == math.floor(xSteps)-1 and xoverfill:
        #print("x",xIndex*samplex+samplex,":",x)
        #for yIndex in range(0,math.floor(ySteps)):
            #print("y",yIndex*sampley,":", yIndex*sampley+sampley)
            #processSubregion(referenceImage, xIndex*samplex+samplex, x, yIndex*sampley, yIndex*sampley+sampley, False)
            #index = index+1
            #if yIndex == math.floor(ySteps)-1 and yoverfill:
                #print("y",yIndex*sampley+sampley,":", y)
                #processSubregion(referenceImage, xIndex*samplex+samplex, x, yIndex*sampley+sampley, y, True)


print("x steps = ", xSteps)
print("y steps = ", ySteps)
#xSteps = math.floor(source)
