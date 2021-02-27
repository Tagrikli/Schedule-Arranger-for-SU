from AddDropHelper import AddDropHelper

helper = AddDropHelper("202002.json")
desiredClasses = ["MATH 204","CS 204", "CS 201", "CS 302"]
possibleSchedules = helper.findMatches(desiredClasses,confLimit=0)
helper.saveCRNs(possibleSchedules,"")
