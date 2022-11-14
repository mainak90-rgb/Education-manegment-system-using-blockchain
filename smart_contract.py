import Db

def smart_contract(marks, ec):
    if 100 > marks >= 80 and ec >= 15:
        print("Outstanding academics & outstanding extra-curricular")
    elif 100 > marks >= 80 and ec >= 10:
        print("Outstanding academics & good extra-curricular")
    elif 100 > marks >= 80 and ec >= 5:
        print("Outstanding academics & average extra-curricular")
    elif 100 > marks >= 80 and ec < 5:
        print("Outstanding academics & no extra-curricular")

    if 80 > marks >= 70 and ec >= 15:
        print("Good academics & outstanding extra-curricular")
    elif 80 > marks >= 70 and ec >= 10:
        print("Good academics & good extra-curricular")
    elif 80 > marks >= 70 and ec >= 5:
        print("Good academics & average extra-curricular")
    elif 80 > marks >= 70 and ec < 5:
        print("Good academics & no extra-curricular")

    if 70 > marks >= 25 and ec >= 15:
        print("Average academics & outstanding extra-curricular")
    elif 70 > marks >= 25 and ec >= 10:
        print("Average academics & good extra-curricular")
    elif 70 > marks >= 25 and ec >= 5:
        print("Average academics & average extra-curricular")
    elif 70 > marks >= 25 and ec < 5:
        print("Average academics & no extra-curricular")

    else:
        print("Backlog")


if __name__ == '__main__':
    id = input("enter your student id")
    # marks = Db.find_one(post={'id': id, 'type': 'Marks'}, collection="Student_record")
    smart_contract(60, 25)
