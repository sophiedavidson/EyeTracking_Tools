# Sophie Davidson, 2022

# The following program will use window design to smooth an eyetracker result

# Imports --------------------------------------------------------------------------------------------------------------
import numpy as np
import csv
# Constants ------------------------------------------------------------------------------------------------------------

# The maximum allowable distance from a previous point before it is interpreted as a saccade
SACCADE_THRESHOLD = 10
# The number of points used in the fixation point calculation
WINDOW_LENGTH = 3

# Globals --------------------------------------------------------------------------------------------------------------

global currentFixation
global potentialFixation


# Functions ------------------------------------------------------------------------------------------------------------
# Calculate the weighted fixation point using a one-sided triangular filter
def calculateFixationPoint(thisFixation):
    numerator = np.array([])
    denominator = np.array([])
    i = 0
    # loop through, multiply each (x,y) set of points by the weighted multiplier
    for multiplier in range(1, (thisFixation.size//2)+1):
        numerator = np.append(numerator, np.multiply(thisFixation[i], multiplier))
        numerator = np.append(numerator, np.multiply(thisFixation[i+1], multiplier))
        denominator = np.append(denominator, multiplier)
        i = i+2

    numX = numerator[::2].sum()
    numY = numerator[1::2].sum()
    denominator = denominator.sum()
    x = numX/denominator
    y = numY/denominator

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
        if currentFixation.size > (2*WINDOW_LENGTH):
            currentFixation = currentFixation[-2*WINDOW_LENGTH::1]
    elif fixation == "potential":
        potentialFixation = np.append(point, potentialFixation)
    else:
        print("Invalid fixation")


def filterPoint(point):
    global currentFixation
    global potentialFixation

    point = np.array([point])
    if isEmpty(currentFixation):
        currentFixation = np.append(currentFixation, point)
        return
    else:
        currentFixationPoint = calculateFixationPoint(currentFixation)
        if isEmpty(potentialFixation):
            distance = calculateDistance(np.array([currentFixationPoint]), point)
            if distance < SACCADE_THRESHOLD:
                addPoint(point, "current")
                # TODO Error starts Here
                currentFixationPoint = calculateFixationPoint(currentFixation)
                return currentFixationPoint
            else:
                addPoint(point, "potential")
                return currentFixationPoint
        else:
            potentialFixationPoint = potentialFixation
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
    filename = "eyeData.csv"
    fields = []
    rows = []

    with open(filename, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        for row in csvreader:
            rows.append(row)

        numberRows = csvreader.line_num
        print(numberRows)

    currentFixation = np.array([])
    potentialFixation = np.array([])
    points = []
    point = np.array([float(row[0]), float(row[1])])
    calculateFixationPoint(point)
    for row in rows[0:50]:
        point = np.array([float(row[0]), float(row[1])])
        print(point)
        print(f"current fixation:\n{currentFixation}")
        print(f"potential fixation: \n{potentialFixation}")
        filteredPoint = filterPoint(point)
        print(f"calculated point\n{filteredPoint}")
        points.append(filteredPoint)
    del points[0]
    with open("output.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(("x", "y"))
        writer.writerows(points)
        print(points)
if __name__ == "__main__":
    main()
# ----------------------------------------------------------------------------------------------------------------------
