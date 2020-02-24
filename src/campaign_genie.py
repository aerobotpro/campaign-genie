import smtplib
from config import *
from tkinter import *
from tkinter import filedialog
import tkinter as tk
from os import getcwd
import webbrowser
from datetime import datetime
from time import sleep

#Wider scoped circuitry: -> Global -> Input -> Get Value[or fail to] -> Repeat
class glbls:
    list_fname = None
    notification = None # Dont flush!
    send_list = list
    smtp_host = None
    smtp_port = None
    sender_email = None
    sender_pass = None
    recvr_email = None
    subject = None
    body = None
    body_string = str()
    logging_current = str()
    logging_universal = str() # Dont flush!

class inputs:
    list_fname = None
    smtp_host = None
    smtp_port = None
    sender_email = None
    sender_pass = None
    subject = None
    body = None

def flush_inputs():
    inputs.list_fname = None
    inputs.smtp_host = None
    inputs.smtp_port = None
    inputs.sender_email = None
    inputs.sender_pass = None
    inputs.subject = None
    inputs.body = None    
    
def flush_glbls():
    glbls.list_fname = None    
                                    #
    glbls.send_list = list
    glbls.smtp_host = None
    glbls.smtp_port = None
    glbls.sender_email = None
    glbls.sender_pass = None
    glbls.subject = None
    glbls.body = None
    glbls.logging_current = str()
                                         #    



def update_log(input_):
    glbls.logging_universal = glbls.logging_universal + f"\n\n[{datetime.now()}] - {input_}"
    

#CLIENT PIPELINE/WORKER
class client:
    def __init__(self, smtp_host, smtp_port, sender_email, sender_pass, mailing_list, subject, body):

        #UPDATE LIST
        try: glbls.send_list = open(glbls.list_fname, "r").read().split('\n')
        except Exception as d:
            glbls.send_list = list
            update_log(d)
            recover(glbls.logging_universal)
            return

            


        
        #Create Object Of Our SMTP Server
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_host, smtp_port, context=context) as server:
            #Try To Reach/Login To Our SMTP Server
            try: server.login(sender_email, sender_pass)
            
            except Exception as er:
                ## If Failed::Revert to initial start screen
                glbls.notification = f"[{glbls.send_list[x]}] - Failed To Send -> -> ->X\n[Error: {er}]"
                glbls.logging_current += glbls.notification
                recover(glbls.logging_universal)
                return

            #If ok:
            
            #Begin Send Loop
            for x in range(0, len(glbls.send_list)):

                #Create Message For This Index
                message = str(
                    f"""\
                    Subject: {subject}
                    To: {glbls.send_list[x]}
                    From: {sender_email}

                    {body}
                    
                    *This is an automated email, please do not reply.*
                    """
                    )
                #Try sending...    
                try:
                    server.sendmail(sender_email, glbls.send_list[x], message)

                #If failed..    
                except Exception as send_failed:
                    glbls.notification = f"[{glbls.send_list[x]}] - Failed To Send -> -> ->X\n[Error: {send_failed}]"

                sleep(10)    

                # UPDATE UI!!!    
                # Todo!
            glbls.logging_universal += "\n{sender_}Sending Complete!" 

                    
        #When Complete, saves session to universal logging then refreshes for next session or close.
        #Flushes all variables and drops the allocated junk from the stack (I think*) would love for someone with more low-level 
        #- knowledge to tap in. :)    
        def pop_and_drop():
            glbls.logging_universal = glbls.logging_universal + glbls.logging_current
            flush_glbls()
        pop_and_drop()
        recover(glbls.logging_universal)    


#ACTIONS: GET VALUES
def start():
    #
    #Static flow here, simple and overdone but explicit :)
    #
    #Assign/update input values from our ui to the backend variables
    glbls.smtp_host = str(inputs.smtp_host.get())
    glbls.smtp_port = int(inputs.smtp_port.get())
    glbls.sender_email = str(inputs.sender_email.get())
    glbls.sender_pass = str(inputs.sender_pass.get())
    glbls.list_fname = str(inputs.list_fname)

    #UPDATE LIST
    try: glbls.send_list = open(glbls.list_fname, "r").read().split('\n')
    except Exception as d:
        glbls.send_list = list
        update_log(d)
        recover(glbls.logging_universal)
        return
    glbls.subject = str(inputs.subject.get())
    glbls.body = glbls.body_string

    #Start the client...
    try:
        client(
            glbls.smtp_host,
            glbls.smtp_port,
            glbls.sender_email,
            glbls.sender_pass,
            glbls.send_list,
            glbls.subject,
            glbls.body
            )
    except Exception as d:
        #debugging::print(d)
        recover(d)        

           
