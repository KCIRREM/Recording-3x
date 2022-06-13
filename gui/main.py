from tkinter import *

import variable
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from threading import Thread
from tkinter import messagebox
def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper

saved_options_dict = {}
button_count = -1
sound_driver_tuple = ("VB-Audio Virtual Cable","VB-Audio Cable A","VB-Audio Cable B")


root = Tk()
root.title("BBC Sounds downloader")
f = Tk.frame(root)


def set_url_label():
    global url_label
    url_label = Label(root, text=f"url = {driver.current_url}",width=50)
    url_label.grid(row=0, column=1,columnspan=9)

def reset_url_label():
    url_label.config(text = "")
    url_label.config(text = driver.current_url)
    root.after(10, reset_url_label)


def get_driver():
    global driver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get('https://www.google.com')
@run_once

def activate_confirm():
    confirm_options.configure(state=NORMAL)

@run_once
def save_url():
    save_url_button.configure(state='disabled')
    check_box1.configure(state=NORMAL)
    check_box2.configure(state=NORMAL)
    check_box3.configure(state=NORMAL)

def activate_time():
    enter_time.configure(state=NORMAL)
    confirm_time.configure(state=NORMAL)

@run_once
def active_rad():
    record_option1.configure(state=NORMAL)
    record_option2.configure(state=NORMAL)
    record_option3.configure(state=NORMAL)
    record_option4.configure(state=NORMAL)
    schedule_box.configure(state=NORMAL)
    enter_time.configure(state=DISABLED)
    confirm_time.configure(state=DISABLED)





def reset_options():
    test = []
    global button_count
    button_count = button_count + 1
    sound_drivers = [item[0] for item in zip(sound_driver_tuple, (virtual.get(), virtual_a.get(), virtual_b.get())) if item[1] == 1]
    global saved_options_dict
    saved_options_dict[button_count] = {'url':driver.current_url,'sound_drivers':sound_drivers,'record method':record_method.get(),'record time':enter_time.get(),'schedule':schedule.get()}

    confirm_options.configure(state=DISABLED)
    save_url_button.configure(state=NORMAL)
    check_box1.configure(state=DISABLED)
    check_box2.configure(state=DISABLED)
    check_box3.configure(state=DISABLED)
    enter_time.configure(state=DISABLED)
    confirm_time.configure(state=DISABLED)
    record_option1.configure(state=DISABLED)
    record_option2.configure(state=DISABLED)
    record_option3.configure(state=DISABLED)

    activate_confirm.has_run = False
    save_url.has_run = False
    active_rad.has_run = False







get_driver(),set_url_label(),reset_url_label()

virtual = IntVar()
virtual_a = IntVar()
virtual_b = IntVar()
record_method = StringVar()
schedule = StringVar()

confirm_options = (Button(root,text="Confirm",state=DISABLED,command=reset_options))
confirm_options.grid(row=9,column=0,columnspan=1,ipadx=20)


schedule_box = Checkbutton(root,text="Schedule",variable=schedule,onvalue="yes",offvalue="no",state=DISABLED,command=activate_confirm)
schedule_box.deselect()
schedule_box.grid(row=8,column=0,columnspan=1,padx=(0,20))


record_option1 = (Radiobutton(root, text="Record all episodes",variable=record_method,value="all",state=DISABLED,command=activate_confirm))
record_option1.select()
record_option1.grid(row=4,column=0,columnspan=3,padx=(0,176))

record_option2 = (Radiobutton(root, text="Record single page",variable=record_method,value="page",state=DISABLED,command=activate_confirm))
record_option2.deselect()
record_option2.grid(row=5,column=0,columnspan=3,padx=(0,178))

record_option3 = (Radiobutton(root, text="Record single episode",variable=record_method,value="episode",state=DISABLED,command=activate_confirm))
record_option3.deselect()
record_option3.grid(row=6,column=0,columnspan=3,padx=(0,162))

record_option4 = (Radiobutton(root, text="None",variable=record_method,value="none",state=DISABLED,command=activate_confirm))
record_option4.grid(row=7,column=0,padx=(0,38))

enter_time = Entry(root,width=20,borderwidth=1,state=DISABLED)
enter_time.grid(row=3,column=1,columnspan=2,padx=(0,66))
confirm_time = Button(root, text="confirm time?",state=DISABLED,command=active_rad)
confirm_time.grid(row=3,column=0,columnspan=1,ipadx=5)


check_box1 = (Checkbutton(root, text="VB-Audio Virtual Cable",variable=virtual,state=DISABLED,command=activate_time))
check_box1.grid(row=1,column=0,columnspan=2)
check_box2 = (Checkbutton(root, text="VB-Audio Cable A",variable=virtual_a,state=DISABLED,command=activate_time))
check_box2.grid(row=1,column=2,columnspan=1)
check_box3 = (Checkbutton(root, text="VB-Audio Cable B",variable=virtual_b,state=DISABLED,command=activate_time))
check_box3.grid(row=1,column=3,columnspan=1)

save_url_button = Button(root, text="save url?",command=lambda : (save_url()))
save_url_button.grid(row=0,column=0,columnspan=1,ipadx=20)






root.mainloop()

print(saved_options_dict)
#print()