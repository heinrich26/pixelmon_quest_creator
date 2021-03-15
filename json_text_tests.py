import tkinter as tk

class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.tag_vars = {
            "underline": tk.IntVar(),
            "red": tk.IntVar(),
            }

        self.text = MyText(self, width=40, height=8)
        self.text.tag_configure("red", foreground="red")
        self.text.tag_configure("underline", underline=True)

        toolbar = tk.Frame(self)
        self.underline = tk.Checkbutton(self, text="Underline",
                                        onvalue = True, offvalue=False,
                                        variable = self.tag_vars["underline"]
                                        )
        self.red = tk.Checkbutton(self, text="Red",
                                  onvalue = True, offvalue=False,
                                  variable = self.tag_vars["red"]
                                  )
        self.underline.pack(in_=toolbar, side="left")
        self.red.pack(in_=toolbar, side="left")

        toolbar.pack(side="top", fill="x")
        self.text.pack(side="top", fill="both", expand=True)

class MyText(tk.Text):
    def __init__(self, parent, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        self.parent = parent

        # add a new bind tag, "CustomText" so we
        # can have code run after the class binding
        # has done it's work
        bindtags = list(self.bindtags())
        i = bindtags.index("Text")
        bindtags.insert(i+1, "CustomText")
        self.bindtags(tuple(bindtags))

        # set a binding that will fire whenever a
        # self-inserting key is pressed
        self.bind_class("CustomText", "<Key>", self.OnKey)

    def OnKey(self, event):
        # we are assuming this is called whenever
        # a character is inserted. Apply or remove
        # each tag depending on the state of the checkbutton
        for tag in self.parent.tag_vars.keys():
            use_tag = self.parent.tag_vars[tag].get()
            if use_tag:
                self.tag_add(tag, "insert-1c", "insert")
            else:
                self.tag_remove(tag, "insert-1c", "insert")

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
