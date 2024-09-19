
import sys
from PyQt6.uic import loadUi
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import *
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel,QMessageBox
from PyQt6.QtCore import QMimeData
from PyQt6.QtGui import QDrag
from PyQt6.QtWidgets import QMainWindow, QFrame 
from PyQt6.QtCore import QPointF
from PyQt6.QtCore import QDate
from PyQt6.QtCore import pyqtSignal
import iconsImage


all_class = [
           {'ClassName': 'Math', 'ClassLimit': 10},
           {'ClassName': 'Science', 'ClassLimit': 15}
]
all_student = [
            {'FullName': 'John Doe', 'Date': '2005-09-15', 'ClassId':'Math'},
            {'FullName': 'Jane Smith', 'Date': '2004-05-22','ClassId':'Math'},
            {'FullName': 'Jevm', 'Date': '2005-09-15', 'ClassId':'Science'},
            {'FullName': 'Sekko ', 'Date': '2005-01-15', 'ClassId':'None'},
        ]
all_user = {'a': '12345678'}  # Dictionary to store users, format: {userName: password}

class LoginSignUpWindow(QMainWindow):
    def __init__(self):
        super(LoginSignUpWindow, self).__init__()
        loadUi("FinalSignInSignUp.ui", self)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        # Connect buttons
        self.btnClose.clicked.connect(self.close)
        self.btnMinimize.clicked.connect(self.showMinimized)
        self.btnSignUp.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.SignUpPage))
        self.btnLogIn_3.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.SignInPage))
        self.lblCreateAccount.mousePressEvent = self.on_lblCreateAccount_clicked
        self.btnClose_2.clicked.connect(self.close)
        self.btnMinimize_2.clicked.connect(self.showMinimized)
        self.btnRegister.clicked.connect(self.addUserToDB)

        self.btnLogInTo.clicked.connect(self.LoggingIn)

        # Set the current widget to the sign-in page
        self.stackedWidget.setCurrentWidget(self.SignInPage)

    # Moving to SignUp Page by clicking Create Account link
    def on_lblCreateAccount_clicked(self):
        self.stackedWidget.setCurrentWidget(self.SignUpPage)

    # Method to add a new user to the simulated database
    def addUserToDB(self):
        # Get user input from text fields
        userName = self.txtUserName_2.text()
        cPassword = self.txtConfirmPassword.text()
        password = self.txtPassword_2.text()

        # Check if user already exists
        if userName in all_user:
            self.lblUserNameError.setText("UserName Already Exists")
        else:
            self.lblUserNameError.setText("")
            if len(password) >= 8 and len(cPassword) >= 8:
                if password == cPassword:
                    # Add the new user to the "database"
                    all_user[userName] = password

                    # Show success message and reset text fields
                    QMessageBox.information(self, "Success", "User added successfully!")
                    self.txtUserName_2.setText("")
                    self.txtConfirmPassword.setText("")
                    self.txtPassword_2.setText("")
                    self.lblPasswordError.setText("")
                    self.lblConfirmPasswordError.setText("")
                    self.lblUserNameError.setText("")
                    self.resetValues()
                else:
                    self.lblPasswordError.setText("")
                    self.lblConfirmPasswordError.setText("*Password should be the same")
            else:
                self.lblPasswordError.setText("*Minimum of 8 Characters")
                self.lblConfirmPasswordError.setText("*Minimum of 8 Characters")

    # Method to log in a user
    def LoggingIn(self):
        # Get user input from text fields
        userName = self.txtUserNameLogIn.text()
        password = self.txtPasswordLogIn.text()

        # Check if the user exists and the password matches
        if userName in all_user and all_user[userName] == password:
            # Authentication successful
            self.current_user = userName  # Store the username as current user
            print("Authentication successful, opening next window...")
            self.NewWindow(self.current_user)

        else:
            # Authentication failed
            print("Authentication failed, please try again.")
            self.lblPassword.setText("*Incorrect UserName or Password")

    # Method to open a new window after successful login
    def NewWindow(self, userName):
        self.close()  # Close the current window
        self.MainWindow = TeacherWindow(userName)
        self.MainWindow.show()

    # Method to reset input fields and errors
    def resetValues(self):
        self.txtUserName_2.clear()
        self.txtConfirmPassword.clear()
        self.txtPassword_2.clear()
        self.lblUserNameError.clear()
        self.lblPasswordError.clear()
        self.lblConfirmPasswordError.clear()


