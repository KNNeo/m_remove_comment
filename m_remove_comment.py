#Objective: To remove all comments in MATLAB .m files
#Introduction: Comments in MATLAB can come in two forms
# % for inline, %{ and %} for multiple lines
#Process:
#(1) read .m file as binary maybe, decode as ascii string
#(2) replace strings between multiple line symbols AND/OR % and newline char
#(3) write back file (as new file probably) as binary, from ascii string
#Optimisation:
# Read file from open file dialog
# Can secretly work with MATLAB related files, thus 'all files' category
# Packaged into executable to work on Windows

import subprocess, re
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select .m file",filetypes = (("m files","*.m"),("all files","*.*")))
directory = root.filename
#print(directory)

with open(root.filename,'rb') as mfile:
    string = mfile.read().decode('ascii')
    #print(string)
    answer = ''

    #while loop on full string
    while string.find("%") != -1:
        temp = string[string.find("%")+1:]
        #print('temp:',temp)
        #if temp.find("\r\n") != -1:
            #print('comment')
        if temp.find("%") != -1:
            temp2 = temp[temp.find("\r\n"):temp.find("%")]
            #print('temp2:',temp2)
            answer = answer+temp2
            #print('content')
        else:
            #print('end content')
            temp2 = temp[temp.find("\r\n"):]
            answer = answer+temp2
        string = temp[temp.find("%"):]
    #remove consecutive whitespaces, even with tabs
    while re.search("\r\n {2,5}\r\n",answer) != None:
        answer = re.sub("\r\n {1,5}\r\n","\r\n",answer)
    #remove paragraph whitespaces, assume tabs taken care of
    answer = re.sub("(\r\n){2,5}","\r\n\r\n",answer)
    #remove initial comment whitespace
    while answer.find("\r\n") == 0:
        answer = answer[2:]
        
    #print('answer:',list(answer))

    filename = directory[:directory.rfind(".m")]
    
    with open(filename+'_new.m','wb') as newfile:
        newfile.write(answer.encode('ascii'))

directory = directory[:directory.rfind("/")+1]
#print(directory)
command = r'explorer /select,"' + directory + '"'
command = command.replace("/","\\")
#print(command)

subprocess.Popen(command)
                                   
#Unresolved Problems:
# Newline characters will appear in excess; has been surpressed in program
