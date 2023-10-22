import csv
import requests
from keys import TFL_APP_ID, TFL_APP_KEY

LATEST_YEAR = 2019  # The latest year to get data from.
NUMBER_OF_YEARS = 10    # For how many years to get data from.
COORD_DECIMAL_PLACES = 4    # Number of decimal places to group coordinates. 4 d.p. = 11 m.
FILENAME = "cycle_accidents.csv"
parameters = {
    "app_id" : TFL_APP_ID,
    "app_key" : TFL_APP_KEY
}

# Get the coordinates of the accidents, grouping equivalent (based on coordinate
# decimal places) locations and totalling their severity.
coords_to_severity = {}    # Using a dict allows to group equivalent locations.
for year in range(LATEST_YEAR, LATEST_YEAR - NUMBER_OF_YEARS, -1):
    response = requests.get(f"https://api.tfl.gov.uk/AccidentStats/{year}", params=parameters)

    for accident in response.json():
        cycle_involved = False
        vehicles = accident["vehicles"]

        for vehicle in vehicles:
            if vehicle["type"] == "PedalCycle":
                cycle_involved = True
                break

        if cycle_involved:
            coordinates = round(accident["lat"], COORD_DECIMAL_PLACES), round(accident["lon"], COORD_DECIMAL_PLACES)
            severity = 0
            match accident["severity"]:
                case "Slight":
                    severity = 1
                case "Serious":
                    severity = 10
                case "Fatal":
                    severity = 100                    
            coords_to_severity[coordinates] = coords_to_severity.get(coordinates, 0) + severity

# Write the accidents to file, in the format lat, lon, severity.
with open(FILENAME, "w", newline="") as f:
    writer = csv.writer(f)

    header = ["lat", "lon", "severity"]
    writer.writerow(header)
    
    for coordinates, severity in coords_to_severity.items():
        writer.writerow([coordinates[0], coordinates[1], severity])
