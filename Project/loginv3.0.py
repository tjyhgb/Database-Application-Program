__author__ = 'RichardWang'

from tkinter import *
import pymysql
from tkinter import messagebox
import re
import time
# from datetime import datetime
# from datetime import timedelta
from datetime import *
from dateutil import parser
import random
import string
import time
from tkinter import ttk
import sys
import random
from Queries import *
from operator import itemgetter

class Courses_n_Projects:
    def __init__(self, rootWindow):
        self.window = rootWindow
        self.loginWindow = self.window
        # self.connectWindow = self.window

        self.login_show()
        self.count_main_items = 0
        self.detached_dict = {}
        self.detached_dict["Projects"] = []
        self.detached_dict["Courses"] = []
        self.detached = []  # keep track of all detached items
        self.user_logged_in = []
        self.catStrListAddCourse = []
        self.catStrListAddProject = []
        self.catStrList = []
        self.databaseHandler = Queries()
    # ================================================================================================================================
    # |															User View														     |
    # ================================================================================================================================
    def login_show(self):

        self.loginWindow.title("SLS")
        loginLabel = Label(self.loginWindow, text="Login", font="Verdana 20 bold")
        loginLabel.grid(row=0, column=0, columnspan=2, pady=10, sticky=EW)

        usernameL = Label(self.loginWindow, text="Username")
        usernameL.grid(row=1, column=0, padx=40, pady=10, sticky=W)

        pwL = Label(self.loginWindow, text="Password")
        pwL.grid(row=2, column=0, padx=40, pady=10, sticky=W)

        self.usernameLogIn = StringVar()
        self.passwordLogIn = StringVar()

        self.usernameENT = Entry(self.loginWindow, textvariable=self.usernameLogIn)
        self.usernameENT.grid(row=1, column=1, padx=30, pady=10, sticky=EW)

        self.pwENT = Entry(self.loginWindow, textvariable=self.passwordLogIn, show="*")
        self.pwENT.grid(row=2, column=1, padx=30, pady=10, sticky=EW)

        loginBTN = Button(self.loginWindow, text="Login", command=self.login, width=10)
        loginBTN.grid(row=3, column=0, padx=100, pady=5, sticky=EW, columnspan=2)

        registerBTN = Button(self.loginWindow, text="Register", command=self.registerBTNClicked, width=10)
        registerBTN.grid(row=4, column=0, padx=100, pady=5, sticky=EW, columnspan=2)

        cancelBTN = Button(self.loginWindow, text="Cancel", command=self.cancelLogin, width=10, fg="red")
        cancelBTN.grid(row=5, column=0, padx=100, pady=5, sticky=EW, columnspan=2)

        buzzImage = PhotoImage(file='buzz.gif')
        panel = Label(self.loginWindow, image=buzzImage)
        panel.photo = buzzImage
        panel.grid(row=6, column=1, padx=10, pady=10, sticky=E)

    def goToMain(self, fromWhere):
        if fromWhere == 1:

            self.loginWindow.withdraw()
            displayName = self.usernameLogIn.get()
        if fromWhere == 0:
            self.registerWin.withdraw()
            displayName = self.regUsername.get()

        self.mainPage = Toplevel()

        self.mainPage.title("Main Page")
        self.num_cate = 0
        # Picture on the top left corner

        backBTN = Button(self.mainPage, text="Log Out", command=self.logOut, fg="red")
        backBTN.grid(row=0, column=0, padx=20, pady=20, sticky=E + W)

        self.photo = PhotoImage(file="User.gif")

        picture = Button(self.mainPage, image=self.photo, command=self.myProfile)
        # picture.photo = photo
        picture.grid(row=0, column=1, padx=20, pady=20, sticky=E + W + N + S)

        pageLB = Label(self.mainPage, text=displayName, font="Verdana 20 bold")
        pageLB.grid(row=0, column=2, padx=20, pady=20)

        titleLB = Label(self.mainPage, text="Title")
        titleLB.grid(row=1, column=0, padx=20, pady=5, sticky=E)

        designationLB = Label(self.mainPage, text="Designation")
        designationLB.grid(row=2, column=0, padx=20, pady=5, sticky=E)

        majorLB = Label(self.mainPage, text="Major")
        majorLB.grid(row=3, column=0, padx=20, pady=5, sticky=E)

        yearLB = Label(self.mainPage, text="Year")
        yearLB.grid(row=4, column=0, padx=20, pady=5, sticky=E)

        categoryLB = Label(self.mainPage, text="Category")
        categoryLB.grid(row=1, column=2, padx=20, pady=5, sticky=W)

        self.titleMain = StringVar()
        titleENT = Entry(self.mainPage, textvariable=self.titleMain, width=20)
        titleENT.grid(row=1, column=1, sticky=E + W, padx=20, pady=5)

        # Category DropDown
        self.catStr = StringVar()
        self.catStr.set("Please Select a Category")
        # catOptions = ["Computing for Good", "Doing Good for Your Neighborhood"]

        catOptions = ["computing for good", "doing good for your neighborhood", "reciprocal teaching and learning",
                      "urban development", "adaptive learning", "technology for social good", "sustainable communities",
                      "crowd-sourced", "collaborative action"]
        catDropDown = OptionMenu(self.mainPage, self.catStr, *catOptions)
        catDropDown.config(width=30)
        catDropDown.grid(row=1, column=3, padx=20, pady=5, sticky=W + E)
        self.catStrList.append(self.catStr)

        # Designation DropDown
        self.dsgStr = StringVar()
        self.dsgStr.set("Please Select a Designation")
        dsgOptions = ["Sustainable Communities", "Community"]
        desigDropDown = OptionMenu(self.mainPage, self.dsgStr, *dsgOptions)
        desigDropDown.grid(row=2, column=1, padx=20, pady=5, sticky=W + E)

        # Major Drop Down
        try:
            db = self.connect()
        except:
            messagebox.showinfo('Cannot Connect', 'Please check your internet connection!')
            return
        all_majors = self.databaseHandler.get_all_major(db)
        # print (all_majors)
        self.mjrStr = StringVar()
        self.mjrStr.set("Please Select a Major")
        mjrOptions = all_majors
        mjrDropDown = OptionMenu(self.mainPage, self.mjrStr, *mjrOptions)
        mjrDropDown.grid(row=3, column=1, padx=20, pady=5, sticky=W + E)

        # Year Drop Down
        self.yrStr = StringVar()
        self.yrStr.set("Please Select a Year")
        yrOptions = ["Freshman", "Sophormore", "Junior", "Senior"]
        yrDropDown = OptionMenu(self.mainPage, self.yrStr, *yrOptions)
        yrDropDown.grid(row=4, column=1, padx=20, pady=5, sticky=W + E)

        self.selectType = IntVar()
        self.selectType.set(1)

        self.projRadBTN = Radiobutton(self.mainPage, text="    Project   ", variable=self.selectType, value=1)
        self.projRadBTN.grid(row=4, column=2)

        self.courseRadBTN = Radiobutton(self.mainPage, text="    Course    ", variable=self.selectType, value=2)
        self.courseRadBTN.grid(row=4, column=3)

        self.bothRadBTN = Radiobutton(self.mainPage, text="    Both    ", variable=self.selectType, value=3)
        self.bothRadBTN.grid(row=4, column=4)

        self.appFilter = Button(self.mainPage, text="Apply Filter", command=self.applyFilter, width=10)
        self.appFilter.grid(row=5, column=3, padx=20, pady=10, sticky=E)

        self.resFilter = Button(self.mainPage, text="Reset Filter", command=self.resetFilter, width=10)
        self.resFilter.grid(row=5, column=4, padx=20, pady=10, sticky=E)

        self.select = Button(self.mainPage, text="View", command=self.selectProjCourse, width=10)
        self.select.grid(row=6, column=4, padx=20, pady=10)

        self.treeview = ttk.Treeview(self.mainPage, show="headings")
        self.treeview['columns'] = ("Name", "Type")
        self.treeview.column("Name", width=400)
        self.treeview.heading("Name", text="Name")

        self.treeview.column("Type", width=20)
        self.treeview.heading("Type", text="Type")

        self.treeview.heading("#0", text="Cnt", anchor='center')
        self.treeview.column("#0", minwidth=5, width=5)

        # Query the database to get Course and Project information to be displayed in treeview
        # This is only the place where the view gets updated
        # Always call the query to get Course/Project to make data consistent when new Course/Project is added into the database
        # treeview.insert("Name", 0, ) # Place holders for now
        # treeview.insert("" , 0, text="Line 1", values=("1A","1b"))

        # =============================================================================================================================================
        # TODO: Write query to get projects and courses
        # =============================================================================================================================================
        try:
            db_project = self.connect()
        except:
            messagebox.showinfo('Cannot Connect', 'Cannot connect to DB. Please check your internet connection!')
            return
        self.projects = self.databaseHandler.get_projects(db_project)

        try:
            db_course = self.connect()
        except:
            messagebox.showinfo('Cannot Connect', 'Cannot connect to DB. Please check your internet connection!')
            return
        self.courses = self.databaseHandler.get_courses(db_course)  
        # print (projects)
        print (self.courses)
        projects_appended = []
        for p in self.projects:
            if p[0] not in projects_appended:
                self.count_main_items += 1
                self.treeview.insert("", 999999, text=str(self.count_main_items), values=(p[0], "Project"))
                projects_appended.append(p[0])

        courses_appended = []
        for c in self.courses:
            if c[0] not in courses_appended:
                self.count_main_items += 1
                self.treeview.insert("", 999999, text=str(self.count_main_items),
                                     values=(c[0], "Course"))
                courses_appended.append(c[0])

        self.treeview.grid(row=7, column=0, columnspan=5, padx=20, pady=10, sticky=EW)

        # self.scrollbar = Scrollbar(self.mainPage)
        # self.scrollbar.grid(side="right")
        #
        addCate = Button(self.mainPage, text="Add Category", command=self.addCate)
        addCate.grid(row=1, column=4, padx=20,pady=10, sticky=W)

    def registerBTNClicked(self):

        print("register")
        # db = self.connect()
        
        self.loginWindow.withdraw()
        self.registerWin = Toplevel()
        self.registerWin.title("New User Registration")

        regLabel = Label(self.registerWin, text="New Student Registration", font="Verdana 20 bold")
        regLabel.grid(row=0, column=0, columnspan=2, pady=10, sticky=EW)

        usernameL = Label(self.registerWin, text="Username")
        usernameL.grid(row=1, column=0, sticky=W, padx=30, pady=5)

        emailAddr = Label(self.registerWin, text="GT Email Address")
        emailAddr.grid(row=2, column=0, sticky=W, padx=30, pady=5)

        password = Label(self.registerWin, text="Password")
        password.grid(row=3, column=0, sticky=W, padx=30, pady=5)

        confirmPwd = Label(self.registerWin, text="Confirm Password")
        confirmPwd.grid(row=4, column=0, sticky=W, padx=30, pady=5)

        self.regUsername = StringVar()
        self.regEmail = StringVar()
        self.regPwd = StringVar()
        self.regConfirmPwd = StringVar()

        regENT = Entry(self.registerWin, textvariable=self.regUsername, width=30)
        regENT.grid(row=1, column=1, sticky=W, padx=20, pady=5)

        emailENT = Entry(self.registerWin, textvariable=self.regEmail, width=30)
        emailENT.grid(row=2, column=1, sticky=W, padx=20, pady=5)

        pwdENT = Entry(self.registerWin, textvariable=self.regPwd, width=30, show="*")
        pwdENT.grid(row=3, column=1, sticky=W, padx=20, pady=5)

        confirmPwdEnt = Entry(self.registerWin, textvariable=self.regConfirmPwd, width=30, show="*")
        confirmPwdEnt.grid(row=4, column=1, sticky=W, padx=20, pady=5)

        regBTN = Button(self.registerWin, text="Register", command=self.register, width=20)
        regBTN.grid(row=5, column=1, padx=20, pady=10, sticky=E + W)

        regCCL = Button(self.registerWin, text="Back", command=self.cancelReg, width=20, fg="red")
        regCCL.grid(row=5, column=0, padx=20, pady=10, sticky=E)

    def myProfile(self):
        self.mainPage.withdraw()
        self.viewProfile = Toplevel()
        self.viewProfile.title("My Profile")

        photo = PhotoImage(file="User2.gif")
        profilePic = Label(self.viewProfile, image=photo)
        profilePic.photo = photo
        profilePic.grid(row=0, column=0, padx=20, pady=5)

        lab = Label(self.viewProfile, text="Me", font="Verdana 20 bold")
        lab.grid(row=1, column=0, padx=20, pady=10, sticky=EW)

        editProfileBTN = Button(self.viewProfile, text="Edit Profile", command=self.editProfile, width=20)
        editProfileBTN.grid(row=2, column=0, padx=20, pady=10, sticky=EW)


        myAppBTN = Button(self.viewProfile, text="My Application", command=self.myApp, width=20)
        myAppBTN.grid(row=3, column=0, padx=20, pady=10, sticky=EW)

        backBTN = Button(self.viewProfile, text="Back", command=self.backToMain, width=20, fg="red")
        backBTN.grid(row=4, column=0, padx=20, pady=10, sticky=EW)

    def editProfile(self):
        self.viewProfile.withdraw()
        self.editProfilePage = Toplevel()
        self.editProfilePage.title("Edit Profile")

        Label(self.editProfilePage, text="Edit Profile", font="Verdana 20 bold").grid(row=0, column=0, columnspan=2,
                                                                                      sticky=EW)

        majorLB = Label(self.editProfilePage, text="Major")
        majorLB.grid(row=1, column=0, sticky=E)

        yearLB = Label(self.editProfilePage, text="Year")
        yearLB.grid(row=2, column=0, sticky=E)

        try:
            db = self.connect()
        except:
            messagebox.showinfo('Cannot Connect', 'Please check your internet connection!')
            return
        all_majors = self.databaseHandler.get_all_major(db)
        self.major = StringVar()
        self.major.set("Please Select a Major")
        # Need to update according to DB
        majorList = all_majors
        mjrDropDown = OptionMenu(self.editProfilePage, self.major, *majorList)
        mjrDropDown.config(width=30)
        mjrDropDown.grid(row=1, column=1, padx=20, pady=5, sticky=EW)

        try:
            db = self.connect()
        except:
            messagebox.showinfo('Cannot Connect', 'Please check your internet connection!')
            return
        student_current_mjr = self.databaseHandler.get_student_info(db, self.username_logged_in)[4]

        try:
            db = self.connect()
        except:
            messagebox.showinfo('Cannot Connect', 'Please check your internet connection!')
            return
        try:
            department = self.databaseHandler.find_dept(db, student_current_mjr)
        except:
            department = ""
        deptLB = Label(self.editProfilePage, text="Department")
        deptLB.grid(row=3, column=0, sticky=E)


        self.year = StringVar()
        self.year.set("Please Select a Year")
        yearList = ["Freshman", "Sophomore", "Junior", "Senior"]
        yrDropDown = OptionMenu(self.editProfilePage, self.year, *yearList)
        yrDropDown.config(width=30)
        yrDropDown.grid(row=2, column=1, padx=20, pady=5, sticky=EW)

        # To be update when update is clicked
        # dept = "College of Computing"

        dept = Label(self.editProfilePage, text=department)
        dept.grid(row=3, column=1, sticky=EW)

        backBTN = Button(self.editProfilePage, text="Back", command=self.backToMyProfile, width=10, fg="red")
        backBTN.grid(row=4, column=0, padx=20, pady=5, sticky=E)

        updateBTN = Button(self.editProfilePage, text="Update", command=self.updateProfile, width=20)
        updateBTN.grid(row=4, column=1, padx=20, pady=5, sticky=EW)
        # self.yrStr = StringVar()
        # self.yrStr.set("Please Select a Year")
        # yrOptions = ["Freshman", "Sophormore", "Junior", "Senior"]
        # yrDropDown = OptionMenu(self.mainPage, self.yrStr, *yrOptions)
        # yrDropDown.grid(row = 4, column = 1, padx = 20, pady = 5, sticky = W+E)

        print("zhi zhang")

    # Has a problem
    def myApp(self):
        print("yea")
        self.viewProfile.withdraw()
        self.myApp = Toplevel()
        self.myApp.title("My Applications")

        Label(self.myApp, text="My Application", font="Verdana 20 bold").grid(row=0, column=0, padx=20, pady=5,
                                                                              columnspan=2, sticky=EW)
        Label(self.myApp, text="", width=30).grid(row=0, column=2, sticky=EW)
        # Label(self.myApp, text = "2").grid(row = 0, column = 2, sticky = EW)
        # Label(self.myApp, text = "3").grid(row = 0, column = 3, sticky = EW)
        # Label(self.myApp, text = "4").grid(row = 0, column = 4, sticky = EW)


        self.treeviewApp = ttk.Treeview(self.myApp, show="headings")
        self.treeviewApp['columns'] = ("Date", "Project Name", "Status")

        self.treeviewApp.column("Date", width=50)
        self.treeviewApp.heading("Date", text="Date")

        self.treeviewApp.column("Project Name", width=200)
        self.treeviewApp.heading("Project Name", text="Project Name")

        self.treeviewApp.column("Status", width=50)
        self.treeviewApp.heading("Status", text="Status")


        # Query the database to get Course and Project information to be displayed in treeview
        # This is only the place where the view gets updated
        # Always call the query to get Course/Project to make data consistent when new Course/Project is added into the database
        # treeview.insert("Name", 0, ) # Place holders for now
        # treeview.insert("" , 0, text="Line 1", values=("1A","1b"))

        # =============================================================================================================================================
        # TODO: Write query to get projects and courses
        # =============================================================================================================================================
        try:
            db = self.connect()
        except:
            messagebox.showinfo('Cannot Connect', 'Please check your internet connection!')
            return

        applications = self.databaseHandler.get_my_apps(db, self.username_logged_in)
        print(applications)

        date = parser.parse("01/01/2017")
        status = ["Approved", "Rejected", "Pending"]
        for i in range(len(applications)):
            # print(date)
            app = applications[i]
            date = str(app[1])
            project_name = app[0]
            status = app[2]

            self.treeviewApp.insert("", 999999, text=str(i),
                                    values=(date, project_name, status))
            # date = date + timedelta(days=1)
        # self.treeviewApp.insert("", 999999, values = ("Course1", "Course", "Approved"))
        # self.treeviewApp.insert("", 999999, values = ("Course1", "Course", "Approved"))

        self.treeviewApp.grid(row=1, column=0, columnspan=5, padx=20, pady=10, sticky=EW)

        backBTN = Button(self.myApp, text="Back", command=self.backToMyProfileFromApp, fg="red", width=10)
        backBTN.grid(row=2, column=2, columnspan=1, sticky=W, padx=10, pady=10)
        print("sha bi")

    def selectProjCourse(self):

        # print(self.treeview.selection())
        # print("selected")
        # print (self.treeview.set(self.treeview.get_children()[0], column = "#0"))
        typeSelected = self.treeview.set(self.treeview.selection(), column=1)
        nameSelected = self.treeview.set(self.treeview.selection(), column=0)
        print (nameSelected)
        if typeSelected == "Project":
            self.viewProject(nameSelected)
            print("Called")
        if typeSelected == "Course":
            self.viewCourse(nameSelected)
            print("Called")
    # def course_or_project(self):

    def viewProject(self, nameSelected):
        self.mainPage.withdraw()
        self.projectDetail = Toplevel()
        self.projectDetail.title("Project Details")
        self.selectedProjectName = nameSelected
        try:
            db = self.connect()
        except:
            messagebox.showinfo('Cannot Connect', 'Please check your internet connection!')
            return
        project_info = self.databaseHandler.view_project(db, nameSelected)
        advisor = project_info[0][0]
        advisor_email = project_info[0][1]
        description = project_info[0][2]
        designation = project_info[0][3]
        category = project_info[0][4]
        major = project_info[0][5]
        year = project_info[0][6]
        dept = project_info[0][7]
        est = str(project_info[0][8])

        if major == None:
            major = ""
        if year == None:
            year = ""
        if dept == None:
            dept = ""

        requirements = major + "\n " + year + "\n " + dept
        print(project_info)


        Label(self.projectDetail, text=nameSelected, font="Verdana 20 bold").grid(row=0, column=0,
                                                                                                   padx=20, pady=10,
                                                                                                   sticky=W, columnspan=2)
        Label(self.projectDetail, text="Advisor:", font="bold").grid(row=1, column=0, padx=20, pady=10, sticky=W)
        Label(self.projectDetail, text=advisor).grid(row=1, column=1, padx=20, pady=10, sticky=W)

        Label(self.projectDetail, text="Descritpion:").grid(row=6, column=0, padx=20, pady=10, sticky=W)
        T = Text(self.projectDetail, height=15, width=70)
        T.insert(END, description)
        T.config(state=DISABLED)
        T.grid(row=7, column=0, padx=30, pady=0, sticky=W, columnspan = 2)
        # S.config(command=T.yview)
        # T.config(yscrollcommand=S.set)
        # Label(self.projectDetail, text="Start Description \n Description Line 2").grid(row=3, column=0, padx=30,
        #                                                                                sticky=W)
        Label(self.projectDetail, text="Designation:").grid(row=2, column=0, padx=20, pady=10, sticky=W)
        Label(self.projectDetail, text=designation).grid(row=2, column=1, padx=20, pady=10, sticky=W)

        Label(self.projectDetail, text="Category:").grid(row=3, column=0, padx=20, pady=10, sticky=W)
        Label(self.projectDetail, text=category).grid(row=3, column=1, padx=20, pady=10, sticky=W)

        Label(self.projectDetail, text="Requirements:").grid(row=4, column=0, padx=20, pady=10, sticky=W)
        Label(self.projectDetail, text=requirements).grid(row=4, column=1, padx=20, pady=10, sticky=W)

        Label(self.projectDetail, text="Estimated Number of Students:").grid(row=5, column=0, padx=20, pady=10, sticky=W)
        Label(self.projectDetail, text=est).grid(row=5, column=1, padx=20, pady=10, sticky=W)

        backBTN = Button(self.projectDetail, text="Back", command=self.backToMainProjectDetail)
        backBTN.grid(row=8, column=0, padx=20, pady=10, sticky=EW)

        applyBTN = Button(self.projectDetail, text="Apply", command=self.apply)
        applyBTN.grid(row=8, column=1, padx=20, pady=10, sticky=EW)

    def viewCourse(self, nameSelected):
        self.mainPage.withdraw()
        self.courseDetail = Toplevel()
        self.courseDetail.title("Course Details")

        try:
            db = self.connect()
        except:
            messagebox.showinfo('Cannot Connect', 'Please check your internet connection!')
            return
        courses = self.databaseHandler.get_course(db, nameSelected)


        Label(self.courseDetail, text=courses[0][0], font="Verdana 20 bold").grid(row=0, column=0,
                                                                                                   padx=20, pady=10,
                                                                                                   sticky=W, columnspan=2)
        # Label(self.courseDetail, text="Course Name:", font="bold").grid(row=1, column=0, padx=20, pady=10, sticky=W)
        # Label(self.courseDetail, text="(Course Name)", font="bold").grid(row=1, column=1, padx=20, pady=10, sticky=W)

        Label(self.courseDetail, text="Instructor").grid(row=1, column=0, padx=20, pady=10, sticky=W)
        Label(self.courseDetail, text=courses[0][1]).grid(row=1, column=1, padx=20, pady=10, sticky=W)

        Label(self.courseDetail, text="Designation:").grid(row=2, column=0, padx=20, pady=10, sticky=W)
        Label(self.courseDetail, text=courses[0][3]).grid(row=2, column=1, padx=20, pady=10, sticky=W)

        Label(self.courseDetail, text="Category:").grid(row=3, column=0, padx=20, pady=10, sticky=W)
        Label(self.courseDetail, text=courses[0][4]).grid(row=3, column=1, padx=20, pady=10, sticky=W)

        Label(self.courseDetail, text="Estimated Number of Students:").grid(row=4, column=0, padx=20, pady=10, sticky=W)
        Label(self.courseDetail, text=str(courses[0][2])).grid(row=4, column=1, padx=20, pady=10, sticky=W)

        backBTN = Button(self.courseDetail, text="Back", command=self.backToMainCourseDetail)
        backBTN.grid(row=5, column=0, padx=20, pady=10, sticky=E)
        print("View Course")

    # ================================================================================================================================
    #                                               Admin User View
    # ================================================================================================================================
    def choose_func(self):
        self.loginWindow.withdraw()
        self.choose_function = Toplevel()
        self.choose_function.title("Choose a Function")

        photo = PhotoImage(file="User2.gif")
        profilePic = Label(self.choose_function, image=photo)
        profilePic.photo = photo
        profilePic.grid(row=0, column=0, padx=20, pady=5)

        lab = Label(self.choose_function, text="Choose Functionality", font="Verdana 20 bold")
        lab.grid(row=1, column=0, padx=20, pady=10, sticky=EW)

        editProfileBTN = Button(self.choose_function, text="View Applications", command=self.viewApplications, width=20)
        editProfileBTN.grid(row=2, column=0, padx=20, pady=10, sticky=EW)

        myAppBTN = Button(self.choose_function, text="View Popular Project Report", command=self.viewPopularProjects, width=20)
        myAppBTN.grid(row=3, column=0, padx=20, pady=10, sticky=EW)

        myAppBTN = Button(self.choose_function, text="View Application Report", command=self.viewApplicationsReport, width=20)
        myAppBTN.grid(row=4, column=0, padx=20, pady=10, sticky=EW)

        myAppBTN = Button(self.choose_function, text="Add a Project", command=self.addAProject, width=20)
        myAppBTN.grid(row=5, column=0, padx=20, pady=10, sticky=EW)

        myAppBTN = Button(self.choose_function, text="Add a Course", command=self.addACourse, width=20)
        myAppBTN.grid(row=6, column=0, padx=20, pady=10, sticky=EW)

        backBTN = Button(self.choose_function, text="Log Out", command=self.logOutAdmin, width=20, fg="red")
        backBTN.grid(row=7, column=0, padx=20, pady=10, sticky=EW)

    def viewApplications(self):
        self.choose_function.withdraw()
        self.applicationDetails = Toplevel()
        self.applicationDetails.title("Applications")

        Label(self.applicationDetails, text="Application", font="Verdana 20 bold").grid(row=0, column=0,
                                                                                                   padx=20, pady=10,
                                                                                                   sticky=EW, columnspan=2)
        self.treeviewAppAdmin = ttk.Treeview(self.applicationDetails, show="headings")
        self.treeviewAppAdmin['columns'] = ("Project", "Applicant Name", "Applicant Major", "Applicant Year", "Status")

        self.treeviewAppAdmin.column("Project", width=100)
        self.treeviewAppAdmin.heading("Project", text="Project")

        self.treeviewAppAdmin.column("Applicant Major", width=100)
        self.treeviewAppAdmin.heading("Applicant Major", text="Applicant Major")

        self.treeviewAppAdmin.column("Applicant Year", width=100)
        self.treeviewAppAdmin.heading("Applicant Year", text="Applicant Year")

        self.treeviewAppAdmin.column("Status", width=100)
        self.treeviewAppAdmin.heading("Status", text="Status")

        self.treeviewAppAdmin.column("Applicant Name", width = 100)
        self.treeviewAppAdmin.heading("Applicant Name", text="Applicant Name")
        # Query the database to get Course and Project information to be displayed in treeview
        # This is only the place where the view gets updated
        # Always call the query to get Course/Project to make data consistent when new Course/Project is added into the database
        # treeview.insert("Name", 0, ) # Place holders for now
        # treeview.insert("" , 0, text="Line 1", values=("1A","1b"))

        # =============================================================================================================================================
        # TODO: Write query to get projects and courses
        # =============================================================================================================================================
        status = ["Approved", "Rejected", "Pending"]
        major = ["CS", "ECE", "MATH", "HISTORY", "ART"]
        year = ["Freshman", "Sophomore", "Junior", "Senior"]

        try:
            db = self.connect()
        except:
            messagebox.showinfo('Cannot Connect', 'Please check your internet connection!')
            return
        application_info = self.databaseHandler.get_application_info(db)

        for i in application_info:
            # print(date)

            self.treeviewAppAdmin.insert("", 999999, text=str(i),
                                    values=(i[0], i[4], i[2], i[3], i[1]))
        # self.treeviewApp.insert("", 999999, values = ("Course1", "Course", "Approved"))
        # self.treeviewApp.insert("", 999999, values = ("Course1", "Course", "Approved"))

        self.treeviewAppAdmin.grid(row=1, column=0, columnspan=5, padx=20, pady=10, sticky=EW)

        accept = Button(self.applicationDetails, text='Accpet', command=self.accept)
        accept.grid(row = 2, column = 2, padx=20, pady=10, sticky=EW)

        reject = Button(self.applicationDetails, text='Reject', command=self.reject)
        reject.grid(row=2, column = 3, padx=20, pady=10, sticky=EW)

        backBTN = Button(self.applicationDetails, text="Back", command=self.backToChooseFunc)
        backBTN.grid(row=2, column=0, padx=20, pady=10, sticky=EW)

    def viewPopularProjects(self):
        print("View Popular Projects")
        self.choose_function.withdraw()
        self.popularProjects = Toplevel()
        self.popularProjects.title("Popular Projects")

        Label(self.popularProjects, text="Popular Projects", font="Verdana 20 bold").grid(row=0, column=0,
                                                                                                   padx=20, pady=10,
                                                                                                   sticky=EW, columnspan=2)
        self.treeviewPopProjects = ttk.Treeview(self.popularProjects, show="headings")
        self.treeviewPopProjects['columns'] = ("Project", "# of Applicants")

        self.treeviewPopProjects.column("Project", width=150)
        self.treeviewPopProjects.heading("Project", text="Project")

        self.treeviewPopProjects.column("# of Applicants", width=100)
        self.treeviewPopProjects.heading("# of Applicants", text="Applicant Major")

        # Query the database to get Course and Project information to be displayed in treeview
        # This is only the place where the view gets updated
        # Always call the query to get Course/Project to make data consistent when new Course/Project is added into the database

        # =============================================================================================================================================
        # TODO: Write query to get projects and courses
        # =============================================================================================================================================
        try:
            db = self.connect()
        except:
            messagebox.showinfo('Cannot Connect', 'Please check your internet connection!')
            return

        pop_projects = self.databaseHandler.get_top_project(db)

        for i in pop_projects:
            self.treeviewPopProjects.insert("", 999999, text=str(i),
                                    values=(i[0], i[1]))
        # self.treeviewApp.insert("", 999999, values = ("Course1", "Course", "Approved"))
        # self.treeviewApp.insert("", 999999, values = ("Course1", "Course", "Approved"))

        self.treeviewPopProjects.grid(row=1, column=0, columnspan=5, padx=20, pady=10, sticky=EW)

        backBTN = Button(self.popularProjects, text="Back", command=self.backToChooseFuncPopProject)
        backBTN.grid(row=2, column=0, padx=20, pady=10, sticky=EW)

    def viewApplicationsReport(self):
        print("View Application Report")
        self.choose_function.withdraw()
        self.appReport = Toplevel()
        self.appReport.title("Application Report")

        Label(self.appReport, text="Popular Projects", font="Verdana 20 bold").grid(row=0, column=0,padx=20, pady=10,
                                                                                    sticky=EW, columnspan=2)
        Label(self.appReport, text="Application overview stats (Fill in later)").grid(row=1, column=0, padx=20, pady=10,
                                                                                    sticky=EW, columnspan=2)
        self.treeviewAppReport = ttk.Treeview(self.appReport, show="headings")
        self.treeviewAppReport['columns'] = ("Project", "# of Applicants", "Accept Rate", "Top 3 Major")

        self.treeviewAppReport.column("Project", width=300)
        self.treeviewAppReport.heading("Project", text="Project")

        self.treeviewAppReport.column("# of Applicants", width=100)
        self.treeviewAppReport.heading("# of Applicants", text="# of Applicants")

        self.treeviewAppReport.column("Accept Rate", width=100)
        self.treeviewAppReport.heading("Accept Rate", text="Accept Rate")

        self.treeviewAppReport.column("Top 3 Major", width=400)
        self.treeviewAppReport.heading("Top 3 Major", text="Top 3 Major")

        # self.treeviewPopProjects.column("Project", width=150)
        # self.treeviewPopProjects.heading("Project", text="Project")
        #
        # self.treeviewPopProjects.column("# of Applicants", width=100)
        # self.treeviewPopProjects.heading("# of Applicants", text="Applicant Major")

        # Query the database to get Course and Project information to be displayed in treeview
        # This is only the place where the view gets updated
        # Always call the query to get Course/Project to make data consistent when new Course/Project is added into the database

        # =============================================================================================================================================
        # TODO: Write query to get projects and courses
        # =============================================================================================================================================
        try:
            db = self.connect()
        except:
            messagebox.showinfo('Cannot Connect', 'Please check your internet connection!')
            return

        application_report_data = self.databaseHandler.app_report()
        data = sorted(application_report_data, key=itemgetter(2), reverse=True)
        # print (application_report_data)
        # return
        for i in data:
            self.treeviewAppReport.insert("", 999999, text=str(i),
                                    values=(i[0], i[1], i[2], i[3]))
        # self.treeviewApp.insert("", 999999, values = ("Course1", "Course", "Approved"))
        # self.treeviewApp.insert("", 999999, values = ("Course1", "Course", "Approved"))

        self.treeviewAppReport.grid(row=2, column=0, columnspan=5, padx=20, pady=10, sticky=EW)

        backBTN = Button(self.appReport, text="Back", command=self.backToChooseFuncAppReport)
        backBTN.grid(row=3, column=0, padx=20, pady=10, sticky=EW)

    def addACourse(self):
        print("add course")
        self.choose_function.withdraw()
        self.addCourse = Toplevel()
        self.addCourse.title("Add a Course")

        Label(self.addCourse, text="Add a Course", font="Verdana 20 bold").grid(row=0, column=0,padx=20, pady=10,sticky=EW, columnspan=3)

        Label(self.addCourse, text="Course Number").grid(row=1, column=0,padx=20, pady=10,sticky=W)
        self.addCourseNumber = StringVar()
        self.courseNumberENT = Entry(self.addCourse, textvariable=self.addCourseNumber, width=30)
        self.courseNumberENT.grid(row=1, column=1, padx=20, pady=10, sticky=W)

        Label(self.addCourse, text="Course Name:").grid(row=2, column=0, padx=20, pady=10, sticky=W)
        self.addCourseName = StringVar()
        self.courseNameENT = Entry(self.addCourse, textvariable=self.addCourseName, width=30)
        self.courseNameENT.grid(row=2, column=1, padx=20, pady=10, sticky=W)

        Label(self.addCourse, text="Instructor:").grid(row=3, column=0, padx=20, pady=10, sticky=W)
        self.addInstructor = StringVar()
        self.instructorENT = Entry(self.addCourse, textvariable=self.addInstructor, width=30)
        self.instructorENT.grid(row=3, column=1, padx=20, pady=10, sticky=W)

        Label(self.addCourse, text="Designation:").grid(row=4, column=0, padx=20, pady=10, sticky=W)

        self.addCourseDsgStr = StringVar()
        self.addCourseDsgStr.set("Please Select a Designation")
        dsgOptions = ["Sustainable Communities", "Community"]
        desigDropDown = OptionMenu(self.addCourse, self.addCourseDsgStr, *dsgOptions)
        desigDropDown.grid(row=4, column=1, padx=20, pady=10, sticky=W)

        # self.addDesignation = StringVar()
        # self.designationENT = Entry(self.addCourse, textvariable=self.addDesignation, width=30)
        # self.designationENT.grid(row=4, column=1, padx=20, pady=10, sticky=W)

        Label(self.addCourse, text="Category:").grid(row=5, column=0, padx=20, pady=10, sticky=W)
        self.cate_num_add_course = 0
        catStr = StringVar()
        catStr.set("Please Select a Category")
        catOptions = ["computing for good", "doing good for your neighborhood", "reciprocal teaching and learning",
                      "urban development", "adaptive learning", "technology for social good", "sustainable communities",
                      "crowd-sourced", "collaborative action"]
        catDropDown = OptionMenu(self.addCourse, catStr, *catOptions)
        catDropDown.config(width=30)
        catDropDown.grid(row=5, column=1, padx=20, pady=10, sticky=W)
        self.catStrListAddCourse.append(catStr)
        # catDropDown.grid(row=1 + self.num_cate, column=3, padx=20, pady=5, sticky=W + E)

        self.estStudentLB = Label(self.addCourse, text="Estimated Number of Students:")
        self.estStudentLB.grid(row=6, column=0, padx=20, pady=10, sticky=W)

        self.addEstNoStudent = StringVar()
        self.estNoStudentENT = Entry(self.addCourse, textvariable=self.addEstNoStudent, width=30)
        self.estNoStudentENT.grid(row=6, column=1, padx=20, pady=10, sticky=W)

        self.addCourseBackBTN = Button(self.addCourse, text="Back", command=self.backToChooseFuncAddCourse)
        self.addCourseBackBTN.grid(row=7, column=0, padx=20, pady=10, sticky=E)

        self.addCourseSubmitBTN = Button(self.addCourse, text="Submit", command=self.submitCourse)
        self.addCourseSubmitBTN.grid(row=7, column=1, padx=20, pady=10, sticky=E)

        addCate = Button(self.addCourse, text="Add a new category", command=self.addCateAddCourse)
        addCate.grid(row=5, column=2, padx=20, pady=10, sticky=E)
        print("View Course")

        # tjyhgb

    def addAProject(self):

        self.choose_function.withdraw()
        self.addProjectPage = Toplevel()
        self.addProjectPage.title("Add a Project")

        self.catStrAddProject = StringVar()
        self.catStrAddProject.set("Please Select a Category")

        self.dsgStrAddProject = StringVar()
        self.dsgStrAddProject.set("Please Select a Designation")

        self.mjrStrAddProject = StringVar()
        self.mjrStrAddProject.set("Please Select a Major")

        self.yrStrAddProject = StringVar()
        self.yrStrAddProject.set("Please Select a Year")

        self.depStrAddProject = StringVar()
        self.depStrAddProject.set('Please Select a Requirement')

        catOptions = ["computing for good",	"doing good for your neighborhood",	"reciprocal teaching and learning",
                      "urban development",	"adaptive learning", "technology for social good", "sustainable communities",
                      "crowd-sourced", "collaborative action"]

        dsgOptions = ["Sustainable Communities", "Community"]

        try:
            db = self.connect()
        except:
            messagebox.showinfo('Cannot Connect', 'Please check your internet connection!')
            return
        all_majors = self.databaseHandler.get_all_major(db)
        majorList = all_majors
        # ["Computer Science", "Mathematics", "Industrial and System Engineering", "Chemical Engineering", "Electrical Engineering", "Computer Engineering"]

        yearList = ["Freshman", "Sophomore", "Junior", "Senior"]


        try:
            db = self.connect()
        except:
            messagebox.showinfo('Cannot Connect', 'Please check your internet connection!')
            return
        depOptions = self.databaseHandler.get_all_dept(db)

        # depOptions = ["College of Computing", "College of Engineering", "College of Liberal Arts", "College of Mathematics"]

        Label(self.addProjectPage, text = 'Add a Project', font = "Verdana 20 bold").grid(row = 0, column = 0, columnspan = 3, pady = 10, sticky = EW)

        self.projName = StringVar()
        Label(self.addProjectPage, text = 'Project Name:').grid(row = 1, column = 0, pady = 10, padx = 40, sticky = EW)
        self.projectNameEntry = Entry(self.addProjectPage, textvariable=self.projName).grid(row = 1, column = 1, pady = 10, padx = 40, sticky = EW)

        self.advisorname = StringVar()
        Label(self.addProjectPage, text = 'Advior:').grid(row = 2, column =0, pady = 10, padx = 40, sticky = EW)
        self.advisorNameEntry = Entry(self.addProjectPage, textvariable=self.advisorname).grid(row = 2, column = 1, pady = 10, padx = 40, sticky = EW)

        self.advisorEmail = StringVar()
        Label(self.addProjectPage, text = 'Advisor Email:').grid(row = 3, column = 0, pady = 10, padx = 40, sticky = EW)
        self.advisorEmailEntry = Entry(self.addProjectPage, textvariable=self.advisorEmail).grid(row = 3, column = 1, pady = 10, padx = 40, sticky = EW)

        self.description = StringVar()
        Label(self.addProjectPage, text = 'Description:').grid(row = 4, column = 0, pady = 10, padx = 40, sticky = EW)
        self.descriptionEntry = Entry(self.addProjectPage, textvariable=self.description).grid(row = 4, column = 1, pady = 10, padx = 40, sticky = EW)

        self.cate_num_add_project = 0
        Label(self.addProjectPage, text = 'Category:').grid(row = 5, column = 0, pady = 10, padx = 40, sticky = EW)
        categoryDropdown1 = OptionMenu(self.addProjectPage, self.catStrAddProject, *catOptions)
        categoryDropdown1.config(width=30)
        categoryDropdown1.grid(row = 5, column = 1, pady = 10, padx = 40, sticky = EW)

        self.catStrListAddProject.append(self.catStrAddProject)

        addCate2 = Button(self.addProjectPage, text = "Add a new category", command = self.addCateAddProject)
        addCate2.grid(row = 5, column = 2, padx = 40, pady = 10, sticky = EW)

        self.designLabel = Label(self.addProjectPage, text = 'Desigation:')
        self.designLabel.grid(row = 6, column = 0, pady = 10, padx = 40, sticky = EW)
        # dsgOptions = ["Sustainable Communities", "Community"]
        self.desigDropDown = OptionMenu(self.addProjectPage, self.dsgStrAddProject, *dsgOptions)
        self.desigDropDown.grid(row = 6, column = 1, pady = 10, padx = 40, sticky = EW)

        self.estimateLabel = Label(self.addProjectPage, text = 'Estimated # of student:')
        self.estimateLabel.grid(row = 7, column = 0, pady = 10, padx = 40, sticky = EW)


        self.estimatedNumber = StringVar()
        self.estimatedNumberEntry = Entry(self.addProjectPage, textvariable=self.estimatedNumber)
        self.estimatedNumberEntry.grid(row = 7, column = 1, pady = 10, padx = 40, sticky = EW)

        self.majorLabel = Label(self.addProjectPage, text = 'Major Requirement:')
        self.majorLabel.grid(row = 8, column  = 0, pady = 10, padx = 40, sticky = EW)
        # mjrOptions = ["To Be Added"]
        self.mjrDropDown = OptionMenu(self.addProjectPage, self.mjrStrAddProject, *majorList)
        self.mjrDropDown.grid(row = 8, column = 1, padx = 40, pady = 10, sticky = EW)

        self.yearLabel = Label(self.addProjectPage, text = 'Year Requirement:')
        self.yearLabel.grid(row = 9, column  = 0, pady = 10, padx = 40, sticky = EW)

        # yrOptions = ["Freshman", "Sophormore", "Junior", "Senior"]
        self.yrDropDown = OptionMenu(self.addProjectPage, self.yrStrAddProject, *yearList)
        self.yrDropDown.grid(row = 9, column = 1, padx = 40, pady = 10, sticky = EW)

        self.depLabel = Label(self.addProjectPage, text = 'Department Requirement:')
        self.depLabel.grid(row = 10, column  = 0, pady = 10, padx = 40, sticky = EW)


        # self.depOptions = ["Place Holder"]

        self.depDropDown = OptionMenu(self.addProjectPage, self.depStrAddProject, *depOptions)
        self.depDropDown.grid(row = 10, column = 1, pady = 10, padx = 40, sticky = EW)

        self.backBTNAddProject = Button(self.addProjectPage, text="Back", command=self.backToChooseFuncAddProject)
        self.backBTNAddProject.grid(row=11, column=0, padx=40, pady=10, sticky = EW)

        self.submitProject = Button(self.addProjectPage, text="Sumbit", command=self.insertProject)
        self.submitProject.grid(row=11, column=1, padx=40, pady=10, sticky=EW)
    # ================================================================================================================================
    # |															User Controller														 |
    # ================================================================================================================================
    def connect(self):

        db = pymysql.connect(host='academic-mysql.cc.gatech.edu', passwd='SD8el4Qq',
                             user='cs4400_Team_32', db='cs4400_Team_32')
        # print("connected to DB")
        return db

    def login(self):
        try:
            db = self.connect()
        except:
            messagebox.showinfo('Cannot Connect', 'Please check your internet connection!')
            return

        username = self.usernameLogIn.get()
        password = self.passwordLogIn.get()
        login = self.databaseHandler.validateLogin(db, username, password)
        print (login)
        if login == 1:
        # Admin login
            print("Admin")
            self.username_logged_in = username
            self.choose_func()
        elif login == 2:
        #     Student Login
            # self.logged
            self.username_logged_in = username
            print("Student")

            self.goToMain(1)

        # if self.usernameLogIn.get() == "u" and self.passwordLogIn.get() == 'p':
        #     self.goToMain()
        # elif self.usernameLogIn.get() == "admin":
        #     self.choose_func()
        else:
            messagebox.showinfo("Login Failed", "The username/password you entered is incorrect. Please try again")

    def logOut(self):
        self.mainPage.withdraw()
        self.loginWindow.deiconify()
        self.usernameENT.delete(0, 'end')
        self.pwENT.delete(0, 'end')

    def register(self):
        print("register")
        try:
            db = self.connect()
        except:
            messagebox.showinfo('Cannot Connect', 'Please check your internet connection!')
            return
        username = self.regUsername.get()
        email = self.regEmail.get()
        regPwd = self.regPwd.get()
        regConfirmPwd = self.regConfirmPwd.get()

        regCode = self.databaseHandler.registerUser(db, username, regPwd, regConfirmPwd, email)
        print(regCode)

        if regCode == 0:
            messagebox.showerror('ERROR','Fill the required information')
        elif regCode == 1:
            messagebox.showerror('ERROR','Passwords do not match')
        elif regCode == 2:
            messagebox.showerror('ERROR','Please enter a valid GT email')
        elif regCode == 3:
            messagebox.showerror('ERROR','Email already exsits, enter a different email')
        elif regCode == 4:
            messagebox.showerror('ERROR','Usename already exsits, enter a different username')
        else:
            messagebox.showinfo('Info','You are successfully registered')
            self.goToMain(0)

        
        print(self.regUsername.get(), self.regEmail.get(), self.regPwd.get(), self.regConfirmPwd.get())

    def cancelReg(self):
        self.registerWin.withdraw()
        self.loginWindow.deiconify()
        print("cancel")

    def cancelLogin(self):
        print("cancel")
        self.loginWindow.destroy()

    def showDropDownValue(self, v):
        print(v)

    # Need to call query agains
    def applyFilter(self):
        # print(applyFilter)
        # print(self.treeview.get_children())
        if self.detached != []:
            for item in self.detached:
                self.treeview.reattach(item[0], "", item[1])

        title = self.titleMain.get()
        des = self.dsgStr.get()
        mjr = self.mjrStr.get()
        yr = self.yrStr.get()
        cat = self.catStr.get()
        selectType = self.selectType.get()
        
        filterType = selectType
        # print(title, des, major, year, cat, selectType)
        if selectType == 0:
            messagebox.showinfo("Type Error", "Please select a type.")
            return
        elif selectType == 1:
            filterType = "Project"
        elif selectType == 2:
            filterType = "Course"
        else:
            filterType = "Both"

        # Padd over courses list
        everything = []
        
        for i in self.courses:
            i = list(i)
            for j in range(3):

                i.append(i[-1])
            i[2] = None
            i[3] = None
            i[4] = None
            everything.append(i)

        for p in self.projects:
            everything.append(list(p))

        # print (everything)
        # print ()

        names = {}
        for e in everything:
            names[e[0]] = e[1:]

        unique_names = names.keys()

        categories = {}
        for u in unique_names:
            categories[u] = []
            for e in everything:
                if e[0] == u:
                    categories[u].append(e[-1])

        print(categories)

        # print()
        things = {}
        for i in self.treeview.get_children():

            name = self.treeview.set(i, 0)
            tyype = self.treeview.set(i, 1)

            things[i] = [name, tyype]
            for p in everything:
                if name == p[0]:
                    things[i] += p[1:]



        catStrList = []
        for sv in self.catStrList:
            catStrList.append(sv.get())

        for key in things.keys():
            name = things[key][0]
            tyype = things[key][1]
            designation = things[key][2]
            major = things[key][3]
            year = things[key][4]
            category = categories[name] 
            # return 
            # # Need update to fit more cretieria
            # print(catStrList)
            # print (category)
            if (filterType != "Both" and tyype != filterType) or (
                    title != "" and title != name) or (
                    designation != None and designation != des and des != "Please Select a Designation") or (
                    major != None and major != mjr and mjr != 'Please Select a Major') or (
                    year != None and year != yr and yr != 'Please Select a Year') or (
                    category != None and set(category) != set(catStrList) and cat != 'Please Select a Category'):
            #     # self.detached_dict[itemType].append
            #     # if title != None and title != self.treeview.set(i, 0):
            #     print(self.treeview.set(i, 1), filterType)

                self.detached.append((key, self.count_main_items - self.treeview.index(key)))
                self.treeview.detach(key)
        # print (things)
            # print(self.treeview.set(i, 0), title)
            # if title != None and title != self.treeview.set(i, 0):
            # 	self.detached.append((i, self.treeview.index(i)))
            # 	self.treeview.detach(i)
            # self.treeview.insert("", 999999, i)

    # Maybe should run query again as the filter in tkinter is wierd
    def resetFilter(self):
        self.titleMain = StringVar()
        titleENT = Entry(self.mainPage, textvariable=self.titleMain, width=20)
        titleENT.grid(row=1, column=1, sticky=E + W, padx=20, pady=5)

        # Category DropDown
        self.catStr = StringVar()
        self.catStr.set("Please Select a Category")
        # catOptions = ["Computing for Good", "Doing Good for Your Neighborhood"]

        catOptions = ["computing for good", "doing good for your neighborhood", "reciprocal teaching and learning",
                      "urban development", "adaptive learning", "technology for social good", "sustainable communities",
                      "crowd-sourced", "collaborative action"]
        catDropDown = OptionMenu(self.mainPage, self.catStr, *catOptions)
        catDropDown.config(width=30)
        catDropDown.grid(row=1, column=3, padx=20, pady=5, sticky=W + E)
        self.catStrList.append(self.catStr)

        # Designation DropDown
        self.dsgStr = StringVar()
        self.dsgStr.set("Please Select a Designation")
        dsgOptions = ["Sustainable Communities", "Community"]
        desigDropDown = OptionMenu(self.mainPage, self.dsgStr, *dsgOptions)
        desigDropDown.grid(row=2, column=1, padx=20, pady=5, sticky=W + E)

        # Major Drop Down
        try:
            db = self.connect()
        except:
            messagebox.showinfo('Cannot Connect', 'Please check your internet connection!')
            return
        all_majors = self.databaseHandler.get_all_major(db)
        # print (all_majors)
        self.mjrStr = StringVar()
        self.mjrStr.set("Please Select a Major")
        mjrOptions = all_majors
        mjrDropDown = OptionMenu(self.mainPage, self.mjrStr, *mjrOptions)
        mjrDropDown.grid(row=3, column=1, padx=20, pady=5, sticky=W + E)

        # Year Drop Down
        self.yrStr = StringVar()
        self.yrStr.set("Please Select a Year")
        yrOptions = ["Freshman", "Sophormore", "Junior", "Senior"]
        yrDropDown = OptionMenu(self.mainPage, self.yrStr, *yrOptions)
        yrDropDown.grid(row=4, column=1, padx=20, pady=5, sticky=W + E)

        self.selectType = IntVar()
        self.selectType.set(1)

        self.projRadBTN = Radiobutton(self.mainPage, text="    Project   ", variable=self.selectType, value=1)
        self.projRadBTN.grid(row=4, column=2)

        self.courseRadBTN = Radiobutton(self.mainPage, text="    Course    ", variable=self.selectType, value=2)
        self.courseRadBTN.grid(row=4, column=3)

        self.bothRadBTN = Radiobutton(self.mainPage, text="    Both    ", variable=self.selectType, value=3)
        self.bothRadBTN.grid(row=4, column=4)

        self.appFilter = Button(self.mainPage, text="Apply Filter", command=self.applyFilter, width=10)
        self.appFilter.grid(row=5, column=3, padx=20, pady=10, sticky=E)

        self.resFilter = Button(self.mainPage, text="Reset Filter", command=self.resetFilter, width=10)
        self.resFilter.grid(row=5, column=4, padx=20, pady=10, sticky=E)

        self.select = Button(self.mainPage, text="View", command=self.selectProjCourse, width=10)
        self.select.grid(row=6, column=4, padx=20, pady=10)

        self.treeview = ttk.Treeview(self.mainPage, show="headings")
        self.treeview['columns'] = ("Name", "Type")
        self.treeview.column("Name", width=400)
        self.treeview.heading("Name", text="Name")

        self.treeview.column("Type", width=20)
        self.treeview.heading("Type", text="Type")

        self.treeview.heading("#0", text="Cnt", anchor='center')
        self.treeview.column("#0", minwidth=5, width=5)

        # Query the database to get Course and Project information to be displayed in treeview
        # This is only the place where the view gets updated
        # Always call the query to get Course/Project to make data consistent when new Course/Project is added into the database
        # treeview.insert("Name", 0, ) # Place holders for now
        # treeview.insert("" , 0, text="Line 1", values=("1A","1b"))

        # =============================================================================================================================================
        # TODO: Write query to get projects and courses
        # =============================================================================================================================================
        try:
            db_project = self.connect()
        except:
            messagebox.showinfo('Cannot Connect', 'Cannot connect to DB. Please check your internet connection!')
            return
        self.projects = self.databaseHandler.get_projects(db_project)

        try:
            db_course = self.connect()
        except:
            messagebox.showinfo('Cannot Connect', 'Cannot connect to DB. Please check your internet connection!')
            return
        self.courses = self.databaseHandler.get_courses(db_course)  
        # print (projects)
        print (self.courses)

        projects_appended = []
        for p in self.projects:
            if p[0] not in projects_appended:
                self.count_main_items += 1
                self.treeview.insert("", 999999, text=str(self.count_main_items), values=(p[0], "Project"))
                projects_appended.append(p[0])

        courses_appended = []
        for c in self.courses:
            if c[0] not in courses_appended:
                self.count_main_items += 1
                self.treeview.insert("", 999999, text=str(self.count_main_items),
                                     values=(c[0], "Course"))
                courses_appended.append(c[0])
        self.treeview.grid(row=7, column=0, columnspan=5, padx=20, pady=10, sticky=EW)
        # for item in self.detached:
        #     self.treeview.reattach(item[0], "", item[1])

    def addCate(self):
        # addedCate = Button(self.mainPage, )
        print("here")
        self.num_cate += 1
        catStr = StringVar()
        catStr.set("Please Select a Category")
        # catOptions = ["Computing for Good", "Doing Good for Your Neighborhood"]

        catOptions = ["computing for good", "doing good for your neighborhood", "reciprocal teaching and learning",
                      "urban development", "adaptive learning", "technology for social good", "sustainable communities",
                      "crowd-sourced", "collaborative action"]
        catDropDown = OptionMenu(self.mainPage, catStr, *catOptions)
        catDropDown.config(width=30)
        catDropDown.grid(row=1 + self.num_cate, column=3, padx=20, pady=5, sticky=W + E)
        self.catStrList.append(catStr)
        if self.num_cate > 2:
            self.projRadBTN.grid(row=4 + self.num_cate - 2, column=2)
            self.courseRadBTN.grid(row=4 + self.num_cate - 2, column=3)
            self.bothRadBTN.grid(row=4 + self.num_cate - 2, column=4)
            self.appFilter.grid(row=5 + self.num_cate - 2, column=3, padx=20, pady=10, sticky=E)
            self.resFilter.grid(row=5 + self.num_cate - 2, column=4, padx=20, pady=10, sticky=E)
            self.treeview.grid(row=6 + self.num_cate - 2, column=0, columnspan=5, padx=20, pady=10, sticky=EW)

    def updateProfile(self):
        major = self.major.get()
        year = self.year.get()
        try:
            # Update Major
            try:
                db = self.connect()
            except:
                messagebox.showinfo('Cannot Connect', 'Please check your internet connection!')
                return
            if major != 'Please Select a Major':
                self.databaseHandler.change_major(db, self.username_logged_in, major)

            # Update Year
            try:
                db = self.connect()
            except:
                messagebox.showinfo('Cannot Connect', 'Please check your internet connection!')
                return
            if year != "Please Select a Year":
                self.databaseHandler.change_year(db, self.username_logged_in, year)


            # update these in the database
            print("shabi")
            messagebox.showinfo("Success", "Your Profile Has Been Updated")
        except:
            messagebox.showerror("ERROR", "An Unknown Error Has Occured")

    def apply(self):
        status = "Pending"
        date = datetime.now()
        project_name = self.selectedProjectName
        student_name = self.username_logged_in

        try:
            db = self.connect()
        except:
            messagebox.showinfo('Cannot Connect', 'Please check your internet connection!')
            return
        try:
            self.databaseHandler.apply_project(db, student_name, project_name)

            self.databaseHandler.check_app_reject(student_name, project_name)

            messagebox.showinfo("Success", "You have successfully applied for project: " + project_name)
        except:
            messagebox.showinfo("Failed", "Application Failed. Please check if you have already applied")
    #     Insert these into DB

    def backToMyProfileFromApp(self):
        self.myApp.withdraw()
        self.viewProfile.deiconify()

    def backToMyProfile(self):
        self.editProfilePage.withdraw()
        self.viewProfile.deiconify()

    def backToMain(self):
        self.viewProfile.withdraw()
        self.mainPage.deiconify()

    def backToMainProjectDetail(self):
        self.projectDetail.withdraw()
        self.mainPage.deiconify()

    def backToMainCourseDetail(self):
        self.courseDetail.withdraw()
        self.mainPage.deiconify()

