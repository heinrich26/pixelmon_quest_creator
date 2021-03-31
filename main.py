#!/usr/bin/env python3
import os
import platform
import json
from uuid import UUID
import string

# import tkinter stuff
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from scrolled_frame import VerticalScrolledFrame
try:
	from PIL import Image, ImageTk
	PIL = True
except:
	PIL = False

# import side-modules
from tooltip_class import CreateToolTip
from json_text_generator import JSON_text_Generator
# from qt_json_text_generator import Qt_JSONTextGenerator

stages = []
strings = []
final = {}
minimized = False

current_os = platform.system()

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
	"item=[mod:]%s count=int()",
	"soundbase=true|false; count=int(); category=physical|special|status;\ntype=<any of the 17 types>;\nmove=<attack name>,<attack name>,<attack name>,<attack name>; result=<proceed|hit|ignore|killed|succeeded|charging|unable|failed|missed|notarget>;\ndamage[=|</>]int(); fulldamage[=|</>]int(); accuracy[=|</>]int()",
	[],
	[],
	[],
	[],
	[],
	"<entity> name=%s text=%s",
	"<dimension_id>",
	"<UUID or class name> <count>",
	"<UUID or class name> <count> <distance>",
	[],
	[],
	[],
	[],
	[],
	[],
	"<UUID> or * for any",
	"<pokémon specs or inserter> <count>",
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	"<Weight>:<ActionA> <Weight>:<ActionB>",
	"<time>",
	"<structure name>",
	[],
	[]
]

objective_data_req[3]=objective_data_req[2]
objective_data_req[4] = objective_data_req[6] = objective_data_req[7] = objective_data_req[13] = objective_data_req[14] = objective_data_req[15] = objective_data_req[16] = objective_data_req[17] = objective_data_req[1]
objective_data_req[20] = objective_data_req[21] = objective_data_req[22] = objective_data_req[23] = objective_data_req[24] = objective_data_req[25] = objective_data_req[26] = objective_data_req[19]
objective_data_req[30] = objective_data_req[11]
objective_data_req[31] = objective_data_req[28]

objective_data_opt = [
	"<y1> at pos2; <y2> at pos5",
	"multiple tag=%s name=%s &/or damage=int()",
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
	"[index]",
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	"[range]",
	[],
	[],
	[]
]

objective_data_opt[4] = objective_data_opt[6] = objective_data_opt[7] = objective_data_opt[13] = objective_data_opt[14] = objective_data_opt[15] = objective_data_opt[16] = objective_data_opt[17] = objective_data_opt[1]
objective_data_opt[31] = objective_data_opt[28]

#pokemon natures & growths
natures = ["Hardy","Lonely","Adamant","Naughty","Brave","Bold","Docile","Impish","Lax","Relaxed","Modest","Mild","Bashful","Rash","Quiet","Calm","Gentle","Careful","Quirky","Sassy","Timid","Hasty","Jolly","Naive","Serious"]
growths = ["Microscopic","Pygmy","Runt","Small","Ordinary","Huge","Giant","Enormous","Ginormous"]
types = ["Normal","Fire","Fighting","Water","Flying","Grass","Poison","Electric","Ground","Psychic","Rock","Ice","Bug","Dragon","Ghost","Dark","Steel","Fairy"]





def new_stage(stage_id):
	if len(stages) == stage_id:
		if len(stages) != 0:
			stages[-1].nextStage = (stage_id - 1) * 10
		stages.append(Stage(stage_id))
	else:
		stages.insert(stage_id, Stage(stage_id))
	for x in stages:
		x.refresh_id()

def new_string_name():
	string_name_selector_window = Toplevel(root)
	string_name_selector_window.attributes("-topmost", True)
	string_name_selector_window.title("Create new String")
	string_name_selector_window.grab_set()
	string_name_selector_window.focus_set()
	new_string_name = StringVar(string_name_selector_window,value="")
	ttk.Label(string_name_selector_window, text="Enter unique Identifier for new String:").grid(row=0, column=0, sticky=N+W, padx=4, pady=4)
	ttk.Entry(string_name_selector_window, textvariable=new_string_name).grid(row=1, column=0, sticky=W+E, padx=10)
	ttk.Button(string_name_selector_window, command=lambda: new_string(new_string_name.get(), string_name_selector_window, custom=True), text="Save").grid(row=2,column=1, padx=4, pady=4)

def new_string(name, *args, custom=False):
	if len(name) == 0 or not [True for char in name if char == "-" or char.isalnum()]:
		# falschen Text entfernen
		messagebox.showerror(message="A String Name cannot contain whitespaces or special characters, only 1-9, Letters and \'-\'s!\nTry again!")
	elif not name in [string.name for string in strings]:
		try:
			args[0].destroy()
		except:
			pass
		strings.append(StringObj(name, custom=custom))
	else:
		messagebox.showwarning(message="Name is already in use!\nTry again!")

