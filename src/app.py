import parking
import json
import os
from flask import Flask
from flask import request, jsonify

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = int(os.environ.get("DB_PORT", 3306))
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")

app = Flask(__name__)
parking = parking.Connection(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
conn = parking.get_conn()

@app.route("/")
def status():
    response = parking.status()
    return jsonify(response)

@app.route("/create_parking_lot", methods=['POST', 'GET'])
def create_parking_lot():
	no_of_slots = request.args.get("number")
	if no_of_slots is not None and no_of_slots.isnumeric():
		if parking.create_parking_lot(no_of_slots):
			return f"Created a parking lot with {no_of_slots} slots"
		else:
			return "Not able to create parking lot"
		return no_of_slots
	else:
		return "Invalid slot number is provided. Please enter valid slot number"


@app.route("/park", methods=['POST', 'GET'])
def park():
	reg_no = request.args.get("carnumber")
	color = request.args.get("color")

	response = parking.park(reg_no, color)

	return response