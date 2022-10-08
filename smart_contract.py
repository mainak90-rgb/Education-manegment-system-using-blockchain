mar_points = 0


class smart_contract:
    def __init__(self):
        self.grades = {
            30: "F",
            40: "E",
            50: "D",
            60: 'C',
            70: "B",
            80: "A",
            90: "O",
            100: "E"
        }
        self.ECA = {
            "Blood donation": 10,
            "inter college sports activity": 5,
            "Participation in webiner": 2,
            "college activity": 5,
            "Participation in quiz contest": 10
        }

    def MAR(self, activity):
        if activity not in self.ECA:
            return "Invalid activity"
        global mar_points
        mar_points += self.ECA[activity]
        return mar_points

    def grading(self, marks):
        for k in self.grades.keys():
            if marks > 100 or marks < 0:
                return "Invalid marks"
            if marks <= k:
                return self.grades[k]


def records(id, type=None, marks=None, ECA=None):
    if id != "Student":
        return
    if not type or type not in ("ECA", "Marks"):
        return
    sc = smart_contract()
    if type == "Marks" and marks:
        return sc.grading(marks)
    if type == "ECA" and ECA:
        return sc.grading(ECA)
    return