class StringObj(object):
	def __init__(self, name, custom=False):
		self.name = name
		self.custom = custom
		self.string_frame = ttk.Frame(string_frame.interior)
		self.string_frame.pack(side=TOP, expand=1, fill=X)
		self.string_frame.columnconfigure(0, weight=1)
		slave_win = Toplevel(root)
		slave_win.wm_overrideredirect(True)
		slave_win.grab_set()
		slave_win.geometry("0x0")
		# self.string_editor = Qt_JSONTextGenerator(self.name)
		# self.string_text = self.string_editor.string
		slave_win.destroy()
		self.labeled_button = ttk.Button(self.string_frame, text=self.name, command=self.edit_string)
		self.labeled_button.grid(row=0, column=0, sticky=EW+S+N)
		self.delete_button = ttk.Button(self.string_frame, image=delete, command=self.rm)
		self.delete_button.grid(row=0, column=1, sticky=E)
		self.del_tooltip = Delete_Tooltip(self.delete_button, text="Delete this String")

	def rm(self):
		if self.custom:
			self.string_frame.destroy()
			strings.remove(self)
			del self

	def edit_string(self):
		slave_win = Toplevel(root)
		slave_win.wm_overrideredirect(True)
		slave_win.grab_set()
		slave_win.geometry("0x0")
		self.string_editor.edit_string()
		self.string_text = self.string_editor.string
		slave_win.destroy()


