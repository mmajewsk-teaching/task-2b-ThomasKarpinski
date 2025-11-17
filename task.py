# Class diary
#
# Create program for handling lesson scores.
# Use python to handle student (highscool) class scores, and attendance.
# Make it possible to:
# - Get students total average score (average across classes)
# - get students average score in class
# - hold students name and surname
# - Count total attendance of student
#
# Please, use your imagination and create more functionalities.
# Your project should be able to handle entire school(s?).
# If you have enough courage and time, try storing (reading/writing)
# data in text files (YAML, JSON).
# If you have even more courage, try implementing user interface (might be text-like).
#
#Try to expand your implementation as best as you can. 
#Think of as many features as you can, and try implementing them.
#Make intelligent use of pythons syntactic sugar (overloading, iterators, generators, etc)
#Most of all: CREATE GOOD, RELIABLE, READABLE CODE.
#The goal of this task is for you to SHOW YOUR BEST python programming skills.
#Impress everyone with your skills, show off with your code.
#
#Your program must be runnable with command "python task.py".
#Show some usecases of your library in the code (print some things)
#
#When you are done upload this code to your github repository. 
#
#Delete these comments before commit!
#Good luck.

class Diary:
    def __init__(self, students):
        self.students = students
        number_of_students_school = 0
        
        

class ClassOfStudents():
    def __init__(self, class_name):
        self.class_name = class_name
        

class Student:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
    
    def average_grade_subject(self):
        pass

class Subject:
    def __init__(self, name_of_sub, coordinator):
        self.name_of_sub = name_of_sub
        self.coordinator = coordinator

class Mark:
    def __init__(self, value, subject, student_name, student_surname):
        self.value = value
        self.subject = subject
        self.stydent_name = student_name
        self.student_surname = student_surname


mark1 = Mark(5.0, "Python", "Thomas", "Karpinski")
print(mark1.value)

student1 = Student("Thomas", "Karpinski")