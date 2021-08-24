import re, csv
from datetime import datetime

#open file if in path, log all contents in list, close
apiLog = open("api.log",'r')
logContents = apiLog.readlines()
apiLog.close()

#regex pattern to extract our data from the strings, with captures
#group 1 is timestamp
#group 2 is endpoint key
#group 3 is log message
fullPattern = '(^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3}) templogger WARNING "([^"]*)" "([^"]*)"'

#datetime string format pattern, for use later
dateTimePattern = '%Y-%m-%d %H:%M:%S.%f'

#initiate empty dictionaries
startInfo = {}
endInfo = {}

#running through each item in list created from apiLog lines
for line in logContents:
    #whitespace normalization, replacing commas with periods for datetime difference later
    line = (re.sub(' +', ' ', line)).replace("\n", "").replace(",", ".")

    #finding regex matches in each line, then iterating
    foundInfo = re.finditer(fullPattern, line)
    for item in foundInfo:
        #if message has 'start', then log it to dictionary as a start line, using endpoint key as dictionary key
        if "start" in item.group(3):
            startInfo[item.group(2)] = [item.group(1), item.group(3)]
        #otherwise if message has 'end', then log it to dictionary as end line, same as above
        elif "end" in item.group(3):
            endInfo[item.group(2)] = [item.group(1), item.group(3)]
            
        #no else case here, purely because file provided is consistent in that each endpoint key has a start line and an end line ONLY, forgive the dirty scripting :)

#use csv library to write our new file
csvFile = open("parsed_apiLog.csv", "w", newline = '')

#csv headers provided by assignment
csvHeaders = ["Log Message", "Start Time", "End Time", "Time Diff"]

#initialize writing
writeLine = csv.writer(csvFile)
#write headers
writeLine.writerow(csvHeaders)

#because each line in the api.log file has a corresponding start and end, use the endpoint key from the "start" line to find both, could definitely be made more robust to handle dirtier logs
counter = 0
for key in startInfo:
    #initialize empty .csv line
    currentLine = []

    #create "Log Message" value for this line
    logMessage = startInfo[key][1] + " - " + endInfo[key][1]

    #create "Start Time" and "End Time" values for this line
    startTimestamp = startInfo[key][0]
    endTimestamp = endInfo[key][0]

    #using datetime library to convert both timestamps and get the delta
    formattedStartTimestamp = datetime.strptime(startTimestamp, dateTimePattern)
    formattedEndTimestamp = datetime.strptime(endTimestamp, dateTimePattern)
    #rounding the delta of the datetimes to 5 decimals and converting to minutes, as requested in the email
    formattedTimeDiff = str(round((formattedEndTimestamp - formattedStartTimestamp).seconds/60, 5))

    #write populated .csv line
    currentLine = [logMessage, startTimestamp, endTimestamp, formattedTimeDiff]
    writeLine.writerow(currentLine)
    counter +=1
    print("Successfully wrote line {}".format(counter))

#close the file to avoid possible IO issues
csvFile.close()
input("\nAll Done! Press ENTER key to close........")
