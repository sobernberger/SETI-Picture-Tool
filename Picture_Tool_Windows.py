import os
import glob
from tkinter import filedialog
import tkinter as tk
from tkinter import Button
from PIL import ImageTk, Image
import numpy as np
import csv

class ImageViewer(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.state('zoomed')
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.images = None

        
        
        self.image, wh, ht, self.filename = self.open_file()
        self.canvas = tk.Canvas(self.root, width=wh, height=ht, bg='black')
        self.canvas.pack(expand=tk.YES)
        self.image_on_canvas = self.canvas.create_image(self.width/2, self.height/2, anchor=tk.CENTER, image=self.image)

        yes = Button(self.root, text='Hit', command=self.yes, width=15, height=4, bg='green')
        no = Button(self.root, text='RFI', command=self.no, width=15, height=4, bg='red')
        skip = Button(self.root, text='Skip', command=self.skip, width=15, height=4, bg='yellow')
        yes.place(x=50, y=100)
        no.place(x=50, y = 40)
        skip.place(x= 50, y= 200)

        self.root.mainloop()

    def open_file(self):
        openfile = filedialog.askopenfilename(initialdir='/Users/sebastian/Documents/SETIsurvey', title='Select image', filetypes=(('png files', '*.png'), ('all files', '*.*')))
        print(os.path.dirname(openfile))
        files =next(os.walk(os.path.dirname(openfile)), (None, None, []))[2] 
        
        self.images = []
        
        for file in files:
            if file.endswith(".png"):
                self.images.append(os.path.dirname(openfile)+'/'+file)
        self.images.remove(openfile)
        self.root.title(openfile)

        img = Image.open(openfile)
        filename = img.filename
        img.thumbnail((self.width, self.height), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        
        return img, self.width, self.height, filename

    def no(self):
        g = open('rfi.csv', 'a')
        writer = csv.writer(g)
        writer.writerow([self.filename])
        g.close()
        print(self.filename)
        os.remove(self.filename)
        if not self.images:
            self.root.destroy()
            print('done')
            return
            #img, wh, ht = self.open_file()
        else:
            
            image = self.images.pop(0)
            self.filename = image
            self.root.title(image)
            img = Image.open(image)
            img.thumbnail((self.width, self.height), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
        
        
        self.canvas.itemconfigure(self.image_on_canvas, image=img)
        self.canvas.config(width=self.width, height=self.height)
        try:
            self.canvas.wait_visibility()
        except tk.TclError:
            pass


    def yes(self):
        f = open('hits.csv', 'a')
        writer = csv.writer(f)
        writer.writerow([self.filename])
        f.close()
        print(self.filename)
        os.remove(self.filename)
        if not self.images:
            self.root.destroy()
            print('done')
            return
            #img, wh, ht = self.open_file()
        else:
            
            image = self.images.pop(0)
            self.filename = image
            self.root.title(image)
            img = Image.open(image)
            img.thumbnail((self.width, self.height), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
        
        
        self.canvas.itemconfigure(self.image_on_canvas, image=img)
        self.canvas.config(width=self.width, height=self.height)
        try:
            self.canvas.wait_visibility()
        except tk.TclError:
            pass


    def skip(self):
        if not self.images:
            img, wh, ht = self.open_file()
        else:
            image = self.images.pop(0)
            self.root.title(image)
            img = Image.open(image)
            img.thumbnail((self.width, self.height), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
        self.canvas.itemconfigure(self.image_on_canvas, image=img)
        self.canvas.config(width=self.width, height=self.height)
        try:
            self.canvas.wait_visibility()
        except tk.TclError:
            pass



ImageViewer()