class TeacherWindow(QMainWindow):
    def __init__(self, teacherId):
        CurrentId = teacherId
        self.btnClicked = None
        super(TeacherWindow, self).__init__()
        loadUi("AdminMainPage.ui", self)
        self.stackedWidget.setCurrentWidget(self.HomePage)
        
        self.showingAllClasses(CurrentId)
        self.fillClassTable(CurrentId)
        self.fillStudentTable()

        # Button connections
        self.btnMenuClass.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.ClassPage))
        self.btnHomeMenu.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.HomePage))
        self.btnStudent.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.StudentPage))

        self.btnHomeMenu.clicked.connect(lambda: self.showingAllClasses(CurrentId))
        self.btnMenuClass.clicked.connect(lambda: self.fillClassTable(CurrentId))
        self.btnStudent.clicked.connect(lambda: self.fillStudentTable())
        self.btnLogOut.clicked.connect(lambda: self.logOut())
        self.btnAddNewClass.clicked.connect(lambda: self.addNewClass(CurrentId))
        self.btnAddNewStudent.clicked.connect(lambda: self.addNewStudent(CurrentId))

    def logOut(self):
        self.close()
        self.SignInSignUp = LoginSignUpWindow()
        self.SignInSignUp.show()

    def fillStudentTable(self):
        # Fetch student data from the simulated database
        rows = all_student
        
        self.tableStudentData.setRowCount(len(rows))
        self.tableStudentData.setColumnCount(3)  # Only two columns now
        self.tableStudentData.horizontalHeader().setVisible(True)
        self.tableStudentData.setHorizontalHeaderLabels(['Full Name', 'Date of Birth', 'Class'])
        self.tableStudentData.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableStudentData.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        
        # Insert the data into the table
        for i, row in enumerate(rows):
            self.tableStudentData.setItem(i, 0, QTableWidgetItem(row['FullName']))
            self.tableStudentData.setItem(i, 1, QTableWidgetItem(row['Date']))
            self.tableStudentData.setItem(i, 2, QTableWidgetItem(row['ClassId']))


    def fillClassTable(self, CurrentId):
    # Fetch class data for the given teacher from the simulated database
        rows = [(class_info['ClassName'], class_info['ClassLimit']) for class_info in all_class]
        
        self.tableAllClasses.setRowCount(len(rows))
        self.tableAllClasses.setColumnCount(2)
        self.tableAllClasses.horizontalHeader().setVisible(True)
        self.tableAllClasses.setHorizontalHeaderLabels(['Class Name', 'Limit of Students'])
        self.tableAllClasses.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableAllClasses.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

        # Insert the data into the table
        for i, row in enumerate(rows):
            for j, col in enumerate(row):
                self.tableAllClasses.setItem(i, j, QTableWidgetItem(str(col)))


    def clearHomePage(self):
        for child in reversed(self.HomePage.children()):
            if not isinstance(child, QVBoxLayout):
                child.deleteLater()

    def showingAllClasses(self, CurrentId):
        self.clearHomePage()
        lbl = QLabel("No classes found")
        lbl.setStyleSheet('color: rgb(77, 78, 186);font-size: 20pt;')

        layout = self.HomePage.layout()
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.setSpacing(20)
        
        classes = [cls['ClassName'] for cls in all_class]
        for cls in classes:
            lbl.setText("")
            btn = QPushButton(cls)
            btn.setStyleSheet('background-color: rgb(77, 78, 186); color: white;font-size: 14pt;')
            btn.setFixedWidth(250)
            layout.addWidget(btn)

        def on_button_clicked():
            self.btnClicked = self.sender()
            self.classDetails(CurrentId, self.btnClicked.text())
            

        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if isinstance(widget, QPushButton):
                widget.clicked.connect(on_button_clicked)


    def classDetails(self, CurrentId, btnName):
        self.Class = ClassDetailsWindow(CurrentId, btnName)
        self.Class.show()

    def addNewClass(self, idx):
        self.Class = AddNewClass(idx)
        self.Class.show()
        self.Class.btnAdd.clicked.connect(lambda: self.fillClassTable(idx))
        self.Class.btnCancel.clicked.connect(lambda: self.fillClassTable(idx))

    def addNewStudent(self, idx):
        self.Class = AddNewStudent(idx)
        self.Class.show()
        self.Class.btnAdd.clicked.connect(lambda: self.fillStudentTable())
        self.Class.btnCancel.clicked.connect(lambda: self.fillStudentTable())

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragPos = event.globalPosition() - QPointF(self.pos())
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition() - self.dragPos)
            event.accept()


