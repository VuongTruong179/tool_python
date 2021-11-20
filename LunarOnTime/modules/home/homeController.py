import tkinter.messagebox as tkmsg
import tkinter as tk
from modules.BaseController import BaseController
from modules.home.homeView import HomeView
from modules.seleniumIDEConfig.configController import ConfigController
from modules.seleniumIDE.autoSeleController import AutoSeleController
from modules.seleniumIDE.autoSeleView import AutoSeleView
from modules.seleniumIDEConfig.configView import ConfigView
from modules.guide.guideController import GuideController
from modules.guide.guideView import GuideView


class HomeController(BaseController):
    def __init__(self) -> None:
        self.view = None
        self.isRunning = False
        self.isRunningRetweet = False

    def bind(self, view: HomeView):
        self.view = view
        self.view.initView(None)
        self.view.buttons["btnStart"].configure(command=self.btnRunStart)
        self.createMenu()

    def createMenu(self):
        root = self.view.getRootView()
        menubar = tk.Menu(root)
        salutations = tk.Menu(menubar, tearoff=False)
        salutations.add_command(label="Hướng dẫn", command=self.btnShowGuide)
        salutations.add_command(label="Cấu hình Auto", command=self.btnConfig)
        salutations.add_separator()
        salutations.add_command(label="Thoát", command=root.destroy)
        menubar.add_cascade(label="File", menu=salutations)
        root.config(menu=menubar)

    def btnConfig(self):
        configController = ConfigController()
        configController.bind(ConfigView(self.view.getRootView()))

    def btnShowGuide(self):
        guideController = GuideController()
        guideController.bind(GuideView(self.view.getRootView()))

    def btnRunStart(self):
        if self.isRunning:
            tkmsg.showerror(title="Đợi Em Ơi", message=f"Vui lòng đợi các luồng hoàn thành!")
        else:
            self.isRunning = True
            configController = AutoSeleController()
            configController.bind(AutoSeleView(self.view.getRootView()))
