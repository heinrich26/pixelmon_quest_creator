from tkinter import *
from tkinter import ttk
import platform

current_os = platform.system()


class VerticalScrolledFrame(ttk.Frame):
	def __init__(self, parent, *args, **kw):
		def _bound_to_mousewheel(event):
			if current_os == "Linux":
				canvas.bind_all("<Button-4>", _on_mousewheel)
				canvas.bind_all("<Button-5>", _on_mousewheel)
			else:
				canvas.bind_all("<MouseWheel>", _on_mousewheel)

		def _unbound_to_mousewheel(event):
			if current_os == "Linux":
				canvas.unbind_all("<Button-4>")
				canvas.unbind_all("<Button-5>")
			else:
				canvas.unbind_all("<MouseWheel>")

		def _on_mousewheel(event):
			if interior.winfo_reqheight() >= self.winfo_height():
				if current_os == "Darwin":
					canvas.yview_scroll(int(-1*event.delta), "units")
				elif current_os == "Windows":
					canvas.yview_scroll(int(-1*(event.delta/120)), "units")
				elif event.num == 4:
					canvas.yview_scroll(-1, "units")
				else:
					canvas.yview_scroll(1, "units")

		ttk.Frame.__init__(self, parent, *args, **kw)
		self.bind('<Enter>', _bound_to_mousewheel)
		self.bind('<Leave>', _unbound_to_mousewheel)



		# create a canvas object and a vertical scrollbar for scrolling it
		vscrollbar = ttk.Scrollbar(self, orient=VERTICAL)
		vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
		canvas = Canvas(self, borderwidth=0, highlightthickness=0,
						yscrollcommand=vscrollbar.set, relief="sunken")
		if "width" in kw:
			canvas["width"] = kw["width"] - vscrollbar.winfo_width()
		if "height" in kw:
			canvas["height"] = kw["height"]
		canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
		vscrollbar.config(command=canvas.yview)

		# reset the view
		canvas.xview_moveto(0)
		canvas.yview_moveto(0)

		# create a frame inside the canvas which will be scrolled with it
		self.interior = interior = ttk.Frame(canvas)
		interior_id = canvas.create_window(0, 0, window=interior,
										   anchor=NW)

		# track changes to the canvas and frame width and sync them,
		# also updating the scrollbar
		def _configure_interior(event):
			# update the scrollbars to match the size of the inner frame
			size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
			canvas.config(scrollregion="0 0 %s %s" % size)
			if interior.winfo_reqwidth() != canvas.winfo_width():
				# update the canvas's width to fit the inner frame
				canvas.config(width=interior.winfo_reqwidth())
		interior.bind('<Configure>', _configure_interior)

		def _configure_canvas(event):
			if interior.winfo_reqwidth() != canvas.winfo_width():
				# update the inner frame's width to fill the canvas
				canvas.itemconfigure(interior_id, width=canvas.winfo_width())
		canvas.bind('<Configure>', _configure_canvas)



if __name__ == "__main__":

	class SampleApp(Tk):
		def __init__(self, *args, **kwargs):
			root = Tk.__init__(self, *args, **kwargs)


			self.frame = VerticalScrolledFrame(root, width=200, )
			self.frame.pack(expand=TRUE,fill=X)
			self.label = Label(text="Shrink the window to activate the scrollbar.")
			self.label.pack()
			buttons = []
			for i in range(10):
				buttons.append(Button(self.frame.interior, text="Button " + str(i)))
				buttons[-1].pack()

	app = SampleApp()
	app.mainloop()
