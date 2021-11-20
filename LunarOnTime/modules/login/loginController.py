import os
import tkinter.messagebox as tkmsg
from modules.BaseController import BaseController
from modules.home.homeController import HomeController
from modules.home.homeView import HomeView
from modules.login.loginView import LoginForm


class LoginController(BaseController):
    def __init__(self) -> None:
        self.view = None

    def bind(self, view: LoginForm):
        self.view = view
        self.view.initView(None)
        self.view.buttons["login"].configure(command=self.btnLogin)


    def btnLogin(self):
        userName = self.view.entries["username"].get()
        password = self.view.entries["password"].get()
        if userName == "" or password == "":
            tkmsg.showerror(title="Lỗi đăng nhập", message=f"Vui lòng nhập tên đăng nhập và mật khẩu")
        else:
            self.view.close()
            homeController = HomeController()
            homeController.bind(HomeView(self.view.getRootView()))

