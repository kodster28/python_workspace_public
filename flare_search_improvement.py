import os
import sys

#grab location data from Flare. Triggered using post-build event
outputDestination = sys.argv[1]
scriptLocation = os.path.join(outputDestination, 'Resources\\Scripts\\MadCapAll.js')

#open the file, store data, and do a brute-force find/replace to add new stop words
originalFile = open(scriptLocation, 'r')
updatedFileData = originalFile.read().replace("StopWords=Array(", 'StopWords=Array("How","how","What","what","Where","When","I","i","Do","why","Why",')
originalFile.close()

#replace the content in the MadCapAll.js file. Save to same location for upload.
updatedFile = open(scriptLocation, 'w')
updatedFile.write(updatedFileData)
updatedFile.close()
