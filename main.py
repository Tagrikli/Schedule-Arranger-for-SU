from AddDropHelper import AddDropHelper
from flask import Flask, render_template, jsonify

app = Flask(__name__)
helper = AddDropHelper("202002.json")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/api/v1/courseCodes")
def courseCodes():
    return jsonify(helper.getCourseCodes)

@app.route("/api/v1/matchRequest/<lolo>&<int:conf>")
def request(lolo,conf):
    lolo = lolo.replace("%20"," ")
    codes = lolo.split(";")
    print(codes)
    possibleSchudules = helper.findMatches(codes,conf)
    helper.saveCRNs(possibleSchudules,"static/")
    with open("static/result.json","r") as file:
        content = file.read()

    return jsonify(content)

app.run()