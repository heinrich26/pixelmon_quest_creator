import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
from tooltip_class import CreateToolTip
import json
stages = []
final = {}

objective_names = [
	"BLOCKER",
	"DIALOGUE",
	"CAR",
	"BANANA",
	"FISH",
]
objective_data_req = [
	[],
	["entity", "name=%s", "text=%s"],
	[],
	[],
	[]
]
objective_data_opt = [
	[],
	["choice=%s"],
	[],
	[],
	[]
]




def new_stage(stage_id):
	if len(stages) == stage_id:
		if len(stages) != 0:
			stages[-1].nextStage = (stage_id - 1) * 10
		stages.append(Stage(stage_id))
	else:
		stages.insert(stage_id, Stage(stage_id))
	for x in stages:
		x.refresh_id()

class Delete_Tooltip(CreateToolTip):
	def enter(self, event=None):
		self.widget['image'] = delete_hover
		super().enter(self)
		

	def close(self, event=None):
		self.widget['image'] = delete
		if self.tw:
			self.tw.destroy()

class Stage:
	def __init__(self, this_stage):
		self.objectives = []
		self.stage = IntVar()
		self.container = ttk.Frame(stage_frame, borderwidth=2, relief="ridge")
		self.container.grid(row=this_stage, sticky="nesw", column=0, pady=(4,0))
		self.container.columnconfigure((0,1), weight=1)
		self.idbox = ttk.Frame(self.container)
		self.idbox.grid(sticky=W, column=0)
		ttk.Label(self.idbox, text="stage").grid(column=0, sticky=W, padx=(1,0))
		ttk.Label(self.idbox, textvariable=self.stage).grid(row=0, column=1, sticky=W)
		ttk.Label(self.container, text="objectives:").grid(row=1, sticky=W, padx=(1,0))
		self.objectives_box = ttk.Frame(self.container, width=158)
		self.objectives_box.grid(row=2, column=1, sticky=E+W, padx=2)
		self.new_objective_button = ttk.Button(self.container, text='New Objective', command=self.new_objective)
		self.new_objective_button.grid(row=3, column=1, pady=3)
		ttk.Button(self.container, text='New Stage', command=lambda: new_stage(stages.index(self)+1)).grid(row=4, column=0, sticky=W, padx=(1,0))
		self.up_button = ttk.Button(self.container, image=arrow_up, command=self.move_up)
		self.up_button.grid(row=0, column=2, sticky=W+E)
		self.down_button = ttk.Button(self.container, image=arrow_down, command=self.move_down)
		self.down_button.grid(row=4, column=2, sticky=W+E)
		self.delete_button = ttk.Button(self.container, image=delete, command=self.rm)
		self.delete_button.grid(row=1, rowspan=3, column=2, sticky=W+E)
		self.del_tooltip = Delete_Tooltip(self.delete_button, text="Delete this stage")
		
		style = ttk.Style()
		style.configure('Red.TEntry', foreground="orange red")
	
	def chance_validation(self, new_number, widget):
		try:
			float(new_number)
		except:
			return False
		print(widget, self.inserter_chance_entry)
		if new_number == "":
			
		if 0.0 <= float(new_number) <= 1.0:
			print(new_number)
			root.nametowidget(widget)['style'] = 'TEntry'
		else: 
			root.nametowidget(widget)['style'] = 'Red.TEntry'
		return True
	
	def move_up(self):
		index = stages.index(self)
		stages[index-1], stages[index] = stages[index], stages[index-1]
		for stage in stages:
			stage.refresh_id()
		
		
	def move_down(self):
		index = stages.index(self)
		stages[index], stages[index+1] = stages[index+1], stages[index]
		for stage in stages:
			stage.refresh_id()
		
	
	def new_objective(self):
		self.objectives.append(Objective(self, len(self.objectives)))
		
	def refresh_id(self):
		self.stage.set(stages.index(self)*10)
		self.container.grid(row=self.stage.get())
		if stages.index(self) == len(stages):
			self.nextStage = -1
		else:
			self.nextStage = stages.index(self)*10+10
			
		if stages.index(self) == len(stages)-1:
			self.down_button['state'] = 'disabled'
		else:
			self.down_button['state'] = 'normal'	
		if stages.index(self) == 0:
			self.up_button['state'] = 'disabled'
		else:
			self.up_button['state'] = 'normal'
		if len(stages) == 1:
			self.delete_button['state'] = 'disabled'
		else:
			self.delete_button['state'] = 'normal'
		
	def new_objective(self):
		this_w = 500
		this_h = 120
		self.edit_window = Toplevel(self.objectives_box)
		self.edit_window.grab_set()
		self.edit_window.title("Choose Objective Type:")
		self.edit_window.geometry('%dx%d+%d+%d' % (this_w, this_h, int(max(master.winfo_x()+(master.winfo_width()-this_w)/2, 0)), int(max(master.winfo_y()+(master.winfo_height()-this_h)/2, 0))))
		self.edit_window.columnconfigure(0, minsize=120)
		self.edit_window.columnconfigure(1, minsize=150)
		ttk.Label(self.edit_window, text="Objective:").grid(row=0)
		ttk.Label(self.edit_window, text="Required Arguments:").grid(row=0, column=1, sticky=W)
		ttk.Label(self.edit_window, text="Optional Arguments:").grid(row=0, column=2, sticky=W)
		self.var = StringVar(self.edit_window)
		self.var.set(objective_names[0])
		self.obj_type = ttk.OptionMenu(self.edit_window, self.var, objective_names[0], *objective_names)
		self.obj_type.grid(row=1)
		self.options_req = StringVar()
		self.options_opt = StringVar()
		ttk.Label(self.edit_window, textvariable=self.options_req, justify=LEFT, wraplength=146).grid(row=1, column=1, sticky=W)
		ttk.Label(self.edit_window, textvariable=self.options_opt).grid(row=1, column=2)
		self.var.trace("w", self.get_options)
		ttk.Button(self.edit_window, text="Apply", command=self.set_objective_type).grid(row=3, column=2, sticky=E, pady=(20,0))
		ttk.Button(self.edit_window, text="Cancel", command=self.edit_window.destroy).grid(row=3, column=3, sticky=W, pady=(20,0))
		
	def rm(self):
		if len(stages) != 1:
			self.container.destroy()
			stages.remove(self)
			del self
			for x in stages:
				x.refresh_id()

	def get_options(self, *args):
		self.options_req.set(objective_data_req[objective_names.index(self.var.get())])
		self.options_opt.set(objective_data_opt[objective_names.index(self.var.get())])
	
	def set_objective_type(self):
		self.objectives.append(eval(self.var.get())(self))
		self.objectives[-1].identifier = len(self.objectives)-1
		self.edit_window.destroy()
		
		
	def edit_objective(self):
		print(self.__class__.__name__)
		this_w = 500
		this_h = 100
		self.edit_window = Toplevel(self.parent.objectives_box)
		self.edit_window.title("Edit Objective: " + self.__class__.__name__)
		self.edit_window.geometry('%dx%d+%d+%d' % (this_w, this_h, int(max(master.winfo_x()+(master.winfo_width()-this_w)/2, 0)), int(max(master.winfo_y()+(master.winfo_height()-this_h)/2, 0))))
		ttk.Label(self.edit_window, text=self.__class__.__name__).grid(row=0)
		ttk.Label(self.edit_window, text="Required Arguments:").grid(row=0, column=1)
		ttk.Label(self.edit_window, text="Optional Arguments:").grid(row=0, column=2)

