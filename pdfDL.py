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

'''
Created by Jessica Bakare 

A program that searches a given website for pdf links and downloads all pdfs found to a given directory. Has a GUI, so command
line isn't needed to run it. 

How to use: When program starts, choose the directory you want to save the file to (make sure to double click!),
then minimize and unminimize the window and enter the website's url. Then press "Start!" button.

If you get an error, you may need to pip3 install python3-tk or sudo apt-get install python3-tk or 
however you can get tkinter for python3
'''


#Method to show a message in the ScrolledText widget
def msg(message):
    m = message + "\n"
    infoWin.insert('end', m)
    infoWin.see('end')
    root.after(200, root.update())

#method that takes in a website's html text and the website's url and returns a list of pdf links found on it
def getLinks(html, url):
    linkLst = []
    soup = BeautifulSoup(html, "html.parser")
    for link in soup.find_all('a', href = True):
        l = str(url[:url.rfind("/") + 1] + link.get('href'))
        if ".pdf" in l:#remove this conditional statement to just add any links to list
            linkLst.append(l)
            out = "Found link: " + l
            msg(out)
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

            #Create list of links to pdf files found
            links = []
            
            # make a list of .html original website first, then search for frames:
            #search initial given website fo links
            
            links = links + getLinks(html, web) #this won't add anything if the pdf links are in html files found in frames/iframes, so...
            
            #get html found in frames and iframes:
            frames = []
            fs = s.find_all(['frame', 'iframe'])
            for fr in fs:
                frames.append(str(web[:web.rfind("/") + 1] + fr.get('src')))
                
            #find the pdf links in each url and add it to the list of links
            for url in frames:
                req = requests.get(url)
                h = req.text
                links = links + getLinks(h, url)
            
            #***Downloading the PDFs:***
            for link in links:
                if not links:
                    out = "No pdf file links found."
                    msg(out)
                    print("No pdf file links found.")
                    break
                out = "Downloading from " + link + "..."
                msg(out)
                root.update()
                print("Downloading from " + link + "...")
                filename = link[link.rfind("/") + 1:]
                out = "Saving as " + filename
                msg(out)
                print("Saving as " + filename)
                fi = requests.get(link)
                fullPath = os.path.join(pa, filename)
                #print("The full path is: " + str(fullPath))
                with open(fullPath, "wb") as pdf:
                    pdf.write(fi.content)
            out = "Done!"
            msg(out)
            print("Done!")
            root.after(10000, root.destroy())#Close window when download complete
            
        except HTTPError as err:
            print("Oh no! an HTTP error has occurred:")
            print(err)
            
        except Exception as e:
            print("Oh no! Something went wrong:")
            print(e)

            
             
#***Creating a GUI to make this PDF Downloader more user friendly***
root = Tk()
root.title("PDF Downloader")
root.geometry("500x600")


label1 = Label(root, text = "PDF File Downloader")

label2 = Label(root, text = "Enter website url: ")
wEntry = Entry(root)

label3 = Label(root, text = "Files are being saved to:")


path = os.path.normpath(filedialog.askdirectory(parent = root, initialdir= os.path.expanduser("~")))

#if no directory is chosen, files are saved to Downloads directory
if path == "" or path == "." or path == "-":
    p = os.path.expanduser('~')
    path = os.path.join(p, "Downloads")


label7 = Label(root, text = str(path))

label4 = Label(root, text = " ")
label5 = Label(root, text = " ")
label6 = Label(root, text = " ")


infoWin = ScrolledText.ScrolledText(root, width = 70, height = 10)


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


