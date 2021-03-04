from itertools import product
import numpy as np
from tqdm import tqdm
import json


class Section:
    def __init__(self, vals, getSule):
        crn, schedule, group, _ = vals

        self.schedules = schedule
        self.sule = getSule(self.schedules)
        self.slots = {group:int(crn)}


    def getCRNs(self):
        return list(self.slots.values())

    def addSlot(self,group,crn):
        self.slots[group] = crn


class Class:
    def __init__(self):
        self.sections = []

    def addSection(self, vals):

        appended = False
        crn, schedule, group, _ = vals
        for section in self.sections:
            if np.all(section.sule == self.getSule(schedule)):
                section.addSlot(group,int(crn))
                appended = True

        if not appended:
            self.sections.append(Section(vals, self.getSule))


    def getSule(self,schedules):
        sule = np.zeros((15,6))
        for sched in schedules:
                day = sched["day"]
                start = sched["start"]
                dur = sched["duration"]
                for i in range(start,start+dur):
                    sule[i][day] = 1

        return sule


    @property
    def sectionCount(self):
        return len(self.sections)


    def getSections(self):
        return self.sections



class Course:
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.classes = []

    def addClass(self, classes):
        for classue in classes:
            classTemp = Class()
            for sec in classue["sections"]:
                classTemp.addSection(
                    (sec["crn"], sec["schedule"], sec["group"], sec["instructors"]))
            self.classes.append(classTemp)

    def getCombinations(self):
        
        sections = []
        for clasue in self.classes:
            sections.append(clasue.getSections())

        return list(product(*sections))



class AddDropHelper:
    def __init__(self,dataFilename):
        with open(dataFilename, "r") as file:
            self.data = json.loads(file.read())

        self.courses = {}
        for course in self.data["courses"]:
            crsTemp = Course(course["name"],course["code"])
            crsTemp.addClass(course["classes"])
            self.courses[course["code"]] = crsTemp

    def findMatches(self,codes,confLimit = 0):
        schedules = []
        for code in codes:
            for course in list(self.courses.values()):
                if course.code == code:
                    schedules.append(course.getCombinations())

        allPossibs = list(product(*schedules))

        possibleSchedules = []
        for possib in tqdm(allPossibs):
            conCo, sule = self.findConflicts(possib)
            if conCo <= 1 + confLimit:
                possibleSchedules.append({"su":possib,"conf":conCo})
            

        return possibleSchedules


    @property
    def getCourseCodes(self):
        return {"codes":list(self.courses.keys())}

    def saveCRNs(self,possibleSchedules,loc):
        
        modif = {"result":[]}
        for onepossib in possibleSchedules:
            crnList = []
            for classue in onepossib["su"]:
                for section in classue:
                    crnList.append(section.getCRNs())

                onepossib["su"] = crnList
            modif["result"].append(onepossib)

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
    print(help.courses.values())