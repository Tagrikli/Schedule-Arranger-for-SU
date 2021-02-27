from itertools import product
import numpy as np
from tqdm import tqdm
import json


class Section:
    def __init__(self, vals):
        crn, schedule, group, instructor = vals

        self.crn = int(crn)
        self.schedules = schedule
        self.group = group
        self.instructor = instructor
        self.sule = self.getSule()

    def getSule(self):
        sule = np.zeros((15,6))
        for sched in self.schedules:
                day = sched["day"]
                start = sched["start"]
                dur = sched["duration"]
                for i in range(start,start+dur):
                    sule[i][day] = 1

        return sule

class Class:
    def __init__(self):
        self.sections = []

    def addSection(self, vals):
        self.sections.append(Section(vals))

    @property
    def sectionCount(self):
        return len(self.sections)

    def getSectionCRNs(self):
        return [sec for sec in self.sections]



class Course:
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.classes = []

    def addClass(self, classes):
        for classue in classes["classes"]:
            classTemp = Class()
            for sec in classue["sections"]:
                classTemp.addSection(
                    (sec["crn"], sec["schedule"], sec["group"], sec["instructors"]))
            self.classes.append(classTemp)

    def getCombinations(self):
        crnList = []

        for clasue in self.classes:
            crnList.append(clasue.getSectionCRNs())

        return list(product(*crnList))



class AddDropHelper:
    def __init__(self,dataFilename):
        with open(dataFilename, "r") as file:
            self.data = json.loads(file.read())

        self.courseList = []
        self.courseCodes = []
        for course in self.data["courses"]:
            crsTemp = Course(course["name"],course["code"])
            crsTemp.addClass(course)
            self.courseList.append(crsTemp)
            self.courseCodes.append(course["code"])

    def findMatches(self,codes,confLimit = 0):
        schedules = []
        for code in codes:
            for course in self.courseList:
                if course.code == code:
                    schedules.append(course.getCombinations())

        allPossibs = list(product(*schedules))
        minCon = 100
        possibleSchedules = []
        for possib in tqdm(allPossibs):
            conCo, sule = self.findConflicts(possib)
            if conCo <= 1 + confLimit:
                possibleSchedules.append({"su":possib,"conf":conCo})
            

        return possibleSchedules


    @property
    def getCourseCodes(self):
        return {"codes":self.courseCodes}

    def saveCRNs(self,possibleSchedules,loc):
        
        modif = {"result":[]}
        for data in possibleSchedules:
            crnList = []
            for su in data["su"]:
                for clasue in su:
                    crnList.append(clasue.crn)

                data["su"] = crnList
            modif["result"].append(data)

        with open(loc + "result.json","w") as file:
            file.write(json.dumps(modif))


    def findConflicts(self,schedule):
        
        suleSum = np.zeros((15,6))
        for clasue in schedule:
            for sect in clasue:
                suleSum += sect.sule
        
        return suleSum.max(), suleSum


if __name__ == "__main__":

    help = AddDropHelper("202002.json")
    print(help.courseCodes)