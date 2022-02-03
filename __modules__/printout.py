import sys
from colorama import (Fore,Style)

sys.dont_write_bytecode = True

class PRINTOUT:
    def __init__(self):
        self.red = Style.BRIGHT+Fore.RED
        self.green = Style.BRIGHT+Fore.GREEN
        self.blue = Style.BRIGHT+Fore.BLUE
        self.reset_all = Style.RESET_ALL+Fore.RESET
        self.white = Style.BRIGHT+Fore.WHITE
        self.yellow = Style.BRIGHT+Fore.YELLOW
        self.cyan = Style.BRIGHT+Fore.CYAN
        self.magenta = Style.BRIGHT+Fore.MAGENTA
        self.begin = "  "

    def info(self,msg):
        sys.stdout.write(
            self.begin+self.white+"["+self.yellow+"INFO"+self.white+"]: "+msg+self.reset_all+"\n"
        )

    def load(self,msg):
        sys.stdout.write(
            "\r"+self.begin+self.white+"["+self.cyan+"INFO"+self.white+"]: "+msg+self.reset_all
        )
        sys.stdout.flush()

    def error(self,error_msg):
        sys.stdout.write(
            self.begin+self.white+"["+self.red+"ERROR"+self.white+"]: %s"%(error_msg)+self.reset_all+"\n"
        )
    
    def failed(self):
        sys.stdout.write(
            self.red+"FAILED"+self.reset_all+"\n"
        )

    def ok(self):
        sys.stdout.write(
            self.green+"O.K."+self.reset_all+"\n"
        )

    def warning(self,warning_msg):
        sys.stdout.write(
            self.begin+self.white+"["+self.magenta+"WARNING"+self.white+"]: %s"%(warning_msg)+self.reset_all+"\n"
        )

    def yes_but_actually_no(self,msg):
        sys.stdout.write(
            self.begin+self.cyan+msg+self.reset_all+"\n"
        )

    def view(self,title_msg):
        sys.stdout.write(
            "\n"+self.begin+self.cyan+"<"+self.blue+"-----"+self.magenta+title_msg+self.blue+"-----"+self.cyan+">"+self.reset_all+"\n"
        )

    def grade_info(self,text,grade,rounded_grade):
        if (type(grade) == float or type(grade) == int):
            if (rounded_grade >= 13):
                this_color = self.green
            if (rounded_grade >= 10 and rounded_grade < 13):
                this_color = self.cyan
            if (rounded_grade >= 7 and rounded_grade <= 9):
                this_color = self.yellow
            if (rounded_grade >= 4 and rounded_grade <= 6):
                this_color = self.blue
            if (rounded_grade < 4):
                this_color = self.red
        else:
            this_color = self.white
        sys.stdout.write(
            self.begin+self.white+"["+self.green+"+"+self.white+"]: "+text+" = "+this_color+"%s (%s)"%(grade,
            rounded_grade)+self.reset_all+"\n"
        )

    def underpointed_warning(self,subject,msg,rounded_grade):
        sys.stdout.write(
            self.begin+self.white+"["+self.red+"%s"%(subject)+self.white+"]: "+self.red+"%s=> %s"%(rounded_grade,msg)+self.reset_all+"\n"
        )

    def no_under_pointed(self):
        sys.stdout.write(
            self.green+"O.K. (nothing found)"+self.reset_all+"\n"
        )

    def found_underpointed(self,number):
        sys.stdout.write(
            self.red+"FOUND %s"%(number)+self.reset_all+"\n"
        )
