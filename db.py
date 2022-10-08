import sqlite3

# conn = sqlite3.connect("ESMdb.db")
print("Opened database successfully")

# cur = conn.cursor()
# cur.execute("INSERT INTO 'Depertment' ('Dept') VALUES ('ME')")
# conn = sqlite3.connect("ESMdb.db")
# cur = conn.cursor()
# cur.execute('INSERT INTO "Result"("Std. Roll", "Paper code", "Sem", "Result")VALUES (23, "cse-001", 5, 89);')
# conn.commit()
# conn.close()
def add_result(roll, paper_code, sem, res):
    conn = sqlite3.connect("ESMdb.db")
    cur = conn.cursor()
    cur.execute(f'INSERT INTO "Result"("Std. Roll", "Paper code", "Sem", "Result")VALUES ({roll}, {paper_code}, {sem}, {res});')
    conn.commit()
    conn.close()

def get_stud():
    pass

def get_teacher():
    pass


# conn.commit()
# conn.close()
