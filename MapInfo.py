import matplotlib.pyplot as plt
plt.style.use('seaborn-pastel')
import numpy as np
from matplotlib.patches import Circle
import cv2
import glob


MAX_X = 500
MAX_Y = 500

plotSquare1 = np.array([(-325, 75), (-475, 75), (-475, -75), (-325, -75)], dtype='float')
plotSquare2 = np.array([(325, 75), (475, 75), (475, -75), (325, -75)], dtype='float')
plotSquare3 = np.array([(-275, 375), (-125, 375), (-125, 225), (-275, 225)], dtype='float')

plotCircle1 = [(100), (0, 0)]
plotCircle2 = [(100), (-200, -300)]
plotCircle3 = [(100), (200, -300)]
plotCircle4 = [(100), (200, 300)]

plotBorderWall1 = np.array([(-500, 500), (500, 500),(500, -500),(-500, -500)], dtype = 'float')
plotBorderWall2 = np.array([(-510, 510), (510, 510),(510, -510),(-510, -510)], dtype = 'float')

fig = plt.figure()
fig.set_dpi(200)

axis = fig.add_subplot(111, aspect='equal', autoscale_on=False, xlim=(-(MAX_X+50), MAX_X+50), ylim=(-(MAX_Y+50), MAX_Y+50))

def circleOne(x, y, clearance):
    if ((x - 0) ** 2 + (y - 0) ** 2 - (100 + clearance) ** 2) <= 0:
        return False
    else:
        return True


def circleTwo(x, y, clearance):
    if ((x - (-200)) ** 2 + (y - (-300)) ** 2 - (100 + clearance) ** 2) <= 0:
        return False
    else:
        return True


def circleThree(x, y, clearance):
    if ((x - 200) ** 2 + (y - (-300)) ** 2 - (100 + clearance) ** 2) <= 0:
        return False
    else:
        return True


def circleFour(x, y, clearance):
    if ((x - 200) ** 2 + (y - 300) ** 2 - (100 + clearance) ** 2) <= 0:
        return False
    else:
        return True


def squareOne(x, y, clearance):
    if (y >= -75 - clearance) and (y <= 75 + clearance) and (x >= -475 - clearance) and (x <= -325 + clearance):
        return False
    else:
        return True

def squareTwo(x, y, clearance):
    if (y >= -75 - clearance) and (y <= 75 + clearance) and (x >= 325 - clearance) and (x <= 475 + clearance):
        return False
    else:
        return True


def squareThree(x, y, clearance):
    if (y >= 225 - clearance) and (y <= 375 + clearance) and (x >= -275 - clearance) and (x <= -125 + clearance):
        return False
    else:
        return True


def isValidStep(position, clearance):
    x = position[0]
    y = position[1]
    if circleOne(x, y, clearance) and circleTwo(x, y, clearance) and circleThree(x, y, clearance) and circleFour(x, y,
                                                                                                                 clearance) and squareOne(
            x, y, clearance) and squareTwo(x, y, clearance) and squareThree(x, y, clearance):
        return True
    else:
        return False

def save_fig(count):
    print("frame no:",count)
    if 0 <= count < 10:
        plt.savefig(r"./Node/0000000" + str(count) + ".png", bbox_inches='tight')
    if 10 <= count < 100:
        plt.savefig(r"./Node/000000" + str(count) + ".png", bbox_inches='tight')
    if 100 <= count < 1000:
        plt.savefig(r"./Node/00000" + str(count) + ".png", bbox_inches='tight')
    if 1000 <= count < 10000:
        plt.savefig(r"./Node/0000" + str(count) + ".png", bbox_inches='tight')
    if 10000 <= count < 100000:
        plt.savefig(r"./Node/000" + str(count) + ".png", bbox_inches='tight')
    if 100000 <= count < 1000000:
        plt.savefig(r"./Node/00" + str(count) + ".png", bbox_inches='tight')

def makeVideo():
    original = []
    title = []
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('Output_video1.avi', fourcc, 10.0, (779, 779))
    filenames = [f for f in glob.iglob("Node/*")]
    filenames.sort()
    for filename in filenames:
        img = cv2.imread(filename)
        print(filename)
        out.write(img)
        original.append(img)
    #time.sleep(1)
    length = len(original)


def showPath(STEP_OBJECT_LIST, pathValues, finalGoal):
    count = 0
    circle1 = plt.Circle((plotCircle1[1]), plotCircle1[0], fc=None)
    circle2 = plt.Circle((plotCircle2[1]), plotCircle2[0], fc=None)
    circle3 = plt.Circle((plotCircle3[1]), plotCircle3[0], fc=None)
    circle4 = plt.Circle((plotCircle4[1]), plotCircle4[0], fc=None)

    square1 = plt.Polygon(plotSquare1)
    square2 = plt.Polygon(plotSquare2)
    square3 = plt.Polygon(plotSquare3)
    borderWall1 = plt.Polygon(plotBorderWall1, fill=None)
    borderWall2 = plt.Polygon(plotBorderWall2, fill=None)
    obstacles = [circle1, circle2, circle3, circle4, square1, square2, square3]

    for item in obstacles:
        axis.add_patch(item)
        axis.add_patch(borderWall1)
        axis.add_patch(borderWall2)
        plt.gca().add_patch(Circle((finalGoal[0], finalGoal[1]), 20, color='green', fill=None))
        plt.axis('off')
        plt.plot(finalGoal[0], finalGoal[1], 'ro')

    frameNo = 0
    frameRate = 3
    for index in range(0, len(STEP_OBJECT_LIST), frameRate):
        try:
            subSteps = STEP_OBJECT_LIST[index].curveSteps
            for i in range(10):
                plt.plot([subSteps[i][0], subSteps[i+1][0]], [subSteps[i][1], subSteps[i+1][1]], color='blue', linewidth=0.2, markersize=5)
            save_fig(frameNo)
            frameNo = frameNo + 1
        except:
            continue

    index = 0
    while(index < len(pathValues)):
        try:
            flag = 0
            while flag < 10:
                plt.plot([pathValues[flag+index][0], pathValues[flag+index+1][0]], [pathValues[flag+index][1], pathValues[flag+index+1][1]], color='red', linewidth=0.3, markersize=5)
                flag+=1
            save_fig(frameNo)
            frameNo = frameNo + 1
            index = index + 10
        except:
            save_fig(frameNo)
            break

    makeVideo()
    plt.show()