class Objective(Stage):
	def __init__(self, parent):
		self.identifier = int()
		self.item = ""
		self.entity = ""
		self.uuid = ""
		self.inserter = ""
		self.class_name = ""
		self.name = ""
		self.text = ""
		self.NPC = ""
		if self.__class__.__name__ == "POKEMON_DEFEAT" or "POKEMON_HAS" or "POKEMON_CAPTURE" or "POKEMON_EVOLVE_POST" or "POKEMON_EVOLVE_PRE" or "POKEMON_HATCH" or "POKEMON_TRADE_GET" or "POKEMON_TRADE_GIVE":
			print("hi there")
		self.entries = []
		self.parent = parent
		self.constructor_box = ttk.Frame(self.parent.objectives_box)
		self.constructor_box.pack(fill=BOTH)
		ttk.Button(self.constructor_box, text=self.__class__.__name__, command=self.edit_objective, width=20).grid(sticky=N+S, pady=1)
		self.delete_button = ttk.Button(self.constructor_box, image=delete, command=self.rm)
		self.delete_button.grid(row=0, column=1, padx=(2,0), pady=1)
		self.delete_tooltip = Delete_Tooltip(self.delete_button, text="Delete this objective")
		self.chance_validation = self.constructor_box.register(self.chance_validation)
		
		
		
	def rm(self):
		self.constructor_box.destroy()
		if len(self.parent.objectives) == 1:
			self.parent.objectives_box.destroy()
			self.parent.objectives_box = ttk.Frame(self.parent.container, width=158)
			self.parent.objectives_box.grid(row=2, column=1, sticky=E+W, padx=2)
		self.parent.objectives.remove(self)
		del self

	def edit_objective(self, optcol="none"):
		this_w = 500
		this_h = 100
		self.edit_window = Toplevel(self.parent.objectives_box)
		self.edit_window.grab_set()
		self.edit_window.title("Edit Objective: " + self.__class__.__name__)
		self.edit_window.geometry('%dx%d+%d+%d' % (this_w, this_h, int(max(master.winfo_x()+(master.winfo_width()-this_w)/2, 0)), int(max(master.winfo_y()+(master.winfo_height()-this_h)/2, 0))))
		ttk.Label(self.edit_window, text="Required Arguments:").grid(row=0, column=0, sticky=W)
		if optcol != "none":
			ttk.Label(self.edit_window, text="Optional Arguments:").grid(row=0, column=optcol, sticky=W)

	def save_callback(self):
		edit_window.destroy()

	def item_entry(self, column, parent="", columns=1):
		if parent == "":
			parent = self.edit_window
		self.item_frame = ttk.Frame(parent)
		self.item_frame.grid(row=1, column=column, columnspan=columns, padx=2)
		if parent == self.edit_window:
			ttk.Label(self.item_frame, text="Item:", ).grid()
		self.item_var = ttk.Entry(self.item_frame)
		self.item_tooltip = CreateToolTip(self.item_frame, text="Enter a <namespace>:item")
		self.item_var.insert(10, self.item)
		self.item_var.grid(row=0,column=1)

	def name_entry(self, column, parent="", columnspan=1):
		if parent == "":
			parent = self.edit_window
		self.name_frame = ttk.Frame(parent)
		self.name_frame.grid(row=1, column=column, columnspan=columns, padx=2)
		if parent == self.edit_window:
			ttk.Label(self.name_frame, text="Name:", ).grid()
		self.name_var = Entry(self.name_frame)
		self.name_tooltip = CreateToolTip(self.name_frame, text="Enter the name that\nshould be displayed")
		self.name_var.insert(10, self.name)
		self.name_var.grid(row=1,column=1)
		
	def uuid_entry(self, column, parent="", columns=1):
		if parent == "":
			parent = self.edit_window
		self.uuid_frame = ttk.Frame(parent)
		self.uuid_frame.grid(row=1, column=column, columnspan=columns, padx=2)
		if parent == self.edit_window:
			ttk.Label(self.uuid_frame, text="UUID:", ).grid()
		self.uuid_var = ttk.Entry(self.uuid_frame)
		self.uuid_tooltip = CreateToolTip(self.uuid_frame, text="Enter a UUID")
		self.uuid_var.insert(10, self.uuid)
		self.uuid_var.grid(row=1,column=1)
		
	def inserter_entry(self, column, parent="", columns=1):
		if parent == "":
			parent = self.edit_window
		self.inserter_frame = ttk.Frame(parent)
		self.inserter_frame.grid(row=1, column=column, columnspan=columns, padx=2)
		if parent == self.edit_window:
			ttk.Label(self.inserter_frame, text="inserter:", ).grid()
		self.inserter_tooltip = CreateToolTip(self.inserter_frame, text="Enter an inserter\nInserters only require to be defined once and can be reused")
		ttk.Label(self.inserter_frame, text="Syntax: !#<type>,<mode>,<chance>,[range],[times...]\n").grid(row=2, column=1)
		ttk.OptionMenu(self.inserter_frame, self.inserter_type, self.inserter_type.get(), *["NPC","Pixelmon"]).grid(row=1, column=0)
		ttk.OptionMenu(self.inserter_frame, self.inserter_mode, self.inserter_mode.get(), *["Time","Spawn"]).grid(row=1, column=1)
		self.inserter_chance_entry = ttk.Entry(self.inserter_frame, textvariable=self.inserter_chance, validate='key', validatecommand=(self.chance_validation, "%P", "%W"))
		self.inserter_chance_entry.grid(row=1, column=2)
		
	def one_out_two_entrys(self, column, entry_one, entry_two):
		self.switch_var_old = "first"
		def one_out_two_swap(*args):
			if switch_var.get() != self.switch_var_old:
				if switch_var.get() == "first":
					getattr(self, entry_two.lower() + "_frame").destroy()
					method1(0, self.one_out_two_entrys_frame, 2)
				else:
					getattr(self, entry_one.lower() + "_frame").destroy()
					method2(0, self.one_out_two_entrys_frame, 2)
				self.switch_var_old = switch_var.get()
		
		self.one_out_two_entrys_frame = ttk.Frame(self.edit_window)
		self.one_out_two_entrys_frame.grid(row=1, column=column)
		self.one_out_two_entrys_frame.columnconfigure((0,1), weight=0, uniform="fred")
		method1 = getattr(self, entry_one.lower()+"_entry")
		method2 = getattr(self, entry_two.lower()+"_entry")
		method1(0, self.one_out_two_entrys_frame, 2)
		switch_var = StringVar(value="first")
		switch_var.trace("w", one_out_two_swap)
		button1 = Radiobutton(self.one_out_two_entrys_frame, variable=switch_var, indicatoron=False, text=entry_one, value="first")
		button1.grid(row=0, column=0,sticky=E+W, padx=(2,0), pady=2)
		button2 = Radiobutton(self.one_out_two_entrys_frame, variable=switch_var, indicatoron=False, text=entry_two, value="second")
		button2.grid(row=0, column=1, sticky=E+W, padx=(0,2), pady=2)
		

		
