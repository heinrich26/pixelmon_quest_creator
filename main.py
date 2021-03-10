#!/usr/bin/env python3
import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from tooltip_class import CreateToolTip
import json
from uuid import UUID
import string
stages = []
final = {}

objective_names = [
	"ABSOLUTE_POSITION",
	"APRICORN_HARVEST",
	"BATTLE_MOVE_TARGET",
	"BATTLE_MOVE_USER",
	"BLOCK_BREAK",
	"BLOCKER",
	"BLOCK_PLACE",
	"BLOCK_USE",
	"DIALOGUE",
	"DIMENSION",
	"ENTITY_INTERACT",
	"ENTITY_VICINITY",
	"FOLLOWTHROUGH",
	"ITEM_CRAFT",
	"ITEM_DROP",
	"ITEM_PICKUP",
	"ITEM_SMELT",
	"ITEM_USE",
	"NPC_RESPOND",
	"POKEMON_CAPTURE",
	"POKEMON_DEFEAT",
	"POKEMON_EVOLVE_POST",
	"POKEMON_EVOLVE_PRE",
	"POKEMON_HAS",
	"POKEMON_HATCH",
	"POKEMON_TRADE_GET",
	"POKEMON_TRADE_GIVE",
	"RANDOM",
	"SERVER_TIME",
	"STRUCTURE",
	"TILEENTITY_VICINITY",
	"WORLD_TIME"
]
objective_data_req = [
	"<x1> <z1> <x2> <z2> <dimension>",
	"item=[mod:]%s count=int",
	"soundbase=true|false; count=int; category=physical|special|status;\ntype=<any of the 17 types>;\nmove=<attack name>,<attack name>,<attack name>,<attack name>; result=<proceed|hit|ignore|killed|succeeded|charging|unable|failed|missed|notarget>;\ndamage[=|</>]int; fulldamage[=|</>]int; accuracy[=|</>]int",
	[],
	[],
	[],
	[],
	[],
	"<entity> name=%s text=%s",
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[]
]

objective_data_req[3]=objective_data_req[2]
objective_data_req[4]=objective_data_req[1]


