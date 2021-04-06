import platform
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter.font import Font
from tkinter import messagebox
import sys
import trace
import threading
import time
import random
import pyglet

current_os = platform.system()

if current_os == "Windows" or current_os == "Darwin":
	pyglet.font.add_file("src/fonts/minecraft_font.ttf")

formatting_codes = {
	"§0": "\"background:#fff;color:#000000;\"",
	"§1": "\"background:#000;color:#0000AA;\"",
	"§2": "\"background:#000;color:#00AA00;\"",
	"§3": "\"background:#000;color:#00AAAA;\"",
	"§4": "\"background:#000;color:#AA0000;\"",
	"§5": "\"background:#000;color:#AA00AA;\"",
	"§6": "\"background:#000;color:#FFAA00;\"",
	"§7": "\"background:#000;color:#AAAAAA;\"",
	"§8": "\"background:#000;color:#555555;\"",
	"§9": "\"background:#000;color:#5555FF;\"",
	"§a": "\"background:#000;color:#55FF55;\"",
	"§b": "\"background:#000;color:#55FFFF;\"",
	"§c": "\"background:#000;color:#FF5555;\"",
	"§d": "\"background:#000;color:#FF55FF;\"",
	"§e": "\"background:#000;color:#FFFF55;\"",
	"§f": "\"background:#000;color:#ffffff;\"",
	"§k": "\"font-family:Wingdings;\"",
	"§l": "\"font-weight: bold;\"",
	"§m": "\"text-decoration: line-through;\"",
	"§n": "\"text-decoration: underline;\"",
	"§o": "\"font-style: italic\""
}

formatting_keys = [
	"§0",
	"§1",
	"§2",
	"§3",
	"§4",
	"§5",
	"§6",
	"§7",
	"§8",
	"§9",
	"§a",
	"§b",
	"§c",
	"§d",
	"§e",
	"§f",
	"§k",
	"§l",
	"§m",
	"§n",
	"§o"
]

formatting_names = [ "black","dark_blue","dark_green","dark_aqua","dark_red","dark_purple","gold","gray","dark_gray","blue","green","aqua","red","light_purple","yellow","white","obfuscated","bold","strikethrough","underline","italic","reset", "New Line" ]

formats = {
	"red": "#FF5555",
	"blue": "#5555FF",
	"green": "#55FF55",
	"dark_blue": "#0000AA",
	"dark_aqua": "#00AAAA",
	"white": "#ffffff",
	"black": "#000000",
	"dark_gray": "#555555",
	"gray": "#AAAAAA",
	"dark_purple": "#AA00AA",
	"light_purple": "#FF55FF",
	"dark_red": "#AA0000",
	"yellow": "#FFFF55",
	"gold": "#FFAA00",
	"aqua": "#55FFFF",
	"dark_green": "#00AA00",
	"strikethrough": "overstrike",
	"underline": "underline",
	"bold": "bold",
	"italic": "italic",
	"obfuscated": ""
}



def rm_unused(tuple):
	new_tuple = tuple.copy()
	for key in new_tuple:
		if len(new_tuple[key]) >= 2:
			for format in new_tuple[key]:
				if format in formatting_names[0:16]:
					for name in formatting_names[0:16]:
						if str(name) != str(format) and name in new_tuple[key]:
							new_tuple[key].remove(name)
					break
			for format in new_tuple[key]:
				for i in range(1,new_tuple[key].count(format)):
					new_tuple[key].remove(format)
	return new_tuple

alphabet = [
"i,;.:!|î", # 1px
"l'`Ììí·´", # 2px
"It[]ÍÎÏïªº•°", #3px
"""kf(){}*¤²”\"""", # 4px
"""ABCDEFGHJKLMNOPQRSTUVWXYZabcdeghjmnopqrsuvwxyz/?$%&+-#_¯=^¨£ÀÁÂÃÄÅÇÈÉÊËÑÒÓÔÕÖÙÚÛÜÝàáâãäåçèéêëñðòóôõöùúûüýÿ0123456789Ææß×¼½¿¬«»""", # 5px
"~@®÷±"]

