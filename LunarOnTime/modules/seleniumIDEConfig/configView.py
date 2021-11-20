from modules.BaseView import BaseView
import tkinter as tk


class ConfigView(BaseView):
    def __init__(self, rootView):
        super().__init__()
        self.rootView = rootView
        self.logView = None
        self.buttonFrame = None
        self.canvasFrame = None
        self.scales = {}
        self.menu = {}
        self.entries = {}
        self.buttons = {}

    def autoFocus(self):
        self.guideWindow.attributes("-topmost", True)

    def getRootView(self):
        return self.rootView

    def getValueFromKey(self, keyName, entriesConfigValues):
        value = entriesConfigValues.get(keyName)
        if value == "None":
            return ""
        else:
            return value

    def initView(self, entriesConfigValues):
        self.guideWindow = tk.Toplevel(self.rootView)
        self.guideWindow.maxsize(width=1020, height=400)
        self.guideWindow.minsize(width=1020, height=400)
        self.guideWindow.title("Cấu hình")
        self.createConfigView(entriesConfigValues)

    def close(self):
        self.guideWindow.destroy()

    def createConfigView(self, entriesConfigValues):
        controlFrame = tk.LabelFrame(self.guideWindow, text="Cấu hình")
        controlFrame.rowconfigure(0, weight=1)
        controlFrame.columnconfigure(0, weight=1)
        controlFrame.grid(row=0, column=0, sticky=tk.S + tk.W)

        # Cột Bên Trái
        self.entries["chromePath"] = self.createEntryInLabel(
            controlFrame, "Nhập đường dẫn Chrome Exe", 0, 0, self.getValueFromKey("chromePath", entriesConfigValues)
        )
        self.buttons["btnChromeFile"] = self.createButton(controlFrame, 0, 1, "Chọn thư mục")

        self.entries["profilePath"] = self.createEntryInLabel(
            controlFrame, "Nhập đường dẫn profile", 1, 0, self.getValueFromKey("profilePath", entriesConfigValues)
        )
        self.buttons["btnProfilePath"] = self.createButton(controlFrame, 1, 1, "Chọn thư mục")

        self.entries["webRtcPath"] = self.createEntryInLabel(
            controlFrame, "Nhập đường dẫn thư mục Extension", 2, 0, self.getValueFromKey("webRtcPath", entriesConfigValues)
        )
        self.buttons["btnWebRTC"] = self.createButton(controlFrame, 2, 1, "Chọn thư mục")

        self.entries["scriptPath"] = self.createEntryInLabel(
            controlFrame, "Nhập đường dẫn file script", 0, 2, self.getValueFromKey("scriptPath", entriesConfigValues)
        )
        self.buttons["btnScriptRun"] = self.createButton(controlFrame, 0, 3, "Chọn file")

        self.entries["keyPath"] = self.createEntryInLabel(
            controlFrame, "Nhập đường dẫn file cấu hình Keywords", 1, 2,
            self.getValueFromKey("keyPath", entriesConfigValues)
        )
        self.buttons["btnKeyPath"] = self.createButton(controlFrame, 1, 3, "Chọn file")

        self.entries["proxyPath"] = self.createEntryInLabel(
            controlFrame, "Nhập đường dẫn file proxy", 2, 2, self.getValueFromKey("proxyPath", entriesConfigValues)
        )
        self.buttons["btnProxyPath"] = self.createButton(controlFrame, 2, 3, "Chọn file")

        # End

        # Cột Bên Phải
        self.entries["maxThread"] = self.createEntryInLabel(
            controlFrame, "Nhập số luồng", 3, 0, self.getValueFromKey("maxThread", entriesConfigValues)
        )
        self.entries["timeDelay"] = self.createEntryInLabel(
            controlFrame, "Nhập thời gian chờ", 3, 1, self.getValueFromKey("timeDelay", entriesConfigValues)
        )
        self.entries["proxySheet"] = self.createEntryInLabel(
            controlFrame, "Nhập tên Sheet Proxy", 3, 2, self.getValueFromKey("proxySheet", entriesConfigValues)
        )
        # End
        self.buttons["btnStart"] = self.createButton(controlFrame, 4, 1, "Lưu cấu hình")
