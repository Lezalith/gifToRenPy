####### File stuff ################################################################################

# Lets you pick a file and returns it.
import easygui

def pickFile():

    # Open the prompt.
    a = easygui.fileopenbox( title = "Pick .gif to split:" )

    # Raise exception if a file wasn't picked
    if not a:
        raise Exception("Nothing selected!")
        
    # Return the file.
    return a

# File path with extension.
gifFilePath = pickFile()

# File name with extension.
gifFile = gifFilePath.split("\\")[-1]

# Check if extension is ".gif"
if gifFile.split(".")[-1] != "gif":
    raise Exception("That is not a gif!")

# File name without extension.
gifFileName = ".".join(gifFile.split(".")[:-1])

# print(gifFilePath)
# print(gifFile)
# print(gifFileName)


####### Preparing a directory for the output ######################################################

# For checking and creating directories.
import os 

# Folder inside which all results are placed.
#
# This is important because this directory is included in paths inside the generated .rpy file.
# "images/" means the result inside should be placed inside a project's "images" folder.
baseOutputDir = "images/"

# If the directory doesn't already exist...
if not os.path.isdir(baseOutputDir):

    # ...create it.
    os.mkdir(baseOutputDir) 

# Folder inside which this result will be placed, in the form of "baseOutputDir/gifFileName/"
gifOutputDir = baseOutputDir + gifFileName + "/"
 
# This directory must not already exist.
if os.path.isdir(gifOutputDir):
    raise Exception("It looks like the directory for output, \"{}\", exists already!".format( baseOutputDir + gifFileName ))

# Create the directory.
os.mkdir(gifOutputDir)


####### Gif into frames ###########################################################################

# For the (gif -> png) conversion.
from PIL import Image

# Load in chosen file.
im = Image.open(gifFilePath)

# List of file paths to individual frames.
# Used in creating the .rpy file.
pathsToFrames = []

# For every frame inside the loaded Image:
for frameIndex in range( im.n_frames ):

    # Point at another frame.
    im.seek(frameIndex)

    # Filename of the saved frame.
    # Format is "[chosen file without extension][index of the frame].png"
    saveFileName = gifOutputDir + "{}{}.png".format(gifFileName, frameIndex)

    # Save the frame.
    im.save( saveFileName )

    # Save the frame path to a list.
    # Used in creating the .rpy file.
    pathsToFrames.append(saveFileName)

print("\nSuccessfully saved all frames into \"{}\"\n\n###########################################################\n".format(gifOutputDir))


####### Optionally creating a .rpy file.

createRpy = raw_input("Would you like to create a .rpy file with an image statement, defining the image for you?\nI do this by default, when nothing is typed in. Type \"n\" if you don't want me to. -- ")

# Negative input.
if createRpy == "n":

    print("\n###########################################################\n\nSkipped creating the .rpy file.")

    # End the script.
    exit()


####### Settings for creating a Ren'Py image statement. ###########################################

print("\nYou will now be asked for some settings.\nDefault values are chosen when nothing is typed in.\n")

### Time interval between frames. ###################################
pauseInterval = raw_input("Pause interval between frames? (float, default is 0.1) -- ")

# Default, if nothing given.
if not pauseInterval:

    pauseInterval = 0.1

# Convert it to a float.
else:

    try:
        pauseInterval = float(pauseInterval)

    # If cannot be converted:
    except:
        raise Exception("Pause interval, if given, must be a whole or a decimal number.")


### Whether the animation should repeat. ############################
addRepeat = raw_input("Should the animation repeat? (y/n, default is \"n\") -- ")

# Positive input.
if addRepeat == "y":

    addRepeat = True

# Negative or no input.
elif addRepeat == "n" or not addRepeat:

    addRepeat = False

# Something else typed in.
else:

    raise Exception("Something other than \"y\", \"n\" or \"\" typed in.")


### Properties that will be added onto the first line. ##############
### These will be in effect throughout the whole animation. #########
firstProperties = raw_input("Add some properties onto the first line? (Properties written like you would in ATL, none by default) -- ")

# If none are given, the line won't be added at all.
if not firstProperties:

    firstProperties = None


####### Creating a .rpy file with an image statement. #############################################

# Path of the .rpy file with extension.
rpyFilePath = gifOutputDir + gifFileName + ".rpy"

# Create the file.
with open(rpyFilePath, "w+") as f:

    # Image statement (first line)
    statement = "image " + gifFileName + ":\n"

    f.write(statement)

    # Add properties onto the first line if any were given.
    if firstProperties is not None:

        properties = "    " + firstProperties + "\n"

        f.write(properties)

    # Write an image path, followed by a pause of given interval.
    for pathToFrame in pathsToFrames:

        f.write( "    " + "\"" + pathToFrame + "\"\n" )
        f.write( "    " + "pause " + str(pauseInterval) + "\n" )

    # Optionally finish with a repeat.
    if addRepeat:

        f.write("    repeat")

print("\n###########################################################\n\nSuccessfully saved the .rpy file as \"{}\"".format(rpyFilePath))