class Safe_Thread(threading.Thread):
  def __init__(self, *args, **keywords):
    threading.Thread.__init__(self, *args, **keywords)
    self.killed = False

  def start(self):
    self.__run_backup = self.run
    self.run = self.__run
    threading.Thread.start(self)

  def __run(self):
    sys.settrace(self.globaltrace)
    self.__run_backup()
    self.run = self.__run_backup

  def globaltrace(self, frame, event, arg):
    if event == 'call':
      return self.localtrace
    else:
      return None

  def localtrace(self, frame, event, arg):
    if self.killed:
      if event == 'line':
        raise SystemExit()
    return self.localtrace

  def kill(self):
    self.killed = True


class animate_obfuscated_text(object):
	def __init__(self, text, starts, ends):
		self.text = text
		self.starts = starts
		self.ends = ends

	def animate_text(self):
		return self.text[0:self.starts[0]] + "".join([self.randtext(i) + self.text[self.ends[i]:self.starts[i+1]] if len(self.starts)-1 != i else self.randtext(i) + self.text[self.ends[i]:] for i in range(0, len(self.starts))])

	def next(self):
		return self.animate_text()

	def randtext(self, i):
		return "".join([self.randchar(char) for char in self.text[self.starts[i]:self.ends[i]]])

	def randchar(self, i):
		global alphabet
		if i == " ":
			return " "
		elif i in alphabet[0]:
			return alphabet[0][random.randrange(0,7,1)]
		elif i in alphabet[1]:
			return alphabet[1][random.randrange(0,7,1)]
		elif i in alphabet[2]:
			return alphabet[2][random.randrange(0,11,1)]
		elif i in alphabet[3]:
			return alphabet[3][random.randrange(0,10,1)]
		elif i in alphabet[4]:
			return alphabet[4][random.randrange(0, len(alphabet[4])-1,1)]
		elif i in alphabet[5]:
			return alphabet[5][random.randrange(0,4,1)]
		else:
			return i

	# def refresh(self):
	#     self.var.set("".join([self.randchar(char) for char in self.text]))
	#     self.self.after(100, self.refresh)