class Arrowed_Tooltip(object):
	def __init__(self, widget, text='widget info', bg_color="orange red"):
		self.minimized = False
		self.widget = root.nametowidget(widget)
		self.widget.update()
		self.parent = self.widget.winfo_toplevel()
		self.text = text
		self.bg_color = bg_color
		x = self.widget.winfo_rootx() + int(round(0.5 * self.widget.winfo_width(),0))
		y = self.widget.winfo_rooty()
		# creates a toplevel window
		self.tw = Toplevel(self.widget)
		self.tw.attributes("-alpha", 0.7)
		if current_os == "Windows":
			self.tw.wm_attributes("-transparentcolor", self.tw["bg"])
		if current_os == "Darwin":
			self.tw.config(bg="systemTransparent")
		# Leaves only the label and removes the app window
		self.tw.wm_overrideredirect(True)
		self.tw.transient()
		self.label = Label(self.tw, text=self.text, justify='center', borderwidth=0, bg=self.bg_color, font=("TkTextFont", "8", "normal"))
		self.label.pack(ipadx=1, side=TOP)
		self.arrow_canv = Canvas(self.tw, width=12, height=6, highlightthickness=0)
		self.arrow_canv.create_polygon([0,0,6,6,12,0], fill=self.bg_color)
		self.arrow_canv.pack(side=BOTTOM)
		self.tw.update()
		self.tw.wm_geometry("+%d+%d" % (x-int(round(0.5*self.tw.winfo_width())), y-self.tw.winfo_height()-2))
		self.parent.bind("<<Minimize_Configure>>", self.repos)
		self.parentx, self.parenty, self.parentwidth, self.parentheight = self.parent.winfo_rootx(), self.parent.winfo_rooty(), self.parent.winfo_width(), self.parent.winfo_height()
		self.expect_event = False

	def repos(self, event):
		if not self.expect_event:
			self.tw.update()
			self.tw.wm_geometry("+%d+%d" % (self.widget.winfo_rootx() + int(round(0.5 * self.widget.winfo_width(),0))-int(round(0.5*self.tw.winfo_width())), self.widget.winfo_rooty()-self.tw.winfo_height()-2))
			self.tw.lift(aboveThis=self.parent)
			self.expect_event = True
		else:
			self.expect_event = False
			self.tw.update()
			self.tw.wm_geometry("+%d+%d" % (self.widget.winfo_rootx() + int(round(0.5 * self.widget.winfo_width(),0))-int(round(0.5*self.tw.winfo_width())), self.widget.winfo_rooty()-self.tw.winfo_height()-2))

	def hide(self):
		self.tw.withdraw()

	def show(self, text="hi"):
		self.tw.deiconify()

	def __del__(self):
		self.tw.destroy()

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
		self.container = ttk.Frame(stage_frame.interior, borderwidth=2, relief="ridge")
		self.container.grid(row=this_stage, sticky="nwse", column=0, pady=(4,0), padx=4)
		self.container.columnconfigure(1, weight=1)
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
		self.edit_window.columnconfigure(0, minsize=178)
		self.edit_window.columnconfigure((1,2), minsize=150, weight=1)
		self.edit_window.rowconfigure(2, weight=1)
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
		ttk.Label(self.edit_window, textvariable=self.options_opt, justify=LEFT, wraplength=240).grid(row=1, column=2, sticky=W)
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
		self.count = StringVar(value=1)
		if self.__class__.__name__ in ("POKEMON_DEFEAT", "POKEMON_HAS", "POKEMON_CAPTURE", "POKEMON_EVOLVE_POST", "POKEMON_EVOLVE_PRE", "POKEMON_HATCH", "POKEMON_TRADE_GET", "POKEMON_TRADE_GIVE"):
			print()
		self.entries = []
		self.parent = parent

		# var assignment
		global types
		global growths
		global natures
		selectable_types = types.copy()
		selectable_types.insert(0, "any")
		selectable_growths = growths.copy()
		selectable_growths.insert(0, "any")
		selectable_natures = natures.copy()
		selectable_natures.insert(0, "any")
		self.selectable_types = StringVar(value=selectable_types)
		self.selectable_growths = StringVar(value=selectable_growths)
		self.selectable_natures = StringVar(value=selectable_natures)

		# building the edit button
		self.constructor_box = ttk.Frame(self.parent.objectives_box)
		self.constructor_box.pack(fill=BOTH)
		ttk.Button(self.constructor_box, text=self.__class__.__name__, command=self.edit_objective, width=20).grid(sticky=N+S, pady=1)
		self.delete_button = ttk.Button(self.constructor_box, image=delete, command=self.rm)
		self.delete_button.grid(row=0, column=1, padx=(2,0), pady=1)
		self.delete_tooltip = Delete_Tooltip(self.delete_button, text="Delete this objective")
		self.chance_validation = self.constructor_box.register(self.chance_validation)
		self.uuid_input_validation = self.constructor_box.register(self.uuid_input_validator)
		self.dex_range_validation = self.constructor_box.register(self.dex_range_validator)
		self.dex_number_validation = self.constructor_box.register(self.dex_number_validator)


	def rm(self):
		self.constructor_box.destroy()
		if len(self.parent.objectives) == 1:
			self.parent.objectives_box.destroy()
			self.parent.objectives_box = ttk.Frame(self.parent.container, width=158)
			self.parent.objectives_box.grid(row=2, column=1, sticky=E+W, padx=2)
		self.parent.objectives.remove(self)
		del self

	def edit_objective(self, optcol="none", requirements=True):
		this_w = 600
		this_h = 160
		self.edit_window = Toplevel(self.parent.objectives_box)
		self.edit_window.grab_set()
		self.edit_window.rowconfigure(1, weight=1)
		self.edit_window.title("Edit Objective: " + self.__class__.__name__)
		self.edit_window.geometry("+%d+%d" % (int(max(root.winfo_x()+(root.winfo_width()-this_w)/2, 0)), int(max(root.winfo_y()+(root.winfo_height()-this_h)/2, 0))))
		self.edit_window.minsize(this_w, this_h)
		if requirements:
			ttk.Label(self.edit_window, text="Required Arguments:").grid(row=0, column=0, sticky=W)
		if optcol != "none":
			ttk.Label(self.edit_window, text="Optional Arguments:").grid(row=0, column=optcol, sticky=W)
		ttk.Button(self.edit_window, command=self.save_objective_changes, text="Save Changes").grid(row=4, column=3, pady=(10,4), padx=4, sticky=E+S)
		self.edit_window.focus_set()
		self.edit_window.resizable(False, False)

	def save_objective_changes(self):
		self.edit_window.destroy()
		try:
			root.deiconify()
		except:
			pass

	def item_entry(self, column, parent="", columns=1):
		if parent == "":
			parent = self.edit_window
		self.item_frame = ttk.Frame(parent)
		self.item_frame.grid(row=1, column=column, columnspan=columns, padx=2)
		if parent == self.edit_window:
			ttk.Label(self.item_frame, text="Item:", ).grid()
		ttk.Entry(self.item_frame, textvariable=self.item).grid(row=0,column=1)
		self.item_tooltip = CreateToolTip(self.item_frame, text="Enter a <namespace>:item")

	def name_entry(self, column, parent="", columns=1):
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

	def dex_range_validator(self, newStr, widget):
		if len(newStr) >= 8:
			return False
		if newStr == "any":
			try:
				self.dex_range_error.hide()
			except:
				pass
			root.nametowidget(widget)['style'] = 'TEntry'
			return True
		if newStr == "" or newStr in ("an", "y", "n", "a", "ny", "ay"):
			root.nametowidget(widget)['style'] = 'Red.TEntry'
			try:
				self.dex_range_error.hide()
			except:
				pass
			return True
		dex_range = newStr.split("-")
		if newStr.replace("-", "",1).isnumeric():
			if len(newStr) >= 4 and newStr.count("-") != 1:
				return False
			if len(dex_range[0]) >= 4 :
				return False
			if len(dex_range) == 2 and dex_range[1] != "" and dex_range[0] != "":
				if len(dex_range[1]) >= 4:
					return False
				if 0 <= int(dex_range[0]) < int(dex_range[1]) <= 898:
					root.nametowidget(widget)['style'] = 'TEntry'
					try:
						self.dex_range_error.hide()
					except:
						pass
					return True
				else:
					root.nametowidget(widget)['style'] = 'Red.TEntry'
					try:
						self.dex_range_error
					except:
						self.dex_range_error=Arrowed_Tooltip(widget, text="Dex entries out of range!")
					self.dex_range_error.show(text="Dex entries out of range!")
					return True
			else:
				root.nametowidget(widget)['style'] = 'TEntry'
				try:
					self.dex_range_error.hide()
				except:
					pass
				return True
		return False

	def dex_number_validator(self, newStr, widget):
		if newStr == "" or newStr in ("an", "y", "n", "a", "ny", "ay"):
			root.nametowidget(widget)['style'] = 'Red.TEntry'
			try:
				self.dex_range_error.hide()
			except:
				pass
			return True
		if newStr == "any":
			root.nametowidget(widget)['style'] = 'TEntry'
			try:
				self.dex_range_error.hide()
			except:
				pass
			return True
		if newStr.isnumeric():
			if 0 <= int(newStr) <= 898:
				root.nametowidget(widget)['style'] = 'TEntry'
				try:
					self.dex_range_error.hide()
				except:
					pass
				return True
			else:
				return False
		else:
			try:
				if newStr.endswith(";"):
					newStr = newStr[0:-1]
				dex_number_list = newStr.split(";")
				for x in dex_number_list:
					if not 0 <= int(x) <= 898:
						root.nametowidget(widget)['style'] = 'Red.TEntry'
						try:
							self.dex_range_error
						except:
							self.dex_range_error=Arrowed_Tooltip(widget, text="Dex entries out of range!")
						self.dex_range_error.show(text="Dex entries out of range!")
						return True
					if dex_number_list.count(x) != 1:
						root.nametowidget(widget)['style'] = 'Red.TEntry'
						try:
							self.dex_range_error
						except:
							self.dex_range_error=Arrowed_Tooltip(widget, text="Dex entries should not repeat!")
						self.dex_range_error.show(text="Dex entries should not repeat!")
						return True

				root.nametowidget(widget)['style'] = 'TEntry'
				try:
					self.dex_range_error.hide()
				except:
					pass
				return True
			except:
				return False

	def inserter_entry(self, column, parent="", columns=1):
		if parent == "":
			parent = self.edit_window
		self.inserter_frame = ttk.Frame(parent)
		self.inserter_frame.grid(row=1, column=column, columnspan=columns, padx=2, sticky=N+W)
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

	def pokemon_inserter_entry(self, column, parent="", columns=1):
		global growths
		global natures
		if parent == "":
			parent = self.edit_window
		self.pokemon_inserter_frame = ttk.Frame(parent)
		self.pokemon_inserter_frame.grid(row=1, column=column, columnspan=columns, pady=4, padx=(4,0), sticky=N+W)
		self.pokemon_inserter_frame.columnconfigure(1, minsize=141)
		self.pokemon_inserter_frame.columnconfigure(0, minsize=88)
		if parent == self.edit_window:
			ttk.Label(self.pokemon_inserter_frame, text="Inserter:", justify=LEFT).grid(row=0, column=0, sticky=W)
			self.pokemon_inserter_mode_desc = StringVar(value="Dex IDs split by \';\'")
			ttk.Label(self.pokemon_inserter_frame, textvariable=self.pokemon_inserter_mode_desc, justify=LEFT).grid(row=0, column=1, sticky=W)
			ttk.Label(self.pokemon_inserter_frame, text="Select Nature(s):").grid(row=0, column=2, sticky=W)
			ttk.Label(self.pokemon_inserter_frame, text="Select Growth(s):").grid(row=0, column=3, sticky=W)
		ttk.OptionMenu(self.pokemon_inserter_frame, self.pokemon_inserter_mode, self.pokemon_inserter_mode.get(), *["Dex","DexRange","Types"]).grid(row=1, column=0, sticky=N+W+E, padx=(0,2))

		# natures selection
		self.pokemon_inserter_natures_frame = ttk.Frame(self.pokemon_inserter_frame)
		self.pokemon_inserter_natures_frame.grid(row=1, column=2)
		self.pokemon_inserter_natures_scrollbar = ttk.Scrollbar(self.pokemon_inserter_natures_frame, orient=VERTICAL)
		self.pokemon_inserter_natures_selector = Listbox(self.pokemon_inserter_natures_frame, yscrollcommand=self.pokemon_inserter_natures_scrollbar.set, listvariable=self.selectable_natures, height=5, selectmode=MULTIPLE, exportselection=0)
		self.pokemon_inserter_natures_selector.grid(row=0, column=0, sticky=N+E+S+W)
		self.pokemon_inserter_natures_scrollbar.config(command=self.pokemon_inserter_natures_selector.yview)
		self.pokemon_inserter_natures_scrollbar.grid(row=0, column=1, sticky=N+S)
		self.pokemon_inserter_natures_old = list(self.pokemon_inserter_natures)
		for item in self.pokemon_inserter_natures:
			self.pokemon_inserter_natures_selector.selection_set(item)

		# growths selection
		self.pokemon_inserter_growths_frame = ttk.Frame(self.pokemon_inserter_frame)
		self.pokemon_inserter_growths_frame.grid(row=1, column=3)
		self.pokemon_inserter_growths_scrollbar = ttk.Scrollbar(self.pokemon_inserter_growths_frame, orient=VERTICAL)
		self.pokemon_inserter_growths_selector = Listbox(self.pokemon_inserter_growths_frame, yscrollcommand=self.pokemon_inserter_growths_scrollbar.set, listvariable=self.selectable_growths, height=5, selectmode=MULTIPLE, exportselection=0)
		self.pokemon_inserter_growths_selector.grid(row=0, column=0, sticky=N+E+S+W)
		self.pokemon_inserter_growths_scrollbar.config(command=self.pokemon_inserter_growths_selector.yview)
		self.pokemon_inserter_growths_scrollbar.grid(row=0, column=1, sticky=N+S)
		self.pokemon_inserter_growths_old = list(self.pokemon_inserter_growths)
		for item in self.pokemon_inserter_growths:
			self.pokemon_inserter_growths_selector.selection_set(item)

		self.pokemon_inserter_dex_numbers_entry = ttk.Entry(self.pokemon_inserter_frame, textvariable=self.pokemon_inserter_dex_numbers, validate="key", validatecommand=(self.dex_number_validation, "%P", "%W"))
		self.pokemon_inserter_dex_range_entry = ttk.Entry(self.pokemon_inserter_frame, textvariable=self.pokemon_inserter_dex_range, validate="key", validatecommand=(self.dex_range_validation, "%P", "%W"))

		# type selection
		self.pokemon_inserter_type_frame = ttk.Frame(self.pokemon_inserter_frame)
		self.pokemon_inserter_type_scrollbar = ttk.Scrollbar(self.pokemon_inserter_type_frame, orient=VERTICAL)
		self.pokemon_inserter_type_selector = Listbox(self.pokemon_inserter_type_frame, yscrollcommand=self.pokemon_inserter_type_scrollbar.set, listvariable=self.selectable_types, height=5, selectmode=MULTIPLE, exportselection=0)
		self.pokemon_inserter_type_selector.grid(row=0, column=0, sticky=N+E+S+W)
		self.pokemon_inserter_type_scrollbar.config(command=self.pokemon_inserter_type_selector.yview)
		self.pokemon_inserter_type_scrollbar.grid(row=0, column=1, sticky=N+S)
		self.pokemon_inserter_type_old = list(self.pokemon_inserter_type)
		for item in self.pokemon_inserter_type:
			self.pokemon_inserter_type_selector.selection_set(item)

		# constructing the mode part
		if self.pokemon_inserter_mode.get() == "Dex":
			self.pokemon_inserter_dex_numbers_entry.grid(row=1, column=1, sticky=W+E+N)
			self.pokemon_inserter_mode_desc.set("Dex IDs split by \';\'")
		elif self.pokemon_inserter_mode.get() == "DexRange":
			self.pokemon_inserter_dex_range_entry.grid(row=1, column=1, sticky=W+E+N)
			self.pokemon_inserter_mode_desc.set("A Range of Dex IDs (a-b):")
		else:
			self.pokemon_inserter_type_frame.grid(row=1, column=1)
			self.pokemon_inserter_mode_desc.set("Select Type(s):")
		self.pokemon_inserter_mode.trace("w", self.pokemon_inserter_mode_swap)
		self.pokemon_inserter_type_selector.bind("<<ListboxSelect>>", self.set_type_selection)
		self.pokemon_inserter_growths_selector.bind("<<ListboxSelect>>", self.set_growths_selection)
		self.pokemon_inserter_natures_selector.bind("<<ListboxSelect>>", self.set_natures_selection)

	def count_entry(self, column, parent="", columns=1):
		if parent == "":
			parent = self.edit_window
		self.count_frame = ttk.Frame(parent)
		self.count_frame.grid(row=1, column=column, columnspan=columns, pady=4, padx=(4,0), sticky=N+W)
		self.count_frame.columnconfigure(0, minsize=50)
		if parent == self.edit_window:
			ttk.Label(self.count_frame, text="Amount:", justify=LEFT).grid(row=0, column=0, sticky=W)
		ttk.Entry(self.count_frame, textvariable=self.count, width=4, validate="key", validatecommand=(natural_num_validation, "%P", "%W"), justify=RIGHT).grid(row=1, column=0, sticky=E+W)

	def inserter_mode_swap(self, *args):
		if not self.inserter_mode.get() == self.inserter_mode_old:
			if self.inserter_mode.get() == "Time":
				self.inserter_range_entry.grid(row=1, column=3)
				self.inserter_times_entry.grid(row=1, column=4)
			else:
				self.inserter_range_entry.grid_forget()
				self.inserter_times_entry.grid_forget()
			self.inserter_mode_old = self.inserter_mode.get()

	def pokemon_inserter_mode_swap(self, *args):
		if not self.pokemon_inserter_mode.get() == self.pokemon_inserter_mode_old:
			if self.pokemon_inserter_mode.get() == "DexRange":
				self.pokemon_inserter_dex_range_entry.grid(row=1, column=1, sticky=W+E+N)
				self.pokemon_inserter_type_frame.grid_forget()
				self.pokemon_inserter_dex_numbers_entry.grid_forget()
				self.pokemon_inserter_mode_desc.set("A Range of Dex IDs (a-b):")
				try:
					self.dex_range_error.hide()
				except:
					pass
			elif self.pokemon_inserter_mode.get() == "Dex":
				self.pokemon_inserter_dex_numbers_entry.grid(row=1, column=1, sticky=W+E+N)
				self.pokemon_inserter_type_frame.grid_forget()
				self.pokemon_inserter_dex_range_entry.grid_forget()
				self.pokemon_inserter_mode_desc.set("Dex IDs split by \';\'")
				try:
					self.dex_range_error.hide()
				except:
					pass
			else:
				self.pokemon_inserter_type_frame.grid(row=1, column=1)
				self.pokemon_inserter_dex_numbers_entry.grid_forget()
				self.pokemon_inserter_dex_range_entry.grid_forget()
				self.pokemon_inserter_mode_desc.set("Select Type(s):")
				try:
					self.dex_range_error.hide()
				except:
					pass
			self.pokemon_inserter_mode_old = self.pokemon_inserter_mode.get()

	def set_type_selection(self, event):
		selection = self.pokemon_inserter_type_selector.curselection()
		if len(selection) >= 2 and 0 in selection:
			if 0 not in self.pokemon_inserter_type_old:
				self.pokemon_inserter_type_selector.selection_clear(1, END)
				self.pokemon_inserter_type_old = [0]
				self.pokemon_inserter_type_selector.selection_set(0)
			else:
				self.pokemon_inserter_type_selector.selection_clear(0,0)
				self.pokemon_inserter_type_old = selection[1:]
		else:
			self.pokemon_inserter_type_old = selection

	def set_growths_selection(self, event):
		selection = self.pokemon_inserter_growths_selector.curselection()
		if len(selection) >= 2 and 0 in selection:
			if 0 not in self.pokemon_inserter_growths_old:
				self.pokemon_inserter_growths_selector.selection_clear(1, END)
				self.pokemon_inserter_growths_old = [0]
				self.pokemon_inserter_growths_selector.selection_set(0)
			else:
				self.pokemon_inserter_growths_selector.selection_clear(0,0)
				self.pokemon_inserter_growths_old = selection[1:]
		else:
			self.pokemon_inserter_growths_old = selection

	def set_natures_selection(self, event):
		selection = self.pokemon_inserter_natures_selector.curselection()
		if len(selection) >= 2 and 0 in selection:
			if 0 not in self.pokemon_inserter_natures_old:
				self.pokemon_inserter_natures_selector.selection_clear(1, END)
				self.pokemon_inserter_natures_old = [0]
				self.pokemon_inserter_natures_selector.selection_set(0)
			else:
				self.pokemon_inserter_natures_selector.selection_clear(0,0)
				self.pokemon_inserter_natures_old = selection[1:]
		else:
			self.pokemon_inserter_natures_old = selection


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

	def edit_objective(self):
		super().edit_objective(requirements=False)
		ttk.Label(self.edit_window, text="There's nothing to edit here!").grid(row=1, column=0)

