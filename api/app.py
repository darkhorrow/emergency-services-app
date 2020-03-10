from flask import Flask, render_template, request, jsonify
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

app = Flask("CLIPS Map", template_folder="templates", static_folder="static")
api = Api(app)
GoogleMaps(app, key="AIzaSyBWoKCv2cZw-GgDhMR2KaDXMLV0dbsvMIw")


@app.route("/")
def display_map():
    my_map = Map(identifier="view-side", lat=-15.42843, lng=28.12504)
    return render_template('index.html', mymap=my_map)


@app.route("/addService", methods=['POST'])
def add_service():
    global service_count
    service = SERVICE_TEMPLATE.new_fact()
    service["id"] = service_count
    service["name"] = Symbol(request.form.get("servicename"))
    service["location"] = [float(request.form.get("locx")), float(request.form.get("locy"))]
    service["n_members"] = int(request.form.get("members"))
    service["movement_speed"] = float(request.form.get("speed"))
    service["prep_time"] = float(request.form.get("preptime"))
    service.assertit()

    if service.asserted:
        service_count += 1

    env.run()

    return jsonify(id=service["id"], service_name=service["name"])


@app.route("/addEmergency", methods=['POST'])
def add_emergency():
    global emergency_count
    service = EMERGENCY_TEMPLATE.new_fact()
    service["id"] = emergency_count
    service["type"] = Symbol(request.form.get("emergencytype"))
    service["location"] = [float(request.form.get("locx")), float(request.form.get("locy"))]
    service["n_affected_people"] = int(request.form.get("affected"))
    service.assertit()

    if service.asserted:
        emergency_count += 1

    env.run()

    return jsonify(id=service["id"], emergency_type=service["type"])


@app.route("/moveService", methods=['POST'])
def move_service():
    fact_id = request.form.get("id")
    loc_x = request.form.get("locx")
    loc_y = request.form.get("locy")

    for fact in env.facts():
        if fact.template.name == 'Service' and fact['id'] == int(fact_id):
            service = SERVICE_TEMPLATE.new_fact()
            service["id"] = int(fact_id)
            service["name"] = fact['name']
            service["location"] = [float(loc_x), float(loc_y)]
            service["n_members"] = int(fact['n_members'])
            service["movement_speed"] = float(fact['movement_speed'])
            service["prep_time"] = float(fact['prep_time'])

            service.assertit()

            fact.retract()

            env.run()

            return jsonify(id=service["id"], service_name=service["name"])

    return jsonify(id=None, service_name=None)


@app.route("/moveEmergency", methods=['POST'])
def move_emergency():
    fact_id = request.form.get("id")
    loc_x = request.form.get("locx")
    loc_y = request.form.get("locy")

    for fact in env.facts():
        if fact.template.name == 'Emergency' and fact['id'] == int(fact_id):
            service = EMERGENCY_TEMPLATE.new_fact()
            service["id"] = int(fact_id)
            service["type"] = fact['type']
            service["location"] = [float(loc_x), float(loc_y)]
            service["n_affected_people"] = int(fact['n_affected_people'])

            service.assertit()

            fact.retract()

            env.run()

            return jsonify(id=service["id"], emergency_type=service["type"])

    return jsonify(id=None, emergency_type=None)


if __name__ == '__main__':
    app.run(debug=True)
