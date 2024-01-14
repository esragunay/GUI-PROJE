from http import HTTPStatus
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QLineEdit, QCommandLinkButton, QVBoxLayout,QStackedWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
from PyQt6 import QtWidgets
from login_form2 import Ui_Form
from register_form import Ui_MainWindow
from teacher_login import Ui_Form1
from anaSayfa_student2 import Ui_MainWindow2
from pymongo import MongoClient
from anaSayfa_teacher import Ui_MainWindow3
import webbrowser
import yeni1
import yeni2
class Form(QWidget):
    def __init__(self):
        super().__init__()
        self.mail=None
        self.usernameRegister=None
        self.passwordRegister=None
        self.toolButton_teacher=None
        self.toolButton_student=None
        self.show_password_checkbox_register=None

        self.login_btn = None
        self.teacher_btn = None
        self.show_password_checkbox= None
        self.password = None
        self.username = None

        self.login_teacher=None
        self.usernameTeacher=None
        self.passwordTeacher=None
        self.show_password_checkbox_teacher=None

        self.logout_student=None
        self.username_info_student=None
        self.lineEdit_newUserName=None


        self.comboBox_il = None
        self.comboBox_ilce = None


        self.commandlink=None
        self.commandlink_teacher=None
        self.commandLinkButton_student = None

        self.ui_login_form2= None
        self.ui_register_form=None
        self.ui_teacher_login=None
        self.ui_anaSayfa_student=None
        self.ui_anaSayfa_teacher=None
        self.init_ui()
    
    def init_ui(self):
        self.login_form_open = True
        self.ui_login_form2=Ui_Form()
        self.ui_login_form2.setupUi(self)

        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['Login_Student']
        self.users_collection_student = self.db['Student_username_password']

        self.users_collection_teacher=self.db['Teacher_username_password']

        self.users_collection = self.db["ilceler"]



        self.username=self.ui_login_form2.lineEdit_username
        self.password=self.ui_login_form2.lineEdit_password
        self.login_btn=self.ui_login_form2.pushButton_login
        self.teacher_btn = self.ui_login_form2.pushButton_login_teacher
        self.show_password_checkbox=self.ui_login_form2.check_button_password
        self.commandlink=self.ui_login_form2.commandLinkButton


        self.login_btn.clicked.connect(self.login_form2)
        self.commandlink.clicked.connect(self.other_window)
        self.password.returnPressed.connect(self.login_form2)
        self.username.returnPressed.connect(self.login_form2)
        self.teacher_btn.clicked.connect(self.teacher_window)
        self.show_password_checkbox.stateChanged.connect(self.toggle_pwd_visibility)

    def anaSayfa_student(self):
        self.login_form_open=False
        self.window=QtWidgets.QMainWindow()
        self.ui=Ui_MainWindow2()
        self.ui.setupUi(self.window)
        self.commandLinkButton_student=self.ui.commandLinkButton_video
        self.logout_student=self.ui.pushButton_logout
        self.logout_student.clicked.connect(self.student_logout)
        self.ui.label_username.setText(self.username.text())

        self.il = self.ui.comboBox_il
        self.ilce = self.ui.comboBox_ilce
        self.iller = self.users_collection.find({}, {"il": 1, "_id": 0})
        self.il.addItem("İl Seçiniz...")
        for il in self.iller:
            self.il.addItem(il["il"])
        self.il.currentIndexChanged.connect(self.il_changed)
        self.ilce.currentIndexChanged.connect(self.ilce_changed)
        self.window.show()



    def il_changed(self, index):
        selected_il = self.il.itemText(index)
        ilce_data = self.users_collection.find_one({"il": selected_il}, {"ilceler": 1, "_id": 0})
        
        if ilce_data and "ilceler" in ilce_data:
            self.ilce.clear()
            self.ilce.addItems(ilce_data["ilceler"])
        else:
            self.ilce.clear()
    def ilce_changed(self,index):
        selected_ilce = self.ilce.itemText(index)
        ogretmen_bilgisi = self.get_ogretmen_bilgisi(selected_ilce)
        

        if ogretmen_bilgisi:
            ogretmen_adi = ogretmen_bilgisi[0]["Ogretmen Adi"]
            ogretmen_soyadi = ogretmen_bilgisi[0]["Ogretmen Soyadi"]
            uzmanlik_alani = ogretmen_bilgisi[0]["Uzmanlık Alani"]
            yorum = ogretmen_bilgisi[0]["Yorum"]

            self.ui.label.setText(f"{ogretmen_adi}")
            self.ui.label_2.setText(f"{ogretmen_soyadi}")
            self.ui.label_3.setText(f"{uzmanlik_alani}")
            self.ui.label_5.setText(f"{yorum}")
            self.commandLinkButton_student.clicked.connect(self.link)
        else:
            self.ui.label.setText("Öğretmen Bulunamadı")
            self.ui.label.clear()
            self.ui.label_2.clear()
            self.ui.label_3.clear()
            self.ui.label_5.clear()

    def link(self,index):
        selected_ilce = self.ilce.itemText(index)
        ogretmen_bilgisi = self.get_ogretmen_bilgisi(selected_ilce)
        ogretmen_adi = ogretmen_bilgisi[0]["Ogretmen Adi"]
    
        if ogretmen_adi == "Murat":
            url = "https://www.youtube.com/watch?v=1D-vOoso0oQ&list=PLKnjBHu2xXNP6Qa6u8GLawPnzo1brHZPP"
            webbrowser.open(url)



    def get_ogretmen_bilgisi(self, ilce):
        document = self.users_collection.find_one({"ilceler." + ilce: {"$exists": True}})
        if document:
            return document["ilceler"][ilce]





    def anaSayfa_teacher(self):
        self.login_form_open=False
        self.window=QtWidgets.QMainWindow()
        self.ui=Ui_MainWindow3()
        self.ui.setupUi(self.window)
        self.window.show()

    def student_logout(self):
        QMessageBox.warning(self,'Exit','Uygulamadan cikis yapiliyor...')
        sys.exit()


    def login_form2(self):
        username=self.username.text().strip()
        password=self.password.text().strip()
        if self.users_collection_student.find_one({"username":username, "password":password}):
            QMessageBox.information(self,'Giris Basarili','Anasayfaya Yönlendiriliyor...')
            my_form.hide()
            self.anaSayfa_student()
        else:
            QMessageBox.warning(self,'Giris Basarisiz','Lütfen Gecerli Kullanıcı Adı ve Şifre Giriniz.')

    def login_Teacher(self):
        username=self.usernameTeacher.text().strip()
        password=self.passwordTeacher.text().strip()
        
        if self.users_collection_teacher.find_one({"username":username,"password":password}):
            QMessageBox.information(self,'Giris Basarili','Anasayfaya Yönlendiriliyor...')
            self.anaSayfa_teacher()

        else:
            QMessageBox.warning(self,'Giris Basarisiz','Lütfen Gecerli Kullanıcı Adı ve Şifre Giriniz.')


    def toggle_pwd_visibility(self):
        if self.show_password_checkbox.isChecked():
            self.password.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password.setEchoMode(QLineEdit.EchoMode.Password)
    
    def toggle_pwd_visibility_register(self):
        if self.show_password_checkbox_register.isChecked():
            self.passwordRegister.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.passwordRegister.setEchoMode(QLineEdit.EchoMode.Password)

    def toggle_pwd_visibility_register_teacher(self):
        if self.show_password_checkbox_teacher.isChecked():
            self.passwordTeacher.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.passwordTeacher.setEchoMode(QLineEdit.EchoMode.Password)
    
    def tool_student(self):
        if self.usernameRegister.text()=='' and self.passwordRegister.text()=='':
            QMessageBox.warning(self,'Basarisiz','Gecerli username ve password giriniz.')
        else:
            QMessageBox.information(self,'Basarili','Kayit Basarili') 
            self.anaSayfa_student()    
    def tool_teacher(self):
        if self.usernameRegister.text()=='' and self.passwordRegister.text()=='':
            QMessageBox.warning(self,'Basarisiz','Geçerli username ve password giriniz')
        else:
            QMessageBox.information(self,'Basarili','Kayit Basarili')
            self.anaSayfa_student()
    
    def other_window(self):
        self.login_form_open = False
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.usernameRegister = self.ui.lineEdit_username_2
        self.mail = self.ui.lineEdit_mailadress
        self.passwordRegister = self.ui.lineEdit_password_2
        self.toolButton_student = self.ui.toolButton_student

        my_form.hide()
        teacher_form = self.window
        teacher_form.hide()
        self.toolButton_student.clicked.connect(self.register_student_control)
        self.toolButton_teacher = self.ui.toolButton_teacher
        self.toolButton_teacher.clicked.connect(self.register_teacher_control)
        self.show_password_checkbox_register = self.ui.check_button_password_2
        self.show_password_checkbox_register.stateChanged.connect(self.toggle_pwd_visibility_register)
        self.window.show()


    def teacher_window(self):
        self.login_form_open = False
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Form1()
        self.ui.setupUi(self.window)
        self.usernameTeacher = self.ui.lineEdit_username_teacher
        self.passwordTeacher = self.ui.lineEdit_password_teacher
        self.login_teacher=self.ui.pushButton_login_teacher
        my_form.hide()
        self.login_teacher.clicked.connect(self.login_Teacher)
        self.commandlink_teacher=self.ui.commandLinkButton_teacher
        self.commandlink_teacher.clicked.connect(self.other_window)
        self.show_password_checkbox_teacher = self.ui.check_button_password_teacher
        self.show_password_checkbox_teacher.stateChanged.connect(self.toggle_pwd_visibility_register_teacher)
        self.window.show()
 

    def register_student_control(self):
        self.username2=self.usernameRegister.text().strip()
        self.password2=self.passwordRegister.text().strip()
        mail=self.mail.text().strip()
        user_data={
            "username": self.username2,
            "password": self.password2,
            "email": mail
        }

        if self.usernameRegister.text()==''  or self.passwordRegister.text()=='' or self.mail.text()=='':
            QMessageBox.warning(self,'Lütfen Gecerli Alanlari Doldurunuz...')
        elif "@" not in self.mail.text() and ".com" not in self.mail.text():
            QMessageBox.warning(self,'Lütfen geçerli mail hesabi giriniz.','Basarisiz')
        else:
            QMessageBox.information(self,'Öğrenci Kayidi Basarili','Kayit Basarili')

        self.users_collection_student.insert_one(user_data)
        QMessageBox.information(self,"Kayit Basarili","Basarili")
        my_form.show()

    def register_teacher_control(self):

        username2=self.usernameRegister.text().strip()
        password2=self.passwordRegister.text().strip()
        mail=self.mail.text().strip()
        user_data={
            "username": username2,
            "password": password2,
            "email": mail
        }

        if self.usernameRegister.text()==''  or self.passwordRegister.text()=='' or self.mail.text()=='':
            QMessageBox.warning(self,'Lütfen Gecerli Alanlari Doldurunuz...')
        elif "@" not in self.mail.text() and ".com" not in self.mail.text():
            QMessageBox.warning(self,'Lütfen geçerli mail hesabi giriniz.','Basarisiz')
        else:
            self.users_collection_teacher.insert_one(user_data)
            QMessageBox.information(self,"Kayit Basarili","Basarili")
            my_form.show()

    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    my_form = Form()
    my_form.show()
    sys.exit(app.exec())

