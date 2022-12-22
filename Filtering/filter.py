# Sophie Davidson, 2022

# The following program will use window design to smooth an eyetracker result

# Imports --------------------------------------------------------------------------------------------------------------
import numpy as np

# Constants ------------------------------------------------------------------------------------------------------------

# The maximum allowable distance from a previous point before it is interpreted as a saccade
SACCADE_THRESHOLD = 2
# The number of points used in the fixation point calculation
WINDOW_LENGTH = 4

# Globals --------------------------------------------------------------------------------------------------------------

global currentFixation
global potentialFixation


# Functions ------------------------------------------------------------------------------------------------------------
# Calculate the weighted fixation point using a one-sided triangular filter
def calculateFixationPoint(thisFixation):
    numerator = np.array([])
    denominator = np.array([])
    # implementing weighted average formula
    print(f"fixation:{thisFixation}")
    for i in range(0, thisFixation.size//2):
        weighted = np.multiply(thisFixation[i], i+1)
        numerator = np.append(numerator, weighted)
        denominator = np.append(denominator, i+1)

    xSum = numerator[::2].copy().sum()
    ySum = numerator[1::2].copy().sum()
    divisor = denominator.sum()
    # calculating x and y values
    x = xSum/divisor
    y = ySum/divisor


    return x, y


# calculate the distance between two points
def calculateDistance(fixation, point):
    distance = np.linalg.norm(fixation - point)
    return distance


# check if a numpy array is empty
def isEmpty(array):
    empty = (array.size == 0)
    return empty


# add a point to a global array
def addPoint(point, fixation):
    global currentFixation
    global potentialFixation

    if fixation == "current":
        currentFixation= np.append(currentFixation, point)
        # If we have exceeded the window length, remove the oldest entries
        #if currentFixation.size > (2*WINDOW_LENGTH):
        #    currentFixation = currentFixation[0:4:1]
    elif fixation == "potential":
        potentialFixation = np.append(point, potentialFixation)
    else:
        print("Invalid fixation")


def filterPoint(point):
    global currentFixation
    global potentialFixation

    point = np.array(point)
    if isEmpty(currentFixation):
        currentFixation = np.append(currentFixation, point)
        return
    else:
        currentFixationPoint = calculateFixationPoint(currentFixation)
        if isEmpty(potentialFixation):
            distance = calculateDistance(np.array([currentFixationPoint]), point)
            if distance < SACCADE_THRESHOLD:
                addPoint(point, "current")
                currentFixationPoint = calculateFixationPoint(currentFixation)
                return currentFixationPoint
            else:
                addPoint(point, "potential")
                return currentFixationPoint
        else:
            potentialFixationPoint = calculateFixationPoint(potentialFixation)
            distanceToCF = calculateDistance(np.array([currentFixationPoint]), point)
            distanceToPF = calculateDistance(np.array([potentialFixationPoint]), point)

            if distanceToCF < distanceToPF:
                if distanceToCF < SACCADE_THRESHOLD:
                    addPoint(point, 'current')
                    calculateFixationPoint(currentFixation)
                    potentialFixation = np.array([])
                    return currentFixationPoint
                else:
                    potentialFixation = np.array(point)
                    return currentFixationPoint
            else:
                if distanceToPF < SACCADE_THRESHOLD:
                    addPoint(point, "potential")
                    currentFixation = potentialFixation
                    potentialFixation = np.array([])
                    return currentFixationPoint
                else:
                    tempFixation = potentialFixation
                    potentialFixation = np.array([])
                    addPoint(point, "potential")

                    tempFixationPoint = calculateFixationPoint(tempFixation)
                    return tempFixationPoint


# Testing --------------------------------------------------------------------------------------------------------------
def main():
    global currentFixation
    global potentialFixation
    point = [2, 3]
    currentFixation = np.array([[1, 2], [2, 3]])
    potentialFixation = np.array([])

    print(f"calculated point\n{filterPoint(point)}")
    print(f"current fixation:\n{currentFixation}")
    print(f"potential fixation: \n{potentialFixation}")


if __name__ == "__main__":
    main()
# ----------------------------------------------------------------------------------------------------------------------
