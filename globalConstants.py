""" The constants for the project """

import logging
import os

# Set the logging level across all files
loggingLevel = logging.DEBUG

# Automatically get the location of the local dropbox folder
if os.path.isdir("C:/Users/Trevor"):
    dropboxPath = "C:/Users/Trevor/Dropbox/"
else:
    dropboxPath = "C:/Users/TrevHP/Dropbox/"
