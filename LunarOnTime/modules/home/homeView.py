from modules.BaseView import BaseView
import tkinter as tk


class HomeView(BaseView):
    def __init__(self, rootView):
        super().__init__()
        self.rootView = rootView
        self.entries = {}
        self.buttons = {}
        self.listItem = {}
        self.listScript = {}
        self.TotalLine = 9
        self.logView = None
        self.menuBar = None
        self.buttonFrame = None
        self.canvasFrame = None

    def getMaxLine(self):
        return self.TotalLine

    def getRootView(self):
        return self.rootView

    def initView(self, initData):
        self.rootView.maxsize(width=900, height=600)
        self.rootView.minsize(width=900, height=600)
        self.rootView.title('Auto Selenium IDE')
        self.rootView.columnconfigure(2, weight=1)

        self.menuBar = tk.Menu(self.rootView)
        self.buttons["btnStart"] = self.createButton(self.rootView, 0, 0, "Start Auto", "Verdana 10 bold")

    def close(self):
        self.rootView.destroy()

    def refreshLayoutFrame(self):
        self.buttonFrame.update_idletasks()  # Needed to make bbox info available.
        bbox = self.canvasFrame.bbox(tk.ALL)  # Get bounding box of canvas with Buttons.
        # print('canvas.bbox(tk.ALL): {}'.format(bbox))

        # Define the scrollable region as entire canvas with only the desired
        # number of rows and columns displayed.
        # w, h = bbox[2] - bbox[1], bbox[3] - bbox[1]
        # dw, dh = int((w / COLS) * COLS_DISP), int((h / ROWS) * ROWS_DISP)
        ROWS, COLS = 7, 6  # Size of grid.
        ROWS_DISP = 6  # Number of rows to display.
        COLS_DISP = 6  # Number of columns to display.
        w, h = self.rootView.winfo_width() - 30, self.rootView.winfo_height()
        dw, dh = int((w / COLS) * COLS_DISP), int((h / ROWS) * ROWS_DISP)
        self.canvasFrame.configure(scrollregion=bbox, width=dw, height=dh)