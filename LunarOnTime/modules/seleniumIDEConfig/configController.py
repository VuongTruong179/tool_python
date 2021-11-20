from tkinter import filedialog, END
from base.utils import Utils
import tkinter.messagebox as tkmsg

from modules.BaseController import BaseController
from modules.seleniumIDEConfig.configModel import ProfileExcel
from modules.seleniumIDEConfig.configView import ConfigView


class ConfigController(BaseController):
    def __init__(self) -> None:
        self.view = None
        self.model = ProfileExcel()
        self.listProfile = iter([])
        self.ListKeywords = {}
        self.entriesConfigValues = Utils.readFileJson(r"./config.json")

    def bind(self, view: ConfigView):
        self.view = view
        self.view.initView(self.entriesConfigValues)

        self.view.buttons["btnProfilePath"].configure(command=self.btnProfilePath)
        self.view.buttons["btnWebRTC"].configure(command=self.btnWebRTC)
        self.view.buttons["btnProxyPath"].configure(command=self.btnProxyPath)
        self.view.buttons["btnScriptRun"].configure(command=self.btnScriptRunPath)

        self.view.buttons["btnChromeFile"].configure(command=self.btnChromeFile)
        self.view.buttons["btnKeyPath"].configure(command=self.btnKeyPath)
        self.view.buttons["btnStart"].configure(command=self.btnSaveConfig)

    def btnKeyPath(self):
        destinationDirectory = filedialog.askopenfilenames(initialdir=self.view.entries["keyPath"].get())
        if isinstance(destinationDirectory, tuple):
            destinationDirectory = destinationDirectory[0]
        if destinationDirectory != "":
            self.view.entries["keyPath"].delete(0, END)
            self.view.entries["keyPath"].insert('1', destinationDirectory)
        self.view.autoFocus()

    def btnChromeFile(self):
        destinationDirectory = filedialog.askdirectory(initialdir=self.view.entries["chromePath"].get())
        if isinstance(destinationDirectory, tuple):
            destinationDirectory = destinationDirectory[0]
        if destinationDirectory != "":
            self.view.entries["chromePath"].delete(0, END)
            self.view.entries["chromePath"].insert('1', destinationDirectory)
        self.view.autoFocus()

    def btnProfilePath(self):
        destinationDirectory = filedialog.askdirectory(initialdir=self.view.entries["profilePath"].get())
        if isinstance(destinationDirectory, tuple):
            destinationDirectory = destinationDirectory[0]
        if destinationDirectory != "":
            self.view.entries["profilePath"].delete(0, END)
            self.view.entries["profilePath"].insert('1', destinationDirectory)
        self.view.autoFocus()

    def btnWebRTC(self):
        destinationDirectory = filedialog.askdirectory(initialdir=self.view.entries["webRtcPath"].get())
        if isinstance(destinationDirectory, tuple):
            destinationDirectory = destinationDirectory[0]
        if destinationDirectory != "":
            if self.view.entries["webRtcPath"].get() != "":
                destinationDirectory += ","
            self.view.entries["webRtcPath"].insert('0', destinationDirectory)
        self.view.autoFocus()

    def btnProxyPath(self):
        destinationDirectory = filedialog.askopenfilenames(initialdir=self.view.entries["proxyPath"].get())
        if isinstance(destinationDirectory, tuple):
            destinationDirectory = destinationDirectory[0]
        if destinationDirectory != "":
            self.view.entries["proxyPath"].delete(0, END)
            self.view.entries["proxyPath"].insert('1', destinationDirectory)
        self.view.autoFocus()

    def btnScriptRunPath(self):
        destinationDirectory = filedialog.askopenfilenames(initialdir=self.view.entries["scriptPath"].get())
        if isinstance(destinationDirectory, tuple):
            destinationDirectory = destinationDirectory[0]
        if destinationDirectory != "":
            self.view.entries["scriptPath"].delete(0, END)
            self.view.entries["scriptPath"].insert('1', destinationDirectory)
        self.view.autoFocus()

    def validateEntries(self):
        isvalid = False
        if self.view.entries["profilePath"].get() == "":
            tkmsg.showerror(
                title="Validation Error", message=f"Vui lòng nhập đường dẫn lưu Profile"
            )
        elif self.view.entries["proxyPath"].get() == "":
            tkmsg.showerror(
                title="Validation Error", message=f"Vui lòng nhập đường dẫn file Proxy"
            )
        elif self.view.entries["webRtcPath"].get() == "":
            tkmsg.showerror(
                title="Validation Error", message=f"Vui lòng nhập đường dẫn thư mục Extension"
            )
        elif self.view.entries["proxySheet"].get() == "":
            tkmsg.showerror(
                title="Validation Error", message=f"Vui lòng nhập tên Sheet"
            )
        elif self.view.entries["scriptPath"].get() == "":
            tkmsg.showerror(
                title="Validation Error", message=f"Vui lòng nhập đường dẫn file Script"
            )
        elif int(self.view.entries["maxThread"].get()) <= 0:
            tkmsg.showerror(
                title="Validation Error", message=f"Vui lòng nhập số luồng"
            )
        elif int(self.view.entries["timeDelay"].get()) <= 0:
            tkmsg.showerror(
                title="Validation Error", message=f"Vui lòng nhập thời gian chờ"
            )
        else:
            if self.view.entries["chromePath"].get() != "":
                self.entriesConfigValues["chromePath"] = self.view.entries["chromePath"].get()
            self.entriesConfigValues["keyPath"] = self.view.entries["keyPath"].get()
            self.entriesConfigValues["profilePath"] = self.view.entries["profilePath"].get()
            self.entriesConfigValues["proxyPath"] = self.view.entries["proxyPath"].get()
            self.entriesConfigValues["webRtcPath"] = self.view.entries["webRtcPath"].get()
            self.entriesConfigValues["proxySheet"] = self.view.entries["proxySheet"].get()
            self.entriesConfigValues["scriptPath"] = self.view.entries["scriptPath"].get()
            self.entriesConfigValues["maxThread"] = int(self.view.entries["maxThread"].get())
            self.entriesConfigValues["timeDelay"] = int(self.view.entries["timeDelay"].get())
            isvalid = True
        return isvalid

    def btnSaveConfig(self):
        if self.validateEntries():
            self.ListKeywords = Utils.readFileJson(self.entriesConfigValues["keyPath"])
            Utils.saveFileJson('./config.json', self.entriesConfigValues)
            self.view.close()
