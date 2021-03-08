import os
from tkinter import *
from tkinter import filedialog
import json
stages = []


def create_json():
	print(json.dumps({
		"radiant": radiant.get(),
		"weight": weight.get(),
		"abandonable": abandonable.get(),
		"repeatable": repeatable.get(),
		"activeStage": activeStage.get()
	}))
	
def new_objective(this_stage, identifier):
	objective = Entry(master)
	r = this_stage + 7 + len(stages[this_stage]["objectives"])
	objective.grid(row=r, column=3)
	stages[this_stage]["objectives"].append("")
	stages[this_stage]["objectives"][-0] = identifier
	


def stage(this_stage):
	stages.append({"stage": this_stage*10})
	Label(master, text="stage: " + str(this_stage*10)).grid(row=0)
	Label(master, text="objectives:").grid(row=0)
	stages[(this_stage)]["objectives"] = []
	n_o_r = this_stage + len(stages[this_stage]["objectives"]) + 7
	Button(master, text='New Objective', command=lambda: new_objective(this_stage, len(stages[this_stage]["objectives"])).grid(row=n_o_r, column=2, sticky=W, pady=4)
	Button(master, text='New Stage', command=lambda: stage(this_stage+1)).grid(row=n_o_r+1, column=2, sticky=W, pady=4)

master = Tk()
Label(master, text="radiant").grid(row=0)
Label(master, text="weight").grid(row=1)
Label(master, text="abandonable").grid(row=2)
Label(master, text="repeatable").grid(row=3)
Label(master, text="activeStage").grid(row=4)
Label(master, text="Stages:").grid(row=6)


radiant = BooleanVar()
Checkbutton(master, variable=radiant).grid(row=0, column=1)
weight = Entry(master)
weight.grid(row=1, column=1)
abandonable = BooleanVar()
Checkbutton(master, variable=abandonable).grid(row=2, column=1)
repeatable = BooleanVar()
Checkbutton(master, variable=repeatable).grid(row=3, column=1)
activeStage = Entry(master)
activeStage.grid(row=4, column=1)

stage(0)



Button(master, text='Quit', command=master.quit).grid(row=6, column=0, sticky=W, pady=4)
Button(master, text='Show', command=create_json).grid(row=6, column=1, sticky=W, pady=4)
Button(master, text="Open JSON")

mainloop()
