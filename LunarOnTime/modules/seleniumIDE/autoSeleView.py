from modules.BaseView import BaseView
import tkinter as tk


class AutoSeleView(BaseView):
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
        self.seleView = tk.Toplevel(self.rootView)
        self.seleView.maxsize(width=900, height=600)
        self.seleView.minsize(width=900, height=600)
        self.seleView.title('Auto')
        self.seleView.columnconfigure(2, weight=1)

    def close(self):
        self.seleView.destroy()

    def refreshLayoutFrame(self):
        self.buttonFrame.update_idletasks()  # Needed to make bbox info available.
        bbox = self.canvasFrame.bbox(tk.ALL)  # Get bounding box of canvas with Buttons.
        print('canvas.bbox(tk.ALL): {}'.format(bbox))

        # Define the scrollable region as entire canvas with only the desired
        # number of rows and columns displayed.
        # w, h = bbox[2] - bbox[1], bbox[3] - bbox[1]
        # dw, dh = int((w / COLS) * COLS_DISP), int((h / ROWS) * ROWS_DISP)
        ROWS, COLS = 7, 6  # Size of grid.
        ROWS_DISP = 6  # Number of rows to display.
        COLS_DISP = 6  # Number of columns to display.
        w, h = self.seleView.winfo_width() - 30, self.seleView.winfo_height()
        dw, dh = int((w / COLS) * COLS_DISP), int((h / ROWS) * ROWS_DISP)
        self.canvasFrame.configure(scrollregion=bbox, width=dw, height=dh)

    def setValueForItemScript(self, posThread, name, text, color="black"):
        listLabels = self.listItem[posThread]
        label = listLabels[name]
        label['text'] = text
        label.config(fg=color)
        self.refreshLayoutFrame()

    def resetListResultStatus(self, posThread):
        scriptResult = self.listScript[posThread]
        for i in range(self.TotalLine):
            scriptResult["type" + str(i)]['text'] = ""
            scriptResult["code" + str(i)]['text'] = ""
            scriptResult["status" + str(i)]['text'] = ""
        self.refreshLayoutFrame()

    def updateListResultStatus(self, posThread, listResult):
        totalResult = len(listResult)
        if totalResult > self.TotalLine:
            totalResult = self.TotalLine
        scriptResult = self.listScript[posThread]
        for i in range(totalResult):
            scriptResult["type" + str(i)]['text'] = listResult[i]["type"]
            scriptResult["code" + str(i)]['text'] = listResult[i]["code"]
            lbStatus = scriptResult["status" + str(i)]
            if listResult[i]["status"]:
                lbStatus['text'] = "Done"
                lbStatus.config(fg="green")
            else:
                lbStatus['text'] = "Error"
                lbStatus.config(bg="red")
        self.refreshLayoutFrame()

    def removeAllChild(self, viewRoot):
        for child in viewRoot.winfo_children():
            child.destroy()

    def createItemScriptRun(self, numThreads):
        self.logView = tk.Frame(self.seleView, bg="Light Blue", bd=3, relief=tk.RIDGE)
        self.logView.grid(row=1, column=0, sticky=tk.NSEW)
        self.logView.columnconfigure(0, weight=1)

        # Create a frame for the canvas and scrollbar(s).
        frame2 = tk.Frame(self.logView)
        frame2.grid(row=3, column=0, sticky=tk.NW)

        # Add a canvas in that frame.
        self.canvasFrame = tk.Canvas(frame2)
        self.canvasFrame.grid(row=0, column=0)

        # Create a vertical scrollbar linked to the canvas.
        vsbar = tk.Scrollbar(frame2, orient=tk.VERTICAL, command=self.canvasFrame.yview)
        vsbar.grid(row=0, column=1, sticky=tk.NS)
        self.canvasFrame.configure(yscrollcommand=vsbar.set)

        # Create a horizontal scrollbar linked to the canvas.
        hsbar = tk.Scrollbar(frame2, orient=tk.HORIZONTAL, command=self.canvasFrame.xview)
        hsbar.grid(row=1, column=0, sticky=tk.EW)
        self.canvasFrame.configure(xscrollcommand=hsbar.set)
        # Create a frame on the canvas to contain the buttons.
        self.buttonFrame = tk.Frame(self.canvasFrame, bd=2)
        for posThread in range(numThreads):
            itemView = tk.LabelFrame(self.buttonFrame, bg="#fff", text="Luồng " + str(posThread + 1))
            itemView.grid_columnconfigure(0, weight=1)
            itemView.grid_columnconfigure(1, minsize=120, weight=3)
            itemView.grid(row=0, column=posThread, pady=6, padx=6, sticky=tk.W + tk.N)
            if self.listItem.get(posThread) is None:
                self.listItem[posThread] = {}
            labels = self.listItem[posThread]

            if self.listScript.get(posThread) is None:
                self.listScript[posThread] = {}
            scriptResult = self.listScript[posThread]

            # Init Item View
            row = 0
            self.createLabel(itemView, row, 0, "Trạng thái ", "Verdana 10 bold", "#fff")
            labels["status"] = self.createLabel(itemView, row, 1, "Đang chờ...", "Verdana 10", "#fff")

            row += 1
            self.createLabel(itemView, row, 0, "Thành công ", "Verdana 10 bold", "#fff")
            labels["rate"] = self.createLabel(itemView, row, 1, "1/1", "Verdana 10", "#fff")

            row += 1
            self.createLabel(itemView, row, 0, "IP ", "Verdana 10 bold", "#fff")
            labels["lbIp"] = self.createLabel(itemView, row, 1, "192.168.0..", "Verdana 10", "#fff")

            row += 1
            self.createLabel(itemView, row, 0, "Email ", "Verdana 10 bold", "#fff")
            labels["lbEmail"] = self.createLabel(itemView, row, 1, "___@gmail.com", "Verdana 10", "#fff")

            self.listItem[posThread] = labels

            row += 1
            self.createLabel(itemView, row, 0, "Lệnh đang thực hiện", "Verdana 10 bold", "#fff")
            for i in range(self.TotalLine):
                row += 1
                scriptResult["type" + str(i)] = self.createLabel(itemView, row, 0, "", "Verdana 10", "#fff")
                scriptResult["code" + str(i)] = self.createLabel(itemView, row, 1, "", "Verdana 10", "#fff")
                scriptResult["status" + str(i)] = self.createLabel(itemView, row, 2, "", "Verdana 10", "#fff")
            # End
            self.listScript[posThread] = scriptResult
        # Create canvas window to hold the buttons_frame.
        self.canvasFrame.create_window((0, 0), window=self.buttonFrame, anchor=tk.NW)
        self.refreshLayoutFrame()
