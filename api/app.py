from flask import Flask, render_template, request
from flask_restful import Api
from flask_googlemaps import GoogleMaps, Map
from clips import Symbol, Environment
from api.model.response import Success, Error
from api.settings import GOOGLE_MAPS_TOKEN
import json

env = Environment()

env.load("expert_system.clp")
env.reset()

SERVICE_TEMPLATE = env.find_template('Service')
EMERGENCY_TEMPLATE = env.find_template('Emergency')

service_count = 0
emergency_count = 0

app = Flask("CLIPS Map", template_folder="templates", static_folder="static")
api = Api(app)
GoogleMaps(app, key=str(GOOGLE_MAPS_TOKEN))


@app.route("/")
def display_map():
    global service_count
    global emergency_count
    service_count = 0
    emergency_count = 0
    my_map = Map(identifier="view-side", lat=-15.42843, lng=28.12504)

    facts = []
    for i, fact in enumerate(env.facts()):
        if fact.template.name == 'Service' or fact.template.name == 'Emergency':
            facts.append(fact)
    for fact in facts:
        fact.retract()
    env.run()

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
        data = {"id": service['id'], "name": service['name']}
        logs = get_current_responses()
        response = Success(callback=data, logs=logs, message="Emergency added successfully")
        json_data = json.dumps(response.__dict__, default=lambda o: o.__dict__, indent=4)
        return json_data

    response = Error(None, None, "Service could not be added. Try again later.")
    json_data = json.dumps(response.__dict__, default=lambda o: o.__dict__, indent=4)
    return json_data


@app.route("/addEmergency", methods=['POST'])
def add_emergency():
    global emergency_count
    emergency = EMERGENCY_TEMPLATE.new_fact()
    emergency["id"] = emergency_count
    emergency["type"] = Symbol(request.form.get("emergencytype"))
    emergency["location"] = [float(request.form.get("locx")), float(request.form.get("locy"))]
    emergency["n_affected_people"] = int(request.form.get("affected"))
    emergency.assertit()

    if emergency.asserted:
        emergency_count += 1
        env.run()
        data = {"id": emergency['id'], "type": emergency['type']}
        logs = get_current_responses()
        response = Success(callback=data, logs=logs, message="Emergency added successfully")
        json_data = json.dumps(response.__dict__, default=lambda o: o.__dict__, indent=4)
        return json_data

    response = Error(None, None, "Emergency could not be added. Try again later.")
    json_data = json.dumps(response.__dict__, default=lambda o: o.__dict__, indent=4)
    return json_data


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

            if service.asserted:
                env.run()
                response = Success(None, None, "Service re-allocated successfully!")
                json_data = json.dumps(response.__dict__, default=lambda o: o.__dict__, indent=4)
                return json_data

    response = Error(None, None, "Service could not be re-allocated. Try again later.")
    json_data = json.dumps(response.__dict__, default=lambda o: o.__dict__, indent=4)
    return json_data


@app.route("/moveEmergency", methods=['POST'])
def move_emergency():
    fact_id = request.form.get("id")
    loc_x = request.form.get("locx")
    loc_y = request.form.get("locy")

    for fact in env.facts():
        if fact.template.name == 'Emergency' and fact['id'] == int(fact_id):
            emergency = EMERGENCY_TEMPLATE.new_fact()
            emergency["id"] = int(fact_id)
            emergency["type"] = fact['type']
            emergency["location"] = [float(loc_x), float(loc_y)]
            emergency["n_affected_people"] = int(fact['n_affected_people'])

            emergency.assertit()

            fact.retract()

            if emergency.asserted:
                env.run()
                response = Success(None, None, "Emergency re-allocated successfully!")
                json_data = json.dumps(response.__dict__, default=lambda o: o.__dict__, indent=4)
                return json_data

        response = Error(None, None, "Emergency could not be re-allocated. Try again later.")
        json_data = json.dumps(response.__dict__, default=lambda o: o.__dict__, indent=4)
        return json_data


def get_current_responses():
    responses = []
    facts = []
    for i, fact in enumerate(env.facts()):
        if fact.template.name == 'Solution':
            fact_data = dict()
            fact_data['code'] = fact['code_error']
            fact_data['id_emergency'] = fact['id_emergency']
            fact_data['id_service'] = fact['id_service']
            fact_data['service'] = fact['name_service']
            fact_data['emergency'] = fact['name_emergency']
            responses.append(fact_data)
            facts.append(fact)
    for fact in facts:
        fact.retract()
    env.run()

    return responses


def is_error_response(response):
    return response['code'] < 0


if __name__ == '__main__':
    app.run(debug=True)
