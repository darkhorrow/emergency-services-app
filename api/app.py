from flask import Flask, render_template, request, Response
from flask_restful import Api
from flask_googlemaps import GoogleMaps, Map
from clips import Symbol, Environment

env = Environment()

env.load("expert_system.clp")
env.reset()

SERVICE_TEMPLATE = env.find_template('Service')
EMERGENCY_TEMPLATE = env.find_template('Emergency')

service_count = 0
emergency_count = 0

app = Flask("CLIPS Map", template_folder="templates")
api = Api(app)
GoogleMaps(app, key="AIzaSyBWoKCv2cZw-GgDhMR2KaDXMLV0dbsvMIw")


@app.route("/")
def display_map():
    my_map = Map(identifier="view-side", lat=-15.42843, lng=28.12504)
    return render_template('example.html', mymap=my_map)


@app.route("/addService", methods=['POST'])
def add_service():
    global service_count
    name = request.form.get("name")
    loc_x = request.form.get("locx")
    loc_y = request.form.get("locy")
    service = SERVICE_TEMPLATE.new_fact()
    service["id"] = service_count
    service["name"] = Symbol(name)
    service["location"] = [loc_x, loc_y]
    service["n_members"] = 100
    service["movement_speed"] = 10.0
    service["prep_time"] = 5.0
    service.assertit()

    if service.asserted:
        service_count += 1

    env.run()

    return Response()


@app.route("/addEmergency", methods=['POST'])
def add_emergency():
    global emergency_count
    e_type = request.form.get("type")
    loc_x = request.form.get("locx")
    loc_y = request.form.get("locy")
    n_people = request.form.get("npeople")
    service = EMERGENCY_TEMPLATE.new_fact()
    service["id"] = emergency_count
    service["type"] = Symbol(e_type)
    service["location"] = [loc_x, loc_y]
    service["n_affected_people"] = int(n_people)
    service.assertit()

    if service.asserted:
        emergency_count += 1

    env.run()

    return Response()


if __name__ == '__main__':
    app.run(debug=True)
