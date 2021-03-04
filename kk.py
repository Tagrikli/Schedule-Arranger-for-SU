from AddDropHelper import AddDropHelper

helper = AddDropHelper("202002.json")
desiredClasses = ["PHIL 301","HUM 207","PSY 343", "PSY 443","PSY 304","PHIL 310"]
possibleSchedules = helper.findMatches(desiredClasses,confLimit=0)
helper.saveCRNs(possibleSchedules,"")

import json

with open("result.json","r") as file:
    data = json.loads(file.read())
    
print(len(data["result"]))

print(",".join(str(item[0]) for item in data["result"][0]["su"]))