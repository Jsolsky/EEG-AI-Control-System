#!/usr/bin/env python3

import os

def findDataFiles(numSubjects, runNum):
    # Define the parent directory where the SXXX directories are located
    parentDir = "rawData/"

    # Loop through each SXXX directory and look for the desired files
    dataFilePaths = [] # Empty list where the paths to the data are stored.

    for i in range(1, (numSubjects + 1)):
        # Generate the SXXX directory name based on the loop index
        subjectDir = "S{:03d}".format(i)
        # Construct the full path to the SXXX directory
        subjectPath = os.path.join(parentDir, subjectDir)

        if os.path.exists(subjectPath):
            # Check if the runNum file exists in the SXXX directory
            for j in range(len(runNum)):
                # Check if the file exists for each runNum in the list
                fileName = "{}.edf".format(subjectDir + runNum[j])
                filePath = os.path.join(subjectPath, fileName)
                if os.path.exists(filePath):
                    dataFilePaths.append(filePath)
                else:
                    print("ERROR: File not found:", filePath)

        else:
            print("Directory not found:", subjectPath)

    return dataFilePaths
