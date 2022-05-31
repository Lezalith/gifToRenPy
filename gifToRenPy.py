# Lets you pick a file and returns it.
import easygui

def pickFile():

    a = easygui.fileopenbox( title = "Pick .gif to split:" )

    # Raise exception if a file wasn't picked
    if not a:
        raise Exception("Nothing selected!")
        
    return a

# File path, with extension.
gifFile = pickFile()