from tkinter import *
import pymysql
from tkinter import messagebox
import re
import time
# from datetime import datetime
# from datetime import timedelta
from datetime import *
from dateutil import parser
import string
import time
from tkinter import ttk
import sys
import random
import collections

class Queries:


    def connect(self):
        try:
            return pymysql.connect(host='academic-mysql.cc.gatech.edu',passwd = 'SD8el4Qq', user = 'cs4400_Team_32', db='cs4400_Team_32')
        except:
            print('Connection Error')
            #messagebox.showerror("Connection Error", "Cannot connect to the database. Please check your internect conneciton!")
    # =========================================================================================
    # |                                Query for student users                                      |
    # =========================================================================================
    # Login a user
    # Return a boolean telling if the user is logged in successfully
    def validateLogin(self, db, username, password):
        # db = connect()
        if db != None:
            cursor = db.cursor()
            sql = "SELECT UserType FROM User WHERE Username = %s AND Password = %s "
            cursor.execute(sql, (username, password))
            c = cursor.fetchall()
            cursor.close()
            if len(c) != 0:
                #messagebox.showinfo('Verified','You logged in successfully.')
                if c[0][0]=='Admin':
                    return 1
                elif c[0][0]=='Student':
                    return 2
                else:
                    return 0
            else:
                print('No matched user')
                return 0
                #messagebox.showerror('ERROR', 'Invalid username or password')

        # Database:
        # A. Get user's username + password for login

        # Validate:
        # A. if the username exists
        # B. if the username and password match a record in the database
        # C. To be continued

    # Register a user
    # Return a boolean if a user is registered
    def registerUser(self, db, username, password, reentered_password, gt_email):
        # Validate:
        # A. if the username already exists. If yes, show error
        # B. if the password and the reentered_password match

        # Then insert new user tuple into database

        # db=connect()
        if db!= None:
            if username=='' or password=='' or reentered_password=='' or gt_email=='':
                return 0     #messagebox.showerror('ERROR','Fill the required information')
            if password != reentered_password:
                return 1     #messagebox.showerror('ERROR','Passwords do not match')
            if '@gatech.edu' not in gt_email:
                return 2     #messagebox.showerror('ERROR','Please enter a valid GT email')
            cur=db.cursor()
            sql= "SELECT Email FROM User WHERE Email = %s "
            cur.execute(sql,gt_email)
            email=cur.fetchall()
            cur=db.cursor()
            sql="SELECT Username FROM User WHERE Username = %s"
            cur.execute(sql,username)
            user=cur.fetchall()
            cur.close()
            if len(email)!=0:
                return 3     #messagebox.showerror('ERROR','Email already exsits, enter a different email')
            if len(user)!=0:
                return 4     #messagebox.showerror('ERROR','Usename already exsits, enter a different username')
            cur=db.cursor()
            sql="INSERT INTO User (Username, Password, Email, UserType) VALUES (%s, %s, %s, %s)"
            cur.execute(sql,(username,password, gt_email, 'Student'))
            sql="INSERT INTO Student (Username, Major, Year) VALUES (%s, %s, %s)"
            cur.execute(sql,(username,None,None))
            cur.close()
            db.commit()
            db.close()
            return 5 #messagebox.showinfo('Info','You are successfully registered')

    # Get all projects names and course (numbers + names)
    def get_projects(self, db):
        # db=connect()
        if db!= None:
            cur=db.cursor()
            sql= """SELECT Project.ProjName, Project.DesignationName,Project_Major_Require.Major, Project_Year_Require.Year, Project_Dept_Require.Dept, Project_is_category.Category_name
                    FROM  `Project`
                    LEFT JOIN Project_Major_Require ON Project.ProjName = Project_Major_Require.Pname
                    LEFT JOIN Project_Year_Require ON Project.ProjName = Project_Year_Require.Pname
                    LEFT JOIN Project_Dept_Require ON Project.ProjName = Project_Dept_Require.Pname
                    LEFT JOIN Project_is_category ON Project.ProjName = Project_is_category.Project_name
                    LIMIT 0 , 30000000000 """
            cur.execute(sql)
            Project=cur.fetchall()
            cur.close()
            db.close()
            #for p in Project:
            #    print(p)
            return Project
    def get_course(self, db, name):
        if db!= None:
            cur=db.cursor()
            sql= """SELECT Course.Name, Course.Instructor, Course.EstNoStudents, Course.Designation_name, Course_is_category.Category_name
                 FROM Course
                 LEFT JOIN Course_is_category ON Course.Name = Course_is_category.Course_name
                 Where Course.Name = %s
                 LIMIT 0 , 30000000000 """
            cur.execute(sql, name)
            Course=cur.fetchall()
            cur.close()
            db.close()
        #for p in Course:
        #    print(p)
            return Course

    def get_courses(self, db):
        if db!= None:
            cur=db.cursor()
            sql= """SELECT Course.Name, Course.Designation_name, Course_is_category.Category_name
                 FROM Course
                 LEFT JOIN Course_is_category ON Course.Name = Course_is_category.Course_name
                 LIMIT 0 , 30000000000 """
            cur.execute(sql)
            Course=cur.fetchall()
            cur.close()
            db.close()
        #for p in Course:
        #    print(p)
            return Course
    # Get applications of the user that's currently logged in
    # Should return application Date, Project Name, and Status from DB
    def get_my_apps(self, db, username):
        print (username)
        if db!= None:
            cur=db.cursor()
            sql= """SELECT Project_name,Date,Status
                    FROM Apply
                    Where Student_name= %s
                    LIMIT 0 , 30000000000 """
            cur.execute(sql,username)
            Apply=cur.fetchall()
            cur.close()
            db.close()
            #for p in Course:
            #    print(p)
            return Apply
    # Edit profile
    # Needs 2 methods
    # 1. update user's major in DB
    def change_major(self, db, username, major_name):
        if db!= None:
            cur=db.cursor()
            sql= """UPDATE  cs4400_Team_32.Student SET  Major =  %s WHERE Student.Username =  %s """
            cur.execute(sql,(major_name,username))
            cur.close()
            db.commit()
            db.close()

    # 2. update user's year in DB
    def change_year(self, db, username, year):
        if db!= None:
            cur=db.cursor()
            sql= """UPDATE  cs4400_Team_32.Student SET  Year =  %s WHERE Student.Username =  %s """
            cur.execute(sql,(year,username))
            cur.close()
            db.commit()
            db.close()


    # View Project Details
    # shoule return Advisor, Description, Designation, Category, Requirements, and Estimated No. of Students
    def view_project(self, db, project_name):
        if db!= None:
            cur=db.cursor()
            sql= """SELECT Project.AdvisorName,Project.AdvisorEmail,Project.Description,Project.DesignationName,Project_is_category.Category_name,Project_Major_Require.Major, Project_Year_Require.Year, Project_Dept_Require.Dept,Project.EstNoStudent
                    FROM  `Project`
                    LEFT JOIN Project_Major_Require ON Project.ProjName = Project_Major_Require.Pname
                    LEFT JOIN Project_Year_Require ON Project.ProjName = Project_Year_Require.Pname
                    LEFT JOIN Project_Dept_Require ON Project.ProjName = Project_Dept_Require.Pname
                    LEFT JOIN Project_is_category ON Project.ProjName = Project_is_category.Project_name
                    WHERE Project.ProjName= %s
                    LIMIT 0 , 30000000000 """
            cur.execute(sql,project_name)
            Project=cur.fetchall()
            cur.close()
            db.close()
            #for p in Project:
            #    print(p)
            return Project
    # # Apply for a project
    # # Insert a new tuple (username, project_name) in Apply entity representing an application being created
    # def apply_project(username, project_name):
    #     # Should check major, year, and department restrictions before inserting

    # # View course details
    # # Should return Course Name, Instructor, Designation, Category, and Estimated Number of Students.
    # def view_course(course_name):

    def get_all_major(self, db):
        if db != None:
            cursor = db.cursor()
            sql = 'SELECT Name FROM Major'
            cursor.execute(sql)
            majorList = []
            for record in cursor:
                majorList.append(record[0])
            cursor.close()
            db.close()
            return majorList

    def apply_project(self, db, username, project_name):
        if db!= None:
        # Should check major, year, and department restrictions before inserting
            Project=self.view_project(db, project_name)
            db = self.connect()
            cur = db.cursor()
            sql="""INSERT INTO Apply (Project_name,Student_name, Date,Status) VALUES (%s, %s, %s, %s)"""
            cur.execute(sql,(project_name,username,datetime.today().date(),'pending'))
            cur.close()
            db.commit()
            db.close()

    def check_app_reject(self, username, project_name):
        #Major check
        db = self.connect()
        cur = db.cursor()
        sql="SELECT Major FROM Project_Major_Require WHERE Pname=%s"
        cur.execute(sql,project_name)
        major=cur.fetchall()
        sql="SELECT Major FROM Student WHERE Username=%s"
        cur.execute(sql,username)
        Smajor=cur.fetchall()
        if len(major)!=0:
            if major[0][0]!=Smajor[0][0]:
                self.reject_app(project_name, username)
                cur.close()
                db.close()
                return
        #Year check
        sql="SELECT Year FROM Project_Year_Require WHERE Pname=%s"
        cur.execute(sql,project_name)
        year=cur.fetchall()
        sql="SELECT Year FROM Student WHERE Username=%s"
        cur.execute(sql,username)
        Syear=cur.fetchall()
        if len(year)!=0:
            if year[0][0]!=Syear[0][0]:
                self.reject_app(project_name, username)
                cur.close()
                db.close()
                return
        #Dept check
        sql="SELECT Dept FROM Project_Dept_Require WHERE Pname=%s"
        cur.execute(sql,project_name)
        dept=cur.fetchall()
        sql="""SELECT Major.Dept_name
            FROM Student
            NATURAL JOIN Major
            WHERE Username =  %s
            AND Major.name = Student.Major"""
        cur.execute(sql,username)
        Sdept=cur.fetchall()
        if len(dept)!=0:
            if dept[0][0]!=Sdept[0][0]:
                self.reject_app(project_name, username)
                cur.close()
                db.close()
                return
        cur.close()
        db.close()

    def reject_app(self, project_name, username):
        db = self.connect()
        cursor = db.cursor()
        status = 'rejected'
        sql = 'UPDATE Apply SET Status = %s WHERE Project_name = %s AND Student_name = %s'
        cursor.execute(sql, (status, project_name, username))
        cursor.close()
        db.commit()
        db.close()

    def approve_app(self, project_name, username):
        db = self.connect()
        cursor = db.cursor()
        status = 'accepted'
        sql = 'UPDATE Apply SET Status = %s WHERE Project_name = %s AND Student_name = %s'
        cursor.execute(sql, (status, project_name, username))
        cursor.close()
        db.commit()
        db.close()

    # # =========================================================================================
    # # |                                Query for admin users                                      |
    # # =========================================================================================

    # Add project
    # def add_project(project_name, advisor, advisor_email, description, category, designation,
    #                     estimated_no_students, major_requirement, year_requirement, department_requirement):
    #     # insert a new project tuple

    def add_project(self, db, project_name, advisor, advisor_email, description, categories, designation, 
                    estimated_no_students, major_requirement, year_requirement, department_requirement):
        # db = connect()
        cursor = db.cursor()
        sql_one = 'INSERT INTO Project (ProjName, Description, AdvisorEmail, AdvisorName, EstNoStudent, DesignationName) VALUES (%s, %s, %s, %s, %s, %s)'
        cursor.execute(sql_one, (project_name, description, advisor_email, advisor, estimated_no_students, designation))
        for cat in categories:
            sql_two = 'INSERT INTO Project_is_category VALUES (%s, %s)'
            cursor.execute(sql_two, (project_name, cat))
        sql_three = 'INSERT INTO Project_Year_Require (Pname, Year) VALUES (%s, %s)'
        sql_four = 'INSERT INTO Project_Major_Require (Pname, Major) VALUES (%s, %s)'
        sql_five = 'INSERT INTO Project_Dept_Require (Pname, Dept) VALUES (%s, %s)'

        if year_requirement != '' and major_requirement != '' and department_requirement != '':
            cursor.execute(sql_three, (project_name, year_requirement))
            cursor.execute(sql_four, (project_name, major_requirement))
            cursor.execute(sql_five, (project_name, department_requirement))
            cursor.close()
            db.commit()
            db.close()
        elif year_requirement != '' and major_requirement != '' and department_requirement == '':
            cursor.execute(sql_three, (project_name, year_requirement))
            cursor.execute(sql_four, (project_name, major_requirement))        
            cursor.close()
            db.commit()
            db.close()
        elif year_requirement != '' and department_requirement != '' and major_requirement == '':
            cursor.execute(sql_three, (project_name, year_requirement))        
            cursor.execute(sql_five, (project_name, department_requirement))
            cursor.close()
            db.commit()
            db.close()
        elif major_requirement != '' and department_requirement != '' and year_requirement == '':
            cursor.execute(sql_four, (project_name, major_requirement))
            cursor.execute(sql_five, (project_name, department_requirement))        
            cursor.close()
            db.commit()
            db.close()
        elif year_requirement != '' and major_requirement == '' and department_requirement == '':
            cursor.execute(sql_three, (project_name, year_requirement))        
            cursor.close()
            db.commit()
            db.close()
        elif major_requirement != '' and year_requirement == '' and department_requirement == '':
            cursor.execute(sql_four, (project_name, major_requirement))
            cursor.close()
            db.commit()
            db.close()
        elif department_requirement != '' and major_requirement == '' and year_requirement == '':
            cursor.execute(sql_five, (project_name, department_requirement))
            cursor.close()
            db.commit()
            db.close()
        elif year_requirement == '' and major_requirement == '' and department_requirement == '':
            #messagebox.showerror('You Must Enter At Least One Requirement For Project!!!')
            pass

    def find_dept(self, db, major_name):
        dept_name = []
        # db = connect()
        cursor = db.cursor()
        sql = 'SELECT Dept_name FROM Major WHERE Name = %s'
        cursor.execute(sql, major_name)
        cursor.close()
        db.close()
        for record in cursor:
            dept_name.append(record[0])
        return dept_name[0]

    def get_student_info(self, db, username):
        student_info = []
        # db = connect()
        cursor1 = db.cursor()
        sql_one = 'SELECT * FROM User WHERE Username = %s'
        cursor1.execute(sql_one, username)
        for record in cursor1:
            student_info.append(record[0])
            student_info.append(record[1])
            student_info.append(record[2])
            student_info.append(record[3])
        cursor1.close()
        cursor2 = db.cursor()
        sql_two = 'SELECT Major, Year FROM Student WHERE Username = %s'
        cursor2.execute(sql_two, username)
        for record in cursor2:
            student_info.append(record[0])
            student_info.append(record[1])
        cursor2.close()
        db.close()
        return student_info

    def get_all_dept(self, db):
        # db = connect()
        cursor = db.cursor()
        sql = 'SELECT DISTINCT Name FROM Depatment'
        cursor.execute(sql)
        deptList = []
        for record in cursor:
            deptList.append(record[0])
        cursor.close()
        db.close()
        return deptList

    def get_application_info(self, db):
        application_info = []
        # db = connect()
        cursor = db.cursor()
        sql = 'SELECT Apply.Project_name, Apply.Status, Student.Major, Student.Year, Student.Username FROM Apply INNER JOIN Student ON Apply.Student_name = Student.Username'
        cursor.execute(sql)
        for record in cursor:
            application_info.append(record)
        return application_info

    def add_course(self, db, course_number, course_name, instructor, designation, estimated_no_students, categories):
        # db = connect()
        cursor = db.cursor()
        sql_one = 'INSERT INTO Course (Name, Course_number, Instructor, EstNoStudents, Designation_name) VALUES (%s, %s, %s, %s, %s)'
        cursor.execute(sql_one, (course_name, course_number, instructor, estimated_no_students, designation))
        for c in categories:
            sql_two = 'INSERT INTO Course_is_category (Course_name, Category_name) VALUES (%s, %s)'
            cursor.execute(sql_two, (course_name, c))
        cursor.close()
        db.commit()
        db.close()

    def get_top_project(self, db):
        project_list = []
        # db = connect()
        cursor = db.cursor()
        sql = 'SELECT Project_name ,COUNT(Project_name) FROM Apply GROUP BY Project_name ORDER BY COUNT(Project_name) DESC '
        cursor.execute(sql)
        return cursor.fetchall()




    def report_num_app(self, Pname):
        db=self.connect()
        cursor = db.cursor()
        sql = 'SELECT COUNT(Project_name) FROM Apply GROUP BY Project_name HAVING Project_name=%s'
        cursor.execute(sql,Pname)
        num=cursor.fetchall()
        if len(num)==0:
            num=0
        else:
            num=num[0][0]
        cursor.close()
        db.close()
        return num

    def report_rate(self, Pname):
        db=self.connect()
        cursor = db.cursor()
        sql = """SELECT COUNT( Project_name )
                 FROM Apply
                 WHERE STATUS =  %s
                 GROUP BY Project_name
                 HAVING Project_name =  %s"""
        cursor.execute(sql,('rejected',Pname))
        num=cursor.fetchall()
        if len(num)==0:
            num=0
        else:
            num=num[0][0]
        base=self.report_num_app(Pname)
        if base==0:
            rate=0
        else:
            rate=(base-num)/base
        cursor.close()
        db.close()
        return rate
    def report_top_major(self, Pname):
        db=self.connect()
        cursor = db.cursor()
        sql = """SELECT Student.Major
               FROM Apply, Student
               WHERE Apply.Student_name = Student.Username
               AND Apply.Project_name =  %s
               GROUP BY Student.Major
               ORDER BY COUNT( Student.Major ) DESC
               LIMIT 0 , 3"""
        cursor.execute(sql,Pname)
        major=cursor.fetchall()
        top=''
        for m in major:
            top=top+m[0]+', '
        cursor.close()
        db.close()
        return top[:-2]
    def app_report(self):
        db=self.connect()
        cursor = db.cursor()
        sql = """SELECT  Project_name
                 FROM Apply
                 GROUP BY Project_name
                 """
        cursor.execute(sql)
        Pname=cursor.fetchall()
        result=[]
        temp=[]
        for p in Pname:
            temp.append(p[0])
            temp.append(self.report_num_app(p[0]))
            temp.append(self.report_rate(p[0]))
            temp.append(self.report_top_major(p[0]))
            result.append(temp)
            temp=[]
        cursor.close()
        db.close()
        return result
        #student_info list order: username, password, email, usertype, major, year
    # # Add a course
    # def add_course(course_number, course_name, instructor, designation, category):
    #     # insert a new course tuple

    # # Approve application
    # def approve_app(project_name, username):
    #     # change the status of a project to "Approved"

    # # Reject application
    # def reject_app(project_name, username):
    #     # change the status of a project to "Rejected"
