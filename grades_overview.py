"""
Notenübersicht <FOS/BOS>
Pulsar
03.02.2022
> Python-Version: 3.8.2
"""
"""
Notenübersicht <FOS/BOS>
Benedikt Fichtner
"""
import sys,os,math,csv,platform
from cv2 import edgePreservingFilter
import pandas as pd
sys.dont_write_bytecode = True
from __modules__ import printout

class VISUALISATION:
    def __init__(self,file_path,p):
        self.file_path = file_path
        self.p = p
        self.status = True
        self.data = {
            "anzahl_noten_insgesamt": 0,
            "fächer": {},
            "overall_grade_average": "None",
            "overall_grade_average_rounded": "None"
        }

    def get_grades_data(self,fach,args_string,grade_type):
        if ("[" in args_string and "]" in args_string):
            argumente_a = args_string.split('[')
            argumente_b = argumente_a[1].split(']')[0]
            if (";" in argumente_b):
                grades = argumente_b.split(';')
                for grade in grades:
                    if (grade.lower() != "none" and grade != "" and grade != " "):
                        self.data['fächer'][fach][grade_type].append(
                            int(grade))
                        self.data['anzahl_noten_insgesamt'] += 1
                    else:
                        pass
            else:
                self.status = False
                self.p.failed(),self.p.error("Missing statement ';'(%s/%s)"%(
                    fach,grade_type))
        else:
            self.status = False

    def get_data(self):
        #Fach,Schulaufgaben,Kurzarbeiten,Mündlich

        self.p.load("Loading data from ({})...".format(self.file_path))
        try:
            with open(self.file_path, 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if (len(row) >= 3):
                        fach = row[0]
                        self.data['fächer'][fach] = {
                            "schulaufgaben": [],
                            "kurzarbeiten": [],
                            "mündlich": [],
                            "grade_average": None,
                            "grade_average_rounded": None
                        }
                        sa_string = row[1] #Schulaufgaben (SA)
                        self.get_grades_data(fach,
                            args_string=sa_string,
                            grade_type="schulaufgaben"
                        )
                        ka_string = row[2] #Kurzarbeiten (KA)
                        self.get_grades_data(fach,
                            args_string=ka_string,
                            grade_type="kurzarbeiten"
                        )
                        mu_string = row[3] #Mündlich (MU)
                        self.get_grades_data(fach,
                            args_string=mu_string,
                            grade_type="mündlich"
                        )
            if (self.data['anzahl_noten_insgesamt'] == 0):
                self.status = False
                self.p.yes_but_actually_no("0 grades")
        except Exception as error:
            self.p.failed(),self.p.error(error)
            self.status = False

    def run(self):
        self.get_data()
        if (self.status == True):
            self.p.ok()
            self.p.info("{} school grades are available".format(
                self.data['anzahl_noten_insgesamt']
            ))
            if (self.data['anzahl_noten_insgesamt'] < 3):
                self.p.warning("Not enough data available!")
            else:
                self.calculate_average_grade()
                self.calculate_overall_grade_average()
                self.check_under_pointed()
                self.print_all_data()
        else:
            self.p.failed()
            self.p.error("No data")
        self.p.info("Closed")

    def check_under_pointed(self):
        underpointed_subjects = {}
        self.p.load("Check for under-pointed subjects...")
        state = True
        for fach in self.data['fächer']:
            try:
                r_grade_average = self.data['fächer'][fach]['grade_average_rounded']
                if (r_grade_average != None):
                    if (r_grade_average < 4):
                        underpointed_subjects[fach] = r_grade_average
            except Exception as error:
                self.p.failed(),self.p.error(error)
                state = False
                break
        if (state == True):
            if (len(underpointed_subjects) == 0):
                self.p.no_under_pointed()
            else:
                self.p.found_underpointed(len(underpointed_subjects))
                for subject in underpointed_subjects:
                    self.p.underpointed_warning(
                        subject,
                        "WARNING!",
                        underpointed_subjects[subject]
                    )
        else:
            self.p.failed()

    def print_all_data(self):
        self.p.view("Grade average from subjects")
        for fach in self.data['fächer']:
            self.p.grade_info(
                "Grade average in %s"%(fach),
                self.data['fächer'][fach]['grade_average'],
                self.data['fächer'][fach]['grade_average_rounded']
            )
        self.p.view("Overall grade average")
        self.p.grade_info("Overall",self.data['overall_grade_average'],
            self.data['overall_grade_average_rounded']
        )
        self.p.view("Overview")
        print("")
        subjects_data = {}
        subjects_data = self.data['fächer']
        for fach in self.data['fächer']:
            del subjects_data[fach]['grade_average']
        df = pd.DataFrame(self.data['fächer'])
        print(df)
        print("")

    def calculate_average_grade(self):
        for fach in self.data['fächer']:
            self.p.load("Calculate average grade of '{}'...".format(fach))
            try:
                (
                    grade_average,ka_counter,ka_summ,mu_counter,
                    mu_summ,sa_counter,sa_summ,ka_mu_grade_average
                ) = (
                    0,0,0,0,0,0,0,0
                )
                #Kurzarbeiten
                for kurzarbeit in self.data['fächer'][fach]['kurzarbeiten']:
                    ka_counter += 2
                    ka_summ += (kurzarbeit*2)
                #Mündlich
                for mündlich in self.data['fächer'][fach]['mündlich']:
                    mu_counter += 1
                    mu_summ += mündlich
                ka_mu_grade_average = ((ka_summ+mu_summ)/(ka_counter+mu_counter))
                #Schulaufgaben
                for schulaufgabe in self.data['fächer'][fach]['schulaufgaben']:
                    sa_counter += 1
                    sa_summ += schulaufgabe
                if (ka_summ != 0 and mu_summ != 0 and sa_summ != 0):
                    grade_average = ((ka_mu_grade_average+sa_summ)/(2))
                else:
                    grade_average = ka_mu_grade_average
                self.data['fächer'][fach]['grade_average'] = grade_average
                self.data['fächer'][fach]['grade_average_rounded'] = round(
                    grade_average
                )
                self.p.ok()
            except Exception as error:
                self.p.failed()#self.p.error(error)

    def calculate_overall_grade_average(self):
        self.p.load("Calulate overall grade average...")
        try:
            (subjects_number,p) = (0,0.0)
            for fach in self.data['fächer']:
                subjects_number += 1
                grade_average = self.data['fächer'][fach]['grade_average']
                if (grade_average != None):
                    p += grade_average
            n = subjects_number
            overall_grade_average = (p/n)
            self.data['overall_grade_average'] = overall_grade_average
            self.data['overall_grade_average_rounded'] = round(overall_grade_average)
            self.p.ok()
            self.p.info(f"{n} Subjects")
        except Exception as error:
            self.p.failed(),self.p.error(error)

#
if (platform.system() == "Windows"):
    os.system("cls")
else:
    os.system("clear")
p = printout.PRINTOUT()
p.info("OS: %s"%(platform.system()))
if (len(sys.argv) < 2):
    p.error("Not enough arguments!")
    p.info("Syntax: python(3) [app].py [CSV-File-Path]")
    sys.exit()
else:
    file_path = sys.argv[1]
    p.info(f"CSV-File: {file_path}")
#

if (__name__ == '__main__'):
    visualisation = VISUALISATION(file_path,p)
    visualisation.run()
