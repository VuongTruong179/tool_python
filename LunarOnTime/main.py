import tkinter as tk

from modules.login.loginController import LoginController
from modules.login.loginView import LoginForm

if __name__ == "__main__":
    root = tk.Tk()
    root.title('Auto Selenium IDE')
    root.configure(background='#f5f5f5')
    # root.wm_attributes("-transparentcolor", 'grey')
    loginController = LoginController()
    loginController.bind(LoginForm(root))

    root.mainloop()
    # End