class AddNewClass(QMainWindow):
    def __init__(self, idx):

        # idx: current user id
        self.currentId = idx
        
        # Call the superclass constructor
        super(AddNewClass, self).__init__()
        
        # Load the user interface from the .ui file
        loadUi("AddNewClass.ui", self)
        
        # Connect the 'Cancel' button to the 'close' method of the window
        self.btnCancel.clicked.connect(self.close)
        
        # Set the validator for the 'Class Limit' text field to only accept integer values
        self.txtClassLimitStudent.setValidator(QIntValidator())
        
        # Connect the 'Add' button to the 'addNewClassToDB' method
        self.btnAdd.clicked.connect(self.addNewClassToDB)
    
    def addNewClassToDB(self):
        className = self.txtClassName.text()
        limit = int(self.txtClassLimitStudent.text())
        rowLimit = int(self.txtRowsStudent.text())

        if className != "" and limit > 0:
            if limit <= 20:
                # Append the class data to the list instead of inserting into a database
                all_class.append({
                    "ClassName": className,
                    "ClassLimit": limit,
                    "StudentInOneRow": rowLimit,
                    "TeacherId": self.currentId
                })
                
                QMessageBox.information(self, "Success", "Class added successfully!")
                self.txtClassName.setText("")
                self.txtClassLimitStudent.setText("")
                self.txtRowsStudent.setText("")
            else:
                self.lblLimitError.setText("*Limit Should be less than 20")

  
# Example data structure to store class and student information


class ClassDetailsWindow(QMainWindow):
    def __init__(self, idx, btnName):
        self.teacherName = idx
        self.btnName = btnName
        super(ClassDetailsWindow, self).__init__()
        loadUi("ClassStudents.ui", self)
        self.btnAddStudentToClass.clicked.connect(self.addingStudentToClass)
        self.fillStudent()

    def addingStudentToClass(self):
        self.new = AddStudentToClass(self.btnName, all_student, self.fillStudent)
        self.new.studentAdded.connect(self.fillStudent)  # Refresh the student list when a new student is added
        self.new.show()
        loadUi("ClassStudents.ui", self)
        self.btnAddStudentToClass.clicked.connect(self.addingStudentToClass)


    def clearStudentPage(self):
        # Clear all widgets from the RegisteredStudent frame
        if self.RegisteredStudent.layout() is not None:
            # Remove all widgets in the layout
            while self.RegisteredStudent.layout().count():
                item = self.RegisteredStudent.layout().takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            # Remove the layout itself
            self.RegisteredStudent.layout().deleteLater()


    def fillStudent(self):
        # Clear the previous student list
        self.clearStudentPage()

        # Retrieve student data from all_student list
        enrolled_students = [student for student in all_student if student["ClassId"] == self.btnName]

        # Create a grid layout with 2 columns
        grid = QGridLayout()
        num_columns = 2

        # Create and add labels for each student with a profile picture and name label
        for i, student in enumerate(enrolled_students):
            row = i // num_columns
            col = i % num_columns
            student_frame = QFrame()
            student_frame_layout = QVBoxLayout(student_frame)

            # Create a profile pic widget with a default image
            profile_pic = QLabel()
            profile_pic.setPixmap(QPixmap("Profile.png"))  # Use student's profile picture
            profile_pic.setFixedSize(80, 80)
            # profile_pic.setAlignment(Qt.AlignmentFlag.AlignCenter)
            student_frame_layout.addWidget(profile_pic)

            # Create a label for the student name
            name_label = QLabel(student["FullName"])
            # name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            name_label.setContentsMargins(10, 0, 10, 0)
            student_frame_layout.addWidget(name_label)

            # Add a "Remove" button for each student
            btnRemoveStudent = QPushButton("Remove")
            btnRemoveStudent.clicked.connect(lambda _, s=student["FullName"]: self.removeStudentFromClass(s))
            btnRemoveStudent.setFixedWidth(100)
            student_frame_layout.addWidget(btnRemoveStudent)

            student_frame.setMouseTracking(True)

            # Make the student frame clickable and connect to the handleProfileClick function
            student_frame.setCursor(Qt.CursorShape.PointingHandCursor)

            # Create the mouse press event handler
            def handle_mouse_press(event, sid):
                self.handleProfileClick(sid)
                self.startDrag(student_frame, event)

            # Connect the mousePressEvent to the handle_mouse_press function
            student_frame.mousePressEvent = lambda event, sid=student["FullName"]: handle_mouse_press(event, sid)

            grid.addWidget(student_frame, row, col)

        # Create a widget to hold the grid and add it to the RegisteredStudent layout
        grid_widget = QWidget()
        grid_widget.setLayout(grid)

        # Get the layout of RegisteredStudent, and if it doesn't exist, create a new one
        seats_layout = self.RegisteredStudent.layout()
        if seats_layout is None:
            seats_layout = QVBoxLayout(self.RegisteredStudent)
            self.RegisteredStudent.setLayout(seats_layout)

        # Clear the existing layout content
        while seats_layout.count():
            item = seats_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Add the new grid_widget to the layout
        seats_layout.addWidget(grid_widget)

    def startDrag(self, frame, event):
        self.current_student = frame
        mime_data = QMimeData()
        pixmap = QPixmap("ProfileDrag.png")
        drag = QDrag(frame)
        drag.setMimeData(mime_data)
        drag.setPixmap(pixmap)
        drag.exec(Qt.DropAction.MoveAction)

    def handleProfileClick(self, student_id):
        student = next((stu for stu in all_student if stu["FullName"] == student_id), None)
        if student:
            self.lblName.setText(student["FullName"])
            self.lblDate.setText(student["Date"])

    def removeStudentFromClass(self, student_name):
        student = next((s for s in all_student if s['FullName'] == student_name), None)
        if student:
            student['ClassId'] = 'None'
            QMessageBox.information(self, "Removed", f"{student_name} has been removed from {self.btnName}.")
            loadUi("ClassStudents.ui", self)
            self.btnAddStudentToClass.clicked.connect(self.addingStudentToClass)
            self.fillStudent()