class BLOCKER(Objective):
	def __init__(self, parent):
		super().__init__(parent)
	
		
class DIALOGUE(Objective):
	def __init__(self, parent):
		super().__init__(parent)
		self.inserter_type = StringVar(value="NPC")
		self.inserter_mode = StringVar(value="Time")
		self.inserter_chance = DoubleVar(value=0.5)
		self.inserter_range = DoubleVar(value=0)
		self.inserter_times = StringVar(value="0")
		
	def edit_objective(self):
		super().edit_objective(optcol=1)
		self.item_entry(1)
		self.one_out_two_entrys(0, "Inserter", "UUID")
		
	
	def save_callback(self):
		self.npc = NPC_var.get()
		self.name = name_var.get()
		self.text = text_var.get()
		super().save_callback(self)
		
		

def create_json():
	print(json.dumps({
		"radiant": radiant.get(),
		"weight": weight.get(),
		"abandonable": abandonable.get(),
		"repeatable": repeatable.get(),
		"activeStage": activeStage.get(),
		"stages": stages
	}))

def only_numbers(char):
	return char.isdigit()


		
root = Tk()
master = ttk.Frame(root)
master.pack(padx=4, pady=4, fill=BOTH)
master.columnconfigure(1,weight=1, minsize=100)

int_validation = master.register(only_numbers)

