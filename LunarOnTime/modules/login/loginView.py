from modules.BaseView import BaseView


class LoginForm(BaseView):
    def __init__(self, rootView):
        super().__init__()
        self.rootView = rootView
        self.entries = {}
        self.buttons = {}

    def getRootView(self):
        return self.rootView

    def initView(self, initData):
        self.rootView.title("100Capital Tool")

        self.rootView.maxsize(width=450, height=200)
        self.rootView.minsize(width=450, height=200)

        self.createLabel(self.rootView, 0, 1, "Đăng nhập", "Verdana 25 bold")
        self.createLabel(self.rootView, 2, 0, "Tên đăng nhập", "Verdana 10 bold")
        self.createLabel(self.rootView, 4, 0, "Mật khẩu", "Verdana 10 bold")

        self.entries["username"] = self.createEntry(self.rootView, 2, 1, "admin")
        self.entries["password"] = self.createEntry(self.rootView, 4, 1, "admin")

        self.buttons["login"] = self.createButton(self.rootView, 5, 1, "Đăng nhập", "Verdana 10 bold")

    def close(self):
        self.removeAllChild(self.rootView)
