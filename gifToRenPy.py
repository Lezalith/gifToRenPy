####### File stuff #####################################

# Lets you pick a file and returns it.
import easygui

def pickFile():

    a = easygui.fileopenbox( title = "Pick .gif to split:" )

    # Raise exception if a file wasn't picked
    if not a:
        raise Exception("Nothing selected!")
        
    return a

# File path with extension.
gifFilePath = pickFile()
# print(gifFilePath)

# File name with extension.
gifFile = gifFilePath.split("\\")[-1]
# print(gifFile)

# File name without extension.
gifFileName = ".".join(gifFile.split(".")[:-1])
# print(gifFileName)


####### Gif into frames #####################################


# For the (gif -> png) conversion.
from PIL import Image

# Load in chosen file.
im = Image.open(gifFilePath)

# For every frame inside the loaded Image:
for frameIndex in range( im.n_frames ):

    # Point at another frame.
    im.seek(frameIndex)

    # Filename of the saved frame.
    # Format is "[chosen file without extension][index of the frame].png"
    saveFileName = "{}{}.png".format(gifFileName, frameIndex)

    # Save the frame.
    im.save( saveFileName )