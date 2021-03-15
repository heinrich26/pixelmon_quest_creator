import platform
import urllib.request
from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from tkinter import font
import pyglet
from tkinterhtml import HtmlFrame
from tkhtmlview import HTMLScrolledText
import ssl

# This restores the same behavior as before.
context = ssl._create_unverified_context()


current_os = platform.system()

if current_os == "Windows" or current_os == "Darwin":
    pyglet.font.add_file("src/fonts/unifont-13.0.06.ttf")
    pyglet.font.add_file("src/fonts/minecraft_font.ttf")

formatting_codes = {
    "§0": "\"background:#fff;color:#000000;\"",
    "§1": "\"background:#000;color: #0000AA;\"",
    "§2": "\"background:#000;color: #00AA00;\"",
    "§3": "\"background:#000;color: #00AAAA;\"",
    "§4": "\"background:#000;color: #AA0000;\"",
    "§5": "\"background:#000;color: #AA00AA;\"",
    "§6": "\"background:#000;color: #FFAA00;\"",
    "§7": "\"background:#000;color: #AAAAAA;\"",
    "§8": "\"background:#000;color: #555555;\"",
    "§9": "\"background:#000;color: #5555FF;\"",
    "§a": "\"background:#000;color: #55FF55;\"",
    "§b": "\"background:#000;color: #55FFFF;\"",
    "§c": "\"background:#000;color:#FF5555;\"",
    "§d": "\"background:#000;color: #FF55FF;\"",
    "§e": "\"background:#000;color: #FFFF55;\"",
    "§f": "\"background:#000;color: #ffffff;\"",
    "§k": "\"font-family:Wingdings;\"",
    "§l": "\"font-weight: bold;\"",
    "§m": "\"text-decoration: line-through;\"",
    "§n": "\"text-decoration: underline;\"",
    "§o": "\"font-style: italic\""
}

# formatting_codes = [
#     "§0",
#     "§1",
#     "§2",
#     "§3",
#     "§4",
#     "§5",
#     "§6",
#     "§7",
#     "§8",
#     "§9",
#     "§a",
#     "§b",
#     "§c",
#     "§d",
#     "§e",
#     "§f",
#     "§k",
#     "§l",
#     "§m",
#     "§n",
#     "§o"
# ]
#
formatting_names = [ "black","dark_blue","dark_green","dark_aqua","dark_red","dark_purple","gold","gray","dark_gray","blue","green","aqua","red","light_purple","yellow","white","obfuscated","bold","striketrough","underline","italic" ]

def find_all(str, sub):
    start = 0
    while True:
        start = str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)




