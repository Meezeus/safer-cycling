# Safer Cycling

This application was created for **HackKing’s 2022**: a 12 hour hackathon organised
by **KCL Tech** and sponsored by **BlackRock**. Working as a team of 5, we had to create
a product to answer the challenge statement: _“How can we take advantage of the
changing technological landscape to contribute to a better future”_.

Our solution is a website that allows users to find safe cycling routes in
London. Users provide latitude and longitude coordinates of a start and end
location. The application will then display up to three routes, each one
color-coded based on how dangerous it is. The danger level of a route is
determined by the number of accidents that have taken place along the route, as
well as their severity.

![](https://github.com/Meezeus/safer-cycling/blob/425ffc54c45b7709129fbecef0da128635f1a21c/safer-cycling-website.png?raw=true)

## How to use

To use the application, first clone the repo. Make sure you have
[Python](https://www.python.org/) >=3.10 and install the following dependencies
using your favourite package manager:

- [Flask](https://flask.palletsprojects.com/en/3.0.x/)
- [Folium](https://pypi.org/project/folium/)
- [openrouteserivce](https://github.com/GIScience/openrouteservice-py)
- [Requests](https://pypi.org/project/requests/)

In the main project directory, create a file called _keys.py_. Inside you must
define 4 variables:

- FLASK_SECRET_KEY = "https://flask.palletsprojects.com/en/2.3.x/config/"
- ORS_KEY = "https://api.openrouteservice.org/"
- TFL_APP_ID = "https://api.tfl.gov.uk/"
- TFL_APP_KEY = "https://api.tfl.gov.uk/"

Replace the links with your own keys.

Run _get_accident_data.py_ to generate the _cycle_accidents.csv_ file, or use the
one provided.

Run _main.py_ and go to _localhost:5000_. In the Start and End field enter the
latitude and longitude (separated by a comma) of two locations, then press the
Search Routes button.

## Disclaimer

While the code for this application was originally written during the hackathon,
I cleaned it up a little and fixed a bug before uploading it here. I did not
modify any existing functionality or add new functionality.