class JSON_text_Generator(object):
	def __init__(self, master, string_name):
		self.string_name = string_name
		self.user_input = "This is a §6formatted§r §lstring!"
		self.self = master
		self.edit_string()

	def edit_string(self):
		self.is_alive = False
		if __name__ == "__main__":
			self.json_frame = ttk.Frame(root)
			self.json_frame.pack(fill=BOTH, expand=1)
			root.protocol("WM_DELETE_WINDOW", self.close_event)
		else:
			self.json_frame = Toplevel(self.self)
			self.json_frame.title("Configure JSON Text")
			self.json_frame.grab_set()
			self.json_frame.transient(self.self)
			self.json_frame.minsize(800, self.json_frame.winfo_height())
			self.json_frame.protocol("WM_DELETE_WINDOW", self.close_event)
		self.json_frame.columnconfigure(0, weight=1, minsize=300)
		self.json_frame.bind_all("<Control-s>", lambda event: self.save_input())
		self.json_frame.rowconfigure((1,3), weight=1)


		# Input field & Label
		ttk.Label(self.json_frame, text="Enter formatted Text (try to avoid gray):").grid(row=0, column=0, sticky=W, pady=4, padx=4)
		self.text_field = Text(self.json_frame, font=("Minecraft Regular", 16), height=6, width=30, wrap=WORD)
		self.text_field.insert(1.0, self.user_input)
		self.text_field.grid(row=1, column=0, padx=(4,0), sticky="nesw")
		self.text_field.bind("<KeyRelease>", self.UpdatePreview)
		self.text_field.focus_set()
		self.text_scrollbar = ttk.Scrollbar(self.json_frame, orient=VERTICAL, command=self.text_field.yview)
		self.text_scrollbar.grid(row=1, column=1, sticky=N+S+W, padx=(0,4))
		self.text_field["yscrollcommand"] = self.text_scrollbar.set

		# Preview field & Label
		ttk.Label(self.json_frame, text="Preview Output:").grid(row=2, column=0, sticky=W, pady=4, padx=4)

		self.prev_field = Text(self.json_frame, font=("Minecraft Regular", 16), height=6, width=30, wrap=WORD, foreground="#fff", background="#AEAEAE")
		self.prev_field.grid(row=3, column=0, padx=(4,0), sticky="nesw")
		self.prev_field.bind('<Key>', lambda event: "break")
		self.prev_scrollbar = ttk.Scrollbar(self.json_frame, orient=VERTICAL, command=self.prev_field.yview)
		self.prev_scrollbar.grid(row=3, column=1, sticky=N+S+W, padx=(0,4))
		self.prev_field["yscrollcommand"] = self.prev_scrollbar.set

		self.UpdatePreview("event_dummy")


		# infographic
		self.formatting_info = Frame(self.json_frame, bg="#a2a9b1")
		self.formatting_info.grid(row=0, column=2, padx=4, rowspan=4, sticky=N, pady=(4,0))
		self.formatting_info.bind_all("<ButtonRelease>", self.UpdatePreview)
		ttk.Label(self.formatting_info, font=("Minecraft Regular", 9), text="Code", anchor="c").grid(row=0, column=0, sticky=W+E, pady=1, ipady=3, padx=1)
		ttk.Label(self.formatting_info, font=("Minecraft Regular", 9), text="Name", anchor="c").grid(row=0, column=1, sticky=W+E, pady=1, ipady=3, padx=(0,1))


		Button(self.formatting_info, text="§0", font=("Minecraft Regular", 9), foreground="#fff", background="#000", command=lambda: self.text_field.insert(INSERT, "§0")).grid(row=1, column=0, sticky=W+E, pady=(0,1), padx=1)
		Button(self.formatting_info, text="§1", font=("Minecraft Regular", 9), foreground="#fff", background="#00a", command=lambda: self.text_field.insert(INSERT, "§1")).grid(row=2, column=0, sticky=W+E, pady=(0,1), padx=1)
		Button(self.formatting_info, text="§2", font=("Minecraft Regular", 9), foreground="#fff", background="#0a0", command=lambda: self.text_field.insert(INSERT, "§2")).grid(row=3, column=0, sticky=W+E, pady=(0,1), padx=1)
		Button(self.formatting_info, text="§3", font=("Minecraft Regular", 9), foreground="#fff", background="#0aa", command=lambda: self.text_field.insert(INSERT, "§3")).grid(row=4, column=0, sticky=W+E, pady=(0,1), padx=1)
		Button(self.formatting_info, text="§4", font=("Minecraft Regular", 9), foreground="#fff", background="#a00", command=lambda: self.text_field.insert(INSERT, "§4")).grid(row=5, column=0, sticky=W+E, pady=(0,1), padx=1)
		Button(self.formatting_info, text="§5", font=("Minecraft Regular", 9), foreground="#fff", background="#a0a", command=lambda: self.text_field.insert(INSERT, "§5")).grid(row=6, column=0, sticky=W+E, pady=(0,1), padx=1)
		Button(self.formatting_info, text="§6", font=("Minecraft Regular", 9), foreground="#000", background="#fa0", command=lambda: self.text_field.insert(INSERT, "§6")).grid(row=7, column=0, sticky=W+E, pady=(0,1), padx=1)
		Button(self.formatting_info, text="§7", font=("Minecraft Regular", 9), foreground="#000", background="#aaa", command=lambda: self.text_field.insert(INSERT, "§7")).grid(row=8, column=0, sticky=W+E, pady=(0,1), padx=1)
		Button(self.formatting_info, text="§8", font=("Minecraft Regular", 9), foreground="#fff", background="#555", command=lambda: self.text_field.insert(INSERT, "§8")).grid(row=9, column=0, sticky=W+E, pady=(0,1), padx=1)
		Button(self.formatting_info, text="§9", font=("Minecraft Regular", 9), foreground="#fff", background="#55f", command=lambda: self.text_field.insert(INSERT, "§9")).grid(row=10, column=0, sticky=W+E, pady=(0,1), padx=1)
		Button(self.formatting_info, text="§a", font=("Minecraft Regular", 9), foreground="#000", background="#5f5", command=lambda: self.text_field.insert(INSERT, "§a")).grid(row=11, column=0, sticky=W+E, pady=(0,1), padx=1)
		Button(self.formatting_info, text="§b", font=("Minecraft Regular", 9), foreground="#000", background="#5ff", command=lambda: self.text_field.insert(INSERT, "§b")).grid(row=12, column=0, sticky=W+E, pady=(0,1), padx=1)
		Button(self.formatting_info, text="§c", font=("Minecraft Regular", 9), foreground="#000", background="#f55", command=lambda: self.text_field.insert(INSERT, "§c")).grid(row=13, column=0, sticky=W+E, pady=(0,1), padx=1)
		Button(self.formatting_info, text="§d", font=("Minecraft Regular", 9), foreground="#000", background="#f5f", command=lambda: self.text_field.insert(INSERT, "§d")).grid(row=14, column=0, sticky=W+E, pady=(0,1), padx=1)
		Button(self.formatting_info, text="§e", font=("Minecraft Regular", 9), foreground="#000", background="#ff5", command=lambda: self.text_field.insert(INSERT, "§e")).grid(row=15, column=0, sticky=W+E, pady=(0,1), padx=1)
		Button(self.formatting_info, text="§f", font=("Minecraft Regular", 9), foreground="#000", background="#fff", command=lambda: self.text_field.insert(INSERT, "§f")).grid(row=16, column=0, sticky=W+E, pady=(0,1), padx=1)
		Button(self.formatting_info, text="§k", font=("Minecraft Regular", 9), foreground="#000", background="#fff", command=lambda: self.text_field.insert(INSERT, "§k")).grid(row=17, column=0, sticky=W+E, pady=(0,1), padx=1)
		Button(self.formatting_info, text="§l", font=("Minecraft Regular", 9), foreground="#000", background="#fff", command=lambda: self.text_field.insert(INSERT, "§l")).grid(row=18, column=0, sticky=W+E, pady=(0,1), padx=1)
		Button(self.formatting_info, text="§m", font=("Minecraft Regular", 9), foreground="#000", background="#fff", command=lambda: self.text_field.insert(INSERT, "§m")).grid(row=19, column=0, sticky=W+E, pady=(0,1), padx=1)
		Button(self.formatting_info, text="§n", font=("Minecraft Regular", 9), foreground="#000", background="#fff", command=lambda: self.text_field.insert(INSERT, "§n")).grid(row=20, column=0, sticky=W+E, pady=(0,1), padx=1)
		Button(self.formatting_info, text="§o", font=("Minecraft Regular", 9), foreground="#000", background="#fff", command=lambda: self.text_field.insert(INSERT, "§o")).grid(row=21, column=0, sticky=W+E, pady=(0,1), padx=1)
		Button(self.formatting_info, text="§r", font=("Minecraft Regular", 9), foreground="#000", background="#fff", command=lambda: self.text_field.insert(INSERT, "§r")).grid(row=22, column=0, sticky=W+E, pady=(0,1), padx=1)
		Button(self.formatting_info, text="\\n", font=("Minecraft Regular", 9), foreground="#000", background="#fff", command=lambda: self.text_field.insert(INSERT, "\\n")).grid(row=23, column=0, sticky=W+E, pady=(0,1), padx=1)

		for i in range(0, 23):
			if i <= 14:
				if i in (0,1,2,3,4,5,8,9):
					ttk.Label(self.formatting_info, text=formatting_names[i], font=("Minecraft Regular", 9), anchor="c", foreground="#fff",background=list(formatting_codes.values())[i][23:30]).grid(row=i+1, column=1, sticky=W+E+N+S, pady=(1,2), padx=(0,3))
				else:
					ttk.Label(self.formatting_info, text=formatting_names[i], font=("Minecraft Regular", 9), anchor="c", background=list(formatting_codes.values())[i][23:30]).grid(row=i+1, column=1, sticky=W+E+N+S, pady=(1,2), padx=(0,3))
			elif i in (15,21,22):
				ttk.Label(self.formatting_info, anchor="c", background="white", font=("Minecraft Regular", 9), text=formatting_names[i]).grid(row=i+1, column=1, sticky=W+E+N+S, pady=(1,2), padx=(0,3))

		self.obfuscated_text = StringVar(value="obfuscated")
		self.obfuscated_example = ttk.Label(self.formatting_info, background="white", anchor="c", font=("Minecraft Regular", 9), width=10, textvariable=self.obfuscated_text, foreground="#000")
		self.obfuscated_example.grid(row=17, column=1, sticky=W+E+N+S, pady=(1,2), padx=(0,3))

		ttk.Label(self.formatting_info, background="white", anchor="c", font=("Minecraft Regular", 9, "bold"), text=formatting_names[17], foreground="#000").grid(row=18, column=1, sticky=W+E+N+S, pady=(1,2), padx=(0,3))
		ttk.Label(self.formatting_info, background="white", anchor="c", font=("Minecraft Regular", 9, "overstrike"), text=formatting_names[18], foreground="#000").grid(row=19, column=1, sticky=W+E+N+S, pady=(1,2), padx=(0,3))
		ttk.Label(self.formatting_info, background="white", anchor="c", font=("Minecraft Regular", 9, "underline"), text=formatting_names[19], foreground="#000").grid(row=20, column=1, sticky=W+E+N+S, pady=(1,2), padx=(0,3))
		ttk.Label(self.formatting_info, background="white", anchor="c", font=("Minecraft Regular", 9, "italic"), text=formatting_names[20], foreground="#000").grid(row=21, column=1, sticky=W+E+N+S, pady=(1,2), padx=(0,3))

		ttk.Button(self.json_frame, text="Save", command=self.save_input).grid(row=4, column=2, padx=4, pady=4, sticky=E)

		if not __name__ == "__main__":
			self.json_frame.wait_window()
		return self.user_input

	def close_event(self):
		dialogue = Toplevel(self.json_frame)
		if __name__ == "__main__":
			dialogue.protocol("WM_DELETE_WINDOW", root.destroy)
		else:
			dialogue.protocol("WM_DELETE_WINDOW", self.json_frame.destroy)
		dialogue.title("Unsaved Changes")
		ttk.Label(dialogue, text="String hasn't been saved!", font=("TkTextFont", 10,"bold")).grid(row=0, column=0, columnspan=3, pady=(8,2))
		ttk.Label(dialogue, text="Do you want to save bevore closing?").grid(row=1, columnspan=3)
		dialogue.rowconfigure(2, uniform="fred")
		ttk.Button(dialogue, text="Save", command=self.save_input).grid(row=2, column=1, pady=(20,8), padx=8)
		if __name__ == "__main__":
			ttk.Button(dialogue, text="Don't Save", command=root.destroy).grid(row=2, column=2, pady=(20,8), padx=8)
		else:
			ttk.Button(dialogue, text="Don't Save", command=self.json_frame.destroy).grid(row=2, column=2, pady=(20,8), padx=8)
		ttk.Button(dialogue, text="Cancel", command=dialogue.destroy).grid(row=2, column=0, pady=(20,8), padx=8)
		dialogue.transient(self.json_frame)
		dialogue.wait_visibility()
		dialogue.grab_set()
		dialogue.wait_window()


	def save_input(self):
		self.user_input = self.text_field.get(1.0,END)[:-1].replace("\n", "\\n").rstrip("\\n")
		if __name__=="__main__":
			root.destroy()
		else:
			self.json_frame.destroy()


	def setup_tag(self, inp_stack):
		global formats
		args = { "font": ["Minecraft Regular", 16] }
		for format in inp_stack:
			if formats[format] == "":
				pass
			elif formats[format][0] == "#":
				args["foreground"] = formats[format]
			else:
				args["font"].append(formats[format])
		args["font"] = tuple(args["font"])
		return args


	def obfuscated_thread(self, current_text):
		self.is_alive = True
		while current_text == self.text_field.get(1.0, END) and self.is_alive:
			self.prev_field.delete(1.0, END)
			self.prev_field.insert(1.0, self.animated_text.next())
			for i in self.tags.keys():
				self.prev_field.tag_add(i, *self.tag_ranges[i])
				self.prev_field.tag_config(i, **self.tags[i])
			time.sleep(0.15)


	def UpdatePreview(self, event):
		self.is_alive = False
		try:
			self.prev_update_thread.kill()
			self.prev_update_thread.join()
		except:
			pass
		def mk_pos(index):
			if "\n" in raw_text[0:index]:
				new_index = str(index - raw_text.rfind("\n", 0, index)-1)
			else:
				new_index = str(index)
			return str(1 + raw_text.count("\n", 0, index)) + "." + new_index

		def obfuscated_finder(stack_pos):
			if "obfuscated" in stack[stack_keys[stack_pos]]:
				obfuscated_starts.append(stack_keys[stack_pos])
				obfuscated_ends.append(stack_keys[stack_pos+1])

		global formatting_keys
		global formatting_names
		try:
			raw_text = self.text_field.get(1.0,END).replace("\\n", "\n").rstrip("\n")
			for key in "0123456789abcdefklmnor":
				raw_text = raw_text.replace("&" + key, "§" + key)
		except:
			# assume window is gone
			return

		# stacks
		if len(raw_text) >= 3:
			replacements = 0
			stack = {}
			for i in range(0, len(raw_text)-1):
				if raw_text[i:i+2] in formatting_keys:
					if len(stack) >= 1:
						stack[i-replacements] = list(stack[max(stack.keys())])
					else:
						stack[i-replacements] = []
					stack[i-replacements].insert(0,formatting_names[formatting_keys.index(raw_text[i:i+2])])
					replacements += 2
					i += 1
				if raw_text[i:i+2] == "§r":
					stack[i-replacements] = []
					i += 1
					replacements += 2
			if replacements != 0:
				for code in formatting_keys:
					raw_text = raw_text.replace(code, "")
				raw_text = raw_text.replace("§r", "")
				stack[len(raw_text)] = []

			obfuscated_starts = []
			obfuscated_ends = []


			stack = rm_unused(stack)
			stack_keys = list(stack.keys())
			stack_keys.sort()
			self.prev_field.delete(1.0,END)
			for tag in self.prev_field.tag_names():
				self.prev_field.tag_delete(tag)
			self.prev_field.insert(0.0, str(raw_text))
			for i in range(0,len(stack_keys)):
				if stack[stack_keys[i]] != []:
					self.prev_field.tag_add(i, mk_pos(stack_keys[i]), mk_pos(stack_keys[i+1]))
					self.prev_field.tag_config(i, **self.setup_tag(stack[stack_keys[i]]))
					obfuscated_finder(i)


			if obfuscated_starts != []:
				self.animated_text = animate_obfuscated_text(raw_text, obfuscated_starts, obfuscated_ends)
				self.tags = {i:self.setup_tag(stack[stack_keys[i]]) for i in range(0,len(stack_keys)) if stack[stack_keys[i]]}
				self.tag_ranges = {i:(mk_pos(stack_keys[i]), mk_pos(stack_keys[i+1])) for i in range(0,len(stack_keys)) if stack[stack_keys[i]]}
				self.prev_update_thread = Safe_Thread(target=self.obfuscated_thread, args=(self.text_field.get(1.0, END),))
				self.prev_update_thread.start()
		else:
			self.prev_field.delete(1.0, END)
			self.prev_field.insert(1.0, raw_text)


if __name__ == "__main__":

	root = Tk()
	root.title("JSON Text Generator")
	root.minsize(800, root.winfo_height())
	mcfont = font.Font(name="mc font", family="mc font", font=("Minecraft Regular", 16))

	app = JSON_text_Generator(root, "String")

	mainloop()
