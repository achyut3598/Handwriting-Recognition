import tkinter as tk                
from tkinter import font  as tkfont
from tkinter import *
from PIL import Image, ImageTk 

class TensorReaderGui(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        # All frames are stacked on top of eachother using hte container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.alphalabels = ["A.img","B.img","C.img"]
        self.diglabels = ["1.img","2.img","3.img"]
        self.currentalph = 0
        self.currentdig = 0
        
        for myFrame in (HomePage, AlphaPage, DigitPage, HelpPage): #Goes through each page
            page_name = myFrame.__name__
            frame = myFrame(parent=container, controller=self)
            self.frames[page_name] = frame

            # All pages are added in order
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("HomePage")

    def show_frame(self, page_name): #Displays frame for name
        frame = self.frames[page_name]
        frame.tkraise()
        
    def next_dig(self,mylabel): #Goes to the next digit file in the list
        if(self.currentdig == 2):
            self.currentdig = 0
        else:
            self.currentdig = self.currentdig + 1
        mylabel.config(text = self.diglabels[self.currentdig])
            
    def next_alph(self, mylabel): #Goes to the next alpha file in the list
        if(self.currentalph == 2):
            self.currentalph = 0
        else:
            self.currentalph = self.currentalph + 1
        mylabel.config(text = self.alphalabels[self.currentalph])
            
    def prev_dig(self,mylabel): #Goes to the previous digit file in the list
        if(self.currentdig == 0):
            self.currentdig = 2
        else:
            self.currentdig = self.currentdig - 1
        mylabel.config(text = self.diglabels[self.currentdig])
            
    def prev_alph(self, mylabel): #Goes to the previous aloha file in the list
        if(self.currentalph == 0):
            self.currentalph = 2
        else:
            self.currentalph = self.currentalph - 1
        mylabel.config(text = self.alphalabels[self.currentalph])
        
    def alph_results(self,mylabel): #Shows results from tensorflow on that alpha file
        #add tensorflow stuff here using the current alphalabel
        mylabel.config(text = "This is the result from tensorflow on that file: ")
    
    def dig_results(self,mylabel): #Shows results from tensorflow on that digit file
        #add tensorflow stuff here using the current diglabel
        mylabel.config(text = "This is the result from tensorflow on that file: ")

class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Home",font='Helvetica 18 bold')
        label.pack(side=TOP, fill=X, pady=10)
        digbutton = tk.Button(self, text="Read a Digit", command=lambda: controller.show_frame("DigitPage"))
        digbutton.pack(side=TOP, anchor=W, fill=X, expand=YES)
        
        alphbutton = tk.Button(self, text="Read an Alphabetical Character", command=lambda: controller.show_frame("AlphaPage"))
        alphbutton.pack(side=TOP, anchor=W, fill=X, expand=YES)
        
        helpbutton = tk.Button(self, text="Help", command=lambda: controller.show_frame("HelpPage"))
        helpbutton.pack(side=TOP, anchor=W, fill=X, expand=YES)
        

class DigitPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = tk.Label(self, text="Digit",font='Helvetica 18 bold')
        label.pack(side=TOP, fill=X, pady=10)
        
        myresultslabel = tk.Label(self, text="")
        myresultslabel.pack(side=TOP, anchor=W, fill=X, expand=YES)
        
        myfilelabel = tk.Label(self, text=controller.diglabels[controller.currentdig])
        myfilelabel.pack(side=TOP, anchor=W, fill=X, expand=YES)
        
        backbutton = tk.Button(self, text="Go Back", command=lambda: controller.show_frame("HomePage"))
        backbutton.pack(side=BOTTOM, anchor=W, fill=X, expand=YES)
        
        cycleleft = tk.Button(self, text="<", command=lambda: controller.prev_dig(myfilelabel))
        cycleleft.pack(side=LEFT, fill=X, expand=YES)
        
        readbutton = tk.Button(self, text="Read", command=lambda: controller.dig_results(myresultslabel))
        readbutton.pack(side=LEFT, fill=X, expand=YES)
        
        cycleright = tk.Button(self, text=">", command=lambda: controller.next_dig(myfilelabel))
        cycleright.pack(side=LEFT, fill=X, expand=YES)


class AlphaPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = tk.Label(self, text="Alphabetical Character",font='Helvetica 18 bold')
        label.pack(side=TOP, fill=X, pady=10)
        
        myresultslabel = tk.Label(self, text="")
        myresultslabel.pack(side=TOP, anchor=W, fill=X, expand=YES)
        
        myfilelabel = tk.Label(self, text=controller.alphalabels[controller.currentalph])
        myfilelabel.pack(side=TOP, anchor=W, fill=X, expand=YES)
        
        backbutton = tk.Button(self, text="Go Back", command=lambda: controller.show_frame("HomePage"))
        backbutton.pack(side=BOTTOM, anchor=W, fill=X, expand=YES)
        
        cycleleft = tk.Button(self, text="<", command=lambda: controller.prev_alph(myfilelabel))
        cycleleft.pack(side=LEFT, fill=X, expand=YES)
        
        readbutton = tk.Button(self, text="Read", command=lambda: controller.alph_results(myresultslabel))
        readbutton.pack(side=LEFT, fill=X, expand=YES)
        
        cycleright = tk.Button(self, text=">", command=lambda: controller.next_alph(myfilelabel))
        cycleright.pack(side=LEFT, fill=X, expand=YES)

class HelpPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = tk.Label(self, text="Help",font='Helvetica 18 bold')
        label.pack(side=TOP, fill=X, pady=10)
        
        backbutton = tk.Button(self, text="Go Back", command=lambda: controller.show_frame("HomePage"))
        backbutton.pack(side=TOP, anchor=W, fill=X, expand=YES)

        

if __name__ == "__main__":
    app = TensorReaderGui()
    app.mainloop()