from opensky_api import OpenSkyApi
import json
import sys

# Declare global / continuous variables
totalCarbonEmissions = 0
averageEmissionRate = 0
countedIntervals = 0 # Since start of site

averageEfficiency = {
    0:0.2, #If no information is available, it is probably overseas, assume worst case
    1:0.2,
    2: 9, # For light aircrafts, the average is around 9 mpg
    3: 9, # Consider both aircraft types relatively 'light'
    4: 1.5, # Modeled after smaller Boeing model
    5: 0.2,
    6: 0.2, # Use 747 for large, long distance flight averages
    7:0,
    8:0,
    9:0,
    10:0,
    11:0,
    12:0,
    13:0,
    14:0,
    15:0,
    16:0,
    17:0,
    18:0,
    19:0,
    20:0
    }   

'''
2 = light
3 = small
4 = large
5 = high vortex large
6 = heavy

Formula for g of CO2 produced:
(1 gal / x miles) * (3785.41mL / 1 gal) * (0.80g fuel / 1 ml fuel) * (3.15g CO2 / 1g fuel)
'''

# Function will return variables
# Run until no error occurs
while True:
    try:
        api = OpenSkyApi()
        states = api.get_states()
    except:
        # If error, retry!
        # print("Error occurred, trying again")
        continue
    else:
        break
    
carbonEmissionRate = 0
distanceTraveled = 0
totalDistanceTraveled = 0

for s in states.states:
    # Multiply velocity by interval (30 seconds) and then multiply by plane type
    distanceTraveled = s.velocity * 30 if s.velocity != None else 0
    distanceTraveled = s.vertical_rate * 30 if s.vertical_rate != None and s.vertical_rate > 0 else 0

    # Convert to miles
    distanceTraveled = distanceTraveled / 1609
    totalDistanceTraveled += distanceTraveled
    
    # Convert to CO2
    if distanceTraveled != 0:
        carbonEmissionRate += (averageEfficiency[s.category]/ distanceTraveled) * (3785.41) * (0.80) * (3.15)

# Convert g to metric tonnes
carbonEmissionRate = carbonEmissionRate / 1000000

totalCarbonEmissions += carbonEmissionRate
# print("Distance traveled (30s) in miles: {}".format(int(totalDistanceTraveled)))
# print("CO2 produced (30s) in tonnes: {}".format(int(carbonEmissionRate)))
# print("Total CO2 produced in tonnes: {}".format(int(totalCarbonEmissions)))

# Once complete, average things lelelel
averageEmissionRate = averageEmissionRate * countedIntervals + carbonEmissionRate

countedIntervals += 1
averageEmissionRate = averageEmissionRate / countedIntervals
# print("Average CO2 produced (30s) in tonnes: {}".format(int(averageEmissionRate)))

returnDict = {'totalCarbonEmissions' : int(totalCarbonEmissions), 'averageEmissionRate' : int(averageEmissionRate), 'carbonEmissionRate' : int(carbonEmissionRate)}

# Return the data in a json object
data = json.dumps(returnDict)
print(data)

sys.stdout.flush()
























