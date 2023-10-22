import csv
from keys import FLASK_SECRET_KEY, ORS_KEY
from flask import Flask, render_template, request, session
from openrouteservice import Client, convert
from folium import Map, GeoJson
from get_accident_data import COORD_DECIMAL_PLACES

def display_routes(start, end):
    """
    Given a start and end location, return a HTML representation of a Folium map
    showing up to 3 routes from start to end, color coded by the total severity
    of accidents along them.
    """
    alternative_params = {
        "target_count" : 3,
        "share_factor" : 0.5,
    }
    raw_routes = osr_client.directions((start, end), alternative_routes=alternative_params)

    routes = []
    for raw_route in raw_routes["routes"]:
        routes.append(convert.decode_polyline(raw_route["geometry"])["coordinates"])

    severity_numbers = [get_route_severity(route, cycle_accidents) for route in routes]    
    severity_colors = get_severity_colors(severity_numbers)

    folium_map = Map(location=(start[1], start[0]), zoom_start=14)
    for index, raw_route in enumerate(raw_routes["routes"]):
        geometry = convert.decode_polyline(raw_route["geometry"])
        color = severity_colors[index]
        GeoJson(geometry, style_function=lambda x, color=color:{"color" : color}).add_to(folium_map)

    return folium_map._repr_html_()

def get_route_severity(route, cycle_accidents):
    """
    Given a route (list of coordinates) and data about cycle accidents,
    calculates the severity of the route by totalling the severity of accidents
    along the route.
    """
    # NOTE: route is in the form lon, lat, rather than the standard lat, lon. This is fixed in rounded_route.
    rounded_route = [[round(lat, COORD_DECIMAL_PLACES), round(lon, COORD_DECIMAL_PLACES)] for lon, lat in route]
    route_severity = 0
    for lat, lon, severity in cycle_accidents:
        if [lat, lon] in rounded_route:
            route_severity += severity
    return route_severity

# def get_route_accidents(route, cycle_accidents):
#     """
#     Given a route (list of coordinates) and data about cycle accidents, returns
#     a list of all accidents along that route (i.e. a list of coordinates).
#     """
#     # NOTE: route is in the form lon, lat, rather than the standard lat, lon. This is fixed in rounded_route.
#     rounded_route = [[round(lat, COORD_DECIMAL_PLACES), round(lon, COORD_DECIMAL_PLACES)] for lon, lat in route]
#     route_accidents = []
#     for lat, lon, severity in cycle_accidents:
#         if [lat, lon] in rounded_route:
#             route_accidents.append([lat, lon, severity])
#     return route_accidents

def get_severity_colors(severity_numbers):
    """
    Given a list of severity numbers, returns a corresponding list of colors.
    """
    severity_colors = []

    for severity_number in severity_numbers:
        if severity_number == min(severity_numbers):
            severity_colors.append("#00ff00")
        elif severity_number == max(severity_numbers):
            severity_colors.append("#ff0000")
        else:
            severity_colors.append("#fbff03")

    return severity_colors

def read_cycle_accidents_csv(filename):
    """
    Takes in the filename of a csv file containing cycle accident data, and
    returns it as a list in the format [lat, lon, severity].
    """
    cycle_accidents = []

    with open(filename, newline="") as f:
        reader = csv.reader(f)
        next(reader)    # Skip header
        cycle_accidents = [[float(i) for i in row] for row in reader]
    
    return cycle_accidents

cycle_accidents = read_cycle_accidents_csv("cycle_accidents.csv")

osr_client = Client(key=ORS_KEY)

app = Flask(__name__)
app.config["SECRET_KEY"] = FLASK_SECRET_KEY

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/map_first_load")
def map_first_load():
    folium_map = Map(location=(51.5121, -0.1169), zoom_start=14)
    return folium_map._repr_html_()

@app.route("/set_session_variables")
def set_session_variables():
    session["start"] = (float(request.args.get("start0")), float(request.args.get("start1")))
    session["end"] = (float(request.args.get("end0")), float(request.args.get("end1")))
    return("Done!")

@app.route("/update_map")
def update_map():
    return display_routes(session["start"], session["end"])

if __name__ == "__main__":
    app.run(debug=True)

# Powered By:

#       __   ___                              _____         _    _                     
#       \ \ / / |                            / ____|       | |  | |                    
#    ___ \ V /| |_ _ __ ___ _ __ ___   ___  | |  __  ___   | |__| | ___  _ __ ___  ___ 
#   / _ \ > < | __| '__/ _ \ '_ ` _ \ / _ \ | | |_ |/ _ \  |  __  |/ _ \| '__/ __|/ _ \
#  |  __// . \| |_| | |  __/ | | | | |  __/ | |__| | (_) | | |  | | (_) | |  \__ \  __/
#   \___/_/ \_\\__|_|  \___|_| |_| |_|\___|  \_____|\___/  |_|  |_|\___/|_|  |___/\___|
                                                                                                                                                             