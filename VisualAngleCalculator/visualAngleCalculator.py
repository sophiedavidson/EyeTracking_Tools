# Sophie Davidson, 2022

"""
The following script will convert pixels to cm, and then calculate the visual angle
using user input.

Example:
calculateVisAngle(500, "Vertical")  where 500 is the number of pixels, and "Vertical" is the orientation.

"""


# Imports
import pyautogui
from psychopy import gui
from numpy import arctan


# Calculate the visual angle using the number of pixels, and the orientation, return as number
def calculateVisAngle(pix, orientation):
    experimentDetails = getUserInput()
    dimensions = (experimentDetails.get("Horizontal"), experimentDetails.get("Vertical"))
    pixPerCm = calculatePixCm(dimensions, orientation)
    cm = pix*pixPerCm
    visualAngle = arctan(cm/experimentDetails.get("Distance"))
    return visualAngle


# calculate the number of pixels per centimeter, return as number
def calculatePixCm(dimensions, orientation):
    (width, height) = pyautogui.size()  # gets the screen resolution
    pixelsPerCm = 0
    if orientation == "Vertical":
        pixelsPerCm = height / dimensions[1]
    elif orientation == "Horizontal":
        pixelsPerCm = width/dimensions[0]
    else:
        print("Invalid Input Orientation")

    return pixelsPerCm


# Get the user input containing screen dimensions and viewing distance, return to dict.
def getUserInput():
    dialogue = gui.Dlg(title="Display Information")
    dialogue.addText("Display Characteristics:", color="Blue")
    dialogue.addField("Screen Vertical:", tip="The height of the screen in cm")
    dialogue.addField("Screen Horizontal", tip="The width of the screen in cm")
    dialogue.addText("Experiment Characteristics")
    dialogue.addField("Viewing Distance from Screen:", tip="Distance in cm from center of screen to viewer")
    userInput = dialogue.show()

    if dialogue.OK:  # if the user clicks ok
        pass
    else:  # if the user clicks cancel
        print("User Cancelled")

    experimentDetails = {"Vertical": int(userInput[0]),
                         "Horizontal": int(userInput[1]),
                         "Distance": int(userInput[2])
                         }
    return experimentDetails
