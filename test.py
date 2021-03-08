import json
import os
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

opened_file = json.loads(open(filedialog.askopenfilename(title='Choose file(s)', filetypes=[('JSON Files', '*.json')]), "r").read())

print(opened_file, "\n", opened_file["radiant"])
