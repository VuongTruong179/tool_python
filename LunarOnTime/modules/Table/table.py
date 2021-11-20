from tkinter import *
from tkinter import ttk, filedialog

import pandas as pd

# df = pd.read_excel("./CountRef.xlsx", sheet_name="Sheet1")
# ws = df.to_dict('records')
# print(ws)

root = Tk()
root.title("Table Python")
root.geometry("700x500")

my_frame = Frame(root)
my_frame.pack(pady=20)
my_frame.pack(padx=20)

#Create tree view

tree_yscroll = ttk.Scrollbar(my_frame)
tree_yscroll.pack(side='right', fill='y')
my_tree = ttk.Treeview(my_frame, yscrollcommand=tree_yscroll.set, selectmode="none")
tree_yscroll.config(command=my_tree.yview())
#my_tree.pack()

def file_open():
    global df
    filename = filedialog.askopenfilename(
        initialdir='./CountRef.xlsx',
        title= "open a file",
        filetype=(("xlsx files", "*.xlsx"),("All Files", "*.*"))
    )
    if filename:
        try:
            df = pd.read_excel(filename)
        except ValueError:
            my_label.config(text="File couldn't be opened...try again!")
        except FileNotFoundError:
            my_label.config(text="File couldn't be found...try again!")
    #clear old treeView
    clear_tree()
    my_tree["column"] = list(df.columns)
    my_tree["show"] = "headings"

    #set up new tree view
    for column in my_tree["column"]:
        my_tree.heading(column, text=column)

    #Loop thr column list for headers
    df_row = df.to_numpy().tolist()
    for row in df_row:
        my_tree.insert("", "end", values=row)

    my_tree.pack()


def clear_tree():
    my_tree.delete(*my_tree.get_children())

#Add a menu
my_menu = Menu(root)
root.config(menu=my_menu)

#add menu dropdow
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Spreadsheets", menu=file_menu)
file_menu.add_command(label="Open", command=file_open)

my_label = Label(root, text='')
my_label.pack(pady=20)
mainloop()