objective_data_opt = [
	"<y1> at pos2; <y2> at pos5",
	"multiple tag=%s, name=%s &/or damage=int",
	[],
	[],
	[],
	[],
	[],
	[],
	"multiple choice=%s",
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
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
		if new_number == "":
			root.nametowidget(widget).set(0.0)
			return True
		try:
			float(new_number)
		except:
			return False
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
		if stages.index(self) == len(stages)-1:
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
		this_w = 650
		this_h = 200
		self.edit_window = Toplevel(self.objectives_box)
		self.edit_window.grab_set()
		self.edit_window.title("Choose Objective Type:")
		self.edit_window.geometry('%dx%d+%d+%d' % (this_w, this_h, int(max(master.winfo_x()+(master.winfo_width()-this_w)/2, 0)), int(max(master.winfo_y()+(master.winfo_height()-this_h)/2, 0))))
		self.edit_window.columnconfigure(0, minsize=120)
		self.edit_window.columnconfigure((1,2), minsize=150, weight=1)
		self.edit_window.rowconfigure(3, weight=1)
		ttk.Label(self.edit_window, text="Objective:").grid(row=0)
		ttk.Label(self.edit_window, text="Required Arguments:").grid(row=0, column=1, sticky=W)
		ttk.Label(self.edit_window, text="Optional Arguments:").grid(row=0, column=2, sticky=W)
		self.var = StringVar(self.edit_window)
		self.var.set(objective_names[5])
		self.obj_type = ttk.OptionMenu(self.edit_window, self.var, objective_names[5], *objective_names)
		self.obj_type.grid(row=1, sticky=N+E+W, padx=(4,2))
		self.options_req = StringVar()
		self.options_opt = StringVar()
		ttk.Label(self.edit_window, textvariable=self.options_req, justify=LEFT, wraplength=240).grid(row=1, column=1, sticky=W)
		ttk.Label(self.edit_window, textvariable=self.options_opt).grid(row=1, column=2)
		self.var.trace("w", self.get_options)
		ttk.Button(self.edit_window, text="Apply", command=self.set_objective_type).grid(row=3, column=2, sticky=E+S, pady=(0,4))
		ttk.Button(self.edit_window, text="Cancel", command=self.edit_window.destroy).grid(row=3, column=3, sticky=W+S, pady=(0,4), padx=4)

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
		this_w = 500
		this_h = 100
		self.edit_window = Toplevel(self.parent.objectives_box)
		self.edit_window.title("Edit Objective: " + self.__class__.__name__)
		self.edit_window.geometry('%dx%d+%d+%d' % (this_w, this_h, int(max(master.winfo_x()+(master.winfo_width()-this_w)/2, 0)), int(max(master.winfo_y()+(master.winfo_height()-this_h)/2, 0))))
		ttk.Label(self.edit_window, text=self.__class__.__name__).grid(row=0)
		ttk.Label(self.edit_window, text="Required Arguments:").grid(row=0, column=1)
		ttk.Label(self.edit_window, text="Optional Arguments:").grid(row=0, column=2)

	def uuid_input_validator(self, wholeString, widget, newChars, action):
		strippedString = wholeString.replace('-','',4)
		if len(newChars) == 1:
			first_occ = wholeString.find('-',0,min(9, len(wholeString)))
			if first_occ != -1:
				second_occ = wholeString.find('-', first_occ + 1, min(first_occ + 6, len(wholeString)))
				if second_occ != -1:
					third_occ = wholeString.find('-', second_occ + 1, min(second_occ + 6, len(wholeString)))
					if third_occ != -1:
						fourth_occ = wholeString.find('-', third_occ + 1, min(third_occ + 6, len(wholeString)))
						if fourth_occ != -1:
							print("as it should be")
						elif len(wholeString) >= 24:
							 root.nametowidget(widget).insert(23, '-')
					elif len(wholeString) >= 19:
						 root.nametowidget(widget).insert(18, '-')
				elif len(wholeString) >= 14:
					 root.nametowidget(widget).insert(13, '-')
			elif len(wholeString) >= 9:
				root.nametowidget(widget).insert(8, '-')
		elif len(newChars) == 32 and all(c in string.hexdigits for c in newChars) and newChars==wholeString:
			root.nametowidget(widget).delete(0,END)
			root.nametowidget(widget).insert(0, newChars[0:8] + "-" + newChars[8:12] + "-" + newChars[12:16] + "-" + newChars[16:20] + "-" + newChars [16:33])
			return False
		if all(c in string.hexdigits for c in strippedString) and len(strippedString) <= 32:
			return True
		else:
			return False


	def is_valid_uuid(uuid_to_test):
		try:
			int(uuid_to_test.replace("-", "", 4), 16)
		except:
			return False
		first_occ = uuid_to_test.find('-',0,min(9, len(uuid_to_test)))
		if first_occ != -1:
			second_occ = uuid_to_test.find('-', first_occ + 1, min(first_occ + 6, len(uuid_to_test)))
			if second_occ != -1:
				third_occ = uuid_to_test.find('-', second_occ + 1, min(second_occ + 6, len(uuid_to_test)))
				if third_occ != -1:
					fourth_occ = uuid_to_test.find('-', third_occ + 1, min(third_occ + 6, len(uuid_to_test)))
					if fourth_occ != -1:
						return True
		return False


class Objective(Stage):
	def __init__(self, parent):
		self.identifier = int()
		self.item = StringVar()
		self.entity = ""
		self.uuid = StringVar()
		self.inserter = ""
		self.class_name = ""
		self.name = ""
		self.text = ""
		self.NPC = ""
		if self.__class__.__name__ in ("POKEMON_DEFEAT", "POKEMON_HAS", "POKEMON_CAPTURE", "POKEMON_EVOLVE_POST", "POKEMON_EVOLVE_PRE", "POKEMON_HATCH", "POKEMON_TRADE_GET", "POKEMON_TRADE_GIVE"):
			print()
		self.entries = []
		self.parent = parent
		self.constructor_box = ttk.Frame(self.parent.objectives_box)
		self.constructor_box.pack(fill=BOTH)
		ttk.Button(self.constructor_box, text=self.__class__.__name__, command=self.edit_objective, width=20).grid(sticky=N+S, pady=1)
		self.delete_button = ttk.Button(self.constructor_box, image=delete, command=self.rm)
		self.delete_button.grid(row=0, column=1, padx=(2,0), pady=1)
		self.delete_tooltip = Delete_Tooltip(self.delete_button, text="Delete this objective")
		self.chance_validation = self.constructor_box.register(self.chance_validation)
		self.uuid_input_validation = self.constructor_box.register(self.uuid_input_validator)


	def rm(self):
		self.constructor_box.destroy()
		if len(self.parent.objectives) == 1:
			self.parent.objectives_box.destroy()
			self.parent.objectives_box = ttk.Frame(self.parent.container, width=158)
			self.parent.objectives_box.grid(row=2, column=1, sticky=E+W, padx=2)
		self.parent.objectives.remove(self)
		del self

	def edit_objective(self, optcol="none"):
		this_w = 600
		this_h = 148
		self.edit_window = Toplevel(self.parent.objectives_box)
		self.edit_window.grab_set()
		self.edit_window.columnconfigure((0,1,2,3,4,5,6), weight=1)
		self.edit_window.title("Edit Objective: " + self.__class__.__name__)
		self.edit_window.geometry('%dx%d+%d+%d' % (this_w, this_h, int(max(master.winfo_x()+(master.winfo_width()-this_w)/2, 0)), int(max(master.winfo_y()+(master.winfo_height()-this_h)/2, 0))))
		ttk.Label(self.edit_window, text="Required Arguments:").grid(row=0, column=0, sticky=W)
		if optcol != "none":
			ttk.Label(self.edit_window, text="Optional Arguments:").grid(row=0, column=optcol, sticky=W)
		ttk.Button(self.edit_window, command=self.save_objective_changes, text="Save Changes").grid(row=4, column=2, pady=(10,4), padx=4, sticky=E)

	def save_objective_changes(self):
		self.edit_window.destroy()


	def item_entry(self, column, parent="", columns=1):
		if parent == "":
			parent = self.edit_window
		self.item_frame = ttk.Frame(parent)
		self.item_frame.grid(row=1, column=column, columnspan=columns, padx=2)
		if parent == self.edit_window:
			ttk.Label(self.item_frame, text="Item:", ).grid()
		ttk.Entry(self.item_frame, textvariable=self.item).grid(row=0,column=1)
		self.item_tooltip = CreateToolTip(self.item_frame, text="Enter a <namespace>:item")

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
		ttk.Entry(self.uuid_frame, textvariable=self.uuid, validate='key', validatecommand=(self.uuid_input_validation, '%P', '%W', '%S', '%d'), width=40).grid(row=1,column=1)
		self.uuid_tooltip = CreateToolTip(self.uuid_frame, text="Enter a UUID")

	def time_validation(self, newStr):
		if newStr.isnumeric():
			if 0 <= int(newStr) <= 24000:
				return True
			else:
				return False
		else:
			try:
				if newStr.endswith(","):
					newStr = newStr[0:-1]
				time_list = newStr.split(",")
				for x in time_list:
					if not 0 <= int(x) <= 24000:
						return False
				return True
			except:
				return False

	def inserter_entry(self, column, parent="", columns=1):
		if parent == "":
			parent = self.edit_window
		self.inserter_frame = ttk.Frame(parent)
		self.inserter_frame.grid(row=1, column=column, columnspan=columns, padx=2)
		if parent == self.edit_window:
			ttk.Label(self.inserter_frame, text="inserter:", ).grid()
		ttk.Label(self.inserter_frame, text="Syntax: !#<type>,<mode>,<chance>,[range],[times...]\n").grid(row=2, column=0, columnspan=5)
		ttk.OptionMenu(self.inserter_frame, self.inserter_type, self.inserter_type.get(), *["NPC","Pixelmon"]).grid(row=1, column=0)
		ttk.OptionMenu(self.inserter_frame, self.inserter_mode, self.inserter_mode.get(), *["Time","Spawn"]).grid(row=1, column=1)
		self.inserter_mode.trace("w", self.inserter_mode_swap)
		self.inserter_chance_entry = ttk.Entry(self.inserter_frame, textvariable=self.inserter_chance, validate='key', validatecommand=(self.chance_validation, "%P", "%W"), width=10)
		self.inserter_chance_entry.grid(row=1, column=2)
		self.inserter_range_entry = ttk.Entry(self.inserter_frame, textvariable=self.inserter_range, validate="key", validatecommand=(int_validation, "%S"), width=10)
		self.inserter_range_entry.grid(row=1, column=3)
		self.inserter_times_entry = ttk.Entry(self.inserter_frame, textvariable=self.inserter_times, validate="key", validatecommand=(self.time_validation, "%P"), width=10)
		self.inserter_times_entry.grid(row=1, column=4)
		self.inserter_tooltip = CreateToolTip(self.inserter_frame, text="Enter an inserter\nInserters only require to be defined once and can be reused")

	def inserter_mode_swap(self, *args):
		if not self.inserter_mode.get() == self.inserter_mode_old:
			if self.inserter_mode.get() == "Time":
				self.inserter_range_entry.grid(row=1, column=3)
				self.inserter_times_entry.grid(row=1, column=4)
			else:
				self.inserter_range_entry.grid_forget()
				self.inserter_times_entry.grid_forget()
			self.inserter_mode_old = self.inserter_mode.get()

	def one_out_two_entrys(self, column, entry_one, entry_two):
		def one_out_two_swap(*args):
			if self.switch_var.get() != self.switch_var_old:
				if self.switch_var.get() == "first":
					getattr(self, entry_two.lower() + "_frame").destroy()
					method1(0, self.one_out_two_entrys_frame, 2)
				else:
					getattr(self, entry_one.lower() + "_frame").destroy()
					method2(0, self.one_out_two_entrys_frame, 2)
				self.switch_var_old = self.switch_var.get()

		self.one_out_two_entrys_frame = ttk.Frame(self.edit_window)
		self.one_out_two_entrys_frame.grid(row=1, column=column)
		self.one_out_two_entrys_frame.columnconfigure((0,1), weight=0, uniform="fred")
		method1 = getattr(self, entry_one.lower()+"_entry")
		method2 = getattr(self, entry_two.lower()+"_entry")
		method1(0, self.one_out_two_entrys_frame, 2)
		self.switch_var.trace("w", one_out_two_swap)
		button1 = Radiobutton(self.one_out_two_entrys_frame, variable=self.switch_var, indicatoron=False, text=entry_one, value="first")
		button1.grid(row=0, column=0,sticky=E+W, padx=(2,0), pady=2)
		button2 = Radiobutton(self.one_out_two_entrys_frame, variable=self.switch_var, indicatoron=False, text=entry_two, value="second")
		button2.grid(row=0, column=1, sticky=E+W, padx=(0,2), pady=2)

	def makestr(self):
		string = self.__class__.__name__
		return string


class BLOCKER(Objective):
	def __init__(self, parent):
		super().__init__(parent)

class FOLLOWTHROUGH(Objective):
	def __init__(self, parent):
		super().__init__(parent)

class DIALOGUE(Objective):
	def __init__(self, parent):
		super().__init__(parent)
		self.inserter_type = StringVar(value="NPC")
		self.inserter_mode = StringVar(value="Time")
		self.inserter_mode_old = "Time"
		self.inserter_chance = DoubleVar(value=0.5)
		self.inserter_range = IntVar(value=0)
		self.inserter_times = StringVar(value="0")
		self.switch_var = StringVar(value="first")
		self.switch_var_old = "first"
		self.time_validation = self.constructor_box.register(self.time_validation)

	def save_objective_changes(self):
		print("hello there")
		super().save_objective_changes()

	def makestr(self):
		string = self.__class__.__name__ + " "
		if self.switch_var.get() == "first":
			inserter = "!#" + self.inserter_type.get() + "," + self.inserter_mode.get() + "," + str(self.inserter_chance.get())
			if self.inserter_mode.get() == "Time":
				inserter += "," + str(self.inserter_range.get()) + ","
				if self.inserter_times.get().isnumeric():
					inserter += str(self.inserter_times.get())
				else:
					if self.inserter_times.get().endswith(","):
						self.inserter_times.set(self.inserter_times.get()[0:-1])
					inserter += str(self.inserter_times.get().split(",")).replace(" ", "").replace("'", "")
			string += inserter
			print(string)
		else:
			string += self.uuid.get()
		return string

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
		"activeStage": int(activeStage.get()),
		"stages": write_stage_data()
	}))

