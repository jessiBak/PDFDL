#!/usr/bin/python3


from tkinter import *
from tkinter import filedialog
import tkinter.scrolledtext as ScrolledText
from bs4 import BeautifulSoup
import sys
import time
import requests
from requests.exceptions import HTTPError
import os.path
import platform
import re
#from io import *
#from contextlib import redirect_stdout
'''
Created by Jessica Bakare 

A program that searches a given website for pdf links and downloads all pdfs found to a given directory. Has a GUI, so command
line isn't needed to run it. 

How to use: When program starts, choose the directory you want to save the file to (make sure to double click!),
then minimize and unminimize the window and enter the website's url. Then press "Start!" button.

If you get an error, you may need to pip3 install python3-tk or sudo apt-get install python3-tk or 
however you can get tkinter for python3
'''
#method that takes in a website's html text and the website's url and returns a list of pdf links found on it
def getLinks(html, url):
    linkLst = []
    soup = BeautifulSoup(html, "html.parser")
    for link in soup.find_all('a', href = True):
        l = str(url[:url.rfind("/") + 1] + link.get('href'))
        if ".pdf" in l:#remove this conditional statement to just add any links to list
            linkLst.append(l)
            out = "Found link: " + l
            infoWin.insert(INSERT, out)
            print(out)
    return linkLst
        
#method that takes website and path retrieved from tkinter Entry widgets to find and download pdf files
def dl():
        try:
            #***Finding links to PDFs:***
            web = wEntry.get()
            pa = str(path)
            r = requests.get(web)
            html = r.text
            s = BeautifulSoup(html, "html.parser")
            #print("Here is web html soup: ")
            #print(s.prettify())
            #Create list of links to pdf files found
            links = []
            # make a list of .html original website first, then search for frames:
            
            #search initial given website fo links
            links = links + getLinks(html, web) #this won't add anything if the pdf links are in html files found in frames/iframes, so...
            
            #get html found in frames and iframes:
            frames = []
            fs = s.find_all(['frame', 'iframe'])
            #print("fs:")
            #print(fs)
            #print("\n\n\n")
            for fr in fs:
                frames.append(str(web[:web.rfind("/") + 1] + fr.get('src')))
                
            #print("Here are the frames found: ")
            #print(frames)
                
            #find the pdf links in each url and add it to the list of links
            for url in frames:
                req = requests.get(url)
                h = req.text
                #print("Here is the text of a frame " + url + ":")
                #print(h)
                #print("\n\n\n\n\n")
                links = links + getLinks(h, url)
            
            #print("Here are all the links found:", file = output)
            #print(links, file = output)
            
            #***Downloading the PDFs:***
            for link in links:
                if not links:
                    #out = "No pdf file links found."
                    #info.insert(END, out)
                    time.sleep(3)
                    out = "No pdf file links found."
                    infoWin.insert(INSERT, out)
                    print("No pdf file links found.")
                    break
                out = "Downloading from " + link + "..."
                infoWin.insert(INSERT, out)    
                print("Downloading from " + link + "...")
                filename = link[link.rfind("/") + 1:]
                out = "Saving as " + filename
                infoWin.insert(INSERT, out)
                print("Saving as " + filename)
                fi = requests.get(link)
                fullPath = os.path.join(pa, filename)
                #print("The full path is: " + str(fullPath))
                with open(fullPath, "wb") as pdf:
                    pdf.write(fi.content)
            #out = "Done!"
            #infoWinTxt.set(out)
            #info.insert(END, out)
            out = "Done!"
            infoWin.insert(INSERT, out)
            print("Done!")
            time.sleep(3)
            root.destroy()#Close window when download complete
            
            #output.close()
            
        except HTTPError as err:
            print("Oh no! an HTTP error has occurred:")
            print(err)
            
        except Exception as e:
            print("Oh no! Something went wrong:")
            print(e)

            
                

#***Creating a GUI to make this PDF Downloader more user friendly***
root = Tk()
root.title("PDF Downloader")


label1 = Label(root, text = "PDF File Downloader")

label2 = Label(root, text = "Enter website url: ")
wEntry = Entry(root)

label3 = Label(root, text = "Files are being saved to:")
path = os.path.normpath(filedialog.askdirectory(parent = root))

label7 = Label(root, text = str(path))

label4 = Label(root, text = " ")
label5 = Label(root, text = " ")
label6 = Label(root, text = " ")



#Here is where print outputs should be going......

#output = StringIO()
#contents = output.getvalue()
#print("Here is what is in the string stream when initialized:")
#print(contents)
infoWin = ScrolledText.ScrolledText(root, width = 30, height = 8)
#infoWin.configure(state = 'disabled')


#Put them on the screen

label1.pack()
label4.pack()
label5.pack()
label6.pack()
label2.pack()
wEntry.pack()
wEntry.focus()
label3.pack()
label7.pack()


startButton = Button(root, text = "Start!", command = dl)
startButton.pack()


infoWin.pack()
root.mainloop() 