class FOLLOWTHROUGH(Objective):
	def __init__(self, parent):
		super().__init__(parent)

	def edit_objective(self):
		super().edit_objective(requirements=False)
		ttk.Label(self.edit_window, text="There's nothing to edit here!").grid(row=1, column=0)

class DIALOGUE(Objective):
	def __init__(self, parent):
		super().__init__(parent)
		self.choices = StringVar()
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
		if len(self.choices) != 0:
			print("hithererere")
		return string

	def edit_objective(self):
		super().edit_objective(optcol=1)
		self.item_entry(1)
		self.one_out_two_entrys(0, "Inserter", "UUID")

class POKEMON_CAPTURE(Objective):
	def __init__(self, parent):
		self.pokemon_inserter_mode = StringVar(value="Dex")
		self.pokemon_inserter_mode_old = "Dex"
		self.pokemon_inserter_dex_numbers = StringVar(value="any")
		self.pokemon_inserter_dex_range = StringVar(value="any")
		self.pokemon_inserter_type = [0]
		self.pokemon_inserter_natures = [0]
		self.pokemon_inserter_growths = [0]
		super().__init__(parent)

	def edit_objective(self):
		super().edit_objective()
		self.pokemon_inserter_entry(0)
		self.count_entry(1)
		self.edit_window.resizable(False, False)

	def makestr(self):
		global types
		global natures
		global growths
		string = self.__class__.__name__ + " "
		inserter = "!#" + self.pokemon_inserter_mode.get() + ","
		if self.pokemon_inserter_mode.get() == "Dex":
			inserter += str(self.pokemon_inserter_dex_numbers.get()) + ","
		elif self.pokemon_inserter_mode.get() == "DexRange":
			inserter += str(self.pokemon_inserter_dex_range.get()) + ","
		elif 0 in self.pokemon_inserter_type:
			inserter += "any,"
		else:
			inserter += ";".join([types[element-1] for element in self.pokemon_inserter_type]) + ","
		if 0 in self.pokemon_inserter_natures:
			inserter += "any,"
		else:
			inserter += ";".join([natures[element-1] for element in self.pokemon_inserter_natures]) + ","
		if 0 in self.pokemon_inserter_growths:
			inserter += "any"
		else:
			inserter += ";".join([growths[element-1] for element in self.pokemon_inserter_growths])
		string += inserter + " " + self.count.get()
		print(string)
		return string

	def save_objective_changes(self):
		if self.pokemon_inserter_mode.get() == "Types":
			print(self.pokemon_inserter_type_frame.bbox(), self.pokemon_inserter_type_frame.winfo_width())
			self.pokemon_inserter_type = self.pokemon_inserter_type_selector.curselection()
		self.pokemon_inserter_growths = self.pokemon_inserter_growths_selector.curselection()
		self.pokemon_inserter_natures = self.pokemon_inserter_natures_selector.curselection()
		super().save_objective_changes()

