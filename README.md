# School-Grade-Overview

A python-script is reading the csv file and calculates the grade average of each school subject. It also calculates the overall grade average.
At the end the programm will display the school grades and the calculated data.

# CSV-File

The data, which you have to insert in the csv-file is seperated with these arguments:

> Fach,Schulaufgaben,Kurzarbeiten,Mündlich

__Here is an example:__
    
    Mathematik,[10;9],[7;9];[5;]
    
1. The subject-name is: *Mathematik*
2. The '*Schulaufgaben*'-grades are: 10 (Points) and 9 (Points)
3. The '*Kurzarbeiten*'-grades are: 7 (Points) and 9 (Points)
4. The '*Mündlich*'-grades are: 5 (Points) and None (Points)

__When you let something empty `(like this: [5;] or [;])`  it means, that it exists only one grade or none.__


# Requirements

    pip install -r requirements.txt


# Executing

    python3 [app_name].py [csv-file-path]