class JSON_text_Generator(object):
    """docstring for JSON_text_Generator."""

    def __init__(self, text=""):
        self.text = text
        if __name__ == "__main__":
            json_frame = ttk.Frame(root)
            json_frame.pack(fill=BOTH, expand=1)
        else:
            json_frame = Toplevel(root)
            json_frame.title("Configure JSON Text")
            json_frame.grab_set()
            json_frame.maxsize(500, 200)
        json_frame.columnconfigure(0, weight=1, minsize=300)
        ttk.Label(json_frame, text="Enter formatted Text:").grid(row=0, column=0, sticky=W, pady=4, padx=4)
        self.text_field = Text(json_frame, font=("Minecraft Regular", 16), height=6, width=30, wrap=WORD)
        self.text_field.grid(row=1, column=0, padx=(4,0), sticky=W+E)
        self.text_field.bind("<KeyRelease>", self.update_prev_text)
        self.text_scrollbar = ttk.Scrollbar(json_frame, orient=VERTICAL, command=self.text_field.yview)
        self.text_scrollbar.grid(row=1,column=1,sticky=N+S+W, padx=(0,4))
        self.text_field["yscrollcommand"] = self.text_scrollbar.set
        ttk.Label(json_frame, text="Preview Output (obfuscated is not acurate):").grid(row=2, column=0, sticky=W, pady=4, padx=4)
        #self.prev_field = HTMLScrolledText(json_frame, html="", font=("Minecraft Regular", 16), width=30, takefocus=0, state="disabled", height=6)
        json_frame.rowconfigure(3, weight=1)
        limiter  = ttk.Frame(json_frame, width=10, height=4)
        limiter.grid(row=3, column=0, padx=4, pady=(0,4), columnspan=2)
        self.prev_field = HtmlFrame(limiter, takefocus=0)
        self.prev_field.pack(pady=(0,4))

        formatting_info = ttk.Treeview(json_frame, columns=("name"))
        formatting_info.grid(row=1, column=2, padx=4, rowspan=3, sticky=N+S)
        formatting_info.column("#0", width=100, anchor=CENTER)
        formatting_info.heading('#0', text="Formatting Code")
        formatting_info.heading("name", text="Name")
        formatting_info.column("name", width=170)

        [formatting_info.insert("", END, key, text=key, values=(formatting_names[list(formatting_codes.keys()).index(key)]), tags=(formatting_names[list(formatting_codes.keys()).index(key)])) for key in list(formatting_codes.keys())]
        formatting_info.insert("", 21, "§r", text="§r", values=("reset"), tags="black")
        self.obfuscated = PhotoImage(file="src/obfuscated.gif")
        formatting_info.set("§k","§k")

        formatting_info.tag_configure("red", foreground="#FF5555", font=("Minecraft Regular", 10))
        formatting_info.tag_configure("blue", foreground="#5555FF", font=("Minecraft Regular", 10))
        formatting_info.tag_configure("green", foreground="#55FF55", font=("Minecraft Regular", 10))
        formatting_info.tag_configure("dark_blue", foreground="#0000AA", font=("Minecraft Regular", 10))
        formatting_info.tag_configure("dark_aqua", foreground="#00AAAA", font=("Minecraft Regular", 10))
        formatting_info.tag_configure("white", foreground="#ffffff", background="#AAAAAA", font=("Minecraft Regular", 10))
        formatting_info.tag_configure("black", foreground="#000000", font=("Minecraft Regular", 10))
        formatting_info.tag_configure("dark_gray", foreground="#555555", font=("Minecraft Regular", 10))
        formatting_info.tag_configure("gray", foreground="#AAAAAA", font=("Minecraft Regular", 10))
        formatting_info.tag_configure("dark_purple", foreground="#AA00AA", font=("Minecraft Regular", 10))
        formatting_info.tag_configure("light_purple", foreground="#FF55FF", font=("Minecraft Regular", 10))
        formatting_info.tag_configure("dark_red", foreground="#AA0000", font=("Minecraft Regular", 10))
        formatting_info.tag_configure("yellow", foreground="#FFFF55", background="#AAAAAA", font=("Minecraft Regular", 10))
        formatting_info.tag_configure("gold", foreground="#FFAA00", font=("Minecraft Regular", 10))
        formatting_info.tag_configure("aqua", foreground="#55FFFF", font=("Minecraft Regular", 10))
        formatting_info.tag_configure("dark_green", foreground="#00AA00", font=("Minecraft Regular", 10))
        formatting_info.tag_configure("bold", font=("Minecraft Regular", 10, "bold"))
        formatting_info.tag_configure("italic", font=("Minecraft Regular", 10, "italic"))
        formatting_info.tag_configure("obfuscated", foreground="#000000",font=("Minecraft Regular", 10), image=self.obfuscated)
        formatting_info.tag_configure("underline", font=("Minecraft Regular", 10, "underline"))
        formatting_info.tag_configure("striketrough", font=("Minecraft Regular", 10, "overstrike"))


    def update_prev_text(self, e):
        global color_formatting
        user_input = self.text_field.get(1.0,END).replace("\n", "<br>").replace("\\n", "<br>")
        # replacements = 0
        formatted_string = str(user_input)
        formatted_string = formatted_string.replace("§r", "</span>")
        for key in list(formatting_codes.keys()):
            formatted_string = formatted_string.replace(key,"<span style=" + formatting_codes[key] + ">")
        spans_to_close = 0
        spans_to_close = formatted_string.count("<span style=") - formatted_string.count("</span>")
        spans = []
        formatted_string += "".join("</span>" for i in range(0, spans_to_close))
        print(formatted_string, spans_to_close)

        html = """<html><body style="background:#000;word-warp:break-word;font-family:minecraft_font;font-size:26px;color:#fff;width:500px;">""" + str(formatted_string) + "</body></html>"
        self.prev_field.set_content(html)

        #self.prev_field.set_html(html)
        # print(user_input, type(user_input))
        formatting_info.delete(0.0,END)
        # [self.prev_field.mark_unset(mark) for mark in self.prev_field.mark_names()[2:]]
        formatting_info.insert(0.0, user_input)
        # replacements = 0
        # for x in formatting_codes:
        #     counter = 0
        #     for occurance in list(find_all(user_input, x)):
        #         self.prev_field.mark_set(formatting_tags[formatting_codes.index(x)] + "-" + str(counter), float("1." + str(occurance-replacements*2)))
        #         self.prev_field.delete(float("1." + str(occurance-replacements*2)), float("1." + str(occurance+2-replacements*2)))
        #         print(float("1." + str(occurance+2-replacements*2)))
        #         counter += 1
        #         replacements += 1
        # print(self.prev_field.mark_names(),self.prev_field.get(1.0,END))
        # for mark in self.prev_field.mark_names()[2:]:
        #     self.prev_field.tag_add(mark.split("-")[0], self.prev_field.index(mark), END)

        # if "§" in user_input:
        #     index = user_input.find("§")
        #     index2 = user_input.find("§", index+1)
        #     if user_input[index+1] in color_formatting and user_input[index2:index2+2] == "§r":
        #         prev_field.bind()



if __name__ == "__main__":

    root = Tk()
    root.title("JSON Text Generator")
    root.maxsize(1000000000, 500)
    mcfont = font.Font(name="mc font", family="mc font", font=("Minecraft Regular", 16))

    app = JSON_text_Generator()

    mainloop()