def initialize(message=None):
    #PURPOSE:
    # If initial run: setup ui,
    # If not:
    #  Flush last session + Setup UI for rerun capability
    flush_glbls()
    
    #SET ICON / TILE
    master.iconbitmap(f'{getcwd()}\\img\\fav.ico')
    master.title("CampaignGenie")
    master.configure(bg='grey')
    

    #SET HEADER IMG - BG
    tk.Label(master, image=bg_image).grid(row=0, column=0)
    #tk.Label(master, image=bg_image).grid(row=0, column=1)

    #SET HEADER LEGEND - FG
    tk.Label(master, text="Legend", bg="black",fg='red').grid(row=1, column=0)  
    tk.Label(master, text="Entry", bg="black",fg='red').grid(row=1, column=1)    

    #INPUT LABELS Schema: LABEL->ENTRY->PLACEMENT
    tk.Label(master, text="SMTP Server", bg="grey").grid(row=2)

    # SMTP HOST SERVER - CREATE DROPDOWN
    mainframe = Frame(master)
    mainframe.grid(column=1,row=2, sticky=(N,W,E,S) )
    mainframe.columnconfigure(0, weight = 1)
    mainframe.rowconfigure(0, weight = 1)
    
    inputs.smtp_host = StringVar(master)
    inputs.smtp_host.set('smtp.gmail.com') # set the default option - most common: smtp.gmail
    
    popupMenu = OptionMenu(mainframe, inputs.smtp_host, *lists.smtp_common)
    popupMenu.grid(row = 1, column =1)
    
    def get_dropdown_val(*args):
        inputs.smtp_host.get()
        
    # link function to change dropdown
    inputs.smtp_host.trace('w', get_dropdown_val)        


    #ENTER PORT - DEFAULT: 
    tk.Label(master, text="SMTP Port", bg="grey").grid(row=3)
    inputs.smtp_port = tk.Entry(master) #input 2
    inputs.smtp_port.grid(row=3, column=1)
    inputs.smtp_port.insert(END, '587')


    #ENTER EMAIL
    tk.Label(master, text="Sender Email", bg="grey").grid(row=4)
    inputs.sender_email = tk.Entry(master) #input 3
    inputs.sender_email.grid(row=4, column=1)

    #ENTER PASS
    tk.Label(master, text="Sender Pass", bg="grey").grid(row=5)
    inputs.sender_pass = tk.Entry(master) #input (password) 4
    inputs.sender_pass.grid(row=5, column=1)






    #SELECT MAILING LIST FILE
    btn_text = tk.StringVar()
    tk.Label(master, text="Mailing List", bg="grey").grid(row=6)
    
    def open_file_browser():
        inputs.list_fname = filedialog.askopenfilename(initialdir = "/",title = "Select Mailing List (.txt) / 1 per-line.",filetypes = (("Text File","*.txt"),("all files","*.*")))
        
    a = tk.Button(master, text="File Browser", command=open_file_browser)
    a.grid(row=6, column=1)
    


    #ENTER EMAIL SUBJECT
    tk.Label(master, text="Subject", bg="grey").grid(row=7)
    inputs.subject = tk.Entry(master) #input 6
    inputs.subject.grid(row=7, column=1)


    #ENTER EMAIL BODY - LARGE ENTRY - NEW WINDOW
    tk.Label(master, text="Body", bg="grey").grid(row=8)

    

        
    def txt_editor():
        #SETUP TEXT EDITOR
        editor = tk.Toplevel(master)
        editor.geometry("420x420")
        editor.title("Campaign Genie - Text Editor - Body")
        
        #GET VALUE LATER- (*)
        def use_current_text():
            inputs.body = text    

        #SAVE BUTTON
        a = tk.Button(editor, text="Save", command=use_current_text, justify=LEFT)
        a.grid(row=0, column=0)

        #EDITOR

        text = Text(editor).grid(row=1)
        
        editor.mainloop()
        
        
        
    b = tk.Button(master, text="Open Text Editor", command=txt_editor)
    b.grid(row=8, column=1)
    #inputs.body = tk.Text(master) #input (Large with markdown capability) 7
    #inputs.body.grid(row=8, column=0)


    #TOP SET OF LINE's (=)
    tk.Label(master, text="""===============""", bg="grey"
             ).grid(row=12)
    tk.Label(master, text="""===============""", bg="grey"
             ).grid(row=12, column=1)

    b = tk.Button(master, text="Start Campaign", command=start)
    b.grid(row=13, column=0)

    c = tk.Button(master, text="Info", command=info)
    c.grid(row=13, column=1)


    #LOGGING 
    #Write Current Log Message
    f = Frame(master, height=12, width=6)
    f.grid(row=15, column=0)
    
    if glbls.logging_universal != None:
        lab = tk.Label(f, text=f"Logging:\n{glbls.logging_universal}",justify=LEFT, bg="grey", fg="red")
        lab.pack_propagate(0)
        lab.pack()
    

    #BOTTOM SET OF LINE's (=)
    tk.Label(master, text="""===============""", bg="grey"
             ).grid(row=14)
    tk.Label(master, text="""===============""", bg="grey"
         ).grid(row=14, column=1)

     
def recover(message=None):
    if message == None: message = glbls.notification
    initialize(glbls.logging_universal)

def info():
    try:webbrowser.open('https://github.com/aerobotpro/campaign-genie/tree/master#campaign-genie')
    except Exception as d:
        update_log(f"Failed To Open Webbrowser: {d}")


master = tk.Tk()
master.geometry("300x420")
bg_image = PhotoImage(file=getcwd()+"\\img\\bg.png")
initialize()
master.mainloop()