def only_numbers(char):
	return char.isnumeric()

def write_stage_data():
	stage_list = []
	for stage in stages:
		stage_list.append({
			"stage": stage.stage.get(),
			"nextStage": stage.nextStage,
			"objectives": [],
			"actions": []
		})
		if len(stage.objectives) != 0:
			for objective in stage.objectives:
				stage_list[-1]["objectives"].append(objective.makestr())
	return stage_list

def _bound_to_mousewheel(event):
    fake_canvas.bind_all("<MouseWheel>", _on_mousewheel)

def _unbound_to_mousewheel(event):
    fake_canvas.unbind_all("<MouseWheel>")

def _on_mousewheel(event):
    fake_canvas.yview_scroll(int(-1*(event.delta/120)), "units")



root = Tk()
root.title("AdvancedQuesting - Pixelmon Quest Creator")
root.geometry("340x500")
root.minsize(width=340, height=500)
master = ttk.Frame(root, pad=(4,4))
master.columnconfigure(1,weight=1, minsize=100)
master.rowconfigure(6, weight=1)
master.pack(fill=BOTH, expand=1)
stage_box=ttk.Frame(master)
stage_box.grid(row=6, column=0, columnspan=2, sticky="ewns", padx=(40,0))
stage_box.rowconfigure(0, weight=1)
stage_box.bind('<Enter>', _bound_to_mousewheel)
stage_box.bind('<Leave>', _unbound_to_mousewheel)
fake_canvas = Canvas(stage_box, highlightthickness=0)
fake_canvas.grid(row=0, columnspan=2, sticky=N+S+E+W)
stage_frame = ttk.Frame(fake_canvas)
stage_frame.rowconfigure(0, weight=1)
stage_frame.bind('<Configure>', lambda e: fake_canvas.configure(scrollregion=fake_canvas.bbox('all')))
stage_scrollbar = Scrollbar(stage_box, command=fake_canvas.yview, width=16)
stage_scrollbar.grid(row=0, column=1, sticky=N+S, padx=0)
fake_canvas.configure(yscrollcommand=stage_scrollbar.set)
fake_canvas.bind('<Configure>', lambda e: fake_canvas.configure(scrollregion=fake_canvas.bbox('all')))
fake_canvas.create_window((0,0), window=stage_frame, anchor="nw")

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
weight.insert(10,0)
weight.grid(row=1, column=1, sticky="ew")
abandonable = BooleanVar()
ttk.Checkbutton(master, variable=abandonable, text="abandonable").grid(row=2, sticky=W)
repeatable = BooleanVar()
ttk.Checkbutton(master, variable=repeatable, text="repeatable").grid(row=3, sticky=W)
ttk.Label(master, text="activeStage:").grid(row=4, sticky=W, padx=(20,0))
activeStage = ttk.Entry(master, validate="key", validatecommand=(int_validation, '%S'))
activeStage.insert(10,0)
activeStage.grid(row=4, column=1, sticky=E+W)
ttk.Label(master, text="Stages:").grid(row=5, sticky=W, padx=(20,0))
stage_frame.columnconfigure(0,weight=1)
new_stage(0)

ttk.Label(master, text="").grid(row=7)
bottom_frame = ttk.Frame(master)
bottom_frame.grid(row=8, columnspan=2, sticky=S)
ttk.Button(bottom_frame, text='Quit', command=root.quit).grid(column=0, sticky=S)
ttk.Button(bottom_frame, text='Show', command=create_json).grid(row=0, column=1, sticky=S)

mainloop()