class POKEMON_HAS(POKEMON_CAPTURE):
	pass

class POKEMON_HATCH(POKEMON_CAPTURE):
	pass

class POKEMON_DEFEAT(POKEMON_CAPTURE):
	pass

class POKEMON_TRADE_GET(POKEMON_CAPTURE):
	pass

class POKEMON_TRADE_GIVE(POKEMON_CAPTURE):
	pass

class POKEMON_EVOLVE_PRE(POKEMON_CAPTURE):
	pass

class POKEMON_EVOLVE_POST(POKEMON_CAPTURE):
	pass

def create_json():
	print(json.dumps({
		"radiant": radiant.get(),
		"weight": weight.get(),
		"abandonable": abandonable.get(),
		"repeatable": repeatable.get(),
		"activeStage": int(activeStage.get()),
		"stages": write_stage_data()
	}))

def only_numbers(newStr, widget):
	if newStr.isnumeric() or newStr == "":
		if newStr == "":
			root.nametowidget(widget)['style'] = 'Red.TEntry'
		else:
			root.nametowidget(widget)['style'] = 'TEntry'
		return True
	else:
		return False

def only_natural_numbers(newStr, widget):
	if newStr == "":
		root.nametowidget(widget)['style'] = 'Red.TEntry'
		return True
	elif newStr.isnumeric() and int(newStr) >=1:
		root.nametowidget(widget)['style'] = 'TEntry'
		return True
	else:
		return False

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


