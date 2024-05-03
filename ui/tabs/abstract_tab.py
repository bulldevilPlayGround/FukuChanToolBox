from tkinter import ttk

class tkTabFrame(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill='both', expand=True)
        self.create_widgets()

    def create_widgets(self):
        pass
