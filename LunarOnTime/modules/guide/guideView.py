from modules.BaseView import BaseView
import tkinter as tk


class GuideView(BaseView):
    def __init__(self, rootView):
        super().__init__()
        self.rootView = rootView
        self.guideWindow = None
        self.entries = {}
        self.buttons = {}

    def initView(self, initData):
        self.guideWindow = tk.Toplevel(self.rootView)
        self.guideWindow.title("Hướng dẫn")

        self.guideWindow.maxsize(width=600, height=800)
        self.guideWindow.minsize(width=600, height=800)

        self.logView = tk.Frame(self.guideWindow, bg="Light Blue", bd=3, relief=tk.RIDGE)
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

        # Create canvas window to hold the buttons_frame.
        self.canvasFrame.create_window((0, 0), window=self.buttonFrame, anchor=tk.NW)

        row = 0
        self.createLabel(self.buttonFrame, 0, 0, "Danh sách từ khóa", "Verdana 25 bold")
        row += 1
        self.createEntry(self.buttonFrame, row, 0, "scroll", "Verdana 10")
        self.createLabel(self.buttonFrame, row, 1, "Scroll tới vị trí x,y ", "Verdana 10")

        row += 1
        self.createEntry(self.buttonFrame, row, 0, "open_tab", "Verdana 10")
        self.createLabel(self.buttonFrame, row, 1, "Mở 1 Tab trình duyệt", "Verdana 10")

        row += 1
        self.createEntry(self.buttonFrame, row, 0, "switch_tab", "Verdana 10")
        self.createLabel(self.buttonFrame, row, 1, "Chuyển sang vị trí Tab", "Verdana 10")

        row += 1
        self.createEntry(self.buttonFrame, row, 0, "close_tab", "Verdana 10")
        self.createLabel(self.buttonFrame, row, 1, "Đóng Tab trình duyệt", "Verdana 10")

        row += 1
        self.createEntry(self.buttonFrame, row, 0, "click", "Verdana 10")
        self.createLabel(self.buttonFrame, row, 1, "Click vào 1 thành phần trên web", "Verdana 10")

        row += 1
        self.createEntry(self.buttonFrame, row, 0, "type", "Verdana 10")
        self.createLabel(self.buttonFrame, row, 1, "Truyền giá trị vào 1 Input", "Verdana 10")

        row += 1
        self.createEntry(self.buttonFrame, row, 0, "sleep", "Verdana 10")
        self.createLabel(self.buttonFrame, row, 1, "Đợi thời gian theo giây(s)", "Verdana 10")

        row += 1
        self.createLabel(self.buttonFrame, row, 0, "command", "Verdana 10")
        self.createLabel(self.buttonFrame, row, 1, "Mã của lệnh", "Verdana 10")

        row += 1
        self.createLabel(self.buttonFrame, row, 0, "target", "Verdana 10")
        self.createLabel(self.buttonFrame, row, 1, "Thành phần cần lấy ở web: xpath", "Verdana 10")

        row += 1
        self.createLabel(self.buttonFrame, row, 0, "value", "Verdana 10")
        self.createLabel(self.buttonFrame, row, 1, "Giá trị cần điền vào input", "Verdana 10")

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
        w, h = self.guideWindow.winfo_width() - 30, self.guideWindow.winfo_height()
        dw, dh = int((w / COLS) * COLS_DISP), int((h / ROWS) * ROWS_DISP)
        self.canvasFrame.configure(scrollregion=bbox, width=dw, height=dh)

    def close(self):
        self.guideWindow.destroy()