root = Tk()
root.event_add("<<Minimize_Configure>>", "<Configure>")
root.title("AdvancedQuesting - Pixelmon Quest Creator")
# root.geometry("354x500")
root.minsize(width=354, height=700)

# image definition
if PIL:
	arrow_img = Image.open("src/icons/16/arrow_up.png")
	arrow_down = ImageTk.PhotoImage(arrow_img.rotate(180))
	arrow_up = ImageTk.PhotoImage(arrow_img)
else:
	arrow_up = PhotoImage(file="src/icons/16/arrow_up.png")
	arrow_down = PhotoImage(file="src/icons/16/arrow_down.png")
	arrow_left = PhotoImage(file="src/icons/16/arrow_left.png")
	arrow_right = PhotoImage(file="src/icons/16/arrow_right.png")

delete = PhotoImage(file='src/icons/16/delete.png')
delete_hover = PhotoImage(file='src/icons/16/delete_hover.png')

# styles

style = ttk.Style()
style.configure('Scroller.Vertical.TScrollbar', width=16)

style.element_create("plain.field", "from", "clam")
style.layout("Red.TEntry",
				[('Entry.plain.field', {'children': [(
					'Entry.background', {'children': [(
						'Entry.padding', {'children': [(
							'Entry.textarea', {'sticky': 'nswe'})],
						'sticky': 'nswe'})], 'sticky': 'nswe'})],
					'border':'2', 'sticky': 'nswe'})])
