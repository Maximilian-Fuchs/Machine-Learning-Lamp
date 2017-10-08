import math
sampleTimeInSeconds = 30
# Writes dummy data due to lack of time...
# Writes to separate file "decision_tree_data_DUMMY_DATA" to avoid accidental change

# Be mindful of sampleTimeInSeconds
# Assumes week starts at Weekday 1
def writeDummyWeekendData():
    # We assume person is not at home weekends
    devices = [
        "tk3iot/iPad DISCONNECTED",
        "tk3iot/esp1 DISCONNECTED",
        "tk3iot/esp2 DISCONNECTED",
        "tk3iot/iPad DISCONNECTED",
        "tk3iot/PC DISCONNECTED",
        "tk3iot/iPhone DISCONNECTED",
        "tk3iot/android DISCONNECTED"
    ]
    secCount = 0
    f = open('decision_tree_data_DUMMY_DATA', 'a')
    
    while secCount < 259200:
        daytime_hour = (secCount/3600)%24

        if daytime_hour < 6 or daytime_hour > 23:
            daytime = 'NIGHT'
        elif daytime_hour < 9:
            daytime = 'EARLY_MORNING'
        elif daytime_hour < 12:
            daytime = 'MORNING'
        elif daytime_hour < 15:
            daytime = 'EARLY_AFTERNOON'
        elif daytime_hour < 18:
            daytime = 'LATE_AFTERNOON'
        elif daytime_hour < 21:
            daytime = 'EVENING'
        elif daytime_hour <= 23:
            daytime = 'LATE_EVENING'

        if daytime == 'NIGHT' or daytime == 'LATE_EVENING':
            daylight = "Daylight False"    
        else:
            daylight = "Daylight True"
        weekday = "Weekday {}".format(math.floor(secCount/(3600*24)) + 5)
        lamp_status = "Lamp Off"
        line = ""
        line += "\t".join(devices)
        line += "\t" + daylight
        line += "\t" + weekday
        line += "\t" + daytime
        line += "\t" + lamp_status


        secCount += sampleTimeInSeconds

        print(line)
        f.write(line + '\n')  # python will convert \n to os.linesep
    
    f.close()
    


writeDummyWeekendData()