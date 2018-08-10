from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class Focus:

    def __init__(self, master):
        self.master = master
        master.title("Pomodoro")
        master.configure(bg = '#ECECEC')

        # Set styles for widgets                     
        self.style = ttk.Style()
        self.style.configure('TFrame', background = '#C6DEFF')
        self.style.configure('TButton', background = '#C6DEFF')
        self.style.configure('TLabel', background = '#e1d8b9', font = ('Arial', 11))
        self.style.configure('Header.TLabel', font = ('Arial', 18))
        self.style.configure('Timer.TLabel', font = ('Arial', 48, 'bold'), foreground = 'blue')

        # Create time and state variables 
        self.state = False
        self.minutes = 25
        self.seconds = 0
        self.bar = 0

        self.mins = 25
        self.secs = 0

        # Build the frame that contains the timer
        self.timer = ttk.Frame(master)
        self.timer.pack()

        self.display = ttk.Label(self.timer,  style = 'Header.TLabel')
        self.display.grid(row = 0, column = 0, columnspan =2, pady=(5,0))
        self.display.config(text= "Let's Get Started")
        
        self.time = ttk.Label(self.timer, style = 'Timer.TLabel')
        self.time.grid(row = 1, column = 0, columnspan=2, padx=5, pady=(5,0))
        self.time.config(text="%02d:%02d" % (self.minutes, self.seconds))

        # Create progressbar
        value = DoubleVar()
        self.progressbar = ttk.Progressbar(self.timer, orient = HORIZONTAL, length = 150)
        self.progressbar.config(mode = 'determinate', maximum = 1500)
        self.progressbar.grid(row=2, column =0, columnspan = 1, padx = 10, pady =(0,15))

        # Create buttons in a new frame
        self.controls = ttk.Frame(master)
        self.controls.pack()
        
        self.start = ttk.Button(self.controls, text = 'Start', command = self.start)
        self.start.grid(row =3, column=0, columnspan = 2, padx = 5)
        self.start.config(width=10)
        
        self.pause = ttk.Button(self.controls, text = 'Pause', command =self.pause)
        self.pause.grid(row =4, column=0, padx = 5)
        self.pause.config(state='disabled')
        self.pause.config(style = 'TButton')

        self.reset = ttk.Button(self.controls, text = 'Reset', command =self.reset)
        self.reset.grid(row =4, column=1, padx = 5)
        self.reset.config(state='disabled')
        self.reset.config(style = 'TButton')

    # Define the commands for each button
    def start(self):
        if self.state == False:
            self.state =  True
            self.display.config(text='Stay Focused')
            self.mins = self.minutes
            self.secs = self.seconds
            self.pause.config(state = 'enabled')
            self.reset.config(state = 'enabled')
            self.start.config(state='disabled')
            self.countdown()

    def pause(self):
        if self.state == True:
            self.state =  False
            self.display.config(text='Paused.')
            self.minutes = self.mins
            self.seconds = self.secs
            self.start.config(state = 'enabled')
            self.pause.config(state='disabled')

    def reset(self):
        self.minutes = 25
        self.seconds = 0
        self.time.config(text="%02d:%02d" % (self.minutes, self.seconds))
        self.start.config(state = 'enabled')
        self.pause.config(state='disabled')
        self.state = False

    # Define the alert logic          
    def break_alert(self):
        result = messagebox.askquestion("Nice job!", "Need a break?", icon='question')
        if result == 'yes':
            self.rest()            
        else:
            self.work()

            
    def work_alert(self):
        result = messagebox.askquestion("Let's jump back in", "Ready to be productive?", icon='warning')
        if result == 'yes':
            self.work()
        else:
            self.minutes = 25
            self.time.config(text="%02d:%02d" % (self.minutes, self.seconds))
            self.display.config(text= "Ready When You Are")
            self.state = False

    def work(self):
        self.minutes = 25
        self.seconds = 0
        self.mins = 25
        time_left = 0
        self.time.config(text="%02d:%02d" % (self.minutes, self.seconds))
        self.display.config(text='Stay Focused')
        self.countdown()

    def rest(self):
        self.minutes = 5
        self.seconds = 0
        self.mins = 5
        time_left = 0
        self.time.config(text="%02d:%02d" % (self.minutes, self.seconds))
        self.start.config(state = 'enabled')
        self.display.config(text='Take a quick break')
        self.countdown()

    # Define the countdown feature
    def countdown(self):
        if self.state == True:
            time_left = 1500-60*self.mins-self.secs
            self.progressbar.config(value = time_left)
            if (self.mins == 0) and (self.secs == 0) and (self.minutes != 5):
                self.mins = 0
                self.secs = 0
                self.time.config(text="%02d:%02d" % (self.mins, self.secs))
                self.break_alert()
            elif (self.mins == 0) and (self.secs == 0) and (self.minutes ==5 ):
                self.mins = 0
                self.secs = 0
                self.time.config(text="%02d:%02d" % (self.mins, self.secs))
                self.work_alert()
 
            else:
                self.time.config(text="%02d:%02d" % (self.mins, self.secs))

                if self.secs == 0:
                    self.mins -= 1
                    self.secs = 59
                    
                else:
                    self.secs -= 1


                self.master.after(1000, self.countdown)
            
        
            
def main():            
    
    root = Tk()
    focus = Focus(root)
    root.mainloop()

if __name__ == "__main__": main()