class AddStudentToClass(QMainWindow): 
    studentAdded = pyqtSignal()  # Custom signal to indicate a student was added

    def __init__(self, Id, all_student, fillStudent):
        self.ClassId = Id  # Class name (e.g., 'Math')
        self.all_student = all_student
        self.fillStudent = fillStudent
        super(AddStudentToClass, self).__init__()
        loadUi("AddStudentToClass.ui", self)
        self.fillStudentTable()

    def fillStudentTable(self):
        # Filter students not enrolled in the current class
        students_not_enrolled = [s for s in self.all_student if s['ClassId'] == 'None']

        self.tableStudentData.setRowCount(len(students_not_enrolled))
        self.tableStudentData.setColumnCount(3)  # Reduced column count
        self.tableStudentData.setHorizontalHeaderLabels(['Add', 'Full Name', 'Added Date'])

        for i, student in enumerate(students_not_enrolled):
            button = QPushButton('Add')
            button.clicked.connect(lambda _, row=i: self.addRowData(row))  # Connect button click
            self.tableStudentData.setCellWidget(i, 0, button)
            self.tableStudentData.setItem(i, 1, QTableWidgetItem(student['FullName']))
            self.tableStudentData.setItem(i, 2, QTableWidgetItem(student['Date']))

    def addRowData(self, row):
        # Get selected student's full name
        student_name = self.tableStudentData.item(row, 1).text()
        # Find the student in the database
        student = next(s for s in self.all_student if s['FullName'] == student_name)
        self.addStudentToClass(student)

    def addStudentToClass(self, student):
        # Update student's ClassId to the selected class
        student['ClassId'] = self.ClassId
        QMessageBox.information(self, "Success", f"{student['FullName']} added to {self.ClassId}.")
        self.fillStudentTable()  # Refresh table after adding
        # Emit the signal to notify that a student has been added
        self.studentAdded.emit()



    
class AddNewStudent(QMainWindow):
    def __init__(self, all_student):
        super(AddNewStudent, self).__init__()
        loadUi("AddNewStudent.ui", self)
        self.btnCancel.clicked.connect(lambda: self.close())
        self.btnAdd.clicked.connect(lambda: self.addNewStudentToDB())

    def addNewStudentToDB(self):
        fullName = self.txtFullName.text()
        DOB = self.dateDOB.date().toString("dd-MM-yyyy")

        if fullName != "":
            all_student.append({
                'FullName': fullName,
                'Date': DOB,
                'ClassId': 'None' 
            })
            QMessageBox.information(self, "Success", "New student added successfully!")
            self.txtFullName.setText("")
            self.dateDOB.setDate(QDate(2000, 1, 1))

      
# Define the main function
def main():
    # Create an instance of the QApplication
    app = QApplication(sys.argv)

    # Create an instance of the LoginSignUpWindow and show it
    window = LoginSignUpWindow()
    window.show()

    # Run the application and exit when done
    sys.exit(app.exec())

# Call the main function
if __name__ == "__main__":
    main()