# image definition

arrow_img = Image.open("src/icons/16/arrow_up.png")
arrow_down = ImageTk.PhotoImage(arrow_img.rotate(180))
arrow_up = ImageTk.PhotoImage(arrow_img)
delete = ImageTk.PhotoImage(Image.open('src/icons/16/delete.png'))
delete_hover = ImageTk.PhotoImage(Image.open('src/icons/16/delete_hover.png'))

radiant = BooleanVar()
ttk.Checkbutton(master, variable=radiant, text="radiant").grid(row=0, sticky=W)
ttk.Label(master, text="weight:").grid(row=1, sticky=W, padx=(20,0))
weight = ttk.Entry(master, validate="key", validatecommand=(int_validation, '%S'))
weight.insert(10,"0")
weight.grid(row=1, column=1, sticky="ew")
abandonable = BooleanVar()
ttk.Checkbutton(master, variable=abandonable, text="abandonable").grid(row=2, sticky=W)
repeatable = BooleanVar()
ttk.Checkbutton(master, variable=repeatable, text="repeatable").grid(row=3, sticky=W)
ttk.Label(master, text="activeStage:").grid(row=4, sticky=W, padx=(20,0))
activeStage = ttk.Entry(master, validate="key", validatecommand=(int_validation, '%S'))
activeStage.grid(row=4, column=1, sticky=E+W)
ttk.Label(master, text="Stages:").grid(row=5, sticky=W, padx=(20,0))
stage_frame = ttk.Frame(master)
stage_frame.grid(row=6, column=0, columnspan=2, sticky="ew", padx=(40,0))
stage_frame.columnconfigure(0,weight=1)
new_stage(0)

ttk.Label(master, text="").grid(row=7)
bottom_frame = ttk.Frame(master)
bottom_frame.grid(row=8, columnspan=2)
ttk.Button(bottom_frame, text='Quit', command=master.quit).grid(column=0)

ttk.Button(bottom_frame, text='Show', command=create_json).grid(row=0,column=1)
def objects():
	for x in stages:
		print(x.objectives)
ttk.Button(bottom_frame, text="Open JSON", command=objects).grid(row=1)

mainloop()
