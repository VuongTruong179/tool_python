from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import ttk, HORIZONTAL, VERTICAL, BOTH, RIGHT, Y, BOTTOM, LEFT


class BaseView():
    @abstractmethod
    def initView(self, initData):
        raise NotImplementedError

    @abstractmethod
    def destroyView(self):
        raise NotImplementedError

    def removeAllChild(self, viewRoot):
        for child in viewRoot.winfo_children():
            child.destroy()

    def createButton(self, frame, row, column, text, font="Verdana 10 bold"):
        button = tk.Button(frame, text=text, font=font)
        button.grid(row=row, column=column, pady=8, padx=8, columnspan=1)
        return button

    def createLabel(self, frame, row, column, labelText, font, color="#f5f5f5"):
        label = tk.Label(frame, text=labelText, font=font, bg=color)
        label.grid(row=row, column=column, pady=6, padx=6, sticky=tk.N + tk.W)
        return label

    def createEntry(self, frame, row, column, textVar, font="Verdana 10"):
        text = tk.StringVar()
        text.set(textVar)
        entry = tk.Entry(frame, textvariable=text, borderwidth="1", font=font)
        entry.grid(row=row, column=column, pady=8, padx=8, columnspan=1, ipadx=20, ipady=4,
                   sticky=tk.N + tk.S + tk.E + tk.W)
        return entry

    def createEntryInLabel(self, frame, label, row, column, textVar):
        labelFrame = tk.LabelFrame(frame, text=label)
        entry = self.createEntry(labelFrame, row, column, textVar)
        labelFrame.columnconfigure(1, weight=1)
        labelFrame.grid(row=row, column=column, sticky=tk.N + tk.S + tk.E + tk.W, pady=2, padx=5, columnspan=1)
        return entry

    def createScale(self, frame, row, column, label):
        labelFrame = tk.LabelFrame(frame, text=label)
        scale = tk.Scale(labelFrame, from_=1, to=100, orient=HORIZONTAL)
        scale.grid(row=1, column=1)
        labelFrame.grid(row=row, column=column, sticky=tk.N + tk.S + tk.E + tk.W)
        return scale

    def createCombobox(self, frame, row, column, label, values):
        labelFrame = tk.LabelFrame(frame, text=label)
        comboBox = ttk.Combobox(labelFrame, values=values)
        comboBox.grid(row=1, column=1)
        labelFrame.grid(row=row, column=column, sticky=tk.N + tk.S + tk.E + tk.W)
        return comboBox
