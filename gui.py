import tkinter as tk
from time import sleep

class GUI:
    
    

    def __init__(self):
        self.btn_num = -1 # -1 for an unselected value
        self.lbl_initialized = False
        self.message = ""

        self.text_size = 18
        self.btn_text_size = 26
        self.btn_padding = 5
        
    def __del__(self):
        self.window.destroy()

    def start_window(self):
        #windows parameters
        self.window = tk.Tk()
        self.window.geometry("800x480")
        self.window.title("EVA")

        for i in range(4):  # 2 rows
            for j in range(2):  # 4 columns
                button = tk.Button(self.window, text=f"    {i*2 + j + 1}    ",
                    font=("calibri",self.btn_text_size),
                    command=lambda num=i*2 + j + 1: self.get_val_from_pressed_btn(num))
                button.grid(row=i, column=j, padx=self.btn_padding, pady=self.btn_padding)

        #output lbl (this just display what would normally go in terminal)
        self.lbl = tk.Label(self.window,text="CONSOLE LOG",font=("calibri", self.text_size), justify="left", height=12, width=60, anchor="w")
        self.lbl.grid(row=0, rowspan=4, column=2, columnspan=300, padx=20, pady=10) #300 cols for this label because thats prob how many chars per line
        self.lbl_initialized = True

        # yes no pause and wait buttons
        self.btn_yes = tk.Button(self.window, text="  YES  ", font=("calibri", self.btn_text_size), command=lambda: self.get_val_from_pressed_btn("y"))
        self.btn_yes.grid(row=6, column=0, padx=self.btn_padding, pady=self.btn_padding)
        self.btn_no = tk.Button(self.window, text="  NO   ", font=("calibri", self.btn_text_size), command=lambda: self.get_val_from_pressed_btn("n"))
        self.btn_no.grid(row=6, column=1, padx=self.btn_padding, pady=self.btn_padding)
        self.btn_pause = tk.Button(self.window, text=" PAUSE ", anchor="w", font=("calibri", self.btn_text_size), command=lambda: self.get_val_from_pressed_btn("pause"))
        self.btn_pause.grid(row=6, column=2, padx=self.btn_padding, pady=self.btn_padding)
        self.btn_skip_set = tk.Button(self.window, text="SKIP SET", font=("calibri", self.btn_text_size), command=lambda: self.get_val_from_pressed_btn("skip"))
        self.btn_skip_set.grid(row=6, column=3, padx=self.btn_padding, pady=self.btn_padding)
        
        #start window
        self.window.mainloop()

    def get_val_from_pressed_btn(self,num):
        self.btn_num = num

    def wait_for_input(self):
        self.btn_num = -1 # reset to default before awaiting an input

        while True:
              sleep(0.01)
              if self.btn_num != -1:
                   return self.btn_num
              
    def lbl_print(self, message):
        self.message = message # store as new message
        self.lbl.config(text=self.message)

    def lbl_add(self, message):
        self.message += message # concatenate to current message
        self.lbl.config(text=self.message)
    

        