style.configure("Red.TEntry",
	background="",
	foreground="white",
	fieldbackground="orange red")

master = ttk.Frame(root, pad=(4,4))
master.columnconfigure(1,weight=1, minsize=100)
master.columnconfigure(0,weight=0, minsize=40)
master.rowconfigure(6, weight=3)
master.pack(fill=BOTH, expand=1)

int_validation = root.register(only_numbers)
natural_num_validation = root.register(only_natural_numbers)

#stage_box & scrollbar stuff
stage_frame = VerticalScrolledFrame(master, width=290, height=120, bd=1, relief="sunken")
stage_frame.grid(row=6, column=0, columnspan=2, sticky=E+N+S+W, padx=(40,0), pady=4)
stage_frame.interior.columnconfigure(0,weight=1)

string_frame = VerticalScrolledFrame(master, width=290, height=20, bd=1, relief="sunken")
string_frame.grid(row=8, column=0, columnspan=2, sticky="wnse", padx=(40,0), pady=4)
string_frame.interior.columnconfigure(0,weight=1)
master.rowconfigure(8, weight=1)


radiant = BooleanVar()
ttk.Checkbutton(master, variable=radiant, text="radiant").grid(row=0, sticky=W)
ttk.Label(master, text="weight:").grid(row=1, sticky=W, padx=(20,0))
weight = ttk.Entry(master, validate="key", validatecommand=(int_validation, '%P', '%W'))
weight.insert(10,0)
weight.grid(row=1, column=1, sticky="ew")
abandonable = BooleanVar()
ttk.Checkbutton(master, variable=abandonable, text="abandonable").grid(row=2, sticky=W)
repeatable = BooleanVar()
ttk.Checkbutton(master, variable=repeatable, text="repeatable").grid(row=3, sticky=W)
ttk.Label(master, text="activeStage:").grid(row=4, sticky=W, padx=(20,0))
activeStage = ttk.Entry(master, validate="key", validatecommand=(int_validation, '%P', '%W'))
activeStage.insert(10,0)
activeStage.grid(row=4, column=1, sticky=E+W)
ttk.Label(master, text="Stages:").grid(row=5, sticky=W, padx=(20,0))
new_stage(0)

new_string_button = ttk.Button(master, command=new_string_name, text="New String")
new_string_button.grid(row=9, column=0, columnspan=3, pady=(4,20), padx=(40,0))

def minimize():
	minimizeButton.winfo_toplevel().iconify()
	print(minimizeButton.bbox(), minimizeButton.winfo_rootx())

def sizes():
	return root.geometry()

ttk.Label(master, text="Strings:").grid(row=7, sticky=W, padx=(20,0))
bottom_frame = ttk.Frame(master)
bottom_frame.grid(row=11, columnspan=2, sticky=S)
ttk.Button(bottom_frame, text='Quit', command=root.quit).grid(column=0, sticky=S)
ttk.Button(bottom_frame, text='Show', command=create_json).grid(row=0, column=1, sticky=S)
ttk.Button(bottom_frame, text="BBox", command=lambda:print(sizes())).grid(column=3,row=0,sticky=S)
minimizeButton = ttk.Button(bottom_frame, text='Show', command=lambda: minimize())
minimizeButton.grid(row=0, column=2, sticky=S)

mainloop()
