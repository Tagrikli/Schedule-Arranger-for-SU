from AddDropHelper import AddDropHelper
from flask import Flask, render_template, jsonify

app = Flask(__name__)
helper = AddDropHelper("202002.json")

@app.route("/")
def home():
    return "Hello!"

@app.route("/api/v1/courseCodes")
def courseCodes():
    response = jsonify(helper.getCourseCodes)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/api/v1/matchRequest/<lolo>")
def request(lolo):
    lolo = lolo.replace("%20"," ")
    codes = lolo.split(";")
    print(codes)
    possibleSchudules = helper.findMatches(codes)
    helper.saveCRNs(possibleSchudules,"static/")
    with open("static/result.json","r") as file:
        content = file.read()

    response = jsonify(content)
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response

app.run()