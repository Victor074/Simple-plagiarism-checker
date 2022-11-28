from tkinter import *
from tkinter import filedialog
import tkinter.messagebox

from class_plag import plag_checker

class GUI(plag_checker):

    def browseFiles(self):
        self.label_1 = filedialog.askopenfilename(initialdir = "C:/Users/valc2/Documents/GitHub/Simple-plagiarism-checker/",
                                            title = "Select a File",
                                            filetypes=[("Python file", "*.py*")])
        
        # Change label contents
        self.label_file_explorer.configure(text=self.label_1)

    def browseFiles_2(self):
        self.label_2 = filedialog.askopenfilename(initialdir = "C:/Users/valc2/Documents/GitHub/Simple-plagiarism-checker/",
                                            title = "Select a File",
                                            filetypes=[("Python file", "*.py*")])
        
        # Change label contents
        self.label_file_explorer_1.configure(text=self.label_2)
    
    def run_plag_check(self):
        if self.label_1!="" and self.label_2!="":
            score_plag = self.run(self.label_1,self.label_2) * 100
            score_plag = round(score_plag,4)
            if score_plag <= 100.0 and score_plag>=90:
                color="red"
            elif score_plag<=89 and score_plag>=50:
                color="orange"
            elif score_plag<=49 and score_plag>=25:
                color="yellow"
            else:
                color="green"

            self.score.configure(text=score_plag,fg=color)
        else:
            tkinter.messagebox.showwarning("WARNING", "Please search for a script before running function")
    
    def create_window(self):
        self.label_1 = ""
        self.label_2 = ""
        self.window = Tk()
        self.window.title("Plagiarism checker")
        self.window.geometry("800x300")
        self.window.config(background="white")
        
        self.create_labels()
        self.create_buttons()
        self.window.mainloop()
    
    def create_labels(self):
        self.label_file_explorer = Label(self.window,
                            text = "First file",font = ("Microsoft JhengHei",10))

        self.label_file_explorer_1 = Label(self.window,
                            text = "Second file",font=("Microsoft JhengHei",10))

        self.score = Label(self.window,
                            text = "0.0",font=("Microsoft JhengHei",24))
        #self.score.pack()
    

        self.label_file_explorer.grid(column = 2, row = 1)
        self.label_file_explorer_1.grid(column = 2, row = 2)
        self.score.grid(column = 1, row = 10)
        self.score.place(relx=0.5,rely=0.5,anchor=N)
    
    def create_buttons(self):
        self.button_explore = Button(self.window,
                        text = "Browse File",
                        command = self.browseFiles)
        self.button_explore_1 = Button(self.window,
                        text = "Browse File",
                        command = self.browseFiles_2)
        self.check_plag = Button(self.window,
                        text = "Run",
                        command = self.run_plag_check)

        self.button_explore.grid(column = 1, row = 1)
        self.button_explore_1.grid(column = 1, row = 2)
        self.check_plag.grid(column = 1, row = 8)
        self.check_plag.place(relx=0.5,rely=0.5,anchor=S)
        

obj = GUI()
obj.create_window()

                                                                                                