# =================================================================================================================================================
# |                                                     Admin Controller                                                                          |
# =================================================================================================================================================
    def backToChooseFunc(self):
        self.applicationDetails.withdraw()
        self.choose_function.deiconify()
        # editProfileBTN = Button(self.choose_function, text="View Applications", command=self.viewApplications, width=20)
        # editProfileBTN.grid(row=2, column=0, padx=20, pady=10, sticky=EW)
        #
        # myAppBTN = Button(self.choose_function, text="View Popular Project Report", command=self.viewPopularProjects, width=20)
        # myAppBTN.grid(row=3, column=0, padx=20, pady=10, sticky=EW)
        #
        # myAppBTN = Button(self.choose_function, text="View Application Report", command=self.viewApplicationsReport, width=20)
        # myAppBTN.grid(row=4, column=0, padx=20, pady=10, sticky=EW)
        #
        # myAppBTN = Button(self.choose_function, text="Add a Project", command=self.addAProject, width=20)
        # myAppBTN.grid(row=5, column=0, padx=20, pady=10, sticky=EW)
        #
        # myAppBTN = Button(self.choose_function, text="Add a Course", command=self.addACourse, width=20)
        # myAppBTN.grid(row=6, column=0, padx=20, pady=10, sticky=EW)

    def logOutAdmin(self):
        self.choose_function.withdraw()
        self.loginWindow.deiconify()
        self.usernameENT.delete(0, 'end')
        self.pwENT.delete(0, 'end')

    def backToChooseFuncPopProject(self):
        self.popularProjects.withdraw()
        self.choose_function.deiconify()

    def backToChooseFuncAppReport(self):
        self.appReport.withdraw()
        self.choose_function.deiconify()

    def backToChooseFuncAddCourse(self):
        self.addCourse.withdraw()
        self.choose_function.deiconify()

    def backToChooseFuncAddProject(self):
        self.addProjectPage.withdraw()
        self.choose_function.deiconify()

    def submitCourse(self):
        courseNum = self.addCourseNumber.get()
        courseName = self.addCourseName.get()
        instructor = self.addInstructor.get()
        designation = self.addCourseDsgStr.get()
        estnostu = self.addEstNoStudent.get()
        # category = self.addDesignation.get()
        categories = []
        for cates in self.catStrListAddCourse:
            categories.append(cates.get())
        try:
            db = self.connect()
        except:
            messagebox.showinfo('Cannot Connect', 'Please check your internet connection!')
            return
        try:
            self.databaseHandler.add_course(db, courseNum, courseName, instructor, designation, estnostu, categories)
            messagebox.showinfo("Success", "Course Successfully Added")
        except:
            messagebox.showerror("ERROR", "An Error Occurred. Please check if the course name already exists")

    def insertProject(self):
        projName = self.projName.get()
        advisor = self.advisorname.get()
        advisorEmail = self.advisorEmail.get()
        description = self.description.get()
        designation = self.dsgStrAddProject.get()
        estnostu = self.estimatedNumber.get()
        majorReq = self.mjrStrAddProject.get()
        yearReq = self.yrStrAddProject.get()
        dept = self.depStrAddProject.get()

        # db, project_name, advisor, advisor_email, description, categories, designation, 
        # estimated_no_students, major_requirement, year_requirement, department_requirement
        all_info = [projName, advisor, advisorEmail, description, designation, estnostu, majorReq, yearReq, dept]
        if "" in all_info or None in all_info or "Please Select" in all_info:
            messagebox.showerror("ERROR", "Please check for null inputs.")
            return
        try:
            db = self.connect()
        except:
            messagebox.showinfo('Cannot Connect', 'Please check your internet connection!')
            return
        categories = []
        for c in self.catStrListAddProject:
            categories.append(c.get())
        if "Please Select" in categories:
            messagebox.showerror("ERROR", "Please check for null inputs.")
            return

        try:
            self.databaseHandler.add_project(db, projName, advisor, advisorEmail, description, categories, 
                                        designation, estnostu, majorReq, yearReq, dept)
            messagebox.showinfo("Success", "Project Added")
        except:
            messagebox.showerror("ERROR", "An Error Occurred. Please check if the project name already exists")
        # print (projName, advisor, advisorEmail, description, designation, estnostu, majorReq, yearReq, dept)
        
    def addCateAddCourse(self):
        # addedCate = Button(self.mainPage, )
        print("here")
        self.cate_num_add_course += 1
        catStr = StringVar()
        catStr.set("Please Select a Category")
        # catOptions = ["Computing for Good", "Doing Good for Your Neighborhood"]

        catOptions = ["computing for good", "doing good for your neighborhood", "reciprocal teaching and learning",
                      "urban development", "adaptive learning", "technology for social good", "sustainable communities",
                      "crowd-sourced", "collaborative action"]
        catDropDown = OptionMenu(self.addCourse, catStr, *catOptions)
        catDropDown.config(width=30)
        catDropDown.grid(row= 5 + self.cate_num_add_course, column=1, padx=20, pady=5, sticky=W)
        self.catStrListAddCourse.append(catStr)

        self.estStudentLB.grid(row=6 + self.cate_num_add_course, column=0, padx=20, pady=10, sticky=W)
        self.estNoStudentENT.grid(row=6 + self.cate_num_add_course, column=1, padx=20, pady=10, sticky=W)
        self.addCourseBackBTN.grid(row=7 + self.cate_num_add_course, column=0, padx=20, pady=10, sticky=E)
        self.addCourseSubmitBTN.grid(row=7 + self.cate_num_add_course, column=1, padx=20, pady=10, sticky=E)

    def addCateAddProject(self):
        self.cate_num_add_project += 1
        catStr = StringVar()
        catStr.set("Please Select a Category")

        catOptions = ["computing for good", "doing good for your neighborhood", "reciprocal teaching and learning",
                      "urban development", "adaptive learning", "technology for social good", "sustainable communities",
                      "crowd-sourced", "collaborative action"]
        catDropDown = OptionMenu(self.addProjectPage, catStr, *catOptions)
        catDropDown.config(width=30)
        catDropDown.grid(row= 5 + self.cate_num_add_project, column=1, padx=40, pady=5, sticky=EW)
        self.catStrListAddProject.append(catStr)

        self.designLabel.grid(row = 6+self.cate_num_add_project, column = 0, pady = 10, padx = 40, sticky = EW)
        self.desigDropDown.grid(row = 6+self.cate_num_add_project, column = 1, pady = 10, padx = 40, sticky = EW)
        self.estimateLabel.grid(row = 7+self.cate_num_add_project, column = 0, pady = 10, padx = 40, sticky = EW)
        self.estimatedNumberEntry.grid(row = 7+self.cate_num_add_project, column = 1, pady = 10, padx = 40, sticky = EW)
        self.majorLabel.grid(row = 8+self.cate_num_add_project, column  = 0, pady = 10, padx = 40, sticky = EW)
        self.mjrDropDown.grid(row = 8+self.cate_num_add_project, column = 1, padx = 40, pady = 10, sticky = EW)
        self.yearLabel.grid(row = 9+self.cate_num_add_project, column  = 0, pady = 10, padx = 40, sticky = EW)
        self.yrDropDown.grid(row = 9+self.cate_num_add_project, column = 1, padx = 40, pady = 10, sticky = EW)
        self.depLabel.grid(row = 10+self.cate_num_add_project, column  = 0, pady = 10, padx = 40, sticky = EW)
        self.depDropDown.grid(row = 10+self.cate_num_add_project, column = 1, pady = 10, padx = 40, sticky = EW)
        self.backBTNAddProject.grid(row=11+self.cate_num_add_project, column = 0, padx=40, pady=10, sticky = EW)
        self.submitProject.grid(row=11+self.cate_num_add_project, column = 1, padx=40, pady=10, sticky = EW)

    def accept(self):

        project_name = self.treeviewAppAdmin.set(self.treeviewAppAdmin.selection(), column=0)
        username = self.treeviewAppAdmin.set(self.treeviewAppAdmin.selection(), column=1)
        # try:
        #     db = self.connect()
        # except:
        #     messagebox.showinfo('Cannot Connect', 'Please check your internet connection!')
        #     return
        self.databaseHandler.approve_app(project_name, username)
        messagebox.showinfo("Success", "Approved")

    def reject(self):
        project_name = self.treeviewAppAdmin.set(self.treeviewAppAdmin.selection(), column=0)
        username = self.treeviewAppAdmin.set(self.treeviewAppAdmin.selection(), column=1)
        # try:
        #     db = self.connect()
        # except:
        #     messagebox.showinfo('Cannot Connect', 'Please check your internet connection!')
        #     return
        self.databaseHandler.reject_app(project_name, username)
        messagebox.showinfo("Success", "Rejected")
        pass
win = Tk()
start = Courses_n_Projects(win)
win.mainloop()
