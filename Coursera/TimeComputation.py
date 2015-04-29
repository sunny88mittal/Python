import sys
import re
from os import listdir
from os.path import isdir, join, isfile, getsize

#Function to get the multiplier for the file size
def gatherStatistics(dirList):
   multiple = 0
   for dir in dirList:
       files = getMp4FilesList(dir)
       if len(files) > 0:
           for file in files:
               fileTime = getTime(file)
               if (fileTime[1] != 0 or fileTime[2] != 0) :
                  fileSizeBytes = getsize(join(dir, file))
                  fileTimeSec = int(fileTime[0]) * 3600 + int(fileTime[1]) * 60 + int(fileTime[2])
                  return float(fileTimeSec)/float(fileSizeBytes)
   return multiple

#Function to get the list of first level directories in a directory
def getDirectories(coursepath):
    finalDirList = []
    dirList = listdir(coursepath)
    for dir in dirList:
        absDirPath = join(coursepath,dir)
        if isdir(absDirPath):
            finalDirList.append(absDirPath)
    return finalDirList

#Function to get the list of files in a directory with mp4 extension
def getMp4FilesList(dirPath):
    finalFilesList = []
    filesList = listdir(dirPath)
    for file in filesList:
        if file.endswith('.mp4'):
            finalFilesList.append(file)
    return finalFilesList

#Extracts the time in the form hhmmss and returns it
def getTime(fileName):
    time = [00,00,00]
    fileName = fileName.replace(':', '_')
    fileName = fileName.replace('-', '_')
    fileName = fileName.replace('[', '(')
    fileName = fileName.replace(']', ')')
    fileName = fileName.replace('mins', 'min')
    pattern = '\([0-9]{1,13}.*\)'
    if (re.search(pattern, fileName) == None):
        return time

    m = re.search(pattern, fileName)
    rawTime = m.group(0)

    if (re.match('(\([0-9]{1,2}[\s]{0,3}min\))',rawTime)):
        pattern = '([0-9]{1,2})'
        time[1] = int (re.search(pattern,rawTime).group(0))

    elif (re.match('(\([0-9]{2}_[0-9]{2}_[0-9]{2}\))',rawTime)):
         pattern = '([0-9]{2}_[0-9]{2}_[0-9]{2})'
         m = re.search(pattern, fileName)
         time = m.group(0).split('_')

    elif (re.match('(\([0-9]{2}_[0-9]{2}\))',rawTime)):
         pattern = '([0-9]{2}_[0-9]{2})'
         m = re.search(pattern, fileName)
         timeTemp = m.group(0).split('_')
         time[1] = timeTemp[0]
         time[2] = timeTemp[1]

    elif (re.match('(\([0-9]{3}\))',rawTime)):
         pattern = '([0-9]{3})'
         m = re.search(pattern, fileName)
         time[1] = int(m.group(0)[0:1])
         time[2] = int(m.group(0)[1:3])

    elif (re.match('(\([0-9]{4}\))',rawTime)):
         pattern = '([0-9]{4})'
         m = re.search(pattern, fileName)
         time[1] = int(m.group(0)[0:2])
         time[2] = int(m.group(0)[2:4])

    return time

#Adds two time arrays
def addTimes(totalTime, timeToAdd):
    for i in range(len(totalTime)):
        totalTime[i] = int(totalTime[i]) + int(timeToAdd[i])
    return totalTime

#Returns proper time in the format hh:mm:ss
def getProperTime(totalTime):
   totalTime[1] = totalTime[1] + totalTime[2] / 60
   totalTime[2] = totalTime[2] % 60;
   totalTime[0] = totalTime[0] + totalTime[1] / 60
   totalTime[1] = totalTime[1] % 60;
   return str(totalTime[0]) + ':' + str(totalTime[1]) + ':' + str(totalTime[2])

#Take the input
#coursepath = '/home/sunny/Documents/Courses/3. Artificial Intelligence/Neural Networks for Machine Learning'
coursepath = sys.argv[1];

#Get the sub directories
dirList = getDirectories(coursepath)
dirList.sort()
courseTotalTime = [00,00,00]
warnings = []
multiple = gatherStatistics(dirList)

#Do the computation for week 0
files = getMp4FilesList(coursepath)
if len(files) > 0:
    for file in files:
        courseTotalTime = addTimes(courseTotalTime,getTime(file))
    print '{0} -- {1}'.format('Week 0', getProperTime(courseTotalTime))

#Do the computation for weeks
for dir in dirList:
    totalTime = [00,00,00]
    files = getMp4FilesList(dir)
    if len(files) > 0:
        for file in files:
            fileTime = getTime(file)
            if (fileTime[1] == 0 and fileTime[2] == 0) :
                warnings.append('Warn: Some problem with file :{0} in dir :{1}'.format(file, dir.split('/')[-1]))
                fileTimeTemp = int(multiple * float(getsize(join(dir, file))))
                fileTime[0] = fileTimeTemp / 3600
                fileTimeTemp = fileTimeTemp % 3600
                fileTime[1] = fileTimeTemp / 60
                fileTime[2] = fileTimeTemp % 60
            totalTime = addTimes(totalTime,fileTime)
        courseTotalTime = addTimes(courseTotalTime, totalTime)
        print '{0} -- {1}'.format(dir.split('/')[-1], getProperTime(totalTime))
print 'Total  -- {0}'.format(getProperTime(courseTotalTime))
if (len(warnings) > 0) :
    print('-----------------------Printing all warnings--------------------------')
    for warning in warnings:
        print(warning)